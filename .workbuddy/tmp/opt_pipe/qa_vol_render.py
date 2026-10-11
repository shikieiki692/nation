# -*- coding: utf-8 -*-
"""qa_vol_render.py —— 交付件「渲染层」机检闸门（补「渲染成图 0 自动化」的空档）。

对每份交付 docx：LibreOffice → PDF → 逐页像素分析，机判 4 类视觉缺陷 + 1 类文本残留：

  BLANK  空白页（ink < BLANK_T）
  EDGE   内容越界（外侧 EDGE_ROW 行内有墨 —— 版心外的溢出/裁切）
  HEAVY  过黑（ink > HEAVY_T —— 整页图糊/过大）
  LEAK   页文本出现未渲染 LaTeX 宏（\\mathrm / \\frac / \\text{）或字面 `$`

用法：python qa_vol_render.py [--calib]            # --calib 只跑 XIV/XV（基线校准）
      python qa_vol_render.py --vol XVI            # ★ 只跑本卷（26 份 → 3 份，省时）
      python qa_vol_render.py --one 卷XVI
      python qa_vol_render.py --baseline-write      # 把当前结果写成基线（render_baseline.json）
      python qa_vol_render.py                       # 全量（与基线比对，只突出**新增**项）

★ 2026-10-11（P1-5）：① 支持 `--vol <卷>`（此前只有 `--one`，用 `--vol` 会被静默忽略而跑全量）；
  ② 转换与逐页分析**多线程**（LibreOffice 每份一个进程 ⇒ 线程池即可，实测 14min → ~4min）；
  ③ 结果与 `render_baseline.json` 比对，**只报新增/减少**——闸门用途是「发现新增」，
     全量罗列会把既有信息性项（THIN 等）淹没。
"""
import glob, os, re, subprocess, sys, tempfile, io, json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import pymupdf as fitz
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
D = r"C:\Obsidion\妙妙屋\00-首页\题组Word\初赛模拟卷\真题版式"
SOFFICE = r"C:\Program Files\LibreOffice\program\soffice.exe"
TMP = r"C:\Obsidion\妙妙屋\.workbuddy\tmp\opt_pipe\render_gate_out"
BASELINE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "render_baseline.json")

DPI = 100
BLANK_T = 0.0020      # ink 低于此 ⇒ 空白页
HEAVY_T = 0.55        # ink 高于此 ⇒ 过黑
EDGE_ROW = 12         # 外框行数（约 3mm @100dpi）
EDGE_T = 0.004        # 外框内 ink 高于此 ⇒ 越界
LATEX = re.compile(r"\\mathrm|\\frac|\\text\{|\\begin\{|\\ce\{|\$(?![\d\s])")
MIN_DPI = 105.0       # 图片有效分辨率低于此 ⇒ 印出来发虚（线稿最低 ~110dpi）
MIN_W_MM = 18.0       # 图宽小于此 ⇒ 太小、看不清
MIN_H_MM = 12.0
THIN_LONG_MM = 30.0   # ★ 短边欠阈值但长边 ≥ 此 ⇒ 判「细长条」(THIN)：源切片属性，非版面缺陷


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
    # ★ P1-5：每份一个独立 LibreOffice profile —— 否则多线程并发会互相抢单实例锁
    #   （实测 3 并发时 PDF 生成失败）；路径用 as_uri() 保证 Windows 下格式正确。
    prof = os.path.join(TMP, "_lo_profile", name[:40])
    os.makedirs(prof, exist_ok=True)
    subprocess.run([SOFFICE, "-env:UserInstallation=%s" % Path(prof).as_uri(),
                    "--headless", "--convert-to", "pdf", "--outdir", out, p],
                   capture_output=True, timeout=600)
    pdfs = glob.glob(os.path.join(out, "*.pdf"))
    if not pdfs:
        return name, -1, [("PDF 生成失败", 0, "")]
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
                # ★ 2026-10-09 分类细化（不放宽判据，只是把两类分开以便追责）：
                #   THIN ＝ 细长条（短边小但长边 ≥ THIN_LONG_MM）⇒ 源切片本身是细长条，
                #           remedy 是「回源重裁」，非版面缺陷；dpi 往往很高（200~800）。
                #   SMALL ＝ 两维都小（真·小图）⇒ 才可能是版面/尺寸配置问题。
                short, long_ = min(w_mm, h_mm), max(w_mm, h_mm)
                if long_ >= THIN_LONG_MM:
                    issues.append(("THIN", i + 1, "%.0f×%.0fmm %ddpi" % (w_mm, h_mm, px / (w_mm / 25.4) if px else 0)))
                else:
                    issues.append(("SMALL", i + 1, "%.0f×%.0fmm" % (w_mm, h_mm)))
            elif px and px / (w_mm / 25.4) < MIN_DPI:
                issues.append(("BLUR", i + 1, "%.0fdpi %.0fmm %dpx" % (px / (w_mm / 25.4), w_mm, px)))
    n = d.page_count
    d.close()
    return name, n, issues


