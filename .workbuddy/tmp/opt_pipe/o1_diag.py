# -*- coding: utf-8 -*-
"""O1 干跑诊断：导出 pick 清单（路径/机构/主题分/题名前 40 字），只读不落盘。"""
import os, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.argv = [sys.argv[0], '--vol', 'O1', '--all-years', '--organic',
            '--exclude', os.path.join(HERE, 'o1_exclude.txt'),
            '--topic-map', os.path.join(HERE, 'o1_topic_map.json')]
import build_org as BO

pool = BO.build_pool()
used = set()
fps0 = []
picks = BO.pick_vol(pool, used, max_per_src=4, fps0=fps0)
for k, (mod, lbl, need) in enumerate(BO.QUOTA):
    print("== %s（need=%d，实得 %d）" % (lbl, need, len(picks[k][1])))
    for c in picks[k][1]:
        print("   %-14s 有机%d 主题分%s | %s" % (
            c['src_dir'], c.get('otopic', -1), c.get('otopic_sc'),
            (c.get('title') or '')[:36]))
        print("        %s" % c['path'].replace('\\', '/'))
with open(os.path.join(HERE, 'o1_cards.txt'), 'w', encoding='utf-8') as f:
    for _, ps in picks:
        for c in ps:
            f.write(c['path'].replace('\\', '/') + '\n')
print("\n卡清单已写 o1_cards.txt（%d 行）" % sum(len(ps) for _, ps in picks))
print()
tc = collections.Counter(c.get('otopic') for _, ps in picks for c in ps)
print("主题分布:", dict(tc))
allc = pool['有机化学']
print("全有机池主题分布:", dict(collections.Counter(c.get('otopic') for c in allc)))
