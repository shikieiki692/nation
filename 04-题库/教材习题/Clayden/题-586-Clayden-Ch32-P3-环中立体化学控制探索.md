---
title: 题-586-Clayden-Ch32-P3-环中立体化学控制探索
type: 题目
fidelity: 原书逐字
submodule: 立体选择性
exam_stage: 初赛
source_subject: 有机化学
difficulty: 4
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[立体化学]]"]
tags: [化竞, Clayden, 有机化学, 立体选择性]
updated: 2026-07-25
aliases: [Clayden-Ch32-P3]
source: Clayden Organic Chemistry 2nd Ed. Chapter 32 Problem 3
cross_references: ["[[题-433-Clayden-Ch24-P2-不饱和羰基直接共轭加成区域选择性]]", "[[题-432-Clayden-Ch24-P1-氨基醇制备中区域选择性试剂选择]]", "[[题-292-Clayden-Ch14-P2-旋光值区分]]", "[[题-291-Clayden-Ch14-P1-五个分子手性判断]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 模块习题集
---
# 题-586: 环中立体化学控制探索

## 题目

**【中文】**请评述这一反应序列（见图）中所实现的立体化学控制。

**【原文】**Comment on the control over stereochemistry achieved in this sequence.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/c3d54b84412391e09bfca73ecc3c2c801463f831537180bc16095d09fe096df1.jpg]]

## 参考答案

**Answer (English)**: The reducing agent could attack either side of the ring in the first step but by reacting with the OH group it can deliver hydride intramolecularly from the bottom face. The mesylation does not affect the stereochemistry as no bonds are formed or broken at any of the stereogenic centres.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/d70024d204ebe031add84353c32bbc1f2ecfab6afc615e59143b940a30525026.jpg]]

The reaction with ammonia probably starts with displacement of the primary mesylate and the second displacement is intramolecular. It is also stereospecific as $S_\mathrm{N}2$ reactions must occur with inversion and, fortunately, the amine is on the bottom face.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/687cc3334f6cd170aa4ddcd5ddb3fedb9d8879cffacc2e89fb8de91d0cbade36.jpg]]

**中文解析**：

关键步骤：
1. **分子内氢负离子转移**：还原剂虽然理论上可以从环的两侧进攻，但通过与OH基团反应，可以从底面（bottom face）分子内递送氢负离子，实现高度立体选择性的还原
2. **甲磺酰化**：这一步不影响立体化学，因为没有任何手性中心上的键被形成或断裂。甲磺酰化只是将OH转化为更好的离去基团
3. **氨开环**：氨首先取代伯位甲磺酰氧基（分子间$S_\mathrm{N}2$），然后第二次取代是分子内的。由于$S_\mathrm{N}2$反应必须发生构型翻转，且胺在底面，因此反应是立体专一性的

> **核心概念**：分子内反应（如氢负离子递送和胺的分子内关环）可以实现极高的立体选择性，因为反应基团的空间关系被预先固定。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[立体化学]] | 分子内氢负离子递送的立体选择性 | 直接 |
| [[立体选择性]] | $S_\mathrm{N}2$构型翻转在环状体系中的应用 | 直接 |
| [[构象分析]] | 环的构象控制反应面选择 | 间接 |

## 解题思路

1. **读题定位**：多步反应序列的立体化学控制——识别关键步骤为分子内还原、甲磺酰化和胺关环
2. **关键转换**：分子内氢负离子从底面递送→甲磺酰化（不影响手性中心）→氨先取代伯位，再分子内$S_\mathrm{N}2$关环（构型翻转）
3. **验证**：检查最终产物的两个手性中心均来自立体选择性/立体专一性反应

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 认为甲磺酰化改变立体化学 | 不理解反应本质 | 甲磺酰化只涉及O-H键断裂，不影响C手性中心 | 甲磺酰化后手性中心的键发生了变化吗？ |
| 忽略分子内反应的优势 | 用分子间反应理解 | 分子内递送氢负离子因为两个基团被固定，选择性极高 | 分子内vs分子间反应的速率差异有多大？ |
| 认为氨的两次取代都是分子间 | 没有考虑关环 | 第二次取代是分子内的，受立体化学控制 | $S_\mathrm{N}2$反应的构型翻转规律是什么？ |