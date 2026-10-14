# -*- coding: utf-8 -*-
r"""打印 XIp 三张图的前 45 行墨迹分布，确定裁剪量。"""
import os, glob
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

for pre in ['b8ea3462d5d84411963b67be129281', '2ef658182fedef4dae80a68033def5', '27e08dea23b925d7a57cf0ff777517']:
    fp = find(pre)
    a = np.asarray(Image.open(fp).convert('L'))
    ink = (a < 190).mean(axis=1)
    print('=== %s  %dx%d ===' % (pre[:16], a.shape[1], a.shape[0]))
    print('  行: ' + ' '.join('%d:%.3f' % (y, ink[y]) for y in range(0, 45, 1) if y < len(ink)))
