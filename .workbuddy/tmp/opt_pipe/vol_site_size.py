# -*- coding: utf-8 -*-
r"""卷内低清图 × 站点配对图 的实际尺寸对比（只读）。"""
import json, io, os, re, glob
from PIL import Image
os.chdir(r'C:\Obsidion\妙妙屋')
IMGDIRS = [r for r, d, f in os.walk('04-题库') if os.path.basename(r) == 'images']
SITE = '.workbuddy/tmp/chemy_site/assets_all'
if not os.path.isdir(SITE):
    SITE = '.workbuddy/tmp/chemy_site'

def find(name):
    b = os.path.basename(name)
    for d in IMGDIRS:
        p = os.path.join(d, b)
        if os.path.isfile(p):
            return p
    return None

mf = {}
for x in json.load(io.open('.workbuddy/tmp/chemy_site/img_match_final.json', encoding='utf-8')):
    mf.setdefault(os.path.basename(x.get('lib_img', '')), x)

rows = {}
for V in ['X', 'XI', 'XIp', 'XIV', 'XV', 'XVI', 'XVII']:
    for tag in ['学生版', '答案版']:
        md = '04-题库/初赛模拟卷%s（非有机·%s）.md' % (V, tag)
        if not os.path.isfile(md):
            continue
        for m in re.finditer(r'!\[\[([^\]]+)\]\]', io.open(md, encoding='utf-8-sig').read()):
            b = os.path.basename(m.group(1))
            rows.setdefault(b, set()).add(V)

print('%-5s %-5s | %-6s %-6s | %s' % ('libW', 'libH', 'siteW', 'siteH', '卷'))
cnt = {'bigger': 0, 'same': 0, 'nosize': 0}
for b, vols in rows.items():
    if b not in mf:
        continue
    fp = find(b)
    if not fp:
        continue
    lw, lh = Image.open(fp).size
    if lw >= 500:
        continue
    e = mf[b].get('e2') or mf[b].get('e1')
    g = glob.glob(os.path.join(SITE, e)) if e else []
    if not g:
        print('%-5d %-5d | %-6s %-6s | %s (站点图缺失)' % (lw, lh, '?', '?', ','.join(sorted(vols))))
        cnt['nosize'] += 1; continue
    sw, sh = Image.open(g[0]).size
    tag = '站点更大' if sw > lw * 1.15 else ('相当' if sw >= lw * 0.85 else '站点更小')
    cnt['bigger' if tag == '站点更大' else ('same' if tag == '相当' else 'small')] = cnt.get('bigger' if tag == '站点更大' else ('same' if tag == '相当' else 'small'), 0) + 1
    print('%-5d %-5d | %-6d %-6d | %s  %s' % (lw, lh, sw, sh, tag, ','.join(sorted(vols))))
print()
print('统计：', cnt)
