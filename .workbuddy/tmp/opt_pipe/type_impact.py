# -*- coding: utf-8 -*-
"""type 归一：现状 / 目标映射 / 视图影响面"""
import io, os, re, collections
os.chdir(r'C:\Obsidion\妙妙屋')
from ruamel.yaml import YAML
y = YAML(typ='safe')
D = '00-首页/活跃任务'

def rf(p):
    return io.open(p, encoding='utf-8-sig').read()

def fm(t):
    m = re.match(r'^---\r?\n(.*?)\r?\n---\r?\n', t, re.S)
    return m.group(1) if m else None

# 1. 当前 00-首页 全库 type: 系统 计数
cnt = collections.Counter()
for dp, dn, fn in os.walk('00-首页'):
    if '.git' in dp:
        continue
    for f in fn:
        if not f.endswith('.md'):
            continue
        s = fm(rf(os.path.join(dp, f)))
        if s is None:
            continue
        d = y.load(s) or {}
        cnt[d.get('type')] += 1
print('=== 00-首页 全库 type 分布（含子目录）===')
for k, v in sorted(cnt.items(), key=lambda x: (x[0] is None, -x[1])):
    print('   %-14s %d' % (repr(k), v))

# 2. 活跃任务 目录的映射
rows = []
for f in sorted(os.listdir(D)):
    if not f.endswith('.md'):
        continue
    s = fm(rf(os.path.join(D, f)))
    d = (y.load(s) or {}) if s else {}
    rows.append((f, d.get('type')))
print()
print('=== 活跃任务/ 映射（%d 文件）===' % len(rows))
mapping = collections.Counter()
for f, ty in rows:
    tgt = '活跃任务卡' if ty == '活跃任务卡' else '系统'
    mapping[tgt] += 1
print('   映射结果:', dict(mapping))
print()
print('=== 将变为「系统」的 %d 个文件 ===' % mapping['系统'])
n = 0
for f, ty in rows:
    if ty != '活跃任务卡':
        n += 1
        print('   %-58s  %s → 系统' % (f[:58], repr(ty)))
print('   合计 %d' % n)

# 3. 视图影响：哪些 dataview/base 会被波及
print()
print('=== 波及的视图（FROM "00-首页" + type 过滤）===')
for dp, dn, fn in os.walk('.'):
    if '.git' in dp or '.workbuddy' in dp:
        continue
    for f in fn:
        if not f.endswith(('.md', '.base')):
            continue
        p = os.path.join(dp, f).replace('\\', '/')
        t = rf(p)
        if '00-首页' in t and re.search(r'type\s*[=!]==?\s*["\']系统["\']', t):
            for i, ln in enumerate(t.split('\n'), 1):
                if '00-首页' in ln or re.search(r'type\s*[=!]==?\s*["\']系统["\']', ln):
                    print('   %s:%d  %s' % (p.replace('./', ''), i, ln.strip()[:80]))
