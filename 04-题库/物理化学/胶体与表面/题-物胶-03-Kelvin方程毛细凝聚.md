---
title: "题-物胶-03-Kelvin方程毛细凝聚"
aliases: ["题-物胶-03"]
type: 题目
fidelity: 原书逐字
difficulty: 4
teaching_level: 挑战
source: "教学改编（胶体与表面物理化学讲义 §三 表面）"
module: "胶体与表面"
subject: 物理化学
syllabus_codes: ["04"]
knowledge_points: ["[[表面张力]]", "[[吸附]]", "[[Kelvin方程]]"]
tags: [化竞, 题目, 物理化学, 表面化学, Kelvin]
updated: 2026-08-04
status: 已填充
exam_stage: 决赛
subject_module: 元素与分析
pack: 模块习题集
---
# 题-物胶-03：Kelvin 方程与弯曲液面蒸气压

## 题目

298 K 时水的饱和蒸气压 $p_0 = 3.17$ kPa，表面张力 $\gamma = 0.072$ N/m，密度 $\rho = 1000$ kg/m³，摩尔质量 $M = 0.018$ kg/mol。求半径 $r = 10$ nm 的**凸液面**与**凹液面**水的蒸气压（$R = 8.314$ J·mol⁻¹·K⁻¹）。

## 参考答案

Kelvin 方程：

$$\ln\frac{p}{p_0} = \frac{2\gamma M}{RT\rho}\cdot\frac{1}{r}\ \ (\text{凸液面取 +，凹液面取 −})$$

$$\frac{2\gamma M}{RT\rho} = \frac{2\times 0.072\times 0.018}{8.314\times 298\times 1000} = \frac{2.592\times10^{-3}}{2.478\times10^{6}} = 1.046\times10^{-9}\ \mathrm{m}$$

**凸液面**（$+$）：

$$\ln\frac{p}{p_0} = \frac{1.046\times10^{-9}}{10\times10^{-9}} = 0.1046\ \Rightarrow\ \frac{p}{p_0} = 1.110\ \Rightarrow\ p = 3.52\ \mathrm{kPa}$$

**凹液面**（$-$）：$p/p_0 = e^{-0.1046} = 0.901 \Rightarrow p = 2.86$ kPa。

**答案**：凸液面 $p \approx 3.52$ kPa（升高 11%）；凹液面 $p \approx 2.86$ kPa（降低 10%）。

> **核心辨析**：弯曲液面蒸气压——凸面升高、凹面降低。毛细凝聚（凹面蒸气压低、易凝结）、微小液滴难形成（凸面蒸气压高、蒸发快）都源于此。纳米尺度（10 nm）效应已显著。

## 知识点映射

- [[表面张力]] · [[吸附]]
- 易错点：凸/凹取号；$r$ 用米；$M$ 用 kg/mol；单位一致避免数量级错误
