# -*- coding: utf-8 -*-
"""全库 FM 严格校验（ruamel YAML 1.2 safe + 拒重复键）：找会 THROW 的 FM"""
import io, os, re, sys, collections, json
os.chdir(r'C:\Obsidion\妙妙屋')
from ruamel.yaml import YAML
from ruamel.yaml.constructor import DuplicateKeyError

SKIP_TOP = {'.git', '.workbuddy', '.claude'}

def strict_parse(src):
    y = YAML(typ='safe', pure=True)
    y.version = (1, 2)
    y.allow_duplicate_keys = False
    try:
        y.load(src)
        return None
    except DuplicateKeyError as e:
        return '重复键: ' + str(e).splitlines()[0]
    except Exception as e:
        s = str(e).splitlines()[0] if str(e) else type(e).__name__
        return s

fails = []
total = 0
for dp, dn, fn in os.walk('.'):
    d = dp.replace('\\', '/')
    top = (d[2:] if d.startswith('./') else d).split('/')[0]
    if top in SKIP_TOP:
        dn[:] = []
        continue
    dn[:] = [x for x in dn if not (x in ('_归档', '_archive', '归档', 'node_modules'))]
    for f in fn:
        if not f.endswith('.md'):
            continue
        p = os.path.join(dp, f).replace('\\', '/')
        rel = p[2:] if p.startswith('./') else p
        try:
            t = io.open(p, encoding='utf-8-sig', errors='replace').read()
        except Exception:
            continue
        m = re.match(r'^---[ \t]*\r?\n(.*?)\r?\n---(\r?\n|$)', t, re.S)
        if not m:
            continue
        total += 1
        err = strict_parse(m.group(1))
        if err:
            fails.append((rel, err))

print('有 FM 的文件 = %d ｜ 严格校验失败 = %d' % (total, len(fails)))
print()
by_top = collections.defaultdict(list)
for rel, err in fails:
    by_top[rel.split('/')[0]].append((rel, err))
for T in sorted(by_top):
    print('◆ %s (%d)' % (T, len(by_top[T])))
    for rel, err in by_top[T][:25]:
        print('   [%s] %s' % (err[:42], rel[:82]))
