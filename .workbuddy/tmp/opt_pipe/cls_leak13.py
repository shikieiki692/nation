# -*- coding: utf-8 -*-
"""把 13 张「题面泄露」分类：尾部串入（可截断） vs 真交错（不可手术）。

判据：
  - 找题面清洗后文本里第一个「外来标记」：`## 第M题`(M≠own) / `M-x`(M≠own) / `## …答案`
  - 若无外来标记 ⇒ 真交错（题面内嵌解答，无清晰切点）
  - 若命中且其**之前**的文本 ≥ 200 字且含本卡号小问 ⇒ 尾部串入，可截断
"""
import os, re, sys, csv, glob
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.workbuddy/tmp/opt_pipe')
sys.argv = ['x', '--vol', 'CLS', '--all-years']
import build_org as BO

ROOT = r'C:\Obsidion\妙妙屋'
rows = [r for r in csv.DictReader(open(os.path.join(ROOT, '09-审计报告/2026-10-07-不可组卷题目清单.csv'), encoding='utf-8-sig'))
        if r['reason'] == '题面泄露']
for r in rows:
    p = os.path.join(ROOT, r['path'])
    t = open(p, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n')
    own = BO.own_qno(t, p)
    c = BO.X.extract(p)
    q = BO.html_table_to_md(BO.conv_imgs(BO.clean_q(c['question'])))
    # 找外来标记
    hits = []
    for m in re.finditer(r'(?m)^[ \t]*(?:#{1,4}[ \t]*)?\*{0,2}[ \t]*(\d{1,2})\s*[-－]\s*\d{1,2}', q):
        n = int(m.group(1))
        if own and n != own and n <= 30:
            hits.append((m.start(), 'subq %d-x' % n))
            break
    for m in re.finditer(r'(?m)^#{1,4}[ \t]*第\s*([0-9一二三四五六七八九十]+)\s*题', q):
        n = BO._cn2int(m.group(1))
        if n and own and n != own:
            hits.append((m.start(), 'heading 第%s题' % m.group(1)))
            break
    for m in re.finditer(r'(?m)^#{1,4}[^\n]*答案[^\n]*$', q):
        hits.append((m.start(), '答案标题'))
        break
    hits.sort()
    if hits:
        off, tag = hits[0]
        before = re.sub(r'\s+', '', q[:off])
        ownk = len(re.findall(r'(?m)^\s*(?:#+\s*)?\*{0,2}\s*%d\s*[-－]' % (own or -1), q[:off]))
        print('%-46s own=%-3s | 切点@%d(%s) 前文%d字 本卡小问%d处' % (
            os.path.basename(p)[:46], own, off, tag, len(before), ownk))
    else:
        print('%-46s own=%-3s | ⛔ 无外来标记 ⇒ 真交错（不可手术）' % (os.path.basename(p)[:46], own))
