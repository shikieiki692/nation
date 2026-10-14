# -*- coding: utf-8 -*-
"""为「chemmy 内部培训资料」卡补渠道标（区分公开合集）。
渠道判定：source_file 指向 vault 根 `2026机构初赛模拟题/10-chemy/` ⇒ 内部资料；
          再按包名分 2026夏令营 / 2026寒假班。
用法：直接跑=dry-run；加 --apply 落盘。
"""
import io, os, re, glob, sys, shutil, datetime, collections

os.chdir(r'C:\Obsidion\妙妙屋')
APPLY = '--apply' in sys.argv

SUMMER = ['第40届chemy初赛模拟', '第40届chemy初赛无机模拟', '第40届chemy初赛有机模拟',
          '第41届chemy联赛', '第42届chemy联赛', '新-2026年暑假Chemy刷题']


def channel(srcfile):
    n = os.path.basename(srcfile)
    for k in SUMMER:
        if k in n:
            return '2026夏令营'
    if '第39届HiChO' in n:
        return None
    return '2026寒假班'


def new_source(s, ch):
    # 在首个空格前的 "chemy" 之后插入渠道标；并清掉误混入的 source_norm 前缀 "chemy-"
    m = re.match(r'^(chemy)\s+(.*)$', s)
    if not m:
        return None
    rest = re.sub(r'^chemy-', '', m.group(2))
    return 'chemy %s·%s' % (ch, rest)


cards = []
for p in glob.glob('04-题库/2026机构初赛模拟题/chemy/题-*.md'):
    t = io.open(p, encoding='utf-8-sig').read()
    g = lambda k: (re.search(r'^%s:\s*"?(.+?)"?\s*$' % k, t, re.M) or [None, ''])[1]
    sf = g('source_file')
    if not sf.startswith('2026机构初赛模拟题/10-chemy/'):
        continue
    ch = channel(sf)
    if not ch:
        continue
    s = g('source')
    if re.match(r'^chemy 20\d\d(夏令营|寒假班)·', s):
        continue                      # 幂等守卫：已带渠道标则跳过
    ns = new_source(s, ch)
    cards.append((p, s, ns, ch))

print('待改卡数', len(cards))
c = collections.Counter(x[3] for x in cards)
print('渠道分布', dict(c))
print()
print('=== 预览（每渠道 4 条）===')
seen = collections.Counter()
for p, s, ns, ch in cards:
    if seen[ch] < 4:
        print('  [%s]' % ch)
        print('     - %s' % s)
        print('     + %s' % ns)
        seen[ch] += 1
print()
bad = [x for x in cards if not x[2]]
print('无法生成新 source 的卡：', len(bad))
for x in bad[:5]:
    print('   ', x[1])

if not APPLY:
    print('\n[dry-run] 未写盘')
    sys.exit(0)

bak = '.workbuddy/tmp/opt_pipe/_bak/channel_%s' % datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
os.makedirs(bak, exist_ok=True)
n = 0
for p, s, ns, ch in cards:
    if not ns:
        continue
    t = io.open(p, encoding='utf-8-sig').read()
    old_line = 'source: "%s"' % s
    new_line = 'source: "%s"' % ns
    if t.count(old_line) != 1:
        print('!! 断言失败，跳过', p, t.count(old_line))
        continue
    shutil.copy2(p, os.path.join(bak, os.path.basename(p)))
    io.open(p, 'w', encoding='utf-8', newline='').write(t.replace(old_line, new_line))
    n += 1
print('已写盘 %d 卡；备份 %s' % (n, bak))
