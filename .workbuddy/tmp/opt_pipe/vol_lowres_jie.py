# -*- coding: utf-8 -*-
r"""卷内低清图 × 源届（找矢量源 32/33 届的机会）（只读）。"""
import os, re, io, glob
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

# 建 "图名 -> 卡路径"（只扫 chemy 卡，够用）
img2card = {}
for p in glob.glob('04-题库/2026机构初赛模拟题/**/*.md', recursive=True):
    try:
        t = io.open(p, encoding='utf-8-sig').read()
    except Exception:
        continue
    for m in re.finditer(r'!\[\[([^\]]+)\]\]', t):
        img2card.setdefault(os.path.basename(m.group(1)), p)
    for m in re.finditer(r'!\[[^\]]*\]\(([^)]+)\)', t):
        img2card.setdefault(os.path.basename(m.group(1)), p)

rows = {}
for V in ['X', 'XI', 'XIp', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII']:
    for tag in ['学生版', '答案版']:
        md = '04-题库/初赛模拟卷%s（非有机·%s）.md' % (V, tag)
        if not os.path.isfile(md):
            continue
        for m in re.finditer(r'!\[\[([^\]]+)\]\]', io.open(md, encoding='utf-8-sig').read()):
            rows.setdefault(os.path.basename(m.group(1)), set()).add(V)

jie = Counter(); vec_hits = []
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
    c = img2card.get(b, '')
    m = re.search(r'chemia|chemy|第(\d+)届', c)
    # 从卡的内容读 source 字段确定届
    j = '?'
    if c:
        t = io.open(c, encoding='utf-8-sig').read(4000)
        mm = re.search(r'第\s*(\d+)\s*届', t)
        if mm:
            j = mm.group(1)
    jie[j] += 1
    if j in ('32', '33'):
        vec_hits.append((w, h, b[:16], j, ','.join(sorted(vols))[:18]))
print('低清卷内图（267）按源届：')
for k, v in jie.most_common():
    print('  第 %-3s 届: %d' % (k, v))
print()
print('=== 来自 32/33 届（矢量源，可任意 dpi 重渲）===');
for r in sorted(vec_hits):
    print('  %dx%d %s 届%s 卷%s' % r)
print('共 %d 张' % len(vec_hits))
