#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
离线模拟 02-数据库/题库.base 各视图的命中行数

不打开 Obsidian，直接用同一套过滤条件在文件上跑一遍，验证：
  1. 顶层 filter 是否如预期覆盖 04-题库 + 05-真题库
  2. 每个视图各命中多少行（改视图前/后对比）
  3. 有没有视图命中 0 行（说明过滤条件写错了或数据已清空）

用法：
    python sim_base_views.py
    python sim_base_views.py --show 部分填充待补全   # 打印该视图的具体行
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXCLUDE = {"README.md", "题库架构总览.md", "新题入库SOP.md",
           "题库格式速查.md", "题库审计清单.md"}
QB_TYPES = {"题目", "真题"}


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


def val(fm, key):
    """取标量值（去引号），空/缺失返回 ''"""
    v = fm.get(key, "").strip().strip('"').strip("'")
    return v


def is_empty(fm, key):
    """isEmpty()：缺失、空串、空数组 [ ] 都算空"""
    if key not in fm:
        return True
    v = val(fm, key)
    if v in ("", "[]", "['']", '[""]'):
        return True
    return False


def load_corpus(trees=("04-题库", "05-真题库")):
    """顶层 filter：inFolder(04-题库) OR inFolder(05-真题库) AND type in {题目, 真题}"""
    rows = []
    for tree in trees:
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


def in_folder(row, folder):
    return row["_path"].startswith(folder + "/")


VIEWS = [
    ("全部题目", lambda r: True),
    # 与 build_module_book.py 的排除条件对齐：pack=模块习题集 且 status != deprecated
    ("精选池（可成书）",
     lambda r: val(r, "pack") == "模块习题集" and val(r, "status") != "deprecated"),
    ("未用过的题", lambda r: is_empty(r, "used_in")),
    ("待治理（废弃待决）", lambda r: val(r, "status") in ("已入库", "deprecated")),
    ("部分填充待补全", lambda r: val(r, "status") == "待填充"),
    ("题型待标注（按目录批量补）", lambda r: is_empty(r, "question_type")),
    ("题型待标注·真题优先",
     lambda r: is_empty(r, "question_type") and in_folder(r, "04-题库/真题")),
    ("层次待定", lambda r: is_empty(r, "teaching_level")),
]


def main():
    rows = load_corpus()
    rows04 = load_corpus(("04-题库",))
    print(f"顶层 filter 命中（04-题库 + 05-真题库，type in {QB_TYPES}）: {len(rows)}")
    print(f"仅 04-题库: {len(rows04)}   增量来自 05-真题库: {len(rows) - len(rows04)}\n")

    show = None
    if "--show" in sys.argv:
        show = sys.argv[sys.argv.index("--show") + 1]

    print(f"{'视图':<28}{'含05':>8}{'仅04':>8}{'增量':>8}   备注")
    print("-" * 66)
    matched = {}
    for name, pred in VIEWS:
        hit = [r for r in rows if pred(r)]
        hit04 = [r for r in rows04 if pred(r)]
        matched[name] = hit
        note = "!! 0 行" if not hit else ""
        print(f"{name:<28}{len(hit):>8}{len(hit04):>8}{len(hit)-len(hit04):>8}   {note}")

    if show and show in matched:
        print(f"\n=== {show} 明细 ===")
        for r in sorted(matched[show], key=lambda x: x["_path"]):
            print(f"  {r['_path']}")
    elif show:
        print(f"\n未知视图: {show}")

    # 交叉校验：不应有重叠
    a = {r["_path"] for r in matched["待治理（废弃待决）"]}
    b = {r["_path"] for r in matched["部分填充待补全"]}
    print(f"\n待治理 ∩ 部分填充 = {len(a & b)}（应为 0，两视图按动作类型互斥）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
