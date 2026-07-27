---
title: 题-002-Nernst方程求Ksp
aliases: [AgCl Ksp测定]
type: 题目
difficulty: 4
teaching_level: 拓展
source: 经典例题
subject: 化学原理
module: 化学原理
syllabus_codes: [8]
knowledge_points: ["[[Nernst方程]]", "[[标准电极电势]]", "[[溶度积]]"]
tags: [化竞, 电化学, Ksp测定]
updated: 2026-05-03
status: 已填充
exam_stage: 初赛
---
# 题-002：Nernst 方程求 Ksp## 题目> 来源：经典例题已知 $E^\circ(\mathrm{Ag^+/Ag}) = +0.799\text{ V}$，$E^\circ(\mathrm{AgCl/Ag}) = +0.222\text{ V}$。求 AgCl 的 $K_{sp}$（25°C）。## 参考答案AgCl/Ag 电极反应：$\mathrm{AgCl} + e^- \rightarrow \mathrm{Ag} + \mathrm{Cl}^-$其标准态对应 $[\mathrm{Cl}^-] = 1\text{ mol/L}$，此时 $[\mathrm{Ag}^+] = K_{sp}$。对 $\mathrm{Ag^+} + e^- \rightarrow \mathrm{Ag}$ 应用 Nernst 方程：$$E = 0.799 + 0.0592\lg[\mathrm{Ag}^+]$$当 $[\mathrm{Cl}^-] = 1$ 时，$[\mathrm{Ag}^+] = K_{sp}$，且 $E = 0.222\text{ V}$：$$0.222 = 0.799 + 0.0592\lg K_{sp}$$$$\lg K_{sp} = \frac{0.222 - 0.799}{0.0592} = -9.75$$$$K_{sp} = 1.8 \times 10^{-10}$$## 知识点映射- [[Nernst方程]] — 非标态电极电势与浓度的关系- [[标准电极电势]] — 两个相关电极的 E° 差值- [[溶度积]] — Ksp 的电化学测定法## 解题思路1. 写出两个电极的 Nernst 方程2. 在特定条件下（[Cl⁻]=1）联立3. 利用 $E^\circ$ 差值求解 $\lg K_{sp}$## 易错分析- 混淆 $E^\circ(\mathrm{AgCl/Ag})$ 和 $E^\circ(\mathrm{Ag^+/Ag})$ 的关系- 忘记 $E^\circ(\mathrm{AgCl/Ag})$ 对应 [Cl⁻] = 1 mol/L