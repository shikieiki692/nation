# -*- coding: utf-8 -*-
"""
连带修复：
  A) 00-首页/教材提炼状态盘点.md —— 4 处真坏链，按教师用书实际文件名修正
  B) 09-审计报告/高中化学基础-链接与图片体检-*.md —— 映射表里的"错误链接名"是示例，
     改成全角方括号，避免被 validate_kb 当真实断链统计

用法：
  python fix_remaining_teacher_links.py            # 预演
  python fix_remaining_teacher_links.py --apply    # 落盘
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

VAULT = r"C:\Obsidion\妙妙屋"
TEACHER = os.path.join(VAULT, "07-资料提炼", "教师用书")
APPLY = "--apply" in sys.argv

teacher_idx = {}
for root, dirs, files in os.walk(TEACHER):
    for f in files:
        if f.endswith(".md"):
            teacher_idx.setdefault(f[:-3], []).append(os.path.join(root, f))

TPL = re.compile(r"^\s*(必修\d|选修\d)\s+(Ch\d+)\s*-\s*(.+?)\s*教师用书提炼\s*$")


def build_fix(target: str):
    m = TPL.match(target)
    if not m:
        return None
    ch, name = m.group(2), m.group(3)
    for cand in (f"{ch}-{name.replace(' ', '')}", f"{ch}-{name.strip()}"):
        if cand in teacher_idx:
            return cand
    return None


JOBS = [
    # (文件, 模式)  A=真修复  B=示例转全角
    (os.path.join("00-首页", "教材提炼状态盘点.md"), "A"),
    (os.path.join("09-审计报告", "高中化学基础-链接与图片体检-2026-09-01.md"), "B"),
]

total = 0
for rel_path, mode in JOBS:
    fp = os.path.join(VAULT, rel_path)
    if not os.path.isfile(fp):
        print(f"!! 跳过（不存在）: {rel_path}")
        continue
    src = open(fp, encoding="utf-8").read()
    out = src
    hits = []

    def sub(mo):
        global total
        inner = mo.group(2)
        core = inner.strip()
        name = core.split("|")[0].split("#")[0].strip()
        fix = build_fix(name)
        if mode == "A" and fix:
            total += 1
            hits.append(("真修复", name, fix))
            return f"[[{fix}{core[len(name):]}]]"
        # 模式 B 只处理"错误链接名"示例（教师用书提炼模板），
        # 保留"应改为"列里的有效真链接
        if mode == "B" and name.endswith("教师用书提炼"):
            total += 1
            hits.append(("转全角", name, None))
            return f"［［{core}］］"
        return mo.group(0)

    out = re.sub(r"(!?)\[\[([^\]]+)\]\]", sub, out)

    print(f"\n{rel_path}  [{mode}]  改动 {len(hits)} 处")
    for kind, old, new in hits[:40]:
        print(f"   {kind}: {old[:52]}" + (f"  ->  {new}" if new else ""))
    if len(hits) > 40:
        print(f"   ... 其余 {len(hits)-40} 处")

    if APPLY and out != src:
        with open(fp, "w", encoding="utf-8", newline="") as fh:
            fh.write(out)

print(f"\n合计 {total} 处" + ("（已应用）" if APPLY else "（预演，未落盘）"))
