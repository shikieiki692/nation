# -*- coding: utf-8 -*-
"""检查打印版图片有效 DPI：显示尺寸 vs 像素尺寸。>=300 优秀，150-300 可用，<150 打印偏虚"""
import sys, io, re, zipfile
from pathlib import Path
from collections import Counter
from PIL import Image

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
DST = Path(r"C:\Obsidion\妙妙屋\00-首页\题组Word\习题书\学生版-打印版")

buckets = Counter()
low = []


def scan(p: Path):
    z = zipfile.ZipFile(str(p))
    xml = z.read('word/document.xml').decode('utf-8', 'replace')
    rels = z.read('word/_rels/document.xml.rels').decode('utf-8', 'replace')
    rid2media = dict(re.findall(r'Id="([^"]+)"[^>]*Target="(media/[^"]+)"', rels))
    # 逐个 graphic 取 extent 与 blip r:embed
    for m in re.finditer(r'<wp:extent cx="(\d+)" cy="(\d+)"/>.*?<a:blip r:embed="(rId\d+)"', xml, re.S):
        cx, cy, rid = int(m.group(1)), int(m.group(2)), m.group(3)
        media = 'word/' + rid2media.get(rid, '')
        if media not in z.namelist():
            continue
        w_cm = cx / 360000
        try:
            img = Image.open(io.BytesIO(z.read(media)))
        except Exception:
            continue
        dpi = img.width / (w_cm / 2.54)
        if dpi >= 300:
            buckets['>=300 优秀'] += 1
        elif dpi >= 200:
            buckets['200-300 良好'] += 1
        elif dpi >= 150:
            buckets['150-200 可用'] += 1
        elif dpi >= 100:
            buckets['100-150 偏虚'] += 1
            low.append((str(p.relative_to(DST)), media.split('/')[-1], round(dpi), round(w_cm, 1)))
        else:
            buckets['<100 很虚'] += 1
            low.append((str(p.relative_to(DST)), media.split('/')[-1], round(dpi), round(w_cm, 1)))


for f in sorted(DST.rglob('*.docx')):
    try:
        scan(f)
    except Exception as e:
        print('ERR', f.name, e)

total = sum(buckets.values())
print(f"图片有效 DPI 分布（共 {total} 张）")
for k in ['>=300 优秀', '200-300 良好', '150-200 可用', '100-150 偏虚', '<100 很虚']:
    if buckets[k]:
        print(f"  {k:<14} {buckets[k]:>4}  ({buckets[k]/total*100:.1f}%)")
if low:
    print(f"\n低于 150 DPI 的图片 {len(low)} 张（打印会发虚，前 15 条）：")
    for r in low[:15]:
        print(f"  {r[0]:<38} {r[1]:<14} {r[2]:>4} dpi  宽 {r[3]}cm")
else:
    print("\n全部图片 >=150 DPI，打印清晰")
