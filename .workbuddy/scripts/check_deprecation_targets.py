#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
校验 superseded_by / deprecation_reason 的目标可解析性

SOP 第 333 行规定：status: deprecated 必须写 superseded_by，且指向
「真实存在的、pack=模块习题集 的取代文件」。

本脚本对「现有的 4 条 + 计划新增的 3 条」目标做三级兜底解析
（路径 → basename → title/aliases），与 validate_kb 的 find_wikilink_target 一致，
并额外报告目标的 pack 值，用于判断是否符合 SOP。
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
QB_TYPES = {"题目", "真题"}
EXCLUDE = {"README.md", "题库架构总览.md", "新题入库SOP.md",
           "题库格式速查.md", "题库审计清单.md"}

# (来源文件, 目标 wikilink, 现状/计划)
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


def read_frontmatter(path: Path):
    try:
        lines = open(path, "r", encoding="utf-8", newline="").read().split("\n")
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


def build_index():
    """三级兜底索引：路径 -> basename -> title/aliases"""
    by_path, by_name, by_title = {}, {}, {}
    for tree in ("04-题库", "05-真题库"):
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
            rel = p.relative_to(ROOT).as_posix()
            by_path[rel] = (rel, fm)
            stem = p.stem
            by_name.setdefault(stem, []).append((rel, fm))
            t = fm.get("title", "").strip().strip('"')
            if t:
                by_title.setdefault(t, []).append((rel, fm))
            al = fm.get("aliases", "").strip()
            for a in al.strip("[]").split(","):
                a = a.strip().strip('"').strip("'")
                if a:
                    by_title.setdefault(a, []).append((rel, fm))
    return by_path, by_name, by_title


def resolve(target, by_path, by_name, by_title):
    if target in by_path:
        return by_path[target], "路径"
    if target in by_name:
        cands = by_name[target]
        return (cands[0], f"basename(命中{len(cands)})")
    if target in by_title:
        cands = by_title[target]
        return (cands[0], f"title/alias(命中{len(cands)})")
    return None, "未命中"


def main():
    by_path, by_name, by_title = build_index()
    print(f"索引题目文件: {len(by_path)}\n")
    print(f"{'状态':<6}{'目标':<32}{'解析方式':<20}{'pack':<14}源")
    print("-" * 108)
    bad = 0
    for src, tgt, kind in TARGETS:
        hit, how = resolve(tgt, by_path, by_name, by_title)
        if hit is None:
            print(f"{kind:<6}{tgt:<32}{'✗ 未命中':<20}{'-':<14}{Path(src).name}")
            bad += 1
            continue
        rel, fm = hit
        pack = fm.get("pack", "").strip() or "(缺)"
        flag = "" if pack == "模块习题集" else "  ← 非模块习题集"
        same_dir = Path(rel).parent == Path(src).parent
        print(f"{kind:<6}{tgt:<32}{how:<20}{pack:<14}{Path(src).name}"
              f"{'  [同目录]' if same_dir else ''}{flag}")
    print(f"\n未命中 {bad} 条" + ("（全部可解析）" if bad == 0 else "（会产生断链！）"))
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
