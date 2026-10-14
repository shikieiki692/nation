# -*- coding: utf-8 -*-
"""侦察 00-首页/活跃任务/ 全量 md 的 FM（type/status/priority）+ git 占用状态"""
import io, os, re, subprocess, collections

os.chdir(r'C:\Obsidion\妙妙屋')
D = '00-首页/活跃任务'

def fm(p):
    t = io.open(p, encoding='utf-8-sig').read()
    m = re.match(r'^---\r?\n(.*?)\r?\n---\r?\n', t, re.S)
    return m.group(1) if m else None

def get(s, k):
    m = re.search(r'^%s:[ \t]*(.*)$' % re.escape(k), s, re.M)
    return m.group(1).strip().strip('"').strip("'") if m else None

files = sorted(f for f in os.listdir(D) if f.endswith('.md'))
print('活跃任务/ md 总数：%d' % len(files))
print()
cnt = collections.Counter()
rows = []
types = collections.Counter(); statuses = collections.Counter()
for f in files:
    p = os.path.join(D, f)
    s = fm(p)
    ty = get(s, 'type') if s else None
    st = get(s, 'status') if s else None
    pr = get(s, 'priority') if s else None
    types[ty] += 1
    if ty == '活跃任务卡':
        statuses[st] += 1
    rows.append((f, ty, st, pr))

print('=== type 分布 ===')
for k, v in types.most_common():
    print('   %-16s %d' % (k, v))
print()
print('=== type=活跃任务卡 的 status 分布 ===')
for k, v in statuses.most_common():
    print('   %-16s %d' % (repr(k), v))
print()

# git 占用
st = subprocess.run(['git', '-c', 'core.quotepath=false', 'status', '--short', D],
                    capture_output=True, text=True, encoding='utf-8').stdout
dirty = set()
for ln in st.split('\n'):
    if not ln.strip():
        continue
    path = ln[3:].strip().strip('"')
    dirty.add(os.path.basename(path))
print('=== 工作区被改动的卡（★＝勿碰）===')
for f, ty, stt, pr in rows:
    if ty != '活跃任务卡':
        continue
    mark = '★' if f in dirty else ' '
    print('  %s %-58s %-12s %s' % (mark, f[:58], repr(stt)[:14], pr))
print()
print('dirty 集合大小：%d' % len(dirty))
for d in sorted(dirty):
    print('   ', d)
