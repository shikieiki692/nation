# -*- coding: utf-8 -*-
"""trim_save.py —— 裁白边后另存为卡片配图。
用法: python -X utf8 trim_save.py <src.png> <dst.jpg> [thr]
"""
import sys
from PIL import Image

src, dst = sys.argv[1], sys.argv[2]
thr = int(sys.argv[3]) if len(sys.argv) > 3 else 238
im = Image.open(src).convert('RGB')
g = im.convert('L')
mask = g.point(lambda p: 255 if p < thr else 0)
bbox = mask.getbbox()
if bbox:
    pad = 6
    b = (max(0, bbox[0] - pad), max(0, bbox[1] - pad),
         min(im.width, bbox[2] + pad), min(im.height, bbox[3] + pad))
    im = im.crop(b)
im.save(dst, quality=92)
print(dst, im.size)
