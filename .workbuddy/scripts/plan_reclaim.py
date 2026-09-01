#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
综合回收方案测算（只读）

把「孤儿删除」与「内容去重」合并计算，避免重复统计，并按风险分级：
  P0 孤儿且不在重复组        -> 直接删，零风险
  P1 孤儿且是重复组冗余副本   -> 直接删（另有一份被引用），零风险
  P2 重复组内 >=2 份被引用     -> 需先重定向引用才能删，有风险
输出 .workbuddy/tmp/reclaim_plan.json
"""
import os, json, collections

VAULT = r"C:\Obsidion\妙妙屋"
U = json.load(open(os.path.join(VAULT, ".workbuddy", "tmp", "image_usage.json"),
                   encoding="utf-8"))
C = json.load(open(os.path.join(VAULT, ".workbuddy", "tmp", "orphan_classified.json"),
                   encoding="utf-8"))


def hsize(n):
    if n >= 1 << 30:
        return "%.2f GB" % (n / (1 << 30))
    if n >= 1 << 20:
        return "%.2f MB" % (n / (1 << 20))
    return "%.1f KB" % (n / 1024)


orphan_set = {}
for lvl in "SABC":
    for x in C.get(lvl, []):
        orphan_set[x["path"].replace("\\", "/")] = lvl

dup = U.get("dup_groups", {})

p0 = []   # 孤儿，不在任何重复组
p1 = []   # 孤儿，在重复组且组内有被引用的副本
p2 = []   # 组内 >=2 份被引用（需重定向）
p1_multi_orphan = []   # 组内全是孤儿（保留1删其余）

in_dup = {}
for h, members in dup.items():
    for rel, size in members:
        in_dup[rel.replace("\\", "/")] = h

for path in orphan_set:
    h = in_dup.get(path)
    if h is None:
        p0.append(path)
    else:
        p1_multi_orphan.append((path, h))

# 按组统计：组内被引用副本数
grp_stat = {}
for h, members in dup.items():
    used = [m for m in members if m[0].replace("\\", "/") not in orphan_set]
    orph = [m for m in members if m[0].replace("\\", "/") in orphan_set]
    grp_stat[h] = {"used": used, "orph": orph}

safe_dup = 0
safe_bytes = 0
for h, members in dup.items():
    g = grp_stat[h]
    if len(g["used"]) >= 1:
        # 组内至少一份被引用 -> 孤儿副本可安全删
        safe_dup += len(g["orph"])
        safe_bytes += sum(s for _, s in g["orph"])
    elif len(g["used"]) == 0 and len(g["orph"]) > 1:
        # 全是孤儿 -> 保留 1 删其余
        keep = max(g["orph"], key=lambda m: m[1])
        rest = [m for m in g["orph"] if m is not keep]
        safe_dup += len(rest)
        safe_bytes += sum(s for _, s in rest)

risk_groups = [h for h, g in grp_stat.items() if len(g["used"]) >= 2]
risk_bytes = 0
risk_extra = 0
for h in risk_groups:
    g = grp_stat[h]
    risk_extra += len(g["used"]) - 1
    keep = max(g["used"], key=lambda m: m[1])
    risk_bytes += sum(s for mm, s in g["used"] if mm != keep[0])

print("=== 重复组构成 ===")
n_used1 = sum(1 for g in grp_stat.values() if len(g["used"]) == 1)
n_used0 = sum(1 for g in grp_stat.values() if len(g["used"]) == 0)
n_used2 = len(risk_groups)
print("  组内恰好 1 份被引用 : %5d 组" % n_used1)
print("  组内全部是孤儿      : %5d 组" % n_used0)
print("  组内 >=2 份被引用   : %5d 组  <-- 需重定向，有风险" % n_used2)
print()
print("=== 回收测算（不重不漏） ===")
print("  P0 孤儿(非重复组)      : %6d 张" % len(p0))
print("  P1 重复组的孤儿副本    : %6d 张 / %s   <- 安全" % (safe_dup, hsize(safe_bytes)))

orph_bytes_all = sum(x["size"] for x in U["orphan"])
print()
print("  孤儿总量              : %6d 张 / %s" % (len(U["orphan"]), hsize(orph_bytes_all)))
print("    (P0+P1 合计 = 孤儿总量，两者互补)")
print()
print("  P2 需重定向的重复     : %6d 组 / 可再省 %s" % (n_used2, hsize(risk_bytes)))
print()
print("=== 建议执行顺序 ===")
print("  阶段1 删 S 级产物      : %s（可重建，零风险）"
      % hsize(sum(x["size"] for x in C.get("S", []))))
print("  阶段2 删 A 级未启用素材: %s"
      % hsize(sum(x["size"] for x in C.get("A", []))))
print("  阶段3 删 B/C 级孤儿    : %s（需确认）"
      % hsize(sum(x["size"] for x in C.get("B", []) + C.get("C", []))))
print("  阶段4 内容去重重定向   : %s（需脚本改引用）" % hsize(risk_bytes))
print()
print("  阶段1+2 立即可回收     : %s"
      % hsize(sum(x["size"] for x in C.get("S", []) + C.get("A", []))))

json.dump({
    "p0_orphan_only": p0,
    "safe_dup_count": safe_dup,
    "safe_dup_bytes": safe_bytes,
    "risk_groups": risk_groups,
    "risk_extra": risk_extra,
    "risk_bytes": risk_bytes,
    "levels": {k: len(v) for k, v in C.items()},
    "level_bytes": {k: sum(x["size"] for x in v) for k, v in C.items()},
}, open(os.path.join(VAULT, ".workbuddy", "tmp", "reclaim_plan.json"), "w",
        encoding="utf-8"), ensure_ascii=False, indent=1)
print()
print("方案 -> .workbuddy/tmp/reclaim_plan.json")
