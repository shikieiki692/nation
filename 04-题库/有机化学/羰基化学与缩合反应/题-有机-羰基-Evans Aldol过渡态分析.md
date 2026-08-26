---
title: "题-有机-羰基-Evans Aldol过渡态分析"
type: 题目
fidelity: 原书逐字
submodule: 羰基化学与缩合反应
exam_stage: 决赛
subject: 有机化学
difficulty: 5
teaching_level: 强化
syllabus_codes: ["49"]
knowledge_points: ["[[Evans Aldol]]", "[[Zimmerman-Traxler模型]]", "硼烯醇盐", "手性辅基"]
tags: [化竞, 题目, 有机化学, 决赛]
updated: 2026-07-10
aliases: ["题-有机-羰基-11"]
source: "Zchem有机反应合成与机理"
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 模块习题集
---
# Evans Aldol过渡态分析

## 题目

**(1)** Evans 手性辅基（oxazolidinone）控制的 Aldol 反应中，为什么使用 Bu₂BOTf/NEt₃ 生成 Z-硼烯醇盐？画出 Z-硼烯醇盐的结构。

**(2)** 画出 Z-硼烯醇盐与醛反应的四种可能的 Zimmerman-Traxler 过渡态（椅式），并判断哪种是主要产物。解释位阻和偶极效应如何共同决定选择性。

**(3)** Evans 辅基的三种裂解方法分别得到什么产物？写出每种方法的试剂和条件。

## 参考答案

### (1) Z-硼烯醇盐的形成

Bu₂BOTf（二丁基三氟甲磺酸硼）与酰胺的烯醇化：

```
Evans辅基-CO-CH₂-R + Bu₂BOTf + NEt₃ → Evans辅基-C(O-BBu₂)=CH-R (Z-烯醇盐)
```

**为什么是Z构型**：
- 硼（B）与酰胺的羰基氧配位 → 形成五元环螯合
- 螯合锁定烯醇盐为 **Z-构型**（O-B 键和烯烃在同一侧）
- NEt₃ 夺取 α-H → 烯醇化完成

Z-硼烯醇盐结构：
```
    O---B(Bu)₂
    |        |
Evans辅基-C=CHR
         Z-构型
```

### (2) Zimmerman-Traxler 四种过渡态

Z-硼烯醇盐 + R'CHO 的椅式过渡态：

**过渡态 A（主要产物）**：
- 醛的 R' 基团处于 **equatorial** 位置
- 烯醇盐的取代基也处于 equatorial
- **位阻最小** → 主产物

**过渡态 B**：
- 醛的 R' 处于 equatorial
- 但烯醇盐取代基处于 axial
- 位阻中等

**过渡态 C**：
- 醛的 R' 处于 **axial** 位置 → 1,3-双轴相互作用
- 位阻大 → 少量

**过渡态 D**：
- 醛的 R' 处于 axial
- 烯醇盐取代基也处于 axial
- **位阻最大** → 极少量

**决定因素**：
1. **位阻**：R' 基团优先 equatorial（A/B > C/D）
2. **偶极**：Z-烯醇盐的偶极矩方向使过渡态 A 的偶极最小化

**主要产物**：过渡态 A → **anti-aldol 产物**（syn/anti 定义取决于具体底物）

### (3) Evans辅基的三种裂解方法

| 方法 | 试剂 | 产物 | 条件 |
|:---|:---|:---|:---|
| **LiOH/H₂O₂** | LiOH + H₂O₂ | **羧酸** | 0°C, THF/H₂O |
| **LiAlH₄** | LiAlH₄ | **伯醇** | 回流, THF |
| **Weinreb胺** | Me(OMe)NH·HCl + AlMe₃ | **Weinreb酰胺** → 酮 | 室温 |

**选择依据**：
- 需要酸 → LiOH/H₂O₂（水解）
- 需要醇 → LiAlH₄（还原）
- 需要酮 → 先转Weinreb酰胺，再加Grignard

### Evans Aldol总结

| 要素 | 内容 |
|:---|:---|
| 手性辅基 | Evans oxazolidinone |
| 烯醇化试剂 | Bu₂BOTf / NEt₃ |
| 烯醇盐构型 | Z-硼烯醇盐 |
| 过渡态 | 椅式 Zimmerman-Traxler |
| 选择性来源 | 位阻 + 偶极最小化 |
| 辅基裂解 | LiOH/H₂O₂ → 酸；LiAlH₄ → 醇 |

## 知识点映射

- Evans Aldol
- [[Zimmerman-Traxler模型]]
- 硼烯醇盐
- 手性辅基