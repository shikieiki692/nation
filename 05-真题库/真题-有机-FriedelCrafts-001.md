---
title: "Friedel-Crafts反应-苯与1-氯丙烷的烷基化与碳正离子重排"
aliases: [Friedel-Crafts烷基化, 碳正离子重排, 1-氯丙烷]
type: 真题
status: 已填充
year: 2022
source: "中国化学奥林匹克(省级初赛)"
type_tag: "推断"
difficulty: 3
knowledge_points: ["[[Friedel-Crafts反应]]", "[[碳正离子]]", "[[芳香亲电取代反应]]"]
tags: [化竞, 真题, 有机化学, Friedel-Crafts反应]
related_notes:
  - "[[专题-芳香反应]]"
updated: 2026-08-31
teaching_level: 巩固
fidelity: 原书改写
exam_stage: 省预赛
subject_module: 有机化学
pack: 预赛专项
---

# Friedel-Crafts反应-苯与1-氯丙烷的烷基化与碳正离子重排

## 题目

在无水 $\mathrm{AlCl_3}$ 催化下，苯与1-氯丙烷 $\mathrm{CH_3CH_2CH_2Cl}$ 反应。

(1) 该反应属于哪一类反应？写出反应类型的名称和核心方程式。

(2) 实验表明，主要产物并非正丙苯，而是异丙苯。请解释原因，并画出完整的碳正离子生成与重排机理。

(3) 该反应还会得到少量多烷基化产物。写出可能生成的二取代产物的结构式（至少三种），并指出哪一种量最多，为什么？

(4) 简述 Friedel-Crafts 烷基化反应的三个主要局限性。


![[eas-mechanism.png]]

## 解析

### 分析

1. 无水 AlCl₃ 催化下卤代烷与苯反应 → **Friedel-Crafts 烷基化反应**。
2. 1-氯丙烷在 AlCl₃ 作用下生成的 1° 碳正离子 $\mathrm{CH_3CH_2CH_2^+}$ 不稳定，会发生**氢负离子的 1,2-迁移**重排为更稳定的 2° 碳正离子 $\mathrm{CH_3\mathop{CH}\limits^{+}CH_3}$ → 最终产物为异丙苯。
3. 烷基化产物比苯更活泼（烷基是活化基团）→ 易发生多取代。
4. 局限性：碳正离子重排、多取代、不能用于钝化苯环、不能引入含强给电子基或强吸电子基的芳环。

### 解答

**(1) 反应类型**

**Friedel-Crafts 烷基化反应**。

总方程式：
$$\mathrm{C_6H_6 + CH_3CH_2CH_2Cl \xrightarrow{AlCl_3} C_6H_5CH(CH_3)_2 + HCl}$$

**(2) 重排机理**

**步骤 1**：AlCl₃ 活化卤代烷，生成亲电试剂

$$\mathrm{CH_3CH_2CH_2Cl + AlCl_3 \longrightarrow CH_3CH_2CH_2^+ + AlCl_4^-}$$

**步骤 2**：1° 碳正离子不稳定，发生 1,2-氢迁移（H⁻ 迁移）

$$\mathrm{CH_3CH_2\mathop{CH}\limits^{+}_2 \longrightarrow CH_3\mathop{CH}\limits^{+}CH_3}$$

重排驱动力：$1^\circ \to 2^\circ$ 碳正离子稳定性增加（超共轭效应更强）。

**步骤 3**：2° 碳正离子作为亲电试剂，进攻苯环

$$\mathrm{C_6H_6 + (CH_3)_2CH^+ \longrightarrow [C_6H_6\text{-}CH(CH_3)_2]^+}$$

（Wheland 中间体 / σ-络合物）

**步骤 4**：去质子化恢复芳香性

$$\mathrm{[C_6H_6\text{-}CH(CH_3)_2]^+ \longrightarrow C_6H_5CH(CH_3)_2 + H^+}$$

因此最终产物是**异丙苯**，而非正丙苯。

**(3) 多烷基化产物**

可能生成的二取代产物（二异丙基苯的三种异构体）：

| 产物 | 结构 | 相对含量 |
|:---|:---|:---|
| 对二异丙基苯 | $p\text{-}\mathrm{C_6H_4[CH(CH_3)_2]_2}$ | 最多 |
| 邻二异丙基苯 | $o\text{-}\mathrm{C_6H_4[CH(CH_3)_2]_2}$ | 较少（位阻） |
| 间二异丙基苯 | $m\text{-}\mathrm{C_6H_4[CH(CH_3)_2]_2}$ | 最少 |

对位产物最多，因为异丙基是邻/对位定位基，且对位无位阻。

**(4) FC 烷基化反应的三个主要局限性**

1. **碳正离子重排**：1° 卤代烷常经重排得到重排产物，难以直接引入直链烷基。
2. **多烷基化不可避免**：烷基使苯环活化 → 产物比反应物更活泼 → 多取代难以避免。可用过量苯减少多取代。
3. **不能用于钝化苯环**：当苯环上已有强吸电子基（如 -NO₂、-CN、-COR）时反应不进行；同样也不能在含 -NH₂/-NHR/-OH 等 Lewis 碱基团的苯环上进行（它们会与 AlCl₃ 络合使催化剂失活）。

### 反思

FC 烷基化是芳香亲电取代的必考内容，其最核心的考点就是**碳正离子重排**——1° 卤代烷的产物往往不是直接的正烷基苯，而是重排后的异构体。要避免重排，可使用 FC 酰基化 + Clemmensen/Wolff-Kishner 还原的组合策略间接引入正烷基。

