# -*- coding: utf-8 -*-
"""source_grade 落库：按 2026-09-17 重评的分级给「尚无 source_grade」的题目文件 FM 补写。
用法： python apply_source_grade.py            # dry-run（只统计不写）
     python apply_source_grade.py --write    # 实写
规则：FM 末尾（闭合 --- 前）追加；**已有 source_grade 则跳过（幂等）**。
      ⚠️ 本脚本**不能改已有值** —— 要重评/改写请用 `.workbuddy/scripts/regen_source_grade.py`
      （就地改写 + 行数守恒 + 单行 diff 断言）。
分级依据（2026-09-17 重评；用户拍板「真题 > 竞赛导向题集 > 教程/讲义 > 大学教材」）：
      真题 A/A- ｜ 竞赛导向题集（能力测试三册/北斗/汇智）A ｜ 竞赛教程（一/二分册）A/A- ｜
      上海中学 B+ ｜ 竞赛教材·讲义（初赛讲义/赵鑫光/ABOC）B ｜ 大学教材课后习题 一律 C ｜ 自编 B-。
      原则：**source_grade 评「考试指向性」，与 source_category（来源性质）正交，故同一 category 可跨档。**
      ⚠️ validate_kb / audit_question_bank **均不校验 source_grade 值集**（无枚举约束），
        但值集约定仍用 A/A-/B+/B/B-/C+/C。
覆盖记录：2026-09-17 就地改 2,564 文件（11 个源），提交见该日 commit。
"""
import io
import os
import re
import sys
import collections

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
WRITE = "--write" in sys.argv
VAULT = r"C:\Obsidion\妙妙屋"
QB = os.path.join(VAULT, "04-题库")

# 路径前缀 → source_grade（长前缀须排在短前缀之前；ASCII 连字符）
RULES = [
    ("真题/省预赛", "A-"),                          # 官方命题·省级初选向
    ("真题/", "A"),                                 # 25~40 届初赛/决赛，组卷首选
    # ── 竞赛导向题集（考试型，真题风格）→ A ──
    ("教材习题/化学能力测试", "A"),                 # 9 章 A/B 卷，d4+ 98%
    ("教材习题/化竟能力测试", "A"),                 # 2 题样板批（已全部 deprecated）
    ("教材习题/一分册能力测试", "A"),               # 教程一分册配套 14 章 A/B 卷
    ("教材习题/二分册能力测试", "A"),               # 36 卷（type: 题组），走豁免条款 A
    ("教材习题/北斗学友", "A"),                     # 7 卷竞赛模拟卷
    ("教材习题/汇智竞赛题目", "A"),                 # 竞赛题目集（2026-09-17 由 C 提为 A）
    # ── 竞赛教程正册 → A / A- ──
    ("教材习题/高中化学竞赛教程第二分册", "A"),     # d4+ 81%
    ("教材习题/高中化学竞赛教程第一分册", "A-"),    # 量大，d4 主体
    # ── 竞赛教材/讲义 → B+ / B ──
    ("教材习题/上海中学竞赛课程", "B+"),
    ("教材习题/化学竞赛初赛讲义", "B"),             # 2026-09-17 由 C+ 提为 B
    ("教材习题/赵鑫光", "B"),                       # 报告「高中化学基础」；2026-09-17 由 C 提为 B
    ("教材习题/ABOC", "B"),                         # 2026-09-17 由 C 提为 B
    # ── 大学教材课后习题 → 一律 C（2026-09-17 归一）──
    ("教材习题/结构化学基础", "C"),                 # 2026-09-17 由 A- 降为 C
    ("教材习题/中级无机化学", "C"),                 # 2026-09-17 由 A 降为 C
    ("教材习题/无机化学第6版Weller", "C"),          # 2026-09-17 由 B+ 降为 C
    ("教材习题/Clayden", "C"),                      # 2026-09-17 由 B 降为 C
    ("教材习题/无机化学例题与习题", "C"),
    ("元文件/教材习题", "C"),                       # 无机例题与习题析出批
    ("教材习题/无机化学第5版", "C"),
    ("教材习题/", "C"),                             # 兜底：未单列的教材课后源
    ("化学原理/Ch", "C"),                           # 普化原理（第4版）习题解析转录
    # ── 自编/改编 ──
    ("有机化学/", "B-"),
    ("分析化学/", "B-"),
    ("元素化学/", "B-"),
    ("物理化学/", "B-"),
    ("教学改编题/", "B-"),
    ("经典例题/", "B-"),
]

# source_category → 期望 grade 一致性校验表（交叉验证用；2026-09-17 重评后口径）
CAT_EXPECT = {
    "竞赛导向·真题": {"A"},
    "竞赛导向·真题（省级）": {"A-"},
    "教材课后习题": {"C"},                          # 2026-09-17 起归一：大学教材课后习题一律 C
    "竞赛导向·竞赛教材": {"A", "A-", "B+", "B"},   # 教程一/二分册 A/A-、上海中学 B+、赵鑫光/ABOC B
    "竞赛导向·竞赛教辅": {"A", "B"},                # 能力测试三册/北斗/汇智 A、初赛讲义 B
    "其他类型·自编章节题": {"B-"},
    "其他类型·教学改编": {"B-"},
    "其他类型·教材例题": {"B-"},
}


stat = collections.Counter()
mismatch = collections.Counter()
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
        m_cat = re.search(r"^source_category:\s*(.+)$", fm, re.M)
        cat = m_cat.group(1).strip().strip('"') if m_cat else "(无category)"
        # ⚠️ 一致性校验必须在「跳过已有值」之前做，否则全部跳过时会假报「全部一致 ✓」
        m_have = re.search(r"^source_grade:\s*(.+)$", fm, re.M)
        if m_have:
            n_skip += 1
            cur = m_have.group(1).strip().strip('"')
            if cat in CAT_EXPECT and cur not in CAT_EXPECT[cat]:
                mismatch[f"{cat} → {cur}（现有值）"] += 1
            continue
        grade = None
        for prefix, g in RULES:
            if rel.startswith(prefix):
                grade = g
                break
        if grade is None:
            stat["⚠ 未匹配规则"] += 1
            print("未匹配:", rel)
            continue
        stat[f"{cat} → {grade}"] += 1
        if cat in CAT_EXPECT and grade not in CAT_EXPECT[cat]:
            mismatch[f"{cat} → {grade}"] += 1
        if WRITE:
            ls.insert(end, f"source_grade: {grade}")
            with open(p, "w", encoding="utf-8", newline="") as f:
                f.write("\n".join(ls))
            n_write += 1

print(f"[{'WRITE' if WRITE else 'DRY-RUN'}] 待写 {sum(stat.values())}｜已有跳过 {n_skip}｜无FM {n_nofm}")
for k, c in sorted(stat.items()):
    print(f"  {c:>5}  {k}")
if mismatch:
    print("⚠ 与 source_category 期望不一致：")
    for k, c in mismatch.most_common():
        print(f"  {c:>5}  {k}")
else:
    print("交叉校验：全部 grade 与 source_category 期望一致 ✓")
if WRITE:
    print(f"实写完成: {n_write}")
