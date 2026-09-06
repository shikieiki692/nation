---
title: "题-物电-02-EθΔGθK全链"
aliases: ["题-物电-02"]
type: 题目
fidelity: 自编
difficulty: 3
question_type: [计算]
teaching_level: 巩固
source: "教学改编（物化综合计算讲义 §四 Nernst 四场景）"
module: "电化学"
source_subject: 物理化学
syllabus_codes: ["10", "06"]
knowledge_points: ["[[Nernst方程]]", "[[Gibbs自由能]]", "[[平衡常数]]", "[[电池电动势]]"]
tags: [化竞, 题目, 物理化学, 电化学]
updated: 2026-08-04
status: 已填充
exam_stage: 决赛
subject_module: 化学原理
pack: 章节练习
source_category: 其他类型·自编章节题
---
# 题-物电-02：Eθ—ΔGθ—K 全链互算

## 题目

298 K 时电池反应 $\mathrm{Zn + Cu^{2+} \rightleftharpoons Zn^{2+} + Cu}$ 的标准电动势 $E^\theta_{\mathrm{cell}} = 1.10$ V，$n = 2$，$F = 96485$ C/mol。求该反应的标准吉布斯自由能变 $\Delta G^\circ$ 与平衡常数 $K$。

## 参考答案

**(1) $\Delta G^\circ$**：

$$\Delta G^\circ = -nFE^\theta_{\mathrm{cell}} = -2\times 96485\times 1.10 = -2.12\times10^{5}\ \mathrm{J/mol} = -212\ \mathrm{kJ/mol}$$

**(2) $K$**（298 K 简式 $\lg K = nE^\theta/0.0592$）：

$$\lg K = \frac{2\times 1.10}{0.0592} = 37.16\ \Rightarrow\ K = 10^{37.16} \approx 1.4\times10^{37}$$

**答案**：$\Delta G^\circ = -212$ kJ/mol，$K \approx 1.4\times10^{37}$。

> **核心辨析**：$E^\theta$、$\Delta G^\circ$、$K$ 是描述反应倾向的三个等价量（转接头）。n 是**转移电子数**而非某物质计量系数——竞赛高频陷阱。$\Delta G^\circ < 0 \Leftrightarrow K > 1 \Leftrightarrow E^\theta > 0$。

## 知识点映射

- [[Nernst方程]] · [[Gibbs自由能]] · [[平衡常数]] · [[电池电动势]]
- 易错点：n 取电子转移数；单位统一（J vs kJ）；$F = 96485$ C/mol
