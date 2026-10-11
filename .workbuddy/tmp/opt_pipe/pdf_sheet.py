# -*- coding: utf-8 -*-
"""pdf_sheet.py：把 PDF 全页渲染成带页码的缩略拼图（用于扫描件定位）。
用法：python pdf_sheet.py "<pdf>" <tag> [dpi] [cols]
"""
import io
import math
import os
import sys

import pymupdf
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
OUT = r"C:\Obsidion\妙妙屋\.workbuddy\tmp\opt_pipe\locate_out\xvi_visual"


def main():
    pdf, tag = sys.argv[1], sys.argv[2]
    dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 42
    cols = int(sys.argv[4]) if len(sys.argv) > 4 else 5
    doc = pymupdf.open(pdf)
    thumbs = []
    for i, pg in enumerate(doc):
        pix = pg.get_pixmap(dpi=dpi)
        im = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
        thumbs.append((i + 1, im))
    cw, ch = thumbs[0][1].size
    rows = math.ceil(len(thumbs) / cols)
    sheet = Image.new("RGB", (cols * cw, rows * (ch + 20)), "white")
    dr = ImageDraw.Draw(sheet)
    for k, (no, im) in enumerate(thumbs):
        r, c = divmod(k, cols)
        sheet.paste(im, (c * cw, r * (ch + 20) + 20))
        dr.text((c * cw + 6, r * (ch + 20) + 5), "P%d" % no, fill="red")
    out = os.path.join(OUT, "sheet_%s.png" % tag)
    sheet.save(out)
    print("页数 %d ｜ 拼图 → %s ｜ 尺寸 %s" % (doc.page_count, out, sheet.size))
    doc.close()


if __name__ == "__main__":
    main()
