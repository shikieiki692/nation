# -*- coding: utf-8 -*-
"""扫描：源卡 H1 标题行（### 第 N 题…）过长 ⇒ 题干被塞进标题行，strip 会误删。

对每张卡：取 ## 题目 区首行匹配 `^#{2,4}\s*第\s*[0-9一二三四五六七八九十]+\s*题` 的行，
测其「去掉题号头部后」的非空白长度；> 45 判为疑似「题干在标题里」。
"""
import os, re, sys, glob
sys.stdout.reconfigure(encoding='utf-8')

cards = glob.glob('04-题库/2026机构初赛模拟题/**/题-*.md', recursive=True)
sus = []
for p in cards:
    t = open(p, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n')
    i = t.find('## 题目'); j = t.find('## 参考答案')
    if i < 0 or j < 0:
        continue
    qz = t[i:j]
    m = re.search(r'(?m)^#{2,4}\s*第\s*[0-9一二三四五六七八九十]+\s*题[^\n]*$', qz)
    if not m:
        continue
    line = m.group(0)
    # 去掉 「### 第 N 题」(含中英文) 头部
    tail = re.sub(r'^#{2,4}\s*第\s*[0-9一二三四五六七八九十]+\s*题\s*', '', line)
    nws = len(re.sub(r'\s+', '', tail))
    if nws > 45:
        sus.append((nws, p, line))

print('H1 标题行携带 > 45 字 的卡：%d 张' % len(sus))
for n, p, line in sorted(sus, reverse=True):
    print('  %3d 字 | %s' % (n, os.path.basename(p)[:52]))
    print('         %r' % line[:110])
