# -*- coding: utf-8 -*-
"""09-审计报告 type 明细（只读）"""
import io, os, re, collections
os.chdir(r'C:\Obsidion\妙妙屋')
from ruamel.yaml import YAML
y = YAML(typ='safe', pure=True); y.version = (1, 2); y.allow_duplicate_keys = True

D = '09-审计报告'
cnt = collections.Counter()
det = collections.defaultdict(list)
for dp, dn, fn in os.walk(D):
    dn[:] = [x for x in dn if x not in ('_归档', '_archive', '归档')]
    for f in sorted(fn):
        if not f.endswith('.md'):
            continue
        p = os.path.join(dp, f).replace('\\', '/')
        t = io.open(p, encoding='utf-8-sig', errors='replace').read()
        m = re.match(r'^---[ \t]*\r?\n(.*?)\r?\n---(\r?\n|$)', t, re.S)
        if not m:
            cnt['(无FM)'] += 1
            det['(无FM)'].append(p)
            continue
        try:
            d = y.load(m.group(1)) or {}
        except Exception:
            cnt['(解析失败)'] += 1
            det['(解析失败)'].append(p)
            continue
        ty = d.get('type')
        cnt[ty] += 1
        det[ty].append(p)

print('=== 09-审计报告 type 分布 ===')
for k, v in cnt.most_common():
    mark = ' ' if k in ('审计报告', '活跃任务卡', '系统') else '⚠️'
    print('  %s %-16s %d' % (mark, repr(k), v))
print()
print('=== 需归一/补全的明细 ===')
for k in cnt:
    if k in ('审计报告', '活跃任务卡', '系统'):
        continue
    print('◆ %s (%d)' % (repr(k), len(det[k])))
    for p in det[k][:30]:
        print('   ', p[:92])
    print()
