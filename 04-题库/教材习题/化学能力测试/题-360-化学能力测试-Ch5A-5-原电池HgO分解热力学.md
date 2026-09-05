---
title: 题-360-化学能力测试-Ch5A-5-原电池HgO分解热力学
type: 题目
aliases:
  - 原电池 HgO 分解
source_subject: 化学竞赛能力测试·第5章A卷
submodule: H₂-NaOH-HgO 原电池与 HgO 分解温度
subject_module: 化学原理
exam_stage: 初赛
question_type:
  - 计算
  - 作图
difficulty: 5
teaching_level: 竞赛
fidelity: 原书逐字
knowledge_points:
  - "[[Gibbs自由能]]"
  - "[[标准电极电势]]"
  - "[[热力学第一定律]]"
concepts:
  - "原电池 H₂(g)│NaOH(aq)│HgO(s)，Hg(l) E^θ=0.926 V"
  - "电池反应 H₂+HgO→H₂O+Hg，ΔrG^θ=−nFE^θ=−178.7 kJ/mol"
  - "HgO 分解 Hg+1/2 O₂ ΔrG^θ=+58.46 kJ/mol，Kp^θθ=5.63×10⁻¹¹，p(O₂)=3.17×10⁻²¹×101.3 kPa"
  - "ΔrH^θ=ΔrG^θ+TΔrS^θ=90.3 kJ/mol（ΔS^θ=106.7 J/K·mol）"
  - "空气中 p(O₂)≤0.21×101.3 kPa → 分解温度 T₂=797.6 K"
pack: 模块习题集
tags:
  - 化竞
  - 教材习题
  - 化学能力测试
  - 第5章
created: 2026-09-03
updated: 2026-09-03
source: 化学竞赛能力测试·第5章 化学热力学初步知识·A卷第5题
source_file: "[[化学竞赛教程/（已压缩）化学竞赛能力测试]]"
status: 已填充
---

# 原电池 HgO 分解热力学

> **来源**：化学竞赛能力测试·第5章·A卷第5题（10 分）

原电池 $\mathrm{H_2(g)\mid NaOH(aq)\mid HgO(s),\ Hg(l)}$ 在 298.15 K 下的标准电动势 $E^\theta = 0.926\ \mathrm{V}$。

反应 $\mathrm{H_2(g) + \tfrac{1}{2}O_2(g) = H_2O(l)}$，$\Delta_\mathrm{r}G^\theta_\mathrm{m}(298\ \mathrm K) = -237.2\ \mathrm{kJ\cdot mol^{-1}}$。

| 物质 | S^θₘ(298 K) / J·K⁻¹·mol⁻¹ |
|---|---|
| Hg(l) | 77.1 |
| HgO(s) | 73.2 |
| O₂(g) | 205.0 |

**5-1** 写出上述原电池的电池反应与电极反应（半反应）。

**5-2** 计算反应 $\mathrm{HgO(s) = Hg(l) + \tfrac{1}{2}O_2(g)}$ 在 298.15 K 下的平衡分压 $p(\mathrm{O_2})$ 和 $\Delta_\mathrm{r}H^\theta_\mathrm{m}(298.15\ \mathrm K)$。

**5-3** 设反应的焓变与熵变不随温度而变化，求 HgO 固体在空气中的分解温度。

<details>
<summary>📖 查看答案与解析</summary>

**5-1** 电极反应：

$$(-)\quad \mathrm{H_2(g) + 2OH^- \longrightarrow 2H_2O(l) + 2e^-}$$

$$(+)\quad \mathrm{HgO(s) + H_2O + 2e^- \longrightarrow 2OH^- + Hg(l)}$$

电池反应：

$$\mathrm{H_2(g) + HgO(s) = H_2O(l) + Hg(l)}$$

**5-2** 电池反应标准自由能变：

$$\Delta_\mathrm{r}G^\theta_\mathrm{m} = -nFE^\theta = -2\times 96500\times 0.926 = -178.7\times 10^3\ \mathrm{J\cdot mol^{-1}}$$

由 Hess 定律：电池反应 = (H₂+½O₂=H₂O) − (HgO=Hg+½O₂)：

$$\Delta_\mathrm{r}G^\theta_\mathrm{m}(\mathrm{HgO \to Hg}) = -237.2 - (-178.7) = -58.46\ \mathrm{kJ\cdot mol^{-1}}$$

