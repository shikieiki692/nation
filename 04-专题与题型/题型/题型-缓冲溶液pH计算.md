---
title: "题型-缓冲溶液pH计算"
type: 题型
tags: [化竞, 题型]
subject: 化学
status: 已填充
stage: review
created: 2026-06-30
updated: 2026-07-12
source_extracts:
  - source_file: "[[07-资料提炼/书籍提炼/提炼-普化原理-第8章-酸碱平衡]]"
    asset_id: "普化原理Ch8"
    asset_type: "书籍提炼"
    asset_summary: "酸碱平衡教材主干，含缓冲溶液pH计算"
---

# 题型 · 缓冲溶液pH计算

> **状态**: 已填充，待审核
> **注意**: 本题型与 [[题型-缓冲溶液计算]] 内容重叠，建议优先使用 [[题型-缓冲溶液计算]]。后续可考虑合并。

## 解题思路

缓冲溶液 pH 计算的核心是 Henderson-Hasselbalch 方程。对于弱酸 HA 及其共轭碱 $\text{A}^-$ 组成的缓冲体系，$\text{pH} = \text{p}K_a + \log\frac{[\text{A}^-]}{[\text{HA}]}$。该方程表明缓冲溶液的 pH 取决于 $\text{p}K_a$ 和共轭酸碱对的浓度比。

缓冲容量 $\beta$ 是衡量缓冲溶液抵抗 pH 变化能力的指标，定义为 $\beta = \frac{dc_b}{d\text{pH}} = -\frac{dc_a}{d\text{pH}}$。当 $[\text{A}^-] = [\text{HA}]$ 时，缓冲容量最大，此时 $\text{pH} = \text{p}K_a$。缓冲溶液的有效缓冲范围为 $\text{pH} = \text{p}K_a \pm 1$。

在计算缓冲溶液 pH 时，需要注意以下几点：(1) 缓冲对浓度应足够大（通常 > 0.01 mol/L），以保证缓冲能力；(2) 当加入强酸或强碱时，需重新计算缓冲对浓度；(3) 当稀释缓冲溶液时，若稀释倍数不大，pH 变化很小；(4) 当缓冲对浓度比超出 0.1~10 范围时，缓冲能力显著下降。

对于多元酸缓冲体系，需选择合适的 $\text{p}K_a$ 值。例如，磷酸盐缓冲液可使用 $\text{H}_2\text{PO}_4^-/\text{HPO}_4^{2-}$ 体系（$\text{p}K_{a2} = 7.21$），适用于 pH 6.2~8.2 的范围。

## 核心方法

1. **Henderson-Hasselbalch 方程法**：直接应用 $\text{pH} = \text{p}K_a + \log\frac{[\text{A}^-]}{[\text{HA}]}$ 计算
2. **物料守恒法**：根据缓冲对的总浓度和加入的强酸/强碱量，重新计算各组分浓度
3. **缓冲容量计算法**：利用 $\beta = 2.303 \times \frac{K_w}{[\text{H}^+]} + 2.303 \times c \times \frac{K_a[\text{H}^+]}{(K_a + [\text{H}^+])^2}$ 计算缓冲容量
4. **缓冲溶液配算法**：根据目标 pH 和缓冲容量，计算所需缓冲对的浓度和比例
5. **稀释影响分析法**：分析稀释对缓冲溶液 pH 和缓冲容量的影响

## 典型例题

### 例题1：HAc/NaAc 缓冲体系 pH 计算

**题目**：将 $0.10\ \text{mol}\ \text{HAc}$ 和 $0.10\ \text{mol}\ \text{NaAc}$ 溶于水配成 $1.0\ \text{L}$ 缓冲溶液。已知 $\text{HAc}$ 的 $K_a = 1.8 \times 10^{-5}$。计算：
(1) 缓冲溶液的 pH
(2) 在 $1.0\ \text{L}$ 该缓冲溶液中加入 $0.010\ \text{mol}\ \text{HCl}$ 后溶液的 pH
(3) 在 $1.0\ \text{L}$ 该缓冲溶液中加入 $0.010\ \text{mol}\ \text{NaOH}$ 后溶液的 pH

**解答**：
(1) 缓冲溶液初始 pH：
$$\text{pH} = \text{p}K_a + \log\frac{[\text{Ac}^-]}{[\text{HAc}]} = -\log(1.8 \times 10^{-5}) + \log\frac{0.10}{0.10} = 4.74 + 0 = 4.74$$

