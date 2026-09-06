#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
僵尸字段盘点：低频 / 非模板 / 命名不一致 的 frontmatter 字段

三张表：
  A. 低频字段（出现 <= ZOMBIE_MAX 次）— 逐个决定：改名 / 删除 / 标 legacy
  B. 命名不一致组（camelCase vs snake_case 同义字段）
  C. 值与 status 语义冲突的（如 deprecated: true 但 status 不是 deprecated）

用法：
    python zombie_fields.py              # 三张表
    python zombie_fields.py --field X    # 列出所有含字段 X 的文件及值
"""
import sys
import re
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parents[2]
TREES = ("04-题库", "05-真题库")
QB_TYPES = {"题目", "真题"}
ZOMBIE_MAX = 20
EXCLUDE = {"README.md", "题库架构总览.md", "新题入库SOP.md",
           "题库格式速查.md", "题库审计清单.md"}

# SOP 模板里的正统字段（§2 模板）。用于区分「模板外的野字段」。
TEMPLATE_FIELDS = {
    "title", "type", "fidelity", "subject_module", "submodule", "module",
    "pack", "difficulty", "exam_stage", "teaching_level", "question_type",
    "syllabus_codes", "knowledge_points", "concepts", "tags", "source",
    "source_subject", "status", "used_in", "updated", "aliases", "year",
    "related", "prerequisite", "subject",
}

# 同义字段分组：key = 规范写法，value = 需要并进来的别名
SYNONYM_GROUPS = {
    "superseded_by": ["supersededBy", "superseded_by"],
    "deprecation_reason": ["deprecation_reason", "superseded_note",
                           "deprecationNote", "deprecation_reason_note"],
    "demoted": ["demoted", "demoted_from"],
    "promoted": ["promoted", "promoted_to"],
}


def read_frontmatter(path: Path):
    try:
        with open(path, "r", encoding="utf-8", newline="") as f:
            lines = f.read().split("\n")
    except Exception:
        return None
    if not lines or lines[0].strip() != "---":
        return None
    fields = {}
    for i in range(1, len(lines)):
        s = lines[i]
        if s.strip() == "---":
            return fields
        if s and not s[:1].isspace() and ":" in s:
            k, _, v = s.partition(":")
            fields[k.strip()] = v.strip()
    return None


def load():
    rows = []
    for tree in TREES:
        base = ROOT / tree
        if not base.exists():
            continue
        for p in base.rglob("*.md"):
            if p.name in EXCLUDE:
                continue
            fm = read_frontmatter(p)
            if fm is None:
                continue
            if fm.get("type", "").strip() not in QB_TYPES:
                continue
            fm["_path"] = p.relative_to(ROOT).as_posix()
            rows.append(fm)
    return rows


def main():
    rows = load()
    print(f"题目类文件: {len(rows)}\n")

    if "--field" in sys.argv:
        key = sys.argv[sys.argv.index("--field") + 1]
        hit = [(r["_path"], r[key]) for r in rows if key in r]
        print(f"=== 字段 [{key}] 共 {len(hit)} 条 ===")
        for p, v in sorted(hit):
            print(f"  {v}")
            print(f"      {p}")
        return 0

    keycnt = Counter()
    by_key = defaultdict(list)
    for r in rows:
        for k in r:
            if k.startswith("_"):
                continue
            keycnt[k] += 1
            by_key[k].append(r)

    # A. 低频字段
    print("=== A. 低频字段（出现 <= %d 次）===" % ZOMBIE_MAX)
    print(f"{'字段':<26}{'次数':>6}  {'模板内':<8} 样例值")
    print("-" * 96)
    for k, n in sorted(keycnt.items(), key=lambda x: x[1]):
        if n > ZOMBIE_MAX:
            continue
        in_tpl = "是" if k in TEMPLATE_FIELDS else "否←野"
        sample = ""
        for r in by_key[k]:
            v = r[k].strip()
            if v:
                sample = v[:44]
                break
        print(f"{k:<26}{n:>6}  {in_tpl:<8} {sample}")

    # B. 命名不一致
    print("\n=== B. 命名不一致组 ===")
    for canon, aliases in SYNONYM_GROUPS.items():
        present = [(a, keycnt.get(a, 0)) for a in aliases if keycnt.get(a, 0)]
        if len(present) > 1 or (len(present) == 1 and present[0][0] != canon):
            total = sum(n for _, n in present)
            detail = " + ".join(f"{a}({n})" for a, n in present)
            print(f"  -> {canon:<22} {detail}   合计 {total}")
        elif present:
            print(f"  ok {canon:<21} 仅 {present[0][0]}({present[0][1]})")

    # C. 语义冲突
    print("\n=== C. 与 status 语义冲突 ===")
    conflicts = 0
    for r in rows:
        st = r.get("status", "").strip()
        dep = r.get("deprecated", "").strip().lower()
        if dep in ("true", "yes") and st != "deprecated":
            print(f"  deprecated={dep} 但 status={st or '(缺失)'}  {r['_path']}")
            conflicts += 1
        if st == "deprecated" and dep not in ("true", "yes"):
            sup = r.get("superseded_by", "").strip()
            if not sup:
                print(f"  status=deprecated 但无 superseded_by   {r['_path']}")
                conflicts += 1
    if not conflicts:
        print("  无冲突")
    return 0


if __name__ == "__main__":
    sys.exit(main())
