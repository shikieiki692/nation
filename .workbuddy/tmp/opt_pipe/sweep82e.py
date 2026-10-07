# -*- coding: utf-8 -*-
"""线1 v5（决定性）：对 82 张卡，在**同机构目录**的所有「答案/解析」md 里做**内容级**查找。

判据：卡题面的**特征串**（首个小问的首句，去空白取 24 字）是否出现在某答案文件里；
      命中 ⇒ 该答案文件可能含本题（可补）；全不命中 ⇒ 确缺。
"""
import csv, os, re, sys, glob, collections
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.workbuddy/tmp/opt_pipe')
sys.argv = ['x', '--vol', 'S82', '--all-years']
import build_org as BO

ROOT = r'C:\Obsidion\妙妙屋'
BASE = os.path.join(ROOT, '2026机构初赛模拟题')

rows = [r for r in csv.DictReader(open(os.path.join(ROOT, '09-审计报告/2026-10-07-不可组卷题目清单.csv'), encoding='utf-8-sig'))
        if r['reason'] == '无答案/占位']


def norm(s):
    return re.sub(r'\s+', '', s)


# 建答案文件索引（按机构目录）
ans_idx = {}
for inst_dir in sorted(os.listdir(BASE)):
    d = os.path.join(BASE, inst_dir)
    if not os.path.isdir(d):
        continue
    fs = [f for f in os.listdir(d) if f.endswith('.md') and re.search(r'答案|解析', f)]
    idx = []
    for f in fs:
        try:
            txt = norm(open(os.path.join(d, f), encoding='utf-8-sig', errors='replace').read())
        except Exception:
            continue
        idx.append((f, txt))
    ans_idx[inst_dir] = idx
    print('[%s] 答案文件 %d 个' % (inst_dir, len(idx)), flush=True)

hit, miss = [], []
for r in rows:
    p = os.path.join(ROOT, r['path'])
    c = BO.X.extract(p)
    q = norm(BO.html_table_to_md(BO.conv_imgs(BO.clean_q(c['question']))))
    frag = q[:24]
    # 该卡所属机构目录
    inst_dir = [x for x in ans_idx if x.split('-', 1)[-1] == r['inst'] or x == r['inst']]
    cands = []
    for k, idx in ans_idx.items():
        if r['inst'] in k or k.split('-', 1)[-1] in r['inst']:
            cands += idx
    found = [f for f, txt in cands if frag and frag in txt]
    if found:
        hit.append((os.path.basename(p), frag, found[:3]))
    else:
        miss.append(os.path.basename(p))

print()
print('=== 内容命中（可能可补）：%d 张 ===' % len(hit))
for bn, fr, fs in hit:
    print('  %-46s | frag=%r | in %s' % (bn[:44], fr[:20], fs))
print('=== 全不命中（确缺）：%d 张 ===' % len(miss))
