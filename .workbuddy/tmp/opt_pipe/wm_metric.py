# -*- coding: utf-8 -*-
r"""水印规模度量（校准 + 全量）。指标：中浅灰「笔画状」像素 / 深墨像素。"""
import os, io, re, glob
import numpy as np
from PIL import Image
os.chdir(r'C:\Obsidion\妙妙屋')
IMGDIRS = [r for r, d, f in os.walk('04-题库') if os.path.basename(r) == 'images']

def find(pre):
    for d in IMGDIRS:
        g = glob.glob(os.path.join(d, pre + '*'))
        if g:
            return g[0]
    return None

def metric(fp):
    a = np.asarray(Image.open(fp).convert('L')).astype(np.int16)
    dark = (a < 110).mean()
    lite = ((a >= 165) & (a <= 228)).mean()
    return dark, lite, (lite / (dark + 1e-6))

print('=== 校准 ===')
for pre, lbl in [('00c6ede6e9c62616', 'XV 圆形「化学」水印'),
                 ('4ff91afe046f91b8', '清北营教育水印'),
                 ('ee9c9692529ab6', 'XIV 装饰(书签+音符)'),
                 ('3005d9a2baf04c34', '干净晶体图'),
                 ('5fc4764497bebb', '干净结构式'),
                 ('60931edafd993448', '干净 XRD 图')]:
    fp = find(pre)
    if not fp:
        print('  %-22s 未找到' % lbl); continue
    d, l, r = metric(fp)
    print('  %-22s 深墨%.3f 中浅灰%.3f 比%.2f' % (lbl, d, l, r))

print()
print('=== 各卷规模（比 > 1.0 视为疑水印）===')
for V in ['X', 'XI', 'XIp', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII']:
    tot = 0; hit = 0
    for tag in ['学生版', '答案版']:
        md = '04-题库/初赛模拟卷%s（非有机·%s）.md' % (V, tag)
        if not os.path.isfile(md):
            continue
        names = list(dict.fromkeys(re.findall(r'!\[\[([^\]]+)\]\]', io.open(md, encoding='utf-8-sig').read())))
        for nm in names:
            fp = find(os.path.basename(nm)[:16])
            if not fp:
                continue
            try:
                d, l, r = metric(fp)
            except Exception:
                continue
            tot += 1
            if r > 1.0:
                hit += 1
    print('  %-6s 去重图 %3d ｜ 疑水印 %3d (%.0f%%)' % (V, tot, hit, 100.0 * hit / tot if tot else 0))
