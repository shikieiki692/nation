---
title: "题-物热-02-Born-Haber循环求晶格能"
aliases: ["题-物热-02"]
type: 题目
fidelity: 原书逐字
difficulty: 3
teaching_level: 巩固
source: "教学改编（普化原理第4版 + 赵鑫光热力学题集）"
module: "热力学与热化学"
subject: 物理化学
syllabus_codes: ["06"]
knowledge_points: ["[[Born-Haber循环]]", "[[晶格能]]", "[[标准生成焓]]", "[[电离能]]", "[[电子亲合能]]"]
tags: [化竞, 题目, 物理化学, 热力学, 晶格能]
updated: 2026-08-04
status: 已填充
exam_stage: 初赛
---
# 题-物热-02：Born-Haber 循环求晶格能

## 题目

已知下列数据（kJ/mol）：Na(s) 升华焓 $+108$；Cl₂(g) 解离能 $+242$；Na 第一电离能 $+496$；Cl 电子亲和能 $-349$；NaCl(s) 标准生成焓 $-411$。用 Born-Haber 循环求 NaCl 的晶格能 $U$。

## 参考答案

Born-Haber 循环闭合：Na(s) → Na⁺(g) + Cl⁻(g) → NaCl(s) 的总焓变等于 NaCl 的生成焓。

$$U = \Delta_fH(\mathrm{NaCl}) - \left[\Delta_{\mathrm{sub}}H(\mathrm{Na}) + \tfrac{1}{2}D(\mathrm{Cl_2}) + IE_1(\mathrm{Na}) + EA(\mathrm{Cl})\right]$$

代入：

$$U = -411 - \left[108 + \tfrac{242}{2} + 496 + (-349)\right] = -411 - (108 + 121 + 496 - 349) = -411 - 376 = -787\ \mathrm{kJ/mol}$$

**答案**：晶格能 $U \approx 787$ kJ/mol（负号表示成晶格放热，习惯上晶格能取正值 787 kJ/mol）。

> **核心辨析**：晶格能是气态离子结合成 1 mol 晶体的放热量；Born-Haber 循环本质是把生成焓分解为五个已知/可测步骤的能量和，缺项即可由闭合性解出。Cl₂ 解离能是键能，须取 $\tfrac{1}{2}$（生成 1 mol Cl⁻ 只需 0.5 mol Cl₂）。

## 知识点映射

- [[Born-Haber循环]] · [[晶格能]] · [[标准生成焓]] · [[电离能]] · [[电子亲合能]]
- 易错点：解离能取半；电子亲和能带负号；循环方向（升华+解离+电离+亲和 → 再放晶格能 → 回到晶体）
