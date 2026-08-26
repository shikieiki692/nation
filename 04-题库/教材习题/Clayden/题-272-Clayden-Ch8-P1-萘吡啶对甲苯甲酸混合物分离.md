---
title: 题-272-Clayden-Ch8-P1-萘吡啶对甲苯甲酸混合物分离
type: 题目
fidelity: 原书逐字
submodule: 酸碱质子理论
exam_stage: 初赛
subject: 有机化学
difficulty: 2
teaching_level: 巩固
syllabus_codes: []
knowledge_points: ["[[酸碱质子理论]]", "[[pKa]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch8-P1]
source: Clayden Organic Chemistry 2nd Ed. Chapter 8 Problem 1
cross_references: ["[[题-273-Clayden-Ch8-P2-苯甲酸提取KOH浓度计算]]", "[[题-279-Clayden-Ch8-P8-五个苯酚pKa值排序]]", "[[题-328-Clayden-Ch20-P1-羰基化合物烯醇式绘制和稳定性]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 章节练习
---
# 题-272: 萘/吡啶/对甲苯甲酸混合物分离

## 题目

Separate a mixture of naphthalene, pyridine, and p-toluic acid into its three components.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/b689ebe8b19cc4808e9a4229f11e1396bd05c29e24f1e4a1c7ce3024e8b45d75.jpg]]

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/a64696d78f1ea1dc564a3b95c5e5d23fb04573ec2a537a04834ad9d0116de806.jpg]]

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/0be07abe76d120d368972a992feae8330394150452833ff1e36dee74dd7e24a3.jpg]]

**原文题目**：分离萘、吡啶和对甲苯甲酸的混合物，得到三个独立的组分。

## 参考答案

**Answer (English)**: Dissolve the mixture in diethyl ether (Et2O). Extract with aqueous acid (e.g., dilute HCl) to remove pyridine (pKa of pyridinium ≈ 5.5, protonated by acid and extracted into aqueous layer). Then extract the remaining ether solution with aqueous NaHCO3 to remove p-toluic acid (pKa ≈ 4.5, deprotonated by base and extracted into aqueous layer). Naphthalene remains in the ether layer — it is neither acidic nor basic.

**中文解析**：
1. **吡啶**（pKa ≈ 5.5）是碱性氮杂环，可用稀酸（如HCl）质子化，生成水溶性盐，从有机相转移至水相。
2. **对甲苯甲酸**（pKa ≈ 4.5）是弱酸，可用NaHCO3去质子化（苯甲酸pKa < H2CO3 pKa ≈ 6.4），生成水溶性羧酸盐，从有机相转移至水相。
3. **萘**是中性烃，既无酸性也无碱性，留在乙醚层中，蒸干乙醚即可得到。
4. 分离顺序：先酸后碱（先除去碱性的吡啶，再除去酸性的对甲苯甲酸），避免吡啶和酸反应干扰后续操作。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[酸碱质子理论]] | 判断分子酸碱性并选择分离试剂 | 直接 |
| [[pKa]] | 比较各组分pKa确定分离策略 | 直接 |
| [[有机酸碱性]] | 吡啶碱性、对甲苯甲酸酸性的本质 | 间接 |

## 解题思路

1. **读题定位**：三种物质——萘（中性）、吡啶（碱性，pKa ~ 5.5）、对甲苯甲酸（酸性，pKa ~ 4.5），需利用酸碱性差异进行萃取分离。
2. **🔑 关键转换**：先用酸萃取吡啶（碱 → 盐），再用NaHCO3萃取对甲苯甲酸（酸 → 盐），最后剩余中性的萘。
3. **验证**：各组分pKa与萃取试剂匹配，吡啶可被稀酸质子化，对甲苯甲酸可被弱碱NaHCO3去质子化（不能用NaOH，因为会同时萃取残留物）。

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 用NaOH代替NaHCO3萃取 | NaOH碱性过强，可能萃取吡啶或残留有机物 | 用NaHCO3，仅去质子化羧酸 | 为什么不能用NaOH？ |
| 先加碱后加酸的顺序 | 吡啶先与酸反应会重新形成盐 | 应先酸萃取吡啶，再碱萃取酸 | 如果顺序反了会怎样？ |
| 认为萘有酸碱性 | 萘是中性芳烃，pKa极高（~43），不参与萃取 | 萘留在有机层即可 | 萘的pKa为什么这么高？ |