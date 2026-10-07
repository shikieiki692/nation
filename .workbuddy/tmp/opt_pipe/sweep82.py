# -*- coding: utf-8 -*-
"""线1：对 82 张「无答案」的 24 个源，系统扫查「同目录/同名的答案文件」与 PDF 树。"""
import csv, os, re, sys, collections, glob
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
    sf = field(t, 'source_file')
    srcs.setdefault(sf, []).append(os.path.basename(r['path'])[:44])

print('源文件 %d 个' % len(srcs))
for sf, cards in sorted(srcs.items(), key=lambda x: -len(x[1])):
    print('=' * 100)
    print('%-64s (%d 张)' % (sf[:64], len(cards)))
    # 1) 在 04-题库 下找同名源
    base = os.path.basename(sf)
    stem = base[:-3] if base.endswith('.md') else base
    found = []
    for pat in ('**/%s.md' % stem, '**/%s*.md' % stem[:18], '**/*%s*' % stem[:14]):
        g = glob.glob('04-题库/2026机构初赛模拟题/**/' + pat.split('/')[-1], recursive=True)
        g = [x for x in g if '题-' not in os.path.basename(x)]
        if g:
            found = sorted(set(g))[:6]
            break
    # 2) 同目录找「答案」文件
    ans = []
    for g in glob.glob('04-题库/2026机构初赛模拟题/**/*.md', recursive=True):
        bn = os.path.basename(g)
        if '题-' in bn:
            continue
        if stem[:10] and stem[:10] in bn and ('答案' in bn or '解析' in bn):
            ans.append(g)
    print('   源候选: %s' % (found if found else '（未在 04-题库 下找到）'))
    print('   同源答案文件: %s' % (sorted(set(ans))[:5] if ans else '（无）'))
