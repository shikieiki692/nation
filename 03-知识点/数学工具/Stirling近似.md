---
title: Stirling近似
aliases: ["斯特林公式", "斯特林近似", "Stirling公式", "阶乘近似", "Stirling's Approximation"]
type: 工具卡
subject: 数学工具
module: 数学工具
tags: [化竞, 数学工具, Stirling近似, 阶乘, 统计热力学, 熵]
related: [组合计数与二项分布, 对数与指数运算, 量纲分析与数量级估算]
prerequisite: [组合计数与二项分布, 对数与指数运算]
difficulty: 4
importance: 4
status: 已填充
stage: published
sources: ["Mortimer《Mathematics for Physical Chemistry》§16", "McQuarrie 数学章节 J"]
source_type: [教材]
syllabus_stage: []
syllabus_code: []
syllabus_module: []
syllabus_note: "数学工具层——中国化学奥林匹克考纲无对应条目，故 syllabus_* 留空"
handout_ref: "[[数学工具-第7讲-组合概率与Stirling近似]]"
template_version: v1.0
updated: 2026-09-11
has_images: false
image_count: 0
---

# Stirling近似

## 一句话

$\ln(N!)$ 在 $N\sim10^{23}$ 时**不是不能算，而是简单得出奇**——把求和换成积分即可，代价是一个可量化的误差。

## 公式

```
简单式：ln(N!) ≈ N ln N − N                       （N ≳ 10³，化学常用）
完整式：ln(N!) ≈ N ln N − N + ½ ln(2πN)           （N ≲ 100 时必须用）
阶乘式：N! ≈ sqrt(2πN) (N/e)^N
```

**推导思路**：$\ln(N!)=\sum_{k=1}^N\ln k \approx \int_1^N\ln x\,dx = N\ln N-N+1$，常数 1 在大 $N$ 时可忽略。

## 精度表（务必看）

| $N$ | $\ln(N!)$ 真值 | 简单式相对误差 | 完整式相对误差 |
|:--|:--|:--|:--|
| 10 | 15.104 | **13.7%** | 0.055% |
| 100 | 363.739 | **0.89%** | `2.3×10⁻⁶` |
| 1000 | 5912.128 | **0.074%** | `~10⁻⁷` |
| $10^6$ | `1.2816×10⁷` | `6×10⁻⁵`% | `~10⁻¹³` |
| $10^{23}$ | `5.196×10²⁴` | `~5×10⁻²⁴` | 可忽略 |

**结论**：$N\lesssim100$ 必须用完整式；$N\geq10^3$ 简单式误差 `<0.1%`；
$N\sim10^{23}$ 时简单式的绝对误差只有约 27（即 $\frac12\ln(2\pi N)$），相对误差约 $10^{-24}$。

## 两个常用推论

- $n\ll N$ 时：$\ln\dfrac{N!}{(N-n)!}\approx n\ln N$
- 二项式系数：$\ln C(2n,n)\approx 2n\ln2-\frac12\ln(\pi n)$，即 $C(2n,n)\approx\dfrac{4^n}{\sqrt{\pi n}}$

## 化学落点

**混合熵**：$W=\dfrac{N!}{\prod N_i!}$ 代入 Stirling，$-N$ 项与 $\sum N_i$ 抵消，得

$\ln W = -N\sum_i x_i\ln x_i \quad\Longrightarrow\quad \Delta S_{\text{mix}} = -nR\sum_i x_i\ln x_i$

等摩尔二元：$R\ln2 = 5.76\ \mathrm{J\,mol^{-1}K^{-1}}$；0.25/0.75：4.68。

**自由膨胀**：$W\propto V^N$，$\Delta S = k\ln(W_2/W_1)=nR\ln(V_2/V_1)$，与热力学公式一致。

## 易错点（最重要的一条）

当 $N!$ 出现在**分子分母相消**的位置（如 $\ln W=\ln N!-\sum\ln N_i!$）时，$-N$ 项会抵消，
但 $\frac12\ln(2\pi N)$ 项**不会完全抵消**。

例：$N=100$ 两等分组，$\ln C(100,50)$ 真值 66.79，简单式给 69.32，**偏高 3.8%**。
净修正为 $\frac12\ln(2\pi\times100)-2\times\frac12\ln(2\pi\times50)=3.22-2\times2.88=-2.53$，加回后 $69.32-2.53=66.79$ ✓

**所以：小体系务必用完整式；$N\sim10^{23}$ 时两者都行。**

## 参见

讲义 [[数学工具-第7讲-组合概率与Stirling近似]]；计数见 [[组合计数与二项分布]]；应用见 [[决赛要求/物理化学深化/Boltzmann统计初步]]。