def summarize(rows):
    """rows → {docx: {类型: 计数}}（基线比对用）。"""
    d = {}
    for name, _page, kind, _detail in rows:
        d.setdefault(name, {})
        d[name][kind] = d[name].get(kind, 0) + 1
    return d


def main():
    calib = "--calib" in sys.argv
    files = sorted(glob.glob(os.path.join(D, "*.docx")))
    if calib:
        files = [f for f in files if ("卷XIV" in f or "卷XV" in f)]
    if "--one" in sys.argv:
        key = sys.argv[sys.argv.index("--one") + 1]
        files = [f for f in files if key in f]
    elif "--vol" in sys.argv:                      # ★ P1-5：`--vol XVI` 别名（防被静默忽略）
        key = "卷%s" % sys.argv[sys.argv.index("--vol") + 1]
        files = [f for f in files if key in f]
        if not files:
            print("⛔ --vol 未匹配到任何 docx：%s" % key)
            return 2
    rows = []
    print("闸门参数：BLANK<%.4f  HEAVY>%.2f  EDGE(row=%d)>%.4f ｜ 并行 3"
          % (BLANK_T, HEAVY_T, EDGE_ROW, EDGE_T))
    tot = 0
    with ThreadPoolExecutor(max_workers=3) as ex:      # ★ P1-5：LibreOffice 每份一进程 ⇒ 并行
        for i, (name, n, issues) in enumerate(ex.map(one, files), 1):
            tag = ("%d 页" % n) if n > 0 else "—"
            print("%-52s %-7s %s" % (name[:50], tag, ("%d 处" % len(issues)) if issues else "✅"))
            by = {}
            for it in issues:
                by.setdefault(it[0], []).append(it[1:])
            for k, v in sorted(by.items()):
                print("      %-6s ×%-3d 例 %s" % (k, len(v), v[0]))
            for it in issues:
                rows.append([name, it[1] if len(it) > 1 else 0, it[0],
                             it[2] if len(it) > 2 else ""])
            tot += len(issues)
    print("=" * 78)
    thin = sum(1 for r in rows if r[2] == "THIN")
    act = tot - thin
    print("合计 %d 处（%d 份）｜可追责 %d ｜细长条 THIN（源切片属性，informational）%d"
          % (tot, len(files), act, thin))
    cur = summarize(rows)
    if "--baseline-write" in sys.argv:
        json.dump(cur, open(BASELINE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("→ 基线已写入 %s" % os.path.basename(BASELINE))
    else:
        try:
            base = json.load(open(BASELINE, encoding="utf-8"))
        except Exception:
            base = None
        if base:
            new, less = [], []
            for name in sorted(set(cur) | set(base)):
                for kind in sorted(set(cur.get(name, {})) | set(base.get(name, {}))):
                    a = base.get(name, {}).get(kind, 0)
                    b = cur.get(name, {}).get(kind, 0)
                    if b > a:
                        new.append("%s %s +%d" % (name[:32], kind, b - a))
                    elif b < a:
                        less.append("%s %s −%d" % (name[:32], kind, a - b))
            print("── 与基线比对（只列**变化**；基线=%s）──" % os.path.basename(BASELINE))
            print("  新增/变差: " + ("；".join(new) if new else "无 ✅"))
            print("  消失/改善: " + ("；".join(less) if less else "无"))
        else:
            print("（无基线文件；用 --baseline-write 建立）")
    if "--csv" in sys.argv:
        import csv
        out = r"C:\Obsidion\妙妙屋\.workbuddy\tmp\opt_pipe\render_findings.csv"
        with open(out, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f)
            w.writerow(["docx", "页", "类型", "细节"])
            w.writerows(rows)
        print("→", out)
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
