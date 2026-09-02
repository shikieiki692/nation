# -*- coding: utf-8 -*-
"""验证 02-数据库/{习题集,习题书,测试题}.base 三视图口径（只读）。

做四件事：
1. PyYAML 解析三个 .base（语法必须合法，Obsidian 才能渲染）
2. 断言顶层 filter 含预期的 teaching_level 条件
3. 用同一套谓词跑语料，断言池大小：习题集 1,769 / 习题书 1,525 / 测试题 888，
   两两交集 0，合计 4,182（teaching_level 覆盖 100%，是干净划分）
4. 输出各池的 status / used_in / subject_module 分布，供组卷参考

用法：python sim_module_pools.py
"""
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
DB = ROOT / "02-数据库"
QB_TYPES = {"题目", "真题"}

POOLS = {
    "习题集": {"基础", "巩固"},
    "习题书": {"拓展"},
    "测试题": {"竞赛"},
}
EXPECTED = {"习题集": 1769, "习题书": 1525, "测试题": 888}


def read_frontmatter(path: Path):
    with open(path, "r", encoding="utf-8", newline="") as f:
        lines = f.read().split("\n")
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


def load_corpus():
    rows = []
    for tree in ("04-题库", "05-真题库"):
        base = ROOT / tree
        for p in base.rglob("*.md"):
            fm = read_frontmatter(p)
            if fm is None or fm.get("type", "").strip() not in QB_TYPES:
                continue
            fm["_path"] = p.relative_to(ROOT).as_posix()
            rows.append(fm)
    return rows


def scalar(v):
    return (v or "").strip().strip('"').strip("'")


def is_empty(fm, key):
    if key not in fm:
        return True
    v = scalar(fm.get(key))
    return v in ("", "[]", "['']", '[""]')


def check_base_files():
    ok = True
    for name in POOLS:
        p = DB / f"{name}.base"
        if not p.exists():
            print(f"[FAIL] 缺文件: {p}")
            ok = False
            continue
        text = p.read_text(encoding="utf-8")
        try:
            data = yaml.safe_load(text)
        except Exception as e:
            print(f"[FAIL] {p.name} YAML 解析失败: {e}")
            ok = False
            continue
        if not isinstance(data, dict) or "filters" not in data or "views" not in data:
            print(f"[FAIL] {p.name} 缺 filters/views 顶层键")
            ok = False
            continue
        for lv in sorted(POOLS[name]):
            cond = f'teaching_level == "{lv}"'
            if cond not in text:
                print(f'[FAIL] {p.name} 顶层 filter 缺 {cond}')
                ok = False
        names = [v.get("name") for v in data.get("views", [])]
        print(f"[OK] {p.name} 语法合法，视图: {names}")
    return ok


def main():
    sys.exit_code = 0
    if not check_base_files():
        sys.exit_code = 1
    print()

    rows = load_corpus()
    print(f"语料（04-题库+05-真题库，type in {sorted(QB_TYPES)}）: {len(rows)} 行")

    pool_rows = {}
    for name, levels in POOLS.items():
        pool_rows[name] = [r for r in rows if scalar(r.get("teaching_level")) in levels]

    # 池大小与划分
    for name in POOLS:
        n = len(pool_rows[name])
        mark = "OK" if n == EXPECTED[name] else "FAIL"
        if n != EXPECTED[name]:
            sys.exit_code = 1
        print(f"[{mark}] {name}: {n}（预期 {EXPECTED[name]}）")
    ids = [set(r["_path"] for r in pool_rows[name]) for name in POOLS]
    total = len(set().union(*ids))
    inter_ab = len(ids[0] & ids[1]) + len(ids[0] & ids[2]) + len(ids[1] & ids[2])
    if inter_ab or total != len(rows):
        sys.exit_code = 1
    print(f"[{'OK' if not inter_ab else 'FAIL'}] 三池两两交集 = {inter_ab}（应 0）")
    print(f"[{'OK' if total == len(rows) else 'FAIL'}] 三池并集 = {total} / 语料 {len(rows)}"
          f"（teaching_level 覆盖应为 100%）")

    # 各池分布
    for name in POOLS:
        rs = pool_rows[name]
        status = {}
        used = 0
        modules = {}
        for r in rs:
            status[scalar(r.get("status")) or "(缺失)"] = status.get(scalar(r.get("status")) or "(缺失)", 0) + 1
            if not is_empty(r, "used_in"):
                used += 1
            m = scalar(r.get("subject_module")) or "(缺失)"
            modules[m] = modules.get(m, 0) + 1
        mod_str = " / ".join(f"{k} {v}" for k, v in sorted(modules.items(), key=lambda x: -x[1]))
        st_str = " / ".join(f"{k} {v}" for k, v in sorted(status.items(), key=lambda x: -x[1]))
        print(f"\n--- {name}（{len(rs)}）---")
        print(f"  status: {st_str}")
        print(f"  已用 used_in 非空: {used}（未用 {len(rs) - used}）")
        print(f"  模块: {mod_str}")

    return sys.exit_code


if __name__ == "__main__":
    sys.exit(main())
