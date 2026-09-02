---
title: 题-289-Clayden-Ch9-P7-Br-Li交换选择性分析
type: 题目
fidelity: 原书逐字
submodule: 有机金属试剂
exam_stage: 初赛
source_subject: 有机化学
difficulty: 3
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[有机锂试剂]]", "[[卤素-金属交换]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch9-P7]
source: Clayden Organic Chemistry 2nd Ed. Chapter 9 Problem 7
cross_references: ["[[题-284-Clayden-Ch9-P2-有机金属反应产物预测]]", "[[题-287-Clayden-Ch9-P5-Biperidin结构预测和Procyclidine合成]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 章节练习
---
# 题-289: Br/Li 交换选择性分析

## 题目

Why is it possible to make the lithium derivative A by Br/Li exchange, but not the lithium derivative B?

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/03ecc795012228d55ab0c4e43ecf1dcc6d7b583d48cfb7c154662d029b6fcacd.jpg]]

**原文题目**：为什么可以通过 Br/Li 交换制备锂衍生物 A，却不能制备锂衍生物 B？

## 参考答案

**Answer (English)**: The first example is a vinyl bromide and vinyl (sp²) carbanions are more stable than saturated (sp³) carbanions because of the greater s-character in the C–Li bond. The second example is saturated, like BuLi, but it is a tertiary alkyl bromide. The t-alkyl carbanion would be less stable than the primary one and its lithium derivative less stable than BuLi, so it is not formed.

**中文解析**：

关键分析：
1. **化合物 A（乙烯基溴化物 → 乙烯基锂）**：乙烯基溴化物的碳为 sp² 杂化，形成的乙烯基碳负离子（sp² carbanion）比饱和碳负离子（sp³）更稳定，因为 sp² 轨道中 s 成分更高（33% vs 25%），电子更靠近碳核，能量更低。Br/Li 交换可以进行
2. **化合物 B（叔烷基溴化物）**：叔丁基溴化物的碳为 sp³ 杂化，形成的叔碳负离子（tertiary carbanion）比伯碳负离子更不稳定（烷基的给电子诱导效应增加了碳上的电子密度，使碳负离子更不稳定）。叔碳负离子的稳定性低于 BuLi 中的伯碳负离子，因此交换反应在热力学上不利
3. **核心原则**：Br/Li 交换的驱动力是生成更稳定的碳负离子。如果产物碳负离子不如反应物（BuLi 中的丁基碳负离子）稳定，交换不会发生

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[有机锂试剂]] | Br/Li 交换的条件和碳负离子稳定性 | 直接 |
| [[卤素-金属交换]] | 卤素-金属交换的热力学驱动力 | 直接 |
| [[碳负离子]] | sp² vs sp³ 碳负离子的稳定性比较 | 间接 |

## 解题思路

1. **读题定位**：比较两个 Br/Li 交换反应的可行性——A 成功，B 失败。需要从碳负离子稳定性角度解释
2. **🔑 关键转换**：Br/Li 交换的热力学要求：产物碳负离子必须比反应物（BuLi 中的伯碳负离子）更稳定。A：sp² 碳负离子 > sp³ 伯碳负离子（可行）；B：叔碳负离子 < 伯碳负离子（不可行）
3. **验证**：检查杂化类型（sp² vs sp³）和取代程度（伯 vs 叔）对碳负离子稳定性的影响，与实验结果一致

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 认为 Br/Li 交换只取决于 C-Br 键强度 | 忽略了碳负离子稳定性 | 交换的驱动力是碳负离子稳定性，不是键能 | 为什么碘代烃最容易发生 Br/Li 交换？ |
| 混淆碳正离子和碳负离子的稳定性规律 | 碳正离子：叔 > 伯；碳负离子：伯 > 叔 | 碳负离子稳定性与碳正离子恰好相反 | 为什么烷基给电子效应对碳负离子不利？ |
| 忽略杂化对碳负离子的影响 | 只考虑了取代效应 | sp² 碳负离子因 s 成分高而更稳定 | sp 碳负离子比 sp² 更稳定吗？ |