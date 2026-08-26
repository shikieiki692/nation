---
title: 题-398-Clayden-Ch22-P8-亲核芳香取代在合成中的应用
type: 题目
fidelity: 原书逐字
submodule: 共轭加成
exam_stage: 初赛
subject: 有机化学
difficulty: 3
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[芳香亲核取代]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch22-P8]
source: Clayden Organic Chemistry 2nd Ed. Chapter 22 Problem 8
cross_references: ["[[题-628-Clayden-Ch38-P1-碱引发两个简单卡宾反应]]", "[[题-321-Clayden-Ch19-P2-两个烯烃溴化机理和产物]]", "[[题-629-Clayden-Ch38-P2-另一种卡宾方法→天然抗生素]]", "[[题-320-Clayden-Ch19-P1-HCl对三个烯烃加成方向]]"]
module: 有机化学
status: 已填充
---
# 题-398: 亲核芳香取代在合成中的应用

## 题目

How would you carry out these two conversions?

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/2f11a52ed031d0e9f66394aa22b2c16ecae963ca400f8dd020ab4dd709ce3505.jpg]]

**原文题目**：Design synthetic routes for two conversions: (1) methoxybenzene to 2-amino-4-cyanomethoxybenzene, and (2) methoxybenzene to 3-amino-4-cyanomethoxybenzene. Explain why simple SNAr won't work.

## 参考答案

**Answer (English)**: Usually you would think of introducing NH₂ by nitration and reduction (chapter 21), but the regioselectivity is wrong for the first reaction: the methoxy group will direct nitration ortho to itself. An alternative is to introduce both NH₂ and CN as nucleophiles, but the ring is unactivated so we can't use the addition-elimination mechanism (there is nowhere for the negative charge to go). The successful alternatives are electrophilic aromatic substitution followed by diazonium salt formation and the benzyne method. Here are two possible routes. Nitration will insert the nitro group ortho to the more strongly electron-donating MeO group. Reduction, diazotization and substitution with copper cyanide by the SN1 mechanism gives one product.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/1307e1054af2de64e74c9b28093ec9e452515483386a3b5fb900a44284147c90.jpg]]

The other product could come from chlorination, elimination to give a benzyne, addition of amide anion to put the anion ortho to MeO (p. 524 in the textbook) and protonation.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/cd0ea25e83448ad7cc42f62e8f23cab80622fbdc1f7a3b8779b6d1d035eda4c9.jpg]]

**中文解析**：

关键步骤：
1. **为什么SNAr不适用**：甲氧基苯（苯甲醚）的苯环没有强吸电子基团活化，无法进行SNAr的加成-消除机理（没有地方稳定负电荷）
2. **路线1（邻位CN）**：硝化（EAS，甲氧基导向邻位）→还原（NO₂→NH₂）→重氮化→CuCN取代（Sandmeyer反应）→得到邻位氰基产物
3. **路线2（间位CN）**：氯化（EAS）→强碱消除生成苯炔→酰胺负离子加成到苯炔→质子化→得到间位氰基产物

> **核心概念**：当SNAr不可用时（环未活化），需要使用替代方法：重氮盐化学（Sandmeyer反应）或苯炔机理。甲氧基的定位效应决定了不同路线的区域选择性。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[芳香亲核取代]] | SNAr不适用时的替代方法 | 直接 |
| [[合成设计]] | 多步合成路线的设计和区域选择性控制 | 直接 |
| SNAr反应 | SNAr对底物活化的要求 | 间接 |

## 解题思路

1. **读题定位**：题目要求设计两条合成路线——从甲氧基苯得到两种不同位置的氰基取代产物
2. **🔑 关键转换**：SNAr不适用（无活化基团）→路线1用Sandmeyer反应（硝化→重氮化→CuCN）→路线2用苯炔机理（氯化→苯炔→加成）
3. **验证**：检查两条路线的区域选择性是否正确，每步反应是否可行

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 认为可以直接SNAr引入CN | 忽略了SNAr对底物活化的要求 | 甲氧基苯没有强吸电子基团，无法进行SNAr | SNAr需要什么样的底物？ |
| 混淆两条路线的区域选择性 | 对甲氧基的定位效应理解不深 | 硝化→邻位（甲氧基导向）；苯炔→间位（酰胺加成到邻位碳） | 为什么两条路线得到不同位置的产物？ |
| 忽略苯炔中间体的形成条件 | 对苯炔化学不熟悉 | 苯炔需要强碱消除邻位卤素形成 | 苯炔是如何形成的？ |