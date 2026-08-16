---
title: 题-528-Clayden-Ch41-P5-简单序列逐步讨论
type: 题目
submodule: 不对称合成
exam_stage: 决赛
subject: 有机化学
difficulty: 3
teaching_level: 巩固
syllabus_codes: ["21"]
knowledge_points: ["[[不对称合成]]", "[[立体化学基础]]"]
tags: [化竞, Clayden, 有机化学, 不对称合成]
updated: 2026-07-25
aliases: [Clayden-Ch41-P5]
source: Clayden Organic Chemistry 2nd Ed. Chapter 41 Problem 5
cross_references: ["[[题-478-Clayden-Ch27-P2-硫叶立德化学区域和立体化学]]", "[[题-291-Clayden-Ch14-P1-五个分子手性判断]]", "[[题-477-Clayden-Ch27-P1-分子内硫叶立德共轭加成环丙烷化]]", "[[题-292-Clayden-Ch14-P2-旋光值区分]]"]
module: 有机化学
status: 已填充
---
# 题-528: 简单序列逐步讨论

## 题目

This reaction sequence can be used to make enantiomerically enriched amino acids. Which compound is the origin of the chirality and how is it made? Suggest why this particular enantiomer of the product amino acid might be formed. Suggest reagents for the last stages of the process. Would the enantiomerically enriched starting material be recovered?

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/3f0999c90c261ca36a937ecd3095c9dbb9a29eaa63afee94e2cef05b10f2ea5e.jpg]]

**原文题目**：This reaction sequence can be used to make enantiomerically enriched amino acids. Which compound is the origin of the chirality and how is it made? Suggest why this particular enantiomer of the product amino acid might be formed. Suggest reagents for the last stages of the process. Would the enantiomerically enriched starting material be recovered?

## 参考答案

**Answer (English)**: The amine, phenylethylamine, is the origin of the chirality. It is easily made by resolution, for example by crystallizing the salt of the racemic amine with tartaric acid. This means that both enantiomers are readily available.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/c6f7e8a677357e9b89ebc5424f29715c0064bbbb1f8c1e59731516febc3495ae.jpg]]

The last stages of the process require cleavage of one C–N bond and hydrolysis of the nitrile. It will be important to do this without racemizing the newly created centre.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/56d7bbf449a0ba3202291385de2c413887b8551e017231e788d1d0083111ab95.jpg]]

The C–N bond can be cleaved reductively by hydrogenation as it is an N-benzyl bond. This would also hydrogenate the nitrile so that must first be hydrolysed using acid or base, as weak as possible. The starting material is not recovered and the chirality is lost as the by-product is just ethyl benzene, the nitrogen atom being transferred to the product.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/4caf918704f3485195ed5db1fd96f8a86c71bf08410eb11ef6195b7f570990c6.jpg]]

**中文解析**：

**整体策略分析**：
本题展示了一种利用手性胺作为手性源来合成手性氨基酸的策略。核心思想是：用手性胺的氮原子参与形成C-N键，通过非对映选择性反应将手性信息传递到新的α-碳上，最后通过裂解C-N键释放出氨基酸产物。

**逐步分析**：

1. **手性源——苯乙胺**：
   - 手性来源是(R)-或(S)-苯乙胺
   - 制备方法：外消旋苯乙胺可通过拆分获得，例如用酒石酸与外消旋胺成盐，分级结晶分离非对映体盐
   - 两种对映体都容易获得，因此可以合成(R)或(S)两种氨基酸

2. **反应序列**：
   - 苯乙胺与适当的亲电试剂反应，将手性信息传递到产物中
   - 通过非对映选择性控制新生成的手性中心

3. **最后阶段**：
   - 需要两步关键反应：(a) 裂解一个C-N键；(b) 水解腈基
   - N-Bn键可通过催化氢化（Pd/C + H₂）还原裂解
   - 腈基水解需要酸或碱——但必须在氢化**之前**进行，因为氢化也会还原腈基
   - 水解条件应尽量温和以避免消旋化

4. **手性源是否回收**：
   - **不回收**。苯乙胺的C-N键被还原裂解后，N原子转移到产物氨基酸中，苯乙胺的骨架变成乙苯（副产物），手性信息丢失
   - 这是一个"手性氮原子转移"过程——氮原子从苯乙胺转移到产物中

**为什么产物是特定对映体**：
产物氨基酸的(S)构型（天然氨基酸构型）由苯乙胺的构型决定。如果使用(R)-苯乙胺则得到(S)-氨基酸，使用(S)-苯乙胺则得到(R)-氨基酸。非对映选择性来自苯乙胺手性中心对新生成手性中心的立体控制。

**参考文献**：K. Q. Do et al., Helv. Chim. Acta, 1979, 62, 956。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[不对称合成]] | 利用手性胺作为手性源合成氨基酸 | 直接 |
| [[立体化学基础]] | 非对映选择性控制新生成手性中心 | 直接 |
| [[合成设计]] | 手性信息传递策略和官能团兼容性 | 直接 |
| [[拆分技术]] | 苯乙胺的酒石酸盐拆分 | 间接 |
| N-苄基保护 | C-N键的催化氢化裂解 | 间接 |

## 解题思路

1. **读题定位**：题目要求识别手性源、解释产物对映体选择性、提出最后阶段试剂、判断手性源是否回收。关键词：手性源、氨基酸合成、C-N键裂解
2. **🔑 关键转换**：苯乙胺是手性源→通过非对映选择性反应传递手性信息→最后通过氢化裂解N-Bn键释放氨基酸→手性源不回收（氮转移到产物中）
3. **验证**：(a) 水解必须在氢化之前（腈基也会被氢化还原）；(b) 水解条件要温和避免消旋化；(c) 乙苯是副产物，苯乙胺的手性信息无法回收

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 认为苯乙胺可以回收 | 没有追踪N原子的去向 | N-Bn键被氢化裂解后，N原子转移到产物中，苯乙胺骨架变成乙苯，无法回收 | 为什么说N原子被"转移"了？ |
| 忘记先水解腈基再氢化 | 没有考虑氢化对腈基的影响 | Pd/C+H₂不仅裂解N-Bn键，也会还原腈基为胺，所以必须先水解腈基 | 氢化腈基会得到什么产物？ |
| 用强酸/强碱水解腈基 | 没有考虑消旋化风险 | 必须用尽可能温和的酸/碱条件水解，避免α-碳消旋化 | α-氨基酸在什么条件下会消旋化？ |
| 只能得到(S)-氨基酸 | 没有考虑手性源的两种对映体 | 苯乙胺的两种对映体都可获得，因此(R)和(S)两种氨基酸都能合成 | 使用(S)-苯乙胺会得到什么构型的氨基酸？ |