---
title: "题-物平-02-van'tHoff温度影响"
aliases: ["题-物平-02"]
type: 题目
fidelity: 原书逐字
difficulty: 3
teaching_level: 巩固
source: "教学改编（物化综合计算讲义 §〇 前置概念）"
module: "化学平衡"
subject: 物理化学
syllabus_codes: ["07", "04"]
knowledge_points: ["[[van't Hoff方程]]", "[[范特霍夫方程]]", "[[平衡常数]]", "[[焓变]]"]
tags: [化竞, 题目, 物理化学, 化学平衡, van'tHoff]
updated: 2026-08-04
status: 已填充
exam_stage: 决赛
subject_module: 化学原理
pack: 章节练习
---
# 题-物平-02：van't Hoff 方程——温度对平衡常数的影响

## 题目

某反应在 298 K 时平衡常数 $K_1 = 1.0\times10^{3}$，反应的标准焓变 $\Delta_rH^\circ = -92.2$ kJ/mol（设在此温度范围内为常数）。求 500 K 时的平衡常数 $K_2$。（$R = 8.314$ J·mol⁻¹·K⁻¹）

## 参考答案

van't Hoff 积分式：

$$\ln\frac{K_2}{K_1} = -\frac{\Delta_rH^\circ}{R}\left(\frac{1}{T_2}-\frac{1}{T_1}\right)$$

代入：

$$\ln\frac{K_2}{1.0\times10^3} = -\frac{(-92.2\times10^3)}{8.314}\left(\frac{1}{500}-\frac{1}{298}\right) = (11090)\times(-1.356\times10^{-3}) = -15.04$$

$$\frac{K_2}{K_1} = e^{-15.04} = 2.9\times10^{-7}\ \Rightarrow\ K_2 = 1.0\times10^{3}\times 2.9\times10^{-7} = 2.9\times10^{-4}$$

**答案**：$K_2 \approx 2.9\times10^{-4}$。

> **核心辨析**：放热反应（ΔH°<0）升温 $K$ 减小——与 Le Châtelier 定性结论一致。van't Hoff 与 Clausius-Clapeyron、Arrhenius 三式同构，区别只在自变量（$K$/$p$/$k$）。

## 知识点映射

- [[van't Hoff方程]] · [[范特霍夫方程]] · [[平衡常数]] · [[焓变]]
- 易错点：ΔH° 负值代入不丢符号；T 用开尔文；$K$ 无单位时按数值比处理
