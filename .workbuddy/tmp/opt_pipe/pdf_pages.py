# -*- coding: utf-8 -*-
"""pdf_pages.py —— 整份 PDF 逐页渲染 + 缩略拼版（供人工核验/定位题目页）。

用法:
  python -X utf8 pdf_pages.py <pdf> <tag> [dpi=120] [start=1] [end=末页]
  python -X utf8 pdf_pages.py <pdf> <tag> --sheet [cols=2 rows=2 dpi=115]   # 只出拼版

输出:
  .workbuddy/tmp/opt_pipe/locate_out/<tag>/page_NN.png    逐页（dpi）
  .workbuddy/tmp/opt_pipe/locate_out/<tag>/sheet_NN.png   拼版（带 pNN 标注）
"""
import os
import sys
import math
import fitz
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "locate_out")


def main():
    pdf = sys.argv[1]
    tag = sys.argv[2]
    rest = sys.argv[3:]
    sheet_only = "--sheet" in rest
    nums = [int(x) for x in rest if x.isdigit()]
    dpi = nums[0] if nums else (115 if sheet_only else 120)
    d = os.path.join(OUT, tag)
    os.makedirs(d, exist_ok=True)
    with fitz.open(pdf) as doc:
        n = doc.page_count
        start = nums[1] if len(nums) > 1 else 1
        end = nums[2] if len(nums) > 2 else n
        pages = list(range(start - 1, min(end, n)))
        imgs = []
        for i in pages:
            pix = doc[i].get_pixmap(dpi=dpi)
            im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
            imgs.append((i + 1, im))
            if not sheet_only:
                im.save(os.path.join(d, "page_%02d.png" % (i + 1)))
        print("逐页:%s 页 1..%d dpi=%d" % (tag, n, dpi))
    if sheet_only:
        cols, rows = 2, 2
        pad, lab = 10, 26
        W = max(im.width for _, im in imgs)
        H = max(im.height for _, im in imgs)
        per = cols * rows
        for s in range(math.ceil(len(imgs) / per)):
            chunk = imgs[s * per:(s + 1) * per]
            sh = Image.new("RGB", (cols * (W + pad) + pad, rows * (H + lab + pad) + pad), "white")
            dr = ImageDraw.Draw(sh)
            for k, (pno, im) in enumerate(chunk):
                r, c = divmod(k, cols)
                x = pad + c * (W + pad)
                y = pad + r * (H + lab + pad)
                dr.text((x + 4, y + 6), "=== p%d ===" % pno, fill="red")
                sh.paste(im, (x, y + lab))
            fp = os.path.join(d, "sheet_%02d.png" % (s + 1))
            sh.save(fp)
            print("拼版:", fp, sh.size)


if __name__ == "__main__":
    main()
