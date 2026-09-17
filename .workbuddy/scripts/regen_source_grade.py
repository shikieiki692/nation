# -*- coding: utf-8 -*-
"""source_grade 重新分级（2026-09-17 用户拍板）

背景：`.workbuddy/scripts/apply_source_grade.py` 只会给「尚无 source_grade」的文件补值，
      不能改已有值，故本脚本就地改写。
用法：python regen_source_grade.py            # dry-run
      python regen_source_grade.py --write    # 实写
安全：newline="" 保行尾；断言行数守恒；断言「仅 1 行不同」；目标值等于现值则跳过。
"""
import io
import os
import sys
from collections import Counter

WRITE = "--write" in sys.argv
ROOT = r"C:\Obsidion\妙妙屋"
QB = os.path.join(ROOT, "04-题库")

# (路径前缀, 期望现值, 新值)
TARGETS = [
    ("教材习题/化学竞赛初赛讲义", "C", "B"),
    ("教材习题/赵鑫光", "C", "B"),
    ("教材习题/ABOC", "C", "B"),
    ("教材习题/汇智竞赛题目", "C", "A"),
    ("教材习题/一分册能力测试", "A-", "A"),
    ("教材习题/北斗学友", "A-", "A"),
    ("教材习题/二分册能力测试", "A-", "A"),
    ("教材习题/中级无机化学", "A", "C"),
    ("教材习题/无机化学第6版Weller", "B+", "C"),
    ("教材习题/Clayden", "B", "C"),
    ("教材习题/结构化学基础", "A-", "C"),
]

stat = Counter()
detail = Counter()
errors = []

for dp, dn, fn in os.walk(QB):
    for f in fn:
        if not f.endswith(".md"):
            continue
        p = os.path.join(dp, f)
        rel = os.path.relpath(p, QB).replace("\\", "/")
        tgt = None
        for pre, old, new in TARGETS:
            if rel.startswith(pre):
                tgt = (pre, old, new)
                break
        if tgt is None:
            continue
        pre, old, new = tgt
        t = io.open(p, encoding="utf-8", newline="").read()
        if not t.startswith("---"):
            stat[(pre, "无FM")] += 1
            continue
        ls = t.split("\n")
        end = None
        for i in range(1, len(ls)):
            if ls[i].strip() == "---":
                end = i
                break
        if end is None:
            stat[(pre, "FM未闭合")] += 1
            continue
        idx = None
        cur = None
        for i in range(1, end):
            if ls[i].startswith("source_grade:"):
                idx = i
                cur = ls[i].split(":", 1)[1].strip().strip('"')
                break
        if idx is None:
            stat[(pre, "缺字段")] += 1
            errors.append((rel, "缺 source_grade"))
            continue
        if cur == new:
            stat[(pre, "已是目标值")] += 1
            continue
        stat[(pre, "待改(%s→%s)" % (cur, new))] += 1
        detail["%s: %s → %s" % (pre, cur, new)] += 1
        if cur != old:
            errors.append((rel, "现值 %s ≠ 期望 %s" % (cur, old)))
        if WRITE:
            ls[idx] = "source_grade: %s" % new
            nt = "\n".join(ls)
            assert len(nt.split("\n")) == len(ls), "行数变化: %s" % rel
            # 单行 diff 断言
            o, n = t.split("\n"), nt.split("\n")
            ndiff = sum(1 for a, b in zip(o, n) if a != b)
            assert ndiff == 1, "差异行数 %d ≠ 1: %s" % (ndiff, rel)
            with io.open(p, "w", encoding="utf-8", newline="") as fh:
                fh.write(nt)

print("[%s]" % ("WRITE" if WRITE else "DRY-RUN"))
tot = 0
for (pre, kind), c in sorted(stat.items()):
    print("  %-34s %-22s %5d" % (pre, kind, c))
    if kind.startswith("待改"):
        tot += c
print("  → 待改合计 %d" % tot)
print()
print("按「源: 旧→新」细目：")
for k, v in sorted(detail.items(), key=lambda x: -x[1]):
    print("  %-52s %5d" % (k, v))
if errors:
    print()
    print("⚠ 异常 %d 条（前 10）：" % len(errors))
    for rel, why in errors[:10]:
        print("   %s  %s" % (why, rel))
else:
    print()
    print("✓ 无异常：所有命中文件的现值都与期望一致")
