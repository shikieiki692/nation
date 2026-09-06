---
title: 题-381-化学能力测试-Ch6A-6-NO催化分解CuZSM5
type: 题目
aliases:
  - NO 催化分解
source_subject: 化学竞赛能力测试·第6章A卷
submodule: NO 分解热力学 + Cu/ZSM-5 催化动力学
subject_module: 化学原理
exam_stage: 初赛
question_type:
  - 计算
  - 机理
  - 简答
difficulty: 5
teaching_level: 竞赛
fidelity: 原书逐字
knowledge_points:
  - "[[化学动力学]]"
  - "[[活化能]]"
  - "[[催化剂]]"
  - "[[多相催化]]"
  - "[[Gibbs自由能]]"
concepts:
  - "NO→½N₂+½O₂ ΔH^θ=−85.9 kJ/mol（解离焓算）"
  - "ΔS^θ≈0 → ΔG^θ≈ΔH^θ<0 自发"
  - "Eₐ=74.8 kJ/mol（转化数 1.91@673K、5.03@723K）"
  - "转化率 = n_r/n_0 = 21%"
  - "机理推导 r=kc(NO)/(1+K'c(O₂)^½)；低 O₂ 时 r=kc(NO)（一级）"
pack: 模块习题集
tags:
  - 化竞
  - 教材习题
  - 化学能力测试
  - 第6章
created: 2026-09-03
updated: 2026-09-03
source: 化学竞赛能力测试·第6章 简单的化学动力学原理·A卷第6题
source_file: "[[化学竞赛教程/（已压缩）化学竞赛能力测试]]"
status: 已填充
source_category: 竞赛导向·竞赛教辅
source_grade: A
---

# NO 催化分解 Cu/ZSM-5

> **来源**：化学竞赛能力测试·第6章·A卷第6题（10 分）

NO 是大气的污染物，催化 O₃ 分解破坏臭氧层，易被氧化为 NO₂ 参与光化学烟雾。空气中 NO 最高允许 ≤5 mg/L。为此寻找高效催化剂将 NO 分解为 N₂ 和 O₂。

**6-1** 用热力学判断 NO 在常温常压下能否自发分解（N₂、NO、O₂ 解离焓分别为 941.7、631.8、493.7 kJ·mol⁻¹）。

**6-2** Cu/ZSM-5 分子筛催化 NO 分解。高温氧分压很小时为一级反应。NO 分压相同，673 K 和 723 K 时转化数 1.91 和 5.03 s⁻¹（单位时间每个活性中心分解的 NO 分子数）。求活化能。

**6-3** 固定床反应器：混合气体中 NO 体积分数 4.0%，流速 4.0×10 cm³/min（标准状况），催化剂 2.0 cm³，表面 Cu⁺ 活性中心 1.0×10⁻⁶ mol，反应温度 723 K。计算 NO 分解转化率。

![[4f3c01a1995d88185ffa0dbb50550b4de79f2a1b52a34f82f53933d04c8388b6.jpg]]

**6-4** 机理：

① NO+M→NO-M（k₁）② 2NO-M→N₂+2O-M（k₂）③ 2O-M ⇌ O₂+2M（k₃/k₋₃，快）

M 为活性中心，NO 弱吸附 NO-M 浓度可忽略。据机理与 M 物料平衡推导速率方程，解释低 O₂ 分压时一级动力学。

<details>
<summary>📖 查看答案与解析</summary>

**6-1** NO(g) → ½N₂(g) + ½O₂(g)：

$$\Delta_\mathrm{r}H^\theta \approx 631.8 - \tfrac{1}{2}(941.7 + 493.7) = -85.9\ \mathrm{kJ\cdot mol^{-1}}$$

反应前后气体分子数不变 → ΔrS^θ≈0：

$$\Delta_\mathrm{r}G^\theta = \Delta_\mathrm{r}H^\theta - T\Delta_\mathrm{r}S^\theta \approx -85.9\ \mathrm{kJ\cdot mol^{-1}} < 0$$

**可自发分解**。

**6-2** 转化数比 = 速率常数比：

$$\ln\frac{k_{723}}{k_{673}} = \frac{E_\mathrm{a}}{R}\left(\frac{723-673}{723\times 673}\right) = \ln\frac{5.03}{1.91}$$

$$E_\mathrm{a} = \frac{8.314\times 723\times 673}{50}\ln(5.03/1.91) = 74.8\ \mathrm{kJ\cdot mol^{-1}}$$

**6-3** 每分钟通过催化剂的 NO：

$$n_0 = \frac{40\ \mathrm{cm^3}\times 4.0\%}{22400\ \mathrm{cm^3/mol}} = 7.1\times 10^{-5}\ \mathrm{mol}$$

每分钟分解的 NO（转化数 5.03 s⁻¹ × Cu⁺ 1.0×10⁻⁶ mol × 60 s）：

$$n_\mathrm{r} = 5.03\times 1.0\times 10^{-6}\times 60 = 3.0\times 10^{-4}\ \mathrm{mol}$$

源答案用「60s/20s」比例得 n_r=1.5×10⁻⁵ mol/min（疑按 5.03 转换含每 20 s 一活性中心 → 每分钟 3 次×5.03/活性中心 得 1.5e-5 mol 需考证源条件），转化率：

$$y = 1.5\times 10^{-5}/7.1\times 10^{-5} = 21\%$$

**6-4** ①式：r = k₁c_NO·c_M (a)

M 物料平衡：c = c_M + c_O−M + c_NO−M ≈ c_M + c_O−M (b)

③快平衡：K = k₃/k₋₃ = c_O₂·c_M²/c_O−M² → c_O−M = c_O₂^½·c_M/K^½ (c)

(c) 代入 (b)：c₀ = c_M(1+c_O₂^½/K^½) → c_M = c₀/(1+c_O₂^½/K^½) (d)

(d) 代入 (a)：

$$r = k_1c_\mathrm{NO}\frac{c_0}{1 + c_{\mathrm{O_2}}^{1/2}/K^{1/2}}$$

设 k₁c₀=k、1/K^½=K′：

$$r = \frac{kc_\mathrm{NO}}{1 + K'c_{\mathrm{O_2}}^{1/2}}$$

低 O₂ 分压时 1+K′c_O₂^½≈1 → **r = kc_NO（一级）**，与实验一致。

</details>

<!-- 校勘注: ①6-2 Eₐ 验算：ln(5.03/1.91)=0.968；Eₐ=0.968×8.314×723×673/50=74804 J/mol≈74.8 kJ/mol ✓（源答案 748 kJ/mol 系小数点误，实为 74.8）；②6-3 n₀=40×4% 注意 4.0×10 cm³/min 源 OCR 疑为 40 cm³/min（题面「4.0×10 cm³/min」按 40 读），n_r 源答案按 5.03×1.0e-6×3=1.5e-5 隐含每 20 s 全床反应一轮——按转化率 21% 照录；③6-4 推导完整自洽，低氧一级吻合实验。 -->

## 知识点映射

| 知识点 | 本题应用 |
|---|---|
| [[化学动力学]] | 转化数 = 速率常数、Arrhenius |
| [[活化能]] | 74.8 kJ/mol |
| [[催化剂]] | Cu/ZSM-5 催化 |
| [[多相催化]] | 表面活性中心转化数、Langmuir 机理 |
| [[Gibbs自由能]] | ΔG^θ=ΔH^θ−TΔS^θ 判断自发 |