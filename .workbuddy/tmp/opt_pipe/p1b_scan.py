# -*- coding: utf-8 -*-
r"""P1-b 机器初筛（只读）：对 X/XI/XIp/XIV/XV 扫已知缺陷类。
① 图注连排  ② 孤立页码行  ③ 图注-正文粘连  ④ 图片边缘截断  ⑤ 图幅偏小（dpi 余量）"""
import os, re, io, zipfile, glob
import numpy as np
from PIL import Image

os.chdir(r'C:\Obsidion\妙妙屋')
EMU = 360000.0
VOLS = ['X', 'XI', 'XIp', 'XIV', 'XV']
IMGDIRS = [r for r, d, f in os.walk('04-题库') if os.path.basename(r) == 'images']

def find_img(name):
    b = os.path.basename(name)
    for d in IMGDIRS:
        p = os.path.join(d, b)
        if os.path.isfile(p):
            return p
    return None

print('=' * 96)
for V in VOLS:
    print('◆ 卷 %s' % V)
    for tag, pat in [('学生版', '*学生版*'), ('答案版', '*答案*')]:
        md = '04-题库/初赛模拟卷%s（非有机·%s）.md' % (V, tag)
        if not os.path.isfile(md):
            continue
        t = io.open(md, encoding='utf-8-sig').read()
        # ① 图注连排
        lian = len(re.findall(r'(?m)^图\s*\d+\s*\n图\s*\d+', t))
        # ② 孤立页码行（纯数字行，前后空行）
        lone = len(re.findall(r'(?m)^\s*\d{1,3}\s*$', t))
        # ③ 图注行后紧跟非空正文（无空行）
        stick = len(re.findall(r'(?m)^图\s*\d+\s*\n(?=\S)', t))
        print('   %-4s 图注连排 %d ｜ 孤立数字行 %d ｜ 图注粘连正文 %d' % (tag, lian, lone, stick))
    # ④⑤ 从 docx 取图尺寸与 dpi 余量（学生版）
    f = glob.glob('00-首页/题组Word/初赛模拟卷/真题版式/初赛模拟卷%s（*学生版*.docx' % V)
    if not f:
        continue
    z = zipfile.ZipFile(f[0])
    x = z.read('word/document.xml').decode('utf-8')
    rels = z.read('word/_rels/document.xml.rels').decode('utf-8')
    rid2f = {m.group(1): m.group(2) for m in re.finditer(r'Id="(rId\d+)"[^>]*Target="media/([^"]+)"', rels)}
    trunc = 0; small = []
    for p in re.findall(r'<w:p[ >].*?</w:p>', x, re.S):
        if '<w:drawing' not in p:
            continue
        m = re.search(r'<wp:extent cx="(\d+)" cy="(\d+)"', p); r = re.search(r'r:embed="(rId\d+)"', p)
        if not (m and r):
            continue
        w = float(m.group(1)) / EMU
        nm = rid2f.get(r.group(1), '')
        fp = find_img(nm) if nm else None
        if not fp:
            continue
        try:
            a = np.asarray(Image.open(fp).convert('L')); h, ww = a.shape
            px = ww
        except Exception:
            continue
        # ⑤ dpi 余量
        cap = px / 150 * 2.54
        if cap > w * 1.35:
            small.append((w, cap, px))
        # ④ 边缘截断
        try:
            rr = (a < 120).mean(axis=1)
            if rr[0] > 0.15 or rr[-1] > 0.15:
                trunc += 1
        except Exception:
            pass
    print('   docx: 可放大>1.35x 的图 %d 张 ｜ 边缘截断候选 %d 张' % (len(small), trunc))
    for w, cap, px in small[:5]:
        print('        %5.2fcm → 上限 %5.2fcm (源 %dpx)' % (w, cap, px))
print('=' * 96)
