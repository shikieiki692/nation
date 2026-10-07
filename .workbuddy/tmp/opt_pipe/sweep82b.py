# -*- coding: utf-8 -*-
"""线1 v2：按 source_file 定位 `2026机构初赛模拟题/<机构>/` 下的**答案文件**。"""
import csv, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = r'C:\Obsidion\妙妙屋'
rows = [r for r in csv.DictReader(open(os.path.join(ROOT, '09-审计报告/2026-10-07-不可组卷题目清单.csv'), encoding='utf-8-sig'))
        if r['reason'] == '无答案/占位']


def field(t, k):
    m = re.search(r'^' + k + r':[ \t]*(.*)$', t, re.M)
    return (m.group(1).strip().strip('"') if m else '')


srcs = {}
for r in rows:
    p = os.path.join(ROOT, r['path'])
    t = open(p, encoding='utf-8-sig', errors='replace').read()
    srcs.setdefault(field(t, 'source_file'), []).append(os.path.basename(r['path'])[:40])

miss = 0
for sf, cards in sorted(srcs.items(), key=lambda x: -len(x[1])):
    d = os.path.join(ROOT, os.path.dirname(sf))
    stem = os.path.basename(sf)
    if stem.endswith('.md'):
        stem = stem[:-3]
    # 去尾部数字/版本
    key = re.sub(r'\d{6,}$', '', stem)
    ans = []
    if os.path.isdir(d):
        for f in os.listdir(d):
            if not f.endswith('.md'):
                continue
            if key[:12] in f and ('答案' in f or '解析' in f):
                ans.append(f)
    ok = '✅' if ans else '❌'
    if not ans:
        miss += 1
    print('%s %-58s (%2d张) dir=%s' % (ok, stem[:58], len(cards), os.path.dirname(sf)))
    print('     答案文件: %s' % (ans[:4] if ans else '（无同名答案）'))
print()
print('无答案文件的源：%d / %d' % (miss, len(srcs)))
