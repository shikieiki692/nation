# -*- coding: utf-8 -*-
import sys
import fitz

for pdf, rng in [
    (r"06-外部资料导入/OCR/chemy/第39届HiChO化学奥林匹克(初赛)模拟试题 1 参考答案 v1.2..pdf", range(0, 3)),
    (r"06-外部资料导入/OCR/01-题目/2026年化英社五一物化班/2026年化英社五一物化班/华英社 物化专题 2026五一期间/第40届决赛模拟试题2答案（清晰版）.pdf", range(0, 20)),
]:
    print('=' * 100)
    print(pdf.split('/')[-1])
    with fitz.open(pdf) as d:
        for i in rng:
            if i >= d.page_count:
                break
            t = d[i].get_text()
            print('--- p%d  len=%d ---' % (i + 1, len(t)))
            if t.strip():
                print(t[:1500])
