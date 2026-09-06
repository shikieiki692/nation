# -*- coding: utf-8 -*-
"""阶段测试卷选题：扫题池 → 分组统计 → 按梯度选 50 题 → 出卷 + used_in 回填"""
import io, os, re, yaml, random, collections, json, sys

ROOT = r"C:\Obsidion\妙妙屋\04-题库"
SKIP = {"deprecated"}

def fm_of(path):
    try:
        text = io.open(path, encoding="utf-8").read()
    except Exception:
        return None
    m = re.match(r"^---\r?\n(.*?)\r?\n---", text, re.S)
    if not m:
        return None
    try:
        fm = yaml.safe_load(m.group(1))
    except Exception:
        return None
    return fm if isinstance(fm, dict) else None

def scan(subject):
    pool = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in {"_归档", "_archive_v2", "浙江卷2021", "浙江卷2022", "浙江卷2023"}]
        for f in filenames:
            if not f.endswith(".md"):
                continue
            p = os.path.join(dirpath, f)
            fm = fm_of(p)
            if not fm:
                continue
            if fm.get("pack") != "模块习题集" or fm.get("subject_module") != subject:
                continue
            if str(fm.get("status", "")).strip() in SKIP or "deprecated" in str(fm.get("status", "")):
                continue
            if fm.get("used_in"):
                continue
            d = fm.get("difficulty")
            try:
                d = int(d)
            except Exception:
                continue
            if not (1 <= d <= 5):
                continue
            rel = os.path.relpath(p, os.path.dirname(ROOT))
            pool.append({
                "file": os.path.splitext(f)[0],
                "rel": rel,
                "submodule": str(fm.get("submodule", "")).strip(),
                "difficulty": d,
                "status": str(fm.get("status", "")).strip(),
            })
    return pool

if __name__ == "__main__":
    for subject in ["结构化学", "有机化学", "元素与分析"]:
        pool = scan(subject)
        sub = collections.Counter(p["submodule"] or "(空)" for p in pool)
        dif = collections.Counter(p["difficulty"] for p in pool)
        print(f"== {subject}: 池 {len(pool)}")
        print("  难度:", dict(sorted(dif.items())))
        print("  子模块 top12:", sub.most_common(12))
