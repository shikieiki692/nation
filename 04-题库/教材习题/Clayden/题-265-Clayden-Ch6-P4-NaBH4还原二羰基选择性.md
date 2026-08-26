---
title: 题-265-Clayden-Ch6-P4-NaBH4还原二羰基选择性
type: 题目
fidelity: 原书逐字
submodule: 羰基亲核加成
exam_stage: 初赛
subject: 有机化学
difficulty: 3
teaching_level: 巩固
syllabus_codes: ["21"]
knowledge_points: ["[[羰基亲核加成]]", "[[化学选择性]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch6-P4]
source: Clayden Organic Chemistry 2nd Ed. Chapter 6 Problem 4
cross_references: ["[[题-262-Clayden-Ch6-P1-硼氢化钠还原醛酮机理]]", "[[题-268-Clayden-Ch6-P8-NaBH4还原氯醛水合物机理]]", "[[题-269-Clayden-Ch6-P10-Grignard加成+NaBH4选择性还原]]"]
module: 有机化学
status: 已填充
---
# 题-265: NaBH₄还原二羰基化合物选择性

## 题目

There are three possible products from the reduction of this compound with sodium borohydride. What are their structures? How would you distinguish them spectroscopically, assuming you can isolate pure compounds?

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/1ee0ee97e32ee44f1d810e4962de1c39b5c4b5cd3dce2875bc8906a6c7483742.jpg]]

**原文题目**：该化合物用NaBH₄还原有三种可能产物。它们的结构是什么？假设可以分离纯品，如何用光谱法区分？

## 参考答案

**Answer (English)**: The three compounds are easily drawn: one or other carbonyl group, or both, may be reduced.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/70141a4ddf2d665c66381504e358fc4eede2c8c9a932d93e390207cf12b6959c.jpg]]

**中文解析**：

三种还原产物：
- **产物A**：只还原醛基（-CHO→-CH₂OH），保留酮基
- **产物B**：只还原酮基（C=O→CH-OH），保留醛基
- **产物C**：两个羰基都被还原（二醇）

**光谱区分方法**：

| 方法 | 产物A（保留酮） | 产物B（保留醛） | 产物C（二醇） |
|------|:---:|:---:|:---:|
| **IR** | C=O伸缩~1680 cm⁻¹（共轭酮） | C=O伸缩~1730 cm⁻¹（非共轭醛） | 无C=O峰 |
| **¹³C NMR** | ~80 ppm（C-OH，酮侧） | ~60 ppm（C-OH，醛侧） | 无C=O峰（>150 ppm无峰） |
| **MS** | 分子离子M⁺ | 分子离子M⁺ | M⁺+2（多了2个H） |

关键区别：羟基酮的C=O是共轭的（~1680 cm⁻¹），羟基醛的C=O是非共轭的（~1730 cm⁻¹）。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|:---:|:---:|
| [[羰基亲核加成]] | NaBH₄对不同羰基的还原 | 直接 |
| [[化学选择性]] | 同一分子中不同羰基的选择性还原 | 直接 |
| [[波谱分析]] | 用IR和NMR区分异构体 | 间接 |
| [[醛酮]] | 醛和酮的化学区别 | 间接 |

## 解题思路

1. **读题定位**：分子有两个不同的羰基（醛和酮），NaBH₄可以还原两者——问三种可能产物的结构和光谱区分
2. **🔑 关键转换**：三个产物 = 只还原醛 + 只还原酮 + 两者都还原。区分关键在IR（共轭vs非共轭C=O）和MS（分子量差）
3. **验证**：二醇产物的MS分子离子应比另外两个高2个质量单位（多2个H）

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 只画出两种产物 | 忘记了两者都被还原的情况 | 三种组合：只还原A、只还原B、A和B都还原 | NaBH₄能区分醛和酮吗？ |
| 混淆共轭和非共轭C=O的IR频率 | 没有理解共轭降低键级 | 共轭C=O频率更低（~1680 cm⁻¹），非共轭更高（~1730 cm⁻¹） | 为什么共轭降低C=O频率？ |
| 用NMR区分时搞错化学位移 | 没有考虑苯环连接位置 | 醛侧C-OH与苯环相连（化学位移不同），酮侧不与苯环相连 | 如何预测13C NMR化学位移？ |