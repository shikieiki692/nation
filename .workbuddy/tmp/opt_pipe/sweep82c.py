# -*- coding: utf-8 -*-
"""线1 v3：**精确**匹配答案文件（去掉尾部数字后，答案文件须含完全相同的题目标识）。"""
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

print('%-60s %s' % ('源（去尾数字）', '同级目录里含「答案/解析」的文件'))
print('-' * 130)
n_ans = 0
for sf, cards in sorted(srcs.items(), key=lambda x: -len(x[1])):
    d = os.path.join(ROOT, os.path.dirname(sf))
    stem = os.path.basename(sf)
    stem = stem[:-3] if stem.endswith('.md') else stem
    key = re.sub(r'\d{6,}$', '', stem)          # 去尾部 6+ 位数字ID
    cands = []
    if os.path.isdir(d):
        for f in sorted(os.listdir(d)):
            if not f.endswith('.md'):
                continue
            if '答案' not in f and '解析' not in f:
                continue
            cands.append(f)
    # 精确命中：candidate 去尾数字后 == key，或 key 是 cand 的前缀（去「-答案」）
    exact = [c for c in cands if re.sub(r'\d{6,}$', '', c[:-3]).replace('-答案', '').replace('答案', '') == key
             or re.sub(r'\d{6,}$', '', c[:-3]) in (key, key + '-答案', key + '答案')]
    if exact:
        n_ans += len(cards)
    print('%-58s | %s' % (key[:58], ('✅ ' + str(exact[:3])) if exact else ('❌（同目录 %d 个答案文件，无本卷）' % len(cands))))
print()
print('可配对答案文件的卡：%d / %d' % (n_ans, len(rows)))
