---
title: Swern氧化
aliases: [Swern Oxidation, 斯文氧化, DMSO氧化]
type: 知识点
template_version: v1.3
subject: 有机化学
module: 有机化学
submodule: 具体反应
syllabus_stage: 基础
parent_overview: 中国化学奥林匹克基本要求-总览
parent_module: 基础要求-有机化学
syllabus_code: [40, 50]
syllabus_module: [有机化学]
tags: [化竞, 有机化学, 氧化反应, 醇氧化, 名称反应, 含硫化合物]
related: [有机氧化反应, Dess-Martin氧化, 醇的氧化, Corey-Chaykovsky反应, Pummerer重排]
prerequisite: [醇的氧化, 有机氧化反应, 含硫化合物]
problem_types: [题型-氧化反应试剂选择, 题型-机理推断]
difficulty: 3
importance: 4
status: 已填充
stage: published
sources: [Arrow Pushing in Inorganic Chemistry-总索引]
source_type: [书籍]
review_cycle: 30d
has_images: false
images_priority: 结构/机理 medium，纯公式 low
images_note: 
teaching_ready: false
source_notes: []
key_images: []
updated: 2026-05-25
---
# Swern 氧化
- 总览：[[中国化学奥林匹克基本要求-总览]]
- 所属模块：[[基础要求-有机化学]]
- 对应考纲条目：[[40-氧化还原反应]]、[[50-有机合成]]
- 外部资料：[[Arrow Pushing in Inorganic Chemistry-总索引]] §6.9

## 一、定义
**Swern 氧化**：使用 **DMSO + 草酰氯 (COCl)₂ + 三乙胺 (Et₃N)** 体系，在低温（−78 °C）下将伯醇/仲醇分别氧化为醛/酮的反应。

$$
\ce{R^1R^2CHOH ->[\text{(COCl)2, DMSO, -70 °C}][\text{Et3N}] R^1R^2C=O}
$$

- 伯醇 → 醛（**不会过氧化为羧酸**，是 Swern 的标志性优势）
- 仲醇 → 酮
- 副产物：CO、CO₂、Me₂S（DMS，气体逸出，恶臭）

## 二、考纲对应
- 对应考纲条目：[[40-氧化还原反应]]、[[50-有机合成]]
- 所属模块：[[基础要求-有机化学]]
- 本知识点在考纲中的作用：**温和氧化伯醇/仲醇至醛/酮**的代表方法，是合成题中替代 Cr(VI) 类强氧化剂的首选；其机理体现"硫叶立德 + 协同重排"的经典思路。

## 三、核心原理

### 3.1 反应总览

![[ArrowPushinginInorganicChemistry_231-336_images/96c52415bf4e0389fb91ecf0f0226eccade0a5c3b0aa2ef89cd73976ccd33769.jpg]]

> 注：DMSO 中的硫氧 S=O 起亲核作用，先被草酰氯活化为高活性硫鎓中间体。

### 3.2 第 1 步：DMSO 被草酰氯活化

DMSO 的氧（带形式负电荷）作为亲核体进攻 (COCl)₂ 的羰基碳：

$$
\ce{Me2S^+(O^-) + ClC(O)C(O)Cl -> Me2S^+-O-C(O)-C(O)Cl + Cl^-}
$$

中间体迅速分解，丢出 CO、CO₂、Cl⁻，生成 **氯代二甲基硫鎓阳离子** $\ce{Me2S^+-Cl}$：

$$
\ce{Me2S^+-O-C(O)C(O)Cl -> Me2S^+-Cl + CO + CO2 + Cl^-}
$$

> **关键**：草酰氯不参与最终的氧化电子转移，它只是把 DMSO 转换为高反应性的 S(IV) 鎓盐。这一步是放气的来源，也是反应必须低温的原因（防止失控）。

### 3.3 第 2 步：醇与硫鎓盐反应生成"烷氧基硫鎓"中间体

醇的羟基氧亲核进攻硫鎓中心，HCl 被 Et₃N 抓走：

$$
\ce{R^1R^2CHOH + Me2S^+-Cl ->[Et3N] R^1R^2CH-O-S^+(Me)2 + Cl^-(Et3NH^+)}
$$

这就是所有 DMSO 类氧化反应（Pfitzner-Moffatt、Kornblum、Albright-Goldman）共有的 **关键中间体** —— **烷氧基二甲基硫鎓** $\ce{ROS^+Me2}$。

### 3.4 第 3 步：Et₃N 拔取硫上甲基的氢（生成硫叶立德）

