---
title: "题-344-Clayden-Ch7-P9-乙醛水合vsDMF不水合"
type: 题目
fidelity: 原书逐字
submodule: 共轭效应
exam_stage: 初赛
subject: 有机化学
difficulty: 3
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[离域效应]]", "[[共轭效应]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch7-P9]
source: Clayden Organic Chemistry 2nd Ed. Chapter 7 Problem 9
cross_references: ["[[题-266-Clayden-Ch6-P5-茚三酮水合选择性]]", "[[题-338-Clayden-Ch7-P3-胍鎓烯醇盐萘电荷分布]]", "[[题-343-Clayden-Ch7-P8-茚与溴的反应活性]]"]
module: 有机化学
status: 已填充
---
# 题-344: 乙醛水合vs DMF不水合（离域效应）

## 题目

In aqueous solution, acetaldehyde (ethanal) is about 50% hydrated. Draw the structure of the hydrate of acetaldehyde. Under the same conditions, the hydrate of N,N-dimethylformamide is undetectable. Why the difference?

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/e1019b5b3ec60dc934820900b5834fd954154264d3f42f78f7d8c80d52ab9279.jpg]]

**原文题目**：In aqueous solution, acetaldehyde (ethanal) is about 50% hydrated. Draw the structure of the hydrate of acetaldehyde. Under the same conditions, the hydrate of N,N-dimethylformamide is undetectable. Why the difference?

## 参考答案

**Answer (English)**:

As you saw in chapter 6, aldehydes are readily hydrated. For amides, however, there is a price to pay: the delocalization that contributes to the stability of the amide would be lost on hydration, so dimethylformamide is not hydrated in aqueous solution.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/64781fbf7a722764380955ed659b375aa3882cdc2f498a0e719bb960ef76b162.jpg]]

**中文解析**：

关键步骤：
1. **乙醛水合**：乙醛 (CH₃CHO) 的C=O与H₂O发生亲核加成，生成偕二醇（gem-diol）水合物 CH₃CH(OH)₂。平衡约50%水合——说明水合物和醛的稳定性相近
2. **DMF不水合**：N,N-二甲基甲酰胺 (DMF, HCONMe₂) 中，N的孤对电子与C=O形成p-π共轭（酰胺共振），这使得酰胺C=O具有额外的稳定性。水合会破坏这一共轭体系（C从sp²变为sp³），因此水合在热力学上不利
3. **核心差异**：乙醛水合时C=O变为两个C-OH，失去的是普通的双键稳定化能；DMF水合时失去的是酰胺共振能（约80 kJ/mol），代价更大

> **离域效应的反应性影响**：共轭/离域不仅影响分子的稳定性，还直接影响反应平衡。酰胺的高稳定性（源于离域）使其不易发生亲核加成。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[离域效应]] | 酰胺共振对反应平衡的影响 | 直接 |
| [[共轭效应]] | 共轭稳定化能对亲核加成的抑制 | 直接 |
| [[羰基亲核加成]] | 水作为亲核试剂对C=O的加成 | 间接 |

## 解题思路

1. **读题定位**：题目比较乙醛（水合50%）和DMF（不水合）的行为差异——为什么同为羰基化合物，水合倾向相差如此大？
2. **🔑 关键转换**：DMF的酰胺共振（N孤对电子→C=O离域）使C=O异常稳定；水合将C(sp²)变为C(sp³)会完全破坏此共振→水合的热力学代价极高→平衡偏向醛形式
3. **验证**：画出两种水合物结构，比较反应前后的共轭体系：乙醛水合只失去C=O双键；DMF水合失去酰胺共振——后者能量代价大得多

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 认为DMF水合后仍有共振 | 未认识到sp³碳无法维持p轨道重叠 | 水合后C变为sp³杂化，四个键均为σ键，无法与N的孤对电子共轭 | 酰胺中C-N键为什么有部分双键性质？ |
| 认为所有醛酮水合程度相同 | 忽略了取代基对C=O活性的影响 | 不同醛酮的水合程度差异很大：甲醛几乎完全水合，三氯乙醛定量水合，而酮通常几乎不水合 | 为什么三氯乙醛的水合程度比乙醛高？ |
| 混淆动力学和热力学 | 将"不水合"理解为反应速率慢 | DMF不水合是热力学原因（平衡常数极小），不是动力学原因（速率慢） | 如何区分动力学控制和热力学控制？ |