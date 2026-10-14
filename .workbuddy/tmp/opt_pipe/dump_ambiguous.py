# -*- coding: utf-8 -*-
"""dump 待判定卡的头部自述（每张 H1 + 前 9 行正文，截断）"""
import io, os, re

os.chdir(r'C:\Obsidion\妙妙屋')
D = '00-首页/活跃任务'
def rd(p): return io.open(p, encoding='utf-8-sig').read()
def fmsplit(t):
    m = re.match(r'^---\r?\n(.*?)\r?\n---\r?\n', t, re.S)
    return (m.group(1), t[m.end():]) if m else ('', t)
def get(s, k):
    m = re.search(r'^%s:[ \t]*(.*)$' % re.escape(k), s, re.M)
    return m.group(1).strip().strip('"') if m else None

TARGETS = []
for f in sorted(os.listdir(D)):
    if not f.endswith('.md'):
        continue
    t = rd(os.path.join(D, f))
    s, b = fmsplit(t)
    if get(s, 'type') != '活跃任务卡':
        continue
    st = get(s, 'status')
    if st in ('已填充', '待审核') and not get(s, 'completed'):
        TARGETS.append((f, st, s, b))

print('待判定 %d 张\n' % len(TARGETS))
for f, st, s, b in TARGETS:
    print('━' * 100)
    print('◆ [%s] %s' % (st, f))
    print('   FM: priority=%s updated=%s created=%s' % (get(s, 'priority'), get(s, 'updated'), get(s, 'created')))
    lines = [l for l in b.split('\n') if l.strip()][:9]
    for l in lines:
        print('   ', l[:108])
    print()
