# -*- coding: utf-8 -*-
"""reskin.py — 源课件最小化换皮（不碰任何现有 shape 的文字/位置/大小/图片）。

改动范围（仅此五类）：
1. 背景：每页 slide 加 <p:bg> 米白 FAF7F0；master bgPr 同步米白
2. 顶部横幅：master 里的全宽照片 pic（9144000×563196）→ 同尺寸纯色墨绿 1B4332 矩形
3. theme1.xml accent1-6 → 设计色板
4. 所有 a:rPr/a:defRPr/a:endParaRPr：latin→Times New Roman，ea→微软雅黑
   （slides + slideLayouts + slideMasters + notesSlides + presentation.xml）
5. 每页追加外壳 3 件（新 id，不动旧 shape）：左侧墨绿竖条+橙黄进度段、底部分隔线、右下页码

用法：python reskin.py <unpacked_dir>
"""
import pathlib
import re
import sys

from lxml import etree

A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
NS = {'a': A, 'p': P}
LATIN = 'Times New Roman'
EA = '微软雅黑'
BG = 'FAF7F0'
GREEN = '1B4332'
ORANGE = 'E8A33D'
GRAY = '6B7280'
LINE = 'DDE5DD'

CX, CY = 9144000, 5143500  # 720×405pt


def q(ns, tag):
    return f'{{{ns}}}{tag}'


# ---------- 4. 字体 ----------
def fix_fonts(root):
    n = 0
    for el in root.iter():
        if el.tag not in (q(A, 'rPr'), q(A, 'defRPr'), q(A, 'endParaRPr')):
            continue
        # latin
        lat = el.find(q(A, 'latin'))
        if lat is None:
            lat = etree.SubElement(el, q(A, 'latin'))
            _move_before(el, lat, ('ea', 'cs', 'sym', 'hlinkClick', 'hlinkMouseOver', 'rtl', 'extLst'))
        lat.set('typeface', LATIN)
        # ea
        ea = el.find(q(A, 'ea'))
        if ea is None:
            ea = etree.SubElement(el, q(A, 'ea'))
            _move_before(el, ea, ('cs', 'sym', 'hlinkClick', 'hlinkMouseOver', 'rtl', 'extLst'))
        ea.set('typeface', EA)
        n += 1
    return n


def _move_before(parent, el, later_tags):
    """把 el 移到指定后续标签之前（满足 rPr 子元素 schema 顺序）。"""
    parent.remove(el)
    for i, ch in enumerate(parent):
        ln = etree.QName(ch).localname
        if ln in later_tags:
            parent.insert(i, el)
            return
    parent.append(el)


# ---------- 5. 外壳 shape ----------
def _sp_base(sid, name, x, y, cx, cy, fill):
    return (
        f'<p:sp xmlns:p="{P}" xmlns:a="{A}">'
        f'<p:nvSpPr><p:cNvPr id="{sid}" name="{name}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
        f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
        f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill><a:ln><a:noFill/></a:ln></p:spPr>'
        f'<p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:endParaRPr lang="zh-CN"/></a:p></p:txBody>'
        f'</p:sp>')


def _sp_text(sid, name, x, y, cx, cy, text):
    return (
        f'<p:sp xmlns:p="{P}" xmlns:a="{A}">'
        f'<p:nvSpPr><p:cNvPr id="{sid}" name="{name}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
        f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr>'
        f'<p:txBody><a:bodyPr wrap="none" lIns="0" tIns="0" rIns="0" bIns="0" rtlCol="0" anchor="t"/><a:lstStyle/>'
        f'<a:p><a:pPr algn="r"/>'
        f'<a:r><a:rPr lang="zh-CN" altLang="en-US" sz="1000" dirty="0">'
        f'<a:solidFill><a:srgbClr val="{GRAY}"/></a:solidFill>'
        f'<a:latin typeface="{LATIN}"/><a:ea typeface="{EA}"/></a:rPr>'
        f'<a:t>{text}</a:t></a:r></a:p></p:txBody>'
        f'</p:sp>')


