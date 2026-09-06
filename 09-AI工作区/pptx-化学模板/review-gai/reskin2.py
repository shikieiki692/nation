# -*- coding: utf-8 -*-
"""reskin2.py - spec-driven reskin engine (editorial green/cream).

Why it generalizes (vs brittle reskin.py):
  * canvas read from <p:sldSz>; all shell coords are canvas proportions -> any size
  * iterates ALL slideMasters + slideLayouts
  * title/section pages detected by ROBUST signals:
      - a full-bleed BACKGROUND IMAGE (covers use photos), or
      - first / last slide (cover / end), or
      - a layout name in `title_layout_names`
    -> no fragile placeholder-type guessing
  * source master top banner pic removed by SEMANTICS (cx>0.8W & cy<0.15H); no assert
  * font mapping: ea->Microsoft YaHei; latin only normalizes serif/old fonts to Arial;
    skips math/symbol fonts -> no line wrap
  * shell placed AFTER the full-bleed background but BEFORE content -> visible, never occludes
  * title/section pages: drop the bg image, full-bleed green + all text to cream (own design)
  * content pages with a dark/colored bg are preserved

Zero content change: only background, decorative shapes, palette, font name/color.
Usage: python reskin2.py <unpacked_dir> [--config template.yaml]
"""
import pathlib
import re
import sys

import yaml
from lxml import etree

A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'


def q(ns, tag):
    return f'{{{ns}}}{tag}'


def lum(hexc):
    h = hexc.lstrip('#')
    if len(h) != 6:
        return 1.0
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return (0.299 * r + 0.587 * g + 0.114 * b) / 255.0


def rect(sid, name, x, y, cx, cy, fill):
    return etree.fromstring(
        f'<p:sp xmlns:p="{P}" xmlns:a="{A}">'
        f'<p:nvSpPr><p:cNvPr id="{sid}" name="{name}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
        f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
        f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill><a:ln><a:noFill/></a:ln></p:spPr>'
        f'<p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:endParaRPr lang="zh-CN"/></a:p></p:txBody>'
        f'</p:sp>')


def text(sid, name, x, y, cx, cy, txt, color, size):
    return etree.fromstring(
        f'<p:sp xmlns:p="{P}" xmlns:a="{A}">'
        f'<p:nvSpPr><p:cNvPr id="{sid}" name="{name}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
        f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr>'
        f'<p:txBody><a:bodyPr wrap="none" lIns="0" tIns="0" rIns="0" bIns="0" rtlCol="0" anchor="t"/>'
        f'<a:lstStyle/><a:p><a:pPr algn="r"/>'
        f'<a:r><a:rPr lang="zh-CN" altLang="en-US" sz="{size}" dirty="0">'
        f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
        f'<a:latin typeface="Arial"/><a:ea typeface="&#24494;&#36719;&#38597;&#40657;"/></a:rPr>'
        f'<a:t>{txt}</a:t></a:r></a:p></p:txBody></p:sp>')


def get_canvas(pres_path):
    s = pres_path.read_text(encoding='utf-8')
    m = re.search(r'<p:sldSz cx="(\d+)" cy="(\d+)"', s)
    return (int(m.group(1)), int(m.group(2))) if m else (9144000, 5143500)


def fix_fonts(root, cfg):
    ea_to = cfg['fonts']['ea']
    latin_to = cfg['fonts']['latin_to']
    replace = set(cfg['fonts'].get('latin_replace', []))
    skip = set(cfg['fonts'].get('skip', []))
    for el in root.iter():
        if etree.QName(el).localname not in ('rPr', 'defRPr', 'endParaRPr'):
            continue
        if el.tag != q(A, 'rPr') and el.tag != q(A, 'defRPr') and el.tag != q(A, 'endParaRPr'):
            continue
        ea = el.find(q(A, 'ea'))
        cur_ea = ea.get('typeface') if ea is not None else None
        if cur_ea not in skip:
            if ea is None:
                ea = etree.SubElement(el, q(A, 'ea'))
            ea.set('typeface', ea_to)
        lat = el.find(q(A, 'latin'))
        cur_lat = lat.get('typeface') if lat is not None else None
        if cur_lat in skip:
            continue
        if cur_lat in replace:
            if lat is None:
                lat = etree.SubElement(el, q(A, 'latin'))
            lat.set('typeface', latin_to)


