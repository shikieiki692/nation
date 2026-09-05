---
title: 题-413-化学能力测试-Ch7B-8-AgAgBr热力学与Br2溶解
type: 题目
aliases:
  - Ag AgBr Br2 Latimer
source_subject: 化学竞赛能力测试·第7章B卷
submodule: Ag/AgBr 电极热力学 + Kf/Ksp + Br Latimer 求 Br₂ 溶解度
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
  - "[[Latimer图]]"
  - "[[溶度积]]"
concepts:
  - "ΔfG^θ(Ag⁺)=77.15 kJ/mol"
  - "Kf[Ag(NH₃)₂⁺]=1.7×10⁷"
  - "Ksp(AgBr)=4.89×10⁻¹³"
  - "AgBr 0.100 M NH₃ 中溶解度 2.9×10⁻⁴ M"
  - "Br₂(aq) 溶解度 0.077 M（E₂°=1.098 V Latimer 组合）"
pack: 模块习题集
tags:
  - 化竞
  - 教材习题
  - 化学能力测试
  - 第7章
created: 2026-09-03
updated: 2026-09-03
source: 化学竞赛能力测试·第7章 溶液中的平衡·B卷第8题
source_file: "[[化学竞赛教程/（已压缩）化学竞赛能力测试]]"
status: 已填充
---

# Ag/AgBr 热力学与 Br₂ 溶解

> **来源**：化学竞赛能力测试·第7章·B卷第8题（10 分）

已知 Ag⁺/Ag E^θ=+0.7996 V；AgBr(s)/Ag,Br⁻ E^θ=+0.0713 V；ΔfG^θ(NH₃(aq))=−26.50、ΔfG^θ[Ag(NH₃)₂⁺]=−17.12 kJ/mol；Br Latimer：BrO₃⁻ +1.491→HOBr +1.584→Br₂(aq) →?→ Br⁻。

**8-1** 计算 ΔfG^θ(Ag⁺(aq))。

**8-2** 计算 Ag⁺+2NH₃→Ag(NH₃)₂⁺ 的 25℃ 平衡常数。

**8-3** 计算 AgBr 的 Ksp。

**8-4** 计算 AgBr 在 0.100 M 氨水中的溶解度。

**8-5** 电池 Br₂(l)+H₂(g)+2H₂O→2Br⁻+2H₃O⁺，阴极加 Ag⁺ 至 [Ag⁺]=0.0600 M 后测 E=1.721 V。计算原电池电动势 ε°。

**8-6** 估计 25℃ 溴在水中 Br₂(aq) 的溶解度。

<details>
<summary>📖 查看答案与解析</summary>

**8-1** ΔG^θ=−FE^θ=−96500×0.7996 对 Ag⁺+e→Ag，ΔrG^θ=−ΔfG^θ(Ag⁺)：

$$\Delta_\mathrm{f}G^\theta(\mathrm{Ag^+}) = F\times 0.7996 = 77.15\ \mathrm{kJ/mol}$$

**8-2**

$$\Delta G^\theta = -17.12 - 77.15 - 2(-26.50) = -41.27\ \mathrm{kJ}$$

$$K_\mathrm{f} = \exp(41270/(8.314\times 298.15)) = 1.7\times 10^7$$

**8-3** AgBr(s)→Ag⁺+Br⁻：ΔE^θ=0.0713−0.7996=−0.7283 V：

$$\ln K_\mathrm{sp} = nF\Delta E^\theta/RT = -28.35 \Rightarrow K_\mathrm{sp} = 4.89\times 10^{-13}$$

**8-4** AgBr+2NH₃⇌Ag(NH₃)₂⁺+Br⁻，K=Ksp·Kf=8.31×10⁻⁶：

$$\frac{S^2}{(0.100-2S)^2} = 8.31\times 10^{-6} \Rightarrow S = 2.9\times 10^{-4}\ \mathrm M$$

**8-5** [Br⁻]=Ksp/[Ag⁺]=8.15×10⁻¹²：

$$\Delta E^\theta = 1.721 + \frac{0.0592}{2}\lg(8.15\times 10^{-12})^2 = 1.065\ \mathrm V$$

**8-6** Latimer 组合求 E^θ(Br₂(aq)+2e→2Br⁻)：

E₆°(BrO₃⁻→Br₂)=(2×4×1.491+2×1.584)/10=1.5096 V；

E₂°(Br₂→Br⁻)=(2×6×1.441−10×1.5096)/2=1.098 V（6E₃=4E₄+E₅+E₂ 核对）。

Br₂(l)+2e→2Br⁻ ΔG₁=−2F×1.065；Br₂(aq)+2e→2Br⁻ ΔG₂=−2F×1.098：

$$\Delta G^\theta(\mathrm{Br_2(l)\to Br_2(aq)}) = \Delta G_1 - \Delta G_2 = 0.066F = 6368\ \mathrm J$$

$$[\mathrm{Br_2(aq)}] = \exp(-6368/RT) = 0.077\ \mathrm M$$

</details>

<!-- 校勘注: ①8-4 溶解度 2.9e-4 M ≫ 纯水 √Ksp=7e-7（氨配位增溶 ~400 倍）；②8-5 ΔE^θ=1.065 V 为 Br₂/Br⁻ 标准（阴极产物），与 8-6 Latimer 组合一致互验；③8-6 Br₂(aq) 0.077 M 与文献 0.21 M（25℃）偏低，源答案方法 Latimer 近似所致照录。 -->

## 知识点映射

| 知识点 | 本题应用 |
|---|---|
| [[标准电极电势]] | ΔG^θ=−nFE^θ |
| [[Gibbs自由能]] | 生成自由能互推 |
| [[Latimer图]] | 组合求未知电对 E^θ |
| [[溶度积]] | AgBr 配体溶解 |