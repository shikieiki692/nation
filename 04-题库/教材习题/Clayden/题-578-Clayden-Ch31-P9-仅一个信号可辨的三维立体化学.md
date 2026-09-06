---
title: 题-578-Clayden-Ch31-P9-仅一个信号可辨的三维立体化学
type: 题目
fidelity: 原书逐字
submodule: 立体电子效应
exam_stage: 初赛
source_subject: 有机化学
difficulty: 4
teaching_level: 竞赛
syllabus_codes: ["21"]
knowledge_points: ["[[NMR谱学]]"]
tags: [化竞, Clayden, 有机化学, 非对映异构]
updated: 2026-07-25
aliases: [Clayden-Ch31-P9]
source: Clayden Organic Chemistry 2nd Ed. Chapter 31 Problem 9
cross_references: ["[[题-550-Clayden-Ch29-P1-杂环上亲电亲核取代产物预测]]", "[[题-551-Clayden-Ch29-P2-烷基吡啶LHMDS侧链延伸]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 模块习题集
source_category: 教材课后习题
---
# 题-578: 仅一个信号可辨的三维立体化学

## 题目

**【中文】**已制备出该环状酮-内酰胺（见图）的两个非对映异构体。NMR 谱中有许多重叠信号，但标记的质子可以清楚辨认：在异构体 A 中它位于 $\delta_{H}$ 4.12 (1H, q, J 3.5)，在异构体 B 中位于 $\delta_{H}$ 3.30 (1H, dt, J 4, 11)。哪个异构体对应哪种立体化学？

**【原文】**Two diastereoisomers of this cyclic keto-lactam have been prepared. The NMR spectra have many overlapping signals but the marked proton can be seen clearly. In isomer A it is at $\delta_{H}$ 4.12 (1H, q, J 3.5) and in isomer B it is $\delta_{H}$ 3.30 (1H, dt, J 4, 11). Which isomer has which stereochemistry?

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/6e6c38ee29daf47a250422464ee56bab0cc1911ccd06e76fb225ba53899094b8.jpg]]

**原文题目**：Assign stereochemistry to isomers A and B based on NMR of the marked proton.

## 参考答案

**Answer (English)**: The two isomers have cis and trans ring junctions so we should start by making conformational drawings of both. The trans compound is easy as it has a fixed trans-decalin shape. The cis compound can have two conformations as both conformers can flip.

one axial-equatorial coupling 4 Hz

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/5c61289b47d7e1b302f1624cec548d29aa113fc5d0e26aa761d177ee2e4f5c44.jpg]]

The vital proton is clearly axial in isomer B as it has two large couplings (10 Hz) to other axial protons so this must be the trans isomer. Isomer A has three equal small couplings and this fits one conformation of the cis isomer.

two axial-axial couplings

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/c8f82c3321ab8b00873b767a788a831bd27823de4474608ec4240c8a6bfaf4fd.jpg]]

no axial-axial couplings

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/9b98f9fdfc8c068ac15f0953625289320dbc2cf04d3fc44828a72e43bdf0408c.jpg]]

**中文解析**：

关键步骤：
1. **识别两种异构体**：环状酮-内酰胺有两个非对映异构体——顺式和反式环并
2. **构象分析**：
   - 反式异构体：固定为反式十氢萘形状（trans-decalin），不能翻转
   - 顺式异构体：两种构象都可翻转
3. **NMR关键信号分析**：
   - **异构体B**：dt, J=4, 11→一个大偶合(11 Hz)为轴向-轴向→该氢为轴向→反式异构体
   - **异构体A**：q, J=3.5→三个相等的小偶合→无轴向-轴向偶合→该氢为平伏→顺式异构体
4. **偶合模式与构象对应**：
   - 反式：标记氢为轴向，有两个轴向邻位氢→两个大J（~10 Hz）
   - 顺式（一种构象）：标记氢为平伏，无轴向邻位→三个小J（~4 Hz）

> **注意**：十氢萘体系中，反式并环保证了刚性构象，使轴向/平伏判断非常明确。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[NMR谱学]] | dt和q的偶合模式解读，大J（轴向-轴向）vs小J（轴向-平伏） | 直接 |
| [[立体化学]] | 顺式/反式环并十氢萘的构象差异 | 直接 |
| [[非对映异构]] | 两个非对映异构体的NMR区分策略 | 间接 |

## 解题思路

1. **读题定位**：两个非对映异构体，NMR大部分重叠，只有标记氢可辨——用一个信号区分顺反
2. **🔑 关键转换**：画出顺式和反式的椅式构象→判断标记氢是轴向还是平伏→大J=轴向(反式)，小J=平伏(顺式)
3. **验证**：检查偶合常数是否与构象一致——dt中的大J(11 Hz)必须对应轴向-轴向偶合

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 将dt中的小J忽略 | 只关注大偶合 | dt表示三个偶合：一个大(11 Hz轴向-轴向)和两个小(4 Hz轴向-平伏) | dt和dd的区别是什么？ |
| 混淆顺式和反式十氢萘 | 对环并构象不熟悉 | 反式十氢萘刚性（不能翻转），顺式可翻转 | 为什么反式十氢萘不能翻转？ |
| 忘记考虑构象翻转 | 只画了一种构象 | 顺式异构体有两种可翻转的构象，需选择与NMR匹配的那个 | 如何判断哪种构象更稳定？ |