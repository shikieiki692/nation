# -*- coding: utf-8 -*-
"""核查「source 里的第N届」是否能在其 source_file 源件中找到 —— 验证届次标注忠于源件。"""
import io, os, re, glob, collections

os.chdir(r'C:\Obsidion\妙妙屋')
BASE = '04-题库/2026机构初赛模拟题/'
cache = {}


def readf(p):
    if p not in cache:
        try:
            cache[p] = io.open(p, encoding='utf-8-sig', errors='replace').read()
        except Exception:
            cache[p] = ''
    return cache[p]


ok = bad = noed = nosrc = 0
badlist = []
for d in sorted(os.listdir(BASE)):
    dp = os.path.join(BASE, d)
    if not os.path.isdir(dp):
        continue
    for p in glob.glob(dp + '/题-*.md'):
        t = io.open(p, encoding='utf-8-sig', errors='replace').read()
        s = re.search(r'^source:[ \t]*"?(.+?)"?[ \t]*$', t, re.M)
        f = re.search(r'^source_file:[ \t]*"?(.+?)"?[ \t]*$', t, re.M)
        if not s:
            continue
        s = s.group(1)
        e = re.search(r'第\s*(\d+)\s*届', s)
        if not e:
            noed += 1
            continue
        ed = e.group(1)
        if not f or not os.path.exists(f.group(1).replace('\\', '/')):
            nosrc += 1
            continue
        body = readf(f.group(1).replace('\\', '/'))
        if re.search(r'第\s*%s\s*届' % ed, body) or re.search(r'%s\s*届' % ed, body):
            ok += 1
        else:
            bad += 1
            badlist.append((d, p, s, f.group(1)))

print('=== 「第N届」标注 vs 源件核验 ===')
print('  源件命中 %d ｜ 源件未见 %d ｜ 无届次 %d ｜ 源件不存在 %d' % (ok, bad, noed, nosrc))
print()
agg = collections.Counter(x[0] for x in badlist)
print('  源件未见（按机构）:', dict(agg))
print()
for x in badlist[:25]:
    print('   [%s] %s' % (x[0], x[2][:64]))
    print('        file= %s' % x[3][:76])
print()
print('=== 带届次的来源（按届次分布）===')
c = collections.Counter()
for d in sorted(os.listdir(BASE)):
    dp = os.path.join(BASE, d)
    if not os.path.isdir(dp):
        continue
    for p in glob.glob(dp + '/题-*.md'):
        t = io.open(p, encoding='utf-8-sig', errors='replace').read()
        s = re.search(r'^source:[ \t]*"?(.+?)"?[ \t]*$', t, re.M)
        if s:
            e = re.search(r'第\s*(\d+)\s*届', s.group(1))
            if e:
                c[(d, e.group(1))] += 1
for k, v in sorted(c.items()):
    print('   %-12s 第%3s届  %d' % (k[0], k[1], v))
