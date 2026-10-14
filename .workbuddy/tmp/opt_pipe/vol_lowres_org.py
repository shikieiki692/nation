# -*- coding: utf-8 -*-
r"""267 张低清卷内图的机构分布 + 源 PDF 可用性（只读）。"""
import os, re, io
from PIL import Image
from collections import Counter
os.chdir(r'C:\Obsidion\妙妙屋')
IMGDIRS = [r for r, d, f in os.walk('04-题库') if os.path.basename(r) == 'images']

def find(name):
    b = os.path.basename(name)
    for d in IMGDIRS:
        p = os.path.join(d, b)
        if os.path.isfile(p):
            return p
    return None

rows = {}
for V in ['X', 'XI', 'XIp', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII']:
    for tag in ['学生版', '答案版']:
        md = '04-题库/初赛模拟卷%s（非有机·%s）.md' % (V, tag)
        if not os.path.isfile(md):
            continue
        for m in re.finditer(r'!\[\[([^\]]+)\]\]', io.open(md, encoding='utf-8-sig').read()):
            rows.setdefault(os.path.basename(m.group(1)), set()).add(V)

org = Counter(); tot = 0; paths = []
for b, vols in rows.items():
    fp = find(b)
    if not fp:
        continue
    try:
        w, h = Image.open(fp).size
    except Exception:
        continue
    if w >= 500:
        continue
    tot += 1
    # 机构 = 04-题库/2026机构初赛模拟题/<org>/images/...
    parts = fp.replace('\\', '/').split('/')
    o = parts[2] if len(parts) > 3 and parts[1] == '2026机构初赛模拟题' else parts[1]
    org[o] += 1
    paths.append(fp)
print('低清（px<500）卷内图 %d 张，机构分布：' % tot)
for o, c in org.most_common():
    print('  %-14s %d' % (o, c))

print()
print('=== 各机构源材料目录是否在库 ===')
for o in org:
    cands = [
        '06-外部资料导入/OCR/' + o,
        '06-外部资料导入/OCR/chemy',
    ]
    hit = [c for c in cands if os.path.isdir(c)]
    print('  %-14s → %s' % (o, hit if hit else '(无同名目录)'))
