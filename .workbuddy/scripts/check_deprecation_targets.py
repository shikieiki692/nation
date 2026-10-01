#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""校验题库 deprecated 收口：目标可解析、明确无替代，或显式待人工对账。

默认扫描 04-题库 与 05-真题库中的全部 status: deprecated 文件。
替代目标按 路径 -> basename -> title/aliases 三级解析；derived_from 只表示来源，
不得当作 superseded_by。replacement_status=待人工对账 只表示已从自动消费中剔除，
不代表已经找到替代目标。--targets-only 仅复核历史 7 条专项对账记录。
"""
from pathlib import Path
import argparse
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
QB_TYPES = {"题目", "真题"}
QB_ROOTS = (ROOT / "04-题库", ROOT / "05-真题库")
EXCLUDE = {"README.md", "题库架构总览.md", "新题入库SOP.md",
           "题库格式速查.md", "题库审计清单.md"}

# 历史专项对账：(旧来源路径, 目标 wikilink, 现状/计划)。默认扫描不依赖此表。
TARGETS = [
    ("04-题库/教材习题/上海中学竞赛课程/题-049-上海中学-离子键与离子晶体-习题2.md",
     "题-赵鑫光-晶体-习6", "现有"),
    ("04-题库/教材习题/无机化学第5版/题-008-碱金属推断.md",
     "例12.6-物质推断题", "现有"),
    ("04-题库/教材习题/无机化学第5版/题-009-过氧化物方程式.md",
     "12.19-12.29-完成配平方程式", "现有"),
    ("04-题库/教材习题/无机化学第5版/题-011-对角线规则应用.md",
     "12.9-12.18-填空题", "现有"),
    ("04-题库/教材习题/无机化学例题与习题/Ch12-碱金属和碱土金属/习题/12.35-12.45-简答题.md",
     "12.35-BeCl2熔盐导电", "新增"),
    ("04-题库/教材习题/无机化学例题与习题/Ch19-铜副族和锌副族/习题/分离鉴别制备19.md",
     "19.57-生产制备过程", "新增"),
    ("04-题库/教材习题/无机化学例题与习题/Ch19-铜副族和锌副族/习题/简答题19.md",
     "19.64-解释实验现象", "新增"),
]


def clean(value):
    value = (value or "").strip().strip("\"'")
    return "" if value.lower() in {"", "null", "none", "~"} else value


def read_frontmatter(path):
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return None
    if not lines or lines[0].strip() != "---":
        return None
    fields = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return fields
        if line and not line[:1].isspace() and ":" in line:
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip()
    return None


def iter_question_files():
    for base in QB_ROOTS:
        if not base.exists():
            continue
        for path in sorted(base.rglob("*.md")):
            if path.name in EXCLUDE:
                continue
            fields = read_frontmatter(path)
            if fields is not None and clean(fields.get("type")) in QB_TYPES:
                yield path, fields


def alias_values(raw):
    raw = (raw or "").strip().strip("[]")
    values = []
    for item in re.split(r"\s*,\s*", raw):
        item = clean(item)
        if item:
            values.append(item)
    return values


def target_names(raw):
    raw = clean(raw)
    if not raw:
        return []
    names = []
    for item in re.split(r"\s*,\s*", raw.strip("[]")):
        item = clean(item)
        if item.startswith("[[") and item.endswith("]]" ):
            item = item[2:-2]
        item = item.split("|", 1)[0].strip()
        if item:
            names.append(item)
    return names


def build_index():
    by_path, by_name, by_title = {}, {}, {}
    all_files = []
    for path, fields in iter_question_files():
        rel = path.relative_to(ROOT).as_posix()
        record = (rel, fields)
        all_files.append(record)
        by_path[rel] = record
        by_path[rel[:-3] if rel.endswith(".md") else rel] = record
        by_name.setdefault(path.stem, []).append(record)
        title = clean(fields.get("title"))
        if title:
            by_title.setdefault(title, []).append(record)
        for alias in alias_values(fields.get("aliases")):
            by_title.setdefault(alias, []).append(record)
    return all_files, by_path, by_name, by_title


def resolve(raw, by_path, by_name, by_title):
    candidates = []
    for target in target_names(raw):
        normalized = target.replace("\\", "/")
        if normalized in by_path:
            candidates.append((by_path[normalized], "路径"))
            continue
        stem = Path(normalized).stem
        hits = by_name.get(stem, [])
        if len(hits) == 1:
            candidates.append((hits[0], "basename"))
            continue
        if len(hits) > 1:
            return None, f"basename 歧义({len(hits)})"
        hits = by_title.get(target, []) or by_title.get(stem, [])
        if len(hits) == 1:
            candidates.append((hits[0], "title/aliases"))
            continue
        if len(hits) > 1:
            return None, f"title/aliases 歧义({len(hits)})"
        return None, "未命中"
    if len(candidates) == 1:
        return candidates[0]
    return None, "空目标" if not candidates else f"多目标({len(candidates)})"


def check_deprecated(rel, fields, index):
    by_path, by_name, by_title = index
    reason = clean(fields.get("deprecation_reason"))
    raw_target = clean(fields.get("superseded_by"))
    replacement_status = clean(fields.get("replacement_status"))
    no_replacement = replacement_status == "无替代"
    pending = replacement_status == "待人工对账"
    derived_only = clean(fields.get("derived_from")) and not raw_target
    errors = []
    warnings = []
    if not reason:
        errors.append("缺少非空 deprecation_reason")
    if raw_target and (no_replacement or pending):
        errors.append(f"superseded_by 与 replacement_status={replacement_status} 冲突")
    if raw_target:
        hit, how = resolve(raw_target, by_path, by_name, by_title)
        if hit is None:
            errors.append(f"superseded_by 无法解析: {raw_target} ({how})")
            target_rel = pack = ""
        else:
            target_rel, target_fields = hit
            pack = clean(target_fields.get("pack")) or "(缺)"
            if pack != "模块习题集":
                warnings.append(f"替代目标 pack 非模块习题集: {pack}")
    elif no_replacement:
        how = "明确无替代"
        target_rel = pack = ""
    elif pending:
        how = "待人工对账"
        target_rel = pack = ""
        warnings.append("已显式列入待人工对账；不得作为自动组卷或发布输入")
    else:
        how = "未闭环"
        target_rel = pack = ""
        errors.append("deprecated 必须填写可解析的 superseded_by，或以 replacement_status=无替代/待人工对账 显式收口")
    if derived_only:
        warnings.append("derived_from 仅表示来源，不作为替代目标")
    return {
        "source": rel,
        "target": target_rel,
        "target_raw": raw_target,
        "resolution": how,
        "pack": pack,
        "errors": errors,
        "warnings": warnings,
    }


def check_historical(all_files, index):
    by_path, by_name, by_title = index
    by_basename = {}
    for rel, _ in all_files:
        by_basename.setdefault(Path(rel).name, []).append(rel)
    rows = []
    for old_src, raw_target, kind in TARGETS:
        source_hits = by_basename.get(Path(old_src).name, [])
        source = source_hits[0] if len(source_hits) == 1 else old_src
        errors = []
        warnings = []
        if len(source_hits) != 1:
            message = f"历史来源迁移后未唯一定位({len(source_hits)})"
            if kind == "新增":
                warnings.append(message + "；原分组来源已拆分，目标解析成功即可复核")
            else:
                errors.append(message)
        hit, how = resolve(raw_target, by_path, by_name, by_title)
        if hit is None:
            errors.append(f"目标无法解析: {raw_target} ({how})")
            target_rel = pack = ""
        else:
            target_rel, target_fields = hit
            pack = clean(target_fields.get("pack")) or "(缺)"
        rows.append({"kind": kind, "source": source, "target": target_rel,
                     "target_raw": raw_target, "resolution": how, "pack": pack,
                     "errors": errors, "warnings": warnings})
    return rows


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--targets-only", action="store_true", help="仅复核历史 7 条专项对账")
    parser.add_argument("--errors-only", action="store_true", help="只输出含 error 的记录")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    all_files, by_path, by_name, by_title = build_index()
    index = (by_path, by_name, by_title)
    if args.targets_only:
        rows = check_historical(all_files, index)
        scope = "历史专项"
    else:
        deprecated = [(rel, fields) for rel, fields in all_files
                      if clean(fields.get("status")) == "deprecated"]
        rows = [check_deprecated(rel, fields, index) for rel, fields in deprecated]
        scope = "全库 deprecated"
    if args.errors_only:
        rows = [row for row in rows if row["errors"]]

    bad = sum(bool(row["errors"]) for row in rows)
    pending = sum(row["resolution"] == "待人工对账" for row in rows)
    unresolved = sum(row["resolution"] not in {"路径", "basename", "title/aliases", "明确无替代"}
                     for row in rows)
    result = {"success": bad == 0, "scope": scope, "indexed": len(all_files),
              "checked": len(rows), "error_files": bad, "unresolved": unresolved,
              "pending": pending, "rows": rows}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"索引题目文件: {len(all_files)}；{scope}检查 {len(rows)} 条")
        for row in rows:
            status = "ERROR" if row["errors"] else "OK"
            target = row.get("target") or row.get("target_raw") or "-"
            pack = row.get("pack") or "-"
            print(f"{status:<5} {row['resolution']:<12} {pack:<14} {target}  <- {row['source']}")
            for message in row["errors"] + row["warnings"]:
                print(f"      {message}")
        print(f"\n错误 {bad} 条；未解析/未闭环 {unresolved} 条；其中待人工对账 {pending} 条")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
