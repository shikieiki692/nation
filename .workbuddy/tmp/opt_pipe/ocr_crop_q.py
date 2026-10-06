# -*- coding: utf-8 -*-
"""按 OCR 索引裁区：给定 pdf + 题号，用 ocr_index 的缓存定位「第q题..第(q+1)题」并裁区。
用法：python ocr_crop_q.py <pdf> <tag> <q> <out_dir> <dest_prefix> [dpi]
"""
import os, re, sys, json
sys.stdout.reconfigure(encoding='utf-8')
try:
    import fitz
    try:
        fitz.TOOLS.mupdf_display_errors(False); fitz.TOOLS.mupdf_display_warnings(False)
    except Exception:
        pass
except Exception:
    fitz = None
LOC = '.workbuddy/tmp/opt_pipe/ocr_loc'
MARK = re.compile(r'第\s*(\d+)\s*题')


def find_mark(data, q, after=None):
    """在 OCR 块里找「第q题」标记 → (page_index, y_ocr) ；after=(page,y) 只取其后。"""
    for pg in data:
        for b in pg['blocks']:
            s = b['t'].replace(' ', '')
            m = MARK.search(s)
            if not m or int(m.group(1)) != q:
                continue
            if s.index('第') > 6:          # 行内提及（非行首标记）→ 跳过
                continue
            if after and (pg['page'] - 1, b['y']) <= after:
                continue
            return pg['page'] - 1, b['y'], pg['scale']
    return None


def main():
    pdf, tag, q = sys.argv[1], sys.argv[2], int(sys.argv[3])
    out_dir, prefix = sys.argv[4], sys.argv[5]
    dpi = int(sys.argv[6]) if len(sys.argv) > 6 else 200
    data = json.load(open(os.path.join(LOC, tag + '.json'), encoding='utf-8'))
    a = find_mark(data, q)
    if not a:
        print('!! 未找到 第%d题' % q); return 1
    b = find_mark(data, q + 1, after=(a[0], a[1]))
    pa, ya, sc = a
    if b:
        pb, yb, _ = b
    else:
        pb, yb = len(data) - 1, len(data[-1]['blocks']) and 10**9 or 10**9
    doc = fitz.open(pdf)
    os.makedirs(out_dir, exist_ok=True)
    n = 0
    for p in range(pa, pb + 1):
        pg = doc[p]; R = pg.rect
        y0 = ya / sc if p == pa else R.y0 + 30 / 72.0 * 72
        y1 = (yb / sc) if (p == pb and b) else (R.y1 - 26)
        y0 = max(R.y0, y0 - 4); y1 = min(R.y1, y1 + 4)
        if y1 - y0 < 10:
            continue
        clip = fitz.Rect(R.x0 + 26, y0, R.x1 - 26, y1)
        pix = pg.get_pixmap(dpi=dpi, clip=clip)
        d = os.path.join(out_dir, '%s_p%02d.png' % (prefix, p + 1))
        pix.save(d); n += 1
        print('  %s p%d y%.0f..%.0f %dx%d' % (os.path.basename(d), p + 1, y0, y1, pix.width, pix.height))
    print('第%d题 → %d 张' % (q, n))
    return 0


if __name__ == '__main__':
    sys.exit(main())
