---
title: "Born-Haber循环-从热力学数据计算NaCl的晶格能"
aliases: [玻恩-哈伯循环, 晶格能计算, 热化学循环]
type: 真题
year: 2020
source: "中国化学奥林匹克(省级初赛)"
type_tag: "计算"
difficulty: 3
knowledge_points:
  - "晶格能"
tags:
  - 化竞
  - 真题
  - Born-Haber循环
  - 晶格能
  - 热化学
related_notes:
  - "[[专题-热力学初步]]"
updated: 2026-06-22
---

# Born-Haber循环-从热力学数据计算NaCl的晶格能

## 题目

利用以下热力学数据（单位：$\mathrm{kJ\cdot mol^{-1}}$），通过 Born-Haber 循环计算 NaCl 晶体的晶格能 $U$：

| 过程 | $\Delta H$ ($\mathrm{kJ\cdot mol^{-1}}$) |
|------|------------------------------------------|
| $\mathrm{Na(s) \to Na(g)}$（升华焓） | $+108$ |
| $\mathrm{\frac{1}{2}Cl_2(g) \to Cl(g)}$（$\mathrm{Cl_2}$ 解离焓的 $\frac{1}{2}$） | $+121$ |
| $\mathrm{Na(g) \to Na^+(g) + e^-}$（电离能 $I_1$） | $+496$ |
| $\mathrm{Cl(g) + e^- \to Cl^-(g)}$（电子亲和能 $E_A$） | $-349$ |
| $\mathrm{Na(s) + \frac{1}{2}Cl_2(g) \to NaCl(s)}$（生成焓 $\Delta_f H^\ominus$） | $-411$ |

(1) 画出 Born-Haber 循环图，标出各步的 $\Delta H$。

(2) 根据 Hess 定律，计算 NaCl 的晶格能 $U$（$\mathrm{Na^+(g) + Cl^-(g) \to NaCl(s)}$）。

(3) 晶格能的理论值（由 Born-Lande 方程计算）约为 $-786\ \mathrm{kJ\cdot mol^{-1}}$。实验值比理论值偏小（绝对值更小），从化学键角度分析可能的原因。


![[born-haber-cycle.png]]

## 解析

### 分析

1. Born-Haber 循环将晶格能与其他可直接测量的热力学量关联，利用 Hess 定律求解
2. 循环路径：$\mathrm{Na(s) + \frac{1}{2}Cl_2(g)} \xrightarrow{\Delta_f H} \mathrm{NaCl(s)}$（直接）vs 经原子化→电离→电子亲和→晶格能（间接）
3. 实验值与 Born-Lande 理论值的偏差可归因于离子模型中未考虑的共价成分和极化效应

### 解答

**(1) Born-Haber 循环图**

```
Na(s) + 1/2 Cl2(g) ——ΔfH°=−411——→ NaCl(s)
    |                                      ↑
    | +108 (升华)                          | U = ?
    ↓                                      |
  Na(g)                                    |
    | +496 (IE1)                           |
    ↓                                      |
  Na+(g) + e−                              |
    |                                      |
    | +121 (解离)                          |
    ↓                                      |
  Na+(g) + Cl(g) + e−                      |
    | −349 (EA)                            |
    ↓                                      |
  Na+(g) + Cl−(g) —————U————→ NaCl(s)
```

**(2) 计算晶格能**

根据 Hess 定律（所有路径焓变之和等于直接生成焓）：

$$\Delta_f H^\ominus = \Delta H_{\text{sub}} + \frac{1}{2}D_{\mathrm{Cl_2}} + I_1 + E_A + U$$

$$-411 = 108 + 121 + 496 + (-349) + U$$

$$-411 = 376 + U$$

$$U = -411 - 376 = -787\ \mathrm{kJ\cdot mol^{-1}}$$

**(3) 实验值与理论值的差异**

实验值 $U = -787\ \mathrm{kJ\cdot mol^{-1}}$，Born-Lande 理论值约 $-786\ \mathrm{kJ\cdot mol^{-1}}$，二者基本吻合（NaCl 是典型的离子晶体）。微小差异（实验值绝对值稍大）可归因于：

- Born-Lande 模型假设纯离子键，实际 NaCl 中含有少量**共价成分**（阴阳离子轨道部分重叠），这种额外相互作用使晶格更稳定
- 离子并非刚性球，存在电子云**极化效应**
- Born-Lande 中的 Madelung 常数和 Born 指数 $n$ 是近似值

> 注：对于 AgCl、CuCl 等共价成分更大的化合物，实验晶格能会显著偏离 Born-Lande 理论值（绝对值更大），因为额外的共价稳定化作用。

### 反思

Born-Haber 循环的核心是状态函数法——无论途径如何，总焓变相同。常见错误：(1) 电子亲和能的符号——放热为负值；(2) 忘记 $\mathrm{Cl_2}$ 的解离焓需要除以 2；(3) 循环中箭头方向与符号的对应关系混乱。

## 答案

(1) 见循环图。

(2) $U = -787\ \mathrm{kJ\cdot mol^{-1}}$。

(3) 理论值 $-786\ \mathrm{kJ\cdot mol^{-1}}$ 与实验值基本一致。微小偏差来自 Born-Lande 模型未考虑的共价成分和极化效应。

