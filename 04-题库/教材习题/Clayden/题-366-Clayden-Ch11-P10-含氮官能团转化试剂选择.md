---
title: 题-366-Clayden-Ch11-P10-含氮官能团转化试剂选择
type: 题目
fidelity: 原书逐字
submodule: 缩醛与亚胺
exam_stage: 初赛
source_subject: 有机化学
difficulty: 3
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[亚胺]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch11-P10]
source: Clayden Organic Chemistry 2nd Ed. Chapter 11 Problem 10
cross_references: ["[[题-328-Clayden-Ch20-P1-羰基化合物烯醇式绘制和稳定性]]", "[[题-262-Clayden-Ch6-P1-硼氢化钠还原醛酮机理]]", "[[题-329-Clayden-Ch20-P2-两个酮烯醇含量差异解释]]", "[[题-263-Clayden-Ch6-P2-环丙酮水合vs半缩醛稳定性]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 章节练习
source_category: 教材课后习题
---
# 题-366: 含氮官能团转化试剂选择

## 题目

In the following scheme

(a) Identify the functional group in each molecule, and

(b) Suggest a reagent or reagents for carrying out each transformation represented by an arrow.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/fe19d20e483e7d251ba392335658967b70e56500bdef1fcc40a1f8ab009b1ac3.jpg]]

**原文题目**：Identify functional groups and suggest reagents for transformations between amines, amides, imines, enamines, and their reduced products.

## 参考答案

**Answer (English)**:

**Primary amines** are transformed into amides by substitution reactions of acid chlorides, and to imines by condensation with an aldehyde in the presence of an acid catalyst. Both amides and imines may be reduced to amines: amides need LiAlH₄, while imines may be reduced by sodium borohydride, sodium cyanoborohydride, or hydrogenation over a palladium catalyst.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/413339b74bfbfdd4c469b5bb58c3aadb0586f28f6fc5a08ae3f3779327615e70.jpg]]

**Secondary amines** react with aldehydes to form enamines, which may be reduced to amines by hydrogenation, or (via their iminium ion tautomer) with sodium borohydride or sodium cyanoborohydride.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/7b952de1a3c1d01a2c7fbd612914c0c9c20772bd23e99e439e6fb5ba2433abd3.jpg]]

**中文解析**：

本题是含氮官能团转化的系统性总结——涵盖胺、酰胺、亚胺、烯胺之间的相互转化及所需试剂。

**伯胺（Primary amine, RNH₂）的转化**：
1. **→ 酰胺**：与酰氯（RCOCl）反应（亲核酰基取代）
2. **→ 亚胺**：与醛/酮在酸催化下缩合（亲核加成→脱水）
3. **← 酰胺还原**：需要LiAlH₄（强还原剂）
4. **← 亚胺还原**：NaBH₄、NaCNBH₃或H₂/Pd催化加氢

**仲胺（Secondary amine, R₂NH）的转化**：
1. **→ 烯胺**：与醛/酮在酸催化下反应（脱水形成C=C-N）
2. **← 烯胺还原**：H₂催化加氢，或通过亚胺离子互变异构体被NaBH₄/NaCNBH₃还原

**关键试剂总结**：

| 转化 | 试剂 | 条件 |
|------|------|------|
| RNH₂ → RCONH₂ | RCOCl（酰氯） | 碱性条件（如Et₃N） |
| RNH₂ → RCH=NR' | R'CHO（醛） | 酸催化（pH 4-5） |
| RCONH₂ → RNH₂ | LiAlH₄ | 无水醚，然后水解 |
| RCH=NR' → RCH₂NHR' | NaBH₄ 或 NaCNBH₃ | 醇溶剂；或H₂/Pd |
| R₂NH → 烯胺 | R'CHO（醛） | 酸催化，脱水 |
| 烯胺 → 胺 | H₂/Pd 或 NaCNBH₃ | 催化加氢或酸性还原 |

> **选择性**：NaCNBH₃在弱酸性条件下选择性还原亚胺/亚胺离子而不还原醛酮——这是还原胺化（reductive amination）的关键试剂。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[亚胺]] | 亚胺的形成和还原——含氮官能团转化的核心枢纽 | 直接 |
| [[烯胺]] | 仲胺与醛酮形成烯胺及其还原 | 直接 |
| [[保护基策略]] | 含氮官能团的选择性转化在合成中的应用 | 间接 |

## 解题思路

1. **读题定位**：题目给出一个转化图，涉及胺、酰胺、亚胺、烯胺等含氮官能团。需要识别每个官能团并建议转化试剂
2. **🔑 关键转换**：理解每个转化的化学本质——酰基取代（胺→酰胺）、缩合（胺→亚胺/烯胺）、还原（亚胺/酰胺→胺）
3. **验证**：检查每个试剂是否能选择性地实现目标转化，而不影响分子中的其他官能团

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 用NaBH₄还原酰胺 | 混淆酰胺和亚胺的还原条件 | 酰胺需要更强的还原剂LiAlH₄；NaBH₄只能还原亚胺/醛酮 | 为什么酰胺比亚胺更难还原？ |
| 伯胺和仲胺与醛反应的产物混淆 | 没有理解N上H的数量对产物的影响 | 伯胺（RNH₂）形成亚胺（C=N）；仲胺（R₂NH）形成烯胺（C=C-N） | 亚胺和烯胺在结构上有什么区别？ |
| NaCNBH₃的选择性不理解 | 不知道NaCNBH₃在酸性条件下的特殊行为 | NaCNBH₃在pH 6-7选择性还原亚胺/亚胺离子，不还原醛酮——这使还原胺化一步完成 | 为什么NaCNBH₃在酸性条件下更活泼？ |