def add_shell(root, page_no, total):
    sptree = root.find(f'.//{q(P, "spTree")}')
    max_id = max(int(e.get('id')) for e in root.iter() if e.get('id', '').isdigit())
    # 进度段高度：与模板进度条同一公式
    h = round(CY * (0.06 + (page_no - 1) * 0.84 / (total - 1)))
    parts = [
        _sp_base(max_id + 1, 'SkinLeftBar', 0, 0, 101600, CY, GREEN),
        _sp_base(max_id + 2, 'SkinProgress', 0, CY - h, 101600, h, ORANGE),
        _sp_base(max_id + 3, 'SkinDivider', 508000, 4876800, 8128000, 12700, LINE),
        _sp_text(max_id + 4, 'SkinPageNum', 7620000, 4927600, 1016000, 254000, f'{page_no} / {total}'),
    ]
    for frag in parts:
        sptree.append(etree.fromstring(frag))


# ---------- 主流程 ----------
def main(root_dir):
    root_dir = pathlib.Path(root_dir)
    slides = sorted((root_dir / 'ppt/slides').glob('slide*.xml'),
                    key=lambda p: int(re.search(r'\d+', p.name).group()))
    total = len(slides)

    # 2. master：背景米白 + 横幅照片→墨绿矩形
    mp = root_dir / 'ppt/slideMasters/slideMaster1.xml'
    t = etree.parse(str(mp))
    r = t.getroot()
    bgpr = r.find(f'.//{q(P, "bg")}/{q(P, "bgPr")}')
    fill = bgpr.find(q(A, 'solidFill'))
    sc = fill.find(q(A, 'schemeClr'))
    if sc is not None:
        sc.tag = q(A, 'srgbClr')
        sc.attrib.clear()
        sc.set('val', BG)
    banner = None
    for pic in r.iter(q(P, 'pic')):
        xfrm = pic.find(f'.//{q(A, "xfrm")}')
        off = xfrm.find(q(A, 'off')) if xfrm is not None else None
        ext = xfrm.find(q(A, 'ext')) if xfrm is not None else None
        if (ext is not None and int(ext.get('cx')) == 9144000
                and int(ext.get('cy')) == 563196):
            banner = pic
            break
    assert banner is not None, 'master banner pic not found'
    nid = banner.find(f'.//{q(P, "cNvPr")}').get('id')
    sp = etree.fromstring(_sp_base(nid, 'SkinBanner', 0, 3, 9144000, 563196, GREEN))
    banner.getparent().replace(banner, sp)
    fix_fonts(r)
    t.write(str(mp), encoding='ascii', xml_declaration=True)
    print('master: bg→米白, banner→墨绿矩形')

    # 3. theme 色板
    tp = root_dir / 'ppt/theme/theme1.xml'
    s = tp.read_text(encoding='utf-8')
    for tag, color in [('accent1', GREEN), ('accent2', '2D6A4F'), ('accent3', ORANGE),
                       ('accent4', 'B45309'), ('accent5', 'C0392B'), ('accent6', GRAY)]:
        s = re.sub(r'(<a:%s><a:srgbClr val=")[0-9A-Fa-f]{6}("/>)' % tag,
                   r'\g<1>%s\g<2>' % color, s)
    tp.write_text(s, encoding='utf-8')
    print('theme: accent1-6 已换')

    # 4+5. slides：字体 + 背景 + 外壳
    for i, sp_path in enumerate(slides, 1):
        t = etree.parse(str(sp_path))
        r = t.getroot()
        # 1. 背景（cSld 第一个子元素位置）
        csld = r.find(q(P, 'cSld'))
        if csld.find(q(P, 'bg')) is None:
            bg = etree.fromstring(
                f'<p:bg xmlns:p="{P}" xmlns:a="{A}"><p:bgPr>'
                f'<a:solidFill><a:srgbClr val="{BG}"/></a:solidFill><a:effectLst/>'
                f'</p:bgPr></p:bg>')
            csld.insert(0, bg)
        fix_fonts(r)
        add_shell(r, i, total)
        t.write(str(sp_path), encoding='ascii', xml_declaration=True)
    print(f'slides: {total} 页已加背景/外壳/字体')

    # 4. layouts / notesSlides / presentation.xml：仅字体
    for f in list((root_dir / 'ppt/slideLayouts').glob('*.xml')) + \
             list((root_dir / 'ppt/notesSlides').glob('*.xml')) + \
             [root_dir / 'ppt/presentation.xml']:
        t = etree.parse(str(f))
        fix_fonts(t.getroot())
        t.write(str(f), encoding='ascii', xml_declaration=True)
    print('layouts/notesSlides/presentation: 字体已统一')


if __name__ == '__main__':
    main(sys.argv[1])
