# -*- coding: utf-8 -*-
"""
Targeted changes on the current Desktop exam file (preserves footers + B卷 page break):
1) A卷/B卷 volume headers: remove shading + bottom border, keep bold + centered (15pt).
2) B卷 questions: larger spacing before (8pt -> 14pt).
"""
import re
from docx import Document
from docx.oxml.ns import qn
from docx.shared import Pt

PATH = r"C:/Users/蕾赛/Desktop/第一轮-4.5小时综合测试（A卷+B卷）.docx"
d = Document(PATH)
paras = d.paragraphs

def find(pred, start=0):
    for i in range(start, len(paras)):
        if pred(paras[i]):
            return i
    return None

idx_title = find(lambda p: p.style.name == 'Heading 1' and '综合测试' in p.text)
idx_bvol  = find(lambda p: p.style.name == 'Heading 1' and p.text.strip() == 'B卷', idx_title)
assert idx_bvol is not None

def strip_special(p):
    pPr = p._p.find(qn('w:pPr'))
    if pPr is None:
        return
    for tag in ('w:shd', 'w:pBdr'):
        el = pPr.find(qn(tag))
        if el is not None:
            pPr.remove(el)
    p.alignment = 1  # CENTER
    for r in p.runs:
        r.font.bold = True

for name in ('A卷', 'B卷'):
    i = find(lambda p: p.style.name == 'Heading 1' and p.text.strip() == name, idx_title)
    if i is not None:
        strip_special(paras[i])
        paras[i].paragraph_format.space_before = Pt(6)
        paras[i].paragraph_format.space_after = Pt(8)
        print(f"Stripped special format from {name} (idx {i}); now bold+centered.")

QSTART = re.compile(r'^\d+[\.．]')
n = 0
for i in range(idx_bvol + 1, len(paras)):
    t = paras[i].text.strip()
    if QSTART.match(t):
        paras[i].paragraph_format.space_before = Pt(14)
        n += 1
print(f"B卷 questions spacing increased to 14pt: {n}")

d.save(PATH)
print("SAVED OK")
