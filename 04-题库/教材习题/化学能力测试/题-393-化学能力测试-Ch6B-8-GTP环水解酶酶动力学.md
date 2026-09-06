---
title: 题-393-化学能力测试-Ch6B-8-GTP环水解酶酶动力学
type: 题目
aliases:
  - GTP 环水解酶 Michaelis-Menten
source_subject: 化学竞赛能力测试·第6章B卷
submodule: 酶促动力学 Michaelis-Menten 与 GTP 环水解酶 II 实验
subject_module: 化学原理
exam_stage: 初赛
question_type:
  - 推导
  - 计算
  - 简答
difficulty: 5
teaching_level: 竞赛
fidelity: 原书逐字
knowledge_points:
  - "[[酶动力学]]"
  - "[[酶催化]]"
  - "[[稳态近似]]"
  - "[[分光光度法]]"
concepts:
  - "E+S⇌ES（k₁/k₋₁）、ES→E+P（k₂）"
  - "Km=(k₋₁+k₂)/k₁"
  - "[ES]=[E]₀[S]/(Km+[S])；d[P]/dt=Vmax[S]/(Km+[S])"
  - "酶 ε(299nm)=9000 dm³·mol⁻¹·cm⁻¹"
  - "Lineweaver-Burk 作图：1/V=(Km/Vmax)(1/[S])+1/Vmax"
  - "Vmax=0.114 μmol·dm⁻³·s⁻¹；Km=50.5 μmol·dm⁻³"
pack: 模块习题集
tags:
  - 化竞
  - 教材习题
  - 化学能力测试
  - 第6章
created: 2026-09-03
updated: 2026-09-03
source: 化学竞赛能力测试·第6章 简单的化学动力学原理·B卷第8题
source_file: "[[化学竞赛教程/（已压缩）化学竞赛能力测试]]"
status: 已填充
source_category: 竞赛导向·竞赛教辅
source_grade: A
---

# GTP 环水解酶酶动力学

> **来源**：化学竞赛能力测试·第6章·B卷第8题（10 分）

酶促动力学在药物发现中重要。酶用 $V_{\max}$ 和 $K_m$ 表征。

酶促反应：E + S ⇌ ES（k₁/k₋₁）、ES → E + P（k₂）。E 游离酶、S 底物、ES 复合物、P 产物。

**8-1** 稳态且 [S]≫[E]：(1) 用 [E]、[S]、[ES] 表示 ES 的生成速率；(2) P 的生成速率。

已知 [E]₀=[E]+[ES]，Km=(k₋₁+k₂)/k₁。

**8-2** 用 [S]、[E]₀、Km 表示 [ES]。

**8-3** 推出用 [E]₀、[S] 表示 P 的生成速率。

**8-4** $V_{\max}=k_2[E]_0$ 时，推出用 $V_{\max}$、$[S]$ 表示 P 生成速率。

GTP 环水解酶 II（cyclohydrolase II）催化细菌核黄素合成第一步：

![[a70a5948c159dd1a7a923b5d2e53fab6c8119d42a09cc1a835eb93710ec66343.jpg]]

迅速混合酶与不同浓度 GTP，299 nm 光（1 cm 光程）测吸光度。100 μM 纯产品 299 nm 吸光度 0.9。

数据：t=6~12 s 各 GTP 浓度（200/150/100/80/60/40/20 μM）吸光度变化 0.002~0.010。

**8-5** 计算各 GTP 浓度的起始速率。

**8-6** 以 y=mx+c 表达 (5) 结果。

**8-7** 推出 $V_{\max}$ 和 $K_m$。

<details>
<summary>📖 查看答案与解析</summary>

**8-1** (1) d[ES]/dt = k₁[E][S] − (k₋₁+k₂)[ES]；稳态 d[ES]/dt=0。

(2) d[P]/dt = k₂[ES]。

**8-2** [E]₀=[E]+[ES] 代入稳态：

$$[\mathrm{ES}] = \frac{[\mathrm E]_0[\mathrm S]}{K_\mathrm m + [\mathrm S]}$$

**8-3**

$$\frac{\mathrm d[\mathrm P]}{\mathrm dt} = \frac{k_2[\mathrm E]_0[\mathrm S]}{K_\mathrm m + [\mathrm S]}$$

**8-4**

$$\frac{\mathrm d[\mathrm P]}{\mathrm dt} = \frac{V_\mathrm{max}[\mathrm S]}{K_\mathrm m + [\mathrm S]}$$

**8-5** 由吸光度 A=εcl：产品 ε=0.9/(100×10⁻⁶×1)=9000 dm³·mol⁻¹·cm⁻¹。由 A~t 斜率求 d[P]/dt（各 GTP 浓度初始速率）：

| GTP/μM | 200 | 150 | 100 | 80 | 60 | 40 | 20 |
|---|---|---|---|---|---|---|---|
| V₀/μmol·dm⁻³·s⁻¹ | 0.0910 | 0.0871 | 0.0755 | 0.0702 | 0.0640 | 0.0464 | 0.0328 |

**8-6** Lineweaver-Burk（双倒数）：

$$\frac{1}{V_0} = \frac{K_\mathrm m}{V_\mathrm{max}}\cdot\frac{1}{[\mathrm S]} + \frac{1}{V_\mathrm{max}}$$

**8-7** 1/V₀ 对 1/[S] 作图（y=mx+c）：

$1/V_{\max}$ = 截距 → **$V_{\max}$ = 0.114 μmol·dm⁻³·s⁻¹**；$K_m/V_{\max}$ = 斜率 → **$K_m$ = 50.5 μmol·dm⁻³**。

</details>

<!-- 校勘注: ①ε=9000：A=εcl → 0.9=ε×100e-6 mol/dm³×1 cm → ε=9000 dm³·mol⁻¹·cm⁻¹ ✓；②起始速率由吸光度~t 初期斜率（前 6-8 s 近似线性）；③8-7 由 1/V₀~1/[S] 最小二乘/作图截距斜率得 Vmax/Km ✓；④本酶为 GTP 环水解酶（黄素合成第一步），产物 2,5-二氨基-6-核糖基氨基-4-嘧啶酮 299 nm 有吸收。 -->

## 知识点映射

| 知识点 | 本题应用 |
|---|---|
| [[酶动力学]] | Michaelis-Menten 稳态推导 |
| [[酶催化]] | $V_{\max}$、$K_m$ 药物靶点表征 |
| [[稳态近似]] | ES 稳态 |
| [[酶动力学]] | Michaelis-Menten 方程与双倒数作图 |
| [[分光光度法]] | ε=9000 由 A=εcl |