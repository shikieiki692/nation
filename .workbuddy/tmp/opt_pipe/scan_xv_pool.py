# -*- coding: utf-8 -*-
"""scan_xv_pool.py —— 真实池里筛卷 XV 晶体候选（结构化学·未用·晶体主题）。"""
import os
import re
import sys
import glob
import json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import build_org as O          # noqa: E402

O.ALL_YEARS = True

used = set()
for f in glob.glob(os.path.join(HERE, "vol_plan_*.json")):
    try:
        d = json.load(open(f, encoding="utf-8"))
        for m, lst in d:
            for it in lst:
                used.add(os.path.basename(it["path"]))
    except Exception:
        pass

pool = O.build_pool()
KEY = re.compile(r"钙钛矿|晶胞|晶系|点阵|密堆积|密置层|晶体|配位多面体|堆积层|布拉维|空间群|晶格")

rows = []
for mod, lst in pool.items():
    if mod != "结构化学":
        continue
    for it in lst:
        b = os.path.basename(it["path"])
        if b in used:
            continue
        blob = (it["question"] or "") + (it["answer"] or "") + (it["title"] or "")
        if not KEY.search(blob):
            continue
        perov = blob.count("钙钛矿")
        rows.append((perov, b, it))

rows.sort(key=lambda r: (-r[0], r[1]))
print("结构化学池 %d 张；未用且含晶体主题 %d 张" % (
    len(pool["结构化学"]), len(rows)))
print("-" * 110)
for perov, b, it in rows:
    ttl = (it["title"] or "")[:22]
    src = it["source"][:34]
    print("%s P%d 图%2d  %-46s %-22s %s" % (
        "★" if perov else " ", perov, len(it["imgs"]), b[:46], ttl, src))