def clean_master_banner(mroot, W, H):
    removed = 0
    for pic in list(mroot.iter(q(P, 'pic'))):
        xfrm = pic.find(f'.//{q(A, "xfrm")}')
        if xfrm is None:
            continue
        ext = xfrm.find(q(A, 'ext'))
        if ext is None:
            continue
        cx, cy = int(ext.get('cx')), int(ext.get('cy'))
        if cx > 0.8 * W and cy < 0.15 * H:
            pic.getparent().remove(pic)
            removed += 1
    return removed


def add_master_shell(mroot, cfg, W, H, sid0):
    g = cfg['geometry']
    c = cfg['colors']
    sp_tree = mroot.find(f'.//{q(P, "spTree")}')
    sid = sid0
    els = []
    sid += 1; els.append(rect(sid, 'SkinSpine',
                              int(g['spine']['x'] * W), int(g['spine']['y'] * H),
                              int(g['spine']['w'] * W), int(g['spine']['h'] * H), c['green']))
    sid += 1; els.append(rect(sid, 'SkinDot',
                              int(g['green_dot']['x'] * W), int(g['green_dot']['y'] * H),
                              int(g['green_dot']['w'] * W), int(g['green_dot']['h'] * H), c['green']))
    sid += 1; els.append(rect(sid, 'SkinTitleRule',
                              int(g['amber_rule']['x'] * W), int(g['amber_rule']['y'] * H),
                              int(g['amber_rule']['w'] * W), int(g['amber_rule']['h'] * H), c['amber']))
    for el in els:
        sp_tree.insert(2, el)
    csld = mroot.find(q(P, 'cSld'))
    bg = csld.find(q(P, 'bg'))
    frag = (f'<p:bg xmlns:p="{P}" xmlns:a="{A}"><p:bgPr>'
            f'<a:solidFill><a:srgbClr val="{c["paper"]}"/></a:solidFill>'
            f'<a:effectLst/></p:bgPr></p:bg>')
    if bg is None:
        csld.insert(0, etree.fromstring(frag))
    else:
        bp = bg.find(q(P, 'bgPr'))
        if bp is not None:
            sf = bp.find(q(A, 'solidFill'))
            if sf is None:
                sf = etree.SubElement(bp, q(A, 'solidFill'))
            sc = sf.find(q(A, 'srgbClr'))
            if sc is None:
                sc = etree.SubElement(sf, q(A, 'srgbClr'))
            sc.set('val', c['paper'])
    return sid


def set_bg(csld, hexc):
    bg = csld.find(q(P, 'bg'))
    frag = (f'<p:bg xmlns:p="{P}" xmlns:a="{A}"><p:bgPr>'
            f'<a:solidFill><a:srgbClr val="{hexc}"/></a:solidFill>'
            f'<a:effectLst/></p:bgPr></p:bg>')
    if bg is None:
        csld.insert(0, etree.fromstring(frag))
    else:
        bp = bg.find(q(P, 'bgPr'))
        if bp is None:
            bg.insert(0, etree.fromstring(frag))
            return
        sf = bp.find(q(A, 'solidFill'))
        if sf is None:
            sf = etree.SubElement(bp, q(A, 'solidFill'))
        for old in list(sf):
            sf.remove(old)
        sc = etree.SubElement(sf, q(A, 'srgbClr'))
        sc.set('val', hexc)


def slide_bg_hex(csld):
    bg = csld.find(q(P, 'bg'))
    if bg is None:
        return None
    bp = bg.find(q(P, 'bgPr'))
    if bp is None:
        return None
    sf = bp.find(q(A, 'solidFill'))
    if sf is None:
        return None
    sc = sf.find(q(A, 'srgbClr'))
    return sc.get('val') if sc is not None else None


def recolor_all_text_cream(root, hexc):
    n = 0
    for r in root.iter(q(A, 'r')):
        rpr = r.find(q(A, 'rPr'))
        if rpr is None:
            continue
        sf = rpr.find(q(A, 'solidFill'))
        if sf is None:
            sf = etree.SubElement(rpr, q(A, 'solidFill'))
        for old in list(sf):
            sf.remove(old)
        sc = etree.SubElement(sf, q(A, 'srgbClr'))
        sc.set('val', hexc)
        n += 1
    return n


def first_fullbleed(sp_tree, W, H):
    for el in sp_tree:
        tag = etree.QName(el).localname
        if tag not in ('sp', 'pic', 'graphicFrame'):
            continue
        xfrm = el.find(f'.//{q(A, "xfrm")}')
        if xfrm is None:
            continue
        off = xfrm.find(q(A, 'off'))
        ext = xfrm.find(q(A, 'ext'))
        if off is None or ext is None:
            continue
        x, y, cx, cy = int(off.get('x')), int(off.get('y')), int(ext.get('cx')), int(ext.get('cy'))
        if x <= 2000 and y <= 2000 and cx >= W * 0.98 and cy >= H * 0.98:
            is_img = el.find(f'.//{q(A, "blip")}') is not None
            return el, is_img
    return None, False


