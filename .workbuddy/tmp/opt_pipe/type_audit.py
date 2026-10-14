# -*- coding: utf-8 -*-
"""type 归一影响面审计：分布 / 逐文件 / 消费方"""
import io, os, re, collections, subprocess
os.chdir(r'C:\Obsidion\妙妙屋')
D = '00-首页/活跃任务'

def fm(t):
    m = re.match(r'^---\r?\n(.*?)\r?\n---\r?\n', t, re.S)
    return m.group(1) if m else ''

def g(s, k):
    m = re.search(r'^%s:[ \t]*(.*)$' % k, s, re.M)
    return m.group(1).strip() if m else None

rows = []
for f in sorted(os.listdir(D)):
    if not f.endswith('.md'):
        continue
    t = io.open(os.path.join(D, f), encoding='utf-8-sig').read()
    s = fm(t)
    rows.append((f, g(s, 'type'), g(s, 'status'), g(s, 'area')))

c = collections.Counter(r[1] for r in rows)
print('=== type 分布（%d 个 md）===' % len(rows))
for k, v in sorted(c.items(), key=lambda x: (x[0] is None, -x[1])):
    print('   %-14s %d' % (repr(k), v))
print()
print('=== 非「活跃任务卡」逐文件（按 type 分组）===')
bytype = collections.defaultdict(list)
for f, ty, st, ar in rows:
    if ty != '活跃任务卡':
        bytype[ty].append(f)
for k in sorted(bytype, key=lambda x: (x is None, x)):
    print('◆ type=%s (%d)' % (repr(k), len(bytype[k])))
    for f in bytype[k]:
        print('     %s' % f[:66])
    print()

print('=== 消费方：谁读 type ===')
for pat in ['活跃任务卡', '活跃任务计划', '"交接"', 'type ==']:
    r = subprocess.run(['git', 'grep', '-l', pat, '--', '*.base', '*.js', '*.py', '*.md'],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    hits = [l for l in (r.stdout or '').split('\n') if l.strip() and '.workbuddy/' not in l][:8]
    print('  [%s] → %s' % (pat, hits if hits else '(无)'))
