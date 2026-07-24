---
title: Clemmensen还原
aliases: [Clemmensen Reduction]
type: 知识点
subject: 有机化学
module: 有机化学
submodule: 氧化与还原
tags: [化竞, 有机化学, 还原反应, 羰基]
related: [Wolff-Kishner还原, 有机还原反应, 醛酮]
status: 已填充
stage: published
importance: 2
difficulty: 1
updated: 2026-07-23
syllabus_code: [40]
template_version: v1.3
source_extracts:
  - source_file: "[[07-资料提炼/书籍提炼/提炼-Clayden-第23章-化学选择性和保护基]]"
    asset_id: "Clayden-第23章-化学选择性和保护基"
    asset_type: "书籍提炼"
    asset_summary: "Clemmensen还原相关内容"
  - source_file: "[[07-资料提炼/书籍提炼/提炼-上海中学竞赛课程-第四分册-芳香烃]]"
    asset_id: "上海中学竞赛课程-第四分册-芳香烃"
    asset_type: "书籍提炼"
    asset_summary: "Clemmensen还原相关内容"
---

# Clemmensen还原

## 一、定位

Clemmensen 还原用于把醛、酮在强酸性条件下还原为亚甲基，常与 [[Wolff-Kishner还原]] 形成“酸性条件 vs 碱性条件”对比。

## 二、学习重点
- 适用底物通常是醛、酮
- 条件以 Zn(Hg) / 浓盐酸为代表
- 选条件时要先看底物是否耐酸

## 三、关联页
- [[有机还原反应]]
- [[Wolff-Kishner还原]]

## 四、核心原理

### 4.1 反应条件与机理

**标准条件**：Zn(Hg) + 浓HCl，回流加热（~100 °C）。

**底物范围**：醛、酮的羰基（C=O）被还原为亚甲基（CH₂）。对酯、酰胺等其他羰基化合物效果差。

**反应机理**：表面金属还原机制。Zn(Hg)在浓HCl中通过锌汞齐表面进行电子转移，将羰基逐步还原。属于异相催化过程，而非自由基机理。关键特征是锌表面吸附底物后发生连续的两电子还原（ECE过程：电子转移–质子化–电子转移–质子化），最终脱氧生成亚甲基。

### 4.2 与Wolff-Kishner还原对比

| 特征 | Clemmensen | Wolff-Kishner |
|---|---|---|
| 条件 | Zn(Hg)/浓HCl（酸性） | NH₂NH₂/KOH/乙二醇（碱性） |
| 温度 | 回流（~100 °C） | 高温（~200 °C） |
| 适用 | 耐酸底物 | 耐碱底物 |
| 不适用 | 含缩醛保护基 | 含酸敏感基团 |

## 五、与其他知识点的关系

1. **[[Wolff-Kishner还原]]**：两种经典的C=O → CH₂还原方法，选择依据是底物在酸/碱中的稳定性，是化竞中必考的对比点。
2. **[[有机还原反应]]**：Clemmensen还原是有机还原反应的重要类型之一，与催化氢化（H₂/Pd）、LiAlH₄还原等共同构成羰基还原的工具箱。
3. **保护基策略（缩醛保护）**：缩醛在碱性条件下稳定但在酸性条件下水解，因此若分子中含缩醛保护基，必须选Wolff-Kishner而非Clemmensen。理解保护基的酸碱稳定性是正确选择还原方法的前提。

## 六、典型题型

**类型一：条件选择题**

> 已知底物结构，判断应选用Clemmensen还原还是Wolff-Kishner还原。
>
> **解题思路**：检查底物中是否存在酸敏感基团（缩醛、缩酮、酯基水解位点）或碱敏感基团（酯、酰胺、Michael受体），据此选择酸性或碱性还原条件。

**类型二：合成路线题**

> 从指定原料出发，设计含Clemmensen还原步骤的合成路线。
>
> **解题思路**：先通过Friedel-Crafts酰基化引入酮羰基，再用Clemmensen还原（Zn(Hg)/浓HCl）脱氧得亚甲基，从而实现苯环上烷基的间接引入（避免直接烷基化的重排问题）。

## 🎯 教学视角

### 学习路径建议

Clemmensen还原应在掌握醛酮化学和还原反应之后学习。建议与Wolff-Kishner还原对比学习（酸性条件vs碱性条件），理解两种方法的适用范围和选择依据，最后掌握在合成中的应用场景。

### 学生易踩的认知误区

| 误区 | 正确理解 |
|:---|:---|
| 认为Clemmensen还原可以还原所有羰基 | Clemmensen还原主要适用于醛酮，对酯、酰胺等羰基化合物效果差 |
| 混淆Clemmensen和Wolff-Kishner的条件 | Clemmensen：Zn(Hg)/浓盐酸（酸性）；Wolff-Kishner：NH₂NH₂/KOH/乙二醇（碱性） |
| 忽略底物的酸敏感性 | 对酸敏感的底物（如含缩醛保护基）不能用Clemmensen还原，应选Wolff-Kishner |

### 入门级例题

**题目**：如何将苯乙酮转化为乙苯？

**解答**：苯乙酮（PhCOCH₃）经Clemmensen还原（Zn(Hg)/浓盐酸，回流）→ 乙苯（PhCH₂CH₃）。羰基（C=O）被还原为亚甲基（CH₂）。

### 与现实世界的联系

- **药物合成**：Clemmensen还原用于将芳香酮还原为烷基苯，是合成抗组胺药等药物的步骤之一
- **香料工业**：某些香料分子中的羰基需要还原为亚甲基以调节气味特性
- **天然产物合成**：在全合成中，Clemmensen还原用于选择性还原酮羰基而不影响其他官能团