def insert_after_bg(sp_tree, el, W, H):
    fb, _ = first_fullbleed(sp_tree, W, H)
    if fb is not None:
        idx = list(sp_tree).index(fb)
        sp_tree.insert(idx + 1, el)
    else:
        sp_tree.insert(2, el)


def layout_name(slide_path, base):
    rels = slide_path.parent / '_rels' / (slide_path.name + '.rels')
    try:
        rs = rels.read_text(encoding='utf-8')
        m = re.search(r'Target="([^"]*slideLayout\d+\.xml)"', rs)
        if m:
            lp = base / 'ppt' / 'slideLayouts' / m.group(1).split('/')[-1]
            if lp.exists():
                nm = re.search(r'<p:cSld[^>]*?name="([^"]+)"', lp.read_text(encoding='utf-8'))
                if nm:
                    return nm.group(1)
    except Exception:
        pass
    return ''


def is_title_page(sp_path, base, idx, total, cfg):
    pages = cfg['pages']
    tree = etree.parse(str(sp_path)).getroot().find(f'.//{q(P, "spTree")}')
    fb, is_img = first_fullbleed(tree, *get_canvas(base / 'ppt/presentation.xml'))
    if fb is not None and is_img:
        return True
    if idx == 1:
        return True
    if pages.get('title_last_slide') and idx == total:
        return True
    names = pages.get('title_layout_names', []) or []
    if layout_name(sp_path, base) in names:
        return True
    return False


def clean_external_rels(root_dir):
    """Remove orphaned EXTERNAL links (e.g. file:///D:\\...png) from master/layout rels."""
    removed = 0
    rels = list(root_dir.glob('ppt/slideMasters/_rels/*.rels')) + \
        list(root_dir.glob('ppt/slideLayouts/_rels/*.rels'))
    for relf in rels:
        try:
            t = etree.parse(str(relf))
        except Exception:
            continue
        r = t.getroot()
        changed = False
        for el in list(r):
            tgt = el.get('Target', '')
            if tgt.startswith('file://') or re.match(r'^[a-zA-Z]:[\\/]', tgt):
                r.remove(el)
                removed += 1
                changed = True
        if changed:
            t.write(str(relf), xml_declaration=True, encoding='UTF-8')
    return removed


def remove_embed_ref(sp_path, rid, root_dir):
    """Drop a relationship (and its media file if now unused) for a removed pic."""
    rels = sp_path.parent / '_rels' / (sp_path.name + '.rels')
    if not rels.exists():
        return
    t = etree.parse(str(rels))
    r = t.getroot()
    target = None
    for el in list(r):
        if el.get('Id') == rid:
            target = el.get('Target')
            r.remove(el)
    t.write(str(rels), xml_declaration=True, encoding='UTF-8')
    if target:
        med = root_dir / 'ppt' / 'media' / pathlib.Path(target).name
        if med.exists():
            # delete only if no other slide/layout/master references it
            needle = pathlib.Path(target).name
            refs = 0
            for f in (list(root_dir.glob('ppt/slides/*.xml')) +
                      list(root_dir.glob('ppt/slideLayouts/*.xml')) +
                      list(root_dir.glob('ppt/slideMasters/*.xml'))):
                if needle in f.read_text(encoding='utf-8', errors='ignore'):
                    refs += 1
            if refs == 0:
                try:
                    med.unlink()
                except Exception:
                    pass


def fix_theme(theme_path, cfg):
    c = cfg['colors']
    s = theme_path.read_text(encoding='utf-8')
    mapping = [('accent1', c['green']), ('accent2', c['green2']), ('accent3', c['amber']),
               ('accent4', '52796F'), ('accent5', '779341'), ('accent6', 'B08968')]
    for tag, color in mapping:
        s = re.sub(r'(<a:%s><a:srgbClr val=")[0-9A-Fa-f]{6}("/>)' % tag,
                   r'\g<1>%s\g<2>' % color, s)
    theme_path.write_text(s, encoding='utf-8')


