# -*- coding: utf-8 -*-
r"""卷内「低分辨率图」机会评估：px<500 的卷内图 × 配对状态（只读）。"""
import json, io, os, re
from PIL import Image
os.chdir(r'C:\Obsidion\妙妙屋')
IMGDIRS = [r for r, d, f in os.walk('04-题库') if os.path.basename(r) == 'images']

def find(name):
    b = os.path.basename(name)
    for d in IMGDIRS:
        p = os.path.join(d, b)
        if os.path.isfile(p):
            return p
    return None

la = {os.path.basename(x.get('lib', '')): x for x in json.load(io.open('.workbuddy/tmp/chemy_site/lib_analysis.json', encoding='utf-8'))}
mf = {}
for x in json.load(io.open('.workbuddy/tmp/chemy_site/img_match_final.json', encoding='utf-8')):
    mf.setdefault(os.path.basename(x.get('lib_img', '')), x)
cd = {os.path.basename(x.get('lib_img', '')): x for x in json.load(io.open('.workbuddy/tmp/chemy_site/img_candidates.json', encoding='utf-8'))}

rows = {}
for V in ['X', 'XI', 'XIp', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII']:
    for tag in ['学生版', '答案版']:
        md = '04-题库/初赛模拟卷%s（非有机·%s）.md' % (V, tag)
        if not os.path.isfile(md):
            continue
        t = io.open(md, encoding='utf-8-sig').read()
        for m in re.finditer(r'!\[\[([^\]]+)\]\]', t):
            b = os.path.basename(m.group(1))
            rows.setdefault(b, set()).add(V)

low = []
for b, vols in rows.items():
    fp = find(b)
    if not fp:
        continue
    try:
        w, h = Image.open(fp).size
    except Exception:
        continue
    if w < 500:
        low.append((w, h, b, sorted(vols)[:3], b in la, la.get(b, {}).get('mapped'), b in mf, b in cd))

low.sort()
print('卷内 px<500 的图：%d 张（去重）' % len(low))
print('%-5s %-5s %-3s %-3s %-3s %-3s  %s' % ('w', 'h', '分析', '映射', '配对', '候选', '卷'))
n_map = sum(1 for r in low if r[5])
n_mf = sum(1 for r in low if r[6])
n_cd = sum(1 for r in low if r[7])
for w, h, b, vols, a, mp, m, c in low[:40]:
    print('%-5d %-5d %-3s %-3s %-3s %-3s  %s' % (w, h, 'Y' if a else '.', 'Y' if mp else '.', 'Y' if m else '.', 'Y' if c else '.', ','.join(vols)))
print()
print('其中：在分析表 %d ｜ mapped %d ｜ 有站点配对 %d ｜ 过候选护栏 %d' %
      (sum(1 for r in low if r[4]), n_map, n_mf, n_cd))
