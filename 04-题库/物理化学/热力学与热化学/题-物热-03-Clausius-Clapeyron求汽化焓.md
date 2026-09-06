---
title: "题-物热-03-Clausius-Clapeyron求汽化焓"
aliases: ["题-物热-03"]
type: 题目
fidelity: 自编
difficulty: 3
teaching_level: 巩固
source: "教学改编（物化综合计算讲义 §〇 前置概念）"
module: "热力学与热化学"
source_subject: 物理化学
syllabus_codes: ["06", "04"]
knowledge_points: ["[[Clapeyron方程]]", "[[沸点]]"]
tags: [化竞, 题目, 物理化学, 相变热力学]
updated: 2026-08-04
status: 已填充
exam_stage: 决赛
subject_module: 化学原理
pack: 章节练习
source_category: 其他类型·自编章节题
source_grade: B-
---
# 题-物热-03：Clausius-Clapeyron 求汽化焓

## 题目

水的蒸气压在 298 K 时为 3.17 kPa，在正常沸点 373 K 时为 101.3 kPa。设汽化焓在此温度范围内为常数，求：(1) 水的摩尔汽化焓 $\Delta_{\mathrm{vap}}H$；(2) 水在 350 K 时的蒸气压。（$R = 8.314$ J·mol⁻¹·K⁻¹）

## 参考答案

**(1)** Clausius-Clapeyron 积分式：

$$\ln\frac{p_2}{p_1} = -\frac{\Delta_{\mathrm{vap}}H}{R}\left(\frac{1}{T_2}-\frac{1}{T_1}\right)$$

$$\ln\frac{101.3}{3.17} = -\frac{\Delta_{\mathrm{vap}}H}{8.314}\left(\frac{1}{373}-\frac{1}{298}\right)$$

$\ln 31.96 = 3.465$；$\frac{1}{373}-\frac{1}{298} = -6.75\times10^{-4}\ \mathrm{K^{-1}}$

$$3.465 = \frac{\Delta_{\mathrm{vap}}H}{8.314}\times 6.75\times10^{-4}\ \Rightarrow\ \Delta_{\mathrm{vap}}H = \frac{3.465\times 8.314}{6.75\times10^{-4}} = 4.27\times10^{4}\ \mathrm{J/mol} \approx 42.7\ \mathrm{kJ/mol}$$

**(2)** 350 K：

$$\ln\frac{p}{3.17} = -\frac{42700}{8.314}\left(\frac{1}{350}-\frac{1}{298}\right),\quad \frac{1}{350}-\frac{1}{298} = -4.99\times10^{-4}$$

$$\ln\frac{p}{3.17} = 5137\times 4.99\times10^{-4} = 2.56\ \Rightarrow\ \frac{p}{3.17} = 12.9\ \Rightarrow\ p \approx 41\ \mathrm{kPa}$$

**答案**：$\Delta_{\mathrm{vap}}H \approx 42.7$ kJ/mol；$p(350\ \mathrm{K}) \approx 41$ kPa（与文献 47.3 kPa 的偏差源于假设 ΔvapH 恒定）。

> **核心辨析**：Clausius-Clapeyron 是"蒸气压随温度"的对数线性关系，与 van't Hoff（平衡常数随温度）、Arrhenius（速率常数随温度）**形式同构**——识别题目问的是 $p$、$K$ 还是 $k$ 是第一步（竞赛综合题高频）。

## 知识点映射

- [[Clapeyron方程]] · [[沸点]] · [[蒸气压]]
- 易错点：$T$ 必须用开尔文；1/T 差值为负要正确处理符号；近似常数时外推高温会偏大