> **机理上的非平凡之处**：
> Et₃N 不能拔取烷氧基上的 α-H（pKa ~30+，太硬），
> 也不能直接在硫上发生消除；
> 实际上 Et₃N 选择拔取 **硫鎓正离子的 α-CH₃** 上的 H（pKa ≈ 16-17），生成 **硫叶立德**：

![[ArrowPushinginInorganicChemistry_231-336_images/b3b8ca7d3896c8e1aeee52c057affbbec14e2f52e8707e86542783575f865d61.jpg]]

$$
\ce{R^1R^2CH-O-S^+(Me)2 ->[Et3N] R^1R^2CH-O-S^+(Me)(=CH2) ->[\text{tautomer}] R^1R^2CH-O-S(Me)-CH2^-}
$$

### 3.5 第 4 步：[2,3]-σ 迁移（协同环状过渡态）

硫叶立德经过 **五元环过渡态** 协同重排，硫上的 CH₂⁻ 拔取烷氧 α-H、同时 C–O 断裂，一步生成醛/酮 + Me₂S：

![[ArrowPushinginInorganicChemistry_231-336_images/e29cd6134013ff39e2537727fc4dbaca407df0d5b5f5e0c2db20108416f5b164.jpg]]

$$
\ce{R^1R^2CH-O-S(Me)-CH2^- -> R^1R^2C=O + Me-S-CH3}
$$

> 这一步是 **协同的、不可逆的**，体现"叶立德介导的 syn 消除"思路，与 Wittig 反应的协同环化机理同源。

## 四、关键结论

- Swern 氧化属于 **DMSO 介导氧化** 大家族，本质是硫从 S(IV) 还原为 S(II)、醇 C-O 部分被氧化的内部氧化还原。
- **不会过氧化醛为酸**：因为反应一旦生成 C=O，就没有 α-OH 可继续氧化。
- 烷氧基硫鎓 $\ce{R-O-S^+Me2}$ 是 DMSO 类氧化反应（Swern、Pfitzner-Moffatt、Kornblum、Albright-Goldman、Corey-Kim）的共同中间体。
- **温度必须 < −60 °C**：否则烷氧基硫鎓会 Pummerer 重排或自发分解。

## 五、常见分类或情形

| 名称 | 活化剂 | 特点 |
|---|---|---|
| **Swern 氧化** | $(COCl)_2$（草酰氯） | 最常用，−78 °C |
| Pfitzner-Moffatt 氧化 | DCC（碳二亚胺） | 1963 年发现，最早的 DMSO 氧化 |
| Albright-Goldman 氧化 | $Ac_2O$（乙酸酐） | 工艺简便 |
| Albright-Onodera 氧化 | $P_2O_5$ | 大规模可用 |
| **Corey-Kim 氧化** | NCS + Me₂S | 不使用 DMSO，改用 DMS |
| **Kornblum 氧化** | DMSO + NaHCO₃，微波加热 | 用于卤代烷 → 醛 |
| Parikh-Doering 氧化 | $SO_3·py$ | 室温可行，被现代合成偏好 |

## 六、适用条件与限制

### 6.1 适用范围
- 一级醇（→ 醛）、二级醇（→ 酮）
- 兼容大多数官能团：烯、炔、酯、酰胺、醚、卤代物、缩醛
- 兼容大多数保护基（TBS、Bn、Bz）

### 6.2 限制
- **必须低温**：> −40 °C 时烷氧基硫鎓盐会分解为副产物（α-甲硫基醚等 Pummerer 产物）。
- **臭味问题**：DMS（二甲硫醚）极臭，需在通风橱中操作。
- 对易脱质子的醇（如 β-酮醇）可能产生消除副产物。
- 立体位阻太大的醇可能反应慢。

## 七、常见比较与易混点

### 7.1 Swern vs Dess-Martin (DMP)

| 对比项 | Swern | [[Dess-Martin氧化]] |
|---|---|---|
| 氧化中心 | S(IV) → S(II) | I(V) → I(III) |
| 温度 | −78 °C | 室温 |
| 操作 | 复杂、忌水 | 简单 |
| 副产物气味 | DMS（恶臭） | AcOH + 苯甲酸碘 |
| 对烯醇化倾向底物 | 偶尔有问题 | 通常更好 |
| 成本 | 试剂便宜 | DMP 较贵 |

### 7.2 Swern vs Jones（CrO₃）

| 对比项 | Swern | Jones |
|---|---|---|
| 伯醇产物 | 醛 | **羧酸**（过氧化） |
| 选择性 | 高 | 低 |
| 重金属污染 | 无 | 含铬，环保差 |

