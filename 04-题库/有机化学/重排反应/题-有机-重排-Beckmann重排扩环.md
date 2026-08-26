---
title: "题-有机-重排-Beckmann重排扩环"
type: 题目
fidelity: 原书逐字
submodule: 重排反应
exam_stage: 初赛
subject: 有机化学
difficulty: 3
teaching_level: 巩固
syllabus_codes: ["49"]
knowledge_points: ["[[Beckmann重排]]", "酮肟", "[[酰胺合成]]"]
tags: [化竞, 题目, 有机化学]
updated: 2026-07-10
aliases: ["题-有机-重排-07"]
source: "Zchem基础有机化学"
module: 有机化学
status: 已填充
---
# Beckmann重排扩环反应

## 题目

**(1)** 环己酮肟在酸性条件（H₂SO₄ 或 PCl₅）下发生 Beckmann 重排，写出产物结构。

**(2)** 写出 Beckmann 重排的机理（从酮肟的活化开始）。

**(3)** 己内酰胺（caprolactam）是合成尼龙-6 的重要单体。如何用 Beckmann 重排从环己酮出发合成己内酰胺？


![[beckmann-mechanism.png]]

## 参考答案

### (1) 环己酮肟的 Beckmann 重排

环己酮肟 → 酸性条件 → **ε-己内酰胺**（七元环内酰胺）

```
环己酮肟（C=N-OH）
    → 酸性活化（OH 变成好的离去基团）
    → 1,2-迁移（反式基团迁移到 N 上）
    → 七元环内酰胺（己内酰胺）
```

**扩环原理**：环己酮肟的 C=N-OH，N 上的 OH 被活化后离去，同时反式位置的 C-C 键断裂并迁移到 N 上，环从六元扩为七元。

### (2) Beckmann 重排机理

**第一步：活化 OH**
$$\text{R-C(=NOH)-R'} \xrightarrow{H^+} \text{R-C(=NOH}_2^+\text{)-R'}$$

OH 质子化 → 变成好的离去基团（H₂O）

**第二步：离去 + 迁移（协同）**

水分子离去的同时，**反式位置的基团**迁移到 N 上：

```
    OH                O
    ‖                 ‖
R-C=N-R'  →  R-C-N-R'
               ‖
               O
```

迁移规则：**与 OH 反式的基团优先迁移**（anti-periplanar 要求）

**第三步：水解**
$$\text{R-C(=O)-NHR'} \xrightarrow{H_2O} \text{R-COOH + H_2N-R'}$$

N-取代酰胺水解 → 羧酸 + 胺

### (3) 己内酰胺的合成

```
环己酮 → 环己酮肟（NH₂OH 处理）
    → ε-己内酰胺（Beckmann 重排，H₂SO₄ 催化）
    → 聚合 → 尼龙-6
```

**工业条件**：
- 底物：环己酮肟
- 催化剂：发烟 H₂SO₄（或 B₂O₃/Al₂O₃ 固体酸）
- 产物：ε-己内酰胺（七元环内酰胺）
- 产率：>95%

这是**尼龙-6 的工业合成路线**，年产量数百万吨。

### Beckmann 重排总结

| 要素 | 内容 |
|:---|:---|
| 底物 | 酮肟（R₂C=NOH） |
| 条件 | 酸性（H₂SO₄、PCl₅ 等） |
| 产物 | N-取代酰胺（迁移基团连接到 N 上） |
| 迁移规则 | **反式迁移**（与 OH 反式的基团迁移） |
| 应用 | 环酮肟 → 内酰胺（扩环）；工业合成尼龙-6 单体 |

> 💡 **与 Baeyer-Villiger 的对比**：
> - BV：酮 → 酯（O 插入 C-C 之间）→ 扩环一个原子
> - Beckmann：酮肟 → 酰胺（C-C 断裂到 N 上）→ 扩环一个原子

## 知识点映射

- [[Beckmann重排]]
- 酮肟
- [[酰胺合成]]