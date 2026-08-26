---
title: 题-581-Clayden-Ch31-P12-最少信息确定立体化学
type: 题目
fidelity: 原书逐字
submodule: 立体电子效应
exam_stage: 初赛
subject: 有机化学
difficulty: 4
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[立体化学]]"]
tags: [化竞, Clayden, 有机化学, 非对映异构]
updated: 2026-07-25
aliases: [Clayden-Ch31-P12]
source: Clayden Organic Chemistry 2nd Ed. Chapter 31 Problem 12
cross_references: ["[[题-550-Clayden-Ch29-P1-杂环上亲电亲核取代产物预测]]", "[[题-551-Clayden-Ch29-P2-烷基吡啶LHMDS侧链延伸]]"]
module: 有机化学
status: 已填充
---
# 题-581: 最少信息确定立体化学

## 题目

A reaction produces two diastereoisomers of the product below: isomer A has $\delta_{H}$ 3.08 (1H, dt, J 4, 9, 9) and 4.32 (1H, d, J 9), while isomer B has $\delta_{H}$ 4.27 (1H, d, J 4). All other protons (except those of the Me groups) overlap in the NMR. Isomer B is converted into isomer A in base. What is the stereochemistry of A and B?

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/fe9fd88ca549be66e44edc1262d1defac65207832b580d14cf8ecf26c01f8661.jpg]]

**原文题目**：Determine the stereochemistry of isomers A and B with minimum NMR information.

## 参考答案

**Answer (English)**: There are only two diastereoisomers and the difference in coupling constants is striking. The observed Hs must be those next to the functional groups. These compounds are not true cyclohexanes as they are flattened by the benzene ring and are best drawn as cyclohexenes. You should imagine the benzene ring coming towards you from the double bond.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/7a39def3a0b87b5caa4dfa6292d91eb4583ff1f1b7f42104e88513a34c44f375.jpg]]

The two protons we can see in isomer A must be H¹ and H² as they have the largest shifts. The proton with only one coupling must be H¹ as it has only one neighbour H². The coupling between these two is 9 Hz so they must both be axial. Isomer A is therefore the trans compound. H² is a double triplet because it has two axial neighbours and one equatorial neighbour (H⁴). Isomer B shows H¹ alone and it is clearly equatorial (J 4) and so it must be the cis isomer.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/053cd647d7093989761b21a64d92f84286936d60716e85f9d81be429dc0c9058.jpg]]

A reminder: we are showing only relative configuration here: NMR tells us nothing about whether we have one or both enantiomers of each diastereoisomer.

Conversion to A occurs by enolate formation and the trans compound is more stable than the cis, as you might expect.

**中文解析**：

关键步骤：
1. **简化环系统**：苯环使六元环变平，最好画成环己烯——想象苯环从双键向你方向伸出
2. **异构体A分析**：
   - 4.32 (d, J=9)：只有一个邻位偶合→H¹，只有H²一个邻居
   - 3.08 (dt, J=4, 9, 9)：两个大偶合(9 Hz)+一个小偶合(4 Hz)→H²，两个轴向邻居+一个平伏邻居(H⁴)
   - J(H¹-H²)=9 Hz→两个都是轴向→**trans异构体**
3. **异构体B分析**：
   - 4.27 (d, J=4)：H¹，小偶合→平伏→**cis异构体**
4. **碱催化转化**：B→A通过烯醇化实现，trans更稳定（热力学控制）

> **注意**：NMR只能确定相对构型（哪个非对映体），不能确定绝对构型（哪个对映体）。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[立体化学]] | 顺式/反式非对映体的偶合常数区分 | 直接 |
| [[NMR谱学]] | 最少信号下的立体化学推断策略 | 直接 |
| [[非对映异构]] | 碱催化非对映体互变（烯醇化） | 间接 |

## 解题思路

1. **读题定位**：两个非对映异构体，大部分信号重叠，只有少量信号可辨——用最少信息确定立体化学
2. **🔑 关键转换**：识别可辨信号为官能团邻位氢→J=9 Hz=两个轴向(trans)→J=4 Hz=平伏(cis)→碱催化B→A=热力学控制
3. **验证**：检查dt的偶合模式是否与trans构象一致，碱催化转化方向是否与稳定性一致

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 忘记考虑苯环对构象的影响 | 按普通环己烷分析 | 苯环使六元环变平，更接近环己烯构象 | 苯环如何影响六元环构象？ |
| 混淆热力学和动力学控制 | 不理解碱催化互变 | B→A是热力学控制→trans更稳定 | 什么条件下是动力学控制？ |
| 试图确定绝对构型 | 超出NMR能力 | NMR只能确定相对构型（非对映体），不能确定对映体 | 什么方法可以确定绝对构型？ |