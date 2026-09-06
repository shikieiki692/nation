---
title: 题-290-Clayden-Ch9-P8-四原料合成三目标分子
type: 题目
fidelity: 原书逐字
submodule: 有机金属试剂
exam_stage: 初赛
source_subject: 有机化学
difficulty: 4
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[逆合成分析]]", "[[Grignard试剂]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch9-P8]
source: Clayden Organic Chemistry 2nd Ed. Chapter 9 Problem 8
cross_references: ["[[题-286-Clayden-Ch9-P4-庚-2-酮蜂信息素两种合成]]", "[[题-288-Clayden-Ch9-P6-Rioprostil前体醇合成设计]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 模块习题集
source_category: 教材课后习题
---
# 题-290: 四原料合成三目标分子

## 题目

**【中文】**如何利用四种商品化起始原料（苯甲醛、碘乙烷、环戊基溴、CO₂）合成以下三个化合物？

**【原文】**
How could you use these four commercially available starting materials

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/19413417ed7b8c01f5980fb79ee63e1385bbb8437194836b159d50d53170c7b9.jpg]]

to make the following three compounds?

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/1e887457003d14bf8ca65c2c73da7f4bc2ba5d5592ad1be6ab25b39e5498cd95.jpg]]

## 参考答案

**Answer (English)**: The first compound contains a phenyl and an ethyl group, so you could convert the ethyl iodide to a Grignard reagent and add it to the aldehyde. The product is an alcohol, so you need to use CrO₃ to oxidize it to the ketone. The second compound is a carboxylic acid, which can come from addition of the Grignard reagent derived from cyclopentyl bromide to carbon dioxide. The third compound is a tertiary alcohol, which you could make by addition of the same cyclopentyl Grignard reagent to a ketone. The ketone will also need to be made by oxidation of an alcohol, itself derived from benzaldehyde and the cyclopentyl Grignard reagent.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/dbb2a61241ca819d7d2e9b05d1bf7a1a725bd08416ab79fa58d5076c7dc131de.jpg]]
![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/cfcac272d5191d8ce0dfc9c95ab61a84c0226ce620b42b6dab1cd14cf9a015d1.jpg]]
![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/f8c274521fd33d178fcfabd95f1538d87533002bbd3f7b453ed0e48876a66827.jpg]]

**中文解析**：

关键分析：

**目标(a)：苯乙酮（1-苯基乙酮）**
- 含苯基 + 乙基 + 酮。逆合成：酮 → 仲醇（CrO₃ 氧化）→ 乙基 Grignard（EtMgBr，由 EtI 制备）+ 苯甲醛
- 路线：EtI → EtMgBr → + PhCHO → PhCH(OH)Me → CrO₃ → PhCOMe

**目标(b)：环戊基甲酸**
- 含环戊基 + 羧酸。逆合成：羧酸 → Grignard + CO₂
- 路线：环戊基溴 → 环戊基 MgBr → + CO₂ → 环戊基 CO₂H

**目标(c)：二环戊基苯甲醇（叔醇）**
- 含两个环戊基 + 苯基 + 叔醇。逆合成：叔醇 → 酮 + Grignard。酮由苯甲醛 + 环戊基 Grignard → 仲醇 → CrO₃ 氧化得到。然后第二个环戊基 Grignard 加成到酮上
- 路线：环戊基溴 → 环戊基 MgBr → (1) + PhCHO → 仲醇 → CrO₃ → 环戊基苯基酮 → (2) + 环戊基 MgBr → 目标叔醇

> **核心策略**：四种原料反复使用，通过 Grignard 试剂的不同组合构建三个不同复杂度的分子。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[逆合成分析]] | 多目标分子的逆合成拆分策略 | 直接 |
| [[Grignard试剂]] | Grignard 试剂与醛、酮、CO₂ 的三类反应 | 直接 |
| [[C-C键形成]] | 通过 Grignard 加成构建三种不同类型的 C-C 键 | 间接 |

## 解题思路

1. **读题定位**：四种原料（PhCHO、EtI、环戊基 Br、CO₂）→ 三个目标分子。分析每个目标的碳骨架组成，匹配可用的原料
2. **🔑 关键转换**：(a) 酮 = 仲醇氧化 → 乙基 Grignard + 苯甲醛；(b) 羧酸 = Grignard + CO₂ → 环戊基 Grignard + CO₂；(c) 叔醇 = 酮 + Grignard → 环戊基苯基酮 + 环戊基 Grignard（酮本身由苯甲醛 + 环戊基 Grignard + CrO₃ 制备）
3. **验证**：检查每个目标的碳原子数和连接方式，确认所有原料均可从四种起始物获得

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 目标(b) 误用 Grignard + 醛再氧化 | 羧酸碳的氧化态比酮更高 | Grignard + CO₂ 是直接制备羧酸的方法 | 为什么 CO₂ 是合成羧酸的特殊试剂？ |
| 目标(c) 忽略需要两当量 Grignard | 叔醇含两个相同取代基 | 第一个环戊基进入酮（由第一步合成），第二个以 Grignard 形式加入 | 如何控制 Grignard 只加成一次？ |
| 未识别原料可以反复使用 | 认为每种原料只能用一次 | 环戊基溴在(a)和(c)中都被使用（转化为 Grignard） | 什么是"收敛式合成"？ |