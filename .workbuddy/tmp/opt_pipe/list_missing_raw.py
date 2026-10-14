# -*- coding: utf-8 -*-
r"""列出「源卡引用、卷内未引用」的图：输出 **原始图名**（非内容 sha）+ 文件路径 + 源卡出处。
用法：python list_missing_raw.py <卷>
"""
import io, os, re, sys, json, hashlib
from PIL import Image

ROOT = r"C:\Obsidion\妙妙屋"
O = os.path.join(ROOT, '.workbuddy', 'tmp', 'opt_pipe')
V = sys.argv[1]
IMG = re.compile(r'!\[\[([^\]]+)\]\]')
IMG_MD = re.compile(r'!\[[^\]]*\]\(([^)]+)\)')
IMG_DIRS = [r for r, d, f in os.walk(os.path.join(ROOT, '04-题库')) if os.path.basename(r) == 'images']


def ckey(name):
    b = os.path.basename(name)
    for d in IMG_DIRS:
        q = os.path.join(d, b)
        if os.path.isfile(q):
            return hashlib.sha256(open(q, 'rb').read()).hexdigest()[:12]
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
cards, n = [], 0
for _g, items in pl:
    for it in items:
        n += 1
        cards.append((n, it['path']))

vol = {}
for tag in ['学生版', '答案版']:
    p = os.path.join(ROOT, '04-题库', '初赛模拟卷%s（非有机·%s）.md' % (V, tag))
    if os.path.isfile(p):
        d = io.open(p, encoding='utf-8-sig').read()
        parts = re.split(r'(?m)^### 第 (\d+) 题', d)
        for i in range(1, len(parts), 2):
            vol.setdefault(int(parts[i]), [])
            vol[int(parts[i])].extend(IMG.findall(parts[i + 1]) + IMG_MD.findall(parts[i + 1]))

for n, cpath in cards:
    ct = io.open(os.path.join(ROOT, cpath), encoding='utf-8-sig').read()
    src = IMG.findall(ct) + IMG_MD.findall(ct)
    vs = {ckey(x) for x in vol.get(n, [])}
    lines = ct.split('\n')
    shown = set()
    for x in src:
        k = ckey(x)
        if k in vs or k in shown:
            continue
        shown.add(k)
        q = find(x)
        sz = ''
        if q:
            try:
                sz = '%dx%d' % Image.open(q).size
            except Exception:
                pass
        # 找上下文（引用后 2 行）
        ctx = ''
        for i, l in enumerate(lines):
            if os.path.basename(x) in l:
                ctx = ' / '.join(s.strip()[:26] for s in lines[i + 1:i + 3] if s.strip())
                break
        print('Q%-3d %s  %-9s %-26s %s' % (n, x[:22], sz, ctx, os.path.basename(cpath)[:30]))
