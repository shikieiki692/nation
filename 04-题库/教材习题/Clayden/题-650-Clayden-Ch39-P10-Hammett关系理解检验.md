---
title: 题-650-Clayden-Ch39-P10-Hammett关系理解检验
type: 题目
fidelity: 原书逐字
submodule: 有机反应机理
exam_stage: 初赛
source_subject: 有机化学
difficulty: 3
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[Hammett方程]]"]
tags: [化竞, Clayden, 有机化学, Hammett方程, 吡啶]
updated: 2026-07-25
aliases: [Clayden-Ch39-P10]
source: Clayden Organic Chemistry 2nd Ed. Chapter 39 Problem 10
cross_references: ["[[题-291-Clayden-Ch14-P1-五个分子手性判断]]", "[[题-584-Clayden-Ch32-P1-环己烯环氧化+胺开环构象分析]]", "[[题-292-Clayden-Ch14-P2-旋光值区分]]", "[[题-585-Clayden-Ch32-P2-非反应对立体化学的影响]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 章节练习
source_category: 教材课后习题
---
# 题-650: Hammett关系理解检验

## 题目

The pKₐ values of some protonated pyridines are as follows:

| X | H | 3-Cl | 3-Me | 4-Me | 3-MeO | 4-MeO | 3-NO₂ |
|---|---|---|---|---|---|---|---|
| pKₐ | 5.2 | 2.84 | 5.68 | 6.02 | 4.88 | 6.62 | 0.81 |

Can the Hammett correlation be applied to pyridines using the σ values for benzene? What equilibrium ρ value does it give and how do you interpret it? Why are no 2-substituted pyridines included in the list?

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/8a81bf0670d64e2a2cbdedd62cc2865353a820934202549fef7df114cae61a1d.jpg]]

**原文题目**：Apply the Hammett relationship to pyridinium ion acidities. Calculate ρ and explain its magnitude. Why are 2-substituted pyridines excluded?

## 参考答案

**Answer (English)**: Plotting pKₐ values against σ values (meta for 3-substituted, para for 4-substituted) gives a good straight line with ρ = +5.9. The sign is positive because the same electronic effects that make benzoic acids more acidic also make pyridinium ions more acidic. The large ρ value reflects the fact that ionization of benzoic acids occurs outside the ring (charge not delocalized round the ring) while deprotonation of pyridinium ions occurs on the ring (charge delocalized round the ring).

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/abd4e42f39732af7369c138f0fc32cdbd3667433bf2c9e5b4c5d81bcaf0dd864.jpg]]

There are no 2-substituted pyridines because, like ortho-substituted benzenes, steric effects prevent good Hammett correlation.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/da43346ca97b25635ab0976fb0de7e89cfb13393967a048e1efe7120aab9db99.jpg]]

**中文解析**：

本题是检验 Hammett 方程理解深度的经典题——将 Hammett 关系应用于吡啶体系，计算并解读 ρ 值。

**Hammett 方程能否应用于吡啶？**

Hammett 方程的核心假设是：取代基效应可以通过 σ 值定量描述，且 ρ 值对同一类反应是常数。吡啶环上的取代基效应与苯环类似，所以可以用苯环的 σ 值来拟合吡啶的酸度数据。

实际操作：
- 3-取代吡啶用 σ_m 值
- 4-取代吡啶用 σ_p 值
- 以 pKₐ 对 σ 作图

**结果：ρ = +5.9**

这是一个非常大的正 ρ 值。解读如下：

**为什么 ρ 为正？**
pKₐ 是酸度常数的负对数。ρ > 0 意味着：
- 吸电子基团（正 σ）使 pKₐ 降低 → 酸性增强
- 给电子基团（负 σ）使 pKₐ 升高 → 酸性减弱

这与苯甲酸的酸度变化方向一致（吸电子基使苯甲酸更强），所以 ρ 为正是合理的。

**为什么 |ρ| = 5.9 这么大？**

对比苯甲酸的酸度（ρ ≈ 1.0），吡啶的 ρ 值大了近 6 倍。原因是：

- **苯甲酸的去质子化**：H⁺ 离开 COOH，负电荷在羧基上，**不在苯环上**。取代基通过诱导/共轭效应影响羧基的电荷，但效应较弱（通过键传递，有衰减）。
- **吡啶的去质子化**：H⁺ 离开 N-H⁺，负电荷（实际上是正电荷的减少）**直接离域在吡啶环上**。取代基直接在环上，效应几乎无衰减。

简而言之：吡啶体系中，反应中心就是环本身，取代基效应被"放大"了。

**为什么没有 2-取代吡啶？**

2-位取代基会产生 **空间位阻效应 (steric effect)**，这是 Hammett 方程无法描述的（Hammett 方程只考虑电子效应）。2-取代基会：
- 阻碍溶剂化
- 改变吡啶环的构象
- 产生额外的立体电子效应

这与苯环的邻位取代类似——邻位取代基的位阻效应使 Hammett 相关性变差。

> **核心概念**：Hammett ρ 值的大小反映了取代基位置与反应中心之间的"耦合强度"。反应中心越靠近环（或电荷越在环上），|ρ| 越大。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[Hammett方程]] | ρ值的计算和物理意义 | 直接 |
| [[有机反应机理]] | 酸度与电子效应的关系 | 直接 |
| [[过渡态]] | 电荷在环上vs环外的差异 | 直接 |
| [[吡啶]] | 吡啶的酸碱化学 | 间接 |
| [[空间位阻]] | 邻位效应与Hammett方程的局限 | 间接 |

## 解题思路

1. **读题定位**：吡啶的 pKₐ 数据，要求用 Hammett 方程拟合
2. **🔑 关键转换**：ρ = +5.9，正值 = 吸电子基增强酸性；|ρ| 大 = 电荷在环上
3. **与苯甲酸对比**：苯甲酸 ρ ≈ 1.0（电荷在环外），吡啶 ρ ≈ 5.9（电荷在环上）→ 电荷位置决定 ρ 值大小
4. **2-取代排除**：空间位阻效应无法用 Hammett 方程描述

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 认为 ρ > 0 说明给电子基增强酸性 | 搞反了 ρ 值符号 | ρ > 0 = 吸电子基增强酸性（正 σ → 低 pKₐ） | 如何从 ρ 值判断电子效应方向？ |
| 认为 ρ = 5.9 说明取代基效应"非常强" | 没有理解 ρ 值的物理意义 | ρ 值大说明反应中心在环上（电荷在环上），不是效应"强" | 为什么有些反应的 ρ 值特别小？ |
| 将 2-取代排除归因于电子效应 | 混淆了位阻效应和电子效应 | 2-位的位阻效应无法用 Hammett 方程描述（只有电子效应） | 如何处理包含位阻效应的取代基？ |
| 认为 Hammett 方程可以应用于所有取代吡啶 | 忽略了方程的适用范围 | 只有当电子效应是唯一变量时 Hammett 方程才有效 | 什么情况下 Hammett 方程会失败？ |