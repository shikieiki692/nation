---
title: 题-299-Clayden-Ch15-P1-SN1与SN2机理判断
type: 题目
fidelity: 原书逐字
submodule: 亲核取代反应
exam_stage: 初赛
source_subject: 有机化学
difficulty: 2
question_type: [机理]
teaching_level: 巩固
syllabus_codes: ["3.2"]
knowledge_points: ["[[SN1反应]]", "[[SN2反应]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch15-P1]
source: Clayden Organic Chemistry 2nd Ed. Chapter 15 Problem 1
cross_references: ["[[题-301-Clayden-Ch15-P3-SN1与SN2微妙选择]]", "[[题-310-Clayden-Ch17-P1-两个消除反应机理]]", "[[题-312-Clayden-Ch17-P3-消除区域选择性]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 章节练习
source_category: 教材课后习题
---
# 题-299: SN1与SN2机理判断

## 题目

Two reactions are given. For each, suggest a mechanism:

1. PhSH + NaOH, then MeOMe → PhSMe + NaOMe
2. t-BuOH + methanesulfonic acid → t-BuOMs + H₂O

**原文题目**：

为下列反应提出合理的机理：

1. 硫酚 (PhSH) 与 NaOH 反应后，再与甲基甲醚 (MeOMe) 反应生成硫醚 (PhSMe) 和 NaOMe
2. 叔丁醇 (t-BuOH) 与甲磺酸反应生成甲磺酸叔丁酯 (t-BuOMs) 和水

## 参考答案

**Answer (English)**:

1. NaOH deprotonates PhSH (pKa ~7) to give PhS⁻, a good nucleophile. PhS⁻ then performs an SN2 attack on MeOMe (methyl substrate), displacing MeO⁻ to give PhSMe.

2. Methanesulfonic acid protonates t-BuOH to give t-BuOH₂⁺. The water leaving group departs to form the tertiary carbocation t-Bu⁺, which is then captured by the methanesulfonate anion (MsO⁻) in an SN1 step to give t-BuOMs.

**中文解析**：

1. **反应一（SN2）**：NaOH 是强碱，将硫酚 (pKa ≈ 7) 去质子化生成硫酚负离子 PhS⁻。PhS⁻ 是一个很好的亲核试剂（硫原子极化率高），对甲基底物 MeOMe 发起 SN2 进攻，从背面进攻甲基碳，同时甲氧基作为离去基团离开，生成硫醚 PhSMe。甲基底物是最理想的 SN2 底物，空间位阻最小。

2. **反应二（SN1）**：甲磺酸 (MsOH) 是强酸，首先将叔丁醇的羟基质子化，生成烷基氧鎓离子 t-BuOH₂⁺。由于叔丁基碳阳离子 (t-Bu⁺) 非常稳定（三个甲基的超共轭和诱导效应），水分子作为离去基团很容易离去，形成碳阳离子。随后甲磺酸根负离子 (MsO⁻) 捕获碳阳离子，生成甲磺酸叔丁酯。这是一个典型的 SN1 机理。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| SN1反应 | 叔碳底物+强酸条件下的SN1机理 | 直接 |
| SN2反应 | 甲基底物的SN2机理及亲核试剂选择 | 直接 |
| [[亲核取代]] | SN1与SN2的判断依据 | 间接 |

## 解题思路

1. **读题定位**：识别底物结构——甲基底物倾向SN2，叔碳底物倾向SN1；注意碱/酸条件对机理选择的影响
2. **🔑 关键转换**：反应一：PhSH的去质子化 (pKa 7, NaOH可完成) → PhS⁻ 的SN2进攻；反应二：ROH质子化 → H₂O离去 → 碳阳离子捕获
3. **验证**：SN2产物构型翻转（甲基无手性）；SN1产物外消旋化（叔碳碳阳离子平面结构）

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 反应一认为是SN1 | 忽视了甲基底物完全不支持SN1 | 甲基碳阳离子极不稳定，只能走SN2 | 为什么甲基底物不能走SN1？ |
| 反应二认为是SN2 | 叔碳底物空间位阻太大，SN2极慢 | 叔碳碳阳离子稳定，优先SN1 | 如果将叔丁醇换成乙醇，机理如何变化？ |
| 忽略NaOH的去质子化步骤 | 认为PhSH直接进攻 | 硫酚pKa=7，NaOH可完全去质子化 | 硫酚和醇的酸性哪个更强？为什么？ |