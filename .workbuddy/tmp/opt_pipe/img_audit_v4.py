# -*- coding: utf-8 -*-
"""图引用体检 v4（修正正则）：全 04-题库 —— 断链 / 畸形(单方括号) / 扩展名错配。
正则要点：扩展名必须落在捕获组内，禁用非贪婪吃扩展名的写法（v3 的坑）。"""
import io, os, re, glob, collections

os.chdir(r'C:\Obsidion\妙妙屋')
SKIP = ('.git', '.workbuddy', '_bak', '_归档', '_待清理')
EXT = r'(?:jpg|jpeg|png|webp|gif|svg)'
BYSTEM = collections.defaultdict(set)
NAMES = set()
for dp, dn, fn in os.walk('.'):
    dn[:] = [d for d in dn if d not in SKIP and not d.startswith('.git')]
    for f in fn:
        e = os.path.splitext(f)[1].lower().lstrip('.')
        if e in ('jpg', 'jpeg', 'png', 'webp', 'gif', 'svg'):
            NAMES.add(f)
            BYSTEM[os.path.splitext(f)[0]].add(e)

R1 = re.compile(r'!\[\[([^\]|]+\.' + EXT + r')(?:\|[^\]]*)?\]\]', re.I)   # ![[name.ext]]
R2 = re.compile(r'!\[[^\]]*\]\(([^)]+\.' + EXT + r')\)', re.I)            # ![](path)
R3 = re.compile(r'<img[^>]*src="([^"]+\.' + EXT + r')"', re.I)
BAD = re.compile(r'!\[([^\[\]]*?\.' + EXT + r')\]', re.I)                 # 单方括号 ![name.ext]

tot = miss = bad = extmis = 0
misslist, badlist, extlist = [], [], []
nfiles = 0
for f in glob.glob('04-题库/**/*.md', recursive=True):
    nfiles += 1
    t = io.open(f, encoding='utf-8-sig', errors='replace').read()
    refs = []
    for rx in (R1, R2, R3):
        refs += rx.findall(t)
    tot += len(refs)
    for r in refs:
        b = os.path.basename(r.replace('\\', '/'))
        if b in NAMES:
            continue
        stem, e = os.path.splitext(b)
        if stem in BYSTEM:
            extmis += 1
            extlist.append((f, b, sorted(BYSTEM[stem])))
        else:
            miss += 1
            misslist.append((f, b))
    for m in BAD.finditer(t):
        bad += 1
        badlist.append((f, m.group(1)))

print('扫描 04-题库 %d 个 md ｜ 图引用 %d' % (nfiles, tot))
print('  真断链（文件名全库不存在）: %d' % miss)
print('  扩展名错配（同名异扩展名）  : %d' % extmis)
print('  畸形引用（单方括号）        : %d' % bad)
print()
print('--- 真断链（前 12）---')
for x in misslist[:12]:
    print('   %s → %s' % (os.path.basename(x[0])[:46], x[1][:66]))
print()
print('--- 扩展名错配（前 12）---')
for x in extlist[:12]:
    print('   %s → %s  (实际: %s)' % (os.path.basename(x[0])[:40], x[1][:58], ','.join(x[2])))
print()
print('--- 畸形（前 12）---')
for x in badlist[:12]:
    print('   %s → %s' % (os.path.basename(x[0])[:46], x[1][:66]))
