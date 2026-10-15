# -*- coding: utf-8 -*-
"""A 类系统层页归一：02-数据库/06-学生侧材料/备课思路/10-索引与统计 的 README/索引/入口页"""
import io, os, re, sys, shutil, datetime
os.chdir(r'C:\Obsidion\妙妙屋')
APPLY = '--apply' in sys.argv
from ruamel.yaml import YAML
y = YAML(typ='safe')
# (path, 目标type, 目标role)
JOBS = [
 ('02-数据库/README.md', '系统', '工具说明'),
 ('06-学生侧材料/README.md', '系统', '资源索引'),
 ('06-学生侧材料/策略卡/README.md', '系统', '资源索引'),
 ('06-学生侧材料/练习卷/README.md', '系统', '资源索引'),
 ('06-学生侧材料/讲义/README-讲义docx产物目录.md', '系统', '资源索引'),
 ('06-学生侧材料/闪卡/README.md', '系统', '资源索引'),
 ('06-学生侧材料/闪卡/anki-export/README.md', '系统', '工具说明'),
 ('06-学生侧材料/闪卡/试印版/README.md', '系统', '资源索引'),
 ('备课思路/README.md', '系统', '方向指引'),
 ('备课思路/高中化学教材索引.md', '系统', '资源索引'),
 ('10-索引与统计/00-图谱雷达总入口.md', '系统', '资源索引'),
 ('10-索引与统计/01-有机化学图谱总索引.md', '系统', '资源索引'),
 ('10-索引与统计/02-结构与无机化学图谱总索引.md', '系统', '资源索引'),
 ('10-索引与统计/03-物化与分析化学图谱总索引.md', '系统', '资源索引'),
 ('10-索引与统计/04-考点题源索引.md', '系统', '资源索引'),
 ('10-索引与统计/90-外部资源导航.md', '系统', '资源索引'),
 ('10-索引与统计/README.md', '系统', '资源索引'),
 ('10-索引与统计/全库核心图谱总索引.md', '系统', '资源索引'),
 ('10-索引与统计/视觉已验证图片索引.md', '系统', '资源索引'),
 ('10-索引与统计/知识点总索引.md', '系统', '资源索引'),
 ('10-索引与统计/讲义用图补录/README.md', '系统', '资源索引'),
]
def getfm(t):
    m = re.match(r'^---\r?\n(.*?)\r?\n---(\r?\n|$)', t, re.S)
    return (m.group(1), t[m.end():], m) if m else (None, t, None)
plan = []
for p, ty, r in JOBS:
    if not os.path.exists(p):
        plan.append((p, '(缺)', None, ty, r, None)); continue
    t = io.open(p, encoding='utf-8-sig').read()
    s, body, m = getfm(t)
    cur = (y.load(s) or {}) if s else {}
    if cur.get('type') == ty and cur.get('role') == r:
        continue
    plan.append((p, cur.get('type'), cur.get('role'), ty, r, s is not None))
print('=== 待改 %d ===' % len(plan))
for p, ct, cr, ty, r, hf in plan:
    print('   %-50s type=%s→%s role=%s→%s' % (p[:50], ct, ty, cr, r))
if not APPLY:
    print('（dry-run）'); sys.exit(0)
bak = '.workbuddy/tmp/opt_pipe/_bak/othersys_%s' % datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
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
