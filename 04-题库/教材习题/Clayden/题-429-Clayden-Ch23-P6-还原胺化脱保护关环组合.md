---
title: 题-429-Clayden-Ch23-P6-还原胺化脱保护关环组合
type: 题目
fidelity: 原书逐字
submodule: 化学选择性与保护基
exam_stage: 初赛
source_subject: 有机化学
difficulty: 4
question_type: [简答]
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[保护基]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch23-P6]
source: Clayden Organic Chemistry 2nd Ed. Chapter 23 Problem 6
cross_references: ["[[题-477-Clayden-Ch27-P1-分子内硫叶立德共轭加成环丙烷化]]", "[[题-478-Clayden-Ch27-P2-硫叶立德化学区域和立体化学]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 模块习题集
source_category: 教材课后习题
---
# 题-429: 还原胺化+脱保护+关环组合

## 题目

**【中文】**为什么这里的还原胺化生成的是这个特定的胺（见图）？

**【原文】**Why is this particular amine formed by reductive amination here?

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/53d979ad933c25e0e0c51b63ea201954325b3c1d558319f0b7046181a42ac42f.jpg]]

## 参考答案

**Answer (English)**: The two acetals will be hydrolysed at pH 5.5 to give the amine a choice between cyclization to one or other of the two aldehydes:

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/a588fc8ecf196558f3b2a38df1f54ba6fba9f9c36fbacd839599d2741623fa4c.jpg]]

Cyclization to a five-membered ring is preferred to cyclization to a (strained) four-membered ring so reductive amination occurs to the right and not to the left (as drawn). Cyanoborohydride is stable under the weakly acidic conditions and does not reduce the remaining aldehyde.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/4d31f084731631dee2313090bc085a259d8b9ca92eab6ebfe6be8a3428ac8d71.jpg]]

This problem is based on work by G. W. Gribble and R. M. Soll, J. Org. Chem., 1981, 46, 2433.

**中文解析**：

关键要点：
1. **缩醛在pH 5.5水解**：两个缩醛在弱酸性条件下选择性水解，释放两个醛基
2. **五元环vs四元环**：胺可以选择进攻两个醛中的任一个——进攻右边的醛形成五元环（稳定），进攻左边的形成四元环（张力大）
3. **动力学和热力学均有利**：五元环形成更快（动力学有利）且更稳定（热力学有利）
4. **氰基硼氢化钠的选择性**：NaBH₃CN在弱酸性条件下稳定，只还原亚胺（C=N）而不还原醛（C=O）

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[保护基]] | 缩醛在特定pH下选择性水解 | 直接 |
| [[还原胺化]] | 胺+醛→亚胺→还原的串联过程 | 直接 |
| [[亚胺]] | 亚胺的形成和还原机理 | 直接 |
| [[环化反应]] | 五元环vs四元环的形成选择性 | 间接 |

## 解题思路

1. **读题定位**：题目问为什么还原胺化得到特定的胺——核心是理解缩醛水解和环化选择性
2. **🔑 关键转换**：两个缩醛在pH 5.5水解→胺面临两个醛→五元环优先于四元环→还原胺化发生在右侧→氰基硼氢化钠选择性还原亚胺
3. **验证**：检查环大小、还原选择性和最终产物结构是否一致

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 不理解为什么五元环优先 | 不了解环张力对环化的影响 | 五元环无张力，四元环有显著角张力 | 五元环和四元环的张力差有多大？ |
| 混淆NaBH₃CN和NaBH₄ | 不了解氰基硼氢化钠的特殊性 | NaBH₃CN在酸性条件下稳定，只还原亚胺不还原醛 | 为什么氰基硼氢化钠比NaBH₄选择性更好？ |
| 忽略pH控制的作用 | 没有理解弱酸性条件的意义 | pH 5.5既能水解缩醛又不会过度质子化胺 | 如果pH太低会发生什么？ |