(2) 加入 $0.010\ \text{mol}\ \text{HCl}$ 后：
$\text{HCl}$ 与 $\text{Ac}^-$ 反应：$\text{HCl} + \text{Ac}^- \rightarrow \text{HAc} + \text{Cl}^-$

反应后：
$$n(\text{HAc}) = 0.10 + 0.010 = 0.11\ \text{mol}$$
$$n(\text{Ac}^-) = 0.10 - 0.010 = 0.09\ \text{mol}$$

$$\text{pH} = 4.74 + \log\frac{0.09}{0.11} = 4.74 + \log(0.818) = 4.74 - 0.087 = 4.65$$

(3) 加入 $0.010\ \text{mol}\ \text{NaOH}$ 后：
$\text{NaOH}$ 与 $\text{HAc}$ 反应：$\text{NaOH} + \text{HAc} \rightarrow \text{NaAc} + \text{H}_2\text{O}$

反应后：
$$n(\text{HAc}) = 0.10 - 0.010 = 0.09\ \text{mol}$$
$$n(\text{Ac}^-) = 0.10 + 0.010 = 0.11\ \text{mol}$$

$$\text{pH} = 4.74 + \log\frac{0.11}{0.09} = 4.74 + \log(1.222) = 4.74 + 0.087 = 4.83$$

### 例题2：缓冲溶液配制计算

**题目**：欲配制 $\text{pH} = 5.00$ 的缓冲溶液 $500\ \text{mL}$，要求缓冲容量最大。现有 $0.10\ \text{mol/L}\ \text{HAc}$ 和 $0.10\ \text{mol/L}\ \text{NaAc}$ 溶液，如何配制？

**解答**：
缓冲容量最大时，$[\text{Ac}^-] = [\text{HAc}]$，此时 $\text{pH} = \text{p}K_a = 4.74$。但题目要求 $\text{pH} = 5.00$，需调整比例。

由 Henderson-Hasselbalch 方程：
$$5.00 = 4.74 + \log\frac{[\text{Ac}^-]}{[\text{HAc}]}$$
$$\log\frac{[\text{Ac}^-]}{[\text{HAc}]} = 0.26$$
$$\frac{[\text{Ac}^-]}{[\text{HAc}]} = 10^{0.26} = 1.82$$

设需要 $\text{HAc}$ 溶液 $V_1\ \text{mL}$，$\text{NaAc}$ 溶液 $V_2\ \text{mL}$，则：
$$V_1 + V_2 = 500\ \text{mL}$$
$$\frac{0.10 \times V_2}{0.10 \times V_1} = 1.82 \Rightarrow \frac{V_2}{V_1} = 1.82$$

解得：
$$V_1 = \frac{500}{1 + 1.82} = 177\ \text{mL}$$
$$V_2 = 500 - 177 = 323\ \text{mL}$$

验证缓冲容量：此时 $[\text{Ac}^-]/[\text{HAc}] = 1.82$，在 0.1~10 范围内，缓冲能力较好。

## 易错点

1. **Henderson-Hasselbalch 方程适用条件**：该方程要求缓冲对浓度足够大（通常 > 0.01 mol/L），且浓度比在 0.1~10 之间。当浓度过低或比例超出此范围时，需用精确公式计算。

2. **加入强酸强碱后浓度计算错误**：加入强酸（如 $\text{HCl}$）会消耗共轭碱（$\text{Ac}^-$），生成弱酸（$\text{HAc}$）；加入强碱（如 $\text{NaOH}$）会消耗弱酸（$\text{HAc}$），生成共轭碱（$\text{Ac}^-$）。需重新计算两者浓度。

3. **缓冲容量最大条件误解**：缓冲容量最大时 $[\text{A}^-] = [\text{HA}]$，此时 $\text{pH} = \text{p}K_a$。但题目要求的 pH 可能不是 $\text{p}K_a$，此时需调整比例，缓冲容量会降低。

4. **稀释对 pH 影响的误解**：对于缓冲溶液，稀释时 $[\text{A}^-]/[\text{HA}]$ 比值不变，pH 基本不变。但缓冲容量会随稀释而降低。

5. **多元酸缓冲体系 $\text{p}K_a$ 选择错误**：如磷酸盐缓冲液，应根据目标 pH 选择合适的 $\text{p}K_a$。$\text{p}K_{a1} = 2.12$，$\text{p}K_{a2} = 7.21$，$\text{p}K_{a3} = 12.32$，分别适用于不同 pH 范围。