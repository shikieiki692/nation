# -*- coding: utf-8 -*-
"""测：12 张题面泄露卡的 答案区 是否已含解答（若已含 ⇒ 题面内的重复解答可安全剥离）。"""
import csv, os, re, sys, difflib
sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'C:\Obsidion\妙妙屋'
rows = [r for r in csv.DictReader(open(os.path.join(ROOT, '09-审计报告/2026-10-07-不可组卷题目清单.csv'), encoding='utf-8-sig'))
        if r['reason'] == '题面泄露']


def nz(s):
    return re.sub(r'\s+', '', s)


for r in rows:
    p = os.path.join(ROOT, r['path'])
    t = open(p, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n')
    i = t.find('## 题目'); j = t.find('## 参考答案'); k = t.find('## 知识点映射')
    qz, az = t[i:j], t[j:k]
    print('=' * 104)
    print('%-44s | 题面 %d / 答案 %d 字' % (os.path.basename(p)[:42], nz(qz).__len__(), nz(az).__len__()))
    print('  答案区前 260: %r' % re.sub(r'\n{2,}', ' / ', az)[:260])
