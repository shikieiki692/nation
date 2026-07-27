---
title: "题-492-Clayden-Ch34-P4-分子间+分子内DA区域立体选择性"
type: 题目
submodule: 环加成反应
exam_stage: 初赛
subject: 有机化学
difficulty: 4
teaching_level: 竞赛拔高
syllabus_codes: ["21"]
knowledge_points: ["[[Diels-Alder反应]]"]
tags: [化竞, Clayden, 有机化学, 环加成反应]
updated: 2026-07-25
aliases: [Clayden-Ch34-P4]
source: Clayden Organic Chemistry 2nd Ed. Chapter 34 Problem 4
cross_references: ["[[题-502-Clayden-Ch35-P2-Claisen-3,3-σ迁移入门]]", "[[题-501-Clayden-Ch35-P1-Nazarov关环+Grignard和cuprate步骤]]"]
module: 有机化学
status: 已填充
---
# 题-492: 分子间+分子内DA区域/立体选择性

## 题目

Explain the formation of single adducts in these reactions.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/7d7297687ec32f0a6197b06ac01948dad5094152dbcee699323f768e3bb3b4bf.jpg]]

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/b56b524e7ac83f3a6c9c387fa97952ce6398ff3cc6b2dd0dd0ccb7b7d0671dae.jpg]]

**原文题目**：Explain the formation of single adducts in these reactions.

## 参考答案

**Answer (English)**:

**Reaction 1 (intermolecular)**: The stereochemistry is straightforward: it gives the endo product.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/1bc31c30acfb701ff1c3048779b67a32878156dbf08fffcacccf575e7ec09340.jpg]]

These are early steps in Corey's synthesis of the plant hormone gibberellic acid (E. J. Corey et al., J. Am. Chem. Soc., 1978, 100, 8031).

The regiochemistry is not quite so simple. The diene has the larger HOMO coefficient at the top end as drawn, so we must deduce that the largest LUMO coefficient in the unsymmetrical quinone is at the top left as drawn. This would result from the electron-donating MeO group making the top carbonyl group and the right-hand alkene less electrophilic, while the bottom carbonyl activates the top end of the left-hand alkene. Or, if you use the mnemonic, this is an 'ortho' product.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/1b4a4f962c3e9826ca0980e490aba1be0165973c7fb4646bc3810ac2ca718d62.jpg]]

**Reaction 2 (intramolecular)**: The second example is intramolecular so the regiochemistry is determined by that alone: the ester linkage between the diene and the dienophile is too short for any variation. This same link ('tether') also forces the dienophile to approach the diene from below. All that remains is the endo/exo question and the diagram shows that the product is endo with the carbonyl group tucked under the back of the diene.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/dbc0357f610e081aad837563bf37e917e5c58b2091f07af987ed534503defced.jpg]]

**中文解析**：

**反应1（分子间DA）**：
1. **区域选择性**：不对称醌作为亲二烯体，其LUMO系数分布不均——MeO基团供电子使上方羰基和右侧烯烃的亲电性降低，而下方羰基活化了左侧烯烃的上端
2. **"ortho"规则**：二烯体HOMO系数较大的一端与亲二烯体LUMO系数较大的一端相连 → "ortho"产物
3. **立体选择性**：endo产物为主（酯基藏在二烯体下方）

**反应2（分子内DA）**：
1. **区域选择性**：分子内反应中，酯键（tether）连接二烯体和亲二烯体，长度太短无法改变连接方式 → 区域选择性由tether决定
2. **面选择性**：tether迫使亲二烯体只能从二烯体下方接近
3. **endo/exo**：产物为endo构型，羰基藏在二烯体背面

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| Diels-Alder反应 | 分子间和分子内DA的区域/立体选择性 | 直接 |
| [[区域选择性]] | "ortho"规则和tether控制的区域化学 | 直接 |
| [[逆合成分析]] | 从产物反推DA反应的断键方式 | 直接 |
| [[endo/exo]] | endo选择性在分子间和分子内反应中的体现 | 直接 |
| [[前线轨道理论]] | HOMO/LUMO系数决定区域选择性 | 间接 |

## 解题思路

1. **读题定位**：两个反应都给出单一加合物 → 需要解释区域和立体选择性
2. **🔑 反应1（分子间）**：
   - 区域选择性：分析醌的LUMO系数分布（MeO供电子效应）
   - 立体选择性：endo规则
3. **🔑 反应2（分子内）**：
   - 区域选择性：tether决定（酯键长度固定）
   - 面选择性：tether迫使从下方接近
   - endo/exo：画出过渡态判断
4. **验证**：检查两种反应的产物是否都与题目一致

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 反应1区域选择性搞反 | 没有分析MeO的供电子效应 | MeO使上方羰基活性降低，左侧烯烃上端被活化 | 醌有两个烯烃，哪个更亲电？ |
| 认为分子内反应区域选择性可变 | 没有考虑tether限制 | 酯键太短，连接方式唯一 | 如果tether更长会怎样？ |
| 忽略面选择性 | 只关注endo/exo | tether还决定了亲二烯体从哪一面接近 | 为什么tether迫使从下方接近？ |
| 混淆"ortho"和"para" | 记忆错误 | "ortho"：相邻位连接；"para"：对位连接 | DA反应的"ortho/para"规则是什么？ |