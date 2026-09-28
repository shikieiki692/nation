---
title: "Cannizzaro反应的同位素示踪与速率方程"
aliases: [Cannizzaro反应, 苯甲醛歧化, 同位素示踪, Cannizzaro动力学]
type: 题目
status: 已填充
year: 2022
source: "第34届中国化学奥林匹克初赛"
type_tag: "机理与动力学"
difficulty: 3
knowledge_points: ["[[Cannizzaro反应]]", "[[醛酮化学]]", "[[同位素示踪]]", "[[反应动力学]]"]
tags: [化竞, 真题, 有机化学, Cannizzaro反应, 反应动力学]
related_notes:
  - "[[专题-羰基化学与缩合反应]]"
updated: 2026-09-24
teaching_level: 巩固
fidelity: 原题
exam_stage: 初赛
subject_module: 有机化学
pack: 初赛专项
source_category: 竞赛导向·真题（全国初赛）
source_grade: A
source_tier: 1
source_norm: "第34届初赛"
---
# Cannizzaro反应的同位素示踪与速率方程

## 题目

Cannizzaro（康尼查罗）反应是醛在强碱浓溶液中发生的歧化反应。以苯甲醛为底物，根据所给条件和信息，回答以下问题：

1. 当反应在重水 $\\mathrm{D_2O}$ 中进行，产物苯甲醇是否含有氘？
2. 当反应在 $\\mathrm{H_2^{18}O}$ 中进行，画出含 $^{18}\\mathrm{O}$ 产物的结构简式。
3. 动力学研究发现，该反应的速率方程可以表达为

$$
v = k_a[\\mathrm{PhCHO}]^2[\\mathrm{OH^-}] + k_b[\\mathrm{PhCHO}]^2[\\mathrm{OH^-}]^2
$$

解释此方程中出现这两项的原因。

## 参考答案

**(1) 有氘，但不形成 C-D 键。**

负氢转移后得到 $\\mathrm{PhCH_2O^-}$，它从 $\\mathrm{D_2O}$ 获取 D，产物可写为 $\\mathrm{PhCH_2OD}$。苯甲醇苄位的两个氢仍来自苯甲醛中的 C-H 键/负氢转移，不会因溶剂为重水而全部变成 D。

**(2) 含 $^{18}\\mathrm{O}$ 的产物。**

最直接的标记产物是 $\\mathrm{PhCO^{18}O^-}$，即 $^{18}\\mathrm{OH^-}$ 亲核进攻苯甲醛后，以羧酸根羰基氧的形式保留下来。由于羟基对羰基的加成可逆，苯甲醛原有氧与溶剂氧可以交换，因此苯甲酸根的两个氧及苯甲醇的氧也可能分别被 $^{18}\\mathrm{O}$ 标记。

**(3) 两项对应两条并行的预平衡路径。**

负氢迁移是决速步，反应物为一分子四面体中间体和另一分子 $\\mathrm{PhCHO}$。两个快平衡分别形成：

- 单负离子中间体 $\\mathrm{T_1}$：$[\\mathrm{T_1}]=K_1[\\mathrm{PhCHO}][\\mathrm{OH^-}]$
- 双负离子中间体 $\\mathrm{T_2}$：$[\\mathrm{T_2}]=K_2[\\mathrm{PhCHO}][\\mathrm{OH^-}]^2$

于是

$$
v=k_1[\\mathrm{PhCHO}][\\mathrm{T_1}]
 +k_2[\\mathrm{PhCHO}][\\mathrm{T_2}]
$$

整理后正好得到题目中的两项：第一项对 $\\mathrm{PhCHO}$ 为二级、对 $\\mathrm{OH^-}$ 为一级；第二项对 $\\mathrm{PhCHO}$ 为二级、对 $\\mathrm{OH^-}$ 为二级。

## 解析

### 核心机理

1. $\\mathrm{OH^-}$ 可逆进攻苯甲醛羰基，形成四面体单负离子；进一步去质子形成双负离子。
2. 四面体中间体向另一分子苯甲醛转移 $\\mathrm{H^-}$，一分子被氧化为苯甲酸根，另一分子被还原为苯甲醇负离子。
3. 苯甲醇负离子与溶剂快速发生质子/氘交换。

### 易错点

- “含氘”不等于形成 C-D 键；本题的氘主要出现在 O-D。
- 不能只画出一种 $^{18}\\mathrm{O}$ 产物而忽略羰基氧交换。
- 速率方程中的 $[\\mathrm{OH^-}]^2$ 不代表决速步必须同时碰撞两分子 $\\mathrm{OH^-}$，它可来自决速步之前形成双负离子的预平衡。

## 来源说明

题干按第34届中国化学奥林匹克初赛第9-2题恢复；同一题也收录于 ABOC 第4章自学练习 4.13.1。参考答案依据第34届初赛官方解析并校正“氘进入羟基而非苄位 C-H”的表述。
