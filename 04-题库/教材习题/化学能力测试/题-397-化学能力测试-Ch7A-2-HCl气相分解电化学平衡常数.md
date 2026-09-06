---
title: 题-397-化学能力测试-Ch7A-2-HCl气相分解电化学平衡常数
type: 题目
aliases:
  - HCl 分解电化学测 Kp
source_subject: 化学竞赛能力测试·第7章A卷
submodule: Pt,H₂|HCl(aq)|Cl₂,Pt 电池测 HCl 分解平衡常数
subject_module: 化学原理
exam_stage: 初赛
question_type:
  - 计算
difficulty: 5
teaching_level: 竞赛
fidelity: 原书逐字
knowledge_points:
  - "[[标准电极电势]]"
  - "[[Gibbs自由能]]"
  - "[[化学平衡]]"
concepts:
  - "电池 H₂|HCl(aq)|Cl₂ 反应 H₂+Cl₂→2HCl"
  - "RT ln Kp° = RT ln[p_HCl²/(p_H₂·p_Cl₂)] + zFE"
  - "ln Kp = 74.6（E=1.190 与 0.973 V 一致）"
  - "E=1.0 V：p_HCl/p_H₂=0.373 → p_HCl≈204 Torr"
  - "E=0（760 Torr 平衡）：p_H₂=p_Cl₂≈5×10⁻¹⁴ Torr（实际无游离氯/氢）"
pack: 模块习题集
tags:
  - 化竞
  - 教材习题
  - 化学能力测试
  - 第7章
created: 2026-09-03
updated: 2026-09-03
source: 化学竞赛能力测试·第7章 溶液中的平衡·A卷第2题
source_file: "[[化学竞赛教程/（已压缩）化学竞赛能力测试]]"
status: 已填充
source_category: 竞赛导向·竞赛教辅
---

# HCl 气相分解电化学平衡常数

> **来源**：化学竞赛能力测试·第7章·A卷第2题（10 分）

可逆电池 Pt, H₂(g) | HCl(aq) | Cl₂(g), Pt（303.1 K），气体与电解质溶液达成平衡。填空缺数据：

| p_HCl/Torr | p_H₂=p_Cl₂/Torr | E/V |
|---|---|---|
| 0.24 | 750 | 1.190 |
| ? | ? | 1.000 |
| 337 | 415 | 0.974 |

760 Torr、回路无电流时的平衡组成？F=9.6487×10⁴、R=8.3143。

<details>
<summary>📖 查看答案与解析</summary>

电池反应：H₂(g) + Cl₂(g) → 2HCl(aq)。气相中氯化氢与溶液中平衡，气相反应 H₂+Cl₂→2HCl 的 ΔG 与电化学相同：

$$\Delta G = RT\ln\frac{p_\mathrm{HCl}^2}{p_\mathrm{H_2}p_\mathrm{Cl_2}}$$

$$\Delta G^\theta = \Delta G + A = \Delta G + zFE$$

$$RT\ln K_\mathrm{p} = RT\ln\frac{p_\mathrm{HCl}^2}{p_\mathrm{H_2}p_\mathrm{Cl_2}} + 2FE$$

$$\ln K_\mathrm{p}^\theta = \ln\frac{p_\mathrm{HCl}^2}{p_\mathrm{H_2}p_\mathrm{Cl_2}} + 76.575E$$

E=1.190 V：ln Kp = ln(0.24²/750²) + 76.575×1.190 = −14.71 + 91.13 = 75.03

E=0.973 V：ln Kp = ln(337²/415²) + 76.575×0.973 = 0.394+0.973×76.575=74.17

平均 **ln Kp = 74.6**。

E=1.0 V：

$$\frac{p_\mathrm{HCl}}{p_\mathrm{H_2}} = \sqrt{\exp(74.6 - 76.575)} = 0.373$$

p总≈750 Torr → p(HCl)≈204 Torr、p(H₂)=p(Cl₂)≈546 Torr。

**E=0（760 Torr 平衡混合物）**：Kp^θ=exp(74.6)=1.58×10¹⁶ → p(HCl)≈760 Torr、p(H₂)=p(Cl₂)≈5×10⁻¹⁴ Torr——游离氯和氢实际不存在。故直接测气相组成定 K 不可能，电化学法是唯一方法。

</details>

<!-- 校勘注: ①源答案 1.190 V 行 lnKp 验算：ln(0.24²/750²)+76.575×1.190 = ln(1.024e-7)+91.12 = −16.09+91.12 = 75.03 ✓；②0.974V 行：ln(337²/415²)=ln(0.6595)=−0.416 → lnKp=−0.416+74.57=74.15 ✓；③两行 lnKp 一致验证 E^θ 恒定假设成立。 -->

## 知识点映射

| 知识点 | 本题应用 |
|---|---|
| [[标准电极电势]] | zFE = 电功耦合 |
| [[Gibbs自由能]] | ΔG^θ=−RT ln Kp^θ |
| [[化学平衡]] | 气相分压平衡常数 |