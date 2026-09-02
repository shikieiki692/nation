---
title: 题-458-Clayden-Ch28-P4-需要选择性的合成设计
type: 题目
fidelity: 原书逐字
submodule: 逆合成分析
exam_stage: 初赛
source_subject: 有机化学
difficulty: 3
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[逆合成分析]]"]
tags: [化竞, Clayden, 有机化学, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch28-P4]
source: Clayden Organic Chemistry 2nd Ed. Chapter 28 Problem 4
cross_references: ["[[题-292-Clayden-Ch14-P2-旋光值区分]]", "[[题-291-Clayden-Ch14-P1-五个分子手性判断]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 章节练习
---
# 题-458: 需要选择性的合成设计

## 题目

Propose syntheses of these two compounds, explaining your choice of reagents and how any selectivity is achieved.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/00828cab6c9c12d6c58ead94862ad1305b96483316861f4a317a75c2fb7186e8.jpg]]

**原文题目**：建议合成这两种化合物的路线，解释试剂选择以及如何实现选择性。

## 参考答案

**Answer (English)**:

**Compound 1 (enone)**: This is an alpha,beta-unsaturated carbonyl compound - the product of an aldol reaction. Disconnect the alkene and write a new carbonyl group. We need a crossed aldol reaction between two ketones so we also need chemoselectivity and regioselectivity. Use a lithium enolate, silyl enol ether, or beta-ketoester.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/2c08985ff21e1ccc941c5b5420d71fde458f07c0959e131a40fe9de2dd5a24fc.jpg]]

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/de8bfcf84839b0370222dcc9564d5db079ca2e54804eef6942f9dea48027d548.jpg]]

**Compound 2 (lactone)**: Disconnect the structural C-O bond first to see the carbon skeleton. We have a 1,5-relationship between the functional groups so we need conjugate addition. Change the alcohol into a ketone, and the acid group to an ester.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/3ab4fff2b9f5421d63167a135e872585f884094ad57edfca5d2729a232f4879b.jpg]]

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/24b0c2e6e78f28772d8de37b17662de67185fb8237ddf196f007c30ce558623e.jpg]]

One possibility: add malonate to the unsaturated ketone (aldol dimer of acetone). Reduce the ketone, expect cyclization to be spontaneous, and decarboxylate.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/8f7934a3b4d80285f513864e278e8634ade770a5e869c60752fa8f14c74822b2.jpg]]

**中文解析**：

**化合物1（烯酮）**：
- 识别：alpha,beta-不饱和羰基化合物是Aldol缩合产物
- 切断：断开C=C双键，还原为两个羰基化合物
- 选择性需求：交叉Aldol反应需要化学选择性和区域选择性
- 解决方案：用锂烯醇负离子、硅烯醇醚或beta-酮酯作为特定烯醇等价物

**化合物2（内酯）**：
- 先断开内酯C-O键揭示碳骨架
- 1,5-关系→需要共轭加成
- 化学选择性：一个C=O被还原，另一个保留→用醛和酯区分
- 具体路线：丙酮Aldol二聚体 + 丙二酸酯共轭加成→还原→自发环化→脱羧→内酯

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[逆合成分析]] | 识别产物类型选择切断策略 | 直接 |
| [[化学选择性]] | 交叉Aldol和选择性还原 | 直接 |
| [[合成设计]] | 利用特定烯醇等价物实现选择性 | 直接 |
| [[Aldol缩合]] | alpha,beta-不饱和羰基的逆合成 | 直接 |

## 解题思路

1. 读题定位：两个需要选择性控制的合成目标
2. 关键转换：烯酮→Aldol产物→断开C=C→特定烯醇等价物；内酯→1,5-关系→共轭加成+选择性还原
3. 验证：检查每步反应的选择性是否能实现

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 用简单Aldol做交叉Aldol | 会得到混合物 | 必须用特定烯醇等价物控制选择性 | 什么是特定烯醇等价物？ |
| 不识别内酯的1,5-关系 | 没有先断开内酯C-O键 | 先断开内酯再分析碳骨架 | 内酯在逆合成分析中如何处理？ |
| 用LiAlH4同时还原两个C=O | 无法选择性还原 | 用不同类型的C=O或选择性还原剂 | 如何区分醛和酮的还原？ |