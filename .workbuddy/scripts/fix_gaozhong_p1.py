# -*- coding: utf-8 -*-
"""
03-知识点/高中化学基础 · P1 竞赛 KP 断链修复

原 4 个断链目标在库内不存在，按"最贴切现有条目"重定向；
硫化学无任何相近条目（硼的硫族化合物讲的是 B-S 缺电子化合物，主题不符），
去链接并标注待建，不擅自造内容。

用法：
  python fix_gaozhong_p1.py            # 预演
  python fix_gaozhong_p1.py --apply    # 落盘
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

VAULT = r"C:\Obsidion\妙妙屋"
TARGET = os.path.join(VAULT, "03-知识点", "高中化学基础")
KP = os.path.join(VAULT, "03-知识点")

APPLY = "--apply" in sys.argv

# 目标文件必须真实存在
REQUIRED = {
    "化学原理/元素周期律.md",
    "化学原理/电离能.md",
    "化学原理/化学热力学.md",
    "化学原理/离子方程式.md",
}
for r in REQUIRED:
    p = os.path.join(KP, r)
    assert os.path.isfile(p), f"目标文件不存在: {r}"

# ---- 逐文件规则（顺序敏感：README 按所在行上下文区分）----
RULES = {
    "README.md": [
        # (匹配行特征, 旧链接, 新链接)
        ("元素周期律基础", "[[元素周期表]]", "[[元素周期律]]"),
        ("电离能与电负性", "[[元素周期表]]", "[[电离能]]"),
        ("化学反应与能量基础", "[[热化学]]", "[[化学热力学]]"),
        ("反应热与盖斯定律", "[[热化学]]", "[[化学热力学]]"),
        ("物质分类与离子反应", "[[离子反应]]", "[[离子方程式]]"),
        ("硫及其化合物", "[[硫化学]]", "硫化学（待建）"),
    ],
    "元素周期律基础.md": [
        (None, "[[元素周期表]]", "[[元素周期律]]"),
    ],
    "电离能与电负性.md": [
        (None, "[[元素周期表]]", "[[电离能]]"),
    ],
    "物质分类与离子反应.md": [
        (None, "[[离子反应]]", "[[离子方程式]]"),
    ],
}

changed = {}
for fn, rules in RULES.items():
    fp = os.path.join(TARGET, fn)
    if not os.path.isfile(fp):
        print(f"!! 文件不存在: {fn}")
        continue
    lines = open(fp, encoding="utf-8").read().split("\n")
    hits = []
    for i, line in enumerate(lines):
        for ctx, old, new in rules:
            if old not in line:
                continue
            if ctx is not None and ctx not in line:
                continue
            lines[i] = line.replace(old, new)
            hits.append((i + 1, old, new))
            break
    if hits:
        changed[fn] = hits
        if APPLY:
            with open(fp, "w", encoding="utf-8", newline="") as fh:
                fh.write("\n".join(lines))

print("=" * 70)
print("P1 竞赛 KP 修复" + ("（已应用）" if APPLY else "（预演，未落盘）"))
print("=" * 70)
total = 0
for fn, hits in changed.items():
    print(f"\n{fn}")
    for ln, old, new in hits:
        total += 1
        print(f"  L{ln}: {old}  ->  {new}")
print(f"\n合计 {total} 处，涉及 {len(changed)} 个文件")
