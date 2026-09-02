---
title: 题-568-Clayden-Ch30-P9-Fischer吲哚合成变体Sterling药厂方法
type: 题目
fidelity: 原书逐字
submodule: 杂环合成
exam_stage: 初赛
source_subject: 有机化学
difficulty: 4
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[Fischer吲哚合成]]"]
tags: [化竞, Clayden, 有机化学, 杂环合成]
updated: 2026-07-25
aliases: [Clayden-Ch30-P9]
source: Clayden Organic Chemistry 2nd Ed. Chapter 30 Problem 9
cross_references: ["[[题-551-Clayden-Ch29-P2-烷基吡啶LHMDS侧链延伸]]", "[[题-550-Clayden-Ch29-P1-杂环上亲电亲核取代产物预测]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 模块习题集
---
# 题-568: Fischer吲哚合成变体（Sterling药厂方法）

## 题目

**【中文】**为该化合物（见图）设计一条合成路线。

**【原文】**Suggest a synthesis for this compound.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/069bb8bd6fabaff790f9d25156966479fc210efc0af70fb8196d19df1774bd5c.jpg]]

**原文题目**：Suggest a synthesis for this indole derivative. Consider the Fischer indole synthesis and the Sterling drug company approach to protecting the amino group.

## 参考答案

**Answer (English)**: This looks very much like a perfect subject for the Fischer indole synthesis.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/cf9c59e1fef4923024922b4aa9215468f09d4ad9af22c10d6117cdae136ef67e.jpg]]

We may wonder how we are going to have an amino group in that position on the keto ester. Surely it will cyclize onto the ester to form a lactam? One solution would be to protect it with a Boc group, but the solution found by the Sterling drug company was partly motivated by a desire to make a variety of compounds with different amine substituents. They chose hydroxyl as an easily replaceable group and accepted that the starting material would exist as a lactone.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/7e7694606bf6a4160bbad6436b0132eff3603d218212f0cdbe9d57d8eea85de4.jpg]]

The first step is a typical Claisen ester condensation and the second is an acid-catalysed thermodynamically controlled transesterification (the lactone and ethyl ester exchange alcohol partners) to give the more stable six-membered lactone, followed by decarboxylation. Now the Fischer indole synthesis works well and work-up with dry HCl in methanol gave the alkyl chloride that could be displaced with amines to give a series of anti-depressants.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/36f9d3a475313fb7095c77c32b777a22b88fc7286cdff3247bc97e6f3b36c4bd.jpg]]

**中文解析**：

**逆合成分析**：目标分子是3-取代吲哚——经典Fischer吲哚合成的底物。

**关键挑战**：酮酯底物上已有氨基，如果直接使用会与酯基形成内酰胺——需要保护。

**Sterling药厂的巧妙策略**：
1. **不使用Boc保护**：虽然Boc保护可行，但Sterling药厂希望快速制备不同胺取代基的化合物库
2. **用羟基作为可替换基团**：起始原料中的OH以六元环内酯形式存在（热力学更稳定），避免了内酰胺问题
3. **Claisen缩合+转酯化**：第一步是Claisen酯缩合，第二步是酸催化热力学控制的转酯化（五元内酯→六元内酯）+脱羧
4. **Fischer吲哚合成+胺化**：Fischer吲哚环化顺利进行，HCl/MeOH处理将内酯转为氯化物，再用不同胺亲核取代得到抗抑郁药物系列

> **药物化学策略**：用可替换的离去基团（OH→Cl）实现快速多样化——这是药物化学中"平行合成"的经典案例。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[Fischer吲哚合成]] | 吲哚环的构建和底物设计 | 直接 |
| [[吲哚]] | 3-取代吲哚的合成策略 | 直接 |
| [[保护基]] | 内酯作为氨基保护的替代策略（vs Boc） | 直接 |
| [[Claisen缩合]] | 酯缩合构建酮酯底物 | 间接 |

## 解题思路

1. **读题定位**：目标是3-取代吲哚抗抑郁药——逆合成到Fischer吲哚合成
2. **🔑 关键转换**：Claisen缩合→转酯化（五元→六元内酯）→脱羧→Fischer吲哚→HCl/MeOH→Cl取代→胺化
3. **验证**：检查内酯环大小变化的热力学驱动力；检查胺化位点是否正确

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 直接用Boc保护氨基 | 没理解Sterling策略的优越性 | 内酯策略允许快速多样化，无需反复脱/装保护基 | Boc保护和内酯策略各有什么优缺点？ |
| 转酯化方向画反 | 没理解热力学控制 | 六元环比五元环更稳定，酸催化下热力学驱动转酯化 | 为什么六元内酯比五元内酯更稳定？ |
| 脱羧步骤遗漏 | 不清楚Claisen缩合后的处理 | β-酮酯需脱羧才能得到最终酮底物 | 什么条件下β-酮酯脱羧？ |