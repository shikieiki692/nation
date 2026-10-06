# -*- coding: utf-8 -*-
"""补录北京夏令营 无机巩固练习二 两张卡（第8/9题）参考答案——按答案页区域裁图回填。"""
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
try:
    import fitz
    try:
        fitz.TOOLS.mupdf_display_errors(False); fitz.TOOLS.mupdf_display_warnings(False)
    except Exception:
        pass
except Exception:
    fitz = None
os.chdir(r'C:\Obsidion\妙妙屋')
PDF = '06-外部资料导入/OCR/01-题目/化学-夏令营-北京/北京夏令营-无机巩固练习二-答案1785491473.pdf'
IMG = '04-题库/2026机构初赛模拟题/北京夏令营/images'
DOC = fitz.open(PDF)
APPLY = '--apply' in sys.argv


def crop(page_idx, y0, y1, dest, dpi=200):
    pg = DOC[page_idx]; r = pg.rect
    pix = pg.get_pixmap(dpi=dpi, clip=fitz.Rect(r.x0, r.y0 + r.height * y0, r.x1, r.y0 + r.height * y1))
    p = os.path.join(IMG, dest); pix.save(p)
    print('   %-32s %dx%d' % (dest, pix.width, pix.height))


def rewrite(card, ans):
    t = open(card, encoding='utf-8-sig').read().replace('\r\n', '\n')
    ia = t.find('## 参考答案'); ik = t.find('## 知识点映射')
    assert ia > 0 and ik > ia, card
    new = t[:ia] + '## 参考答案\n\n' + ans + '\n\n' + t[ik:]
    if APPLY:
        open(card, 'w', encoding='utf-8', newline='\n').write(new)


crop(6, 0.05, 0.605, 'bjly02_ans_q8.jpg')
crop(6, 0.605, 0.875, 'bjly02_ans_q9.jpg')

B = '04-题库/2026机构初赛模拟题/北京夏令营/'
rewrite(B + '题-BJLY-02-08-称取与32的乙醇溶液混合然后.md',
        '第 8 题（11 分）解答（源答案册原文：Cr 配合物化学式 [Cr(ten)(bipy)₂]Cl₃·H₂O 推导、'
        '6 个几何异构体、d³sp³ 杂化能级分裂等）：\n\n'
        '![](images/bjly02_ans_q8.jpg)\n\n'
        '> 📌 据源答案册（`北京夏令营-无机巩固练习二-答案`）第 8 题区域裁图，含图与公式，未作转录以免失真。\n')

rewrite(B + '题-BJLY-02-09-某过渡金属X的单质A在生活中.md',
        '第 9 题（9 分）解答（源答案册原文：A–K 推断表 Fe/FeSO₄/(NH₄)₂Fe(SO₄)₂·6H₂O/…/'
        'Na₂[Fe(CO)₄]，及 3 个反应方程式）：\n\n'
        '![](images/bjly02_ans_q9.jpg)\n\n'
        '> 📌 据源答案册（`北京夏令营-无机巩固练习二-答案`）第 9 题区域裁图，含表格与方程式，未作转录以免失真。\n')

print('\n%s' % ('[APPLY] 已写盘' if APPLY else '[DRY-RUN]'))
