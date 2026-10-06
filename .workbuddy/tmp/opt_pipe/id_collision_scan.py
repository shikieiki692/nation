# -*- coding: utf-8 -*-
"""卡 ID 撞车影响面分析：
  1) 统计重复 ID（按 aliases）与其覆盖卡数
  2) 统计全库 md 中对这些 ID 的**入站 wikilink**数（含 `[[ID]]`、`[[ID|别名]]`、`[[路径/ID...]]`）
  3) 统计来自卡片自身（FM aliases）之外的引用，判断「改 alias 是否安全」
"""
import os, re, sys, glob, collections

sys.stdout.reconfigure(encoding='utf-8')
os.chdir(r'C:\Obsidion\妙妙屋')
BASE = '04-题库/2026机构初赛模拟题'
SRCS = os.listdir(BASE)

byid = collections.defaultdict(list)
for r in SRCS:
    d = os.path.join(BASE, r)
    if not os.path.isdir(d):
        continue
    for p in glob.glob(os.path.join(d, '**', '题-*.md'), recursive=True):
        t = open(p, encoding='utf-8-sig').read().replace('\r\n', '\n')
        m = re.search(r'^aliases:[ \t]*\[(.*?)\]', t, re.M)
        if not m:
            continue
        for a in re.findall(r'"([^"]+)"', m.group(1)):
            byid[a.strip()].append(p.replace(os.sep, '/'))
dup = {k: v for k, v in byid.items() if len(v) > 1}
print('唯一 ID %d ；重复 ID %d ；涉及卡 %d' % (len(byid), len(dup), sum(len(v) for v in dup.values())))

# 扫描全库入站 wikilink
ALL = []
for p in glob.glob('**/*.md', recursive=True):
    pp = p.replace(os.sep, '/')
    if pp.startswith('.git/') or pp.startswith('09-AI工作区/'):
        continue
    ALL.append(pp)
print('全库 md %d' % len(ALL))

dupids = set(dup.keys())
hit = collections.Counter()          # ID -> 引用处数（排除卡自身 FM aliases 行）
for p in ALL:
    try:
        t = open(p, encoding='utf-8-sig').read().replace('\r\n', '\n')
    except Exception:
        continue
    for m in re.finditer(r'\[\[([^\]\|#]+)(?:\|[^\]]*)?\]\]', t):
        tgt = m.group(1).strip().split('/')[-1]
        if tgt.endswith('.md'):
            tgt = tgt[:-3]
        if tgt in dupids:
            hit[tgt] += 1
print('\n被 wikilink 引用的重复 ID：%d 个，共 %d 处' % (len(hit), sum(hit.values())))
for k, v in hit.most_common(20):
    print('   %-18s ×%d   (该 ID 有 %d 张卡)' % (k, v, len(dup[k])))
# 卡片总数中的撞车率
print('\n⇒ 重复 ID 覆盖 %d / %d 卡（%.1f%%）'
      % (sum(len(v) for v in dup.values()), sum(len(v) for v in byid.values()),
         100.0 * sum(len(v) for v in dup.values()) / sum(len(v) for v in byid.values())))
