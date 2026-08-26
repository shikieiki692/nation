---
title: 题-532-Clayden-Ch41-P9-可靠催化反应识别
type: 题目
fidelity: 原书逐字
submodule: 不对称合成
exam_stage: 决赛
subject: 有机化学
difficulty: 3
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[不对称催化还原]]", "[[不对称环氧化]]"]
tags: [化竞, Clayden, 有机化学, 不对称催化]
updated: 2026-07-25
aliases: [Clayden-Ch41-P9]
source: Clayden Organic Chemistry 2nd Ed. Chapter 41 Problem 9
cross_references: ["[[题-291-Clayden-Ch14-P1-五个分子手性判断]]", "[[题-292-Clayden-Ch14-P2-旋光值区分]]", "[[题-478-Clayden-Ch27-P2-硫叶立德化学区域和立体化学]]", "[[题-477-Clayden-Ch27-P1-分子内硫叶立德共轭加成环丙烷化]]"]
module: 有机化学
status: 已填充
---
# 题-532: 可靠催化反应识别

## 题目

Propose catalytic methods for the asymmetric synthesis of these four precursors to drug molecules.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/83e2e611dae2672f4ecf7d4311ce55dcfbeb15990744e7316421c7f9db8aa8ac.jpg]]

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/904e669e76071183d0eb775e4f877a77b01881bb9ba82731f2f7508227e99a6e.jpg]]

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/85d98a180cbeede1d549fa42fca83f5b084bae27ce68029ebb4ee45ccf12caa4.jpg]]  
precursor to AZT

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/42bf1a4239365b2a50481df63b90ea93c780a647065f6104322688fc7bc90588.jpg]]  
precursor to indicine

**原文题目**：Propose catalytic methods for the asymmetric synthesis of these four precursors to drug molecules.

## 参考答案

**Answer (English)**: The sertraline precursor is a chiral alcohol with the stereogenic centre adjacent to an aromatic ring. An obvious approach is to make the hydroxyl group by asymmetric reduction of the corresponding ketone. CBS reduction is a possibility, as is a ruthenium-catalysed hydrogenation using the ligand TsDPEN.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/fb435fbb6dbcc9f607956615edeea7310355afb776188d8aee5b504048572578.jpg]]

The second compound is a chiral sulfide. Although there are direct asymmetric ways of making chiral sulfur compounds, a reliable approach to sulfides is to use SN2 substitution of a more readily made chiral precursor, because a thiolate is usually a good nucleophile. The SN2 reaction goes with inversion, so we need the chiral alcohol shown below, converted to a derivative (such as a tosylate) capable of undergoing substitution.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/024e83325656d679480f328d1bbc4e7fec5b8d9195b1a887c2a4da699459f873.jpg]]

The third compound contains a 1,2,3-trifunctionalized arrangement that should prompt you to think of asymmetric epoxidation. Azide is a good nucleophile for opening epoxides, so we can start with the allylic alcohol shown here, carry out an asymmetric epoxidation, and convert to the target with inversion of configuration.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/3af4de88d0a5bc8d1b674d3ec270e95010131415cd025c17da0891564700d89b.jpg]]

The final compound is a diol, so asymmetric dihydroxylation is a possible approach. The precursor is a rather unreactive alkene, but asymmetric dihydroxylation is a versatile reaction which can still perform well on challenging substrates.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/dfd57905f46014bca656556039f98dc3b5a84fc143021746be477427d6788dd4.jpg]]

**中文解析**：

**整体策略分析**：
本题要求为四个药物前体设计催化不对称合成方法。核心能力是：(1) 识别目标分子的结构特征；(2) 将结构特征匹配到可靠的催化不对称反应；(3) 理解每个催化反应的底物要求和局限性。题目特别强调"catalytic methods"——催化量的手性源即可，不需要化学计量的手性助剂。

**四个目标分子的催化策略分析**：

**1. 舍曲林（Sertraline）前体——手性仲醇**：
- 结构特征：手性中心在苯环旁边，是一个手性仲醇
- 催化策略：**不对称还原相应的酮**
- 方法选择：
  - **CBS还原**：噁唑硼烷催化剂 + BH₃，高ee值
  - **Ru-TsDPEN催化氢化**：Noyori型不对称氢化，TsDPEN作为手性配体
