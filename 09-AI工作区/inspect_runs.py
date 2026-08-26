# -*- coding: utf-8 -*-
import re
from docx import Document
from docx.oxml.ns import qn

SRC = r"C:/Users/蕾赛/Desktop/第一轮-4.5小时综合测试（A卷+B卷）最终.docx"
d = Document(SRC)

q_pat = re.compile(r'^(\d+)\.')
targets = [3, 214, 210, 12, 75, 248]
for idx in targets:
    p = d.paragraphs[idx]
    print(f"\n--- PARA {idx} text={p.text[:30]!r} ---")
    for j, r in enumerate(p.runs):
        bold = r.font.bold
        print(f"  run{j}: bold={bold!s:5} text={r.text!r}")
    # also check tables for numbers? skip
