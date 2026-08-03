---
title: "Cannizzaro反应-苯甲醛在浓碱中的歧化"
aliases: [Cannizzaro反应, 歧化反应, 苯甲醛浓碱]
type: 真题
year: 2019
source: "中国化学奥林匹克(省级初赛)"
type_tag: "推断"
difficulty: 3
knowledge_points:
  - "Cannizzaro反应"
tags: [化竞, 真题, 有机化学, Cannizzaro反应]
related_notes:
  - "[[专题-羰基化学与缩合反应]]"
updated: 2026-06-22
teaching_level: 巩固
---

# Cannizzaro反应-苯甲醛在浓碱中的歧化

## 题目

苯甲醛 $\mathrm{PhCHO}$ 在浓 $\mathrm{NaOH}$（50%）溶液中加热，发生 Cannizzaro 反应。

(1) 写出主要有机产物的结构式和名称，并计算反应的原子经济性（原子利用率）。

(2) 写出 Cannizzaro 反应的详细机理，说明为什么需要浓碱条件，以及为什么是一分子醛被氧化、另一分子被还原。

(3) 甲醛 $\mathrm{HCHO}$ 在 Cannizzaro 反应条件下与苯甲醛混合，产物组成有何特点？写出产物。

(4) 为什么 Cannizzaro 反应仅适用于**无 α-H 的醛**（如苯甲醛、甲醛、三甲基乙醛）？若有 α-H 存在会发生什么竞争反应？

![[cannizzaro-mechanism-benzaldehyde.png]]

## 解析

### 分析

1. Cannizzaro 反应是无 α-H 的醛在浓碱中的**歧化反应**：一分子醛被氧化为羧酸盐，另一分子被还原为醇。
2. 关键中间体是 $\mathrm{PhCH(O^-)O^-}$（四面体双负离子），其中一分子提供 H⁻ 给另一分子醛。
3. 交叉 Cannizzaro 中，甲醛总是被氧化（更易形成四面体中间体）。
4. 若有 α-H 则发生 Aldol 缩合，而非 Cannizzaro 反应。

### 解答

**(1) 主要产物**

$$2\mathrm{PhCHO + NaOH \xrightarrow{浓} PhCH_2OH + PhCOONa}$$

- 还原产物：**苯甲醇**（$\mathrm{PhCH_2OH}$）
- 氧化产物：**苯甲酸钠**（$\mathrm{PhCOONa}$），酸化后得到苯甲酸

**原子经济性**：
原子利用率 = $\frac{M(\text{目标产物})}{M(\text{总反应物})} \times 100\%$

若以苯甲醇为目标产物：$\frac{108}{2\times106 + 40} = \frac{108}{252} \approx 42.9\%$

若以苯甲酸为目标产物：$\frac{122}{252} \approx 48.4\%$

较低的原子经济性体现了歧化反应的本质特征——一半原料被"牺牲"了。

**(2) 详细机理**

**步骤 1**：OH⁻ 对一分子苯甲醛的羰基进行亲核加成

$$\mathrm{PhCHO + OH^- \rightleftharpoons PhCH(O^-)OH}$$

（四面体中间体，去质子化后得 $\mathrm{PhCH(O^-)O^-}$ 双负离子）

**步骤 2（关键步）**：四面体中间体作为**氢负离子供体**，将 H⁻ 转移给第二分子苯甲醛

$$\mathrm{PhCH(O^-)O^- + PhCHO \longrightarrow PhCOO^- + PhCH_2O^-}$$

这是 Cannizzaro 反应的核心——从四面体中间体上离去的是 **H⁻**（不是质子），H⁻ 直接转移到另一分子醛的羰基碳上。这一步需要浓碱条件是因为只有高浓度 OH⁻ 才能将四面体中间体充分去质子化为双负离子，双负离子才是有效的 H⁻ 供体。

**步骤 3**：质子交换

$$\mathrm{PhCH_2O^- + H_2O \rightleftharpoons PhCH_2OH + OH^-}$$

**(3) 甲醛存在的交叉 Cannizzaro**

在浓碱条件下，苯甲醛 + 甲醛 → **苯甲醇 + 甲酸钠**

$$\mathrm{PhCHO + HCHO + NaOH \longrightarrow PhCH_2OH + HCOONa}$$

关键：甲醛总是被**氧化**（生成甲酸盐）。这是因为：
- 甲醛（$\mathrm{HCHO}$）的羰基碳空间位阻最小、亲电性最强
- 甲醛形成四面体中间体的速率最快
- 甲醛的四面体中间体比苯甲醛的更容易将 H⁻ 转移出去

因此，交叉 Cannizzaro 中甲醛优先作为"H⁻ 受体"→ 被还原为甲酸盐，而另一分子醛被氧化。

**(4) 适用范围**

Cannizzaro 反应仅适用于**无 α-H 的醛**，原因：

若醛有 α-H（如乙醛 $\mathrm{CH_3CHO}$），在浓碱中优先发生 **Aldol 缩合**——α-H 被 OH⁻ 夺去生成烯醇负离子，进而进攻另一分子醛的羰基。Aldol 缩合的反应速率远快于 Cannizzaro 反应的 H⁻ 转移步骤 → Cannizzaro 被完全抑制。

因此，Cannizzaro 的"必要非充分"条件是：醛必须无 α-H。常见底物：$\mathrm{HCHO}$、$\mathrm{PhCHO}$、$\mathrm{(CH_3)_3CCHO}$（三甲基乙醛）、呋喃甲醛（糠醛）等。

### 反思

Cannizzaro 反应是初赛中最容易与 Aldol 缩合混淆的反应。区分法则：**无 α-H → Cannizzaro；有 α-H → Aldol**。交叉 Cannizzaro 中，甲醛永远被氧化。另一个常考变体是分子内 Cannizzaro（如乙二醛 → 乙醇酸盐）。
