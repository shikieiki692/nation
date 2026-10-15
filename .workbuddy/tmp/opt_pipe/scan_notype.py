# -*- coding: utf-8 -*-
"""全库「有FM但无type」与「无FM」盘点（只读）"""
import io, os, re, collections
os.chdir(r'C:\Obsidion\妙妙屋')
from ruamel.yaml import YAML
y = YAML(typ='safe')

by_dir = collections.defaultdict(lambda: {'nofm': [], 'notype': []})
for dp, dn, fn in os.walk('.'):
    d = dp.replace('\\', '/')
    if d.startswith('./.git') or d.startswith('./.workbuddy'):
        continue
    if '_归档' in d or '_archive' in d or '归档' in d:
        continue
    for f in fn:
        if not f.endswith('.md'):
            continue
        p = os.path.join(dp, f).replace('\\', '/')
        rel = p[2:] if p.startswith('./') else p
        top = rel.split('/')[0]
        try:
            t = io.open(p, encoding='utf-8-sig', errors='replace').read()
        except Exception:
            continue
        m = re.match(r'^---\r?\n(.*?)\r?\n---(\r?\n|$)', t, re.S)
        if not m:
            by_dir[top]['nofm'].append(rel)
            continue
        try:
            dd = y.load(m.group(1)) or {}
        except Exception:
            by_dir[top]['notype'].append(rel + '  (FM解析失败)')
            continue
        if not dd.get('type'):
            by_dir[top]['notype'].append(rel)

print('=== 各顶层目录：无 FM / 有FM无type ===')
tn = tt = 0
for T in sorted(by_dir):
    a = by_dir[T]['nofm']; b = by_dir[T]['notype']
    if not a and not b:
        continue
    tn += len(a); tt += len(b)
    print('  ◆ %-22s 无FM %-4d ｜ 有FM无type %-4d' % (T, len(a), len(b)))
print()
print('合计：无 FM %d ｜ 有FM无type %d' % (tn, tt))
print()
print('=== 明细（有FM无type）===')
for T in sorted(by_dir):
    b = by_dir[T]['notype']
    if not b:
        continue
    print('◆', T, '(%d)' % len(b))
    for p in b[:40]:
        print('   ', p[:92])
print()
print('=== 明细（无 FM）===')
for T in sorted(by_dir):
    a = by_dir[T]['nofm']
    if not a:
        continue
    print('◆', T, '(%d)' % len(a))
    for p in a[:30]:
        print('   ', p[:92])
