---
title: 题-580-Clayden-Ch31-P11-Ambruticin环丙烷复杂NMR解析
type: 题目
fidelity: 原书逐字
submodule: 立体电子效应
exam_stage: 初赛
subject: 有机化学
difficulty: 4
teaching_level: 竞赛拔高
syllabus_codes: ["21"]
knowledge_points: ["[[NMR谱学]]"]
tags: [化竞, Clayden, 有机化学, 构象分析]
updated: 2026-07-25
aliases: [Clayden-Ch31-P11]
source: Clayden Organic Chemistry 2nd Ed. Chapter 31 Problem 11
cross_references: ["[[题-550-Clayden-Ch29-P1-杂环上亲电亲核取代产物预测]]", "[[题-551-Clayden-Ch29-P2-烷基吡啶LHMDS侧链延伸]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 模块习题集
---
# 题-580: Ambruticin环丙烷复杂NMR解析

## 题目

The structure and stereochemistry of the antifungal antibiotic ambruticin was in part deduced from the NMR spectrum of this simple cyclopropane which forms part of its structure. Interpret the NMR and show how it gives definite information on the stereochemistry.

$\delta_{H}$ 1.21 (3H, d, J 7 Hz), 1.29 (3H, t, J 9), 1.60 (1H, t, J 6), 1.77 (1H, ddq, J 13, 6, 7), 2.16 (1H, dt, J 6, 13), 4.18 (2H, q, J 9), 6.05 (1H, d, J 20), and 6.62 (1H, dd, J 20, 13).

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/7b6e5fcd4da369d944bcf02d5a9f1dc472e11f1a9273e4772400236b015e3cca.jpg]]

**原文题目**：Interpret the NMR of the cyclopropane subunit of ambruticin and determine its stereochemistry.

## 参考答案

**Answer (English)**: In cyclopropanes the cis coupling is usually larger than the trans coupling because the dihedral angle for cis Hs is 0° but that of trans Hs is not 180°. Assigning the three ring hydrogens depends on (a) the quartet coupling to the methyl group, and (b) the 13 Hz coupling to the proton on the alkene. This means that the third proton on the ring (t, J 7) must be next to the carbonyl group. The two trans couplings round the ring are the same (6 Hz) and smaller than the cis coupling (7 Hz). The double bond geometry is on more certain grounds as 20 Hz can be only a trans coupling.

$\delta$ 1.21    $\delta$ 1.77

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/37d53721fb029a130122be2279268a54a703ab45c3dee5a2751f2a473ff51e40.jpg]]

**中文解析**：

关键步骤：
1. **环丙烷偶合常数特点**：环丙烷中cis偶合通常大于trans偶合——cis H的二面角为0°（Karplus曲线最大值），trans H的二面角不是180°
2. **三个环氢的归属**：
   - 1.77 (ddq, J=13, 6, 7)：与甲基偶合(J=7)→通过四重峰识别；与烯烃氢偶合(J=13)→邻近烯烃
   - 1.60 (t, J=6)：两个偶合相同→两个trans偶合(6 Hz each)→位于羰基旁
   - 1.21 (d, J=7)：甲基信号→与环上一个氢偶合
3. **偶合常数分配**：
   - cis偶合(7 Hz) > trans偶合(6 Hz)→符合环丙烷特征
   - 13 Hz为环氢与烯烃氢的偶合
4. **双键几何构型**：20 Hz只能是trans偶合→反式烯烃

> **注意**：环丙烷的Karplus关系与开链体系不同——cis H的二面角接近0°（J大），trans H的二面角约为120-150°（J较小）。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[NMR谱学]] | 环丙烷偶合常数的特殊性（cis > trans） | 直接 |
| [[立体化学]] | 环丙烷立体化学与偶合常数的关系 | 直接 |
| [[构象分析]] | 小环体系的刚性构象限制 | 间接 |

## 解题思路

1. **读题定位**：环丙烷亚基的NMR解析——需要归属三个环氢并确定立体化学
2. **🔑 关键转换**：识别环丙烷偶合特殊性(cis > trans)→用ddq的四重峰识别甲基邻位氢→用t的对称偶合识别羰基邻位氢→20 Hz确认反式烯烃
3. **验证**：检查所有偶合常数是否与环丙烷几何结构一致，特别是cis(7 Hz) > trans(6 Hz)

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 用开链体系的Karplus关系套用环丙烷 | 忽略小环的特殊几何 | 环丙烷中cis H二面角=0°→J最大，与开链不同 | 环丙烷的Karplus曲线有何不同？ |
| 将20 Hz误认为其他偶合 | 不了解烯烃偶合范围 | 20 Hz只能是trans烯烃偶合（cis通常6-12 Hz） | trans和cis烯烃的J值范围？ |
| ddq的归属错误 | 不理解多重峰含义 | ddq=两个不同偶合的双峰+一个四重峰→与三个不同氢偶合 | ddq信号如何拆解？ |