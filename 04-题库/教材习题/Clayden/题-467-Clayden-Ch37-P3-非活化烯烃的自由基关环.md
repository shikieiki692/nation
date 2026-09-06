---
title: 题-467-Clayden-Ch37-P3-非活化烯烃的自由基关环
type: 题目
fidelity: 原书逐字
submodule: 自由基反应
exam_stage: 初赛
source_subject: 有机化学
difficulty: 3
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[自由基]]"]
tags: [化竞, Clayden, 有机化学, 自由基反应]
updated: 2026-07-25
aliases: [Clayden-Ch37-P3]
source: Clayden Organic Chemistry 2nd Ed. Chapter 37 Problem 3
cross_references: ["[[题-465-Clayden-Ch37-P1-重要自由基反应复习]]", "[[题-466-Clayden-Ch37-P2-重氮盐亲核取代vs自由基对比]]", "[[题-291-Clayden-Ch14-P1-五个分子手性判断]]", "[[题-292-Clayden-Ch14-P2-旋光值区分]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 章节练习
source_category: 教材课后习题
---
# 题-467: 非活化烯烃的自由基关环反应

## 题目

Suggest a mechanism for this reaction and comment on the ring size formed. What is the minor product likely to be?

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/4ebdbbad19ede233382c45d3a917a832a649849be29f5311a0f7d6be1012769c.jpg]]

**原文题目**：Suggest a mechanism for this reaction and comment on the ring size formed. What is the minor product likely to be?

## 参考答案

**Answer (English)**: The peroxide is a source of benzoyloxy radicals (PhCO₂·) and these capture hydrogen atoms to give the most stable radical. The best one here is stabilized by both CN and CO₂Et. Cyclization onto the alkene gives mainly a secondary radical on a six-membered ring and this abstracts a hydrogen from starting material to complete the cycle.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/e001e2a2a129f7daff5c5d9aa73028fe62540bf98ecf86f3c89d0187a2b040fc.jpg]]

The alternative is to add to the more substituted end of the alkene. This gives a less stable primary radical, but this '5-exo' ring closure is often preferred because the orbital alignment is better. The minor product has a five-membered ring.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/61ac7af60a454517c89bac76663edd505e1dbf951d0cba67ead9f3345933c0c3.jpg]]

**中文解析**：

关键步骤：
1. **引发**：过氧化苯甲酰（BPO）热分解产生苯甲酰氧自由基（PhCO₂·），该自由基从底物的活泼C-H键（被CN和CO₂Et双重活化的位点）夺取氢原子，产生碳自由基
2. **关环（6-endo vs 5-exo）**：
   - **主产物（6-endo）**：自由基加成到烯烃的末端碳上，形成六元环上的仲自由基（热力学更稳定的自由基）
   - **副产物（5-exo）**：自由基加成到烯烃的内部碳上，形成五元环上的伯自由基（轨道对齐更好，动力学更有利）
3. **链传递**：关环后的自由基从另一分子底物夺取氢原子，完成链循环

> **注意**：Baldwin规则和Beckwith-Houk模型预测5-exo关环通常比6-endo更有利（轨道对齐更好），但这里6-endo产物为主，说明自由基稳定性因素在此占主导。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[自由基]] | 自由基的产生、关环和链传递 | 直接 |
| [[自由基机理]] | 完整的自由基链反应机理（引发-传递-终止） | 直接 |
| [[关环反应]] | 5-exo vs 6-endo关环的选择性 | 直接 |
| [[Baldwin规则]] | 关环的立体电子学要求 | 间接 |

## 解题思路

1. **读题定位**：题目要求画机理、讨论环大小、预测副产物——这是自由基关环反应的经典问题
2. **🔑 关键转换**：过氧化物引发 → 夺氢产生碳自由基 → 关环到非活化烯烃 → 两种可能的环大小（5-exo和6-endo）→ 夺氢完成链
3. **验证**：检查主产物是否为六元环（6-endo），副产物是否为五元环（5-exo），自由基稳定性是否合理

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 认为自由基只能发生5-exo关环 | 教条地应用Baldwin规则 | 5-exo通常更有利，但自由基稳定性可以逆转选择性 | 什么时候6-endo会比5-exo更有利？ |
| 忘记画链传递步骤 | 只关注关环步骤 | 自由基关环后必须夺氢完成链传递，否则反应无法持续 | 链传递的氢来源是什么？ |
| 将过氧化物引发写成离子机理 | 混淆自由基和离子引发 | BPO均裂产生PhCO₂·自由基，不是离子 | 过氧化物为什么容易均裂？ |
| 混淆主副产物的环大小 | 没有分析两种关环路径的稳定性 | 6-endo→六元环（主），5-exo→五元环（副） | 为什么5-exo的动力学更有利？ |