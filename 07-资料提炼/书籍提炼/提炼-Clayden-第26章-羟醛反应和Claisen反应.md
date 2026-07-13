---
title: 提炼-Clayden-第26章-羟醛反应和Claisen反应
aliases: [Clayden Ch26, 羟醛反应, Aldol反应, Claisen缩合, 烯醇盐, 烯醇硅醚, Dieckmann, Robinson增环, Knoevenagel, Reformatsky]
type: 资料提炼
subject: 有机化学
source: "Clayden, Organic Chemistry, 2nd Ed., Chapter 26"
source_path: clayden 有机化学/Clayden中文版_601-800.md
source_range: line 1183–2399
chapter: "26"
template_version: v1.3
extracted_date: 2026-07-09
status: 已提炼
tags: [化竞, 有机化学, 羟醛反应, Aldol, Claisen缩合, 烯醇盐, 烯醇硅醚, Dieckmann, Robinson增环, Knoevenagel, Reformatsky, Darzens, 碳上酰基化, Clayden]
handout_plan:
  - target: "有机化学基础"
    status: completed
    priority: P1
    source_sections: ["第26章 羟醛反应和Claisen反应（Aldol缩合、交叉缩合、不对称酮的控制、烯醇等价物、Claisen酯缩合、碳上酰基化、分子内反应、Robinson增环）"]
    estimated_pages: 28
knowledge_points: [烯醇, 亲核加成, Reformatsky反应, Michael加成, 羟醛反应, 交叉Aldol, 动力学烯醇盐, 热力学烯醇盐, Mukaiyama Aldol, Claisen缩合, Dieckmann缩合, Robinson增环, Knoevenagel反应, Mannich反应, Darzens反应, 烯醇盐, 烯醇硅醚, Wittig反应, 1,3-二羰基化合物, β-酮酯, 逆合成分析, 立体化学]
---

# Clayden 第26章：羟醛反应和Claisen反应 资料提炼

---

## 一、核心概念与定义

### 1.1 羟醛反应（Aldol Reaction）
- **定义**：烯醇或烯醇盐（亲核试剂）进攻另一分子醛或酮的羰基碳（亲电试剂），形成新的 C-C 键，生成 β-羟基羰基化合物（羟醛）的反应。
- **名称由来**：产物同时含醛基（aldehyde）和羟基（ol），故称 aldol。
- **本质**：[[烯醇]]盐对羰基的[[亲核加成]]，是有机合成中构建 C-C 键最重要的方法之一。
- **驱动力**：碱催化下，少量烯醇盐在未烯醇化的羰基化合物中形成并立即反应。

### 1.2 羟醛缩合（Aldol Condensation）
- **定义**：羟醛产物进一步脱水，生成 α,β-不饱和羰基化合物（烯基酮/烯基醛）。
- **条件**：碱催化下经 E1cB 机理脱水；酸催化下经 E1 机理脱水。
- **关键**：脱水使反应不可逆，是推动平衡正向进行的重要驱动力。

### 1.3 交叉缩合（Crossed Aldol Condensation）
- **定义**：两种不同羰基化合物之间的羟醛反应。
- **成功条件**（三个标准）：
  1. 仅一个组分可以烯醇化
  2. 仅一组可烯醇化的质子
  3. 另一个组分不可烯醇化，且比可烯醇化的组分更活泼（亲电性更强）
- **失败原因**：不满足上述条件时，得到多种产物的混合物。

### 1.4 Claisen 酯缩合（Claisen Ester Condensation）
- **定义**：酯的烯醇盐进攻另一分子酯的羰基碳，发生碳上酰基化，生成 β-酮酯的反应。
- **与 Aldol 的区别**：Aldol 中间体（烷氧基负离子）捕获质子得产物；Claisen 中间体有离去基团（EtO⁻），发生消除得 β-二羰基产物。
- **驱动力**：产物 β-酮酯具有酸性 α-H，被碱不可逆去质子形成稳定烯醇盐，拉动平衡。

---

## 二、碱催化与酸催化羟醛反应

### 2.1 碱催化 Aldol 反应
- **机理**（以乙醛 + NaOH 为例）：
  1. OH⁻ 夺取 α-H → 少量烯醇盐（平衡浓度）
  2. 烯醇盐进攻另一分子乙醛的 C=O → 烷氧基负离子
  3. 水质子化 → β-羟基醛（羟醛产物）
