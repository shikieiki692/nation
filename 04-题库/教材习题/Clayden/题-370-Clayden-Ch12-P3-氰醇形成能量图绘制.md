---
title: 题-370-Clayden-Ch12-P3-氰醇形成能量图绘制
type: 题目
fidelity: 原书逐字
submodule: 反应动力学
exam_stage: 初赛
subject: 有机化学
difficulty: 3
teaching_level: 巩固
syllabus_codes: ["21"]
knowledge_points: ["[[反应动力学]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch12-P3]
source: Clayden Organic Chemistry 2nd Ed. Chapter 12 Problem 3
cross_references: ["[[题-336-Clayden-Ch7-P1-共轭判断和弯曲箭头表示]]", "[[题-346-Clayden-Ch10-P2-酯化酸催化vs碱不反应分析]]", "[[题-337-Clayden-Ch7-P2-复杂化合物中共轭体系范围]]", "[[题-345-Clayden-Ch10-P1-Phenaglycodol合成试剂选择]]"]
module: 有机化学
status: 已填充
---
# 题-370: 氰醇形成能量图绘制

## 题目

Draw an energy profile diagram for this reaction. You will of course need to draw the mechanism first. Suggest which step in this mechanism is likely to be the slow step and what kinetics would be observed.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/5a34cc4a26b29a17b52874e5d253ee963daf8fbbd529bed294d091d973c2f03e.jpg]]

**原文题目**：Draw an energy profile diagram for this reaction. You will of course need to draw the mechanism first. Suggest which step in this mechanism is likely to be the slow step and what kinetics would be observed.

## 参考答案

**Answer (English)**:

The first thing is to draw the mechanism of the reaction.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/3e63e6aa4c04dea5b8c0dd25ad399706e02fc314b095720a6e703ac6decbb161.jpg]]

The first step is bimolecular and forms a new C–C bond. The second step is just a proton transfer between oxygen atoms and is certainly fast. The first step must be the rate-determining step and the intermediate must have a higher energy than the starting material or the product.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/ced6b336703fc2156122bfd25a6f0f551bf9d65496f94320f55f7884199da3c3.jpg]]

**中文解析**：

关键步骤：
1. **机理分析（氰醇形成）**：
   - **第一步**：CN⁻作为亲核试剂进攻酮的C=O碳，形成C-C键，产生烷氧基负离子中间体（四面体中间体）
   - **第二步**：质子转移（从溶剂或HCN向氧负离子转移），生成氰醇产物
2. **速决步判断**：第一步是双分子反应（形成新C-C键），需要克服较大的活化能；第二步是简单的质子转移（O到O），非常快。因此第一步是速决步
3. **能量图绘制**：
   - 反应物能量→过渡态1（最高点）→中间体（能量凹谷）→过渡态2（较低的能垒）→产物
   - 中间体能量高于反应物和产物（因为是活性中间体）
   - 第一步的活化能（Ea₁）远大于第二步的活化能（Ea₂）

> **能量图关键特征**：两个过渡态+一个中间体（双峰一谷）。中间体对应四面体负离子，第一个峰对应CN⁻进攻C=O的过渡态（速决步）。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[反应动力学]] | 从机理推断速决步和动力学级数 | 直接 |
| [[过渡态]] | 能量图中过渡态和中间体的表示 | 直接 |
| [[活化能]] | 速决步具有最大活化能 | 间接 |

## 解题思路

1. **读题定位**：题目要求画能量图——先画机理，再判断速决步，最后绘制能量曲线
2. **🔑 关键转换**：氰醇形成机理=CN⁻亲核进攻C=O→四面体中间体→质子转移→产物。速决步=第一步（C-C键形成，双分子，高活化能）。能量图=两峰一谷
3. **验证**：检查能量图是否合理——反应物和产物能量相近（反应可逆），中间体为局部最低点，两个过渡态为局部最高点，第一步的能垒明显高于第二步

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 将质子转移步画为速决步 | 低估了质子转移的速度 | 质子在O原子间的转移极快（通过氢键网络），几乎不需活化能 | 为什么质子转移通常不是速决步？ |
| 能量图只画一个峰 | 未意识到反应有两步 | 两步反应=两个过渡态+一个中间体，必须画两峰一谷 | 如何从能量图判断反应有几步？ |
| 中间体能量画得低于反应物 | 混淆了中间体和产物 | 四面体中间体是活性中间体，能量应高于反应物（否则反应物会自发转化为中间体） | 中间体和过渡态有什么区别？ |