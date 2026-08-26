---
title: "题-481-Clayden-Ch27-P5-Z烯烃制备NMR复习"
type: 题目
fidelity: 原书逐字
submodule: 硫硅磷化学
exam_stage: 初赛
subject: 有机化学
difficulty: 3
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[Wittig反应]]"]
tags: [化竞, Clayden, 有机化学, NMR]
updated: 2026-07-25
aliases: [Clayden-Ch27-P5]
source: Clayden Organic Chemistry 2nd Ed. Chapter 27 Problem 5
cross_references: ["[[题-425-Clayden-Ch23-P2-内酯选择性开环]]", "[[题-424-Clayden-Ch23-P1-溴代醛选择性转化为两个产物]]"]
module: 有机化学
status: 已填充
---
# 题-481: Z-烯烃制备+NMR复习

## 题目

Deduce the structure of the product of this reaction from the NMR spectra and explain the stereochemistry. Compound A has δH 0.95 (6H, d, J 7 Hz), 1.60 (3H, d, J 5), 2.65 (1H, double septuplet, J 4 and 7), 5.10 (1H, dd, J 10 and 4), and 5.35 (1H, dq, J 10 and 5).

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/ead97408b32aca8c373dfc21463fe51aa8ee0d2fe9dd4a7da602ebaa1b98ceca.jpg]]

**原文题目**：Deduce the structure of the product of this reaction from the NMR spectra and explain the stereochemistry.

## 参考答案

**Answer (English)**: This is obviously a Wittig reaction and we should expect a Z-alkene as the ylid is not stabilized by further conjugation. The evidence is plain: the signals at 5.10 and 5.35 are the alkene hydrogens and the coupling constant between them is 10 Hz. This is definitely a Z-alkene.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/a0dc3186193848a9d10af80e25147145c0315e95acfab3606f0976167f0c8540.jpg]]

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/70272c9a8ee05f8da8580e0695b9a5e570469b506fd0d06c42020f1639d66ca4.jpg]]

**中文解析**：

关键步骤：
1. **Wittig反应识别**：底物是溴化鏻盐+碱+醛→Wittig反应生成烯烃
2. **立体化学判断**：非稳定化叶立德→Z-烯烃（动力学控制）
3. **NMR验证**：
   - δ 5.10 (dd, J=10, 4 Hz) 和 δ 5.35 (dq, J=10, 5 Hz)：烯烃质子
   - J=10 Hz 的耦合常数 → cis（Z）构型（Jtrans通常为15-18 Hz）
   - δ 0.95 (6H, d, J=7 Hz)：异丙基的两个甲基
   - δ 1.60 (3H, d, J=5 Hz)：与烯烃相连的甲基
   - δ 2.65 (double septuplet)：异丙基的CH

> **核心要点**：非稳定化Wittig叶立德→Z-烯烃；NMR中J=10 Hz确认cis构型。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| Wittig反应 | 非稳定化叶立德给出Z-烯烃 | 直接 |
| [[烯烃立体选择性]] | Z/E选择性与叶立德稳定性的关系 | 直接 |
| [[NMR谱学]] | 耦合常数判断烯烃构型（J值） | 直接 |

## 解题思路

1. **读题定位**：Wittig反应+NMR解析→需从NMR数据推断结构和立体化学
2. **关键转换**：非稳定化叶立德→Z-烯烃→J=10 Hz确认cis→组装完整结构
3. **验证**：所有NMR信号是否与结构吻合（化学位移、积分、裂分模式）

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 将J=10 Hz误判为trans | J值判断不熟 | Jcis≈6-12 Hz，Jtrans≈15-18 Hz；10 Hz明确是cis | Z和E烯烃的典型J值范围？ |
| 忽略double septuplet | 不熟悉高级裂分 | 异丙基CH被两个甲基(6H)和一个烯烃H耦合 | 什么是double septuplet？ |
| 认为稳定化叶立德也给Z | 混淆Wittig规则 | 非稳定化→Z（kinetic）；稳定化→E（thermodynamic） | 如何记忆Wittig立体化学规则？ |