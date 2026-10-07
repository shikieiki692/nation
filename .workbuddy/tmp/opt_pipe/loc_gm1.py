#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""loc_gm1.py —— 对伽马「五一杭州答案1」答案册做 OCR，定位「第7题」所在页与 y。"""
import json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
import fitz
try:
    fitz.TOOLS.mupdf_display_errors(False); fitz.TOOLS.mupdf_display_warnings(False)
except Exception:
    pass
R = r"C:\Obsidion\妙妙屋"
PDF = os.path.join(R, "06-外部资料导入/OCR/01-题目/2026年五一伽马初赛模拟杭州班/试题➕答案/五一伽马杭州答案1.pdf")
LOC = os.path.join(R, ".workbuddy/tmp/opt_pipe/ocr_loc")
os.makedirs(LOC, exist_ok=True)

from rapidocr_onnxruntime import RapidOCR
ocr = RapidOCR()
doc = fitz.open(PDF)
data = []
for i in range(doc.page_count):
    pg = doc[i]
    pix = pg.get_pixmap(dpi=150)
    tmp = os.path.join(LOC, "_tmp_gm1.png"); pix.save(tmp)
    res, _ = ocr(tmp)
    blocks = []
    for box, txt, sc in (res or []):
        y = float(min(p[1] for p in box)); x = float(min(p[0] for p in box))
        blocks.append(dict(y=round(y, 1), x=round(x, 1), t=txt))
    blocks.sort(key=lambda b: (b["y"], b["x"]))
    data.append(dict(page=i + 1, w=pix.width, h=pix.height, scale=150 / 72.0, blocks=blocks))
json.dump(data, open(os.path.join(LOC, "GM_ans1.json"), "w", encoding="utf-8"), ensure_ascii=False)
doc.close()
os.remove(os.path.join(LOC, "_tmp_gm1.png"))

MARK = re.compile(r"第\s*(\d+)\s*题")
for row in data:
    hits = [(m.group(1), b["y"], b["x"], b["t"][:40]) for b in row["blocks"]
            if (m := MARK.search(b["t"].replace(" ", ""))) and len(b["t"]) <= 22]
    if hits:
        print("p%-3d 页高%-5d %s" % (row["page"], row["h"], hits))
print("(OCR 索引已存 ocr_loc/GM_ans1.json)")
