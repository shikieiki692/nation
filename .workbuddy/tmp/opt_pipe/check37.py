# -*- coding: utf-8 -*-
"""核 37 张同签名卡：在池状态 + 题面尾部内容。"""
import os, re, sys, glob, csv
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.workbuddy/tmp/opt_pipe')
sys.argv = ['x', '--vol', 'S37', '--all-years']
import build_org as BO

ROOT = r'C:\Obsidion\妙妙屋'
verd = {}
for r in csv.DictReader(open(os.path.join(ROOT, '09-审计报告/2026-10-07-不可组卷题目清单.csv'), encoding='utf-8-sig')):
    verd[os.path.basename(r['path'])] = (r['verdict'], r['reason'])

ANS_HEAD = re.compile(r'(?m)^#{1,4}[ \t]*([^\n]{0,60}?答案[^\n]{0,30})$')
cards = glob.glob('04-题库/2026机构初赛模拟题/**/题-*.md', recursive=True)
for p in cards:
    t = open(p, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n')
    i = t.find('## 题目'); j = t.find('## 参考答案'); k = t.find('## 知识点映射')
    if i < 0 or j < 0 or k < 0:
        continue
    qz = t[i:j]
    titles = [m.group(1).strip() for m in ANS_HEAD.finditer(qz)
              if m.group(1).strip() not in ('参考答案', '答案')]
    if not titles:
        continue
    bn = os.path.basename(p)
    v, rsn = verd.get(bn, ('?', '?'))
    print('%-46s | %-6s %-10s | 题面含: %s' % (bn[:44], v, rsn or '-', titles[0][:26]))
    # 该标题在题面中的位置（相对尾部）
    off = qz.find(titles[0])
    print('      题面 %d 字，该标题@%d（后随 %d 字）' % (len(qz), off, len(qz) - off))
