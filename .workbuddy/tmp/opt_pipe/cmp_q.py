# -*- coding: utf-8 -*-
"""比对 extract.question 与文件 ## 题目 区，找差异。"""
import os, re, sys, glob
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.workbuddy/tmp/opt_pipe')
sys.argv = ['x', '--vol', 'CMP', '--all-years']
import build_org as BO

p = glob.glob('04-题库/2026机构初赛模拟题/**/题-HYS-02-06-表面张力*.md', recursive=True)[0]
t = open(p, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n')
i = t.find('## 题目'); j = t.find('## 参考答案')
rawq = t[i + len('## 题目'):j]
c = BO.X.extract(p)
cq = c['question']
print('len(rawq)=%d len(extract.q)=%d' % (len(rawq), len(cq)))
print('rawq[:150]=%r' % rawq[:150])
print('extract.q[:150]=%r' % cq[:150])
print()
print('rawq[-200:]=%r' % rawq[-200:])
print('extract.q[-200:]=%r' % cq[-200:])
print()
print('rawq 里出现 "## " 的行:')
for l in rawq.split('\n'):
    if l.startswith('#'):
        print('   %r' % l[:80])
print()
print('rawq 里 <table> 数 =', rawq.count('<table>'), ' extract.q 里 =', cq.count('<table>'))
print('rawq 里 图数 =', len(re.findall(r'!\[', rawq)), ' extract.q 里 =', len(re.findall(r'!\[', cq)))
