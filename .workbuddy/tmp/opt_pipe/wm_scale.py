# -*- coding: utf-8 -*-
r"""图内水印规模估计（只读）：中灰像素占比启发式。
校准：水印图多为「大片中灰」，纯线稿/表格图近乎二值。"""
import os, io, re
import numpy as np
from PIL import Image
os.chdir(r'C:\Obsidion\妙妙屋')
IMGDIRS = [r for r, d, f in os.walk('04-题库') if os.path.basename(r) == 'images']

def find(name):
    b = os.path.basename(name)
    for d in IMGDIRS:
        p = os.path.join(d, b)
        if os.path.isfile(p):
            return p
    return None

def gray_ratio(p):
    try:
        a = np.asarray(Image.open(p).convert('L'))
    except Exception:
        return None
    if a.ndim != 2 or a.size < 400:
        return None
    mid = ((a >= 150) & (a < 235)).mean()
    return float(mid)

# 校准样本
CAL = ['00c6ede6e9c62616', '3005d9a2baf04c34', 'b8ea3462d5d84411', '4ff91afe046f91b8']
print('=== 校准 ===')
for c in CAL:
    fp = find(c)
    print('  %s 中灰占比=%.3f' % (c, gray_ratio(fp) if fp else -1))

TH = 0.06
print()
print('=== 各卷「疑水印」图数（中灰占比 > %.2f）===' % TH)
for V in ['X', 'XI', 'XIp', 'XIV', 'XV', 'XVI', 'XVII']:
    for tag in ['学生版', '答案版']:
        md = '04-题库/初赛模拟卷%s（非有机·%s）.md' % (V, tag)
        if not os.path.isfile(md):
            continue
        t = io.open(md, encoding='utf-8-sig').read()
        names = re.findall(r'!\[\[([^\]]+)\]\]', t)
        uniq = list(dict.fromkeys(names))
        hit = 0; n = 0
        for nm in uniq:
            fp = find(nm)
            if not fp:
                continue
            g = gray_ratio(fp)
            if g is None:
                continue
            n += 1
            if g > TH:
                hit += 1
        print('  %-6s %-4s 去重图 %3d ｜ 疑水印 %3d (%.0f%%)' % (V, tag, n, hit, (100.0 * hit / n) if n else 0))
