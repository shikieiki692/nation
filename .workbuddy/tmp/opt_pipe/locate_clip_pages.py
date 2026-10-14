# -*- coding: utf-8 -*-
"""定位高疑「被裁切」单元格的页号（匹配率 <70%），供定向目检。"""
import os, re, glob, zipfile
import fitz

ROOT = r"C:\Obsidion\妙妙屋"
DOCX_DIR = os.path.join(ROOT, '00-首页', '题组Word', '初赛模拟卷', '真题版式')
PDF_ROOT = os.path.join(ROOT, '.workbuddy', 'tmp', 'opt_pipe', 'render_gate_out')


def norm(s):
    return re.sub(r'[\s\u00a0]+', '', s)


def cell_texts(docx_path):
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


def longest_prefix(a, b):
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if a[:mid] in b:
            lo = mid
        else:
            hi = mid - 1
    return lo


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
    doc = fitz.open(pdfs[0])
    pages = [norm(pg.get_text()) for pg in doc]
    full = '\n'.join(pages)
    for ti, t in cell_texts(docx):
        n = norm(t)
        if len(n) < 5 or n in full:
            continue
        r = longest_prefix(n, full) / len(n)
        if r >= 0.70:
            continue
        pgno = next((i + 1 for i, p in enumerate(pages) if n[:max(3, len(n) // 3)] in p), None)
        print('%s' % name)
        print('   表%-2d 匹配率%.0f%% 页%s  ｜ docx: %s' % (ti, r * 100, pgno, t[:50]))
    doc.close()
