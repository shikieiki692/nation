# -*- coding: utf-8 -*-
"""检查卷 XII 原计划 10 卡是否仍在池中（定位 plan-lock 失效原因）。"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, r"C:\Obsidion\妙妙屋\.workbuddy\tmp\opt_pipe")
sys.path.insert(0, r"C:\Obsidion\妙妙屋\.workbuddy\tmp")
import build_org as BO  # noqa: E402

BO.ALL_YEARS = True
pool = BO.build_pool()
paths = {}
for _m in pool:
    for _c in pool[_m]:
        paths[_c["path"].replace("\\", "/")] = _m

KEYS = ["题-CM-145-03-", "题-QBY-04-02-21有一种", "题-HZ-08-03-", "题-GChO-03-02-", "题-XeC-15-03-",
        "题-GChO-12-03-", "题-CM-103-04-", "题-QBY-06-03-", "题-HYS-10-04-已知在29815K下将具有完",
        "题-FY-10-04-"]
base = "04-题库/2026机构初赛模拟题"
for k in KEYS:
    hit, mod = None, None
    for p, m in paths.items():
        if k in p:
            hit, mod = p, m
            break
    if hit:
        print("  ✓ 在池   %-6s %s" % (mod, os.path.basename(hit)[:50]))
    else:
        # 全库找该卡文件，确认文件存在但被剔除
        import glob
        cand = glob.glob(os.path.join(BO.R if hasattr(BO, "R") else r"C:\Obsidion\妙妙屋", base, "*", k + "*.md"))
        print("  ✗ 掉池   %s   （磁盘上%s）" % (k, "存在" if cand else "不存在"))
        if cand:
            print("            %s" % cand[0][-70:])
print("\n池规模:", {m: len(pool[m]) for m in pool}, "合计", sum(len(pool[m]) for m in pool))
