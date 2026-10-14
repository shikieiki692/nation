# -*- coding: utf-8 -*-
r"""把「源卡有、卷内无」的图拼成一张联系表（contact sheet），供一次目检定真伪。
用法：python montage_missing.py <卷> <输出.png>
"""
import io, os, re, sys, json, hashlib
from PIL import Image, ImageDraw

ROOT = r"C:\Obsidion\妙妙屋"
O = os.path.join(ROOT, '.workbuddy', 'tmp', 'opt_pipe')
V = sys.argv[1]
OUT = sys.argv[2]
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
    if not os.path.isfile(p):
        continue
    d = io.open(p, encoding='utf-8-sig').read()
    parts = re.split(r'(?m)^### 第 (\d+) 题', d)
    for i in range(1, len(parts), 2):
        vol.setdefault(int(parts[i]), [])
        vol[int(parts[i])].extend(IMG.findall(parts[i + 1]) + IMG_MD.findall(parts[i + 1]))

items = []
for n, cpath in cards:
    ct = io.open(os.path.join(ROOT, cpath), encoding='utf-8-sig').read()
    src = IMG.findall(ct) + IMG_MD.findall(ct)
    vs = {ckey(x) for x in vol.get(n, [])}
    seen = set()
    for x in src:
        k = ckey(x)
        if k in vs or k in seen:
            continue
        seen.add(k)
        q = find(x)
        if q:
            items.append((n, k, q))

print('待目检 %d 张' % len(items))
COLS, TH, PAD = 6, 210, 8
CELLW = 200
rows = (len(items) + COLS - 1) // COLS
sheet = Image.new('RGB', (COLS * (CELLW + PAD) + PAD, rows * (TH + 26 + PAD) + PAD), 'white')
dr = ImageDraw.Draw(sheet)
for i, (qno, k, path) in enumerate(items):
    r, c = divmod(i, COLS)
    x = PAD + c * (CELLW + PAD)
    y = PAD + r * (TH + 26 + PAD)
    try:
        im = Image.open(path).convert('RGB')
        im.thumbnail((CELLW, TH))
        sheet.paste(im, (x + (CELLW - im.width) // 2, y))
        dr.text((x, y + TH + 4), 'Q%d %s %dx%d' % (qno, k[:8], im.width, im.height), fill='black')
    except Exception as e:
        dr.text((x, y), 'ERR %s' % k[:8], fill='red')
sheet.save(OUT)
print('已保存', OUT, sheet.size)
