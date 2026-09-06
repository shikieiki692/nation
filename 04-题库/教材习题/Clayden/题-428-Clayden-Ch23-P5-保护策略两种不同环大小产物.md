---
title: 题-428-Clayden-Ch23-P5-保护策略两种不同环大小产物
type: 题目
fidelity: 原书逐字
submodule: 化学选择性与保护基
exam_stage: 初赛
source_subject: 有机化学
difficulty: 4
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[保护基]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch23-P5]
source: Clayden Organic Chemistry 2nd Ed. Chapter 23 Problem 5
cross_references: ["[[题-477-Clayden-Ch27-P1-分子内硫叶立德共轭加成环丙烷化]]", "[[题-478-Clayden-Ch27-P2-硫叶立德化学区域和立体化学]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 模块习题集
source_category: 教材课后习题
---
# 题-428: 保护策略——两种不同环大小产物

## 题目

**【中文】**你会如何把这个硝基化合物转化为图中所示的两种产物？请解释各步的先后顺序，特别注意还原步骤。

**【原文】**How would you convert this nitro compound into the two products shown? Explain the order of events with special regard for reduction steps.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/1e7c78a8530919faf130fe16e6f0cf9f993cad9ccb18b56abc2b34f67c64d490.jpg]]

## 参考答案

**Answer (English)**: The nitro group must be reduced to an amino group and cyclized onto the ketone or the carboxylic acid. Reductive amination allows the amine to cyclize onto the more electrophilic ketone (five-membered ring):

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/e35428c3337d76f7ba93308e8b1d46fae72615c5c2eb9475d2d9402cce5a5118.jpg]]

Forming the six-membered ring requires more control. Protection of the ketone (as the acetal) before reduction will give the six-membered cyclic amide. Now the amide carbonyl must be reduced with LiAlH₄ and the ketone deprotected:

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/db8d4b0afcf5abec999df8b2b7fbe42e71e88cb371a9ced541c39a52d698cea7.jpg]]

**中文解析**：

关键要点：
1. **五元环产物**：还原胺化——NO₂→NH₂→NH₂进攻酮（更亲电）→亚胺→还原得五元环胺
2. **六元环产物**：需要更多控制——先保护酮为缩醛→还原NO₂→NH₂进攻CO₂H形成酰胺→LiAlH₄还原酰胺→脱保护得六元环胺
3. **选择性关键**：还原胺化天然选择进攻酮（五元环）；要得到六元环必须保护酮，迫使NH₂进攻CO₂H

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[保护基]] | 缩醛保护酮基以改变环化方向 | 直接 |
| [[化学选择性]] | 还原胺化中酮vs酸的选择性 | 直接 |
| [[逆合成分析]] | 从目标环大小逆推保护策略 | 间接 |
| [[还原胺化]] | NO₂还原→胺→环化→还原的串联反应 | 直接 |

## 解题思路

1. **读题定位**：题目要求从同一原料合成两个不同环大小的产物——核心是通过保护策略控制环化方向
2. **🔑 关键转换**：五元环：还原胺化直接环化到酮；六元环：保护酮→NH₂进攻酸→形成酰胺→还原酰胺→脱保护
3. **验证**：检查每步反应的选择性和保护/脱保护条件是否兼容

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 不理解为什么五元环优先 | 没有考虑动力学vs热力学控制 | 还原胺化中NH₂优先进攻更亲电的酮 | 酮和酸哪个更亲电？ |
| 六元环路线忘记保护 | 没有识别需要改变选择性 | 必须保护酮才能迫使NH₂进攻酸 | 如果不保护酮会发生什么？ |
| LiAlH₄还原酰胺后忘记脱保护 | 步骤遗漏 | 最后需酸性水解脱保护恢复酮 | 酰胺被LiAlH₄还原成什么？ |