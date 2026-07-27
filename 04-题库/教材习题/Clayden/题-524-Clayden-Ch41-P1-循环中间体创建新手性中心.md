---
title: 题-524-Clayden-Ch41-P1-循环中间体创建新手性中心
type: 题目
submodule: 不对称合成
exam_stage: 决赛
subject: 有机化学
difficulty: 3
teaching_level: 巩固
syllabus_codes: ["21"]
knowledge_points: ["[[不对称合成]]", "[[手性中心]]"]
tags: [化竞, Clayden, 有机化学, 不对称合成]
updated: 2026-07-25
aliases: [Clayden-Ch41-P1]
source: Clayden Organic Chemistry 2nd Ed. Chapter 41 Problem 1
cross_references: ["[[题-478-Clayden-Ch27-P2-硫叶立德化学区域和立体化学]]", "[[题-291-Clayden-Ch14-P1-五个分子手性判断]]", "[[题-477-Clayden-Ch27-P1-分子内硫叶立德共轭加成环丙烷化]]", "[[题-292-Clayden-Ch14-P2-旋光值区分]]"]
module: 有机化学
status: 已填充
---
# 题-524: 循环中间体创建新手性中心

## 题目

Explain how this synthesis of amino acids, starting with natural proline, works. Explain the stereoselectivity of each step after the first.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/1d8ed1caf6442f4f1e7cc33885ff5281943c7e9c3377f5f5e7bdeb9cf4abc7f8.jpg]]

**原文题目**：Explain how this synthesis of amino acids, starting with natural proline, works. Explain the stereoselectivity of each step after the first.

## 参考答案

**Answer (English)**: Nothing exciting happens until the hydrogenation step. The stereoselectivity of the reaction with ammonia is interesting but not of any consequence as that stereochemistry disappears in the elimination. This gives the E-enone as expected since the alkene and the carbonyl group are in the same plane. The new stereogenic centre is created in the hydrogenation step. The molecule is slightly folded and the catalyst interacts best with the outside (convex) face so that it adds hydrogen from the same face as the ring junction hydrogen. All that remains is to hydrolyse the product without racemization. The configuration of the new amino acid (S) is the same as that of the natural amino acids.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/591770853b655c6b1cf83ef1cb53f5af23e38cabdb668bb43cd8669133f32cad.jpg]]

**中文解析**：

**整体策略分析**：
本题展示了如何利用天然氨基酸（L-脯氨酸）作为手性源，通过循环中间体策略创建新的手性中心，最终合成其他手性氨基酸。这是一种经典的"手性池"策略的变体——利用已有手性分子的立体化学信息来控制新手性中心的构型。

**逐步分析**：
1. **第一步（NH₃加成）**：NH₃对不饱和内酰胺的Michael加成，虽然产生了新的手性中心，但这步的立体选择性并不关键，因为随后的消除反应会消除该手性信息。消除产生E-烯酮，因为烯烃和羰基在同一平面上时热力学更稳定
2. **关键步骤——催化氢化**：这是创建新手性中心的核心步骤。分子具有轻微折叠的构象，催化剂（如Pd/C）从空间位阻较小的凸面（convex face）接近底物，因此H₂从与环接点氢相同的一面加入。这种面选择性是由底物的立体化学控制的——天然脯氨酸的构型决定了凸面的可接近性
3. **水解**：氢化产物经水解得到新的氨基酸，且不发生消旋化。新生成的氨基酸为(S)构型，与天然氨基酸构型一致

**为什么这种方法巧妙**：
- 利用脯氨酸的吡咯烷环作为手性模板，通过环的折叠构象实现非对映选择性氢化
- 一个手性中心的信息被"传递"到新的手性中心
- 反应引用：B. W. Bycroft and G. R. Lee, J. Chem. Soc., Chem. Commun., 1975, 988

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[不对称合成]] | 利用手性池化合物创建新手性中心的策略 | 直接 |
| [[手性中心]] | 氢化步骤中新sp³碳的立体化学控制 | 直接 |
| [[立体化学]] | 催化氢化的面选择性（凸面/凹面） | 直接 |
| [[催化氢化]] | 异相催化氢化的立体化学结果 | 间接 |

## 解题思路

1. **读题定位**：题目要求解释从天然脯氨酸出发合成氨基酸的路线，并解释每步的立体选择性。关键词：天然脯氨酸（手性源）、立体选择性
2. **🔑 关键转换**：识别出真正的手性中心创建步骤是催化氢化——分子的折叠构象使催化剂从凸面接近，H₂从环接点氢同面加入
3. **验证**：产物氨基酸的(S)构型与天然氨基酸一致，说明手性信息成功传递；NH₃加成/消除步骤的立体化学"无关紧要"因为会被消除

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 认为NH₃加成步是关键 | 混淆了产生手性中心和"有效"创建手性中心 | NH₃加成产生的立体化学会在后续消除中消失，真正的关键步骤是氢化 | 为什么消除会消除之前建立的立体化学？ |
| 忽略分子折叠构象 | 没有考虑催化剂接近的空间位阻 | 底物的折叠构象使凸面（outside face）更易被催化剂接近 | 如果脯氨酸是(D)构型，产物氨基酸构型会怎样？ |
| 认为水解会导致消旋化 | 担心酸/碱水解会破坏手性中心 | 该水解条件下新生成的α-氨基酸手性中心不受影响（α-碳上没有可交换的酸性质子） | 在什么条件下氨基酸会发生消旋化？ |