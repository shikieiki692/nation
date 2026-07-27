---
title: 题-401-Clayden-Ch22-P11-NMR揭示共轭加成过程
type: 题目
submodule: 共轭加成
exam_stage: 初赛
subject: 有机化学
difficulty: 3
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[共轭加成]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch22-P11]
source: Clayden Organic Chemistry 2nd Ed. Chapter 22 Problem 11
cross_references: ["[[题-628-Clayden-Ch38-P1-碱引发两个简单卡宾反应]]", "[[题-320-Clayden-Ch19-P1-HCl对三个烯烃加成方向]]", "[[题-629-Clayden-Ch38-P2-另一种卡宾方法→天然抗生素]]", "[[题-321-Clayden-Ch19-P2-两个烯烃溴化机理和产物]]"]
module: 有机化学
status: 已填充
---
# 题-401: NMR揭示共轭加成过程

## 题目

Stirring thioacetic acid with acrolein (propenaldehyde) in acetone gives a compound with the NMR data shown below. What is the compound?

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/38332535a437e68bda057ecc70de37259baa62217c8e0951533075677a0458d3.jpg]]

δH: 2.28 (3H, s), 3.58 (2H, d, J 8), 4.35 (1H, td, J 8, 6), 6.44 (1H, t, J 6), 7.67 (1H, d, J 6).

δC: 23.5, 31.0, 99.3, 144.2, 196.5.

**原文题目**：Determine the structure of the product from thioacetic acid and acrolein using NMR data. Explain why the product is an enol rather than the expected aldehyde.

## 参考答案

**Answer (English)**: The product formula is the sum of the reaction partners, and all 5 C and 8 H atoms are visible in the NMR spectra, so this looks like an addition reaction. The ¹³C NMR tells us that there are two alkene carbons and one carbonyl, and the proton NMR clearly shows the aldehyde has gone. But it can't be direct addition to the C=O group, because the coupling pattern isn't right for a terminal alkene. The product is in fact the enol formed from conjugate addition of the sulfur, which is stable under these conditions. The low coupling constant across the alkene tells us it's formed unusually as the Z-isomer, probably because of an intramolecular proton transfer from the thioacid to the new OH group. The anhydrous conditions in dry acetone prevent the enol from tautomerizing back to the aldehyde.

This work is described by Lukas Hintermann in J. Org. Chem., 2012, 77, 11345.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/cdd00c9239671376f87bd0bd6758d7f4b752ff41bd9712cab0a93764c3c8ba40.jpg]]

**中文解析**：

关键步骤：
1. **分子式分析**：产物分子式是两个反应物之和，所有5个C和8个H都在NMR中可见，说明是加成反应（不是取代）
2. **NMR解析**：
   - δC 196.5：羰基碳（但不是醛基，因为没有醛基质子信号）
   - δC 144.2和99.3：两个烯烃碳
   - δH 6.44和7.67：烯烃质子，偶合常数J=6 Hz（较小，表明是Z-构型）
   - δH 4.35 (td)：连接O和S的碳上的质子
   - δH 3.58 (d)：CH₂S质子
   - δH 2.28 (s)：CH₃CO质子
3. **产物结构**：硫代乙酸对丙烯醛进行共轭加成，生成的烯醇在无水丙酮中稳定存在（不会互变异构回醛）

> **核心概念**：共轭加成的产物可以烯醇形式存在，特别是在无水条件下。Z-构型的选择性可能来自分子内质子转移。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[共轭加成]] | 硫代乙酸对丙烯醛的共轭加成 | 直接 |
| [[NMR谱学]] | 利用¹H和¹³C NMR确定共轭加成产物结构 | 直接 |
| [[Michael加成]] | 共轭加成产物的烯醇形式稳定化 | 间接 |

## 解题思路

1. **读题定位**：题目给出反应和NMR数据，要求推断产物结构——底物是丙烯醛+硫代乙酸，产物是共轭加成产物
2. **🔑 关键转换**：分子式=加成→NMR显示无醛基→有烯烃+羰基→烯醇形式→Z-构型（小J值）
3. **验证**：检查NMR数据是否与烯醇结构一致——化学位移、积分、偶合常数是否匹配

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 将产物误认为是醛 | 没有注意到醛基质子信号缺失 | δH中没有9-10 ppm的醛基质子，说明醛基已转化为烯醇 | 为什么醛基会变成烯醇？ |
| 错误判断烯烃构型 | 对偶合常数的理解不深 | J=6 Hz较小，表明是Z-构型（顺式）；E-构型的J值通常更大 | Z-和E-烯烃的偶合常数有什么区别？ |
| 忽略无水条件对烯醇稳定化的作用 | 对互变异构平衡不熟 | 无水丙酮中烯醇不会互变异构回醛 | 什么条件下烯醇会互变异构回醛？ |