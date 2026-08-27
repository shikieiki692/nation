---
title: "题-物动-02-Arrhenius求活化能"
aliases: ["题-物动-02"]
type: 题目
fidelity: 自编
difficulty: 3
teaching_level: 巩固
source: "教学改编（化学动力学讲义 §三 Arrhenius）"
module: "化学动力学"
subject: 物理化学
syllabus_codes: ["08"]
knowledge_points: ["[[Arrhenius方程]]", "[[活化能]]", "[[化学动力学]]"]
tags: [化竞, 题目, 物理化学, 动力学]
updated: 2026-08-04
status: 已填充
exam_stage: 初赛
subject_module: 化学原理
pack: 章节练习
---
# 题-物动-02：Arrhenius 方程求活化能

## 题目

某一级反应在 300 K 时速率常数 $k_1 = 2.0\times10^{-3}\ \mathrm{s^{-1}}$，在 320 K 时 $k_2 = 8.0\times10^{-3}\ \mathrm{s^{-1}}$。求活化能 $E_a$（设 $E_a$ 与 $A$ 在此温度范围内不变）。

## 参考答案

Arrhenius 对数式：

$$\ln\frac{k_2}{k_1} = -\frac{E_a}{R}\left(\frac{1}{T_2}-\frac{1}{T_1}\right)$$

$$\ln\frac{8.0\times10^{-3}}{2.0\times10^{-3}} = \ln 4 = 1.386 = -\frac{E_a}{8.314}\left(\frac{1}{320}-\frac{1}{300}\right)$$

$\dfrac{1}{320}-\dfrac{1}{300} = -2.083\times10^{-4}$，代入：

$$1.386 = \frac{E_a}{8.314}\times 2.083\times10^{-4}\ \Rightarrow\ E_a = \frac{1.386\times 8.314}{2.083\times10^{-4}} = 5.53\times10^{4}\ \mathrm{J/mol} \approx 55\ \mathrm{kJ/mol}$$

**答案**：$E_a \approx 55$ kJ/mol。

> **核心辨析**：$\ln k$ 对 $1/T$ 作图得直线，斜率 $=-E_a/R$。两组数据即可解 $E_a$；升温 20 K 使速率提高 4 倍，对应活化能约 55 kJ/mol——中等活化能的典型表现。

## 知识点映射

- [[Arrhenius方程]] · [[活化能]] · [[化学动力学]]
- 易错点：$T$ 用开尔文；两组数据务必区分 T₁/T₂ 与 k₁/k₂ 的对应关系
