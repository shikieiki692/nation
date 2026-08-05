---
title: "题-物统-01-Boltzmann布居比"
aliases: ["题-物统-01"]
type: 题目
difficulty: 3
teaching_level: 巩固
source: "教学改编（统计热力学与Maxwell关系讲义 §二）"
module: "统计热力学与相图"
subject: 物理化学
syllabus_codes: ["04"]
knowledge_points: ["[[Boltzmann统计初步]]"]
tags: [化竞, 题目, 物理化学, 统计热力学]
updated: 2026-08-04
status: 已填充
exam_stage: 决赛
---
# 题-物统-01：Boltzmann 分布与能级布居

## 题目

某分子有两个能级，能级间隔 $\Delta\varepsilon = 2.5$ kJ/mol，$T = 300$ K。求高能级与低能级的布居比 $N_2/N_1$，并说明温度升高时比值如何变化。（$R = 8.314$ J·mol⁻¹·K⁻¹）

## 参考答案

Boltzmann 分布：

$$\frac{N_2}{N_1} = e^{-\Delta\varepsilon/RT} = \exp\left(-\frac{2500}{8.314\times 300}\right) = e^{-1.002} = 0.367$$

**温度效应**：$T$ 升高 → 指数绝对值减小 → $N_2/N_1$ 增大（高能级布居增多）。

**答案**：$N_2/N_1 \approx 0.37$；升温使比值增大。

> **核心辨析**：Boltzmann 因子 $e^{-\Delta\varepsilon/kT}$ 是一切统计分布的基石。$\Delta\varepsilon \ll RT$ 时两能级近等布居，$\Delta\varepsilon \gg RT$ 时高能级几乎空置——用于判断分子振动激发、反应活性等。

## 知识点映射

- [[Boltzmann统计初步]]
- 易错点：$\Delta\varepsilon$ 用 J/mol 时配 $R$；用 J/分子 时配 $k_B$；勿混用
