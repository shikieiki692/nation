---
title: 题-476-Clayden-Ch37-P12-结构分析+自由基官能团化
type: 题目
fidelity: 原书逐字
submodule: 自由基反应
exam_stage: 初赛
subject: 有机化学
difficulty: 3
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[自由基]]"]
tags: [化竞, Clayden, 有机化学, 自由基反应]
updated: 2026-07-25
aliases: [Clayden-Ch37-P12]
source: Clayden Organic Chemistry 2nd Ed. Chapter 37 Problem 12
cross_references: ["[[题-465-Clayden-Ch37-P1-重要自由基反应复习]]", "[[题-466-Clayden-Ch37-P2-重氮盐亲核取代vs自由基对比]]", "[[题-292-Clayden-Ch14-P2-旋光值区分]]", "[[题-291-Clayden-Ch14-P1-五个分子手性判断]]"]
module: 有机化学
status: 已填充
---
# 题-476: 羧酸的自由基双溴化+碱性环化

## 题目

Reaction of this carboxylic acid (C₅H₈O₂) with bromine in the presence of dibenzoyl peroxide gives an unstable compound A (C₅H₆Br₂O₂) that gives a stable compound B (C₅H₅BrO₂) on treatment with base. Compound B has IR 1735 and 1645 cm⁻¹ and NMR δ_H 6.18 (1H, s), 5.00 (2H, s) and 4.18 (2H, s). What is the structure of the stable product B? Deduce the structure of the unstable compound A and mechanisms for the reactions.

CO₂H → [Br₂/(PhCO₂)₂] A → base B

**原文题目**：Reaction of this carboxylic acid (C₅H₈O₂) with bromine in the presence of dibenzoyl peroxide gives an unstable compound A (C₅H₆Br₂O₂) that gives a stable compound B (C₅H₅BrO₂) on treatment with base. Compound B has IR 1735 and 1645 cm⁻¹ and NMR δ_H 6.18 (1H, s), 5.00 (2H, s) and 4.18 (2H, s). What is the structure of the stable product B? Deduce the structure of the unstable compound A and mechanisms for the reactions.

## 参考答案

**Answer (English)**: The starting material is C₅H₈O₂ so the stable compound B has gained a bromine and lost three hydrogens. There must be an extra double bond equivalent (DBE) somewhere in B. The IR spectrum shows that the OH has gone and suggests a carbonyl group, possibly an ester because of the high frequency, and an alkene. The NMR shows that both methyl groups have gone and have been replaced by CH₂ groups. The bromine must be on one of them and the ester oxygen on the other. The extra DBE is a ring.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/b7c5df0a5bc29a884cd991b52805c3c616b07663dbda5123f9aecee9dbe3c10e.jpg]]

Since both methyl groups are functionalized, unstable A must have one Br on each methyl group. The peroxide produces benzoyl radicals that abstract protons from both allylic positions to give stabilized radicals that attack bromine molecules to give bromide radicals to continue the chain reaction. In base the carboxylate cyclizes onto the cis CH₂Br group.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/87a7d790440cf09c0690eb993d42a07a7ae7ffca7d5d64f26df271cc7c139254.jpg]]

**中文解析**：

关键分析：

**产物B的结构鉴定**：
- C₅H₈O₂ → B比原料多一个Br，少三个H → 额外一个DBE
- IR 1735 cm⁻¹ → 酯羰基（高频率）；1645 cm⁻¹ → C=C双键
- NMR：δ 6.18 (1H, s) → 烯氢；δ 5.00 (2H, s) → CH₂（连O）；δ 4.18 (2H, s) → CH₂（连Br）
- 结构：α-亚甲基-γ-丁内酯衍生物（含Br的五元内酯环）

**不稳定中间体A**：
- C₅H₆Br₂O₂ → 两个甲基都被溴化 → 2-亚甲基戊二酸的二溴甲基酯？
- 实际上是2-亚甲基戊二酸的双(溴甲基)中间体

**机理**：
1. **自由基溴化**：过氧化苯甲酰产生苯甲酰氧自由基 → 从两个烯丙位甲基夺氢 → 产生两个烯丙基自由基 → 与Br₂反应 → 二溴代物A
2. **碱性环化**：碱去质子化CO₂H → CO₂⁻ → 进攻顺式的CH₂Br → S_N2环化 → 五元内酯环 + Br⁻

> **注意**：这个例子展示了自由基官能团化（溴化）与离子环化（S_N2）的组合应用。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[自由基]] | 过氧化物引发的自由基烯丙位溴化 | 直接 |
| [[波谱分析]] | 通过IR和NMR推断产物结构 | 直接 |
| [[结构鉴定]] | DBE计算、官能团识别、耦合模式分析 | 间接 |
| 内酯化 | 羧酸根的分子内S_N2环化 | 间接 |

## 解题思路

1. **读题定位**：推断题——通过波谱数据确定B的结构，推导A的结构，写出两个机理
2. **关键转换**：计算DBE → 分析IR确定官能团 → 分析NMR确定连接方式 → 推断B为含Br的五元内酯 → A为双溴代前体 → 自由基溴化+碱性环化机理
3. **验证**：检查B的分子式是否与波谱一致，A→B的转化是否合理（碱性环化消除一个HBr）

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 忘记计算DBE | 没有分析不饱和度变化 | B比原料少3个H多1个Br，DBE增加1 → 额外一个环或双键 | DBE如何计算？ |
| 将1735 cm⁻¹误认为酮 | 没有注意频率偏高 | 1735 cm⁻¹高于典型酮（1715），更可能是酯 | 酯和酮的IR区别是什么？ |
| 画单溴化产物 | 没有分析NMR中两个CH₂ | 两个甲基都被溴化（两个CH₂信号），所以A是二溴代物 | 如何从NMR判断溴化程度？ |
| 环化机理写成SN1 | 没有考虑底物结构 | 羧酸根是强亲核试剂，CH₂Br是好的SN2底物 → 分子内SN2 | 什么条件下SN2比SN1更有利？ |