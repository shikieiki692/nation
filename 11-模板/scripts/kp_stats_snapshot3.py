# -*- coding: utf-8 -*-
"""批次4 补充统计3：分模块 KP 规模与 source_extracts 覆盖。"""
import os
import re
from collections import Counter

VAULT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def read_head(path, n=4000):
    try:
        with open(path, "rb") as f:
            return f.read(n).decode("utf-8-sig", errors="replace")
    except OSError:
        return ""


def fm_value(text, key):
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    m = re.search(rf"(?m)^\s*{re.escape(key)}\s*:\s*(.+?)\s*$", text[3:end])
    return m.group(1) if m else None


def main():
    root = os.path.join(VAULT, "03-知识点")
    mods = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for fn in filenames:
            if not fn.lower().endswith(".md"):
                continue
            p = os.path.join(dirpath, fn)
            rel = os.path.relpath(p, root)
            parts = rel.split(os.sep)
            # 决赛要求细分二级
            if parts[0] == "决赛要求" and len(parts) > 2:
                mod = f"决赛要求/{parts[1]}"
            else:
                mod = parts[0] if len(parts) > 1 else "(根目录)"
            head = read_head(p)
            st = (fm_value(head, "status") or "").strip()
            src = fm_value(head, "source_extracts")
            d = mods.setdefault(mod, {"total": 0, "merged": 0, "src": 0, "diff": 0, "imp": 0})
            d["total"] += 1
            if st == "已合并":
                d["merged"] += 1
                continue
            if src:
                d["src"] += 1
            if fm_value(head, "difficulty"):
                d["diff"] += 1
            if fm_value(head, "importance"):
                d["imp"] += 1
    print("模块 | 总数 | 已合并 | 有效 | src_ext | difficulty | importance")
    for m in sorted(mods):
        d = mods[m]
        eff = d["total"] - d["merged"]
        print(f"{m} | {d['total']} | {d['merged']} | {eff} | {d['src']}/{eff} | {d['diff']}/{eff} | {d['imp']}/{eff}")


if __name__ == "__main__":
    main()
