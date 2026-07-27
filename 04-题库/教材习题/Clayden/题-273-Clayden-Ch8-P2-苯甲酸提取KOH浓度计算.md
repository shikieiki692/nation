---
title: 题-273-Clayden-Ch8-P2-苯甲酸提取KOH浓度计算
type: 题目
submodule: 酸碱质子理论
exam_stage: 初赛
subject: 有机化学
difficulty: 2
teaching_level: 巩固
syllabus_codes: []
knowledge_points: ["[[pKa]]", "[[酸碱质子理论]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch8-P2]
source: Clayden Organic Chemistry 2nd Ed. Chapter 8 Problem 2
cross_references: ["[[题-272-Clayden-Ch8-P1-萘吡啶对甲苯甲酸混合物分离]]", "[[题-279-Clayden-Ch8-P8-五个苯酚pKa值排序]]", "[[题-328-Clayden-Ch20-P1-羰基化合物烯醇式绘制和稳定性]]"]
module: 有机化学
status: 已填充
---
# 题-273: 苯甲酸提取KOH浓度计算

## 题目

How concentrated must a KOH solution be to keep the pH above the pKa of benzoic acid (4.2)?

**原文题目**：用KOH溶液提取苯甲酸（pKa = 4.2），KOH浓度需要多高才能使pH始终高于苯甲酸的pKa？

## 参考答案

**Answer (English)**: If the pH drops below pKa (4.2), benzoic acid becomes protonated and loses water solubility. To keep pH ≥ 4.2, a very dilute KOH solution (10⁻⁹ M) would technically suffice at equilibrium (giving pH 5), but the volume required would be impractically large. In practice, use 0.1 M KOH — for 1.22 g (0.01 mol) of PhCO2H, approximately 100 mL of 0.1 M KOH is needed.

**中文解析**：
1. **pH与pKa的关系**：苯甲酸pKa = 4.2。当pH > pKa时，苯甲酸以去质子化的苯甲酸根形式存在（水溶性好）；当pH < pKa时，苯甲酸以质子化的酸形式存在（不溶于水）。
2. **理论最低浓度**：若仅需pH > 4.2，则pH = 5时[OH⁻] = 10⁻⁹ M，即极稀的KOH即可。但此浓度下体积极大，不实用。
3. **实际操作**：用0.1 M KOH，对于1.22 g（0.01 mol）苯甲酸，需约100 mL 0.1 M KOH（恰好中和），此时pH远高于pKa，确保完全萃取。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[pKa]] | pH与pKa关系决定酸碱存在形式 | 直接 |
| [[酸碱质子理论]] | 萃取时酸碱平衡的实际应用 | 直接 |
| [[酸碱强度]] | 弱酸的pKa与萃取效率的关系 | 间接 |

## 解题思路

1. **读题定位**：苯甲酸pKa = 4.2，需用KOH将其去质子化使其溶于水，要求pH > pKa。
2. **🔑 关键转换**：pH > pKa时，[A⁻]/[HA] = 10^(pH-pKa)，pH只需略高于4.2即可。但实际需足够碱量完全中和。
3. **验证**：0.1 M KOH × 0.1 L = 0.01 mol，恰好中和0.01 mol苯甲酸，确保完全萃取。

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 认为pH需远高于pKa | pH高于pKa约1-2个单位即有90%以上去质子化 | 只需pH > pKa，但实际需足够碱量 | pH = 5时苯甲酸去质子化比例是多少？ |
| 忽略体积实用性 | 理论计算与实际操作差异 | 用0.1 M KOH等实用浓度 | 为什么不用极稀的碱？ |
| 混淆pKa与pH | pKa是常数，pH随溶液变化 | 明确pKa是酸的固有性质，pH是溶液性质 | pKa和pH有什么区别？ |