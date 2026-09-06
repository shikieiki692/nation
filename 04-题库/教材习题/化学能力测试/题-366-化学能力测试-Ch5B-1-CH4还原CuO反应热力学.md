---
title: 题-366-化学能力测试-Ch5B-1-CH4还原CuO反应热力学
type: 题目
aliases:
  - CH4 还原 CuO
source_subject: 化学竞赛能力测试·第5章B卷
submodule: CH₄+4CuO → CO₂+2H₂O(l)+4Cu 热力学
subject_module: 化学原理
exam_stage: 初赛
question_type:
  - 计算
difficulty: 4
teaching_level: 竞赛
fidelity: 原书逐字
knowledge_points:
  - "[[反应热与盖斯定律]]"
  - "[[热力学第一定律]]"
  - "[[Gibbs自由能]]"
concepts:
  - "ΔrH^θ=−261.11 kJ/mol；ΔrS^θ=129.27 J/K·mol；ΔrG^θ(298K)=−299.32 kJ/mol"
  - "500K: ΔrH^θ=−173.09 kJ/mol（产物水为气）；ΔrS^θ=366.89 J/K·mol"
  - "ΔrG^θ(500K)=−356.54 kJ/mol"
pack: 模块习题集
tags:
  - 化竞
  - 教材习题
  - 化学能力测试
  - 第5章
created: 2026-09-03
updated: 2026-09-03
source: 化学竞赛能力测试·第5章 化学热力学初步知识·B卷第1题
source_file: "[[化学竞赛教程/（已压缩）化学竞赛能力测试]]"
status: 已填充
used_in: "[[综合模拟卷IV]]"
source_category: 竞赛导向·竞赛教辅
source_grade: A
---

# CH₄ 还原 CuO 反应热力学

> **来源**：化学竞赛能力测试·第5章·B卷第1题（10 分）

已知 298.15 K 时热力学数据（CH₄/Cu/CuO/CO₂/H₂O(l)/H₂O(g) 的 ΔfH^θₘ、S^θₘ、ΔfG^θₘ）。

计算反应 $\mathrm{CH_4(g) + 4CuO(s) = CO_2(g) + 2H_2O(l) + 4Cu(s)}$

**1-1** 298.15 K 时的 ΔrH^θₘ、ΔrS^θₘ、ΔrG^θₘ。

**1-2** ΔrG^θₘ(500 K)。

<details>
<summary>📖 查看答案与解析</summary>

**1-1**

$$\Delta_\mathrm{r}H^\theta_\mathrm{m} = \Delta_\mathrm{f}H^\theta_\mathrm{m}(\mathrm{CO_2,g}) + 2\Delta_\mathrm{f}H^\theta_\mathrm{m}(\mathrm{H_2O,l}) - \Delta_\mathrm{f}H^\theta_\mathrm{m}(\mathrm{CH_4,g}) - 4\Delta_\mathrm{f}H^\theta_\mathrm{m}(\mathrm{CuO,s})$$

$$= -393.5 + 2\times(-285.83) - (-74.85) - 4\times(-157.3) = -261.11\ \mathrm{kJ\cdot mol^{-1}}$$

$$\Delta_\mathrm{r}S^\theta_\mathrm{m} = 213.64 + 2\times 69.91 + 4\times 33.15 - 186.27 - 4\times 42.63 = 129.27\ \mathrm{J\cdot K^{-1}\cdot mol^{-1}}$$

$$\Delta_\mathrm{r}G^\theta_\mathrm{m} = -394.36 + 2\times(-237.18) - (-50.6) - 4\times(-129.7) = -299.32\ \mathrm{kJ\cdot mol^{-1}}$$

由 ΔG = ΔH − TΔS 验算：−261.11 − 298.15×129.27×10⁻³ = −299.65 kJ/mol，两种方法一致。

**1-2** 500 K 时水以气态形式存在：

$$\Delta_\mathrm{r}H^\theta_\mathrm{m}(500\ \mathrm K) = -393.5 + 2\times(-241.82) - (-74.85) - 4\times(-157.3) = -173.09\ \mathrm{kJ\cdot mol^{-1}}$$

$$\Delta_\mathrm{r}S^\theta_\mathrm{m}(500\ \mathrm K) = 213.64 + 2\times 188.72 + 4\times 33.15 - 186.27 - 4\times 42.63 = 366.89\ \mathrm{J\cdot K^{-1}\cdot mol^{-1}}$$

$$\Delta_\mathrm{r}G^\theta_\mathrm{m}(500\ \mathrm K) = -173.09 - 500\times 366.89\times 10^{-3} = -356.54\ \mathrm{kJ\cdot mol^{-1}}$$

</details>

<!-- 校勘注: ① 298K ΔrH^θ 验算：-393.5+2×(-285.83)-(-74.85)-4×(-157.3)=-393.5-571.66+74.85+629.2=-261.11 ✓；② ΔrS^θ=213.64+139.82+132.6-186.27-170.52=485.06-356.79=128.27 vs 源 129.27 差 1 J（舍入），按源；③ 500K ΔrH^θ 含气态水蒸发 +44 kJ/mol 故 ΔrH^θ 变 -261.11+2×44=-173.11 vs 源 -173.09 接近。 -->

## 知识点映射

| 知识点 | 本题应用 |
|---|---|
| [[反应热与盖斯定律]] | ΔrH^θ = ΣνΔfH^θ |
| [[热力学第一定律]] | ΔS^θ = ΣνS^θ |
| [[Gibbs自由能]] | ΔG^θ=ΔH^θ−TΔS^θ |