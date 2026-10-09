# -*- coding: utf-8 -*-
"""把 render_findings.csv 整理成正式清单（09-审计报告）。"""
import csv, io, os, re, collections

R = r"C:\Obsidion\妙妙屋"
src = os.path.join(R, ".workbuddy", "tmp", "opt_pipe", "render_findings.csv")
dst = os.path.join(R, "09-审计报告", "2026-10-09-交付件低清图与碎片图清单.csv")

rows = list(csv.DictReader(io.open(src, encoding="utf-8-sig")))


def split_vol(name):
    m = re.search(r"初赛模拟卷([XVIp]+)（非有机·([^·]+)", name)
    return (m.group(1), m.group(2)) if m else ("?", name)


agg = collections.Counter()
out = []
for r in rows:
    v, ed = split_vol(r["docx"])
    out.append([v, ed, r["页"], r["类型"], r["细节"]])
    agg[(v, r["类型"])] += 1

with open(dst, "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["卷", "版本", "页", "类型", "细节"])
    w.writerows(sorted(out, key=lambda x: (x[0], x[1], int(x[2]), x[3])))

print("清单 → %s（%d 条）" % (os.path.basename(dst), len(out)))
print("按卷/类型：")
for (v, t), n in sorted(agg.items()):
    print("  卷%-5s %-7s %d" % (v, t, n))
