#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""audit_gcho_bounds.py —— 检查 GChO 裁图卡的题界是否错乱。
判据：markers 阅读流序列中，本卡题号 q 的下一个标记题号应为 q+1；
      若不为 q+1（或 q 无标记但被兜底），则题界可疑。
"""
import glob, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, r"C:\Obsidion\妙妙屋\.workbuddy\tmp\opt_pipe")
import gcho_crop as GC

rows = []
for rnd in range(0, 200):
    f = os.path.join(GC.LOC, "GChO%d.json" % rnd)
    if not os.path.exists(f):
        continue
    idx = json.load(open(f, encoding="utf-8"))
    mks = GC.markers(idx, 150)
    order = [q for q, _, _, _, _ in mks]
    pos = {q: i for i, q in enumerate(order)}
    cards = sorted(glob.glob(os.path.join(GC.GDIR, "题-GChO-%02d-*.md" % rnd)))
    for c in cards:
        q = GC.card_qno(c)
        if q is None:
            continue
        if q not in pos:
            rows.append((rnd, q, "无标记(兜底)", None, os.path.basename(c)))
            continue
        nxt = order[pos[q] + 1] if pos[q] + 1 < len(order) else None
        if nxt != q + 1:
            rows.append((rnd, q, "下一标记=%s" % nxt, pos[q], os.path.basename(c)))

print("题界可疑卡：%d 张" % len(rows))
import collections
byr = collections.Counter(r[0] for r in rows)
print("按届:", dict(sorted(byr.items())))
print()
for rnd, q, why, pi, name in sorted(rows):
    print("  届%-3d 第%-3d题 %-14s %s" % (rnd, q, why, name[:46]))
