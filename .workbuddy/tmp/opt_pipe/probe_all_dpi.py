# -*- coding: utf-8 -*-
"""全量 dpi 汇总（权威版）：直接读 docx 内嵌 media 的像素，算每张图的有效 dpi。

不依赖外部 ORGBASE 反查 ⇒ 覆盖降采样改名图，且能发现「文档内的图」。
"""
import glob
import io
import os
import re
import zipfile

from PIL import Image

VAULT = r"C:\Obsidion\妙妙屋"
OUT = os.path.join(VAULT, "00-首页", "题组Word", "初赛模拟卷", "真题版式")

DRAW_RE = re.compile(r"<w:drawing>.*?</w:drawing>", re.S)
BLIP_RE = re.compile(r'<a:blip[^>]*r:embed="([^"]+)"')
EXT_RE = re.compile(r'<wp:extent cx="(\d+)" cy="(\d+)"')
RELS_RE = re.compile(r'<Relationship[^>]*Id="([^"]+)"[^>]*Target="([^"]+)"')
EMU_CM = 360000


def media_px(z):
    rels = z.read("word/_rels/document.xml.rels").decode("utf-8")
    rid2t = {m.group(1): m.group(2) for m in RELS_RE.finditer(rels)}
    cache = {}

    def get(rid):
        if rid in cache:
            return cache[rid]
        t = rid2t.get(rid, "")
        name = "word/" + t.replace("../", "") if not t.startswith("word/") else t
        name = name.replace("word/word/", "word/")
        try:
            with Image.open(io.BytesIO(z.read(name))) as im:
                cache[rid] = im.size
        except Exception:
            cache[rid] = None
        return cache[rid]

    return get


tot = 0
bad_all = []
for f in sorted(glob.glob(os.path.join(OUT, "*.docx"))):
    z = zipfile.ZipFile(f)
    x = z.read("word/document.xml").decode("utf-8")
    get = media_px(z)
    rows = []
    for d in DRAW_RE.findall(x):
        b = BLIP_RE.search(d)
        e = EXT_RE.search(d)
        if not b or not e:
            continue
        wh = get(b.group(1))
        if not wh:
            continue
        cx = int(e.group(1))
        rows.append((wh[0] / ((cx / EMU_CM) / 2.54), wh, cx / EMU_CM))
    if not rows:
        print("%-52s 图 0" % os.path.basename(f)[:52])
        continue
    rows.sort()
    bad = [r for r in rows if r[0] < 149.9]
    tot += len(rows)
    bad_all += [(os.path.basename(f), r) for r in bad]
    print("%-52s 图 %-3d 最低 %7.2f dpi  <150：%d%s"
          % (os.path.basename(f)[:52], len(rows), rows[0][0], len(bad),
             ("｜" + "、".join("%.1f@%dx%d/%.2fcm" % (r[0], r[1][0], r[1][1], r[2]) for r in bad[:3])) if bad else ""))
print("=" * 96)
print("图合计 %d 张 ｜ <150dpi %d 处" % (tot, len(bad_all)))
for fn, r in bad_all[:10]:
    print("   ", fn[:44], "%.1f dpi" % r[0], r[1])
