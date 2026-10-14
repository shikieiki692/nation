# -*- coding: utf-8 -*-
r"""候选图联系表（按前缀 glob）。"""
import os, glob
from PIL import Image, ImageDraw
os.chdir(r'C:\Obsidion\妙妙屋')
IMGDIRS = [r for r, d, f in os.walk('04-题库') if os.path.basename(r) == 'images']

def find(pre):
    for d in IMGDIRS:
        g = glob.glob(os.path.join(d, pre + '*'))
        if g:
            return g[0]
    return None

CANDS = [
 '12caa4e80a9b03fd', 'a6ac38603af86101', '4ff91afe046f91b8',
 '88c72e3283681232', '3ecb6a8a1b7fd32a', '6fdcac94d2607339',
 'b8ea3462d5d84411', 'ee483295375b4030', '9831e7e81596b1a8',
 '2ef658182fedef4d', '27e08dea23b925d7', 'f380e9544b4788e5',
 '00c6ede6e9c62616', '72595a8ea67e133b', '4d09f4727126dea2',
 '3005d9a2baf04c34', 'd30ac8db123e48db',
]
CELL_W, CELL_H, COLS = 460, 360, 4
rows = (len(CANDS) + COLS - 1) // COLS
sheet = Image.new('RGB', (COLS * CELL_W, rows * CELL_H), 'white')
dr = ImageDraw.Draw(sheet)
ok = 0
for i, pre in enumerate(CANDS):
    fp = find(pre)
    if not fp:
        print('MISS', pre); continue
    im = Image.open(fp).convert('RGB')
    im.thumbnail((CELL_W - 12, CELL_H - 44))
    cx = (i % COLS) * CELL_W; cy = (i // COLS) * CELL_H
    dr.rectangle([cx, cy, cx + CELL_W - 1, cy + CELL_H - 1], outline=(200, 0, 0))
    dr.text((cx + 6, cy + 6), '#%d %s' % (i + 1, pre[:12]), fill=(200, 0, 0))
    sheet.paste(im, (cx + 6, cy + 34)); ok += 1
sheet.save('.workbuddy/tmp/opt_pipe/topcut_sheet.png')
print('saved %dx%d 贴入 %d/%d' % (sheet.size[0], sheet.size[1], ok, len(CANDS)))
