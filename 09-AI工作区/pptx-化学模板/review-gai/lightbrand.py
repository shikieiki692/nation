# -*- coding: utf-8 -*-
"""lightbrand.py - LIGHT personalization overlay.

Goal: turn an already-good PPT into "your own template" WITHOUT touching
its native design. Only adds a small, consistent title-area decoration to
content/section slides:
    * a short vertical accent bar to the LEFT of the title (in the margin)
    * a thin underline just BELOW the title
Accent color is taken from the title's own run color (so it harmonizes
with each slide's existing palette); falls back to mint #56CA95.

It does NOT:
    * change any text, font, image, or background
    * touch the cover (slide 1) or the end slide (last)
    * add page numbers / signatures (those are separate, optional steps)

Usage: python lightbrand.py <unpacked_dir>
"""
import pathlib
import re
import sys

from lxml import etree

A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
P = 'http://schemas.openxmlformats.org/presentationml/2006/main'

# decoration geometry (EMU). 914400 EMU = 1 inch (~2.54 cm).
BAR_GAP = 150000     # gap between title left edge and the bar
BAR_W = 95000        # bar width
BAR_MIN_H = 360000   # min bar height (single-line titles)
BAR_MAX_H = 1150000  # max bar height (multi-line titles)
UNDER_GAP = 75000    # gap between title bottom and underline
UNDER_H = 40000      # underline thickness
UNDER_MAX_W = 1900000  # underline max width (~2.1 cm)
FALLBACK_ACCENT = '56CA95'  # mint, from reference palette accent3

MINT = FALLBACK_ACCENT


def q(ns, tag):
    return f'{{{ns}}}{tag}'


def rect(sid, name, x, y, cx, cy, fill):
    return etree.fromstring(
        f'<p:sp xmlns:p="{P}" xmlns:a="{A}">'
        f'<p:nvSpPr><p:cNvPr id="{sid}" name="{name}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
        f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
        f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill><a:ln><a:noFill/></a:ln></p:spPr>'
        f'<p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:endParaRPr lang="zh-CN"/></a:p></p:txBody>'
        f'</p:sp>')


def get_canvas(pres_path):
    s = pres_path.read_text(encoding='utf-8')
    m = re.search(r'<p:sldSz cx="(\d+)" cy="(\d+)"', s)
    return (int(m.group(1)), int(m.group(2))) if m else (9144000, 5143500)


def title_shape(sp_tree):
    """Return (element, x, y, cx, cy) of the title text box, or None."""
    W, H = get_canvas(__import__('pathlib').Path(
        sp_tree.getroottree().docinfo.URL).parent.parent / 'presentation.xml') if False else (12192000, 6858000)
    candidates = []
    for el in sp_tree:
        tag = etree.QName(el).localname
        if tag not in ('sp',):
            continue
        xfrm = el.find(f'.//{q(A, "xfrm")}')
        if xfrm is None:
            continue
        off = xfrm.find(q(A, 'off'))
        ext = xfrm.find(q(A, 'ext'))
        if off is None or ext is None:
            continue
        x, y, cx, cy = int(off.get('x')), int(off.get('y')), int(ext.get('cx')), int(ext.get('cy'))
        ph = el.find(f'.//{q(P, "ph")}')
        pht = ph.get('type') if ph is not None else None
        txt = ''.join(t.text or '' for t in el.findall(f'.//{q(A, "t")}'))
        if not txt.strip():
            continue
        if cx < 0.15 * 12192000:
            continue
        candidates.append((el, x, y, cx, cy, pht, len(txt)))
    if not candidates:
        return None
    # 1) placeholder title / ctrTitle
    for c in candidates:
        if c[5] in ('title', 'ctrTitle'):
            return c[:5]
    # 2) topmost text shape (smallest y)
    c = min(candidates, key=lambda c: c[2])
    return c[:5]


def title_accent(el):
    """Detect the title's own run color to harmonize the decoration."""
    for rpr in el.iter(q(A, 'rPr')):
        sf = rpr.find(q(A, 'solidFill'))
        if sf is not None:
            sc = sf.find(q(A, 'srgbClr'))
            if sc is not None:
                return sc.get('val').upper()
        # theme color -> skip (use fallback)
    return FALLBACK_ACCENT


def main(root_dir):
    root_dir = pathlib.Path(root_dir)
    W, H = get_canvas(root_dir / 'ppt/presentation.xml')
    slides = sorted((root_dir / 'ppt/slides').glob('slide*.xml'),
                    key=lambda p: int(re.search(r'\d+', p.name).group()))
    total = len(slides)
    sid = 20000
    decorated = 0
    for i, sp_path in enumerate(slides, 1):
        # skip cover (1) and end (last)
        if i == 1 or i == total:
            continue
        t = etree.parse(str(sp_path))
        r = t.getroot()
        sp_tree = r.find(f'.//{q(P, "spTree")}')
        res = title_shape(sp_tree)
        if res is None:
            continue
        el, x, y, cx, cy = res
        accent = title_accent(el)
        # vertical bar to the left of the title (in the margin)
        bx = x - BAR_GAP - BAR_W
        if bx < 0:
            bx = x + cx + BAR_GAP  # put it to the RIGHT if no left room
        bh = max(BAR_MIN_H, min(cy, BAR_MAX_H))
        by = y + (cy - bh) // 2  # vertically center on the title
        # underline below the title
        uy = y + cy + UNDER_GAP
        uw = min(cx, UNDER_MAX_W)
        sid += 1
        sp_tree.append(rect(sid, 'BrandBar', bx, by, BAR_W, bh, accent))
        sid += 1
        sp_tree.append(rect(sid, 'BrandRule', x, uy, uw, UNDER_H, accent))
        t.write(str(sp_path), encoding='ascii', xml_declaration=True)
        decorated += 1
    print(f'canvas={W}x{H} slides={total} decorated(title bar+rule)={decorated} (cover+end skipped)')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage: python lightbrand.py <unpacked_dir>')
        sys.exit(1)
    main(sys.argv[1])
