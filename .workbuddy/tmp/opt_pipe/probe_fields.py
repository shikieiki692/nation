# -*- coding: utf-8 -*-
"""用 ruamel(py3.12) 直读 32 张卡的三字段真值 + 既有写法样例"""
import io, os, re, sys
os.chdir(r'C:\Obsidion\妙妙屋')
from ruamel.yaml import YAML
yaml = YAML(typ='safe')
D = '00-首页/活跃任务'
def rd(p): return io.open(p, encoding='utf-8-sig').read()

rows = []
for f in sorted(os.listdir(D)):
    if not f.endswith('.md'):
        continue
    t = rd(os.path.join(D, f))
    m = re.match(r'^---\r?\n(.*?)\r?\n---\r?\n', t, re.S)
    if not m:
        continue
    try:
        d = yaml.load(m.group(1)) or {}
    except Exception as e:
        print('PARSE FAIL', f, e); continue
    if d.get('type') != '活跃任务卡':
        continue
    rows.append((f, d))

print('=== YAML 级三字段真值（缺失/空 ⇒ 会触发健康检查）===')
import collections
miss = collections.Counter()
for f, d in rows:
    flags = []
    for k in ('source_notes', 'related_notes', 'evidence'):
        v = d.get(k)
        if not v:
            flags.append(k)
            miss[k] += 1
    if flags:
        print('  %-52s 缺 %s' % (f[:52], flags))
print()
print('YAML 级缺口：source_notes %d ｜ related_notes %d ｜ evidence %d' % (miss['source_notes'], miss['related_notes'], miss['evidence']))
print()
print('=== 既有写法样例（含三字段的卡，取 2 张）===')
n = 0
for f, d in rows:
    if d.get('source_notes') and d.get('related_notes') and d.get('evidence'):
        print('◆', f[:56])
        for k in ('source_notes', 'related_notes', 'evidence'):
            v = d[k]
            print('   %-15s %s' % (k, (v if not isinstance(v, list) else v[:2])))
        n += 1
        if n >= 3:
            break
print()
print('=== 全部类型统计 ===')
print('  source_notes 非空 %d/%d' % (len(rows) - miss['source_notes'], len(rows)))
print('  related_notes 非空 %d/%d' % (len(rows) - miss['related_notes'], len(rows)))
print('  evidence 非空 %d/%d' % (len(rows) - miss['evidence'], len(rows)))
