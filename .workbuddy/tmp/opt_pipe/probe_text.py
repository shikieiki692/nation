# -*- coding: utf-8 -*-
import sys
import fitz

pairs = [
    (r"06-外部资料导入/OCR/01-题目/2026年化英社4月春季班/2026化英社 春季班试卷/11/第40届初赛模拟11（清晰版）.pdf", 4),
    (r"06-外部资料导入/OCR/01-题目/2026年化英社4月春季班/2026化英社 春季班试卷/11/第40届初赛模拟试题11答案-清晰版.pdf", 6),
]
for pdf, pno in pairs:
    with fitz.open(pdf) as d:
        t = d[pno - 1].get_text()
    print("=" * 80)
    print(pdf.split("/")[-1], "p", pno, "len(text)=", len(t))
    print(repr(t[:800]))
