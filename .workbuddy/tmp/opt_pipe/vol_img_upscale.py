# -*- coding: utf-8 -*-
r"""卷级后处理补丁（通用版，--vol 指定卷）：图片「放大到 dpi 许可上限」，改善排版观感（幂等）。

背景（2026-10-14 卷 XVII 实测）：
  构建器 `build_volX_zhenti.py` 的 `CAP_ORG = {"land":(8.4,5.2),"port":(4.8,6.8),"sq":(6.0,6.0)}`
  按**朝向**给目标尺寸，再由 `apply_dpi_cap` 按「150dpi 上限」**只缩不放**。
  结果：源图 px 偏小的排得极小（如 3.08×1.29cm），与相邻大图（8.4cm）观感悬殊。

本补丁：在**保证 ≥150dpi** 的前提下，把图放大到 `min(dpi_cap, CAP_ORG[朝向]×SCALE)`，
  使同类图宽趋于一致、整体更舒展；对已到顶的图无副作用。**幂等**（重复跑不叠加）。

登记：`vol_meta_<VOL>.json` 的 `post_patches`（由 build_volX_zhenti 自动串行执行并校验退出码）。
"""
import os, re, sys, zipfile, shutil, io
from PIL import Image

SCALE = 1.35                      # 目标放大系数（再受 dpi 上限约束）
MAX_W_CM = 12.0                   # ★ 绝对上限：避免图占满行宽、与正文比例失衡
CAP_ORG = {"land": (8.4, 5.2), "port": (4.8, 6.8), "sq": (6.0, 6.0), "page": (16.5, 21.0)}
MIN_DPI = 150.0
EMU_PER_CM = 360000.0

ROOT = r"C:\Obsidion\妙妙屋"
DOCX_DIR = os.path.join(ROOT, '00-首页', '题组Word', '初赛模拟卷', '真题版式')
VOL = 'XVII'
for _i, _a in enumerate(sys.argv):
    if _a == '--vol' and _i + 1 < len(sys.argv):
        VOL = sys.argv[_i + 1]
DRY = '--dry' in sys.argv


def orient(w_px, h_px):
    if w_px >= 1700 and h_px >= 1700:
        return 'page'
    r = w_px / float(h_px)
    if r >= 1.25:
        return 'land'
    if r <= 0.8:
        return 'port'
    return 'sq'


def cell_caps(x):
    """★ 2026-10-15：求「表格单元格内 <w:drawing> 片段 → 可用宽度(twips)」映射。

    病根：本补丁按朝向目标尺寸放大，**不知图是否在表格单元格内** ⇒ 三列并排图（列宽 5.73cm）
          被放大到 8.10cm，超出单元格 ⇒ Word/LO **裁切右缘**（实测 XIp 第 6 题 D/E/F/B 图右缘被切）。
    治法：逐行累加 gridCol 得每列宽（含 gridSpan），单元格内图的目标宽不得超该列宽。
    """
    caps = {}
    for mt in re.finditer(r'<w:tbl>.*?</w:tbl>', x, re.S):
        tbl = mt.group(0)
        cols = [int(c) for c in re.findall(r'<w:gridCol w:w="(\d+)"', tbl)]
        if not cols:
            continue
        # ★ 单元格左右内边距（未显式设 tblCellMar 时 Word 默认 108 twips/侧）
        marL = marR = 108
        mm2 = re.search(r'<w:tblCellMar>.*?</w:tblCellMar>', tbl, re.S)
        if mm2:
            ml = re.search(r'<w:left w:w="(\d+)"', mm2.group(0))
            mr2 = re.search(r'<w:right w:w="(\d+)"', mm2.group(0))
            if ml:
                marL = int(ml.group(1))
            if mr2:
                marR = int(mr2.group(1))
        for mr in re.finditer(r'<w:tr\b.*?</w:tr>', tbl, re.S):
            row = mr.group(0)
            ci = 0
            for mc in re.finditer(r'<w:tc\b[^>]*>.*?</w:tc>', row, re.S):
                cell = mc.group(0)
                span = 1
                gs = re.search(r'<w:gridSpan w:val="(\d+)"', cell)
                if gs:
                    span = int(gs.group(1))
                w = sum(cols[ci:ci + span]) if ci < len(cols) else 0
                ci += span
                w = max(0, w - marL - marR)      # 扣除内边距 ⇒ 可用宽
                for md in re.finditer(r'<w:drawing>.*?</w:drawing>', cell, re.S):
                    if w > 0:
                        caps[md.group(0)] = max(caps.get(md.group(0), 0), w)
    return caps