def main(root_dir, config_path):
    root_dir = pathlib.Path(root_dir)
    cfg = yaml.safe_load(pathlib.Path(config_path).read_text(encoding='utf-8'))
    colors = cfg['colors']
    geom = cfg['geometry']
    pages = cfg['pages']
    W, H = get_canvas(root_dir / 'ppt/presentation.xml')
    print(f'canvas = {W} x {H}')

    sid = 10000
    ext_removed = clean_external_rels(root_dir)
    masters = sorted(root_dir.glob('ppt/slideMasters/slideMaster*.xml'))
    layouts = sorted(root_dir.glob('ppt/slideLayouts/slideLayout*.xml'))
    banner_removed = 0
    for mp in masters + layouts:
        t = etree.parse(str(mp))
        r = t.getroot()
        banner_removed += clean_master_banner(r, W, H)
        sid = add_master_shell(r, cfg, W, H, sid)
        fix_fonts(r, cfg)
        t.write(str(mp), encoding='ascii', xml_declaration=True)
    print(f'masters={len(masters)} layouts={len(layouts)} top-banner-removed={banner_removed} external-rels-removed={ext_removed}')

    fix_theme(root_dir / 'ppt/theme/theme1.xml', cfg)
    print('theme accent updated')

    slides = sorted((root_dir / 'ppt/slides').glob('slide*.xml'),
                    key=lambda p: int(re.search(r'\d+', p.name).group()))
    total = len(slides)
    title_count = 0
    for i, sp_path in enumerate(slides, 1):
        t = etree.parse(str(sp_path))
        r = t.getroot()
        csld = r.find(q(P, 'cSld'))
        sp_tree = r.find(f'.//{q(P, "spTree")}')
        is_title = is_title_page(sp_path, root_dir, i, total, cfg)

        if is_title and pages.get('title_full_bleed'):
            # drop full-bleed bg image if present (and its orphaned rel/media)
            fb, is_img = first_fullbleed(sp_tree, W, H)
            if fb is not None:
                if is_img:
                    blip = fb.find(f'.//{q(A, "blip")}')
                    rid = blip.get(f'{{{R}}}embed') if blip is not None else None
                    if rid:
                        remove_embed_ref(sp_path, rid, root_dir)
                fb.getparent().remove(fb)
            set_bg(csld, colors['green'])
            if pages.get('title_text_to_cream'):
                recolor_all_text_cream(r, colors['cream'])
            title_count += 1
            bg_dark = True
        else:
            cur = slide_bg_hex(csld)
            if cur and lum(cur) < pages['dark_luminance_threshold'] and pages.get('respect_dark_content_bg'):
                bg_dark = True
            else:
                set_bg(csld, colors['paper'])
                bg_dark = False

        p = i / total
        hprog = int(p * H)
        yprog = H - hprog
        line_col = colors['line_dark'] if bg_dark else colors['line_light']
        page_col = colors['page_dark'] if bg_dark else colors['page_light']
        sid += 1
        insert_after_bg(sp_tree, rect(sid, 'SkinProgress',
                                      int(geom['progress']['x'] * W), yprog,
                                      int(geom['progress']['w'] * W), hprog, colors['amber']), W, H)
        sid += 1
        insert_after_bg(sp_tree, rect(sid, 'SkinFooter',
                                      int(geom['footer_div']['x'] * W), int(geom['footer_div']['y'] * H),
                                      int(geom['footer_div']['w'] * W), int(geom['footer_div']['h'] * H), line_col), W, H)
        sid += 1
        pn = geom['page_num']
        insert_after_bg(sp_tree, text(sid, 'SkinPageNum',
                                      int(pn['x'] * W), int(pn['y'] * H),
                                      int(pn['w'] * W), int(pn['h'] * H),
                                      f'{i} / {total}', page_col, int(pn['size'])), W, H)
        fix_fonts(r, cfg)
        t.write(str(sp_path), encoding='ascii', xml_declaration=True)

    print(f'slides={total} title/section(满版墨绿)={title_count} shell+fonts applied')

    for f in list((root_dir / 'ppt/notesSlides').glob('*.xml')) + [root_dir / 'ppt/presentation.xml']:
        t = etree.parse(str(f))
        fix_fonts(t.getroot(), cfg)
        t.write(str(f), encoding='ascii', xml_declaration=True)
    print('notesSlides/presentation fonts unified')
    print('DONE')


if __name__ == '__main__':
    args = sys.argv[1:]
    d = None
    conf = 'template.yaml'
    k = 0
    while k < len(args):
        if args[k] == '--config':
            conf = args[k + 1]; k += 2
        else:
            d = args[k]; k += 1
    main(d, conf)
