# -*- coding: utf-8 -*-
r"""把 render_gate_out 的 PDF 逐页渲染成 PNG（只读）。用法: pdf2png.py <卷> [stu|ans|both]"""
import sys, os, glob
import fitz
os.chdir(r'C:\Obsidion\妙妙屋')
BASE = '.workbuddy/tmp/opt_pipe/render_gate_out'
OUT = '.workbuddy/tmp/opt_pipe/p1b_png'
os.makedirs(OUT, exist_ok=True)

V = sys.argv[1]
which = sys.argv[2] if len(sys.argv) > 2 else 'both'
jobs = [('学生版', 'stu'), ('答案与解析版', 'ans')]
for tag, ab in jobs:
    if which not in ('both', ab):
        continue
    fs = glob.glob(os.path.join(BASE, '初赛模拟卷%s（非有机·%s·真题版式）' % (V, tag), '*.pdf'))
    if not fs:
        print('MISS', V, tag); continue
    d = fitz.open(fs[0]); n = 0
    for i, pg in enumerate(d):
        pg.get_pixmap(dpi=110).save(os.path.join(OUT, '%s_%s_p%02d.png' % (V, ab, i + 1))); n += 1
    print('%s %s: %d 页 → %s/%s_%s_p*.png' % (V, tag, n, OUT, V, ab)); d.close()
