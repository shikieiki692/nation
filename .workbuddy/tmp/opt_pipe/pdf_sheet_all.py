# -*- coding: utf-8 -*-
"""把一份 PDF 的全部页渲染并拼成**一张**网格图（带页码），用于扫描件快速定位题页。
用法：python pdf_sheet_all.py <pdf> <tag> [cols] [dpi]
输出：.workbuddy/tmp/opt_pipe/locate_out/<tag>/all_pages.png
"""
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
try:
    import fitz
    from PIL import Image, ImageDraw
    try:
        fitz.TOOLS.mupdf_display_errors(False); fitz.TOOLS.mupdf_display_warnings(False)
    except Exception:
        pass
except Exception:
    fitz = None


def main():
    pdf, tag = sys.argv[1], sys.argv[2]
    cols = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    dpi = int(sys.argv[4]) if len(sys.argv) > 4 else 55
    out = os.path.join('.workbuddy/tmp/opt_pipe/locate_out', tag)
    os.makedirs(out, exist_ok=True)
    doc = fitz.open(pdf)
    ims = []
    for i in range(doc.page_count):
        pix = doc[i].get_pixmap(dpi=dpi)
        ims.append((i + 1, Image.frombytes('RGB', (pix.width, pix.height), pix.samples)))
    CW = max(im.width for _, im in ims) + 8
    CH = max(im.height for _, im in ims) + 18
    rows = (len(ims) + cols - 1) // cols
    c = Image.new('RGB', (cols * CW, rows * CH), 'white')
    d = ImageDraw.Draw(c)
    for k, (n, im) in enumerate(ims):
        r, cc = divmod(k, cols)
        x, y = cc * CW + 4, r * CH + 16
        c.paste(im, (x, y))
        d.text((x, y - 12), 'p%d' % n, fill='red')
    p = os.path.join(out, 'all_pages.png')
    c.save(p)
    print('拼版 %s  %dx%d  页数=%d' % (p, c.width, c.height, len(ims)))


if __name__ == '__main__':
    main()
