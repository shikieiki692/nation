# -*- coding: utf-8 -*-
"""列卷 XII 各卡答案区的裸写「N 分」上下文（只读），用于判定是否可安全规范为「（N 分）」。"""
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
d = json.load(io.open(os.path.join(R, ".workbuddy/tmp/opt_pipe/vol_plan_XII.json"), encoding="utf-8"))
cards = [c["path"] for _m, lst in d for c in lst]
BARE = re.compile(r"(?<![0-9（(])(\d+)\s*分(?![子])")
for i, rel in enumerate(cards, 1):
    t = io.open(os.path.join(R, rel), encoding="utf-8-sig").read()
    a = re.search(r"^## 参考答案\s*\n(.*?)(?=^## 知识点映射|\Z)", t, re.S | re.M)
    seg = a.group(1) if a else ""
    ms = list(BARE.finditer(seg))
    if not ms:
        continue
    print("=" * 92)
    print("卷内第%2d题 ← %s  （%d 处）" % (i, os.path.basename(rel)[:50], len(ms)))
    for m in ms:
        s = max(0, m.start() - 46)
        print("   …%s…" % seg[s:m.end() + 14].replace("\n", "⏎"))
