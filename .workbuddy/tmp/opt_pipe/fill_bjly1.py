# -*- coding: utf-8 -*-
"""补录北京夏令营 无机巩固练习一 三张卡（第4/7/8题）的参考答案。
- 图型小问：直接抽答案 PDF 内嵌位图（过滤 logo/二维码）
- 文字/公式型小问：裁答案页区域为图（避免转录失真）
- 回填 `## 参考答案`，保留 FM 与 `## 知识点映射`
用法：python fill_bjly1.py [--apply]
"""
import os, re, sys, shutil

sys.stdout.reconfigure(encoding='utf-8')
try:
    import fitz
    try:
        fitz.TOOLS.mupdf_display_errors(False); fitz.TOOLS.mupdf_display_warnings(False)
    except Exception:
        pass
except Exception:
    fitz = None

ROOT = r'C:\Obsidion\妙妙屋'
os.chdir(ROOT)
PDF = '06-外部资料导入/OCR/01-题目/化学-夏令营-北京/北京夏令营-无机巩固练习一-答案1785409364.pdf'
IMG = '04-题库/2026机构初赛模拟题/北京夏令营/images'
DOC = fitz.open(PDF)
APPLY = '--apply' in sys.argv


def grab_image(page_idx, img_idx, dest):
    pg = DOC[page_idx]
    im = pg.get_images(full=True)[img_idx]
    base = DOC.extract_image(im[0])
    p = os.path.join(IMG, dest)
    open(p, 'wb').write(base['image'])
    return p, base['width'], base['height']


def grab_crop(page_idx, y0, y1, dest, dpi=200):
    pg = DOC[page_idx]
    r = pg.rect
    clip = fitz.Rect(r.x0, r.y0 + r.height * y0, r.x1, r.y0 + r.height * y1)
    pix = pg.get_pixmap(dpi=dpi, clip=clip)
    p = os.path.join(IMG, dest)
    pix.save(p)
    return p, pix.width, pix.height


def block(items):
    out = []
    for dest, kind, *args in items:
        if kind == 'img':
            p, w, h = grab_image(args[0], args[1], dest)
        else:
            p, w, h = grab_crop(args[0], args[1], args[2], dest)
        out.append('![](images/%s)  ' % dest)
        print('   %-34s %dx%d' % (dest, w, h))
    return '\n'.join(out)


def rewrite(card, ans_md):
    t = open(card, encoding='utf-8-sig').read().replace('\r\n', '\n')
    ia = t.find('## 参考答案')
    ik = t.find('## 知识点映射')
    assert ia > 0 and ik > ia, card
    new = t[:ia] + '## 参考答案\n\n' + ans_md + '\n\n' + t[ik:]
    if APPLY:
        open(card, 'w', encoding='utf-8', newline='\n').write(new)
    return new


B = '04-题库/2026机构初赛模拟题/北京夏令营/'

print('== 第4题 BJLY-01-04 ==')
f4 = block([
    ('bjly01_ans_q4_411.jpg', 'img', 3, 1),
    ('bjly01_ans_q4_412.jpg', 'img', 3, 2),
    ('bjly01_ans_q4_421a.jpg', 'img', 3, 3),
    ('bjly01_ans_q4_421b.jpg', 'img', 3, 4),
    ('bjly01_ans_q4_421ts.jpg', 'img', 4, 2),
    ('bjly01_ans_q4_422_1.jpg', 'img', 4, 3),
    ('bjly01_ans_q4_422_2.jpg', 'img', 4, 4),
    ('bjly01_ans_q4_422_3.jpg', 'img', 4, 5),
    ('bjly01_ans_q4_422_4.jpg', 'img', 4, 6),
    ('bjly01_ans_q4_431.jpg', 'img', 4, 7),
    ('bjly01_ans_q4_432.jpg', 'img', 4, 8),
])
a4 = """4-1-1（2 分）：

![](images/bjly01_ans_q4_411.jpg)

4-1-2（3 分；骨架 1 分，Ge₄ 簇构象未示出扣 1 分，未示出三角锥与平面三角形 VSEPR 模型扣 1 分）：

![](images/bjly01_ans_q4_412.jpg)

4-2-1（各 2 分，立体化学错误扣 1 分；过渡态 3 分，过渡态符号 1 分、表观电荷分布 1 分）C、D 及 B→C 过渡态：

![](images/bjly01_ans_q4_421a.jpg)
![](images/bjly01_ans_q4_421b.jpg)
![](images/bjly01_ans_q4_421ts.jpg)

4-2-2（8 分）C、D、E、F（图内标注沿用源答案册原文编号）：

![](images/bjly01_ans_q4_422_1.jpg)
![](images/bjly01_ans_q4_422_2.jpg)
![](images/bjly01_ans_q4_422_3.jpg)
![](images/bjly01_ans_q4_422_4.jpg)

4-3（8 分）P₁～P₄ 结构（图内标注沿用源答案册原文编号）：

![](images/bjly01_ans_q4_431.jpg)
![](images/bjly01_ans_q4_432.jpg)

> 📌 据源答案册（`北京夏令营-无机巩固练习一-答案`）逐图提取，图序与分问对应按原册排布；结构图保留了原册图内标注。

"""
rewrite(B + '题-BJLY-01-04-人们对低价Ge的研究从未停止.md', a4)

