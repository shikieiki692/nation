# -*- coding: utf-8 -*-
"""扫 FM 隐患：① 值含 ' #' 未加引号（注释截断）② 值含裸 ': ' ③ 以保留字符开头"""
import io, os, re, collections
os.chdir(r'C:\Obsidion\妙妙屋')
from ruamel.yaml import YAML
y = YAML(typ='safe', pure=True); y.version = (1, 2); y.allow_duplicate_keys = True
SKIP_TOP = {'.git', '.workbuddy', '.claude'}

# 匹配 FM 行: key: value （不含列表项 / 注释行 / 空行）
LINE = re.compile(r'^([A-Za-z_][A-Za-z0-9_\-]*):[ \t]*(.*)$')

def quoted(v):
    v = v.strip()
    return (len(v) >= 2 and v[0] == v[-1] and v[0] in ('"', "'")) or v.startswith('[') or v.startswith('{') or v in ('|', '>') or v.startswith('|') or v.startswith('>')

hits = collections.defaultdict(list)
n = 0
for dp, dn, fn in os.walk('.'):
    d = dp.replace('\\', '/')
    top = (d[2:] if d.startswith('./') else d).split('/')[0]
    if top in SKIP_TOP:
        dn[:] = []
        continue
    dn[:] = [x for x in dn if x not in ('_归档', '_archive', '归档', 'node_modules')]
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
        n += 1
        fm = m.group(1)
        # 解析出的字典，用于比对
        try:
            d = y.load(fm) or {}
        except Exception:
            continue
        for ln in fm.split('\n'):
            mm = LINE.match(ln)
            if not mm:
                continue
            k, v = mm.group(1), mm.group(2)
            if quoted(v):
                continue
            # ① ' #' 截断
            if re.search(r'\s#', v):
                parsed = d.get(k)
                literal = v.split(' #')[0].strip().rstrip(',')
                if str(parsed) != literal:
                    hits['注释截断'].append((rel, k, ln[:100]))
            # ② 裸 ': '（未加引号的 mapping 风险）
            if ': ' in v:
                hits['裸冒号'].append((rel, k, ln[:100]))
            # ③ 保留字符开头
            if v[:1] in ('*', '&', '%', '@', '`'):
                hits['保留字符开头'].append((rel, k, ln[:100]))

print('扫过有 FM 文件 = %d' % n)
for cat in ('注释截断', '裸冒号', '保留字符开头'):
    L = hits[cat]
    print()
    print('=== %s (%d) ===' % (cat, len(L)))
    by = collections.Counter(x[0].split('/')[0] for x in L)
    print('    按目录:', dict(by.most_common(8)))
    for rel, k, ln in L[:12]:
        print('    [%s] %s' % (k, ln[:96]))
