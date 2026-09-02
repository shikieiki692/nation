---
title: 题-313-Clayden-Ch17-P4-E1cB机理和绝对立体化学
type: 题目
fidelity: 原书逐字
submodule: 消除反应
exam_stage: 初赛
source_subject: 有机化学
difficulty: 4
teaching_level: 拓展
syllabus_codes: ["3.2"]
knowledge_points: ["[[E1cb反应]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch17-P4]
source: Clayden Organic Chemistry 2nd Ed. Chapter 17 Problem 4
cross_references: ["[[题-307-Clayden-Ch15-P9-两个反应的立体化学]]", "[[题-316-Clayden-Ch17-P7-三个消除反应中烯烃位置]]", "[[题-295-Clayden-Ch14-P5-反应产物手性和对映体纯度]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 模块习题集
---
# 题-313: E1cB机理和绝对立体化学

## 题目

**【中文】**解释这些反应产物中烯烃的位置。起始原料是光学纯的。产物是否也是光学纯的？

**【原文】**
Explain the position of the alkene in the products of these reactions. The starting materials are enantiomerically pure. Are the products also enantiomerically pure?

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/3c7395ff0357434f0be99ee61f163d6cdf83d63002e2b77840a87918b1ac5715.jpg]]

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/cf089cd29c12757ce476b450d7c8041e3876b4f4cb0b9600c71f9134907e322b.jpg]]

## 参考答案

**Answer (English)**:

E1cB reactions are on p. 399 in the textbook.

The first reaction is an E1cB elimination of a β-hydroxy-ketone. The product is still chiral although it has lost one stereogenic centre. The other (quaternary) centre is not affected by the reaction so the product is enantiomerically pure.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/390fddef648230daf823be2dc9e8d4d4609d975a2b2468e4376a41cd5ffc2df2.jpg]]

The second example already has an electron-rich alkene (an enol ether) present in the starting material so this is more of an E1 than an E1cB mechanism. The intermediate is a hemiacetal that hydrolyses to a ketone (p. 224 in the textbook). The product has two chiral centres unaffected by the reaction and is still chiral so it is also enantiomerically pure.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/da854b8b6eddb0aa6157fbe2d7a2ebc37df9243d7100b36680df1cfb55c2431b.jpg]]

**中文解析**：

**E1cB机理详解**

E1cB（消除单分子共轭碱）是一个两步消除机理，与E1和E2都不同。

**E1cB的两个步骤**：

| 步骤 | 过程 | 速率 | 特点 |
|------|------|------|------|
| 1 | 碱夺取α-氢 → 碳负离子 | 快（可逆） | 需要酸性α-氢（邻位C=O活化） |
| 2 | 碳负离子排出离去基团 → 烯烃 | 慢（速率决定步骤） | 离去基团可以是OH⁻（差的离去基团） |

**为什么β-羟基酮走E1cB？**

1. **酸性α-氢**：邻位C=O使α-氢具有酸性（pKa ~20），碱容易夺取
2. **差的离去基团**：OH⁻是差的离去基团，在E2中难以直接消除
3. **碳负离子稳定化**：C=O可以稳定邻位碳负离子（共振）

**E1cB vs E2 vs E1对比**：

| 特征 | E1 | E2 | E1cB |
|------|----|----|------|
| 中间体/过渡态 | 碳阳离子 | 协同过渡态 | 碳负离子 |
| 速率决定步骤 | 碳阳离子形成 | 协同消除 | 离去基团离开 |
| 碱的作用 | 不需要强碱 | 需要强碱 | 需要强碱 |
| 底物要求 | 稳定碳阳离子 | 反式共平面 | 酸性α-氢 |

**绝对立体化学的影响**：

E1cB消除中，**不涉及的手性中心不受影响**：

- 如果分子中有其他手性中心（不在消除位点），它们的构型保持不变
- 消除只影响α和β碳的立体化学
- 产物中远离消除位点的手性中心保持原来的绝对构型

**具体例子**：
- β-羟基酮消除后，如果分子中还有其他手性中心（如季碳），这些中心的构型完全保持
- 半缩醛水解→酮→E1cB消除，其他手性中心不受影响

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| E1cb反应 | E1cB的两步机理 | 直接 |
| [[消除反应]] | E1cB与其他消除机理的区别 | 直接 |
| [[立体电子效应]] | E1cB的立体化学要求 | 间接 |

## 解题思路

1. **读题定位**：β-羟基酮的消除，需要识别E1cB机理
2. **🔑 关键转换**：酸性α-氢 → 碱夺取 → 碳负离子 → 排出OH⁻ → 烯烃；其他手性中心不受影响
3. **验证**：检查α-氢的酸性（邻位C=O活化），确认E1cB的适用性

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 认为所有消除都是E2 | 没有识别E1cB的特殊条件 | β-羟基酮有酸性α-氢+差的离去基团→E1cB | 如何区分E1cB和E2？ |
| 认为消除会影响所有手性中心 | 没有理解E1cB的作用范围 | 只有消除位点的立体化学会改变 | 如何预测E1cB产物的立体化学？ |
| 混淆E1cB和E1 | 没有理解碳负离子vs碳阳离子 | E1cB经过碳负离子，E1经过碳阳离子 | E1cB和E1的速率决定步骤有什么不同？ |