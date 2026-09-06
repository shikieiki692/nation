---
title: 题-406-化学能力测试-Ch7B-1-依数性HAc缔合与Kb
type: 题目
aliases:
  - HAc 缔合 依数性
source_subject: 化学竞赛能力测试·第7章B卷
submodule: 依数性：HAc 缔合/沸点升高/蒸气压
subject_module: 化学原理
exam_stage: 初赛
question_type:
  - 计算
difficulty: 4
teaching_level: 竞赛
fidelity: 原书逐字
knowledge_points:
  - "[[稀溶液依数性]]"
  - "[[拉乌尔定律]]"
  - "[[Clapeyron方程]]"
concepts:
  - "HAc 在水中 M=60（单体）；苯中 M=120→二聚缔合 (HAc)₂"
  - "Kb(H₂O)=0.521 K·kg·mol⁻¹；M₂=105 g/mol"
  - "ΔvapH(H₂O)=40.0 kJ/mol（由 Kb=RTb²M₁/ΔvapH 反推）"
  - "298K 纯水蒸气压 3.94 kPa（Clausius）；溶液 3.91 kPa（拉乌尔 x₁=0.9927）"
pack: 模块习题集
tags:
  - 化竞
  - 教材习题
  - 化学能力测试
  - 第7章
created: 2026-09-03
updated: 2026-09-03
source: 化学竞赛能力测试·第7章 溶液中的平衡·B卷第1题
source_file: "[[化学竞赛教程/（已压缩）化学竞赛能力测试]]"
status: 已填充
source_category: 竞赛导向·竞赛教辅
source_grade: A
---

# 依数性：HAc 缔合与 Kb

> **来源**：化学竞赛能力测试·第7章·B卷第1题（10 分）

**1-1** 0.900 g HAc 溶于 50.0 g 水凝固点 −0.558℃；2.32 g HAc 溶于 100 g 苯凝固点降低 0.970℃。分别计算 HAc 在水中与苯中的摩尔质量并解释差异（Kf 水=1.86、苯=5.12 K·kg·mol⁻¹）。

**1-2** 100 g 水中溶入 2.220 g 不挥发性溶质（M₁=110.1）沸点升高 0.105℃；再加入 2.160 g 未知溶质沸点又升高 0.107℃。计算 (1) 水的 Kb、未知物摩尔质量 M₂、水的摩尔蒸发热 ΔH；(2) 该溶液 298 K 的蒸气压（理想溶液）。

<details>
<summary>📖 查看答案与解析</summary>

**1-1** ΔTf=Kf·m₂/(M₂·m₁)：

$$M(\mathrm{HAc})_{水} = \frac{1.86\times 0.900}{0.558\times 50.0/1000} = 60\ \mathrm{g/mol}$$

$$M(\mathrm{HAc})_{苯} = \frac{5.12\times 2.32}{0.970\times 100/1000} = 122\ \mathrm{g/mol}$$

水中单体（60），苯中约二倍（122）→ **HAc 在苯中分子缔合为 (HAc)₂**。

**1-2** (1) ΔTb=Kb·m₂/(M₂·m₁)：

$$K_\mathrm{b} = \frac{0.105\times 100\times 110.1}{2.220\times 1000} = 0.521\ \mathrm{K\cdot kg\cdot mol^{-1}}$$

$$M_2 = \frac{0.521\times 2.160}{0.107\times 100/1000} = 105\ \mathrm{g/mol}$$

Kb = RT_b*²M₁/ΔvapH：

$$\Delta_\mathrm{vap}H = \frac{8.314\times 373^2\times 18\times 10^{-3}}{0.521} = 40.0\ \mathrm{kJ/mol}$$

(2) 373 K 纯水 p^θ=101.325 kPa，Clausius-Clapeyron 外推 298 K：

$$p_1^*(298) = 101.325\times\exp[40000\times(298-373)/(8.314\times 373\times 298)] = 3.94\ \mathrm{kPa}$$

溶质总摩尔分数 x₂ = 7.279×10⁻³ → 拉乌尔：

$$p_1(298) = 3.94\times(1 - 7.279\times 10^{-3}) = 3.91\ \mathrm{kPa}$$

</details>

<!-- 校勘注: ①HAc 苯中缔合为二聚体（分子间氢键）→ 表观摩尔质量翻倍 ✓；②Kb 实验值 0.521 vs 理论 0.512 差异来自题给数据，照题算；③40.0 kJ/mol 与标准 ΔvapH(H₂O)=40.7 kJ/mol 接近 ✓。 -->

## 知识点映射

| 知识点 | 本题应用 |
|---|---|
| [[稀溶液依数性]] | ΔTf/ΔTb 与摩尔质量 |
| [[拉乌尔定律]] | 溶液蒸气压降低 |
| [[Clapeyron方程]] | 蒸气压温度外推 |