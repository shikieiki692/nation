# -*- coding: utf-8 -*-
"""救回 题-GChO-63-07：回源裁「如下的转化」反应式图 → 存入卡图目录 → 写入题面。"""
import os, re, sys, hashlib
sys.stdout.reconfigure(encoding='utf-8')
import fitz

ROOT = r'C:\Obsidion\妙妙屋'
PDF = os.path.join(ROOT, r'06-外部资料导入\OCR\01-题目\质心合集新\GChO模拟试题合集\ZCHEM-GChO63试题.pdf')
CARD = os.path.join(ROOT, r'04-题库\2026机构初赛模拟题\01-质心GChO\题-GChO-63-07-如下的转化在Lewis酸的催.md')
IMGDIR = os.path.join(ROOT, r'04-题库\2026机构初赛模拟题\01-质心GChO\images')

# 1) 裁图 → JPEG 字节
doc = fitz.open(PDF)
pg = doc[7]
pix = pg.get_pixmap(dpi=320, clip=fitz.Rect(150, 597, 522, 645))
jpg = pix.tobytes('jpeg', jpg_quality=92)
h = hashlib.sha256(jpg).hexdigest()
os.makedirs(IMGDIR, exist_ok=True)
fp = os.path.join(IMGDIR, h + '.jpg')
open(fp, 'wb').write(jpg)
print('图已存: %s.jpg  %d 字节  (%dx%d)' % (h[:12], len(jpg), pix.width, pix.height))

# 2) 写入题面
t = open(CARD, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n')
i = t.find('## 题目'); j = t.find('## 参考答案')
qz = t[i:j]
anchor = '如下的转化在 Lewis 酸的催化下可以非常快的进行。写出至少三个关键的中间体，不要求立体化学。'
if '![[' in qz:
    print('题面已有图，跳过插图'); sys.exit(0)
k = qz.find(anchor)
assert k > 0, '未找到锚点'
ins = k + len(anchor)
newq = qz[:ins] + '\n\n![[' + h + '.jpg]]' + qz[ins:]
new_t = t[:i] + newq + t[j:]
open(CARD, 'w', encoding='utf-8', newline='\n').write(new_t)

t2 = open(CARD, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n')
i2 = t2.find('## 题目'); j2 = t2.find('## 参考答案')
print('题面区 %d 字；含图 %s' % (len(t2[i2:j2]), '![[' in t2[i2:j2]))
print(re.sub(r'\n{2,}', '\n', t2[i2:j2]))
