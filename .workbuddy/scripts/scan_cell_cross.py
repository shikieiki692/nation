# -*- coding: utf-8 -*-
r"""交付件「表格单元格文字越界/裁切」渲染级判据（advisory，与 scan_table_cell_clip.py 互补）。

背景（2026-10-15 卷 XII 实测）：
  ④-d `scan_table_cell_clip.py` 用「PDF 文字层最长前缀匹配」判裁切 —— **对
  「LibreOffice 视觉裁切但文字仍留在 PDF 文字层」的形态会漏报**（XII 3 张真裁切只报出 1 张，
  另一张热力学表 2 处越界**完全零命中**）。
  本判据改从**渲染几何**入手：文字 span 的包围盒若跨过一条**长竖线**（表格竖border），即候选。

判据：竖线长 ≥ 12pt；span 宽 ≥ 15pt；span 的 x 区间严格包含该竖线 x，且 y 中点落在竖线 y 区间内。
  ⇒ 命中＝**候选**，必须**逐处目检**定性（见下「已知假阳性」）。

已知假阳性（占比高，勿自动修）：
  · OMML 自身的竖笔画：`\left|…\right|` 绝对值、`∝`、大括号 `\left\{`、根号竖笔、`\mid` 等
    （表现为跨线 span 文本为 `'|='`／`' ⋅'`／`'||'`／`' ∝'` 等**窄符号**）。
  · 非表格区域的公式：本判据不区分「表格竖border」与「公式内部竖笔画」⇒ 页码需目检。
  收紧阈值（span ≥15pt）可滤掉绝大多数此类；放宽到 8pt 会大量误报，仅作普查用。

用法（**须用带 pymupdf 的解释器**：受管 venv）：
  python scan_cell_cross.py --vol XII
  python scan_cell_cross.py --all [--strict] [--span-min 15] [--no-render]
  期望 VERDICT: PASS（退出码 0）。命中 ⇒ 逐处裁图目检；确认真裁切后按 SOP 修
  （表格内 OMML 过宽：拆单位成纯文本 / 缩短内容 / 改纯文本 Unicode）。

白名单：`cellcross_keep.json`（同目录），key = `<卷>/<版式>/p<页>/x<竖线x>`；
  仅收「**确已 400dpi 目检**、定性为非表格 OMML 定界笔画」的项，必须写明 卷/页/日期/结论。

缓存：PDF 落在 `.workbuddy/tmp/opt_pipe/cellcross_out/<卷_版式>/`；docx 较新则自动重渲染。
"""
import os, sys, glob, subprocess, json

ROOT = r"C:\Obsidion\妙妙屋"
ZX = os.path.join(ROOT, "00-首页", "题组Word", "初赛模拟卷", "真题版式")
SOFFICE = r"C:\Program Files\LibreOffice\program\soffice.exe"
BASE = os.path.join(ROOT, ".workbuddy", "tmp", "opt_pipe", "cellcross_out")
sys.path.insert(0, r"C:\Users\蕾赛\.workbuddy\binaries\python\envs\default\Lib\site-packages")
import pymupdf

