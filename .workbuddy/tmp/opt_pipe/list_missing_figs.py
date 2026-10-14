# -*- coding: utf-8 -*-
r"""列出某卷「源卡有、卷内无」的图（含尺寸与图注上下文），供逐条判定真伪。
用法：python list_missing_figs.py <卷>
"""
import io, os, re, sys, json, hashlib, glob

ROOT = r"C:\Obsidion\妙妙屋"
O = os.path.join(ROOT, '.workbuddy', 'tmp', 'opt_pipe')
V = sys.argv[1] if len(sys.argv) > 1 else 'X'

IMG = re.compile(r'!\[\[([^\]]+)\]\]')
IMG_MD = re.compile(r'!\[[^\]]*\]\(([^)]+)\)')
IMG_DIRS = [r for r, d, f in os.walk(os.path.join(ROOT, '04-题库')) if os.path.basename(r) == 'images']


def ckey(name):
    b = os.path.basename(name)
    for d in IMG_DIRS:
        q = os.path.join(d, b)
        if os.path.isfile(q):
            try:
                return hashlib.sha256(open(q, 'rb').read()).hexdigest()[:12]
            except Exception:
                break
    m = re.match(r'^[0-9a-f]{8,}', b)
    return m.group(0)[:12] if m else b


def find(name):
    b = os.path.basename(name)
    for d in IMG_DIRS:
        q = os.path.join(d, b)
        if os.path.isfile(q):
            return q
    return None


pl = json.load(io.open(os.path.join(O, 'vol_plan_%s.json' % V), encoding='utf-8'))
cards = []
n = 0
for _g, items in pl:
    for it in items:
        n += 1
        cards.append((n, it['path']))

# 卷内图（两版并集）
vol = {}
for tag in ['学生版', '答案版']:
    p = os.path.join(ROOT, '04-题库', '初赛模拟卷%s（非有机·%s）.md' % (V, tag))
    if not os.path.isfile(p):
        continue
    d = io.open(p, encoding='utf-8-sig').read()
    parts = re.split(r'(?m)^### 第 (\d+) 题', d)
    for i in range(1, len(parts), 2):
        vol.setdefault(int(parts[i]), [])
        vol[int(parts[i])].extend(IMG.findall(parts[i + 1]) + IMG_MD.findall(parts[i + 1]))

print('卷 %s —— 源卡有、卷内无 的图（逐条判定）' % V)
print('=' * 100)
for n, cpath in cards:
    cp = os.path.join(ROOT, cpath)
    ct = io.open(cp, encoding='utf-8-sig').read()
    src = IMG.findall(ct) + IMG_MD.findall(ct)
    vs = {ckey(x) for x in vol.get(n, [])}
    miss = [x for x in src if ckey(x) not in vs]
    if not miss:
        continue
    # 去重
    seen, uniq = set(), []
    for x in miss:
        k = ckey(x)
        if k not in seen:
            seen.add(k); uniq.append(x)
    print('\n■ 第 %d 题 ｜ %s' % (n, os.path.basename(cpath)[:56]))
    for x in uniq:
        q = find(x)
        sz = ''
        if q:
            try:
                from PIL import Image
                sz = '%dx%d' % Image.open(q).size
            except Exception:
                sz = '?'
        # 图注上下文：找该图引用后 2 行
        lines = ct.split('\n')
        ctx = ''
        for i, l in enumerate(lines):
            if x in l:
                ctx = ' / '.join(s.strip()[:24] for s in lines[i + 1:i + 3] if s.strip())
                break
        print('   %s  %-9s  %s' % (ckey(x), sz, ctx))
