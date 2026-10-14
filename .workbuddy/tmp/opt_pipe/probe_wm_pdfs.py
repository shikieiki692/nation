# -*- coding: utf-8 -*-
r"""探测各机构源 PDF 的「页级水印 XObject」形态（只读）。"""
import os, glob, sys
import fitz
from collections import Counter
os.chdir(r'C:\Obsidion\妙妙屋')
ROOT = '06-外部资料导入/OCR/01-题目'

ORGS = ['清北营', '化英社', '伽马', '汇智', '壹尖', '2ChO', '一式', '方圆', 'XeChem', 'XEchem', '北斗']
for org in ORGS:
    pdfs = []
    for d in glob.glob(os.path.join(ROOT, '*')):
        if org.lower() in os.path.basename(d).lower():
            pdfs += glob.glob(os.path.join(d, '**', '*.pdf'), recursive=True)
    if not pdfs:
        print('%-8s 无 PDF' % org); continue
    # 取第一个 PDF 探形
    f = pdfs[0]
    try:
        doc = fitz.open(f)
    except Exception as e:
        print('%-8s 打不开: %s' % (org, e)); continue
    sizes = Counter()
    nwm = 0
    for i in range(min(6, doc.page_count)):
        for im in doc[i].get_images(full=True):
            sizes[(im[2], im[3])] += 1
    print('%-8s %-3d个PDF ｜ 样本「%s」%d页' % (org, len(pdfs), os.path.basename(f)[:34], doc.page_count))
    print('          内嵌图尺寸分布(前5): %s' % sizes.most_common(5))
    doc.close()
