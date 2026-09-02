---
title: 题-432-Clayden-Ch24-P1-氨基醇制备中区域选择性试剂选择
type: 题目
fidelity: 原书逐字
submodule: 区域选择性
exam_stage: 初赛
source_subject: 有机化学
difficulty: 3
teaching_level: 巩固
syllabus_codes: ["21"]
knowledge_points: ["[[区域选择性]]"]
tags: [化竞, Clayden, 有机化学, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch24-P1]
source: Clayden Organic Chemistry 2nd Ed. Chapter 24 Problem 1
cross_references: ["[[题-291-Clayden-Ch14-P1-五个分子手性判断]]", "[[题-608-Clayden-Ch36-P1-原子编号追踪重排]]", "[[题-609-Clayden-Ch36-P2-Beckmann重排立体化学和机理]]", "[[题-292-Clayden-Ch14-P2-旋光值区分]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 章节练习
---
# 题-432: 氨基醇制备中区域选择性试剂选择

## 题目

Two routes are proposed for the preparation of this amino-alcohol. Which do you think is more likely to succeed and why?

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/cf671bbed8e39dcb0349e0f931f870627ed41387c26e4c50ca6533682d31a5cb.jpg]]

**原文题目**：给出两条制备该氨基醇的路线，哪一条更可能成功？为什么？

## 参考答案

**Answer (English)**: Either route might give the product but enals are more likely to undergo direct addition to the carbonyl group rather than conjugate addition while conjugated esters are better at conjugate addition. So the ester is probably better.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/b12b0c41fae4d42858fae86b34a26e5c4205f55ff48e43ad20872869052c4d37.jpg]]

**中文解析**：

两条路线的关键区别在于亲电底物的类型：

1. **路线一（α,β-不饱和醛）**：α,β-不饱和醛（enal）中的C=C双键与C=O共轭，但醛基的羰基碳亲电性很强。胺作为亲核试剂更容易直接进攻C=O（1,2-加成），而不是进行共轭加成（1,4-加成）。因此，预期的共轭加成产物产率可能很低。

2. **路线二（α,β-不饱和酯）**：共轭酯的C=C双键虽然同样与C=O共轭，但酯基的羰基碳亲电性较弱（烷氧基的给电子共轭效应降低了羰基碳的正电性）。胺更容易进攻β-碳（共轭加成），而不是羰基碳（直接加成）。

**核心结论**：共轭酯比共轭醛更有利于共轭加成，因为酯基的亲电性较弱，抑制了1,2-直接加成的竞争反应。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[区域选择性]] | 1,2-加成 vs 1,4-加成的选择 | 直接 |
| [[共轭加成]] | α,β-不饱和羰基化合物的共轭加成 | 直接 |
| [[Markovnikov规则]] | 加成反应中的区域选择性规律 | 间接 |
| [[醛酮]] | 醛基与酯基对亲核进攻的不同反应性 | 间接 |

## 解题思路

1. **读题定位**：题目要求比较两条路线的优劣——涉及α,β-不饱和羰基化合物与胺的反应区域选择性
2. **🔑 关键转换**：识别1,2-加成（直接加成到C=O）和1,4-加成（共轭加成到β-碳）的竞争。醛基C=O亲电性强→倾向1,2-加成；酯基C=O亲电性弱→倾向1,4-加成
3. **验证**：产物要求胺连接在β-碳上（共轭加成产物），因此酯路线更有利

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 认为两条路线都能给出好结果 | 忽略了醛和酯在亲电性上的差异 | 醛的C=O更强亲电，胺优先进攻C=O而非β-碳 | 为什么醛比酯更容易发生1,2-加成？ |
| 混淆1,2-和1,4-加成产物的结构 | 没有区分胺连接在不同碳上的产物 | 1,2-加成：胺连接在羰基碳上；1,4-加成：胺连接在β-碳上 | 如何从产物结构判断加成模式？ |
| 认为胺总是进行共轭加成 | 胺的亲核性较强，可以进攻硬亲电位点 | 胺既可以进行1,2-加成也可以1,4-加成，取决于底物 | 什么样的亲核试剂倾向于共轭加成？ |