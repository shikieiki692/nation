# -*- coding: utf-8 -*-
r"""顶部截断扫描 v2（只读）：兼容**浅色**残字（阈值放宽到 <190）。
判据：顶带(0~5行)有墨（比例 0.006~0.45，排除实心边框）＋ 随后 ≥8 行空白 ＋ 再出主内容。"""
import os, re, io
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

def scan_one(p):
    try:
        a = np.asarray(Image.open(p).convert('L'))
    except Exception:
        return None
    if a.ndim != 2 or a.shape[0] < 40:
        return None
    ink = (a < 190).mean(axis=1)
    n = len(ink)
    topink = float(ink[0:6].max())
    if not (0.006 <= topink <= 0.45):
        return None
    # 主内容起点：从行 8 起连续 3 行 ink>0.012
    start = None
    for y in range(8, min(n, int(n * 0.15))):
        if ink[y] > 0.012 and ink[y + 1] > 0.012 and ink[y + 2] > 0.012:
            start = y; break
    if start is None:
        return None
    gap = start - 5
    if gap >= 8:
        return (round(topink, 3), start, gap, a.shape[1], a.shape[0])
    return None

hits = {}
for V in ['X', 'XI', 'XIp', 'XIV', 'XV', 'XVI', 'XVII']:
    for tag in ['学生版', '答案版']:
        md = '04-题库/初赛模拟卷%s（非有机·%s）.md' % (V, tag)
        if not os.path.isfile(md):
            continue
        t = io.open(md, encoding='utf-8-sig').read()
        for m in re.finditer(r'!\[\[([^\]]+)\]\]', t):
            nm = m.group(1)
            fp = find(nm)
            if not fp:
                continue
            r = scan_one(fp)
            if r and nm not in hits:
                hits[nm] = (V, tag, r)
print('v2 顶部截断候选：%d 张' % len(hits))
for nm, (V, tag, r) in sorted(hits.items(), key=lambda x: x[1][0]):
    print('  [%s/%s] %-30s 顶墨%.3f 起y=%d 间隔%d 尺寸%dx%d' % (V, tag, nm[:30], r[0], r[1], r[2], r[3], r[4]))