- **特点**：碱是催化剂（最后再生）；碱浓度需低，否则产物脱水。
- **脱水机理（E1cB）**：烯醇化 → OH⁻ 离去 → 共轭烯基酮。

### 2.2 酸催化 Aldol 反应
- **机理**：
  1. 酸催化烯醇化 → 烯醇
  2. 烯醇进攻质子化的醛（酸使亲电试剂更活泼）→ 羟醛
  3. 酸催化脱水（E1 机理）→ 烯基酮
- **特点**：通常直接得到脱水产物（烯基酮/烯基醛），而非羟醛。
- **适用**：对称环状酮的缩合（如环戊酮 → 双环烯基酮）。

### 2.3 碱催化 vs 酸催化对比
| 特征 | 碱催化 | 酸催化 |
|:---|:---|:---|
| 脱水机理 | E1cB | E1 |
| 产物 | 可能是羟醛或烯基酮 | 通常为烯基酮 |
| 条件强度 | 弱碱（NaOH, Ba(OH)₂） | 强酸、高温 |
| 适用底物 | 醛、酮 | 酮（尤其对称酮） |

---

## 三、不对称酮的控制——动力学与热力学烯醇盐

### 3.1 动力学烯醇盐（Kinetic Enolate）
- **制备**：LDA, THF, −78°C
- **选择少取代侧**（甲基侧）：质子酸性更强、可及性更好、LDA 空阻大。
- **特点**：快速生成，不可逆去质子；低温下稳定。
- **应用**：姜酚（gingerol）的合成——在甲基一侧生成烯醇盐，与戊醛反应。

### 3.2 热力学烯醇盐（Thermodynamic Enolate）
- **制备**：弱碱（如 NaOEt），较高温度，平衡条件
- **选择多取代侧**（更稳定烯醇）：取代基更多的双键更稳定。
- **应用**：1-苯基-2-丙酮在共轭一侧烯醇化（热力学压倒性有利）。

### 3.3 六甲基二硅基氨基锂（LiHMDS）
- 比 LDA 空阻更大、碱性稍弱，用于高选择性制备动力学烯醇盐。

---

## 四、特别烯醇等价物——控制交叉 Aldol 反应

### 4.1 烯醇锂（Lithium Enolates）
- **制备**：LDA, THF, −78°C，定量转化。
- **反应**：六元环过渡态（Zimmerman-Traxler 模型），锂与亲电试剂羰基氧配位。
- **优势**：即使亲电组分为可烯醇化的醛，也能高选择性反应。
- **限制**：醛的烯醇锂难以干净制备（自缩合竞争）。

### 4.2 烯醇硅醚（Silyl Enol Ethers）——Mukaiyama Aldol
- **制备**：弱碱（叔胺）+ Me₃SiCl，捕获平衡浓度的烯醇。
- **反应**：需 Lewis 酸（如 TiCl₄）催化，烯醇硅醚 + 醛 → 羟醛。
- **机理**：Lewis 酸活化醛 → 烯醇硅醚进攻 → Cl⁻ 去硅基 → 烷氧基钛水解。
- **优势**：醛做烯醇组分的最佳方法；无自缩合；区域选择性由烯醇硅醚制备决定。
- **应用**：manicone（蚂蚁信息素）的合成。

### 4.3 烯胺与烯胺盐（Enamines & Aza-Enolates）
- **烯胺**：醛/酮 + 仲胺 → 亚胺 → 烯胺。活性不足以做 Aldol，但用于酰基化。
- **烯胺盐**：醛 + 伯胺 → 亚胺 → LDA 锂化 → 烯胺锂。可与醛/酮干净反应。
- **优势**：可制备醛的烯醇等价物（醛的烯醇锂自缩合问题的解决方案）。

### 4.4 1,3-二羰基化合物（Knoevenagel 反应）
- **丙二酸酯/乙酰乙酸乙酯**：pKa ≈ 13，弱碱即可去质子。
- **Knoevenagel 反应**：1,3-二羰基 + 醛，胺/羧酸催化 → α,β-不饱和二羰基。
- **Doebner 改进**：用丙二酸代替丙二酸二乙酯，反应中脱羧。
- **选择性**：1,3-二羰基的烯醇盐更稳定，优先形成，不与自身反应。

### 4.5 Horner-Wadsworth-Emmons（HWE）反应
- **膦酸酯烯醇盐**：(RO)₂P(O)CH₂COR' 用碱去质子 → 烯醇盐。
- **与醛反应**：E 选择性，生成 α,β-不饱和羰基化合物。
- **优势**：比 Wittig 反应更稳定、反应性更高、E 选择性好。

