# -*- coding: utf-8 -*-
"""混合修复后的闸门：FM 严格校验 + type 分布复核"""
import io, os, re, subprocess
os.chdir(r'C:\Obsidion\妙妙屋')
from ruamel.yaml import YAML

MINE = []
st = subprocess.run(['git', '-c', 'core.quotepath=false', 'status', '--short', '--untracked-files=all', '09-审计报告', '11-模板/规范'],
                    capture_output=True, text=True, encoding='utf-8').stdout
for ln in st.split('\n'):
    if not ln.strip():
        continue
    code = ln[:2]; p = ln[3:].strip().strip('"')
    if not p.endswith('.md'):
        continue
    if 'chemy' in p or '图升级线' in p:
        continue
    MINE.append(p)
print('本批 md =', len(MINE))
bad = []
for p in MINE:
    t = io.open(p, encoding='utf-8-sig').read()
    m = re.match(r'^---[ \t]*\r?\n(.*?)\r?\n---[ \t]*\r?\n', t, re.S)
    if not m:
        bad.append((p, 'FM 结构不符')); continue
    y = YAML(typ='safe', pure=True); y.version = (1, 2); y.allow_duplicate_keys = False
    try:
        y.load(m.group(1))
    except Exception as e:
        bad.append((p, str(e).splitlines()[0]))
print('FM strict: %d/%d' % (len(MINE) - len(bad), len(MINE)))
for p, e in bad[:8]:
    print('  FAIL', p, e)

# 09-审计报告 type 分布
print()
print('=== 09-审计报告 type 分布（非归档）===')
cnt = {}
y2 = YAML(typ='safe', pure=True); y2.version = (1, 2); y2.allow_duplicate_keys = True
import collections
c = collections.Counter()
for dp, dn, fn in os.walk('09-审计报告'):
    if '_归档' in dp or '归档' in dp:
        continue
    for f in fn:
        if not f.endswith('.md'):
            continue
        t = io.open(os.path.join(dp, f), encoding='utf-8-sig', errors='replace').read()
        m = re.match(r'^---[ \t]*\r?\n(.*?)\r?\n---', t, re.S)
        if not m:
            c['(无FM)'] += 1; continue
        try:
            d = y2.load(m.group(1)) or {}
        except Exception:
            c['(解析失败)'] += 1; continue
        c[d.get('type')] += 1
for k, v in c.most_common(12):
    mark = ' ' if k in ('审计报告', '活跃任务卡', '系统') else '⚠️'
    print('  %s %-14s %d' % (mark, repr(k), v))
