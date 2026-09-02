---
title: "题-WCh19.06-M+M负离子稳定性"
type: 题目
source: "无机化学第6版Weller Ch19 练习题19.6"
source_file: "06-外部资料导入/无机化学Weller/无机化学第6版Welle19-21章.md"
subject: 无机和结构化学
year: 2023
difficulty: 4
knowledge_points: ["[[过渡元素]]", "[[电离能]]"]
status: 已补全答案
tags: [化竞, 无机化学, Weller, d区元素]
created: 2026-08-27
updated: 2026-08-30
subject_module: 元素与分析
pack: 模块习题集
fidelity: 原书逐字
exam_stage: 决赛
used_in: "[[元素与分析阶段测试卷]]"
---

# M+M负离子稳定性

> **来源**：无机化学第6版（Weller等著，中文版）Ch19 练习题19.6
> **难度**：⭐⭐⭐⭐

## 题目

查找 Cu、Ag、Au 的得电子焓和第 1 族金属的电离能, 根据相关数据讨论: 化合物 $\mathrm{M^{+}M^{\prime-}}$ 可能是稳定的 (化学式中的 M 为第 1 族金属, $\mathrm{M^{\prime}}$ 为第 11 族金属)。

## 参考答案

### 1. 数据

下面给出第一族金属的第一电离能 $IE_1$ 和第 11 族金属的得电子焓 $EAH$（即 $\mathrm{M^{\prime}(g)+e^-\rightarrow M^{\prime-}(g)}$ 的焓变，放热为负；数值为常用手册近似值）：

| M（第 1 族） | $IE_1$ / kJ·mol⁻¹ | M′（第 11 族） | M′⁻ 电子组态 | $EAH$ / kJ·mol⁻¹ |
|---|---:|---|:--|--:|
| Li | 520 | Cu | [Ar]3d¹⁰4s² | −118 |
| Na | 496 | Ag | [Kr]4d¹⁰5s² | −126 |
| K | 419 | Au | [Xe]4f¹⁴5d¹⁰6s² | −223 |
| Rb | 403 | | | |
| Cs | 376 | | | |

### 2. 能量分析

形成固体 $\mathrm{M^+M^{\prime-}}$ 的焓变可由 Born-Haber 循环估计：

$$\Delta H \approx \Delta_{at}H(\mathrm{M}) + \Delta_{at}H(\mathrm{M^{\prime}}) + IE_1(\mathrm{M}) + EAH(\mathrm{M^{\prime}}) - U$$

其中 $\Delta_{at}H$ 为原子化焓，$U$ 为晶格焓（正数，表示离子结合能）。判稳的关键是 $IE_1(\mathrm{M})$ 与 $EAH(\mathrm{M^{\prime}})$ 之和相对晶格焓的大小：第一族金属的第一电离能只有约 376～520 kJ·mol⁻¹，第 11 族金属的得电子焓为 −118～−223 kJ·mol⁻¹，两者之和远小于典型 1:1 离子盐数百至上千 kJ·mol⁻¹ 的晶格焓贡献，因此从焓的角度看 $\mathrm{M^+M^{\prime-}}$ 是可能稳定的。

三种 M′⁻ 均取 d¹⁰s² 闭壳层组态，与卤离子类似，有利于形成离子型化合物。得电子焓最有利的是 Au（−223 kJ·mol⁻¹），这与 6s 轨道因相对论效应收缩、电子亲和增大一致；第一电离能最低的是 Cs（376 kJ·mol⁻¹），且 Cs⁺ 与 Au⁻ 的离子半径匹配较好。因此 Cs⁺Au⁻ 是最优先的组合。

### 3. 结论

数据支持 $\mathrm{M^+M^{\prime-}}$ 型离子化合物可稳定存在，特别是 CsAu：它已被实验表征为含 Au⁻ 的离子型固体。若换用 Cu 或 Ag，得电子焓负值较小、晶格焓收益有限，形成相应 $\mathrm{M^+M^{\prime-}}$ 的驱动力较弱，稳定性不如金化物。完整的 Born-Haber 循环还应计入升华焓与阴离子半径效应，但上述数据已足以说明题目要求的稳定性倾向。