### 4.6 [[Reformatsky反应]]（酯烯醇锌）
- **制备**：α-溴代酯 + Zn → 烯醇锌（Reformatsky 试剂）。
- **反应**：烯醇锌 + 醛/酮 → 羟醛（β-羟基酯）。
- **优势**：不与酯自缩合；锌只与醛/酮反应；不需要特别烯醇等价物。

### 4.7 特别烯醇等价物总结表
| 烯醇盐类别 | 醛 | 酮 | 酯 | 酸 |
|:---|:---|:---|:---|:---|
| 烯醇锂 | × | √ | √ | √ |
| 烯醇硅醚 | √ | √ | √ | √ |
| 烯胺 | √ | √ | × | × |
| 烯胺盐 | √ | √ | × | × |
| 烯醇锌 | × | × | √ | × |

---

## 五、Claisen 酯缩合与交叉 Claisen

### 5.1 经典 Claisen 酯缩合
- **乙酸乙酯自缩合**：EtO⁻/EtOH → 乙酰乙酸乙酯（β-酮酯）。
- **机理**：
  1. EtO⁻ 去质子 → 少量烯醇盐
  2. 烯醇盐进攻另一分子酯 → 四面体中间体
  3. EtO⁻ 离去 → β-酮酯
  4. EtO⁻ 不可逆去质子 → 稳定烯醇盐（驱动力）
  5. 酸后处理 → β-酮酯产物
- **关键**：EtO⁻ 足以去质子产物（pKa ≈ 10），但不足以完全去质子原料（pKa ≈ 25）。

### 5.2 不能烯醇化的活泼酯（交叉 Claisen 组分）
| 酯 | 特点 | 亲电性 |
|:---|:---|:---|
| 草酸二乙酯 | 1,2-二羰基，LUMO 更低 | 最强 |
| 甲酸酯 | 缺少 σ-共轭 | 强 |
| 碳酸二乙酯 | 两个氧共轭竞争 | 中 |
| 芳香酸酯 | 芳环共轭钝化 | 弱 |

### 5.3 酮与碳酸酯的酰基化
- **碳酸酯做酰基化试剂**：酮烯醇盐 + (EtO)₂C=O → β-酮酯。
- **区域选择性**：少取代烯醇盐优先形成（脱水不可逆步骤决定）。
- **应用**：Acifran（心血管药物）合成关键步。

### 5.4 碳上酰基化 vs 氧上酰基化
- **问题**：活泼烯醇盐（如烯醇锂）与活泼酰基化试剂（如酰氯）反应，倾向 O-酰基化。
- **解决方案**：
  - 活性差的烯醇等价物（烯胺/烯醇硅醚）+ 活泼酰基化试剂（酰氯）→ C-酰基化
  - 活泼烯醇（烯醇阴离子）+ 活性差的酰基化试剂（酯）→ C-酰基化
- **烯胺 + 酰氯**：N-酰基化可逆（不稳定盐），C-酰基化不可逆 → 最终 C-酰基化产物。

---

## 六、Mannich 反应与甲醛化学

### 6.1 Mannich 反应
- **组成**：可烯醇化的酮 + 仲胺 + 甲醛（水溶液）+ HCl 催化。
- **产物**：β-氨基酮（Mannich 碱）。
- **机理**：
  1. 胺 + 甲醛 → 亚胺盐（Eschenmoser 盐）
  2. 酮烯醇进攻亚胺盐 → Mannich 碱
- **应用**：
  - 制备氨基酮（药物中间体）
  - Mannich 碱 → MeI 烷基化 → 铵盐 → E1cB → 外-亚甲基化合物（Michael 受体前体）

### 6.2 甲醛的特殊性
- 太活泼，碱催化下多次反应 → 季戊四醇 C(CH₂OH)₄
- Cannizzaro 反应：无 α-H 醛在浓碱下歧化（自身氧化还原）

---

## 七、分子内 Aldol 与 Claisen（Dieckmann 缩合）

### 7.1 分子内 Aldol 反应
- **规则**：五元环和六元环产物优先形成；弱酸/弱碱平衡条件即可。
- **预测方法**：从产物结构逆推——双键位置 → 羟醛 → 烯醇化位点 → 亲电羰基。
- **1,6-环十二酮**：烯醇化后五元环关环，产率 ~96%。
- **2,8-壬二酮**：两种烯醇 → 六元环 vs 八元环 → 仅六元环产物（85%）。
- **Baldwin 规则**：五元/六元环有利；三/四元环及八元以上不利。

