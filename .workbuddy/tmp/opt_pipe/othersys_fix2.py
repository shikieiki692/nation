# -*- coding: utf-8 -*-
"""二次补修：备课思路 6 索引 + 02-数据库 2"""
import io, os, re, sys, shutil, datetime
os.chdir(r'C:\Obsidion\妙妙屋')
APPLY = '--apply' in sys.argv
from ruamel.yaml import YAML
y = YAML(typ='safe')
JOBS = [
 ('备课思路/新课大章节-第一轮化学原理.md', '系统', '资源索引'),
 ('备课思路/新课大章节-第一轮结构化学初步.md', '系统', '资源索引'),
 ('备课思路/新课大章节-第二轮元素化学.md', '系统', '资源索引'),
 ('备课思路/新课大章节-第二轮分析化学.md', '系统', '资源索引'),
 ('备课思路/新课大章节-第三轮有机化学.md', '系统', '资源索引'),
 ('备课思路/新课大章节-第三轮结构化学与物理化学深化.md', '系统', '资源索引'),
 ('02-数据库/薄壳KP分诊表.md', '系统', '资源索引'),
 ('02-数据库/片段-真题组卷面板.md', '系统', '资源索引'),
]
def getfm(t):
    m = re.match(r'^---\r?\n(.*?)\r?\n---(\r?\n|$)', t, re.S)
    return (m.group(1), t[m.end():], m) if m else (None, t, None)
plan = []
for p, ty, r in JOBS:
    t = io.open(p, encoding='utf-8-sig').read()
    s, body, m = getfm(t)
    cur = (y.load(s) or {}) if s else {}
    if cur.get('type') == ty and cur.get('role') == r:
        continue
    plan.append((p, cur.get('type'), cur.get('role'), ty, r, s is not None))
print('=== 待改 %d ===' % len(plan))
for p, ct, cr, ty, r, hf in plan:
    print('   %-48s type=%s→%s role=%s→%s' % (p[:48], ct, ty, cr, r))
if not APPLY:
    print('（dry-run）'); sys.exit(0)
bak = '.workbuddy/tmp/opt_pipe/_bak/othersys2_%s' % datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
os.makedirs(bak, exist_ok=True); n = 0
for p, ct, cr, ty, r, hf in plan:
    shutil.copy2(p, os.path.join(bak, os.path.basename(p)))
    t = io.open(p, encoding='utf-8-sig').read()
    s, body, m = getfm(t)
    if hf:
        nl = '\r\n' if '\r\n' in t[:m.end()] else '\n'
        if re.search(r'^type:', s, re.M):
            s = re.sub(r'^type:[ \t]*.*$', 'type: ' + ty, s, count=1, flags=re.M)
        else:
            s = 'type: ' + ty + nl + s
        if re.search(r'^role:', s, re.M):
            s = re.sub(r'^role:[ \t]*.*$', 'role: ' + r, s, count=1, flags=re.M)
        else:
            s = s + nl + 'role: ' + r
    else:
        nl = '\n'
        h1 = next((l[2:].strip() for l in body.split('\n') if l.startswith('# ')), os.path.basename(p)[:-3])
        s = nl.join(['title: ' + h1, 'type: ' + ty, 'role: ' + r]); body = nl + body
    io.open(p, 'w', encoding='utf-8', newline='').write('---' + nl + s + nl + '---' + nl + body); n += 1
print('已写盘 %d（备份 %s）' % (n, bak))
