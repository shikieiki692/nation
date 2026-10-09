# -*- coding: utf-8 -*-
"""qa_vol_render.py —— 交付件「渲染层」机检闸门（补「渲染成图 0 自动化」的空档）。

对每份交付 docx：LibreOffice → PDF → 逐页像素分析，机判 4 类视觉缺陷 + 1 类文本残留：

  BLANK  空白页（ink < BLANK_T）
  EDGE   内容越界（外侧 EDGE_ROW 行内有墨 —— 版心外的溢出/裁切）
  HEAVY  过黑（ink > HEAVY_T —— 整页图糊/过大）
  LEAK   页文本出现未渲染 LaTeX 宏（\\mathrm / \\frac / \\text{）或字面 `$`

用法：python qa_vol_render.py [--calib]      # --calib 只跑 XIV/XV（基线校准）
      python qa_vol_render.py                # 全量 21 份
"""
import glob, os, re, subprocess, sys, tempfile, io
import pymupdf as fitz
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
D = r"C:\Obsidion\妙妙屋\00-首页\题组Word\初赛模拟卷\真题版式"
SOFFICE = r"C:\Program Files\LibreOffice\program\soffice.exe"
TMP = r"C:\Obsidion\妙妙屋\.workbuddy\tmp\opt_pipe\render_gate_out"

DPI = 100
BLANK_T = 0.0020      # ink 低于此 ⇒ 空白页
HEAVY_T = 0.55        # ink 高于此 ⇒ 过黑
EDGE_ROW = 12         # 外框行数（约 3mm @100dpi）
EDGE_T = 0.004        # 外框内 ink 高于此 ⇒ 越界
LATEX = re.compile(r"\\mathrm|\\frac|\\text\{|\\begin\{|\\ce\{|\$(?![\d\s])")
MIN_DPI = 105.0       # 图片有效分辨率低于此 ⇒ 印出来发虚（线稿最低 ~110dpi）
MIN_W_MM = 18.0       # 图宽小于此 ⇒ 太小、看不清
MIN_H_MM = 12.0


def ink_stats(im):
    g = im.convert("L")
    w, h = g.size
    px = list(g.getdata())
    n = len(px)
    ink = sum(1 for v in px if v < 240) / n
    # 外框
    fr = []
    for y in range(h):
        row = g.crop((0, y, w, y + 1))
        if y < EDGE_ROW or y >= h - EDGE_ROW:
            fr.append(sum(1 for v in row.getdata() if v < 240))
        else:
            l = g.crop((0, y, EDGE_ROW, y + 1))
            r = g.crop((w - EDGE_ROW, y, w, y + 1))
            fr.append(sum(1 for v in l.getdata() if v < 240) + sum(1 for v in r.getdata() if v < 240))
    border = sum(fr) / (n if h else 1)
    return ink, border


def one(p):
    name = os.path.basename(p)
    out = os.path.join(TMP, name.replace(".docx", ""))
    os.makedirs(out, exist_ok=True)
    for f in glob.glob(os.path.join(out, "*")):
        try:
            os.remove(f)
        except Exception:
            pass
    subprocess.run([SOFFICE, "--headless", "--convert-to", "pdf", "--outdir", out, p],
                   capture_output=True, timeout=600)
    pdfs = glob.glob(os.path.join(out, "*.pdf"))
    if not pdfs:
        return name, -1, [("PDF 生成失败",)]
    d = fitz.open(pdfs[0])
    issues = []
    for i in range(d.page_count):
        pg = d[i]
        pix = pg.get_pixmap(dpi=DPI)
        im = Image.open(io.BytesIO(pix.tobytes("png")))
        ink, border = ink_stats(im)
        txt = pg.get_text()
        if ink < BLANK_T:
            issues.append(("BLANK", i + 1, "ink=%.4f" % ink))
        elif ink > HEAVY_T:
            issues.append(("HEAVY", i + 1, "ink=%.4f" % ink))
        if border > EDGE_T:
            issues.append(("EDGE", i + 1, "border=%.4f" % border))
        m = LATEX.search(txt)
        if m:
            issues.append(("LEAK", i + 1, repr(txt[max(0, m.start() - 30):m.start() + 30])))
        for info in pg.get_image_info():
            bb = info.get("bbox") or (0, 0, 0, 0)
            w_mm = (bb[2] - bb[0]) / 72 * 25.4
            h_mm = (bb[3] - bb[1]) / 72 * 25.4
            px = info.get("width") or 0
            py = info.get("height") or 0
            if px and py and h_mm > 0.5:
                r_src, r_pdf = px / py, w_mm / h_mm
                if abs(r_src - r_pdf) / r_src > 0.15:
                    issues.append(("SQUASH", i + 1, "源 %d×%d(%.2f) → 版面 %.0f×%.0fmm(%.2f)"
                                   % (px, py, r_src, w_mm, h_mm, r_pdf)))
            if w_mm < MIN_W_MM or h_mm < MIN_H_MM:
                issues.append(("SMALL", i + 1, "%.0f×%.0fmm" % (w_mm, h_mm)))
            elif px and px / (w_mm / 25.4) < MIN_DPI:
                issues.append(("BLUR", i + 1, "%.0fdpi %.0fmm %dpx" % (px / (w_mm / 25.4), w_mm, px)))
    n = d.page_count
    d.close()
    return name, n, issues


def main():
    calib = "--calib" in sys.argv
    files = sorted(glob.glob(os.path.join(D, "*.docx")))
    if calib:
        files = [f for f in files if ("卷XIV" in f or "卷XV" in f)]
    if "--one" in sys.argv:
        key = sys.argv[sys.argv.index("--one") + 1]
        files = [f for f in files if key in f]
    rows = []
    print("闸门参数：BLANK<%.4f  HEAVY>%.2f  EDGE(row=%d)>%.4f" % (BLANK_T, HEAVY_T, EDGE_ROW, EDGE_T))
    tot = 0
    for i, f in enumerate(files, 1):
        name, n, issues = one(f)
        tag = ("%d 页" % n) if n > 0 else "—"
        print("%-52s %-7s %s" % (name[:50], tag, ("%d 处" % len(issues)) if issues else "✅"))
        by = {}
        for it in issues:
            by.setdefault(it[0], []).append(it[1:])
        for k, v in sorted(by.items()):
            print("      %-6s ×%-3d 例 %s" % (k, len(v), v[0]))
        for it in issues:
            rows.append([name, it[1], it[0], it[2] if len(it) > 2 else ""])
        tot += len(issues)
    print("=" * 78)
    print("合计 %d 处（%d 份）" % (tot, len(files)))
    if "--csv" in sys.argv:
        import csv
        out = r"C:\Obsidion\妙妙屋\.workbuddy\tmp\opt_pipe\render_findings.csv"
        with open(out, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f)
            w.writerow(["docx", "页", "类型", "细节"])
            w.writerows(rows)
        print("→", out)


if __name__ == "__main__":
    main()
