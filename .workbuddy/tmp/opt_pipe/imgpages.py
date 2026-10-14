# -*- coding: utf-8 -*-
r"""按实际版面放置列出含图页（只读）。用法: imgpages.py <卷>"""
import sys, os, glob
import fitz
os.chdir(r'C:\Obsidion\妙妙屋')
BASE = '.workbuddy/tmp/opt_pipe/render_gate_out'
V = sys.argv[1]
for tag in ['学生版', '答案与解析版']:
    fs = glob.glob(os.path.join(BASE, '初赛模拟卷%s（非有机·%s·真题版式）' % (V, tag), '*.pdf'))
    if not fs:
        print('MISS', V, tag); continue
    d = fitz.open(fs[0])
    pages = []
    for i, pg in enumerate(d):
        infos = pg.get_image_info()
        # 只算「有实际面积」的（> 30x30 pt）
        big = [x for x in infos if x.get('bbox') and (x['bbox'][2] - x['bbox'][0]) > 30 and (x['bbox'][3] - x['bbox'][1]) > 30]
        if big:
            pages.append((i + 1, len(big)))
    print('%s %s: 共 %d 页 ｜ 含图页 %s' % (V, tag, d.page_count, pages))
    d.close()
