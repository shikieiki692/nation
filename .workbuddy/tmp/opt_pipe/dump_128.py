# -*- coding: utf-8 -*-
r"""Dump 全部 29 处 `\\mathrm` 的上下文 + 判是否在 array 内（只读）。"""
import io, re
p = '04-题库/教材习题/ABOC/题-128-ABOC-Ch4-4.13.1-Cannizzaro 康尼查罗 反应是醛在强碱浓溶液中发生的.md'
t = io.open(p, encoding='utf-8-sig').read()
RUN = re.compile(r'(\\+)mathrm')
# 记录 array 区间
arrays = [(m.start(), m.end()) for m in re.finditer(r'\\begin\{array\}.*?\\end\{array\}', t, re.S)]
def in_array(i):
    return any(a <= i < b for a, b in arrays)
n = 0
for m in RUN.finditer(t):
    if len(m.group(1)) != 2:
        continue
    n += 1
    s = max(0, m.start() - 55)
    seg = t[s:m.end() + 30].replace('\n', '⏎')
    print('[%2d]%s %s' % (n, 'A' if in_array(m.start()) else ' ', seg))
print()
print('共 %d 处；其中在 array 内 %d 处' %
      (n, sum(1 for m in RUN.finditer(t) if len(m.group(1)) == 2 and in_array(m.start()))))
print('\\begin{array} 数:', len(arrays))
