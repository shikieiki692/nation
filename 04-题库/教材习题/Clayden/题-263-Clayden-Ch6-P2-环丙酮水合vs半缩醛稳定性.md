---
title: 题-263-Clayden-Ch6-P2-环丙酮水合vs半缩醛稳定性
type: 题目
submodule: 羰基亲核加成
exam_stage: 初赛
subject: 有机化学
difficulty: 3
teaching_level: 巩固
syllabus_codes: ["21"]
knowledge_points: ["[[羰基亲核加成]]", "[[半缩醛]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch6-P2]
source: Clayden Organic Chemistry 2nd Ed. Chapter 6 Problem 2
cross_references: ["[[题-266-Clayden-Ch6-P5-茚三酮水合选择性]]", "[[题-267-Clayden-Ch6-P6-羟基酮IR异常→环状半缩醛]]", "[[题-357-Clayden-Ch11-P1-缩醛和亚胺形成机理]]"]
module: 有机化学
status: 已填充
---
# 题-263: 环丙酮水合vs半缩醛稳定性

## 题目

Cyclopropanone exists as the hydrate in water but 2-hydroxyethanal does not exist as the hemiacetal. Explain.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/685c41560ff2ab0455ff8f16a9f130a62530fd294f7a7bffdc74b7b93cbdd035.jpg]]

**原文题目**：环丙酮在水中以水合物形式存在，但2-羟基乙醛不以半缩醛形式存在。解释原因。

## 参考答案

**Answer (English)**: Hydration is an equilibrium reaction. We must consider the effect of the three-membered ring on relative stability. Cyclopropanone is very strained because the sp² carbonyl carbon wants 120° but gets 60° — '60° of strain.' In the hydrate, that carbon becomes sp³, so only about '49° of strain' remains. The hydrate is more stable than the ketone.

For 2-hydroxyethanal: the hydroxy-aldehyde is not strained at all, but the hemiacetal has '49° of strain' at each atom. Even without strain, hemiacetals are usually less stable than their carbonyl forms because one C=O bond is worth more than two C-O bonds. Here the hemiacetal is even less stable and can escape strain by breaking a C-O ring bond.

**中文解析**：

两个案例的关键对比：

**环丙酮→水合物（有利）**：
- 三元环张力大：C=O的sp²碳理想键角120°，实际只有60°，有~60°的角张力
- 水合后sp²→sp³，理想键角109.5°，角张力降为~49°
- 虽然水合物通常不如酮稳定（1个C=O > 2个C-O），但三元环张力释放使平衡偏向水合物

**2-羟基乙醛→半缩醛（不利）**：
- 开链醛无环张力
- 半缩醛形成五元环，每个原子都有~49°角张力
- 且开链醛本身就无张力，半缩醛化不仅得不到张力释放，反而引入了张力
- 加上"1个C=O > 2个C-O"的一般规律，平衡强烈偏向醛

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[羰基亲核加成]] | 水合/半缩醛化作为亲核加成的平衡 | 直接 |
| [[半缩醛]] | 半缩醛稳定性与环张力的关系 | 直接 |
| [[环张力]] | 三元环角张力对平衡的影响 | 直接 |
| [[平衡常数]] | 热力学控制的平衡方向判断 | 间接 |

## 解题思路

1. **读题定位**：两个对比案例——环丙酮水合（发生）vs 2-羟基乙醛半缩醛化（不发生），问为什么
2. **🔑 关键转换**：从环张力角度分析——环丙酮水合释放张力（sp²→sp³使角张力从60°降到49°），而2-羟基乙醛半缩醛化反而引入张力（五元环）
3. **验证**：记住一般规律——水合物/半缩醛通常不如母体羰基化合物稳定，只有在特殊因素（如环张力释放）驱动下才偏向水合物

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 认为水合物总是比酮稳定 | 没有考虑平衡方向 | 通常水合物不如酮稳定（C=O > 2C-O），环丙酮是特例 | 甲醛水合物稳定的原因是什么？ |
| 忘记比较sp²和sp³的角张力 | 没有考虑杂化对键角的影响 | sp²碳在三元环中角张力更大（120°→60° vs 109.5°→60°） | 环丙烯的角张力比环丙烷大还是小？ |
| 忽略"可逃逸"因素 | 没考虑半缩醛可开环 | 2-羟基乙醛的半缩醛可以通过开环消除张力，所以更不稳定 | 什么条件下环状半缩醛会开环？ |