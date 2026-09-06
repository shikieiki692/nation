# -*- coding: utf-8 -*-
"""source_category 落库：按已确认分类给全部题目文件 FM 写入 source_category 字段。
用法： python apply_source_category.py            # dry-run（只统计不写）
     python apply_source_category.py --write    # 实写
规则：FM 末尾（闭合 --- 前）追加；已有 source_category 则跳过（幂等）。"""
import io
import os
import re
import sys
import collections

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
WRITE = "--write" in sys.argv
VAULT = r"C:\Obsidion\妙妙屋"
QB = os.path.join(VAULT, "04-题库")

# 路径前缀 → source_category（按确认清单定稿顺序匹配）
RULES = [
    ("真题/省预赛", "竞赛导向·真题（省级）"),
    ("真题/", "竞赛导向·真题"),
    ("教材习题/化学竞赛初赛讲义", "竞赛导向·竞赛教辅"),
    ("教材习题/高中化学竞赛教程第一分册", "竞赛导向·竞赛教材"),
    ("教材习题/一分册能力测试", "竞赛导向·竞赛教辅"),
    ("教材习题/高中化学竞赛教程第二分册", "竞赛导向·竞赛教材"),
    ("教材习题/化学能力测试", "竞赛导向·竞赛教辅"),
    ("教材习题/化竟能力测试", "竞赛导向·竞赛教辅"),
    ("教材习题/ABOC", "竞赛导向·竞赛教材"),
    ("教材习题/上海中学竞赛课程", "竞赛导向·竞赛教材"),
    ("教材习题/汇智竞赛题目", "竞赛导向·竞赛教辅"),
    ("教材习题/赵鑫光", "竞赛导向·竞赛教材"),
    ("教材习题/Clayden", "教材课后习题"),
    ("教材习题/结构化学基础", "教材课后习题"),
    ("教材习题/无机化学例题与习题", "教材课后习题"),
    ("元文件/教材习题", "教材课后习题"),
    ("教材习题/无机化学第6版Weller", "教材课后习题"),
    ("教材习题/中级无机化学", "教材课后习题"),
    ("教材习题/无机化学第5版", "教材课后习题"),
    ("教材习题/", "教材课后习题"),
    ("化学原理/Ch", "教材课后习题"),
    ("有机化学/", "其他类型·自编章节题"),
    ("分析化学/", "其他类型·自编章节题"),
    ("元素化学/", "其他类型·自编章节题"),
    ("物理化学/", "其他类型·自编章节题"),
    ("教学改编题/", "其他类型·教学改编"),
    ("经典例题/", "其他类型·教材例题"),
]

stat = collections.Counter()
n_write = n_skip = n_nofm = 0
for dp, _, ns in os.walk(QB):
    for n in ns:
        if not n.endswith(".md"):
            continue
        p = os.path.join(dp, n)
        rel = os.path.relpath(p, QB).replace("\\", "/")
        t = open(p, encoding="utf-8", newline="").read()
        if not t.startswith("---"):
            n_nofm += 1
            continue
        ls = t.split("\n")
        end = None
        for i in range(1, len(ls)):
            if ls[i].strip() == "---":
                end = i
                break
        if end is None:
            n_nofm += 1
            continue
        fm = "\n".join(ls[1:end])
        if not re.search(r"^type:\s*题目", fm, re.M):
            continue
        if re.search(r"^source_category:", fm, re.M):
            n_skip += 1
            continue
        cat = None
        for prefix, c in RULES:
            if rel.startswith(prefix):
                cat = c
                break
        if cat is None:
            stat["⚠ 未匹配规则"] += 1
            print("未匹配:", rel)
            continue
        stat[cat] += 1
        if WRITE:
            ls.insert(end, f"source_category: {cat}")
            with open(p, "w", encoding="utf-8", newline="") as f:
                f.write("\n".join(ls))
            n_write += 1

print(f"[{'WRITE' if WRITE else 'DRY-RUN'}] 待写 {sum(stat.values())}｜已有跳过 {n_skip}｜无FM {n_nofm}")
for k, c in stat.most_common():
    print(f"  {c:>5}  {k}")
if WRITE:
    print(f"实写完成: {n_write}")
