---
title: "题-物电-01-Nernst方程计算"
aliases: ["题-物电-01"]
type: 题目
fidelity: 自编
difficulty: 3
teaching_level: 巩固
source: "教学改编（电化学基础讲义 §Nernst）"
module: "电化学"
subject: 物理化学
syllabus_codes: ["10"]
knowledge_points: ["[[Nernst方程]]", "[[标准电极电势]]", "[[电极]]"]
tags: [化竞, 题目, 物理化学, 电化学]
updated: 2026-08-04
status: 已填充
exam_stage: 初赛
subject_module: 化学原理
pack: 章节练习
---
# 题-物电-01：Nernst 方程计算电极电势

## 题目

计算 298 K 时 Zn²⁺/Zn 电极在 $[\mathrm{Zn^{2+}}] = 0.10$ mol/L 下的电极电势。已知 $E^\theta(\mathrm{Zn^{2+}/Zn}) = -0.762$ V，$F = 96485$ C/mol。

## 参考答案

Nernst 方程（298 K 简式，n = 2）：

$$E = E^\theta + \frac{0.0592}{n}\lg[\mathrm{Zn^{2+}}] = -0.762 + \frac{0.0592}{2}\lg(0.10) = -0.762 + 0.0296\times(-1) = -0.792\ \mathrm{V}$$

**答案**：$E = -0.792$ V。

> **核心辨析**：电极电势随离子浓度降低而变负（氧化型浓度小，还原能力增强）。写 Nernst 式时还原型（Zn 固体）不写入，活度取 1。

## 知识点映射

- [[Nernst方程]] · [[标准电极电势]] · [[电极]]
- 易错点：n 是转移电子数；固体/纯液体活度为 1 不写入；浓度降低 10 倍 n=2 时电势变负 0.0296 V
