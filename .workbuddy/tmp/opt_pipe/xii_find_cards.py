# -*- coding: utf-8 -*-
"""按前缀在磁盘上找回卷 XII 原始 10 张卡的完整路径（不依赖池与计划锁）。"""
import glob
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
BASE = os.path.join(R, "04-题库", "2026机构初赛模拟题")
PRE = ["题-CM-145-03-", "题-QBY-04-02-21有一种", "题-HZ-08-03-过渡金属硼化物", "题-GChO-03-02-",
       "题-XeC-15-03-随着核电的发展", "题-GChO-12-03-", "题-CM-103-04-",
       "题-QBY-06-03-某新型多孔框架", "题-HYS-10-04-已知在29815K下将具有完", "题-FY-10-04-"]
out = []
for k in PRE:
    hits = glob.glob(os.path.join(BASE, "**", k + "*.md"), recursive=True)
    if len(hits) != 1:
        print("  ⚠ 前缀 %r 命中 %d 个: %s" % (k, len(hits), [os.path.basename(h) for h in hits]))
        continue
    rel = os.path.relpath(hits[0], R).replace(os.sep, "/")
    out.append(rel)
    print("  %s" % rel)
with open(os.path.join(R, ".workbuddy/tmp/opt_pipe/xii_cards_orig.txt"), "w",
          encoding="utf-8", newline="\n") as f:
    f.write("\n".join(out) + "\n")
print("共 %d 张 → xii_cards_orig.txt" % len(out))
