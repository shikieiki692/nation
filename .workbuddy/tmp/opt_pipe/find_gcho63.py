# -*- coding: utf-8 -*-
"""定位 GChO63 第7题页并渲染成 PNG（供目视裁剪反应式图）。"""
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
import fitz

PDF = r'C:\Obsidion\妙妙屋\06-外部资料导入\OCR\01-题目\质心合集新\GChO模拟试题合集\ZCHEM-GChO63试题.pdf'
OUT = r'C:\Obsidion\妙妙屋\.workbuddy\tmp\opt_pipe\render_out\gcho63'
os.makedirs(OUT, exist_ok=True)
doc = fitz.open(PDF)
print('页数', doc.page_count)
hits = []
for i in range(doc.page_count):
    txt = doc[i].get_text()
    if re.search(r'第\s*7\s*题', txt):
        hits.append(i)
        print('  页 %d 含「第7题」| 文字层 %d 字' % (i + 1, len(txt.strip())))
print('命中页:', [h + 1 for h in hits])
# 渲染命中页（或全部前 8 页）
for i in (hits or list(range(min(6, doc.page_count)))):
    pg = doc[i]
    pix = pg.get_pixmap(dpi=170)
    fp = os.path.join(OUT, 'p%02d.png' % (i + 1))
    pix.save(fp)
    print('  → %s  %dx%d' % (os.path.basename(fp), pix.width, pix.height))
