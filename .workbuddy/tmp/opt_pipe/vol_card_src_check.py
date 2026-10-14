# -*- coding: utf-8 -*-
"""逐卷逐题：卷内「> 来源」行 ↔ 题卡 FM 的 source 字段 对账。
卷末选题清单提供 「题号 → 题卡 wikilink」，据此把题下的来源行与卡片 FM 对齐。"""
import io, os, re, glob

os.chdir(r'C:\Obsidion\妙妙屋')
CARD_DIRS = ['04-题库/2026机构初赛模拟题']


def find_card(name):
    """按 wikilink 目标名（不含 .md）找卡文件。"""
    for base in CARD_DIRS:
        for dp, dn, fn in os.walk(base):
            for f in fn:
                if f.endswith('.md') and f[:-3] == name:
                    return os.path.join(dp, f)
    return None


def card_source(path):
    t = io.open(path, encoding='utf-8-sig', errors='replace').read()
    m = re.search(r'^source:\s*(.+)$', t, re.M)
    m2 = re.search(r'^source_norm:\s*(.+)$', t, re.M)
    return (m.group(1).strip() if m else '?'), (m2.group(1).strip() if m2 else '?')


def norm(s):
    s = re.sub(r'｜.*$', '', s)          # 去 ｜难度…
    s = re.sub(r'\|.*$', '', s)
    s = re.sub(r'\s+', '', s)
    return s.strip()


VOLS = sorted(glob.glob('04-题库/初赛模拟卷*（非有机·答案版）.md'))
tot = mism = 0
report = []
for p in VOLS:
    vol = os.path.basename(p).replace('初赛模拟卷', '').replace('（非有机·答案版）.md', '')
    t = io.open(p, encoding='utf-8-sig').read()
    L = t.split('\n')
    # 1) 卷末清单：| 题号 | 题名 | [[卡]] | ...
    tbl = {}
    for l in L:
        m = re.match(r'\|\s*(\d+)\s*\|.*?\[\[([^\]|]+)', l)
        if m:
            tbl[m.group(1)] = m.group(2).strip()
    # 2) 正文：### 第 N 题 → 紧随的 > 来源
    body = {}
    cur = None
    for l in L:
        m = re.match(r'^###\s*第\s*(\d+)\s*题', l)
        if m:
            cur = m.group(1)
            continue
        ms = re.match(r'^>\s*来源[:：]\s*(.+)$', l)
        if ms and cur:
            body[cur] = ms.group(1).strip()
            cur = None
    # 3) 对账
    for k in sorted(set(tbl) | set(body), key=lambda x: int(x)):
        tot += 1
        card = find_card(tbl.get(k, ''))
        if not card:
            report.append((vol, k, 'NO-CARD:' + tbl.get(k, '?'), body.get(k, '-'), '-'))
            mism += 1
            continue
        cs, cn = card_source(card)
        if norm(body.get(k, '')) != norm(cs):
            report.append((vol, k, tbl[k], body.get(k, '-'), cs))
            mism += 1

print('检查 %d 题；不一致 %d 处' % (tot, mism))
for r in report:
    print('  ⚠️ 卷%s 第%s题 [%s]\n      卷= %s\n      卡= %s' % (r[0], r[1], r[2], r[3], r[4]))
