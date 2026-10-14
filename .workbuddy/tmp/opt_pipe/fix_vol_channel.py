# -*- coding: utf-8 -*-
"""把卷内 `> 来源` 行同步为带渠道标的新写法（仅内部资料渠道；公开合集不动）。"""
import io, os, re, glob, shutil, datetime, sys

os.chdir(r'C:\Obsidion\妙妙屋')
APPLY = '--apply' in sys.argv

BAK = sorted(glob.glob('.workbuddy/tmp/opt_pipe/_bak/channel_*'))[-1]
print('用备份对照：', BAK)

# 构造 旧source -> 新source 映射
pairs = []
for old_p in glob.glob(BAK + '/*.md'):
    cur_p = '04-题库/2026机构初赛模拟题/chemy/' + os.path.basename(old_p)
    if not os.path.exists(cur_p):
        continue
    go = re.search(r'^source:\s*"?(.+?)"?\s*$', io.open(old_p, encoding='utf-8-sig').read(), re.M)
    gn = re.search(r'^source:\s*"?(.+?)"?\s*$', io.open(cur_p, encoding='utf-8-sig').read(), re.M)
    if go and gn and go.group(1) != gn.group(1):
        pairs.append((go.group(1), gn.group(1)))
print('映射对', len(pairs))

VOLS = sorted(glob.glob('04-题库/初赛模拟卷*（非有机·答案版）.md'))
plan = []
for v in VOLS:
    t = io.open(v, encoding='utf-8-sig').read()
    n = 0
    for o, nw in pairs:
        c = t.count(o)
        if c:
            t = t.replace(o, nw)
            n += c
    if n:
        plan.append((v, n, t))

print('涉及卷数', len(plan), '共替换', sum(x[1] for x in plan))
for v, n, _ in plan:
    print('   %-46s %d 处' % (os.path.basename(v), n))

# 兜底：看卷里还剩多少未带渠道标的 chemmy 内部资料来源行
LEFT = re.compile(r'^>\s*来源[:：]\s*chemy (?!20\d\d(夏令营|寒假班))(.+)$', re.M)
rest = 0
for v, n, t in plan:
    for m in LEFT.finditer(t):
        if re.search(r'第40届chemy初赛|第4[12]届chemy联赛|新-2026年暑假Chemy刷题|chemy-初赛模拟|chemy-15套卷|第三十九届Chemy化学奥林匹克竞赛联赛5', m.group(2)):
            rest += 1
            print('   残留:', os.path.basename(v), '|', m.group(2)[:70])
print('内部资料类残留未改:', rest)

if not APPLY:
    print('\n[dry-run] 未写盘')
    sys.exit(0)

bak = '.workbuddy/tmp/opt_pipe/_bak/vol_channel_%s' % datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
os.makedirs(bak, exist_ok=True)
for v, n, t in plan:
    shutil.copy2(v, os.path.join(bak, os.path.basename(v)))
    io.open(v, 'w', encoding='utf-8', newline='').write(t)
print('已写盘 %d 卷；备份 %s' % (len(plan), bak))
