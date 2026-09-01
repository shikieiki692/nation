# -*- coding: utf-8 -*-
"""
统计 frontmatter 断链（主要是 knowledge_points）涉及的唯一目标与频次。

目的：这类断链是「知识点笔记尚未创建」造成的真红链，无法自动改写，
只能通过新建笔记消除。本脚本给出投入产出表 —— 建哪些笔记收益最大。
"""
import os, re, sys, collections

VAULT = r"C:\Obsidion\妙妙屋"
sys.path.insert(0, os.path.join(VAULT, "11-模板", "scripts"))

import validate_kb as V

QB_LINK_FIELDS = V.QB_LINK_FIELDS
find = V.find_wikilink_target
is_ph = V.is_placeholder_target
VAULT_ROOT = V.VAULT_ROOT

SKIP = {".git", "node_modules", ".obsidian", "__pycache__", ".trash"}

cnt = collections.Counter()          # 目标 -> 出现处数
by_field = collections.Counter()     # 字段 -> 处数
where = collections.defaultdict(set)  # 目标 -> {来源文件}
total = 0

RE_YAML = re.compile(r"^---\n(.*?)\n---", re.S)

files = 0
for root, dirs, fs in os.walk(VAULT):
    dirs[:] = [d for d in dirs if d not in SKIP]
    for fn in fs:
        if not fn.lower().endswith(".md"):
            continue
        p = os.path.join(root, fn)
        rel = os.path.relpath(p, VAULT).replace("\\", "/")
        if V.is_excluded_path(rel) and not V.is_link_resolution_extra_path(rel):
            continue
        try:
            t = open(p, encoding="utf-8").read(20000)
        except Exception:
            continue
        m = RE_YAML.match(t)
        if not m:
            continue
        try:
            import yaml
            fm = yaml.safe_load(m.group(1))
        except Exception:
            continue
        if not isinstance(fm, dict):
            continue
        files += 1
        for field in QB_LINK_FIELDS:
            vals = fm.get(field)
            if isinstance(vals, str):
                vals = [vals]
            if not isinstance(vals, list):
                continue
            for v in vals:
                if not isinstance(v, str):
                    continue
                for tgt in re.findall(r"(?<!\!)\[\[([^\]|#]+)", v):
                    tgt = tgt.strip().rstrip("/\\").strip()
                    if not tgt or is_ph(tgt):
                        continue
                    if os.path.splitext(tgt)[1].lower() in {
                            ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}:
                        continue
                    if find(tgt, VAULT_ROOT) is None:
                        cnt[tgt] += 1
                        by_field[field] += 1
                        where[tgt].add(rel)
                        total += 1

print(f"扫描 md: {files}")
print(f"frontmatter 断链总处数: {total}")
print(f"唯一目标数: {len(cnt)}")
print(f"\n字段分布: {dict(by_field)}")

print(f"\n--- Top 40 高频红链（建这些笔记收益最大）---")
cum = 0
for i, (k, v) in enumerate(cnt.most_common(40), 1):
    cum += v
    print(f"  {i:3d}. {v:4d}  {k}")

# 投入产出：建 top N 个笔记能消掉多少
print("\n--- 投入产出估算 ---")
run = 0
for n in (10, 25, 50, 100, 200, 300, 500):
    run = sum(v for _, v in cnt.most_common(n))
    print(f"  新建 top {n:3d} 个笔记 → 消除 {run:4d} 处 ({run/total*100:.1f}%)")

# 频次分布
dist = collections.Counter(cnt.values())
print("\n--- 频次分布（出现 N 处的目标有多少个）---")
for n in sorted(dist)[:10]:
    print(f"  出现 {n:2d} 处: {dist[n]:4d} 个目标")
print(f"  仅出现 1 处的目标共 {dist[1]} 个（长尾）")

import json
json.dump({"total": total, "unique": len(cnt),
           "top": cnt.most_common(),
           "where": {k: sorted(v) for k, v in where.items()}},
          open(os.path.join(VAULT, r".workbuddy\tmp\fm_redlinks.json"), "w",
               encoding="utf-8"), ensure_ascii=False, indent=1)
