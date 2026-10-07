# -*- coding: utf-8 -*-
"""试裁 GChO63 第7题反应式图（多组候选，供目视挑）。"""
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
import fitz

PDF = r'C:\Obsidion\妙妙屋\06-外部资料导入\OCR\01-题目\质心合集新\GChO模拟试题合集\ZCHEM-GChO63试题.pdf'
OUT = r'C:\Obsidion\妙妙屋\.workbuddy\tmp\opt_pipe\render_out\gcho63'
doc = fitz.open(PDF)
pg = doc[7]
print('页尺寸(pt):', pg.rect)
# 候选矩形（PDF pt）
CANDS = {
    'a': (140, 605, 520, 665),
    'b': (140, 600, 540, 675),
    'c': (120, 595, 560, 690),
}
for k, r in CANDS.items():
    pix = pg.get_pixmap(dpi=320, clip=fitz.Rect(*r))
    fp = os.path.join(OUT, 'crop_%s.png' % k)
    pix.save(fp)
    print('  %s %s → %s %dx%d' % (k, r, os.path.basename(fp), pix.width, pix.height))
