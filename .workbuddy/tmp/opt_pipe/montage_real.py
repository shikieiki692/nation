# -*- coding: utf-8 -*-
r"""把指定图名拼成联系表（按**原始图名**查文件）。"""
import os, sys, io
from PIL import Image, ImageDraw

ROOT = r"C:\Obsidion\妙妙屋"
IMG_DIRS = [r for r, d, f in os.walk(os.path.join(ROOT, '04-题库')) if os.path.basename(r) == 'images']

NAMES = [
    ('XV-Q4', 'images/451a4e6e83d0945'),
    ('XV-Q9a', 'images/023f35336b6db2d'),
    ('XV-Q9b', 'images/809216ae313611e'),
    ('XV-Q10a', 'images/f4df0a6065155cd'),
    ('XV-Q10b', 'images/00c6ede6e9c6261'),
    ('XVI-Q10', 'images/96ea08d2500c9bd'),
    ('XI-Q16', 'images/ec25ca675cadba6'),
]
OUT = sys.argv[1] if len(sys.argv) > 1 else '.workbuddy/tmp/opt_pipe/miss_real.png'

found = []
for tag, n in NAMES:
    b = os.path.basename(n)
    hit = None
    for d in IMG_DIRS:
        # 前缀匹配（图名在卡里可能被截断显示，但文件是全名）
        for f in os.listdir(d):
            if f.startswith(b[:20]):
                hit = os.path.join(d, f); break
        if hit:
            break
    print('%-8s %s' % (tag, hit[-60:] if hit else '(未找到：%s)' % b))
    if hit:
        found.append((tag, hit))

COLS, TH, PAD = 4, 300, 10
CW = 300
rows = (len(found) + COLS - 1) // COLS
sheet = Image.new('RGB', (COLS * (CW + PAD) + PAD, rows * (TH + 26 + PAD) + PAD), 'white')
dr = ImageDraw.Draw(sheet)
for i, (tag, path) in enumerate(found):
    r, c = divmod(i, COLS)
    x = PAD + c * (CW + PAD); y = PAD + r * (TH + 26 + PAD)
    im = Image.open(path).convert('RGB')
    w, h = im.size
    im.thumbnail((CW, TH))
    sheet.paste(im, (x + (CW - im.width) // 2, y))
    dr.text((x, y + TH + 4), '%s %dx%d' % (tag, w, h), fill='black')
sheet.save(OUT)
print('saved', OUT, sheet.size)
