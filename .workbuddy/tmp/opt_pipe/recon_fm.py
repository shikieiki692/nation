# -*- coding: utf-8 -*-
"""侦察：① 无 role 的系统页 ② 现有 role 分布 ③ 无 FM 文件 ④ FM 惯例"""
import io, os, re, collections
os.chdir(r'C:\Obsidion\妙妙屋')
from ruamel.yaml import YAML
y = YAML(typ='safe')
SKIPDIR = ('归档', '_archive')

def read(p):
    return io.open(p, encoding='utf-8-sig').read()

def getfm(t):
    m = re.match(r'^---\r?\n(.*?)\r?\n---(\r?\n|$)', t, re.S)
    return (m.group(1), t[m.end():]) if m else (None, t)

norole = []      # 系统页缺 role
roles = collections.Counter()
nofm = []
for dp, dn, fn in os.walk('00-首页'):
    if '.git' in dp:
        continue
    if any(s in dp for s in SKIPDIR):
        continue
    for f in sorted(fn):
        if not f.endswith('.md'):
            continue
        p = os.path.join(dp, f).replace('\\', '/')
        t = read(p)
        s, body = getfm(t)
        if s is None:
            h1 = next((l[2:].strip() for l in body.split('\n') if l.startswith('# ')), '')
            nofm.append((p, h1))
            continue
        d = y.load(s) or {}
        if d.get('type') == '系统':
            roles[d.get('role')] += 1
            if not d.get('role'):
                h1 = next((l[2:].strip() for l in body.split('\n') if l.startswith('# ')), '')
                norole.append((p, h1[:46]))
print('=== ① 系统页缺 role（%d）===' % len(norole))
for p, h in norole:
    print('   %-58s | %s' % (p.replace('00-首页/', '')[:58], h))
print()
print('=== ② 现有 role 分布 ===')
for k, v in roles.most_common():
    print('   %-16s %d' % (repr(k), v))
print()
print('=== ③ 无 FM 文件（%d）===' % len(nofm))
for p, h in nofm:
    print('   %-58s | %s' % (p.replace('00-首页/', '')[:58], h[:40]))