源答案记作 $\Delta_\mathrm{r}G^\theta_\mathrm{m}(\mathrm{HgO \to Hg + ½O_2) = +58.46\ \mathrm{kJ\cdot mol^{-1}}$（正向为分解方向）。

$$\ln K_\mathrm{p}^\theta = -\-\Delta_\mathrm{r}G^\theta/RT = -(58.46\times 10^3)/(8.314\times 298.15) = -23.58$$

$$K_\mathrm{p}^\theta = 5.632\times 10^{-11}$$

$$K_\mathrm{p}^\theta = [p(\mathrm{O_2})/p^\theta]^{1/2}$$

$$p(\mathrm{O_2}) = (K_\mathrm{p}^\theta)^2\times p^\theta = 3.17\times 10^{-21}\times 101.3\ \mathrm{kPa}$$

$$\Delta_\mathrm{r}S^\theta = S(\mathrm{Hg}) + \tfrac{1}{2}S(\mathrm{O_2}) - S(\mathrm{HgO}) = 77.1 + 102.5 - 73.2 = 106.7\ \mathrm{J\cdot K^{-1}\cdot mol^{-1}}$$

$$\Delta_\mathrm{r}H^\theta = \Delta_\mathrm{r}G^\theta + T\Delta_\mathrm{r}S^\theta = 58.46\times 10^3 + 298.15\times 106.7 = 90278\ \mathrm{J\cdot mol^{-1}} \approx 90.3\ \mathrm{kJ\cdot mol^{-1}}$$

**5-3** HgO 稳定存在要求 $p(\mathrm{O_2}) \le 0.21\times 101.3\ \mathrm{kPa}$（空气中 O₂ 分压）。

由 Van't Hoff 方程：

$$\ln(K_2^\theta/K_1^\theta) = \ln(p_2^{1/2}/p_1^{1/2}) = \tfrac{1}{2}\ln(p_2/p_1) = \Delta H^\theta/R(1/T_1 - 1/T_2)$$

代入：

$$\tfrac{1}{2}\ln(0.21/(3.17\times 10^{-21})) = 90278/8.314\times (1/298.15 - 1/T_2)$$

$$\tfrac{1}{2}\times 47.99 = 10860 \times (1/298.15 - 1/T_2)$$

$$23.99/10860 = 1/298.15 - 1/T_2$$

$$1/T_2 = 1/298.15 - 0.002209 = 0.001145$$

$$T_2 = 873\ \mathrm{K}$$

源答案给出 $T_2 = 797.6\ \mathrm{K}$，按 Van't Hoff 方程验算：

$$\tfrac{1}{2}\ln(0.21/3.17\times 10^{-21}) = 23.99$$
$$\(90278/8.314) \times (1/298.15 - 1/T_2) = 10860 \times (0.003354 - 1/T_2)$$

解 $1/T_2 = 0.003354 - 23.99/10860 = 0.003354 - 0.002209 = 0.001145$，$T_2 = 873\ \mathrm{K}$。

源答案 797.6 K 与验算有差异（疑源答案误用 $\Delta_\mathrm{r}H^\theta$ 单位 kJ 而非 J，或 R 值差），照录并注存疑。

</details>

<!-- 校勘注: ①5-2 中 lnKp^θθ 计算：−58460/(8.314×298.15)=−23.58 → Kp^θθ=e⁻²³·⁵⁸=5.63×10⁻¹¹ ✓；p(O₂)=Kp^θθ² × p^θ = (5.63×10⁻¹¹)² × 101.3 = 3.21×10⁻¹⁹ × 101.3 = 3.25×10⁻¹⁷ kPa——源答案给 3.17×10⁻²¹×101.3 kPa 验算差异（疑 ln Kp^θθ 中 ΔrG^θ符号），实际 Kp^θθ² = (5.63×10⁻¹¹)² ≈ 3.17×10⁻²¹ ✓；②5-3 分解温度 Van't Hoff 验算得 ~873 K 而源答案 797.6 K 差异，按源答案照录并注存疑；③源答案 5-2 题给 H₂O 标准生成态 ΔrG^θ=−237.2 → HgO 分解 ΔrG^θ 方向符号处理与电池反应方向相关，本题答案记为 HgO=Hg+½O₂ 方向 ΔrG^θ=+58.46 kJ/mol（与电池方向相反，符合 Hess 循环）。 -->

## 知识点映射

| 知识点 | 本题应用 |
|---|---|
| [[Gibbs自由能]] | ΔG^θ=−nFE^θ（电化学）+ ΔG^θ=−RT ln Kp^θθ |
| [[标准电极电势]] | 原电池 E^θ → ΔG^θ 转换 |
| [[热力学第一定律]] | ΔH^θ=ΔG^θ+TΔS^θ、ΔS^θ 状态函数计算 |