# -*- coding: utf-8 -*-
r"""卷级后处理补丁：图片「放大到 dpi 许可上限」，改善排版观感（幂等）。

背景（2026-10-14 卷 XVII 实测）：
  构建器 `build_volX_zhenti.py` 的 `CAP_ORG = {"land":(8.4,5.2),"port":(4.8,6.8),"sq":(6.0,6.0)}`
  按**朝向**给目标尺寸，再由 `apply_dpi_cap` 按「150dpi 上限」**只缩不放**。
  结果：源图 px 偏小的排得极小（如 3.08×1.29cm），与相邻大图（8.4cm）观感悬殊。

本补丁：在**保证 ≥150dpi** 的前提下，把图放大到 `min(dpi_cap, CAP_ORG[朝向]×SCALE)`，
  使同类图宽趋于一致、整体更舒展；对已到顶的图无副作用。**幂等**（重复跑不叠加）。

登记：`vol_meta_XVII.json` 的 `post_patches`（由 build_volX_zhenti 自动串行执行并校验退出码）。
"""
import os, re, sys, zipfile, shutil, io
from PIL import Image

SCALE = 1.35                      # 目标放大系数（再受 dpi 上限约束）
MAX_W_CM = 12.0                   # ★ 绝对上限：避免图越出版心（与 vol_img_upscale.py 对齐）
CAP_ORG = {"land": (8.4, 5.2), "port": (4.8, 6.8), "sq": (6.0, 6.0), "page": (16.5, 21.0)}
MIN_DPI = 150.0
EMU_PER_CM = 360000.0

ROOT = r"C:\Obsidion\妙妙屋"
DOCX_DIR = os.path.join(ROOT, '00-首页', '题组Word', '初赛模拟卷', '真题版式')
VOL = 'XVII'
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
    changes = []
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
        if new_cx <= cx and new_cy <= cy:
            continue                       # 已到顶 ⇒ 不动（幂等）
        # ★ 2026-10-15 修（与 vol_img_upscale.py 对齐）：原为 `s = max(new_cx/cx, new_cy/cy)`
        #   ⇒ 扁宽图按**高度**目标放大时**溢出宽度目标**，实测 1350×282px 图被吹到 22.86cm
        #     （> A4 版心 17.2cm，页面上越界）。改为 min ⇒ 宽/高两维都不超目标且不超 dpi 上限。
        s = min(new_cx / cx, new_cy / cy, cap_w / cx, cap_h / cy)
        if s <= 1.001:
            continue
        ncx, ncy = int(cx * s), int(cy * s)
        frag2 = frag.replace('<wp:extent cx="%d" cy="%d"' % (cx, cy),
                             '<wp:extent cx="%d" cy="%d"' % (ncx, ncy))
        frag2 = frag2.replace('<a:ext cx="%d" cy="%d"' % (cx, cy),
                              '<a:ext cx="%d" cy="%d"' % (ncx, ncy))
        if frag2 != frag:
            x = x.replace(frag, frag2, 1)
            changes.append((o, cx / EMU_PER_CM, ncx / EMU_PER_CM, w_px))

    if not changes:
        print('  %s：无需放大（全部已到 dpi 上限或已达目标）' % os.path.basename(path)[:40])
        return 0
    print('  %s：放大 %d 张' % (os.path.basename(path)[:40], len(changes)))
    for o, a, b, px in changes[:8]:
        print('     %-5s %5.2f→%5.2fcm (源%4dpx)' % (o, a, b, px))
    if DRY:
        return 0
    blobs['word/document.xml'] = x.encode('utf-8')
    tmp = path + '.tmp_up'
    with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zo:
        for n in names:
            zo.writestr(n, blobs[n])
    shutil.move(tmp, path)
    return len(changes)


if __name__ == '__main__':
    tot = 0
    for tag in ('学生版', '答案与解析版'):
        p = os.path.join(DOCX_DIR, '初赛模拟卷%s（非有机·%s·真题版式）.docx' % (VOL, tag))
        if os.path.isfile(p):
            tot += patch(p)
    print('  图片放大补丁：共 %d 张%s' % (tot, '（dry）' if DRY else ''))
