# -*- coding: utf-8 -*-
"""Analyze a slide's shapes: type, geometry, fill color, text, bg."""
import sys
from lxml import etree

A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
P = 'http://schemas.openxmlformats.org/presentationml/2006/main'


def q(ns, t):
    return f'{{{ns}}}{t}'


def fill_of(el):
    sf = el.find(f'.//{q(A, "solidFill")}')
    if sf is not None:
        sc = sf.find(q(A, 'srgbClr'))
        if sc is not None:
            return 'srgb#' + sc.get('val')
        sch = sf.find(q(A, 'schemeClr'))
        if sch is not None:
            return 'scheme#' + sch.get('val')
    gr = el.find(f'.//{q(A, "gradFill")}')
    if gr is not None:
        return 'grad'
    no = el.find(f'.//{q(A, "noFill")}')
    if no is not None:
        return 'none'
    return '?'


def text_of(el):
    return ''.join(t.text or '' for t in el.iter(q(A, 't'))).strip()


def analyze(path):
    t = etree.parse(path)
    r = t.getroot()
    sld = r.find(q(P, 'cSld'))
    bg = sld.find(q(P, 'bg'))
    print(f'--- {path} ---')
    if bg is not None:
        print('  BG:', fill_of(bg))
    else:
        print('  BG: (inherit/master)')
    tree = sld.find(q(P, 'spTree'))
    n = 0
    for el in tree:
        ln = etree.QName(el).localname
        if ln not in ('sp', 'pic', 'graphicFrame', 'cxnSp', 'grpSp'):
            continue
        n += 1
        xf = el.find(f'.//{q(A, "xfrm")}')
        if xf is not None:
            off = xf.find(q(A, 'off'))
            ext = xf.find(q(A, 'ext'))
            geo = (f"x={int(off.get('x'))//360000}cm y={int(off.get('y'))//360000}cm "
                   f"w={int(ext.get('cx'))//360000}cm h={int(ext.get('cy'))//360000}cm"
                   if off is not None and ext is not None else "no-xfrm")
        else:
            geo = "no-xfrm"
        ph = el.find(f'.//{q(P, "ph")}')
        pht = ph.get('type') if ph is not None else '-'
        txt = text_of(el)
        fl = fill_of(el)
        extra = f"  ph={pht} fill={fl} {geo}"
        if txt:
            extra += f"  TEXT={txt[:40]!r}"
        print(f'  [{n:02d}] {ln:12s}{extra}')
    print(f'  total shapes={n}')


if __name__ == '__main__':
    for p in sys.argv[1:]:
        analyze(p)
