# -*- coding: utf-8 -*-
"""按「题标记」在答案 PDF 中定位并裁区为图（忠实保留公式/图，免转录失真）。
用法：
  python ans_crop_q.py <pdf> <out_dir> <tag> --start "<起点文本>" [--end "<终点文本>"] \
      [--page-lo N] [--page-hi M] [--dpi 200] [--margin 6]
输出：<out_dir>/<tag>_pXX.png（可能多张），并打印每张的 y 区间。
"""
import argparse, os, sys

sys.stdout.reconfigure(encoding='utf-8')
try:
    import fitz
    try:
        fitz.TOOLS.mupdf_display_errors(False); fitz.TOOLS.mupdf_display_warnings(False)
    except Exception:
        pass
except Exception:
    fitz = None


def _hits(pg, txt):
    """容错定位：尝试原文 / 去空格 / 单空格 三种写法。"""
    out = []
    for v in dict.fromkeys([txt, txt.replace(' ', ''), txt.replace('  ', ' ')]):
        if v:
            out += pg.search_for(v)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('pdf'); ap.add_argument('out_dir'); ap.add_argument('tag')
    ap.add_argument('--start', required=True); ap.add_argument('--end', default='')
    ap.add_argument('--section', default='', help='起点之前必须先出现的分节锚（如「模拟试卷3 答案」）')
    ap.add_argument('--page-lo', type=int, default=0); ap.add_argument('--page-hi', type=int, default=0)
    ap.add_argument('--dpi', type=int, default=200); ap.add_argument('--margin', type=float, default=6)
    a = ap.parse_args()
    os.makedirs(a.out_dir, exist_ok=True)
    doc = fitz.open(a.pdf)
    lo = a.page_lo or 0
    hi = a.page_hi or doc.page_count
    # 分节锚（用「页文本包含」匹配，比 search_for 稳）
    sp_sec = sy_sec = None
    if a.section:
        key = a.section.replace(' ', '')
        for p in range(lo, min(hi, doc.page_count)):
            if key in doc[p].get_text().replace(' ', '').replace('\n', ''):
                sp_sec = p
                r = _hits(doc[p], a.section)
                sy_sec = min(x.y0 for x in r) if r else 0.0
                break
        if sp_sec is None:
            print('!! 未找到分节锚：%s' % a.section); return 1
    # 定位起点
    sp = sy = None
    for p in range(lo, min(hi, doc.page_count)):
        for x in _hits(doc[p], a.start):
            if sp_sec is not None and (p < sp_sec or (p == sp_sec and x.y0 <= sy_sec + 2)):
                continue
            sp, sy = p, x.y0; break
        if sp is not None:
            break
    if sp is None:
        print('!! 未找到起点：%s' % a.start); return 1
    # 定位终点
    ep, ey = None, None
    if a.end:
        for p in range(sp, min(hi, doc.page_count)):
            r = _hits(doc[p], a.end)
            r = [x for x in r if (p > sp or x.y0 > sy + 2)]
            if r:
                ep, ey = p, min(x.y0 for x in r); break
    if ep is None:
        ep, ey = min(hi - 1, doc.page_count - 1), doc[sp].rect.y1 - 40
    print('起点 p%d y%.0f ；终点 p%d y%.0f' % (sp + 1, sy, ep + 1, ey if ey else -1))
    n = 0
    for p in range(sp, ep + 1):
        pg = doc[p]; R = pg.rect
        y0 = (sy - a.margin) if p == sp else (R.y0 + 34)
        y1 = (ey + a.margin) if p == ep else (R.y1 - 34)
        if y1 - y0 < 12:
            continue
        clip = fitz.Rect(R.x0 + 40, max(R.y0, y0), R.x1 - 40, min(R.y1, y1))
        pix = pg.get_pixmap(dpi=a.dpi, clip=clip)
        dest = os.path.join(a.out_dir, '%s_p%02d.png' % (a.tag, p + 1))
        pix.save(dest)
        print('  %s  p%d y%.0f..%.0f  %dx%d' % (os.path.basename(dest), p + 1, y0, y1, pix.width, pix.height))
        n += 1
    print('输出 %d 张' % n)
    return 0


if __name__ == '__main__':
    sys.exit(main())
