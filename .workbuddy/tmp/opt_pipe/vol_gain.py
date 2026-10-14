# -*- coding: utf-8 -*-
r"""对「卷内低清图 × 站点图」算裁剪到墨迹框后的真实宽度增益（复刻并行会话 TH=200/PAD=8）。"""
import json, io, os, re, glob
import numpy as np
from PIL import Image
os.chdir(r'C:\Obsidion\妙妙屋')
IMGDIRS = [r for r, d, f in os.walk('04-题库') if os.path.basename(r) == 'images']
SITE = '.workbuddy/tmp/chemy_site/assets_all'
if not os.path.isdir(SITE):
    SITE = '.workbuddy/tmp/chemy_site'
TH, PAD = 200, 8

def find(name):
    b = os.path.basename(name)
    for d in IMGDIRS:
        p = os.path.join(d, b)
        if os.path.isfile(p):
            return p
    return None

def ink_bbox(fp, th=TH):
    a = np.asarray(Image.open(fp).convert('L'))
    m = a < th
    if not m.any():
        return a.shape[1], a.shape[0]
    ys, xs = np.where(m)
    return int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1)

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
            rows.setdefault(os.path.basename(m.group(1)), set()).add(V)

print('%-22s %-6s %-6s %-6s %-6s %s' % ('lib', 'lib墨宽', 'lib墨高', '站墨宽', '站墨高', '增益'))
gains = []
for b, vols in rows.items():
    if b not in mf:
        continue
    fp = find(b)
    if not fp:
        continue
    w, h = Image.open(fp).size
    if w >= 500:
        continue
    lw, lh = ink_bbox(fp)
    e = mf[b].get('e2') or mf[b].get('e1')
    g = glob.glob(os.path.join(SITE, e)) if e else []
    if not g:
        continue
    sw, sh = ink_bbox(g[0])
    gain = sw / lw if lw else 0
    gains.append(gain)
    print('%-22s %-6d %-6d %-6d %-6d %.2fx  %s' % (b[:20], lw, lh, sw, sh, gain, ','.join(sorted(vols))))
if gains:
    print('\n墨迹宽增益：min %.2f / 中位 %.2f / max %.2f ｜ ≥1.15 的 %d/%d'
          % (min(gains), sorted(gains)[len(gains) // 2], max(gains), sum(1 for x in gains if x >= 1.15), len(gains)))
