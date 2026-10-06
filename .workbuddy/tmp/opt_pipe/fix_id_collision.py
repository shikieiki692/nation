# -*- coding: utf-8 -*-
"""卡 ID 撞车治理：把**重复的 aliases** 加「系列判别后缀」使其唯一。
- 不改文件名（16,118 条 wikilink 指向文件名，改名必断链）
- 每个撞车组保留 1 张原始短 ID（按路径排序首个），其余加 `·<系列名>`
用法：python fix_id_collision.py [--apply]
"""
import os, re, sys, glob, collections

sys.stdout.reconfigure(encoding='utf-8')
os.chdir(r'C:\Obsidion\妙妙屋')
APPLY = '--apply' in sys.argv
BASE = '04-题库/2026机构初赛模拟题'
SRCS = os.listdir(BASE)


def series_of(norm, inst):
    s = norm
    s = re.sub(r'^' + re.escape(inst) + r'[-—]', '', s)
    s = re.sub(r'第\s*\d+\s*届', '', s)
    for w in ['中国化学奥林匹克', '化学奥林匹克', '奥林匹克', 'Chemy', 'chemy',
              '（初赛）', '(初赛)', '（决赛）', '(决赛)', '化学', inst]:
        s = s.replace(w, '')
    s = re.sub(r'[-—·\s]+', '', s)
    return s.strip() or 'x'


cards = []
for r in SRCS:
    d = os.path.join(BASE, r)
    if not os.path.isdir(d):
        continue
    for p in sorted(glob.glob(os.path.join(d, '**', '题-*.md'), recursive=True)):
        t = open(p, encoding='utf-8-sig').read().replace('\r\n', '\n')
        m = re.search(r'^aliases:[ \t]*\[(.*?)\]', t, re.M)
        n = re.search(r'^source_norm:[ \t]*(.*?)[ \t]*$', t, re.M)
        if not m:
            continue
        al = re.findall(r'"([^"]+)"', m.group(1))
        norm = (n.group(1).strip().strip('"') if n else '')
        cards.append(dict(path=p.replace(os.sep, '/'), inst=r, aliases=al, norm=norm))

byid = collections.defaultdict(list)
for c in cards:
    for a in c['aliases']:
        byid[a].append(c)
dup = {k: v for k, v in byid.items() if len(v) > 1}
print('重复 ID %d ；涉及卡 %d' % (len(dup), sum(len(v) for v in dup.values())))

# 设计新 alias（确保全局唯一）
plan = []          # (card, old_alias, new_alias)
used = set(byid.keys())
for aid, group in dup.items():
    seen = collections.Counter()
    for idx, c in enumerate(group):          # group 已按路径排序
        if idx == 0:
            continue                          # 保留首个（原始短 ID 仍可用）
        suf = series_of(c['norm'], c['inst']) or 'x'
        seen[suf] += 1
        if seen[suf] > 1:
            suf = '%s-%d' % (suf, seen[suf])
        new = '%s·%s' % (aid, suf)
        k = 1
        while new in used:
            k += 1
            new = '%s·%s-%d' % (aid, suf, k)
        used.add(new)
        plan.append((c, aid, new))

# 自证：新 alias 全局唯一，且不与现有任何 alias 冲突
existing = set(byid.keys())
news = [p[2] for p in plan]
assert len(news) == len(set(news)), '新 alias 内部重复！'
clash = [x for x in news if x in existing]
if clash:
    print('!! 与现有 alias 冲突 %d 个（示例 %s）' % (len(clash), clash[:3]))
print('改标 %d 个 alias' % len(plan))
print('样例：')
for c, a, n2 in plan[:12]:
    print('   %-26s → %-40s  [%s]' % (a, n2[:40], os.path.basename(c['path'])[:22]))

if APPLY:
    touch = collections.defaultdict(list)
    for c, a, n2 in plan:
        touch[c['path']].append((a, n2))
    for p, pairs in touch.items():
        raw = open(p, 'rb').read()
        bom = raw[:3] == b'\xef\xbb\xbf'
        t = raw.decode('utf-8-sig').replace('\r\n', '\n')
        for a, n2 in pairs:
            t = t.replace('"%s"' % a, '"%s"' % n2, 1)
        open(p, 'wb').write((b'\xef\xbb\xbf' if bom else b'') + t.encode('utf-8'))
    print('[APPLY] 已写盘 %d 卡' % len(touch))
else:
    print('[DRY-RUN]')