ALL_VOLS = ['X', 'XI', 'XIp', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII']
VOLS, STRICT, SPAN_MIN, NO_RENDER = [], False, 15.0, False
for i, a in enumerate(sys.argv):
    if a == '--vol' and i + 1 < len(sys.argv):
        VOLS.append(sys.argv[i + 1])
    if a == '--all':
        VOLS = ALL_VOLS
    if a == '--strict':
        STRICT = True
    if a == '--no-render':
        NO_RENDER = True
    if a == '--span-min' and i + 1 < len(sys.argv):
        SPAN_MIN = float(sys.argv[i + 1])
if not VOLS:
    print(__doc__); sys.exit(2)


def ensure_pdf(src, tag):
    out = os.path.join(BASE, tag)
    os.makedirs(out, exist_ok=True)
    pdfs = glob.glob(os.path.join(out, "*.pdf"))
    if pdfs and (NO_RENDER or os.path.getmtime(pdfs[0]) >= os.path.getmtime(src)):
        return pdfs[0]
    subprocess.run([SOFFICE, "--headless", "--convert-to", "pdf", "--outdir", out, src],
                   capture_output=True, timeout=420)
    pdfs = glob.glob(os.path.join(out, "*.pdf"))
    return pdfs[0] if pdfs else None


def scan(pdf):
    doc = pymupdf.open(pdf)
    hits, npg = [], doc.page_count
    for pi in range(npg):
        page = doc[pi]
        vx = []
        for d in page.get_drawings():
            for it in d["items"]:
                if it[0] == "l":
                    a, b = it[1], it[2]
                    if abs(a.x - b.x) < 0.4 and abs(a.y - b.y) >= 12:
                        vx.append((min(a.x, b.x), min(a.y, b.y), max(a.y, b.y)))
                elif it[0] == "re":
                    r = it[1]
                    if r.width < 1.2 and r.height >= 12:
                        vx.append((r.x0, r.y0, r.y1))
        for blk in page.get_text("dict")["blocks"]:
            if blk.get("type") != 0:
                continue
            for ln in blk["lines"]:
                for sp in ln["spans"]:
                    x0, y0, x1, y1 = sp["bbox"]
                    if x1 - x0 < SPAN_MIN:
                        continue
                    for (x, ya, yb) in vx:
                        if x0 + 1.0 < x < x1 - 1.0 and ya + 0.5 < (y0 + y1) / 2 < yb - 0.5:
                            hits.append({"page": pi + 1, "vx": round(x, 1),
                                         "span": [round(x0, 1), round(y0, 1), round(x1, 1), round(y1, 1)],
                                         "text": sp["text"][:48]})
                            break
    doc.close()
    return npg, hits


print("=" * 88)
print("单元格文字越界（跨竖线）扫描 ｜ span≥%.0fpt ｜ 命中＝候选，须目检定表" % SPAN_MIN)
print("-" * 88)
# 白名单：仅「已目检定性为非表格 OMML 定界笔画」的项
KEEP_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cellcross_keep.json")
KEEP = {}
if os.path.isfile(KEEP_PATH):
    KEEP = json.load(open(KEEP_PATH, encoding="utf-8"))
kept = []
total, nfiles = 0, 0
for v in VOLS:
    for tag in ("学生版", "答案与解析版"):
        fn = f"初赛模拟卷{v}（非有机·{tag}·真题版式）.docx"
        src = os.path.join(ZX, fn)
        if not os.path.isfile(src):
            continue
        pdf = ensure_pdf(src, f"{v}_{tag}")
        if not pdf:
            print("  !! PDF 失败", fn); continue
        n, hits = scan(pdf)
        nfiles += 1
        kept += [h for h in hits if f"{v}/{tag}/p{h['page']}/x{h['vx']}" in KEEP]
        hits = [h for h in hits if f"{v}/{tag}/p{h['page']}/x{h['vx']}" not in KEEP]
        total += len(hits)
        print("%s %-12s %2d 页  命中 %d" % ("⚠️" if hits else "✅", f"{v}/{tag}", n, len(hits)))
        for h in hits:
            print("      p%-3s 竖线x=%-7s span=%-26s %r" % (h["page"], h["vx"], str(h["span"]), h["text"]))
print("-" * 88)
print("受检 %d 份 ｜ 候选合计 %d 处 ｜ 白名单豁免 %d 处" % (nfiles, total, len(kept)))
print("VERDICT: %s" % ("PASS" if total == 0 else "WARN（逐处裁图目检定表）"))
json.dump({"span_min": SPAN_MIN, "files": nfiles, "hits": total, "kept": len(kept)},
          open(os.path.join(ROOT, ".workbuddy", "tmp", "cellcross_summary.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
sys.exit(1 if (STRICT and total) else 0)
