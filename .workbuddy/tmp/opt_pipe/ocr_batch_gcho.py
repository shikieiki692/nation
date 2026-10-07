#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ocr_batch_gcho.py —— 批量对全部 GChO 手稿 PDF 建 OCR 定位索引（模型只加载一次）。"""
import glob, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
try:
    import fitz
    try:
        fitz.TOOLS.mupdf_display_errors(False); fitz.TOOLS.mupdf_display_warnings(False)
    except Exception:
        pass
except Exception:
    fitz = None
R = r"C:\Obsidion\妙妙屋"
ANS = os.path.join(R, "06-外部资料导入/OCR/01-题目/质心合集新/GChO模拟试题合集答案")
LOC = os.path.join(R, ".workbuddy/tmp/opt_pipe/ocr_loc")
os.makedirs(LOC, exist_ok=True)

pdfs = {}
for f in sorted(glob.glob(os.path.join(ANS, "ZCHEM-GChO*解析手稿.pdf"))):
    m = re.search(r"ZCHEM-GChO(\d+)解析手稿", os.path.basename(f))
    if m:
        pdfs[int(m.group(1))] = f
todo = [(n, f) for n, f in sorted(pdfs.items()) if not os.path.exists(os.path.join(LOC, "GChO%d.json" % n))]
only = ""
for i, a in enumerate(sys.argv):
    if a == "--only" and i + 1 < len(sys.argv):
        only = sys.argv[i + 1]
    elif a.startswith("--only="):
        only = a.split("=", 1)[1]
if only:
    sel = {int(x) for x in only.split(",") if x.strip()}
    todo = [(n, f) for n, f in todo if n in sel]
print("待 OCR %d 届" % len(todo))
if not todo:
    sys.exit(0)

from rapidocr_onnxruntime import RapidOCR
ocr = RapidOCR()
for n, f in todo:
    doc = fitz.open(f)
    data = []
    marks_total = 0
    for i in range(doc.page_count):
        pg = doc[i]
        pix = pg.get_pixmap(dpi=150)
        tmp = os.path.join(LOC, "_tmp.png"); pix.save(tmp)
        res, _ = ocr(tmp)
        blocks = []
        for box, txt, sc in (res or []):
            y = float(min(p[1] for p in box)); x = float(min(p[0] for p in box))
            blocks.append(dict(y=round(y, 1), x=round(x, 1), t=txt))
        blocks.sort(key=lambda b: (b["y"], b["x"]))
        data.append(dict(page=i + 1, w=pix.width, h=pix.height, scale=150 / 72.0, blocks=blocks))
        marks_total += sum(1 for b in blocks if re.search(r"第\s*\d+\s*题", b["t"].replace(" ", "")))
    json.dump(data, open(os.path.join(LOC, "GChO%d.json" % n), "w", encoding="utf-8"), ensure_ascii=False)
    print("  ✓ 届%-3d 页%-3d 题标记%d" % (n, doc.page_count, marks_total), flush=True)
    doc.close()
if os.path.exists(os.path.join(LOC, "_tmp.png")):
    os.remove(os.path.join(LOC, "_tmp.png"))
print("全部完成")