### 7.3 容易混淆的"DMSO 氧化"
- DMSO 本身不是氧化剂；
- **DMSO + 活化剂** 才是；
- 各种 DMSO 类氧化的差异只在第 1 步（活化剂不同），第 2-4 步完全相同。

## 八、与其他知识点的联系
- 前置知识：[[醇的氧化]]、[[有机氧化反应]]、[[亲核取代反应]]、[[含硫化合物]]
- 相关知识：[[Dess-Martin氧化]]（同样温和的现代醇氧化）、[[Corey-Chaykovsky反应]]（同源的硫叶立德）、[[Pummerer重排]]（α-乙酰氧基硫醚副反应路径）
- 应用知识：[[有机合成]]、[[保护基化学]]、[[多步合成路线]]

## 九、典型题型
- 题型-氧化反应试剂选择：根据底物选氧化剂
- 题型-机理推断：写出 Swern 氧化机理（4 步）
- 题型-合成设计：在多步路线中选择 Swern 替代 PCC

## 十、例题

### 例题 1：机理写出
**题目：** 写出 Swern 氧化将 1-苯乙醇氧化为苯乙酮的完整机理（4 步）。

**分析：**
- 第 1 步：DMSO + (COCl)₂ → $\ce{Me2S^+Cl}$ + CO + CO₂ + 2 Cl⁻
- 第 2 步：醇 + $\ce{Me2S^+Cl}$ → $\ce{PhCH(Me)-O-S^+Me2}$ + HCl
- 第 3 步：Et₃N 拔取 α-CH₃ 的 H → 硫叶立德 $\ce{PhCH(Me)-O-S(Me)CH2^-}$
- 第 4 步：五元环协同 [2,3] 重排 → PhCOMe + Me₂S

**反思：**
注意 Et₃N 拔的不是醇 α-H 而是硫上 CH₃。

### 例题 2：副反应
**题目：** Swern 氧化温度回升至 0 °C 后，常会得到 α-甲硫基醚副产物，请用机理说明。

**解答：** 烷氧基硫鎓 $\ce{R-O-S^+Me2}$ 在较高温度下不走叶立德路径，而走 **Pummerer 重排**：质子从 α-CH₃ 转出后形成硫鎓-α-碳正离子对，醇氧迁移给该碳，得到 α-MeS-O-R 类副产物。

## 十一、易错点
- ❌ 误以为 Et₃N 拔取烷氧基 α-H：实际拔取的是硫上 CH₃ 的 H。
- ❌ 误以为草酰氯本身是氧化剂：草酰氯只是活化剂，最终被还原成 CO 和 CO₂。
- ❌ 误以为产物是羧酸：Swern **不过氧化**，产物只到醛/酮。
- ❌ 写成"DMSO + Et₃N"反应：必须先有活化剂将 DMSO 激活。
- ❌ 忽略温度要求：> −40 °C 时几乎不能得到清洁产物。

## 十二、竞赛拓展
- **Pummerer 重排**（§6.9 习题 6.12）：α-乙酰氧基硫醚的形成；
- **Kornblum 氧化**：从烷基卤直接得到醛，不经醇中间体；
- **Corey-Kim 氧化**：硫醚 + NCS 替代 DMSO + 草酰氯（无气体放出）；
- **TPAP / NMO 氧化**：相同立场的"温和、不过氧化"现代方法；
- 与 [[β-硅基效应]] 联用：β-硅醇的 Swern 氧化常在合成中作为关键转化。

## 十三、外部资料出处
- [[Arrow Pushing in Inorganic Chemistry-总索引]] **§6.9 Swern and Related Oxidations**（pp. 240-247）
- 经典文献：Mancuso, A. J.; Huang, S.-L.; Swern, D. *J. Org. Chem.* **1978**, *43*, 2480.
- Tojo, G.; Fernández, M. *Oxidation of Alcohols to Aldehydes and Ketones*, Springer, 2006.

## 十四、待完善项
- [ ] 补充 Pummerer 重排单独成 KP（[[Pummerer重排]]）
- [ ] 补充各 DMSO 氧化方法的工艺规模对比表
- [ ] 补充竞赛真题中出现的 Swern 应用例

---

```dataview
TABLE file.name AS "文件名", year AS "年份", type AS "题型", difficulty AS "难度"
FROM "04-题库"
WHERE contains(knowledge_points, "Swern氧化")
SORT year DESC, difficulty ASC
```

## 十二、🎯 教学视角

## 十三、竞赛拓展

## 十四、外部资料出处

## 十五、待完善项
