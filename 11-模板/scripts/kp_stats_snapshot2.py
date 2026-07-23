# -*- coding: utf-8 -*-
"""批次4 补充统计：题库二级分桶、KP字段覆盖率、题型页计数。"""
import os
import re
from collections import Counter

VAULT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def read_head(path, n=4000):
    try:
        with open(path, "rb") as f:
            raw = f.read(n)
        return raw.decode("utf-8-sig", errors="replace")
    except OSError:
        return ""


def read_all(path):
    try:
        with open(path, "rb") as f:
            return f.read().decode("utf-8-sig", errors="replace")
    except OSError:
        return ""


def fm_value(text, key):
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    fm = text[3:end]
    m = re.search(rf"(?m)^\s*{re.escape(key)}\s*:\s*(.+?)\s*$", fm)
    return m.group(1) if m else None


def scan_dir(rel):
    root = os.path.join(VAULT, rel)
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for fn in filenames:
            if fn.lower().endswith(".md"):
                out.append(os.path.join(dirpath, fn))
    return out


def main():
    # ---------- 题库二级分桶 ----------
    tk = scan_dir("04-题库")
    b2 = Counter()
    b2_timu = Counter()
    for p in tk:
        head = read_head(p)
        ty = (fm_value(head, "type") or "").strip().strip("'\"")
        rel = os.path.relpath(p, os.path.join(VAULT, "04-题库"))
        parts = rel.split(os.sep)
        key = "/".join(parts[:2]) if len(parts) > 2 else (parts[0] if len(parts) > 1 else "(根目录)")
        # 真题按初赛/决赛聚合
        if parts[0] == "真题" and len(parts) > 1:
            sub = parts[1]
            key = "真题/决赛" if "决赛" in sub else ("真题/初赛" if "初赛" in sub else f"真题/{sub}")
        b2[key] += 1
        if ty == "题目":
            b2_timu[key] += 1
    print("===== 04-题库 二级分桶 (md总数 / type=题目) =====")
    for k, v in sorted(b2.items()):
        print(f"  {k}: {v} / {b2_timu.get(k, 0)}")

    # ---------- KP 字段覆盖率 ----------
    kp = scan_dir("03-知识点")
    total = len(kp)
    filled = 0
    c_diff = c_imp = c_src = c_view = 0
    for p in kp:
        head = read_head(p)
        st = (fm_value(head, "status") or "").strip()
        if st == "已合并":
            continue
        filled += 1
        if fm_value(head, "difficulty"):
            c_diff += 1
        if fm_value(head, "importance"):
            c_imp += 1
        if fm_value(head, "source_extracts"):
            c_src += 1
        body = read_all(p)
        if "教学视角" in body:
            c_view += 1
    print("\n===== 03-知识点 字段覆盖（剔除 status=已合并） =====")
    print(f"有效 KP 数（总{total} - 已合并）: {filled}")
    print(f"difficulty 有值: {c_diff}")
    print(f"importance 有值: {c_imp}")
    print(f"source_extracts 有值: {c_src}")
    print(f"正文含『教学视角』: {c_view}")

    # ---------- 题型页 ----------
    for sub in ("题型",):
        d = os.path.join("04-专题与题型", sub)
        if os.path.isdir(os.path.join(VAULT, d)):
            fs = scan_dir(d)
            stc = Counter()
            for p in fs:
                stc[fm_value(read_head(p), "status") or "(无status字段)"] += 1
            print(f"\n===== 04-专题与题型/{sub} =====")
            print(f"md 总数: {len(fs)}")
            for k, v in stc.most_common():
                print(f"  {k}: {v}")

    # ---------- 题库 knowledge_points 覆盖 ----------
    c_kp = 0
    t_timu = 0
    c_sub = 0
    c_dif = 0
    for p in tk:
        head = read_head(p)
        ty = (fm_value(head, "type") or "").strip().strip("'\"")
        if ty != "题目":
            continue
        t_timu += 1
        if fm_value(head, "knowledge_points"):
            c_kp += 1
        if fm_value(head, "subject"):
            c_sub += 1
        if fm_value(head, "difficulty"):
            c_dif += 1
    print("\n===== 04-题库 type=题目 字段覆盖 =====")
    print(f"type=题目: {t_timu}")
    print(f"knowledge_points 有值: {c_kp}")
    print(f"subject 有值: {c_sub}")
    print(f"difficulty 有值: {c_dif}")


if __name__ == "__main__":
    main()