def patch(path):
    z = zipfile.ZipFile(path)
    names = z.namelist()
    blobs = {n: z.read(n) for n in names}
    z.close()
    x = blobs['word/document.xml'].decode('utf-8')
    rels = blobs['word/_rels/document.xml.rels'].decode('utf-8')
    rid2f = {m.group(1): m.group(2) for m in re.finditer(r'Id="(rId\d+)"[^>]*Target="media/([^"]+)"', rels)}

    # 逐 drawing 片段处理
    frags = re.findall(r'<w:drawing>.*?</w:drawing>', x, re.S)
    caps = cell_caps(x)
    changes = []
    shrinks = []
    for frag in frags:
        m = re.search(r'<wp:extent cx="(\d+)" cy="(\d+)"', frag)
        r = re.search(r'r:embed="(rId\d+)"', frag)
        if not (m and r):
            continue
        cx, cy = int(m.group(1)), int(m.group(2))
        name = 'word/media/' + rid2f.get(r.group(1), '')
        if name not in blobs:
            continue
        try:
            im = Image.open(io.BytesIO(blobs[name]))
            w_px, h_px = im.size
        except Exception:
            continue
        o = orient(w_px, h_px)
        cap_w = w_px / MIN_DPI * 2.54 * EMU_PER_CM
        cap_h = h_px / MIN_DPI * 2.54 * EMU_PER_CM
        tgt_w = min(CAP_ORG[o][0] * SCALE, MAX_W_CM) * EMU_PER_CM
        tgt_h = min(CAP_ORG[o][1] * SCALE, MAX_W_CM) * EMU_PER_CM
        # 目标尺寸，再与 dpi 上限取 min（保证 ≥150dpi）
        new_cx = int(min(tgt_w, cap_w))
        new_cy = int(min(tgt_h, cap_h))
        # ★ 单元格宽度上限（治「表格内图被裁切」）
        cell_tw = caps.get(frag, 0)
        cell_emu = cell_tw / 567.0 * EMU_PER_CM if cell_tw else 0
        enlarge = new_cx > cx or new_cy > cy
        shrink = bool(cell_emu and cx > cell_emu)
        if not enlarge and not shrink:
            continue                       # 已到顶且不超列宽 ⇒ 不动（幂等）
        # 缩放比取 min：保证**宽/高两维都不超**目标，且都不超 dpi 上限
        # （曾用 max ⇒ 按高度放大时会溢出宽度目标，实测 8.40cm 图被放到 14.82cm）
        s = min(new_cx / cx, new_cy / cy, cap_w / cx, cap_h / cy)
        if cell_emu:
            s = min(s, cell_emu / cx)      # ★ 单元格内不超列宽（必要时**缩小**治裁切）
        ncx, ncy = int(cx * s), int(cy * s)
        if ncx == cx and ncy == cy:
            continue
        frag2 = frag.replace('<wp:extent cx="%d" cy="%d"' % (cx, cy),
                             '<wp:extent cx="%d" cy="%d"' % (ncx, ncy))
        frag2 = frag2.replace('<a:ext cx="%d" cy="%d"' % (cx, cy),
                              '<a:ext cx="%d" cy="%d"' % (ncx, ncy))
        if frag2 != frag:
            x = x.replace(frag, frag2, 1)
            if ncx < cx:
                shrinks.append((o, cx / EMU_PER_CM, ncx / EMU_PER_CM, w_px))
            else:
                changes.append((o, cx / EMU_PER_CM, ncx / EMU_PER_CM, w_px))

    if not changes and not shrinks:
        print('  %s：无需放大（全部已到 dpi 上限或已达目标）' % os.path.basename(path)[:40])
        return 0
    if changes:
        print('  %s：放大 %d 张' % (os.path.basename(path)[:40], len(changes)))
        for o, a, b, px in changes[:8]:
            print('     %-5s %5.2f→%5.2fcm (源%4dpx)' % (o, a, b, px))
    if shrinks:
        print('  %s：★收窄至列宽 %d 张（治表格裁切）' % (os.path.basename(path)[:40], len(shrinks)))
        for o, a, b, px in shrinks[:8]:
            print('     表格内 %5.2f→%5.2fcm (源%4dpx)' % (a, b, px))
    if DRY:
        return 0
    blobs['word/document.xml'] = x.encode('utf-8')
    tmp = path + '.tmp_up'
    with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zo:
        for n in names:
            zo.writestr(n, blobs[n])
    shutil.move(tmp, path)
    return len(changes) + len(shrinks)


if __name__ == '__main__':
    tot = 0
    for tag in ('学生版', '答案与解析版'):
        p = os.path.join(DOCX_DIR, '初赛模拟卷%s（非有机·%s·真题版式）.docx' % (VOL, tag))
        if os.path.isfile(p):
            tot += patch(p)
    print('  图片放大补丁：共 %d 张%s' % (tot, '（dry）' if DRY else ''))
