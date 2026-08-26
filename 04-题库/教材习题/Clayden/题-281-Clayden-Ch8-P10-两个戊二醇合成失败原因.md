---
title: 题-281-Clayden-Ch8-P10-两个戊二醇合成失败原因
type: 题目
fidelity: 原书逐字
submodule: 酸碱质子理论
exam_stage: 初赛
subject: 有机化学
difficulty: 4
teaching_level: 拓展
syllabus_codes: []
knowledge_points: ["[[pKa]]", "[[酸碱强度]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch8-P10]
source: Clayden Organic Chemistry 2nd Ed. Chapter 8 Problem 10
cross_references: ["[[题-282-Clayden-Ch8-P11-选择合适的碱去质子化给定分子]]", "[[题-280-Clayden-Ch8-P9-半胱氨酸和精氨酸pKa及不同pH结构]]"]
module: 有机化学
status: 已填充
---
# 题-281: 两个戊二醇合成失败原因

## 题目

Explain why the synthesis of pentan-1,4-diol fails in two cases: (1) using 2 equivalents of Grignard, (2) using excess Grignard. OH (pKa ~ 16) protonates Grignard reagent.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/3ad8c56813b6a5be5d9f7045a4c08d1f7fc5dcd92cf1a091f7fc60277e484402.jpg]]

**原文题目**：解释为什么戊-1,4-二醇的合成在两种情况下失败：(1) 使用2当量的Grignard试剂，(2) 使用过量的Grignard试剂。OH（pKa ~ 16）会质子化Grignard试剂。

## 参考答案

**Answer (English)**: 
- Grignard reagents (RMgX) are strong bases (conjugate acid RH has pKa ~ 50). They will deprotonate any O-H bond (pKa ~ 16) before nucleophilic addition occurs.
- Case 1 (2 equiv): The first Grignard deprotonates one OH, the second deprotonates the other OH — no nucleophilic addition happens.
- Case 2 (excess Grignard): Intramolecular deprotonation kills the reaction before addition can occur.
- Solution: Use a protecting group (e.g., THP or silyl ether) to mask the OH groups before Grignard addition.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/e5763910c5fcd912e49d3a6683364b38d7d1db7983598453acf971c6d20ac25b.jpg]]

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/f39e1c05a589086880f1341ca0fbaa731a14e501ebc7fe04e8a5eb84e2c9f263.jpg]]

**中文解析**：
1. **Grignard试剂的碱性**：RMgX是极强碱（共轭酸RH的pKa ~ 50），远强于任何醇（pKa ~ 16）。Grignard会优先质子化OH而不是进行亲核加成。
2. **2当量情况**：第一当量Grignard去质子化一个OH，第二当量去质子化另一个OH，两个OH都被消耗，无亲核加成发生。
3. **过量情况**：分子内去质子化（两个OH在分子内竞争）使反应在加成前就失败。
4. **解决方案**：使用保护基（如THP或硅醚）保护OH，再进行Grignard反应，最后脱保护。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[pKa]] | Grignard碱性与OH酸性的pKa比较 | 直接 |
| [[酸碱强度]] | Grignard是极强碱，会优先质子化酸性氢 | 直接 |
| [[有机酸碱性]] | 官能团兼容性和保护基策略 | 间接 |

## 解题思路

1. **读题定位**：分子有两个OH（pKa ~ 16），Grignard是强碱（共轭酸pKa ~ 50），会优先质子化OH。
2. **🔑 关键转换**：pKa差值巨大（50 vs 16），Grignard会瞬间质子化OH，无法进行亲核加成。需用保护基。
3. **验证**：2当量Grignard恰好消耗两个OH；过量Grignard则更多消耗。两种情况都导致无产物。

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 认为Grignard会加成到OH上 | Grignard是亲核试剂，但OH的酸性使其先质子化 | 酸碱反应比亲核加成快 | Grignard的碱性和亲核性哪个优先？ |
| 认为2当量恰好够用 | 2当量恰好消耗两个OH，无剩余用于加成 | 需要保护OH后再加成 | 为什么2当量不够？ |
| 忽略保护基策略 | 不保护OH无法进行Grignard反应 | 用THP或硅醚保护OH | 有哪些常用的OH保护基？ |