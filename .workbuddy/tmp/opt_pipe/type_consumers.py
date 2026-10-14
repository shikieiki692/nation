# -*- coding: utf-8 -*-
"""扫全库：谁把 type 当过滤条件（.base / dataviewjs / dataview DQL）"""
import io, os, re
os.chdir(r'C:\Obsidion\妙妙屋')
SKIP = ('.git', '.workbuddy', 'node_modules')
PAT_BASE = re.compile(r'type\s*==\s*["\']([^"\']+)["\']')
PAT_BASE2 = re.compile(r'type\s*!=\s*["\']([^"\']+)["\']')
PAT_DVJS = re.compile(r'\.type\s*[=!]==?\s*["\']([^"\']+)["\']')
PAT_DQL = re.compile(r'(?:WHERE|where)\s+.*?type\s*=\s*["\']([^"\']+)["\']')
fence = re.compile(r'^```')
hits = []
for dp, dn, fn in os.walk('.'):
    dn[:] = [d for d in dn if d not in SKIP]
    for f in fn:
        if not f.endswith(('.md', '.base')):
            continue
        p = os.path.join(dp, f).replace('\\', '/')
        try:
            t = io.open(p, encoding='utf-8-sig', errors='replace').read()
        except Exception:
            continue
        for i, ln in enumerate(t.split('\n'), 1):
            for rx, tag in ((PAT_BASE, 'base=='), (PAT_BASE2, 'base!='),
                            (PAT_DVJS, 'dvjs'), (PAT_DQL, 'dql')):
                for m in rx.finditer(ln):
                    hits.append((p, i, tag, m.group(1), ln.strip()[:90]))
print('=== type 过滤条件（%d 处）===' % len(hits))
cur = None
for p, i, tag, val, raw in hits:
    if p != cur:
        print('◆ %s' % p)
        cur = p
    print('   L%-5d [%-7s] type=%s   %s' % (i, tag, val, raw))
print()
from collections import Counter
print('按被筛的 type 值聚合：', dict(Counter(v for _, _, _, v, _ in hits)))
print('按文件聚合：', dict(Counter(p for p, _, _, _, _ in hits)))
