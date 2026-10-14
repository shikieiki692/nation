# -*- coding: utf-8 -*-
"""卷族图引用体检（v3）：全库（排除 .git/.workbuddy/备份）图片名索引。"""
import io, os, re, glob, collections

os.chdir(r'C:\Obsidion\妙妙屋')
IDX = set()
SKIP = ('.git', '.workbuddy', '_bak', '_归档', '_待清理')
n = 0
for dp, dn, fn in os.walk('.'):
    dn[:] = [d for d in dn if d not in SKIP and not d.startswith('.git')]
    for f in fn:
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif', '.svg')):
            IDX.add(f)
            n += 1
print('全库图片文件 %d ｜ 唯一名 %d' % (n, len(IDX)))

OK1 = re.compile(r'!\[\[([^\]|]+?)\.(?:jpg|jpeg|png|webp|gif|svg)(?:\|[^\]]*)?\]\]')
OK2 = re.compile(r'!\[[^\]]*\]\(([^)]+)\)')
OK3 = re.compile(r'<img[^>]*src="([^"]+)"')

tot = miss = 0
per_vol = collections.Counter()
examples = []
for v in sorted(glob.glob('04-题库/初赛模拟卷*.md')):
    t = io.open(v, encoding='utf-8-sig').read()
    refs = []
    for rx in (OK1, OK2, OK3):
        for r in rx.finditer(t):
            s = r.group(1).strip().replace('\\', '/')
            if not s.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif', '.svg')):
                s += '.jpg'
            refs.append(s)
    tot += len(refs)
    for r in refs:
        b = os.path.basename(r)
        if b not in IDX:
            miss += 1
            per_vol[os.path.basename(v)] += 1
            if len(examples) < 10:
                examples.append((os.path.basename(v), r))

print('卷族图引用 %d ｜ 断链 %d' % (tot, miss))
for k, v in per_vol.most_common():
    print('   %-44s %d' % (k, v))
for x in examples:
    print('   例:', x[0], '→', x[1][:80])
