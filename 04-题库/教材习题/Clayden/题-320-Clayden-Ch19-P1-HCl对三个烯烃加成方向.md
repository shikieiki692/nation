---
title: 题-320-Clayden-Ch19-P1-HCl对三个烯烃加成方向
type: 题目
fidelity: 原书逐字
submodule: 烯烃的亲电加成
exam_stage: 初赛
source_subject: 有机化学
difficulty: 2
teaching_level: 巩固
syllabus_codes: ["2.3"]
knowledge_points: ["[[亲电加成]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch19-P1]
source: Clayden Organic Chemistry 2nd Ed. Chapter 19 Problem 1
cross_references: ["[[题-324-Clayden-Ch19-P5-HBr加成后SN1水解（镇静剂合成）]]", "[[题-327-Clayden-Ch19-P8-烯烃区域立体选择性转化试剂选择]]", "[[题-392-Clayden-Ch22-P2-共轭加成本质和不发生的情况]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 章节练习
source_category: 教材课后习题
---
# 题-320: HCl对三个烯烃加成方向

## 题目

Predict the products of the addition of HCl to each of the following alkenes:

1. Propene (CH₂=CHCH₃)
2. 2-Methylpropene (CH₂=C(CH₃)₂)
3. Styrene (PhCH=CH₂)

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/b378e5ac6c79f01882743a021d1fa1507a55b283a3418da1c6ba6654e1dd3700.jpg]]

**原文题目**：

预测 HCl 与下列各烯烃加成的产物：

1. 丙烯 (CH₂=CHCH₃)
2. 2-甲基丙烯 (CH₂=C(CH₃)₂)
3. 苯乙烯 (PhCH=CH₂)

## 参考答案

**Answer (English)**:

1. **Propene**: HCl adds to give 2-chloropropane (CH₃CHClCH₃). The proton adds to the terminal carbon to give the secondary carbocation (more stable), which is then captured by Cl⁻.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/e605a863f6c30d7a74020a00ef52052a9b156f620dbdd820c2f01a1db11ed485.jpg]]

2. **2-Methylpropene**: HCl adds to give 2-chloro-2-methylpropane (t-BuCl, (CH₃)₃CCl). Protonation gives the tertiary carbocation, the most stable option.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/e3af42fda21dc5f906fa19c87502dd500c09692c87ea403e2039a7c59e60d983.jpg]]

3. **Styrene**: HCl adds to give 1-chloro-1-phenylethane (PhCHClCH₃). Protonation at the terminal carbon gives the benzylic carbocation, stabilized by resonance with the benzene ring.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/0d8962dd79dde7f33045766c4a7399eb42a3594f8ff9674a20dfe164d621baf5.jpg]]

**中文解析**：

HCl 对烯烃的加成遵循 **Markovnikov 规则**：氢加到含氢较多的碳上（即取代程度较低的碳），卤素加到取代程度较高的碳上。其本质是反应通过更稳定的碳阳离子中间体进行。

1. **丙烯**：H⁺ 加到 C-1（含 2 个 H），形成仲碳阳离子 CH₃C⁺HCH₃。Cl⁻ 捕获后生成 2-氯丙烷（仲碳产物）。若 H⁺ 加到 C-2 则形成极不稳定的伯碳阳离子。
2. **2-甲基丙烯**：H⁺ 加到 C-1，形成叔碳阳离子 (CH₃)₃C⁺，这是三个甲基超共轭稳定化的三级碳阳离子，非常稳定。Cl⁻ 捕获得叔丁基氯。
3. **苯乙烯**：H⁺ 加到 C-1（CH₂端），形成苄基碳阳离子 PhC⁺HCH₃。苄基碳阳离子通过苯环共振稳定，稳定性远超对位伯碳阳离子。Cl⁻ 捕获得 1-氯-1-苯基乙烷。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[亲电加成]] | HCl对烯烃亲电加成的基本机理：质子化→碳阳离子→亲核捕获 | 直接 |
| [[Markovnikov规则]] | Markovnikov取向的碳阳离子稳定性解释 | 直接 |
| [[烯烃]] | 烯烃电子密度分布与亲电试剂进攻位点 | 间接 |

## 解题思路

1. **读题定位**：每个烯烃都需要判断 HCl 加成的区域选择性——H 和 Cl 分别加在哪个碳上
2. **🔑 关键转换**：确定质子化后形成的碳阳离子——选取代程度更高的碳阳离子（2° > 1°，3° > 2°，苄基 > 仲碳）
3. **验证**：检查每个产物中 Cl 所在碳的取代度是否最高；苄基碳阳离子因共振稳定可优先于普通仲碳

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 丙烯加成产物写成1-氯丙烷 | 没有应用Markovnikov规则 | 反马产物需要过氧化物条件（仅HBr） | 为什么HCl加成不存在过氧化物效应？ |
| 苯乙烯产物写成β-氯乙苯 | 未考虑苄基碳阳离子的特殊稳定性 | H⁺加到CH₂端→苄基碳阳离子→Cl捕获在α位 | 苄基碳阳离子为什么特别稳定？ |
| 认为所有烯烃加成都一样 | 不同烯烃碳阳离子稳定性差异巨大 | 逐个分析可能的碳阳离子，选最稳定的路径 | 三级碳阳离子比二级碳阳离子稳定多少？ |