#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""diag_a_noans.py —— A 类「无答案/占位」87 张：源文件分组 + 全库答案册配对。"""
import csv, os, re, sys, collections
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
rows = [r for r in csv.DictReader(open(os.path.join(R, "09-审计报告/2026-10-07-不可组卷题目清单.csv"), encoding="utf-8-sig"))
        if r["reason"] == "无答案/占位"]
print("A 类「无答案/占位」 %d 张\n" % len(rows))

ANSKW = ("答案", "参考", "讲评", "解析", "详解", "题解", "评分")


def fm(p):
    d = {}
    try:
        t = open(p, encoding="utf-8-sig", errors="replace").read()
    except Exception:
        return d
    if t.startswith("---"):
        for l in t.split("---", 2)[1].split("\n"):
            m = re.match(r'^([a-z_]+):\s*"?(.*?)"?\s*$', l)
            if m:
                d[m.group(1)] = m.group(2)
    return d


# ── 建全库索引（md + pdf 的 stem → 路径）
POOLS = [
    os.path.join(R, "04-题库/2026机构初赛模拟题"),
    os.path.join(R, "06-外部资料导入"),
    os.path.join(R, ".workbuddy/tmp/backup_2026timu_md"),
]
idx = {}
for pool in POOLS:
    if not os.path.isdir(pool):
        continue
    for root, ds, fs in os.walk(pool):
        for f in fs:
            if f.lower().endswith((".md", ".pdf")):
                idx.setdefault(f, []).append(os.path.join(root, f))
print("索引文件 %d 个（含 %d 个 md/pdf 名）\n" % (sum(len(v) for v in idx.values()), len(idx)))

grp = collections.defaultdict(list)
unknown = []
for r in rows:
    p = os.path.join(R, r["path"])
    d = fm(p)
    sf = (d.get("source_file") or "").strip()
    sn = (d.get("source_norm") or "").strip()
    key = os.path.basename(sf) if sf else "(无 source_file)"
    grp[(r["inst"], key)].append((os.path.basename(r["path"]), sf, sn))

print("=== 按（机构 × 源文件）分组 ===")
for (inst, key), v in sorted(grp.items(), key=lambda x: (-len(x[1]), x[0])):
    print("%-10s %-46s %d 张" % (inst, key[:46], len(v)))

print("\n=== 逐源找「答案/讲评/解析」同源文件 ===")
for (inst, key), v in sorted(grp.items(), key=lambda x: (-len(x[1]), x[0])):
    stem = re.sub(r"\.(md|pdf)$", "", key)
    stem = re.sub(r"^\d+[-_]?", "", stem)          # 去序号前缀
    core = re.sub(r"(试题|试卷|习题|模拟|刷题|分享)", "", stem)[:12]
    hits = []
    for name, ps in idx.items():
        ns = re.sub(r"\.(md|pdf)$", "", name)
        if stem[:14] and stem[:14] in ns:
            if any(w in ns for w in ANSKW):
                hits.append((name, ps[0]))
        elif core and core in ns and any(w in ns for w in ANSKW) and name != key:
            hits.append((name, ps[0]))
    print("-" * 92)
    print("%-10s %s（%d 张）" % (inst, key[:60], len(v)))
    if hits:
        for n, p in hits[:4]:
            print("    ✅ 候选: %s" % n[:70])
            print("            %s" % p.replace(R + os.sep, "")[:100])
    else:
        print("    ❌ 全库无同源「答案/讲评/解析」文件")
