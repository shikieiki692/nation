# -*- coding: utf-8 -*-
import os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
root = "04-课件/习题集/习题书-教师版"
tot = 0
n = 0
per = {}
detail = []
for dp, dn, fn in os.walk(root):
    for f in fn:
        if not f.endswith(".md") or f in ("目录.md", "来源索引.md"):
            continue
        p = os.path.join(dp, f)
        t = open(p, encoding="utf-8", errors="replace").read()
        m = re.search(r"^question_count:\s*(\d+)", t, re.M)
        if not m:
            detail.append((p, None))
            continue
        v = int(m.group(1))
        tot += v
        n += 1
        mod = p.replace("\\", "/").split("/")[-2]
        per[mod] = per.get(mod, 0) + v
        detail.append((p, v))
print("章数 %d ；题数合计 %d" % (n, tot))
for k, v in per.items():
    print("  %-12s %d" % (k, v))
miss = [p for p, v in detail if v is None]
if miss:
    print("无 question_count 的文件:", miss)