### 7.2 Dieckmann 缩合（分子内 Claisen）
- **定义**：二酯的分子内 Claisen 缩合，生成环状 β-酮酯。
- **与分子内 Aldol 类似**：五元/六元环产物优先；平衡条件下完成。
- **选择性**：多种烯醇盐可能 → 仅一种能形成稳定烯醇盐（两个羰基间有酸性 H）的产物被锁定。
- **应用**：环状 1,3-二羰基化合物的制备。

### 7.3 对称性诡计
- 不对称二酯的 Dieckmann 缩合可能给出两种 β-酮酯产物。
- 但如果两种产物水解/脱羧后给出相同酮，则混合物无碍。

---

## 八、Robinson 增环反应

### 8.1 反应概述
- **定义**：两步环合成法——[[Michael加成]] + 分子内 Aldol 缩合。
- **发明者**：Robert Robinson（1947 年诺贝尔化学奖）。
- **核心步骤**：
  1. 1,3-二酮烯醇盐对烯基酮的 Michael 加成 → 三酮
  2. 分子内 Aldol 缩合 → 稠环烯基酮

### 8.2 应用
- **甾体合成**：Robinson 合成了包含环 A 和 B 的双环二酮（甾类基本结构）。
- **脯氨酸催化**：Ch41 中讨论的不对称 Robinson 增环。

### 8.3 其他增环方法
- 乙酰乙酸乙酯 + 烯基酮 → 环己烯酮（简单实例）。
- 任何可烯醇化化合物 + 烯基酮 → 增环产物。

---

## 九、Darzens 反应与环氧制备

### 9.1 Darzens 反应
- **定义**：α-卤代羰基化合物在碱作用下与醛/酮反应，生成环氧（缩水甘油酯）。
- **机理**：
  1. α-卤代酯去质子 → 烯醇盐
  2. 烯醇盐对羰基加成 → 烷氧基负离子
  3. O-烷基化（分子内 SN2，卤素离去）→ 环氧
- **与 Aldol 的关系**：是 Aldol 反应的变体（O-烷基化代替 C-C 键形成后质子化）。
- **应用**：药物达卢生坦（darusentan）的合成。

---

## 十、竞赛题型与解题策略

### 10.1 产物预测型
- **碱催化 Aldol**：判断自缩合产物（β-羟基醛/酮）或脱水产物（烯基酮/烯基醛）。
- **Claisen 缩合**：判断 β-酮酯产物（两个酯 → β-酮酯）。
- **Dieckmann**：判断环状 β-酮酯（二酯 → 环）。

### 10.2 立体化学控制型
- **动力学 vs 热力学烯醇盐**：LDA/−78°C → 少取代侧；弱碱/室温 → 多取代侧。
- **Zimmerman-Traxler 六元环过渡态**：预测 anti/syn 选择性。

### 10.3 合成路线设计型
- **交叉 Aldol 设计**：确定谁做烯醇组分、谁做亲电组分；选择合适烯醇等价物。
- **Robinson 增环**：识别 Michael 受体和 Michael 供体 → 分子内 Aldol。
- **β-酮酯的制备**：自缩合 vs 碳酸酯酰基化 vs 烷基化路线的选择。

### 10.4 竞赛高频考点清单
1. Aldol 反应的机理与产物预测
2. 交叉 Aldol 的成功条件（三个标准）
3. 动力学烯醇盐 vs 热力学烯醇盐的制备与选择性
4. 烯醇硅醚 + Lewis 酸（Mukaiyama Aldol）
5. Claisen 酯缩合的机理与 β-酮酯的制备
6. Dieckmann 缩合的区域选择性（六元环优先）
7. Robinson 增环反应的两步法
8. Mannich 反应制备外-亚甲基化合物
9. Darzens 反应制备环氧
10. 烯胺/烯胺盐在酰基化中的应用

---

## 十一、重要图表与图片引用

