# -*- coding: utf-8 -*-
"""卷族两项检查：
① 卷内来源行首词（机构） vs 卡片所在目录（机构）—— 查张冠李戴
② 跨卷用卡重复 —— 各卷口径行承诺「与前 N 卷用题零重复」
"""
import io, os, re, glob, collections

os.chdir(r'C:\Obsidion\妙妙屋')
CARD = {}
for p in glob.glob('04-题库/**/*.md', recursive=True):
    CARD[os.path.basename(p)[:-3]] = p

VOLS = sorted(glob.glob('04-题库/初赛模拟卷*（非有机·答案版）.md'))
use = collections.defaultdict(list)     # 卡片 basename -> [卷]
mismatch = []
for v in VOLS:
    vol = os.path.basename(v).replace('初赛模拟卷', '').replace('（非有机·答案版）.md', '')
    L = io.open(v, encoding='utf-8-sig').read().split('\n')
    tbl = {}
    for l in L:
        m = re.match(r'\|\s*(\d+)\s*\|.*?\[\[([^\]|]+)', l)
        if m:
            tbl[m.group(1)] = m.group(2).strip()
    body, cur = {}, None
    for l in L:
        m = re.match(r'^###\s*第\s*(\d+)\s*题', l)
        if m:
            cur = m.group(1); continue
        ms = re.match(r'^>\s*来源[:：]\s*(.+)$', l)
        if ms and cur:
            body[cur] = ms.group(1).strip(); cur = None
    for k in sorted(set(tbl) & set(body), key=int):
        name = tbl[k]
        use[name].append(vol)
        cp = CARD.get(name)
        src_head = body[k].split()[0] if body[k].split() else ''
        if not cp:
            continue
        # 卡片所在目录（末两级）
        d = '/'.join(cp.split(os.sep)[-2:])
        # 来源首词是已知机构名时，应与目录相符
        known = ['chemy', 'XeChem', '2ChO', '伽马', '化英社', '汇智', '一式', '方圆',
                 '清北营', '壹尖培优', '质心GChO', '质心UChO', '北京夏令营', '北斗学友']
        for kk in known:
            if src_head.startswith(kk):
                if kk.lower() not in d.lower():
                    mismatch.append((vol, k, name, src_head, d))
                break

print('===== ① 来源首词(机构) vs 卡片目录 =====')
print('   不一致 %d 处' % len(mismatch))
for r in mismatch[:15]:
    print('   卷%-5s 第%-2s题 %-42s' % (r[0], r[1], r[2][:42]))
    print('        来源=%-14s 目录=%s' % (r[3], r[4]))
print()
print('===== ② 跨卷用卡重复 =====')
dup = {k: v for k, v in use.items() if len(v) > 1}
print('   重复用卡 %d 张 / 共 %d 张' % (len(dup), len(use)))
for k, v in list(dup.items())[:20]:
    print('   %-48s → %s' % (k[:48], ','.join(v)))
