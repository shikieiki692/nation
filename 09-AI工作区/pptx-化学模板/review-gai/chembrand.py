# -*- coding: utf-8 -*-
"""chembrand.py - add CHEMISTRY-themed decorative emblems to a PPT.

Unlike the minimal lightbrand (title bar only), this makes the chemistry
identity clearly visible: it draws vector chemistry motifs (atom with
electron orbits, benzene ring, ball-and-stick molecule) into the emptiest
corner(s) of each content slide, using the slide's own title color so it
harmonizes with the existing design. Motifs are semi-transparent so even a
minor overlap reads as background texture, never as obstruction.

It does NOT touch any text, image, or background. Cover (slide 1) and the
end slide are skipped (their native design is kept intact).

Usage: python chembrand.py <unpacked_dir>
"""
import math
import pathlib
import re
import sys

from lxml import etree

A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'

# motif transparency (0..100000). Lines a bit lighter than dots.
ALPHA_LINE = 60000
ALPHA_FILL = 72000
FALLBACK = '56CA95'  # mint

# corner zone size (EMU). ~1.25 cm on 16:9. Capped so it never dominates.
CZ_FRAC_H = 0.165
CZ_CAP = 1450000


def q(ns, tag):
    return f'{{{ns}}}{tag}'


def solid(color, alpha):
    if color is None:
        return '<a:noFill/>'
    return (f'<a:solidFill><a:srgbClr val="{color}">'
            f'<a:alpha val="{int(alpha)}"/></a:srgbClr></a:solidFill>')


def mk_sp(sid, name, x, y, cx, cy, prst='rect', fill=None, line=None,
          line_w=12700, rot=0, alpha_fill=100000, alpha_line=100000):
    rot_xml = f' rot="{int(rot)}"' if rot else ''
    if line is None:
        ln_xml = '<a:ln><a:noFill/></a:ln>'
    else:
        ln_xml = (f'<a:ln w="{int(line_w)}">{solid(line, alpha_line)}</a:ln>')
    return etree.fromstring(
        f'<p:sp xmlns:p="{P}" xmlns:a="{A}">'
        f'<p:nvSpPr><p:cNvPr id="{sid}" name="{name}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
        f'<p:spPr><a:xfrm{rot_xml}><a:off x="{int(x)}" y="{int(y)}"/>'
        f'<a:ext cx="{int(cx)}" cy="{int(cy)}"/></a:xfrm>'
        f'<a:prstGeom prst="{prst}"><a:avLst/></a:prstGeom>'
        f'{solid(fill, alpha_fill)}{ln_xml}</p:spPr>'
        f'<p:txBody><a:bodyPr/><a:lstStyle/><a:p>'
        f'<a:endParaRPr lang="zh-CN"/></a:p></p:txBody>'
        f'</p:sp>')


def bond(sid, name, p1, p2, t, color, alpha):
    x1, y1 = p1
    x2, y2 = p2
    dx, dy = x2 - x1, y2 - y1
    L = int((dx * dx + dy * dy) ** 0.5)
    if L <= 0:
        return None
    ang = math.degrees(math.atan2(dy, dx))
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    rot = int(ang * 60000)
    x = mx - L / 2
    y = my - t / 2
    return mk_sp(sid, name, x, y, L, t, prst='rect', fill=color, line=None,
                 alpha_fill=alpha, alpha_line=100000, rot=rot)


def emblem_atom(sid, cx0, cy0, S, color):
    els = []
    rx, ry = S * 0.5, S * 0.17
    for k in range(3):
        els.append(mk_sp(sid, 'ChemOrbit', cx0 - rx, cy0 - ry, 2 * rx, 2 * ry,
                         prst='ellipse', fill=None, line=color, line_w=12000,
                         rot=int(k * 60 * 60000), alpha_line=ALPHA_LINE))
        sid += 1
    d = S * 0.14
    els.append(mk_sp(sid, 'ChemNucleus', cx0 - d / 2, cy0 - d / 2, d, d,
                     prst='ellipse', fill=color, line=None, alpha_fill=ALPHA_FILL))
    sid += 1
    return els, sid


def emblem_benzene(sid, cx0, cy0, S, color):
    els = []
    els.append(mk_sp(sid, 'ChemHex', cx0 - S / 2, cy0 - S / 2, S, S,
                     prst='hexagon', fill=None, line=color, line_w=12000,
                     alpha_line=ALPHA_LINE))
    sid += 1
    di = S * 0.5
    els.append(mk_sp(sid, 'ChemHexIn', cx0 - di / 2, cy0 - di / 2, di, di,
                     prst='ellipse', fill=None, line=color, line_w=11000,
                     alpha_line=int(ALPHA_LINE * 0.85)))
    sid += 1
    R = S * 0.5
    for k in range(6):
        ang = math.radians(90 + k * 60)
        vx, vy = cx0 + R * math.cos(ang), cy0 + R * math.sin(ang)
        d = S * 0.075
        els.append(mk_sp(sid, 'ChemAtom', vx - d / 2, vy - d / 2, d, d,
                         prst='ellipse', fill=color, line=None, alpha_fill=ALPHA_FILL))
        sid += 1
    return els, sid


def emblem_mol(sid, cx0, cy0, S, color):
    els = []
    r = S * 0.10
    pts = [(cx0, cy0 - S * 0.24),
           (cx0 - S * 0.21, cy0 + S * 0.18),
           (cx0 + S * 0.21, cy0 + S * 0.18)]
    t = 13000
    for a, b in ((0, 1), (1, 2), (2, 0)):
        bnd = bond(sid, 'ChemBond', pts[a], pts[b], t, color, ALPHA_LINE)
        if bnd is not None:
            els.append(bnd)
            sid += 1
    for (px, py) in pts:
        els.append(mk_sp(sid, 'ChemNode', px - r, py - r, 2 * r, 2 * r,
                         prst='ellipse', fill=color, line=None, alpha_fill=ALPHA_FILL))
        sid += 1
    return els, sid


