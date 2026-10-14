# -*- coding: utf-8 -*-
r"""定位「表格单元格被裁切」：比对 docx 单元格文本 与 PDF 实际渲染文本。

思路：裁切的特征是**尾部丢失** ⇒ 对每个「含 OMML 的表格单元格」，
在 PDF 全文里找其最长前缀匹配长度；匹配率 <90% 且缺失尾部 ⇒ 疑裁切。
（归一化去空格/换行；允许 PDF 数学字符与 docx 提取有少量差异。）
"""
import os, re, glob, zipfile, sys

ROOT = r"C:\Obsidion\妙妙屋"
DOCX_DIR = os.path.join(ROOT, '00-首页', '题组Word', '初赛模拟卷', '真题版式')
PDF_ROOT = os.path.join(ROOT, '.workbuddy', 'tmp', 'opt_pipe', 'render_gate_out')

import fitz   # pymupdf


def norm(s):
    s = re.sub(r'[\s\u00a0]+', '', s)
    return s


def cell_texts(docx_path):
    """返回 [(表序, 单元格文本)]，仅含 OMML 的单元格。"""
    x = zipfile.ZipFile(docx_path).read('word/document.xml').decode('utf-8')
    out = []
    for ti, tb in enumerate(re.findall(r'<w:tbl>.*?</w:tbl>', x, re.S), 1):
        for c in re.findall(r'<w:tc>.*?</w:tc>', tb, re.S):
            if '<m:oMath' not in c:
                continue
            t = ''.join(re.findall(r'<(?:w|m):t[^>]*>([^<]*)</(?:w|m):t>', c)).strip()
            if t:
                out.append((ti, t))
    return out


def pdf_text(pdf_path):
    d = fitz.open(pdf_path)
    t = '\n'.join(pg.get_text() for pg in d)
    d.close()
    return norm(t)


def longest_prefix(a, b):
    """a 在 b 中的最长前缀匹配长度。"""
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if a[:mid] in b:
            lo = mid
        else:
            hi = mid - 1
    return lo


flag = 0
checked = 0
for dp in sorted(glob.glob(os.path.join(PDF_ROOT, '初赛模拟卷*'))):
    if not os.path.isdir(dp):
        continue
    pdfs = glob.glob(os.path.join(dp, '*.pdf'))
    if not pdfs:
        continue
    name = os.path.basename(dp)
    docx = os.path.join(DOCX_DIR, name + '.docx')
    if not os.path.isfile(docx):
        continue
    pt = pdf_text(pdfs[0])
    cells = cell_texts(docx)
    bad = []
    for ti, t in cells:
        n = norm(t)
        if len(n) < 5:
            continue
        checked += 1
        if n in pt:
            continue
        lp = longest_prefix(n, pt)
        ratio = lp / len(n)
        if ratio < 0.9:
            bad.append((ti, t, ratio))
    if bad:
        flag += len(bad)
        print('■ %s' % name)
        for ti, t, r in bad:
            print('   表%-2d 匹配率%.0f%%  %s' % (ti, r * 100, t[:60]))

print('=' * 90)
print('检查 %d 个含 OMML 单元格 ｜ 疑裁切 %d' % (checked, flag))
