---
title: "题-有机-SNE-二级卤代烷SN2vsE2竞争产物预测"
type: 题目
submodule: 亲核取代与消除反应
exam_stage: 初赛
subject: 有机化学
difficulty: 4
teaching_level: 强化
syllabus_codes: ["28"]
knowledge_points: ["[[SN2反应]]", "[[E2反应]]", "[[亲核取代]]", "[[消除反应]]"]
tags: [化竞, 题目, 有机化学, 第三轮]
updated: 2026-06-06
aliases: ["题-有机-SNE-02"]
source: "专题页提炼"
module: 有机化学
status: 已填充
---
# 二级卤代烷 SN2 vs E2 竞争产物预测

## 题目

2-溴丁烷（$\mathrm{CH_3CHBrCH_2CH_3}$）在下列三种不同条件下反应。对每种条件：
1. 判断 SN2 与 E2 哪个占主导；
2. 写出所有可能的主要有机产物（含立体化学和区域选择性信息）；
3. 若产物为混合物，估算各产物的比例并说明理由。

三种条件：
- **(A)** $\mathrm{NaSCH_3}$（硫醇钠）在 $\mathrm{CH_3OH}$ 中，$25^\circ\mathrm{C}$
- **(B)** $\mathrm{NaOC(CH_3)_3}$（叔丁醇钠）在 $\mathrm{(CH_3)_3COH}$ 中，回流
- **(C)** $\mathrm{NaOCH_3}$ 在 $\mathrm{CH_3OH}$ 中，$60^\circ\mathrm{C}$


![[sn2-reaction.svg]]

## 参考答案

### 关键分析框架

2-溴丁烷是**二级卤代烷**，处于 SN2/E2 的"灰色地带"——两种路径都可能发生。产物分布取决于：

1. **试剂的亲核性 vs 碱性**：S 亲核试剂 $\gg$ O 亲核试剂；空间位阻大的碱 $\gg$ 空间位阻小的碱 更偏向消除。
2. **温度**：高温有利于 E2（熵增加）。
3. **E2 的区域选择性**：Saytzeff 规则（生成取代更多的烯烃）vs Hofmann 规则（大位阻碱生成取代少的烯烃）。

### 条件 A：$\mathrm{NaSCH_3}$ / $\mathrm{CH_3OH}$，25°C

**$\mathrm{CH_3S^-}$ 是极其优秀的亲核试剂**（S 的 3p 轨道与 C 的 2p 轨道重叠好，极化率高），同时碱性较弱（$\mathrm{CH_3SH}$ 的 $\mathrm{p}K_\mathrm{a} \approx 10.3$，而 $\mathrm{CH_3OH} \approx 15.5$）。

- SN2 极快，E2 缓慢。
- 低温抑制消除。

**判断：SN2 占绝对主导（>95%）。**

产物：$\mathrm{CH_3CH(SCH_3)CH_2CH_3}$（2-甲硫基丁烷），构型翻转（若底物为手性纯 R，产物为 S）。

### 条件 B：$\mathrm{NaOC(CH_3)_3}$ / $\mathrm{(CH_3)_3COH}$，回流

**$\mathrm{(CH_3)_3CO^-}$ 是大位阻强碱**，亲核取代因位阻极大而受阻。叔丁醇钾/钠是经典的**Hofmann 消除试剂**。

- 大位阻使 SN2 几乎不可能发生（过渡态中 C-OTs 太拥挤）。
- 回流高温强烈推动 E2。
- E2 的区域选择性：大位阻碱优先进攻**空间上最容易接近的 β-H**，即取代较少的 β-C 上的 H（Hofmann 取向），而非 Saytzeff 取向。

**判断：E2 占绝对主导（>99%）。**

2-溴丁烷有两个不同的 β-C：
- C1（$\mathrm{CH_3}$—）：1 个 β-H
- C3（$\mathrm{CH_2}$—末端）：2 个 β-H（Saytzeff 烯烃前体）

Saytzeff 产物：2-丁烯（$\mathrm{CH_3CH=CHCH_3}$），cis/trans 混合物。
Hofmann 产物：1-丁烯（$\mathrm{CH_2=CHCH_2CH_3}$）。

叔丁醇钾为 Hofmann 取向试剂，**1-丁烯 : 2-丁烯 ≈ 70 : 30**（典型值）。

### 条件 C：$\mathrm{NaOCH_3}$ / $\mathrm{CH_3OH}$，60°C

$\mathrm{CH_3O^-}$ 既是中等亲核试剂又是中等强碱，处于 SN2/E2 的竞争中间地带。60°C 的中等高温对消除有利但不极端。

- SN2 和 E2 都会发生。
- E2 的区域选择性：$\mathrm{CH_3O^-}$ 位阻不大，以 Saytzeff 取向为主（过渡态类似烯烃，取代更多的烯烃更稳定）。

**判断：SN2 与 E2 竞争，大致 SN2 : E2 ≈ 40 : 60（温度偏高，消除略占优）。**

产物混合物：
- SN2：$\mathrm{CH_3CH(OCH_3)CH_2CH_3}$（2-甲氧基丁烷），构型翻转。
- E2 Saytzeff 产物：2-丁烯（trans 为主，约 80% trans, 20% cis），约占消除产物的 80%。
- E2 Hofmann 产物：1-丁烯，约占消除产物的 20%。

### 比较总结表

| 条件 | 试剂特征 | 主导路径 | 取代/消除比 | 烯烃区域选择性 |
|:---|:---|:---|:---:|:---|
| A: $\mathrm{CH_3S^-}$, 25°C | 强亲核/弱碱 | **SN2** | >95:5 | — |
| B: $\mathrm{t-BuO^-}$, 回流 | 大位阻强碱/弱亲核 | **E2** | <1:99 | Hofmann (1-丁烯为主) |
| C: $\mathrm{CH_3O^-}$, 60°C | 中等亲核/中等碱 | **E2 略占优** | ≈40:60 | Saytzeff (2-丁烯为主) |

### 核心规律

对于二级卤代烷的 SN2/E2 竞争：
- **硫亲核试剂**（$\mathrm{RS^-}$、$\mathrm{I^-}$）→ SN2 主导。
- **大位阻强碱**（$\mathrm{t-BuO^-}$、$\mathrm{LDA}$）→ E2 主导 + Hofmann 取向。
- **中等碱/亲核试剂**（$\mathrm{RO^-}$、$\mathrm{OH^-}$）→ 竞争，高温偏消除，区域选择性偏 Saytzeff。

## 知识点映射

- SN2反应
- E2反应
- [[亲核取代]]
- [[消除反应]]