### 羟醛反应基本机理
- ![[clayden 有机化学/Clayden中文版_601-800_images/f6fd96fe4f0ebfcc683b1e8ef28d53357466dec93291185f3a452a12edb64f4c.jpg]] —— 乙醛的烯醇化（line 1249）
- ![[clayden 有机化学/Clayden中文版_601-800_images/c550f973c2d794ad058eac0866fd115ccadd123f08d8f8ce964aa52432890a8f.jpg]] —— 碱催化 Aldol 反应机理（line 1255）
- ![[clayden 有机化学/Clayden中文版_601-800_images/40bdb5254af6e9966ea4f15d7f97b0f0e8f0adca4c4baf82715b3241584ff0c1.jpg]] —— 新 C-C 键的形成（line 1261）
- ![[clayden 有机化学/Clayden中文版_601-800_images/a211e9a4132596dac5db82faf4a3f8a867c4a62bed830c91ce5bc97a90c6218e.jpg]] —— 丙酮的 Aldol 反应（line 1265）
- ![[clayden 有机化学/Clayden中文版_601-800_images/bd5a7a136bff350a0e6be2db076f90a18a4218a7e793eadb06ab2362cdeb1c02.jpg]] —— 脱水生成烯基酮（line 1269）

### 酸催化与碱催化脱水
- ![[clayden 有机化学/Clayden中文版_601-800_images/fa9c1adbbd4979f3bd3b641bab42a7f7c9ffe7f3601546a501cc8761f1833843.jpg]] —— 酸催化烯醇化（line 1285）
- ![[clayden 有机化学/Clayden中文版_601-800_images/70f471b986ade710881cafc24b3390075b85062c86aae0311292f5e3e2e39da4.jpg]] —— 酸催化 Aldol 机理（line 1289）
- ![[clayden 有机化学/Clayden中文版_601-800_images/fc7aac3fd573e2eb3a5c38626ac496006ba848c6ae08d653ff1a0acf3f25a0c4.jpg]] —— 碱催化 E1cB 脱水（line 1303）

### 交叉 Aldol 与 Mannich 反应
- ![[clayden 有机化学/Clayden中文版_601-800_images/13d443b5031d84d3ba27e4f6bc5685055a33a84e939362e0a74acbd6f68c3c4e.jpg]] —— 成功的交叉 Aldol 示例（line 1361）
- ![[clayden 有机化学/Clayden中文版_601-800_images/f1e92083eb3eb8506f35f5e687797f2abacc11fd6aeb936065e7d5af8d98c62f.jpg]] —— Mannich 反应机理（line 1432）
- ![[clayden 有机化学/Clayden中文版_601-800_images/5f68ba49dd481427c776b4f58aed727da9c3098e354035ed30a79b23fd2a4812.jpg]] —— Mannich 碱的形成（line 1436）

### 烯醇锂与烯醇硅醚
- ![[clayden 有机化学/Clayden中文版_601-800_images/3bd8be3f2ff53536d9b2dc456f6115fda55763d0c8fa5499bdebce6771801688.jpg]] —— 烯醇锂的 Aldol 反应（六元环过渡态）（line 1552）
- ![[clayden 有机化学/Clayden中文版_601-800_images/b5fcd6ce8f920677339e1e2376a137271679de137e6036d7406853e3613148f5.jpg]] —— Mukaiyama Aldol（烯醇硅醚 + TiCl₄）（line 1600）
- ![[clayden 有机化学/Clayden中文版_601-800_images/b32ea3e6052ffa12da5094042c182fea4ed070bb433c9e0c06e28b682fa65eaf.jpg]] —— Mukaiyama Aldol 机理（line 1606）

### Claisen 酯缩合
- ![[clayden 有机化学/Clayden中文版_601-800_images/8abb0be13bdf8c88a347ab138ac23d505f4a24a7f9c4f2f09630b59cd44e391.jpg]] —— Aldol 与 Claisen 对比（line 1965）
- ![[clayden 有机化学/Clayden中文版_601-800_images/4b68f067d18205357ec5bea925782f9a7187e334e672992770e2da428c383425.jpg]] —— 烯醇盐进攻酯（line 1969）
- ![[clayden 有机化学/Clayden中文版_601-800_images/ce0a5cbdf755eea079682f05bf85a33df30a5a0a861a9192905f385d7def9fff.jpg]] —— Claisen 完整机理（line 1979）

### Dieckmann 与分子内反应
- ![[clayden 有机化学/Clayden中文版_601-800_images/3cbdda90d7ac5746ffd78f3bf62659099d8eb62811e1eaf062d2c8fa12551b1a.jpg]] —— 1,6-环十二酮的分子内 Aldol（line 1878）
- ![[clayden 有机化学/Clayden中文版_601-800_images/dc5ee17566eac46c893b02060dfb67b5e2b5145d2fead319874584218ed0889f.jpg]] —— 分子内 Claisen（Dieckmann）（line 2326）

