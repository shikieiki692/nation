# -*- coding: utf-8 -*-
"""
全库图片引用体检（只读，不改任何文件）

对每个 md 里的 Markdown 图片语法 ![alt](path) 做四种解析尝试：
  1. rel   —— 按当前文件所在目录相对解析（Obsidian 主路径）
  2. root  —— 按 vault 根兜底解析（Obsidian fallback）
  3. strip —— 剥掉前导 ../ 后挂 vault 根（本次高中化学基础的病灶）
  4. kp    —— 剥掉前导 ../ 后挂 03-知识点（P0' 病灶）

输出分类统计与明细，用于判断剩余病灶是否为同一根因。
"""
import os
import re
import sys
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8")

VAULT = r"C:\Obsidion\妙妙屋"
IMG = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
SKIP_DIRS = {".git", ".obsidian", "node_modules", ".workbuddy"}

stat = defaultdict(int)
by_dir = defaultdict(lambda: defaultdict(int))
details = defaultdict(list)

for root, dirs, files in os.walk(VAULT):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
    for fn in files:
        if not fn.endswith(".md"):
            continue
        fp = os.path.join(root, fn)
        rel_fp = os.path.relpath(fp, VAULT)
        top = rel_fp.split(os.sep)[0]
        try:
            text = open(fp, encoding="utf-8").read()
        except Exception:
            continue

        for m in IMG.finditer(text):
            path = m.group(2).strip()
            if path.startswith(("http://", "https://", "data:")):
                stat["外链跳过"] += 1
                continue
            p = path.replace("\\", "/").rstrip("/")
            stat["图片引用"] += 1

            if os.path.isfile(os.path.normpath(os.path.join(root, p))):
                stat["1.相对解析命中"] += 1
                by_dir[top]["ok_rel"] += 1
                continue

            stripped = p
            while stripped.startswith("../"):
                stripped = stripped[3:]

            if os.path.isfile(os.path.normpath(os.path.join(VAULT, p))):
                stat["2.根兜底命中"] += 1
                by_dir[top]["ok_root"] += 1
            elif os.path.isfile(os.path.normpath(os.path.join(VAULT, stripped))):
                stat["3.剥../后命中(可修)"] += 1
                by_dir[top]["fixable_strip"] += 1
                details["strip"].append((rel_fp, path[:100]))
            elif os.path.isfile(
                os.path.normpath(os.path.join(VAULT, "03-知识点", stripped))
            ):
                stat["4.挂03-知识点后命中(可修)"] += 1
                by_dir[top]["fixable_kp"] += 1
                details["kp"].append((rel_fp, path[:100]))
            else:
                stat["5.真缺失"] += 1
                by_dir[top]["missing"] += 1
                details["missing"].append((rel_fp, path[:100]))

print("=" * 72)
print("全库图片引用体检")
print("=" * 72)
for k in [
    "图片引用",
    "外链跳过",
    "1.相对解析命中",
    "2.根兜底命中",
    "3.剥../后命中(可修)",
    "4.挂03-知识点后命中(可修)",
    "5.真缺失",
]:
    print(f"  {k:<26} {stat[k]:>6}")

print("\n--- 按顶层目录 ---")
print(f"  {'目录':<28}{'OK':>6}{'兜底':>6}{'可修':>6}{'真缺':>6}")
rows = []
for d, c in by_dir.items():
    ok = c["ok_rel"] + c["ok_root"]
    fix = c["fixable_strip"] + c["fixable_kp"]
    miss = c["missing"]
    if fix or miss:
        rows.append((fix + miss, d, c["ok_rel"], c["ok_root"], fix, miss))
for _, d, a, b, f, m in sorted(rows, reverse=True):
    print(f"  {d:<28}{a+b:>6}{b:>6}{f:>6}{m:>6}")

for kind, label in [("strip", "剥 ../ 可修"), ("kp", "挂 03-知识点 可修"), ("missing", "真缺失")]:
    items = details[kind]
    if not items:
        continue
    print(f"\n--- {label}：{len(items)} 处（前 15 条）---")
    for fp, p in items[:15]:
        print(f"  {fp[:52]}")
        print(f"      -> {p}")
    if len(items) > 15:
        print(f"  ... 其余 {len(items)-15} 处")
