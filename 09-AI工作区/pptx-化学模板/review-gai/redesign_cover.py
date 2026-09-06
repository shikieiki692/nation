# -*- coding: utf-8 -*-
"""redesign_cover.py - restyle slide 1 (cover) of the unpacked pptx.

Reference style: the user's original self-made template (高中化学课件模板.pptx):
  deep green bg #1B4332, amber #E8A33D bars/blocks, cream #FAF7F0 title
  panel, bottom green bar #2D6A4F, page number. The original cover TEXT is
preserved (same strings) but rebuilt as fresh text shapes with explicit
colors (no inherited shape fill / theme color). Benzene rings (vector)
are the decorative motif: a hero ring + two satellites + bonds on the
right, plus a faint watermark ring behind the title.
"""
import math
import pathlib
import sys

from lxml import etree

A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
P = 'http://schemas.openxmlformats.org/presentationml/2006/main'

GREEN = '1B4332'
GREEN2 = '2D6A4F'
AMBER = 'E8A33D'
CREAM = 'FAF7F0'
EMU = 360000


def cm(n):
    return int(round(n * EMU))


def q(ns, t):
    return f'{{{ns}}}{t}'


def solid(color, alpha):
    if color is None:
        return '<a:noFill/>'
    return (f'<a:solidFill><a:srgbClr val="{color}">'
            f'<a:alpha val="{int(alpha)}"/></a:srgbClr></a:solidFill>')


def mk_sp(sid, name, x, y, cx, cy, prst='rect', fill=None, line=None,
          line_w=12700, rot=0, alpha_fill=100000, alpha_line=100000,
          round_=False):
    prst = 'roundRect' if round_ else prst
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


