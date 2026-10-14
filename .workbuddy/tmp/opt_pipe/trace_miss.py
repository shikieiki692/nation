# -*- coding: utf-8 -*-
"""chemy 的 240 张 source_file 缺失卡：追查指向、判定性质。"""
import io, os, re, glob, collections

os.chdir(r'C:\Obsidion\妙妙屋')
BASE = '04-题库/2026机构初赛模拟题/chemy/'

miss = collections.Counter()
samples = {}
for p in glob.glob(BASE + '题-*.md'):
    t = io.open(p, encoding='utf-8-sig', errors='replace').read()
    m = re.search(r'^source_file:[ \t]*"?(.+?)"?[ \t]*$', t, re.M)
    sf = m.group(1) if m else ''
    if sf and not os.path.exists(sf.replace('\\', '/')):
        miss[sf] += 1
        samples.setdefault(sf, (p, re.search(r'^source:[ \t]*"?(.+?)"?[ \t]*$', t, re.M).group(1) if re.search(r'^source:[ \t]*"?(.+?)"?[ \t]*$', t, re.M) else ''))

print('=== 缺失的 source_file 值（%d 种 / %d 卡）===' % (len(miss), sum(miss.values())))
for k, v in miss.most_common():
    print('   %4d  %s' % (v, k))
    print('         例卡 source: %s' % samples[k][1][:70])
print()
print('=== 全库是否存在该名称的文件 ===')
for k in miss:
    name = os.path.basename(k)
    found = glob.glob('**/' + name, recursive=True)
    found = [f for f in found if not f.startswith('.git')]
    print('   %-56s → %s' % (name[:56], found[:2] if found else '**未找到**'))
print()
print('=== chemy 卡 source_file 后缀分布 ===')
suf = collections.Counter()
for p in glob.glob(BASE + '题-*.md'):
    t = io.open(p, encoding='utf-8-sig', errors='replace').read()
    m = re.search(r'^source_file:[ \t]*"?(.+?)"?[ \t]*$', t, re.M)
    if m:
        suf[os.path.splitext(m.group(1))[1] or '(无后缀)'] += 1
print('  ', dict(suf))