def get_canvas(pres_path):
    s = pres_path.read_text(encoding='utf-8')
    m = re.search(r'<p:sldSz cx="(\d+)" cy="(\d+)"', s)
    return (int(m.group(1)), int(m.group(2))) if m else (12192000, 6858000)


def title_color(sp_tree):
    for el in sp_tree:
        if etree.QName(el).localname != 'sp':
            continue
        ph = el.find(f'.//{q(P, "ph")}')
        pht = ph.get('type') if ph is not None else None
        if pht not in ('title', 'ctrTitle'):
            continue
        for rpr in el.iter(q(A, 'rPr')):
            sf = rpr.find(q(A, 'solidFill'))
            if sf is not None:
                sc = sf.find(q(A, 'srgbClr'))
                if sc is not None:
                    return sc.get('val').upper()
    # fallback: first solid color run on any shape
    for el in sp_tree:
        if etree.QName(el).localname != 'sp':
            continue
        for rpr in el.iter(q(A, 'rPr')):
            sf = rpr.find(q(A, 'solidFill'))
            if sf is not None:
                sc = sf.find(q(A, 'srgbClr'))
                if sc is not None:
                    return sc.get('val').upper()
    return FALLBACK


def ink_boxes(sp_tree):
    boxes = []
    for el in sp_tree:
        ln = etree.QName(el).localname
        if ln not in ('sp', 'pic', 'graphicFrame', 'cxnSp', 'grpSp'):
            continue
        xfrm = el.find(f'.//{q(A, "xfrm")}')
        if xfrm is None:
            continue
        off = xfrm.find(q(A, 'off'))
        ext = xfrm.find(q(A, 'ext'))
        if off is None or ext is None:
            continue
        x, y, cx, cy = (int(off.get('x')), int(off.get('y')),
                        int(ext.get('cx')), int(ext.get('cy')))
        # ignore tiny decorative bits
        if cx < 260000 and cy < 260000:
            continue
        boxes.append((x, y, cx, cy))
    return boxes


def intersect_area(a, z):
    ax, ay, acx, acy = a
    zx, zy, zcx, zcy = z
    ox = max(0, min(ax + acx, zx + zcx) - max(ax, zx))
    oy = max(0, min(ay + acy, zy + zcy) - max(ay, zy))
    return ox * oy


def free_score(zone, boxes):
    za = zone[2] * zone[3]
    ov = sum(intersect_area(b, zone) for b in boxes)
    return za - ov, ov


def main(root_dir):
    root_dir = pathlib.Path(root_dir)
    W, H = get_canvas(root_dir / 'ppt/presentation.xml')
    Cz = min(int(CZ_FRAC_H * H), int(0.22 * W), CZ_CAP)
    zones = {
        'TL': (0, 0, Cz, Cz),
        'TR': (W - Cz, 0, Cz, Cz),
        'BL': (0, H - Cz, Cz, Cz),
        'BR': (W - Cz, H - Cz, Cz, Cz),
    }
    zcent = {k: (z[0] + z[2] / 2, z[1] + z[3] / 2) for k, z in zones.items()}
    slides = sorted((root_dir / 'ppt/slides').glob('slide*.xml'),
                    key=lambda p: int(re.search(r'\d+', p.name).group()))
    total = len(slides)
    counts = {0: 0, 1: 0, 2: 0}
    for i, sp_path in enumerate(slides, 1):
        if i == 1 or i == total:
            continue
        t = etree.parse(str(sp_path))
        r = t.getroot()
        sp_tree = r.find(f'.//{q(P, "spTree")}')
        color = title_color(sp_tree)
        boxes = ink_boxes(sp_tree)
        # existing ids to avoid collision
        sids = [int(e.get('id')) for e in sp_tree.iter(q(P, 'cNvPr'))
                if e.get('id', '').isdigit()]
        sid = (max(sids) + 1) if sids else 20000
        # rank corners by free area
        ranked = sorted(zones.items(), key=lambda kv: free_score(kv[1], boxes)[0],
                        reverse=True)
        best = ranked[0]
        fmain, _ = free_score(best[1], boxes)
        placed = 0
        new_els = []
        if fmain > 0.35 * (Cz * Cz):
            S = Cz * 0.74
            cx0, cy0 = zcent[best[0]]
            els, sid = emblem_atom(sid, cx0, cy0, S, color)
            new_els += els
            placed += 1
            # try a second emblem (benzene) in the next-freest corner
            second = ranked[1]
            fsec, _ = free_score(second[1], boxes)
            if fsec > 0.5 * (Cz * Cz):
                S2 = Cz * 0.6
                cx2, cy2 = zcent[second[0]]
                els2, sid = emblem_benzene(sid, cx2, cy2, S2, color)
                new_els += els2
                placed += 1
        if new_els:
            for el in new_els:
                sp_tree.append(el)
            t.write(str(sp_path), encoding='ascii', xml_declaration=True)
        counts[placed] += 1
        print(f'slide {i:2d}: color={color} placed={placed} '
              f'({best[0]}{("+"+ranked[1][0]) if placed==2 else ""})')
    print(f'TOTAL slides={total} | 2 emblems={counts[2]} '
          f'1 emblem={counts[1]} 0 emblems={counts[0]} (cover+end skipped)')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage: python chembrand.py <unpacked_dir>')
        sys.exit(1)
    main(sys.argv[1])
