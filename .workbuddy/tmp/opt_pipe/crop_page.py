# -*- coding: utf-8 -*-
"""crop_page.py —— 高分辨率裁切 PDF 页面的局部区域。
用法: python -X utf8 crop_page.py <pdf> <页码1based> <y0frac> <y1frac> <dpi> <out.png>
"""
import sys
import fitz

pdf, pno = sys.argv[1], int(sys.argv[2])
y0, y1 = float(sys.argv[3]), float(sys.argv[4])
dpi = int(sys.argv[5])
out = sys.argv[6]
with fitz.open(pdf) as d:
    p = d[pno - 1]
    r = p.rect
    clip = fitz.Rect(r.x0, r.y0 + (r.y1 - r.y0) * y0, r.x1, r.y0 + (r.y1 - r.y0) * y1)
    pix = p.get_pixmap(dpi=dpi, clip=clip)
    pix.save(out)
    print(out, pix.width, pix.height)