def mk_text(sid, name, x, y, cx, cy, text, color, sz, bold=False,
            align='l'):
    rpr = (f'<a:rPr lang="zh-CN" sz="{sz}"{" b=\"1\"" if bold else ""}>'
           f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill></a:rPr>')
    para = (f'<a:p><a:pPr algn="{align}"/>'
            f'<a:r>{rpr}<a:t>{text}</a:t></a:r></a:p>')
    return etree.fromstring(
        f'<p:sp xmlns:p="{P}" xmlns:a="{A}">'
        f'<p:nvSpPr><p:cNvPr id="{sid}" name="{name}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
        f'<p:spPr><a:xfrm><a:off x="{int(x)}" y="{int(y)}"/>'
        f'<a:ext cx="{int(cx)}" cy="{int(cy)}"/></a:xfrm>'
        f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
        f'<a:noFill/><a:ln><a:noFill/></a:ln></p:spPr>'
        f'<p:txBody><a:bodyPr/><a:lstStyle/>{para}</p:txBody>'
        f'</p:sp>')


def benz(sid, cx0, cy0, S, color, a_line, a_fill):
    els = []
    els.append(mk_sp(sid, 'CovHex', cx0 - S / 2, cy0 - S / 2, S, S,
                     prst='hexagon', fill=None, line=color, line_w=13000,
                     alpha_line=a_line))
    sid += 1
    di = S * 0.5
    els.append(mk_sp(sid, 'CovHexIn', cx0 - di / 2, cy0 - di / 2, di, di,
                     prst='ellipse', fill=None, line=color, line_w=11000,
                     alpha_line=int(a_line * 0.85)))
    sid += 1
    R = S * 0.5
    for k in range(6):
        ang = math.radians(90 + k * 60)
        vx, vy = cx0 + R * math.cos(ang), cy0 + R * math.sin(ang)
        d = S * 0.08
        els.append(mk_sp(sid, 'CovNode', vx - d / 2, vy - d / 2, d, d,
                         prst='ellipse', fill=color, line=None,
                         alpha_fill=a_fill))
        sid += 1
    return els, sid


def bond(sid, name, p1, p2, t, color, alpha):
    x1, y1 = p1
    x2, y2 = p2
    dx, dy = x2 - x1, y2 - y1
    L = int((dx * dx + dy * dy) ** 0.5)
    if L <= 0:
        return None, sid
    ang = math.degrees(math.atan2(dy, dx))
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    rot = int(ang * 60000)
    return (mk_sp(sid, name, mx - L / 2, my - t / 2, L, t, prst='rect',
                  fill=color, line=None, alpha_fill=alpha), sid + 1)


def main(root_dir, total_pages=31):
    root_dir = pathlib.Path(root_dir)
    W, H = 12192000, 6858000
    sp_path = root_dir / 'ppt/slides/slide1.xml'
    t = etree.parse(str(sp_path))
    r = t.getroot()
    cSld = r.find(q(P, 'cSld'))
    sp_tree = cSld.find(q(P, 'spTree'))
    # wipe all current children (decor + old text); keep nothing
    for el in list(sp_tree):
        sp_tree.remove(el)

    sid = 9000
    new = []

    # 0) left amber design spine (echoes template's left blocks)
    new.append(mk_sp(sid, 'CovSpine', cm(1.1), cm(2.2), cm(0.16), cm(12.5),
                     fill=AMBER, line=None))
    sid += 1

    # 1) faint watermark benzene behind the title (cream, very low alpha)
    wm, sid = benz(sid, cm(7), cm(9.2), cm(15), CREAM, 11000, 11000)
    new += wm

    # 2) cream title panel (behind title text)
    new.append(mk_sp(sid, 'CovTitlePanel', cm(1.3), cm(5.9), cm(19), cm(3.8),
                     fill=CREAM, line=None, round_=True))
    sid += 1

    # 3) amber period tag panel (behind period text)
    new.append(mk_sp(sid, 'CovPeriodPanel', cm(1.6), cm(13.9), cm(4.2),
                     cm(1.1), fill=AMBER, line=None, round_=True))
    sid += 1

    # 4) original cover TEXT, rebuilt with explicit colors (no inherited fill)
    new.append(mk_text(sid, 'CovEyebrow', cm(1.6), cm(2.2), cm(26), cm(1.0),
                       '高中化学人教版（2019）必修第一册', CREAM, 160, False))
    sid += 1
    new.append(mk_text(sid, 'CovChapter', cm(1.6), cm(4.2), cm(26), cm(1.3),
                       '第一章 物质及其变化', AMBER, 220, True))
    sid += 1
    new.append(mk_text(sid, 'CovTitle', cm(1.7), cm(6.4), cm(18), cm(3.0),
                       '物质的分类', GREEN, 540, True))
    sid += 1
    new.append(mk_text(sid, 'CovSub', cm(1.6), cm(11.8), cm(20), cm(1.5),
                       '第一节 物质的分类及转化', CREAM, 220, False))
    sid += 1
    new.append(mk_text(sid, 'CovPeriod', cm(1.7), cm(14.1), cm(8), cm(1.0),
                       '第1课时', CREAM, 180, True))
    sid += 1

    # 5) teacher / date line (new)
    new.append(mk_text(sid, 'CovTeacher', cm(1.6), cm(15.8), cm(26), cm(1.0),
                       '授课教师：____________      日期：20__-__-__',
                       CREAM, 150, False))
    sid += 1

    # 6) top amber bar
    new.append(mk_sp(sid, 'CovTopBar', 0, 0, W, cm(0.35), fill=AMBER,
                     line=None))
    sid += 1

    # 7) bottom green bar
    new.append(mk_sp(sid, 'CovBotBar', 0, H - cm(0.62), W, cm(0.62),
                     fill=GREEN2, line=None))
    sid += 1

    # 8) page number on bottom bar, right
    new.append(mk_text(sid, 'CovPage', W - cm(3.4), H - cm(0.6), cm(3.0),
                       cm(0.5), f'1 / {total_pages}', CREAM, 130, False,
                       align='r'))
    sid += 1

    # 9) benzene hero + satellites + bonds on the right
    hc = (cm(25.5), cm(9.6))
    s1 = (cm(30.4), cm(4.4))
    s2 = (cm(30.8), cm(15.0))
    hero, sid = benz(sid, hc[0], hc[1], cm(8.6), AMBER, 90000, 95000)
    new += hero
    sat1, sid = benz(sid, s1[0], s1[1], cm(3.6), AMBER, 70000, 72000)
    new += sat1
    sat2, sid = benz(sid, s2[0], s2[1], cm(3.2), AMBER, 70000, 72000)
    new += sat2
    b1, sid = bond(sid, 'CovBond', hc, s1, 13000, AMBER, 70000)
    if b1 is not None:
        new.append(b1)
    b2, sid = bond(sid, 'CovBond', hc, s2, 13000, AMBER, 70000)
    if b2 is not None:
        new.append(b2)

    for el in new:
        sp_tree.append(el)

    # dark green background
    bg = etree.Element(q(P, 'bg'))
    bgpr = etree.SubElement(bg, q(P, 'bgPr'))
    sf = etree.SubElement(bgpr, q(A, 'solidFill'))
    sc = etree.SubElement(sf, q(A, 'srgbClr'))
    sc.set('val', GREEN)
    etree.SubElement(bgpr, q(A, 'effectLst'))
    cSld.insert(0, bg)

    t.write(str(sp_path), encoding='ascii', xml_declaration=True)
    print(f'cover rebuilt: bg={GREEN}, shapes={len(new)}, all text fresh')


if __name__ == '__main__':
    d = sys.argv[1] if len(sys.argv) > 1 else '.'
    tp = int(sys.argv[2]) if len(sys.argv) > 2 else 31
    main(d, tp)
