# -*- coding: utf-8 -*-
"""inst_census.py —— 按机构统计「可用池」，并单列 chemy 的来源批次构成（查真题是否混入）。"""
import os
import re
import sys
import glob
import collections

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import build_org as O          # noqa: E402
import build_multi as B        # noqa: E402
import mv_extract as X         # noqa: E402

BASE = O.BASE


def g(t, k):
    m = re.search(r'^' + k + r':\s*(.*)$', t, re.M)
    return m.group(1).strip() if m else ''


def run(all_years):
    per = collections.defaultdict(lambda: collections.Counter())
    details = []
    for rel in O.SRCS:
        for p in sorted(glob.glob(os.path.join(BASE, rel, '**', '题-*.md'), recursive=True)):
            t = open(p, encoding='utf-8-sig').read()
            mod, stage, diff = g(t, 'subject_module'), g(t, 'exam_stage'), int(g(t, 'difficulty') or 0)
            norm, sf = g(t, 'source_norm'), g(t, 'source_file')
            per[rel]['总卡'] += 1
            if not (all_years or O.in_2526(norm, sf)):
                continue
            if O.BATCH_BAD.search(norm):
                continue
            if mod not in ('元素与分析', '结构化学', '化学原理') or stage == '省预赛':
                continue
            if diff < 4 or [x for x in B.RISK if x in t]:
                continue
            if B.is_cn_prelim(re.sub(r'<!--.*?-->', '', t, flags=re.S)):
                continue
            if B.ORG_CHAP.search(g(t, 'source')) or B.ORG_CHAP.search(
                    (re.search(r'^#\s+(.+)$', t, re.M) or [None, ''])[1] if re.search(r'^#\s+(.+)$', t, re.M) else ''):
                continue
            try:
                c = X.extract(p)
            except Exception:
                continue
            rawq, rawa = c['question'], c['answer']
            if O.PLACEHOLDER.search(rawa) or O.PLACEHOLDER.search(rawq):
                continue
            if O.has_fake_struct(rawa) or O.has_fake_struct(rawq):
                continue
            if len(rawa) >= 400 and rawa.count('$') == 0 and rawq.count('$') >= 10:
                continue
            q0 = O.conv_imgs(O.clean_q(rawq)); a0 = O.clean_a(O.conv_imgs(rawa), q0)
            q, a = O.html_table_to_md(q0), O.html_table_to_md(a0)
            if O.LEAK.search(q):
                continue
            qn = re.sub(r'\s+', '', q); an = re.sub(r'\s+', '', a)
            if len(qn) < 60 or len(an) < 25:
                continue
            if len(B.ORGRE.findall(q + ' ' + a)) >= 3:
                continue
            if len(re.findall(r'^\*\*\s*\d{1,2}\s*[.．]\s*\*\*', q + '\n' + a, re.M)) >= 8:
                continue
            per[rel][mod] += 1
            if rel == 'chemy':
                details.append(norm)
    return per, details


print('=== 默认（年份硬闸）· 按机构可用数 ===')
per0, _ = run(False)
for inst in O.SRCS:
    c = per0[inst]
    n = c['元素与分析'] + c['结构化学'] + c['化学原理']
    print('  %-8s 总卡%5d  可用%4d（元素%d/结构%d/原理%d）' % (inst, c['总卡'], n, c['元素与分析'], c['结构化学'], c['化学原理']))

print('\n=== --all-years · 按机构可用数 ===')
per1, chemy_detail = run(True)
tot = collections.Counter()
for inst in O.SRCS:
    c = per1[inst]
    n = c['元素与分析'] + c['结构化学'] + c['化学原理']
    tot['元素与分析'] += c['元素与分析']; tot['结构化学'] += c['结构化学']; tot['化学原理'] += c['化学原理']
    print('  %-8s 总卡%5d  可用%4d（元素%d/结构%d/原理%d）' % (inst, c['总卡'], n, c['元素与分析'], c['结构化学'], c['化学原理']))
print('  ★ 合计 %d（元素%d/结构%d/原理%d）' % (sum(tot.values()), tot['元素与分析'], tot['结构化学'], tot['化学原理']))

print('\n=== chemy 可用卡的批名分布（--all-years）===')
for k, v in collections.Counter(chemy_detail).most_common(30):
    print('  %4d  %s' % (v, k))
