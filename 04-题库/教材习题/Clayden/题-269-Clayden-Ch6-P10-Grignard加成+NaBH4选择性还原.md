---
title: 题-269-Clayden-Ch6-P10-Grignard加成+NaBH4选择性还原
type: 题目
fidelity: 原书逐字
submodule: 羰基亲核加成
exam_stage: 初赛
subject: 有机化学
difficulty: 3
teaching_level: 巩固
syllabus_codes: ["21"]
knowledge_points: ["[[Grignard试剂]]", "[[羰基亲核加成]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch6-P10]
source: Clayden Organic Chemistry 2nd Ed. Chapter 6 Problem 10
cross_references: ["[[题-262-Clayden-Ch6-P1-硼氢化钠还原醛酮机理]]", "[[题-265-Clayden-Ch6-P4-NaBH4还原二羰基选择性]]", "[[题-283-Clayden-Ch9-P1-有机金属加成羰基的机理]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 章节练习
---
# 题-269: Grignard加成+NaBH₄选择性还原

## 题目

What would be the products of these reactions? In each case give a mechanism to justify your prediction.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/a4a42ff3707943f45f3d114fd7130c0343c2c2079f1a3174f8c10379232f1780.jpg]]

$\xrightarrow[\mathrm{Et}_{2}\mathrm{O}]{\mathrm{EtMgBr}}?$

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/c23a84710c769901adc4200a29c1a9c71a51221adbf99ee2e1f7887761cdb9be.jpg]]

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/e26d0bb48a771001883853bc70b6c709749c53854fe54965df51ff77f510e64a.jpg]]

**原文题目**：这些反应的产物是什么？在每种情况下给出机理来支持你的预测。

## 参考答案

**Answer (English)**: The Grignard reagent will add to the carbonyl group and the work-up will give a tertiary alcohol as the final product.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/2c38fc3ec1dac528baba5915b76411ef6f3a563922779d213b55f809c5706f0f.jpg]]

The second reaction should give you brief pause for thought as you need to recall that borohydride reduces ketones but not esters.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/33c8bc120add3ea836ff5f97634b28d71aed3770a6a5f1bf8876c95f284572a7.jpg]]

**中文解析**：

**反应1：酮 + EtMgBr → 三级醇**
- EtMgBr（格氏试剂）作为碳亲核试剂进攻酮的C=O
- Et⁻加到羰基碳上，形成C-C键
- 水处理（work-up）后得到三级醇（叔醇）
- 机理：EtMgBr → Et⁻ + MgBr⁺；Et⁻进攻C=O → O⁻MgBr → H₃O⁺ → 产物

**反应2：含酮和酯的底物 + NaBH₄ → 只还原酮**
- NaBH₄还原酮（C=O→CH-OH）但**不还原酯**
- 这是NaBH₄的重要化学选择性——它只能还原醛和酮，不能还原酯、酰胺、羧酸
- 酯需要更强的还原剂（如LiAlH₄）才能还原

> **关键区别**：NaBH₄ vs LiAlH₄的还原范围：
> - NaBH₄：醛 ✓ 酮 ✓ 酯 ✗ 酰胺 ✗
> - LiAlH₄：醛 ✓ 酮 ✓ 酯 ✓ 酰胺 ✓

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[Grignard试剂]] | EtMgBr作为碳亲核试剂进攻C=O | 直接 |
| [[羰基亲核加成]] | 两种不同的亲核加成反应 | 直接 |
| [[化学选择性]] | NaBH₄选择性还原酮而不还原酯 | 直接 |
| [[醛酮]] | 醛酮vs酯的反应性差异 | 间接 |

## 解题思路

1. **读题定位**：两个不同的反应——反应1是Grignard对酮的加成，反应2是NaBH₄对多官能团底物的选择性还原
2. **🔑 关键转换**：反应1：EtMgBr的Et⁻加到C=O碳上→叔醇。反应2：NaBH₄只还原酮→酯保持不变（化学选择性）
3. **验证**：反应1产物是三级醇（三个取代基在同一个碳上）；反应2产物保留酯基，只还原了酮

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 反应2中NaBH₄同时还原酯 | 混淆了NaBH₄和LiAlH₄的还原范围 | NaBH₄只能还原醛和酮，不能还原酯/酰胺/羧酸 | 哪种还原剂可以只还原酯而不还原酮？ |
| 反应1中忘记水处理步骤 | 只画了格氏加成 | 格氏加成后必须有酸性水处理（work-up）才能得到醇 | 为什么格氏反应必须无水操作？ |
| 搞混亲核试剂和亲电试剂的角色 | 基础概念不清 | EtMgBr中的Et⁻是亲核试剂，C=O碳是亲电中心 | Grignard试剂中碳的氧化态是多少？ |