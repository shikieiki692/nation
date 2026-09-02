---
title: 题-385-Clayden-Ch21-P5-NMR推断硝化产物结构
type: 题目
fidelity: 原书逐字
submodule: 芳香亲电取代
exam_stage: 初赛
source_subject: 有机化学
difficulty: 3
teaching_level: 巩固
syllabus_codes: ["21"]
knowledge_points: ["[[芳香亲电取代]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch21-P5]
source: Clayden Organic Chemistry 2nd Ed. Chapter 21 Problem 5
cross_references: ["[[题-336-Clayden-Ch7-P1-共轭判断和弯曲箭头表示]]", "[[题-337-Clayden-Ch7-P2-复杂化合物中共轭体系范围]]", "[[题-525-Clayden-Ch41-P2-拆分法规划不对称合成入门]]", "[[题-524-Clayden-Ch41-P1-循环中间体创建新手性中心]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 章节练习
---
# 题-385: NMR推断硝化产物结构

## 题目

Nitration of these compounds gives products with the ¹H NMR spectra shown. Deduce the structures of the products and explain the position of substitution. WARNING: do not decide the structure by saying where the nitro group 'ought to go'! Chemistry has many surprises and it is the evidence that counts.

**原文题目**：这些化合物的硝化产物具有所示的1H NMR谱。推断产物的结构并解释取代位置。警告：不要通过硝化基"应该去"哪里来决定结构！化学有很多意外，证据才是关键。

## 参考答案

**Answer (English)**: The first product has only eight hydrogens so two nitro groups must have been added. The molecule is clearly symmetrical and the coupling constant is right for neighbouring hydrogens so a substitution on each ring must have occurred in the para position. Note that the hydrogen next to the nitro group has the larger shift. We can deduce that each benzene ring is an ortho,para-directing group on the other because the intermediate cation is stabilized by conjugation.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/8ea36b4354629a7fac83d2b9f2e0bb2d3885ead16e1b04b49ad3b5d59173919b.jpg]]

The hydrogen count reveals that the next two products are mono-nitro compounds. There are two hydrogens ortho to nitro in the second compound and one of them also has a typical ortho coupling to a neighbouring hydrogen while the other has only a small coupling (2 Hz) which must be a meta coupling. Substitution has occurred para to one of the chlorines and ortho to the other. The chlorines are ortho,para-directing thus activating all remaining positions so steric hindrance must explain the site of nitration.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/8c56767cf4faa21f41960fe1b08d4261469e3c76d4c00f88b6bdbed61d13034d.jpg]]

The third compound has the extra complication of couplings to fluorine. The coupling of 7 Hz shown by one hydrogen and 6 Hz shown by the other must be to fluorine as they occur once only. The symmetry of the compound and the typical ortho coupling between the hydrogens (8 Hz) shows that para substitution must have occurred.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/955013b244f1d5c3a7e97621bdd55d33d1cb49634007744ae7e2e7aac22f30a5.jpg]]

**中文解析**：

本题考察利用NMR数据推断芳香亲电取代产物结构的能力。

关键要点：
1. **联苯衍生物**：第一个产物只有8个H，说明引入了2个NO₂。分子对称且偶合常数表明每个环上发生了对位取代
2. **二氯苯衍生物**：第二个产物是单硝基化合物。2个H在NO₂的邻位，其中一个是典型邻位偶合（8-10 Hz），另一个只有小偶合（2 Hz，为间位偶合）。硝化发生在Cl的对位和另一个Cl的邻位
3. **含氟化合物**：第三个产物有F-H偶合（7 Hz和6 Hz各出现一次），对称性表明是对位取代
4. **核心方法**：先数H确定取代基数目→分析对称性→用偶合常数判断取代位置

> **NMR在有机化学中的应用**：H NMR的化学位移、积分值和偶合常数可以提供关于分子结构的丰富信息，特别是在推断取代模式时。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[芳香亲电取代]] | 硝化产物的结构推断 | 直接 |
| [[NMR谱学]] | 利用化学位移、积分和偶合常数分析结构 | 直接 |
| [[定位效应]] | 根据取代基效应预测硝化位置 | 间接 |
| [[偶合常数]] | 邻位偶合（8-10 Hz）与间位偶合（<2 Hz）的区别 | 间接 |

## 解题思路

1. **读题定位**：题目给出NMR数据，要求推断硝化产物结构——这是"证据驱动"的结构推断
2. **🔑 关键转换**：先数H确定硝基数目→分析对称性→用偶合常数判断邻/间/对位取代→注意F-H偶合的特殊性
3. **验证**：检查推断的结构与所有NMR数据（化学位移、积分、偶合常数）是否一致

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 不数H就猜结构 | 未利用积分信息 | H的数目可以确定硝基的数目 | 如何从NMR积分判断取代基数目？ |
| 混淆邻位和间位偶合 | 对偶合常数不熟悉 | 邻位偶合（vicinal）8-10 Hz，间位偶合（meta）<2 Hz | 如何区分对称和不对称的取代模式？ |
| 忽略F-H偶合 | 不了解异核偶合 | F-I偶合会在H NMR中出现额外的偶合常数 | 哪些常见元素会与H产生偶合？ |