print('== 第7题 BJLY-01-07 ==')
f7 = block([
    ('bjly01_ans_q7_71.jpg', 'img', 6, 2),
    ('bjly01_ans_q7_72_1.jpg', 'img', 6, 3),
    ('bjly01_ans_q7_72_2.jpg', 'img', 6, 4),
    ('bjly01_ans_q7_72_3.jpg', 'img', 6, 5),
    ('bjly01_ans_q7_72_4.jpg', 'img', 6, 6),
    ('bjly01_ans_q7_73_1.jpg', 'img', 6, 7),
    ('bjly01_ans_q7_73_2.jpg', 'img', 6, 8),
    ('bjly01_ans_q7_73_3.jpg', 'img', 6, 9),
    ('bjly01_ans_q7_74_1.jpg', 'img', 6, 10),
    ('bjly01_ans_q7_74_2.jpg', 'img', 6, 11),
    ('bjly01_ans_q7_75_1.jpg', 'img', 7, 2),
    ('bjly01_ans_q7_75_2.jpg', 'img', 7, 3),
    ('bjly01_ans_q7_75_3.jpg', 'img', 7, 4),
])
a7 = """7-1（2 分）铝簇结构：

![](images/bjly01_ans_q7_71.jpg)

7-2（2 分＋2 分＋1 分＋1 分）L、A、B、X：

![](images/bjly01_ans_q7_72_1.jpg)
![](images/bjly01_ans_q7_72_2.jpg)
![](images/bjly01_ans_q7_72_3.jpg)
![](images/bjly01_ans_q7_72_4.jpg)

7-3（2 分＋2 分＋3 分）P、C、D：

![](images/bjly01_ans_q7_73_1.jpg)
![](images/bjly01_ans_q7_73_2.jpg)
![](images/bjly01_ans_q7_73_3.jpg)

7-4（2 分＋2 分）M、N：

![](images/bjly01_ans_q7_74_1.jpg)
![](images/bjly01_ans_q7_74_2.jpg)

7-5（2 分＋2 分＋3 分）O₁、O₂、O₃：

![](images/bjly01_ans_q7_75_1.jpg)
![](images/bjly01_ans_q7_75_2.jpg)
![](images/bjly01_ans_q7_75_3.jpg)

> 📌 据源答案册（`北京夏令营-无机巩固练习一-答案`）第 7 题逐图提取，图序按原册排布。

"""
rewrite(B + '题-BJLY-01-07-71一种三价铝物种与足量的钾.md', a7)

print('== 第8题 BJLY-01-08 ==')
f8 = block([
    ('bjly01_ans_q8_81.jpg', 'img', 7, 5),
    ('bjly01_ans_q8_82.jpg', 'img', 7, 6),
    ('bjly01_ans_q8_text.jpg', 'crop', 8, 0.05, 0.91),
])
a8 = """8-1（2 分）笼目（kagome）网：

![](images/bjly01_ans_q8_81.jpg)

8-2（3 分）Ca–O 层结构：

![](images/bjly01_ans_q8_82.jpg)

8-3、8-4 文字与计算解答（源答案册原文，含 8-3-1 Cu、8-3-2 Mg 12 配位／Cu 6 配位／截角四面体、8-3-3 最短距离计算、8-4 LaRu₃Si₂ 晶胞参数推导）：

![](images/bjly01_ans_q8_text.jpg)

> 📌 据源答案册（`北京夏令营-无机巩固练习一-答案`）逐图/逐区提取。8-3、8-4 含公式与数值，按原册裁图保留，未作转录以免失真。

"""
rewrite(B + '题-BJLY-01-08-81K结构可描述如下正六边形.md', a8)

print('\n%s' % ('[APPLY] 已写盘' if APPLY else '[DRY-RUN] 未写盘（加 --apply 生效）'))
