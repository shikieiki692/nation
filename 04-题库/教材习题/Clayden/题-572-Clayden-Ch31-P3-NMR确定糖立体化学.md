---
title: 题-572-Clayden-Ch31-P3-NMR确定糖立体化学
type: 题目
fidelity: 原书逐字
submodule: 立体电子效应
exam_stage: 初赛
source_subject: 有机化学
difficulty: 4
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[NMR谱学]]"]
tags: [化竞, Clayden, 有机化学, 杂环化合物]
updated: 2026-07-25
aliases: [Clayden-Ch31-P3]
source: Clayden Organic Chemistry 2nd Ed. Chapter 31 Problem 3
cross_references: ["[[题-550-Clayden-Ch29-P1-杂环上亲电亲核取代产物预测]]", "[[题-551-Clayden-Ch29-P2-烷基吡啶LHMDS侧链延伸]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 模块习题集
used_in: "[[有机化学阶段测试卷]]"
---
# 题-572: NMR确定糖立体化学+立体电子构象

## 题目

**【中文】**抗生素 kijanimycin 的一种糖组分具有如图所示的基本结构，其 NMR 谱数据如下。它的立体化学是什么？推断出结构后，请指出该分子倾向于采取哪种构象。

**【原文】**One of the sugar components of the antibiotic kijanimycin has the basic structure shown here and NMR spectrum given below. What is the stereochemistry? When you have deduced the structure, suggest which conformation the molecule will prefer.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/96dd7948bf57509a34f56b896b0cb8807c752ee583cacff3accd4ab08255218a.jpg]]

$\delta_{H}$ 1.33 (3H, d, J 6 Hz), 1.61* (1H, broad s), 1.87 (1H, ddd, J 14, 3, 3.5 Hz), 2.21 (1H, ddd, J 14, 3, 1.5 Hz), 2.87 (1H, dd, J 10, 3 Hz), 3.40 (3H, s), 3.99 (1H, dq, J 10, 3 Hz), 3.47 (3H, s), 4.24 (1H, ddd, J 3, 3, 3.5 Hz) and 4.79 (1H, dd, J 3.5, 1.5 Hz). The signal marked \* exchanges with D₂O.

**原文题目**：Determine the stereochemistry of the sugar component and suggest its preferred conformation based on NMR data.

## 参考答案

**Answer (English)**: You can make some preliminary assignments from a combination of shift and coupling:

| Signal | Integral and splitting | Comments | Assignment |
|---|---|---|---|
| 1.33 | 3H, d, J 6 | 3H, d must be CHMe | Me⁷ |
| 1.61* | 1H broad s | exchanges so must be OH | OH |
| 1.87 | 1H, ddd, J 14, 3, 3.5 | 14 Hz looks like CH₂ | H² or H³ |
| 2.21 | 1H, ddd, J 14, 3, 1.5 | 2.21 and 1.87 are CH₂ | H² or H³ |
| 2.87 | 1H, dd, J 10, 3 | must be axial H (10 Hz) | H⁴ or H⁵ |
| 3.40 | 3H, s | one OMe group | OMe |
| 3.47 | 3H, s | the other OMe group | OMe |
| 3.99 | 1H, dq, J 10, 6 | q means H⁶ (axial) | H⁶ |
| 4.24 | 1H, ddd, J 3, 3, 3.5 | small J must be equatorial | H⁴ or H⁵ |
| 4.79 | 1H, dd, J 3.5, 1.5 | small J must be equatorial | H¹ |

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/b0ee828c5344f6349ce15228b9ebaca2199d98f21c8d87ad95ff478b3612862b.jpg]]

Since H⁶ is a 10 Hz doublet coupled with H⁵, we know that H⁵ is at 2.87 and is axial. This gives the entire assignment and the stereochemistry: H⁵ and H⁶ are axial; H¹ and H⁴ are equatorial. That is why there are no large vicinal (³J) couplings to the diastereotopic CH₂ group (H² and H³). All couplings not shown on the diagram are <4 Hz.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/b89b964612a685134f6bb38e686873abc300e8539c8da0121e4c02918321ab30.jpg]]

**中文解析**：

关键步骤：
1. **初步归属**：从化学位移和偶合模式出发——1.33(d, 3H)为CHMe，1.61(宽s, D₂O交换)为OH，3.40和3.47(s, 各3H)为两个OMe
2. **关键偶合常数分析**：H⁶的10 Hz双峰偶合H⁵→H⁵在2.87处为轴向氢；H¹的4.79处小偶合(J=3.5, 1.5)→H¹为平伏氢
3. **立体化学确定**：H⁵和H⁶为轴向，H¹和H⁴为平伏→全反式排列
4. **构象预测**：基于异头效应，缩醛氧处于轴向，整体采取椅式构象

> **注意**：³J偶合常数是判断轴向/平伏取向的最有力工具——轴向-轴向偶合约10-12 Hz，轴向-平伏或平伏-平伏偶合约2-5 Hz。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[NMR谱学]] | ¹H NMR化学位移、偶合常数、积分的综合分析 | 直接 |
| [[立体电子效应]] | 异头效应决定缩醛构象，轴向/平伏取向影响偶合常数 | 直接 |
| [[杂环化合物]] | 糖类含氧杂环的立体化学特征 | 间接 |

## 解题思路

1. **读题定位**：题目给出NMR数据要求确定糖的立体化学和构象
2. **🔑 关键转换**：逐个归属信号→用偶合常数判断轴向/平伏→确定全反式排列→验证构象
3. **验证**：检查所有偶合常数是否与推定的椅式构象一致，特别是H⁵-H⁶的10 Hz轴向-轴向偶合

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 忽略D₂O交换信号 | 不理解宽s的意义 | D₂O交换表明活泼氢(OH)，不是碳上的氢 | 如何通过D₂O交换区分OH和CH？ |
| 将14 Hz偶合误认为轴向-轴向 | 14 Hz是¹J(CH₂)的同碳偶合 | 同碳偶合²J(CH₂)通常10-15 Hz，不是³J | 如何区分同碳偶合和邻位偶合？ |
| 忘记异头效应构象 | 只考虑空间位阻 | 缩醛氧必须轴向以获得异头效应稳定化 | 糖的构象为什么与普通环己烷不同？ |