---
title: "题-有机-重排-Pinacol重排不对称底物判断"
type: 题目
fidelity: 自编
submodule: 重排反应
exam_stage: 初赛
source_subject: 有机化学
difficulty: 4
teaching_level: 拓展
syllabus_codes: ["46"]
knowledge_points: ["[[Pinacol重排]]"]
tags: [化竞, 题目, 有机化学, 第三轮]
updated: 2026-06-06
aliases: ["题-有机-重排-01"]
source: "专题页提炼"
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 模块习题集
---
# Pinacol 重排不对称底物判断

## 题目

2,3-二甲基-2,3-丁二醇（pinacol，频哪醇）在 $\mathrm{H_2SO_4}$ 催化下发生 Pinacol 重排，生成频哪酮（pinacolone，3,3-二甲基-2-丁酮）。

**(1)** 写出对称 pinacol 重排的完整机理（用箭头推电子）。

**(2)** 对于**不对称**底物——2-苯基-2,3-丁二醇（$\mathrm{PhC(CH_3)(OH)CH(OH)CH_3}$），在酸催化下发生 Pinacol 重排：
- (a) 两个 OH 中，哪一个更易质子化后离去？为什么？
- (b) 哪一个基团发生 1,2-迁移？预测两种可能产物及其比例。
- (c) 写出完整的重排机理和产物。

**(3)** Pinacol 重排与半频哪醇重排（semipinacol rearrangement）有什么区别？各举一例。

## 参考答案

### (1) 对称 Pinacol 重排机理

底物：$\mathrm{(CH_3)_2C(OH)C(OH)(CH_3)_2}$

**Step 1 ——质子化与脱水**：
一个 OH 被 $\mathrm{H^+}$ 质子化后以 $\mathrm{H_2O}$ 形式离去，生成碳正离子：
$$
\mathrm{(CH_3)_2C(OH)C(OH)(CH_3)_2 \xrightarrow{H^+} (CH_3)_2C(OH)C(OH_2^+)(CH_3)_2 \xrightarrow{-H_2O} (CH_3)_2C(OH)C^+(CH_3)_2}
$$

**Step 2 ——1,2-甲基迁移**：
邻位 C 上的甲基带着一对电子迁移到缺电子碳，同时 OH 失去质子形成羰基：
$$
\mathrm{(H_3C)_2C(OH)C^+(CH_3)_2 \xrightarrow{1,2-CH_3\;shift} (H_3C)_2\overset{+}{C}C(OH)(CH_3)_2 \longrightarrow (CH_3)_3CC(=O)CH_3}
$$

（迁移基团从 OH 所在碳的相邻碳迁移至碳正离子中心，OH 变为 C=O。）

产物为频哪酮（3,3-二甲基-2-丁酮）。

### (2) 不对称 Pinacol 重排

底物：$\mathrm{PhC(CH_3)(OH)CH(OH)CH_3}$（2-苯基-2,3-丁二醇）

#### (a) 哪个 OH 先离去？

两个 OH 分别位于：
- C2：$\mathrm{PhC(CH_3)(OH)}$——连接苯基
- C3：$\mathrm{CH(OH)CH_3}$——连接 H 和 CH₃

质子化后脱水，生成的碳正离子稳定性决定了哪个 OH 更易离去。

- 若 C2-OH 离去 → C2 碳正离子：$\mathrm{Ph\overset{+}{C}(CH_3)CH(OH)CH_3}$（苄基型二级碳正离子，共振稳定化能约 50 kJ/mol）
- 若 C3-OH 离去 → C3 碳正离子：$\mathrm{PhC(CH_3)(OH)\overset{+}{C}HCH_3}$（普通二级碳正离子）

**C2 生成的碳正离子是苄基型**，比 C3 的普通二级碳正离子稳定得多。

**结论：C2-OH 优先离**去（形成苄基型碳正离子）。

#### (b) 迁移基团选择

C2 碳正离子生成后（$\mathrm{Ph\overset{+}{C}(CH_3)CH(OH)CH_3}$），C3 上的基团发生 1,2-迁移。C3 上可迁移的基团：
- $\mathrm{H}$（氢迁移，生成醛）
- $\mathrm{CH_3}$（甲基迁移，生成酮）
- $\mathrm{OH}$（羟基迁移，但羟基的迁移倾向低于 H 和烷基）

**1,2-迁移倾向（迁移基团的"迁移能力"）**：
$$
\mathrm{Ph \approx H > CH_3 > C_2H_5 > (CH_3)_2CH > (CH_3)_3C}
$$

苯基（通过桥式过渡态）和 H 最容易迁移。

在 C2 碳正离子上，C3 的迁移基团选择：H 迁移 > CH₃ 迁移。

**两种可能产物**：
- **H 迁移**（主要）：生成 $\mathrm{PhC(CH_3)_2CHO}$（2-苯基异丁醛或类似结构的醛）
- **CH₃ 迁移**（次要）：生成 $\mathrm{PhCH(CH_3)COCH_3}$（相应的酮）

比例：H 迁移 : CH₃ 迁移 ≈ 70 : 30（典型 Pinacol 重排中 H > 烷基的迁移倾向）。

#### (c) 完整机理

**主路径（H 迁移）**：

1. C2-OH 质子化 → 脱水 → 形成苄基型碳正离子：
   $\mathrm{PhC(CH_3)(OH_2^+)CH(OH)CH_3 \xrightarrow{-H_2O} Ph\overset{+}{C}(CH_3)CH(OH)CH_3}$
2. C3 上的 H 1,2-迁移到 C2 → C3 变为羰基：
   $\mathrm{Ph\overset{+}{C}(CH_3)CH(OH)CH_3 \xrightarrow{1,2-H\;shift} PhCH(CH_3)\overset{+}{C}(OH)CH_3 \xrightarrow{-H^+} PhCH(CH_3)COCH_3}$
   
   产物：3-苯基-2-丁酮 $\mathrm{PhCH(CH_3)COCH_3}$

**次要路径（CH₃ 迁移）**：

C3 上的 CH₃ 1,2-迁移到 C2（与 H 迁移竞争的次要路径）→ 生成另一种酮。

### (3) Pinacol 重排 vs 半频哪醇重排

| | Pinacol 重排 | 半频哪醇重排 (Semipinacol) |
|:---|:---|:---|
| 底物 | 1,2-二醇 | $\beta$-羟基（或烷氧基）离去基团（如 $\beta$-羟基环氧化物、$\beta$-羟基卤代物等） |
| 驱动力 | OH 质子化脱水生成碳正离子 | 离去基团的电离或开环（如环氧化物酸催化开环） |
| 中间体 | 碳正离子 | 碳正离子 |
| 经典例子 | Pinacol → Pinacolone | 2,3-环氧醇 → $\alpha$-取代酮 |

**半频哪醇重排实例**：

环己烯氧化物在 $\mathrm{BF_3}$ 催化下开环重排：

$$
\mathrm{环氧环己烷 \xrightarrow{BF_3} 开环碳正离子 \xrightarrow{1,2-H\;shift} 环己酮}
$$

H 迁移后生成环己酮（氧化环己烯经半频哪醇重排异构化为环己酮的合成用途）。

两者本质上都是 **1,2-迁移重排**，区别在于生成碳正离子的前体不同。

## 知识点映射

- [[1,2-迁移与重排]]
- [[Pinacol重排]]