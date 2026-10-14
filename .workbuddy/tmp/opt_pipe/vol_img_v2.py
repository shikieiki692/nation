# -*- coding: utf-8 -*-
"""卷族图引用体检（v2）：建全库图片名索引后再判断链。"""
import io, os, re, glob, collections

os.chdir(r'C:\Obsidion\妙妙屋')
IDX = collections.defaultdict(list)
for dp, dn, fn in os.walk('04-题库'):
    for f in fn:
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif')):
            IDX[f].append(os.path.join(dp, f))
print('全库图片文件数', sum(len(v) for v in IDX.values()), '｜ 唯一名', len(IDX))

OK1 = re.compile(r'!\[\[([^\]|]+?)\.(?:jpg|jpeg|png|webp|gif)(?:\|[^\]]*)?\]\]')
OK2 = re.compile(r'!\[[^\]]*\]\(([^)]+)\)')
OK3 = re.compile(r'<img[^>]*src="([^"]+)"')

tot = miss = 0
misslist = []
per_vol = collections.Counter()
for v in sorted(glob.glob('04-题库/初赛模拟卷*.md')):
    t = io.open(v, encoding='utf-8-sig').read()
    refs = []
    for rx in (OK1, OK2, OK3):
        for r in rx.finditer(t):
            s = r.group(1).strip().replace('\\', '/')
            refs.append(s if s.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif')) else s + '.jpg')
    tot += len(refs)
    for r in refs:
        base = os.path.basename(r)
        stem = steam = os.path.splitext(base)[0]
        if base in IDX or (stem + any(e for e in ['.jpg'] ) if False else False):
            continue
        # 也允许无扩展名索引（卷里可能只写 hash）
        hit = base in IDX or any(k.startswith(stem) for k in IDX)
        if not hit:
            miss += 1
            per_vol[os.path.basename(v)] += 1
            if len(misslist) < 10:
                misslist.append((os.path.basename(v), r))

print('卷族图引用 %d ｜ 断链 %d' % (tot, miss))
for k, v in per_vol.most_common(10):
    print('   %-44s %d' % (k, v))
for x in misslist:
    print('   例:', x[0], '→', x[1][:80])
