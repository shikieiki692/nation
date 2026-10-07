# -*- coding: utf-8 -*-
"""救回 题-GChO-63-07：把裁图放进**正确**目录（质心GChO），写题面，清理误建目录。"""
import os, re, sys, shutil
sys.stdout.reconfigure(encoding='utf-8')

ROOT = r'C:\Obsidion\妙妙屋'
BASE = os.path.join(ROOT, r'04-题库\2026机构初赛模拟题')
H = '5d4d4010f41da5ef340eef815e918d524c2e306c9ee0d1b5a693248f9e98ed63'
SRC = os.path.join(BASE, '01-质心GChO', 'images', H + '.jpg')
DSTDIR = os.path.join(BASE, '质心GChO', 'images')
CARD = os.path.join(BASE, '质心GChO', '题-GChO-63-07-如下的转化在Lewis酸的催.md')

# 1) 归位图片
os.makedirs(DSTDIR, exist_ok=True)
shutil.move(SRC, os.path.join(DSTDIR, H + '.jpg'))
print('图归位:', os.path.exists(os.path.join(DSTDIR, H + '.jpg')))

# 2) 清理误建目录
bog = os.path.join(BASE, '01-质心GChO')
try:
    os.rmdir(os.path.join(bog, 'images'))
    os.rmdir(bog)
    print('误建目录已删:', not os.path.exists(bog))
except OSError as e:
    print('误建目录清理失败:', e)

# 3) 写题面
t = open(CARD, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n')
i = t.find('## 题目'); j = t.find('## 参考答案')
qz = t[i:j]
anchor = '如下的转化在 Lewis 酸的催化下可以非常快的进行。写出至少三个关键的中间体，不要求立体化学。'
if '![[' in qz:
    print('题面已有图，跳过'); sys.exit(0)
k = qz.find(anchor)
assert k > 0, '未找到锚点'
ins = k + len(anchor)
new_t = t[:i] + qz[:ins] + '\n\n![[' + H + '.jpg]]' + qz[ins:] + t[j:]
open(CARD, 'w', encoding='utf-8', newline='\n').write(new_t)

t2 = open(CARD, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n')
i2 = t2.find('## 题目'); j2 = t2.find('## 参考答案')
print('题面区 %d 字；含图 %s' % (len(t2[i2:j2]), '![[' in t2[i2:j2]))
print(re.sub(r'\n{2,}', '\n', t2[i2:j2]))
print('结构:', {h: t2.count(h) for h in ['## 题目', '## 参考答案', '## 知识点映射']})