- 教学要点：不需要记住哪种对映体的配体给出哪种产物——重要的是识别出"手性仲醇→不对称还原"这一匹配

**2. 手性硫化物**：
- 结构特征：手性中心在硫原子上（或邻近硫）
- 催化策略：**间接法**——通过手性醇的SN2取代构建C-S键
- 路线：(a) 不对称催化还原→手性醇；(b) 转化为甲磺酸酯/对甲苯磺酸酯（好的离去基团）；(c) 硫醇盐亲核取代（SN2，构型翻转）
- 为什么选间接法：硫醇盐是优秀的亲核试剂，SN2反应高效；直接不对称构建C-S键的方法不如间接法可靠
- 注意消除副反应：硫醇盐是好的亲核试剂但碱性不强，消除不严重

**3. AZT前体——1,2,3-三官能团化化合物**：
- 结构特征：相邻碳上分别有OH、N₃（叠氮）和另一个官能团（1,2,3-三官能团化）
- 催化策略：**Sharpless不对称环氧化** + 叠氮开环
- 路线：(a) 从烯丙醇出发；(b) Sharpless不对称环氧化→手性环氧化物；(c) 叠氮化物亲核开环（构型翻转）→目标产物
- 为什么想到环氧化：1,2,3-三官能团化是环氧化-开环的经典产物模式

**4. Indicine前体——邻二醇**：
- 结构特征：相邻碳上的两个羟基（1,2-二醇）
- 催化策略：**Sharpless不对称双羟化（AD）**
- 路线：从烯烃出发，Sharpless AD反应一步构建邻二醇
- 注意：底物是一个不太活泼的烯烃，但Sharpless AD的适用范围很广，对这类底物仍然有效
- 两种手性配体（(DHQD)₂PHAL和(DHQ)₂PHAL）可分别得到两种对映体

**关键教学要点**：
- 催化不对称反应的核心优势：只需要催化量的手性源（经济性高）
- "结构特征→方法匹配"是不对称合成设计的基本功
- 每个催化方法都有其最佳适用底物范围

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[不对称催化还原]] | CBS还原和Noyori氢化制备手性仲醇 | 直接 |
| [[不对称环氧化]] | Sharpless环氧化构建1,2,3-三官能团化 | 直接 |
| [[不对称双羟化]] | Sharpless AD构建邻二醇 | 直接 |
| [[金属有机化学]] | Ru催化氢化、Ti催化环氧化 | 间接 |

## 解题思路

1. **读题定位**：题目要求提出"催化"方法合成四个药物前体。关键词：催化、不对称合成、药物前体
2. **🔑 关键转换**：(a) 手性仲醇→CBS/Noyori不对称还原；(b) 手性硫化物→间接法（手性醇→SN2取代）；(c) 1,2,3-三官能团化→Sharpless环氧化+叠氮开环；(d) 邻二醇→Sharpless不对称双羟化
3. **验证**：每个方案是否使用催化量的手性源？底物是否可得？产物立体化学是否可控？

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 为所有目标都选同一种催化方法 | 没有分析不同结构特征 | 不同结构特征匹配不同催化方法：仲醇→不对称还原，邻二醇→AD，三官能团→环氧化+开环 | 为什么手性硫化物不选直接不对称方法？ |
| 混淆Sharpless环氧化和双羟化 | 对两类反应的产物不熟 | 环氧化→环氧化物（三元环醚），双羟化→邻二醇 | Sharpless环氧化的底物要求是什么？ |
| 不知道间接法构建C-S键 | 认为必须直接不对称构建 | 手性醇→磺酸酯→SN2取代（硫醇盐亲核），构型翻转可预测 | SN2反应中构型如何翻转？ |
| 担心底物不反应 | 对催化反应的适用范围不熟 | Sharpless AD对各种烯烃底物都有良好适用性，包括不太活泼的烯烃 | 什么因素影响AD反应的ee值？ |