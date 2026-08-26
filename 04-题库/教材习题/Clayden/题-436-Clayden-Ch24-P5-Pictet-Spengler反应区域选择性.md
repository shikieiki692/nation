---
title: 题-436-Clayden-Ch24-P5-Pictet-Spengler反应区域选择性
type: 题目
fidelity: 原书逐字
submodule: 区域选择性
exam_stage: 初赛
subject: 有机化学
difficulty: 4
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[区域选择性]]"]
tags: [化竞, Clayden, 有机化学, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch24-P5]
source: Clayden Organic Chemistry 2nd Ed. Chapter 24 Problem 5
cross_references: ["[[题-609-Clayden-Ch36-P2-Beckmann重排立体化学和机理]]", "[[题-291-Clayden-Ch14-P1-五个分子手性判断]]", "[[题-292-Clayden-Ch14-P2-旋光值区分]]", "[[题-608-Clayden-Ch36-P1-原子编号追踪重排]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 模块习题集
---
# 题-436: Pictet-Spengler反应区域选择性

## 题目

Comment on the regioselectivity and chemoselectivity of the reactions shown below.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/bbbdbe357b1de26b49f187cea4375bead4a29724689cd43aa5f67378ff598c90.jpg]]

**原文题目**：评论下列反应的区域选择性和化学选择性。

## 参考答案

**Answer (English)**:

The reaction of an aldehyde with an amine gives an imine, and in acid (HCl), protonation gives an iminium ion, the electrophile that attacks the aromatic ring. The iminium ion is tethered to the ring, so it has only two choices of reaction site, since it can't reach any further than the positions ortho to the tether. The one it chooses is the less hindered. It is also para to an electron-donating methoxy group, so the reaction works well.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/20d27f40415dd15ae86701a141138580197287adccae706aec75218f42bfb420.jpg]]

In the second case, there is only one methoxy group, and both the positions ortho to the tether are meta to it, where it can't activate substitution. The positions ortho to itself, where it can activate, are too far away for the iminium to reach, so no substitution takes place. Presumably the iminium ion forms, but it is just hydrolysed back to the aldehyde.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/751320004f19806bd4bdd9694b2a352a0d1e7ea7ad6864991507a8121f1063b2.jpg]]

This reaction is a useful way of making some important alkaloid natural products (and indeed it mimics the way nature makes them). It is sometimes known as the 'Pictet-Spengler reaction'.

**中文解析**：

Pictet-Spengler反应是合成含氮杂环（特别是异喹啉类生物碱）的重要方法：

**第一个反应（成功）**：
1. **化学选择性**：醛与胺反应生成亚胺（imine），在酸性条件（HCl）下质子化生成亚胺离子（iminium ion）——这是真正的亲电体
2. **区域选择性**：亚胺离子被"系链"（tethered）连接在芳环上，只能到达连接点的两个邻位
3. **位阻选择性**：两个可及位点中，选择了位阻较小的那个
4. **电子效应**：该位置恰好对位于给电子的甲氧基——双重有利

**第二个反应（失败）**：
1. 甲氧基只有一个，且连接点的两个邻位都处于甲氧基的间位
2. 甲氧基的邻/对位定位效应无法激活间位位置
3. 甲氧基的邻位虽然被活化，但距离太远，亚胺离子的系链够不到
4. 结果：亚胺离子形成后被水解回醛——没有发生环化

**核心教训**：Pictet-Spengler反应的成功需要两个条件同时满足——(1) 反应位点在亚胺离子的可及范围内；(2) 该位点被活化基团活化。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[区域选择性]] | 分子内亲电取代的位点选择 | 直接 |
| [[杂环化合物]] | Pictet-Spengler反应合成异喹啉环系 | 直接 |
| [[芳香亲电取代]] | 亚胺离子作为亲电体的分子内环化 | 直接 |
| [[亚胺]] | 醛+胺→亚胺→亚胺离子的形成 | 间接 |

## 解题思路

1. **读题定位**：两个底物结构相似但甲氧基数量和位置不同，一个成功环化，一个不成功
2. **🔑 关键转换**：识别反应本质——分子内亲电芳香取代。亚胺离子是亲电体，芳环是亲核体。成功需要：可达位点 + 该位点被活化
3. **验证**：第一个反应中可达位点对位于OMe（被活化）✓；第二个反应中可达位点位于OMe的间位（未被活化）✗

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 认为第二个反应只是反应慢 | 没有认识到间位无法被甲氧基活化 | 不是速度问题，而是反应在热力学上不有利——亲电体无法到达被活化的位点 | 为什么甲氧基不能活化间位？ |
| 混淆亚胺和亚胺离子 | 没有理解酸催化的必要性 | 中性亚胺亲电性不够强；质子化后的亚胺离子才是有效的亲电体 | 为什么需要酸性条件？ |
| 忽略系链的空间限制 | 认为分子内反应总是比分子间有利 | 系链的长度限制了可达位点；不是所有环上位置都能被分子内亲电体到达 | 如果增加系链长度会怎样？ |
| 不理解Pictet-Spengler反应的生物意义 | 只把它当作普通有机反应 | 该反应模拟了生物体内生物碱的生物合成途径 | 哪些天然生物碱通过类似途径合成？ |