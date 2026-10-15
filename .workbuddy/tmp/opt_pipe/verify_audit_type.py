# -*- coding: utf-8 -*-
"""校验本次改动文件的 FM + 列 09-审计报告 剩余非规范 type"""
import io, os, re, subprocess, collections
os.chdir(r'C:\Obsidion\妙妙屋')
from ruamel.yaml import YAML

# 1) 本次改动（已跟踪 M）md
out = subprocess.run(['git', '-c', 'core.quotepath=false', 'diff', '--name-only', '--', '09-审计报告'],
                     capture_output=True, text=True, encoding='utf-8').stdout
mine = [x for x in out.split('\n') if x.endswith('.md')]
print('git diff (M) md =', len(mine))
bad = []
for p in mine:
    t = io.open(p, encoding='utf-8-sig').read()
    m = re.match(r'^---[ \t]*\r?\n(.*?)\r?\n---', t, re.S)
    if not m:
        bad.append((p, '无FM'))
        continue
    y = YAML(typ='safe', pure=True); y.version = (1, 2); y.allow_duplicate_keys = False
    try:
        y.load(m.group(1))
    except Exception as e:
        bad.append((p, str(e).splitlines()[0]))
print('FM strict: %d/%d' % (len(mine) - len(bad), len(mine)))
for p, e in bad:
    print('  FAIL', p, e)

# 2) 剩余非规范 type
print()
print('=== 09-审计报告 剩余非规范 type ===')
y2 = YAML(typ='safe', pure=True); y2.version = (1, 2); y2.allow_duplicate_keys = True
OK = {'审计报告', '活跃任务卡', '系统'}
groups = collections.defaultdict(list)
for dp, dn, fn in os.walk('09-审计报告'):
    for f in sorted(fn):
        if not f.endswith('.md'):
            continue
        p = os.path.join(dp, f).replace('\\', '/')
        t = io.open(p, encoding='utf-8-sig', errors='replace').read()
        m = re.match(r'^---[ \t]*\r?\n(.*?)\r?\n---(\r?\n|$)', t, re.S)
        if not m:
            continue
        try:
            d = y2.load(m.group(1)) or {}
        except Exception:
            groups['(解析失败)'].append(p)
            continue
        if d.get('type') not in OK:
            groups[d.get('type')].append(p)
tot = 0
for k in sorted(groups, key=lambda x: (x is None, str(x))):
    tot += len(groups[k])
    print('◆ %s (%d)' % (repr(k), len(groups[k])))
    for p in groups[k][:16]:
        print('     ', p.replace('09-审计报告/', '')[:86])
print('  剩余非规范合计 =', tot)
