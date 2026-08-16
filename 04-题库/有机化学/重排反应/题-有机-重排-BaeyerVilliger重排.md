---
title: "题-有机-重排-BaeyerVilliger重排"
type: 题目
submodule: 重排反应
exam_stage: 初赛
subject: 有机化学
difficulty: 3
teaching_level: 巩固
syllabus_codes: ["49"]
knowledge_points: ["BaeyerVilliger重排", "过氧酸氧化", "迁移能力"]
tags: [化竞, 题目, 有机化学]
updated: 2026-07-10
aliases: ["题-有机-重排-06"]
source: "Zchem基础有机化学"
module: 有机化学
status: 已填充
---
# Baeyer-Villiger氧化重排

## 题目

**(1)** 环戊酮与 mCPBA（间氯过氧苯甲酸）反应，写出产物结构。

**(2)** 写出 Baeyer-Villiger 重排的完整机理（从过氧酸进攻酮开始）。

**(3)** 下列酮用 mCPBA 氧化时，O 原子插入到哪个 C-C 键之间？给出迁移基团的优先顺序。

- **(a)** 甲基环己基酮（CH₃CO-C₆H₁₁）
- **(b)** 苯乙酮（CH₃CO-C₆H₅）


![[wagner-meerwein.png]]

## 参考答案

### (1) 环戊酮的 BV 氧化

环戊酮 + mCPBA → **δ-戊内酯**（五元环内酯，六元环含一个 O）

酮的 C=O 被"撑开"，插入一个 O 原子，环戊酮（五元环）→ δ-戊内酯（六元环内酯）。

### (2) BV 重排机理

**第一步**：过氧酸（mCPBA）的亲核氧进攻酮的 C=O → 形成四面体中间体（Criegee 加合物）

**第二步**：过氧键（O-O）异裂，同时一个基团迁移至 O → 形成酯/内酯

```
R-C(=O)-R' + mCPBA 
    → [R-C(OH)(OOC(=O)Ar)-R']（四面体中间体）
    → R-C(=O)-O-R' + mCPBA的羧酸部分
```

**关键**：迁移基团带着电子对迁移到缺电子的 O 上，与 SN1 中碳正离子重排类似。

### (3) 迁移基团选择

**迁移能力顺序**：

$$\text{叔烷基} > \text{仲烷基} \approx \text{苯基} > \text{伯烷基} > \text{甲基}$$

**更精确的顺序**：

$$p\text{-MeOC}_6\text{H}_4 > p\text{-MeC}_6\text{H}_4 > \text{C}_6\text{H}_5 > 3° > 2° > 1° > \text{CH}_3$$

**(a) 甲基环己基酮**：

环己基（仲烷基）的迁移能力 > 甲基 → O 插入在 **环己基与 C=O 之间**

产物：环己基-O-CO-CH₃（乙酸环己酯）

**(b) 苯乙酮**：

苯基的迁移能力 > 甲基 → O 插入在 **苯基与 C=O 之间**

产物：苯基-O-CO-CH₃（乙酸苯酯）

### BV 重排总结

| 要素 | 内容 |
|:---|:---|
| 试剂 | mCPBA 或其他过氧酸 |
| 底物 | 酮（R-CO-R'） |
| 产物 | 酯（R-CO-O-R'）或内酯（环酮） |
| 关键 | 迁移能力大的基团优先迁移到 O 上 |
| 应用 | 环酮 → 内酯（扩环一个原子） |

> 💡 **快速判断**：酮 → 酯，O 插入到迁移能力更强的基团一侧。

## 知识点映射

- BaeyerVilliger重排
- 过氧酸氧化
- 迁移能力