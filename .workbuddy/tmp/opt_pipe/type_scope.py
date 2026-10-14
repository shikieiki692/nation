# -*- coding: utf-8 -*-
"""列出 00-首页 全部非规范 type 文件（含路径），并标并行脏文件"""
import io, os, re, collections
os.chdir(r'C:\Obsidion\妙妙屋')
from ruamel.yaml import YAML
y = YAML(typ='safe')
OK = {'系统', '活跃任务卡', '工作日志'}
rows = []
for dp, dn, fn in os.walk('00-首页'):
    if '.git' in dp or '/归档' in dp or '\\归档' in dp:
        continue
    for f in sorted(fn):
        if not f.endswith('.md'):
            continue
        p = os.path.join(dp, f)
        t = io.open(p, encoding='utf-8-sig').read()
        m = re.match(r'^---\r?\n(.*?)\r?\n---\r?\n', t, re.S)
        if not m:
            continue
        d = y.load(m.group(1)) or {}
        ty = d.get('type')
        if ty not in OK:
            rows.append((p.replace('\\', '/'), ty))
# 并行脏文件
import subprocess
st = subprocess.run(['git', '-c', 'core.quotepath=false', 'status', '--short'],
                    capture_output=True, text=True, encoding='utf-8').stdout
dirty = set()
for ln in st.split('\n'):
    if ln.strip() and '00-首页' in ln:
        dirty.add(ln[3:].strip().strip('"'))
print('=== 00-首页 非规范 type 文件（%d 个，已排除 _归档）===' % len(rows))
byfolder = collections.Counter('/'.join(p.split('/')[:-1]) for p, _ in rows)
print('按目录:', dict(byfolder))
print()
cur = None
for p, ty in sorted(rows):
    fol = '/'.join(p.split('/')[:-1])
    if fol != cur:
        print('◆ %s' % fol)
        cur = fol
    flag = '  ⚠️并行脏' if p in dirty else ''
    print('   %-56s %s%s' % (p.split('/')[-1][:56], repr(ty), flag))
print()
print('并行脏（必须排除）:', sorted(x for x in dirty if x.endswith('.md')))
