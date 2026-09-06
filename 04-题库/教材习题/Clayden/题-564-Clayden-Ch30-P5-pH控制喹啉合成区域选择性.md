---
title: 题-564-Clayden-Ch30-P5-pH控制喹啉合成区域选择性
type: 题目
fidelity: 原书逐字
submodule: 杂环合成
exam_stage: 初赛
source_subject: 有机化学
difficulty: 4
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[杂环合成]]"]
tags: [化竞, Clayden, 有机化学, 杂环合成]
updated: 2026-07-25
aliases: [Clayden-Ch30-P5]
source: Clayden Organic Chemistry 2nd Ed. Chapter 30 Problem 5
cross_references: ["[[题-550-Clayden-Ch29-P1-杂环上亲电亲核取代产物预测]]", "[[题-551-Clayden-Ch29-P2-烷基吡啶LHMDS侧链延伸]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 模块习题集
source_category: 教材课后习题
source_grade: B
---
# 题-564: pH控制喹啉合成区域选择性

## 题目

**【中文】**请解释为什么由相同原料出发的图中所示两个喹啉（quinoline）合成会（主要）给出不同的产物。

**【原文】**Explain why these two quinoline syntheses from the same starting materials give (mainly) different products.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/3954533357ec146428360007de618034de7d57aa0b33be757b151b9cd2d4b703.jpg]]

## 参考答案

**Answer (English)**: You have a choice here: either you first form an enol(ate) from butanone and do an aldol reaction with the aromatic ketone or you first make an imine and then form enamines from that. In either case, you would expect enol or enamine formation on the more substituted side in acid but the less substituted side in base.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/3057691438ee8568fd926f02a3bd1c1039819510d1890f03a46a8e48b57d97f3.jpg]]

> This selective route to quinolines by the Friedländer synthesis was discovered by E. A. Fehnel, J. Org. Chem., 1966, 31, 2899.

**中文解析**：

关键步骤：
1. **酸性条件**（产物A为主）：先形成亚胺（胺+酮缩合），然后在酸催化下烯胺化——酸性条件有利于在**取代较多**的α位形成烯胺/烯醇，因为更稳定的碳正离子中间体
2. **碱性条件**（产物B为主）：先形成烯醇负离子（碱夺取α-H），然后与芳香酮做Aldol反应——碱性条件有利于在**取代较少**的α位去质子化（动力学控制，位阻更小）
3. **区域选择性翻转**：同一底物，通过pH控制可以翻转区域选择性——酸性→多取代烯胺；碱性→少取代烯醇负离子

> **核心概念**：Friedländer喹啉合成中，pH通过控制烯胺/烯醇的形成位点来决定区域选择性。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[杂环合成]] | Friedländer喹啉合成的区域选择性控制 | 直接 |
| [[区域选择性]] | 酸碱条件对烯胺/烯醇形成位点的翻转控制 | 直接 |
| [[烯胺]] | 酸催化烯胺形成倾向于多取代位点 | 直接 |
| [[烯醇负离子]] | 碱催化烯醇负离子形成倾向于少取代位点 | 直接 |

## 解题思路

1. **读题定位**：相同底物（2-氨基苯甲醛+丁酮）在不同pH下给出不同喹啉产物——识别为pH控制的区域选择性问题
2. **🔑 关键转换**：酸性→亚胺→多取代烯胺→Aldol环化→产物A；碱性→少取代烯醇负离子→Aldol→亚胺→产物B
3. **验证**：检查两个产物中丁酮残基的连接方向——一个连在多取代端，一个连在少取代端

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 酸性和碱性条件下产物相同 | 没理解pH控制区域选择性的原理 | 酸性→热力学控制（多取代），碱性→动力学控制（少取代） | 为什么酸性有利于多取代位点？ |
| 混淆亚胺和烯胺的形成顺序 | 不清楚反应的先后 | 酸性：先亚胺→再烯胺；碱性：先烯醇负离子→再Aldol | 亚胺和烯胺有什么区别？ |
| 画错Aldol环化方向 | 没有追踪碳骨架连接 | 仔细追踪丁酮的C1和C2分别连接到喹啉环的哪个位置 | 如何快速判断Aldol的连接方式？ |