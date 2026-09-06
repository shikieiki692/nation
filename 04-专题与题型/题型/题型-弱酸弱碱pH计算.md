---
title: "题型-弱酸弱碱pH计算"
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
    asset_summary: "酸碱平衡教材主干，含弱酸弱碱pH精确计算"
---

# 题型 · 弱酸弱碱pH计算

> **来源专题**：[[专题-酸碱理论]]
> **核心考向**：一元/多元弱酸pH近似计算、精确公式、分步近似

## 解题思路

弱酸弱碱pH计算的核心是**先判据、再选公式、最后验证**。拿到题目后，第一步不是代公式，而是判断近似条件是否成立：$c/K_a \geq 400$ 时可用最简式 $[\mathrm{H}^+] = \sqrt{cK_a}$，否则需解二次方程。对于多元弱酸，若 $K_{a1} \gg K_{a2}$（相差 $10^5$ 倍以上），可分步近似——先当一元弱酸处理求 $[\mathrm{H}^+]$，再利用总平衡求低级电离产物浓度。

一元弱碱的处理与弱酸完全对称，只需将 $K_a$ 替换为 $K_b = K_w/K_a$，将 $[\mathrm{H}^+]$ 替换为 $[\mathrm{OH}^-]$。两性物质（如 NaHCO₃、Na₂HPO₄）需用近似公式 $[\mathrm{H}^+] \approx \sqrt{K_{a1}K_{a2}}$，该公式在 $c \gg K_{a1}$ 且 $cK_{a2} \gg K_w$ 时成立。

验证环节不可省略：算出 $[\mathrm{H}^+]$ 后必须检查是否小于初始浓度 $c$，电离度 $\alpha = [\mathrm{H}^+]/c$ 是否小于5%。若 $\alpha > 5\%$，说明近似失效，必须回到精确方程。

## 核心方法

1. **判据优先**：$c/K_a \geq 400$ → 最简式；$cK_a > 10K_w$ → 可忽略水电离
2. **多元酸分步近似**：$K_{a1} \gg K_{a2}$ 时，一级电离主导 $[\mathrm{H}^+]$，二级电离可忽略
3. **两性物质公式**：$[\mathrm{H}^+] \approx \sqrt{K_{a1}K_{a2}}$（适用条件：$c \gg K_{a1}$ 且 $cK_{a2} \gg K_w$）
4. **精确解方程**：$K_a = x^2/(c-x)$，当近似条件不满足时必须解二次方程
5. **验证5%原则**：$\alpha = [\mathrm{H}^+]/c < 5\%$，否则近似无效

## 典型例题

### 例题 1：一元弱酸HF的pH计算（⭐⭐⭐）

**题目**：1.00 mol/L HF溶液，$K_a = 7.2 \times 10^{-4}$，求pH。

**解答**：

判据检查：
$$c/K_a = 1.00/(7.2 \times 10^{-4}) = 1389 > 400 \quad \checkmark$$
$$cK_a = 7.2 \times 10^{-4} > 10K_w \quad \checkmark$$

最简式适用：
$$[\mathrm{H}^+] = \sqrt{cK_a} = \sqrt{1.00 \times 7.2 \times 10^{-4}} = 2.68 \times 10^{-2}\ \mathrm{mol/L}$$

$$\mathrm{pH} = -\lg(2.68 \times 10^{-2}) = \mathbf{1.57}$$

验证：$\alpha = 2.68 \times 10^{-2}/1.00 = 2.68\% < 5\%$ ✓

**反思**：HF的$K_a$数量级（$10^{-4}$）是常见弱酸的"边界案例"。若浓度降至0.01 mol/L，则$c/K_a = 13.9 < 400$，最简式失效，需解二次方程。

---

### 例题 2：二元弱酸H₂S分步近似（⭐⭐⭐⭐）

**题目**：0.10 mol/L H₂S溶液，$K_{a1} = 8.9 \times 10^{-8}$，$K_{a2} = 1.2 \times 10^{-13}$，求pH和$[\mathrm{S}^{2-}]$。

**解答**：

**(1) pH计算**：

判据检查：
$$cK_{a1} = 0.10 \times 8.9 \times 10^{-8} = 8.9 \times 10^{-9} > 10K_w \quad \checkmark$$
$$c/K_{a1} = 0.10/(8.9 \times 10^{-8}) = 1.1 \times 10^{6} > 400 \quad \checkmark$$

$$[\mathrm{H}^+] = \sqrt{cK_{a1}} = \sqrt{0.10 \times 8.9 \times 10^{-8}} = 9.4 \times 10^{-5}\ \mathrm{mol/L}$$

$$\mathrm{pH} = \mathbf{4.03}$$

**(2) $[\mathrm{S}^{2-}]$计算**：

利用总平衡 $\mathrm{H_2S \rightleftharpoons 2H^+ + S^{2-}}$，$K = K_{a1}K_{a2} = 1.07 \times 10^{-20}$：

$$[\mathrm{S}^{2-}] = \frac{K_{a1}K_{a2} \cdot [\mathrm{H_2S}]}{[\mathrm{H}^+]^2} \approx \frac{1.07 \times 10^{-20} \times 0.10}{(9.4 \times 10^{-5})^2} = \mathbf{1.2 \times 10^{-13}\ \mathrm{mol/L}}$$

**反思**：$K_{a1}$与$K_{a2}$相差约$10^5$倍，二级电离对$[\mathrm{H}^+]$的贡献可忽略。$[\mathrm{S}^{2-}]$受pH强烈控制——这正是后续硫化物沉淀平衡的基础。

## 易错点

1. **不判据就代公式**：最简式的前提条件是$c/K_a \geq 400$，不满足时必须解二次方程，否则可能得出$[\mathrm{H}^+] > c$的荒谬结果
2. **多元酸分步近似条件不满足**：若$K_{a1}/K_{a2} < 10^5$，不能忽略二级电离对$[\mathrm{H}^+]$的贡献
3. **两性物质公式误用**：$[\mathrm{H}^+] = \sqrt{K_{a1}K_{a2}}$仅在$c \gg K_{a1}$且$cK_{a2} \gg K_w$时成立，Na₂HPO₄等体系需更精确的公式
4. **忘记验证5%原则**：算出$[\mathrm{H}^+]$后必须检查$\alpha < 5\%$，否则近似无效
