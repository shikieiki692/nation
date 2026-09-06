---
title: "题-297-Clayden-Ch14-P7-RS构型标注"
type: 题目
fidelity: 原书逐字
submodule: 立体化学
exam_stage: 初赛
source_subject: 有机化学
difficulty: 2
teaching_level: 基础
syllabus_codes: ["36"]
knowledge_points: ["[[立体化学]]", "[[手性]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch14-P7]
source: Clayden Organic Chemistry 2nd Ed. Chapter 14 Problem 7
cross_references: ["[[题-291-Clayden-Ch14-P1-五个分子手性判断]]", "[[题-294-Clayden-Ch14-P4-四个化合物立体化学讨论]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 章节练习
source_category: 教材课后习题
---
# 题-297: R/S构型标注

## 题目

Assign a configuration (R or S) to each of these compounds.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/d5bf98fff5f0ec6b3748708cb0d838eb3534d206239c1a47684a8d3744edaae0.jpg]]

**原文题目**：给这些化合物指定构型（R或S）。

## 参考答案

**Answer (English)**: Carrying out the procedure given in the chapter: prioritize substituents 1-4 and deduce the configuration. In all cases '4' is H and goes at the back.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/006c0ea37d8eee29e0276b246dc431998eabe29f5f14b5818bb538f5a6a2b67b.jpg]]

(R)-2,2,2-三氟-1-(9-蒽基)乙醇

**中文解析**：

**CIP优先级规则**（Cahn-Ingold-Prelog）：

| 化合物 | 手性碳上的基团 | 优先级排序 | 构型 | 说明 |
|--------|--------------|:---:|:---:|------|
| Pirkle手性溶剂化试剂 | -OH, -CF₃, -Ar, -H | O > CF₃ > Ar > H | **R** | 用于检测对映体纯度 |
| 半胱氨酸 | -NH₂, -SH, -COOH, -H | S > N > O > H | **R** | 天然氨基酸是R（因为S优先于O）——其他天然氨基酸都是S |
| 香茅醇 | -OH, -CH₂CH=..., -CH₂CH₃, -H | O > C(连C=C) > C(连C) > H | **S** | 天然香茅醇 |

**半胱氨酸的特殊性**：S优先于O→NH₂(1), SH(2), COOH(3), H(4)→R构型。这是例外——几乎所有其他天然氨基酸都是S。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[立体化学]] | R/S构型的指定方法 | 直接 |
| [[手性]] | CIP优先级规则 | 直接 |
| [[Fischer投影式]] | 从结构式确定构型 | 间接 |

## 解题思路

1. **读题定位**：3个化合物，每个需要指定R/S构型
2. **🔑 关键转换**：按CIP规则排列4个基团优先级→H放后面→1→2→3顺时针=R，逆时针=S
3. **验证**：半胱氨酸是例外——S(原子序数16) > O(8)→所以是R而非S

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 半胱氨酸标为S | 认为所有天然氨基酸都是S | S优先于O→半胱氨酸是R | 原子序数如何决定优先级？ |
| 搞混R和S的定义 | 记忆错误 | 1→2→3顺时针=R，逆时针=S（H在后方时） | 如果H不在后方怎么办？ |
| 忽略双键的处理 | 不了解CIP规则对双键的处理 | C=C视为C连两个C（虚拟原子） | 为什么C=C按两个C计算？ |