### Robinson 增环
- ![[clayden 有机化学/Clayden中文版_601-800_images/2cdb31c922e0fb5667eae80800467dc4c4f2d318ef0c5c7e7b026773e6707de4.jpg]] —— Robinson 增环反应概述（line 1926）
- ![[clayden 有机化学/Clayden中文版_601-800_images/cc8c24ca980e44958d5f5f34318177b849b96b08b0e405eaeebd99ce4c9adbe9.jpg]] —— Robinson 增环的 Michael 加成（line 1930）

### Knoevenagel 与特殊烯醇等价物
- ![[clayden 有机化学/Clayden中文版_601-800_images/88c8d8e4dbcd5bd2dace30505a422e5d2948ecc3b558111bff8edc292ceb9943.jpg]] —— 1,3-二羰基化合物（line 1658）
- ![[clayden 有机化学/Clayden中文版_601-800_images/027ef952f1e2b42fb7b536e4a149b7edac0f3b8fb0bf85e0ff62ecf2dde8e9f1.jpg]] —— Knoevenagel 反应（line 1676）
- ![[clayden 有机化学/Clayden中文版_601-800_images/6788419ef3dd77a812c06746235695463edeee60a1f22acadbbd6432ceaa11fb.jpg]] —— 特别烯醇等价物列表（line 1528）

### 烯胺与酰基化
- ![[clayden 有机化学/Clayden中文版_601-800_images/cb6152b79d13105cada9b330b4fcd6af875529099e1062ee9773afca0f407daf.jpg]] —— 烯胺的酰基化（line 2256）
- ![[clayden 有机化学/Clayden中文版_601-800_images/e9227cf26687deb348cd9404fbd8557e28bc77aa1cbbb36cd2dcaa1aa31ec163.jpg]] —— 长叶烯合成中的烯胺酰基化（line 2276）

### Darzens 反应
- ![[clayden 有机化学/Clayden中文版_601-800_images/3a509a8e3cbc01810444cb8de21eb1c0df44f932be42de852d174181eb81ac3d.jpg]] —— Darzens 反应制备环氧（line 1955）

---

## 十二、与考纲的对应关系

| 考纲条目 | 对应内容 | Clayden 位置 |
|:---|:---|:---|
| [[羟醛反应]] | 碱/酸催化 Aldol，机理，脱水 | lines 1245–1310 |
| [[交叉Aldol]] | 成功条件，选择性控制 | lines 1357–1392 |
| [[动力学烯醇盐]] | LDA/−78°C，少取代侧 | lines 1798–1830 |
| [[热力学烯醇盐]] | 弱碱/室温，多取代侧 | lines 1858–1863 |
| [[Mukaiyama Aldol]] | 烯醇硅醚 + TiCl₄ | lines 1592–1618 |
| [[Claisen缩合]] | 酯缩合机理，β-酮酯制备 | lines 1961–2038 |
| [[Dieckmann缩合]] | 分子内 Claisen，环状 β-酮酯 | lines 2322–2367 |
| [[Robinson增环]] | Michael + 分子内 Aldol | lines 1920–1949 |
| [[Knoevenagel反应]] | 1,3-二羰基 + 醛 | lines 1654–1704 |
| [[Reformatsky反应]] | 酯烯醇锌 + 醛/酮 | lines 1726–1736 |
| [[Mannich反应]] | 酮 + 胺 + 甲醛 | lines 1397–1463 |
| [[Darzens反应]] | α-卤代酯 + 环氧制备 | lines 1951–1958 |

---

## 十三、与已有个体知识点的关联

- [[烯醇盐]] —— 本章核心亲核试剂，贯穿 Aldol 和 Claisen
- [[烯醇硅醚]] —— Mukaiyama Aldol 的关键试剂
- [[Wittig反应]] —— Ch27 详述，Ch26 中提及共轭 Wittig 试剂
- [[Michael加成]] —— Robinson 增环的第一步
- [[1,3-二羰基化合物]] —— Knoevenagel 反应的底物，Claisen 缩合的产物
- [[β-酮酯]] —— Claisen 缩合产物，可水解脱羧得酮
- [[逆合成分析]] —— Ch28 将用 Aldol/Claisen 切断讨论合成设计
- [[立体化学]] —— Zimmerman-Traxler 模型预测 anti/syn 选择性