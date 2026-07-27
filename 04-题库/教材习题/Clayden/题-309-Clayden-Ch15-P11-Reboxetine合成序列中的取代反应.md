---
title: 题-309-Clayden-Ch15-P11-Reboxetine合成序列中的取代反应
type: 题目
submodule: 亲核取代
exam_stage: 初赛
subject: 有机化学
difficulty: 3
teaching_level: 拓展
syllabus_codes: ["33"]
knowledge_points: ["[[亲核取代]]", "[[逆合成分析]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch15-P11]
source: Clayden Organic Chemistry 2nd Ed. Chapter 15 Problem 11
cross_references: ["[[题-303-Clayden-Ch15-P5-β-内酰胺合成中的亲核取代]]", "[[题-295-Clayden-Ch14-P5-反应产物手性和对映体纯度]]"]
module: 有机化学
status: 已填充
---
# 题-309: Reboxetine合成序列中的取代反应

## 题目

The pharmaceutical company Pfizer made the antidepressant reboxetine by the following sequence of reactions. Suggest a reagent for each step, commenting on aspects of stereochemistry or reactivity.

**原文题目**：辉瑞公司通过以下反应序列制备抗抑郁药Reboxetine。为每步建议试剂。

## 参考答案

**Answer (English)**: The synthesis involves multiple SN2 reactions: epoxide opening with phenoxide (inversion), mesylation of primary OH, intramolecular SN2 to form new epoxide, azide opening + reduction, acylation, intramolecular cyclization, and amide reduction.

**中文解析**：

| 步骤 | 反应类型 | 试剂 | 关键点 |
|------|----------|------|--------|
| 1 | 环氧化物开环（SN2） | PhONa | 苄位SN2更快，构型翻转 |
| 2 | 羟基→甲磺酸酯 | MsCl, Et₃N | 伯OH比仲OH反应更快 |
| 3 | 分子内SN2→新环氧化物 | NaOH | OH进攻MsO⁻离去的碳 |
| 4 | 环氧化物+N₃⁻开环 | NaN₃ | 还原后得胺 |
| 5 | 胺→酰胺 | 酰氯 + 碱 | 标准酰化 |
| 6 | 分子内取代→新环 | KOt-Bu | 醇去质子化后进攻Cl |
| 7 | 酰胺→胺 | LiAlH₄ | 还原 |

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[亲核取代]] | 多步SN2反应综合应用 | 直接 |
| [[逆合成分析]] | 从产物逆推每步试剂 | 直接 |
| SN2反应 | 构型翻转在合成中的应用 | 间接 |

## 解题思路

1. **读题定位**：多步合成→每步需选试剂→分析反应类型和立体化学
2. **🔑 关键转换**：每步都是SN2（构型翻转）→环氧化物开环→甲磺酰化→分子内关环→叠氮开环→酰化→再关环→还原
3. **验证**：检查每步立体化学——所有SN2都导致构型翻转

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 步骤2选错OH | 没考虑位阻 | 伯OH比仲OH反应更快 | 为什么伯OH更快？ |
| 步骤4用NH₃ | 不了解叠氮化物策略 | NaN₃更好：更亲核、还原后得伯胺 | 叠氮如何还原为胺？ |
| 忘记步骤3需碱 | OH亲核性不够 | OH需去质子化才能进攻 | 哪些碱适合？ |