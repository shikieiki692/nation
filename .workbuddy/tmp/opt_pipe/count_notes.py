# -*- coding: utf-8 -*-
"""量化：题面/答案区含「内部注记行」（行首 📎/⛔/📄 或含 答案出处：）的卡。"""
import os, re, sys, glob
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.workbuddy/tmp/opt_pipe')
sys.argv = ['x', '--vol', 'NOTE', '--all-years']
import build_org as BO

NOTE = re.compile(r'^(?:[>]+[ \t]*)*(?:📎|⛔|📄)|答案出处[：:]')
nq = na = nb = 0
sample = []
for p in glob.glob('04-题库/2026机构初赛模拟题/**/题-*.md', recursive=True):
    t = open(p, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n')
    i = t.find('## 题目'); j = t.find('## 参考答案'); k = t.find('## 知识点映射')
    if i < 0 or j < 0 or k < 0:
        continue
    qz, az = t[i:j], t[j:k]
    hq = any(NOTE.search(l.strip()) for l in qz.split('\n') if l.strip())
    ha = any(NOTE.search(l.strip()) for l in az.split('\n') if l.strip())
    if hq:
        nq += 1
        if len(sample) < 10:
            ln = next(l for l in qz.split('\n') if l.strip() and NOTE.search(l.strip()))
            sample.append(('题面', p, ln.strip()[:80]))
    if ha:
        na += 1
    if hq or ha:
        nb += 1
print('题面含注记 %d 张 / 答案含注记 %d 张 / 任一 %d 张' % (nq, na, nb))
for tag, p, ln in sample:
    print('  [%s] %-44s | %s' % (tag, os.path.basename(p)[:42], ln))
