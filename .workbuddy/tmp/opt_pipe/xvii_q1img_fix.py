# -*- coding: utf-8 -*-
r"""卷 XVII 第 1 题补图：从 HiChO 源 PDF 提取缺失的 3 张图（源图块 4/5/6）。

源卷（第39届 HiChO 第 5 题「高压氮化物」）共 8 图：
  图1/图2/图3（Fe/C 晶胞） 图3'（ZnN₂三方）  图4（ZnN₂正交）★缺 图5（化合物D）★缺
  图6（化合物E）★缺  图7（化合物F ＋ La 小图）
卷内建卡时只落了 图1/2/3/3'/7 —— 图4/5/6 **丢失**（但图注 4/5/6/7 都留着 ⇒ 被合并成「图 4～图 7」）。
本脚本按 PDF 内嵌原图**无损提取**，按库规范命名（sha256 前 64 位 + .jpg），插入卷 md，并修正图注。
"""
import fitz, glob, os, io, hashlib, re, shutil, datetime

ROOT = r"C:\Obsidion\妙妙屋"
SRC = glob.glob(os.path.join(ROOT, '06-外部资料导入/OCR/chemy/_mineru_out/第39届HiChO化学奥林匹克(初赛)模拟试题 1 v1.2/auto/*origin.pdf'))[0]
IMG_DIR = os.path.join(ROOT, '04-题库', '2026机构初赛模拟题', 'chemy', 'images')
BAK = os.path.join(ROOT, '.workbuddy/tmp/opt_pipe/_bak/xvii_q1img_%s' % datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
os.makedirs(BAK, exist_ok=True)

# 源 p3 的图块（rect 见探查输出）：图4/5/6
TARGETS = [(65, '图4'), (66, '图5'), (67, '图6')]

d = fitz.open(SRC)
pg = d[2]
saved = []
for xref, tag in TARGETS:
    rects = pg.get_image_rects(xref)
    if not rects:
        print('!! 未找到 xref=%d' % xref); continue
    r = rects[0]
    # 从 PDF 取内嵌原图（无损）
    info = [i for i in pg.get_images(full=True) if i[0] == xref][0]
    base = d.extract_image(xref)
    data = base['image']
    ext = base['ext']
    h = hashlib.sha256(data).hexdigest()
    fn = '%s.%s' % (h, ext if ext in ('jpg', 'jpeg', 'png') else 'jpg')
    with open(os.path.join(IMG_DIR, fn), 'wb') as f:
        f.write(data)
    saved.append((tag, fn, base['width'], base['height']))
    print('%s → %s  (%dx%d, %d bytes)  源 rect=(%.0f,%.0f,%.0f,%.0f)'
          % (tag, fn[:20], base['width'], base['height'], len(data), r.x0, r.y0, r.x1, r.y1))
d.close()

# 插入卷 md（两版）
NAMES = {t: fn for t, fn, _, _ in saved}
for vol_tag in ['学生版', '答案版']:
    p = os.path.join(ROOT, '04-题库', '初赛模拟卷XVII（非有机·%s）.md' % vol_tag)
    txt = io.open(p, encoding='utf-8', newline='').read()
    shutil.copy2(p, os.path.join(BAK, os.path.basename(p)))
    # ① 在原「图 4/5/6/7」四连注处重建：图4 + 图5 + 图6 + 图7
    old_block = re.compile(r'(!\[\[ce154830[^\]]+\]\]\n)图 4～图 7\n')
    def repl(m):
        return ('![[%s]]\n图 4\n\n![[%s]]\n图 5\n\n![[%s]]\n图 6\n\n%s图 7\n'
                % (NAMES['图4'], NAMES['图5'], NAMES['图6'], m.group(1)))
    new, n = old_block.subn(repl, txt)
    print('%s：图注块替换 %d 处' % (vol_tag, n))
    if n:
        io.open(p, 'w', encoding='utf-8', newline='').write(new)
print('备份：', BAK)
