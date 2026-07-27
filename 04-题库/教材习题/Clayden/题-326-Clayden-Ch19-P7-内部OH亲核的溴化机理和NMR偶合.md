---
title: 题-326-Clayden-Ch19-P7-内部OH亲核的溴化机理和NMR偶合
type: 题目
submodule: 烯烃的亲电加成
exam_stage: 初赛
subject: 有机化学
difficulty: 4
teaching_level: 拓展
syllabus_codes: ["2.3", "4.1"]
knowledge_points: ["[[溴鎓离子]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch19-P7]
source: Clayden Organic Chemistry 2nd Ed. Chapter 19 Problem 7
cross_references: ["[[题-322-Clayden-Ch19-P3-溴水对三个烯烃加成产物]]", "[[题-396-Clayden-Ch22-P6-SNAr机理和选择性]]", "[[题-336-Clayden-Ch7-P1-共轭判断和弯曲箭头表示]]"]
module: 有机化学
status: 已填充
---
# 题-326: 内部OH亲核的溴化机理和NMR偶合

## 题目

When an alkene containing an internal hydroxyl group is treated with Br₂, an intramolecular reaction occurs. Propose a mechanism. The product's NMR spectrum shows large J coupling constants. Explain what this tells you about the conformation and identify the positions of Br and Me groups.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/a5aa6fa8ff71829af9864d7d7edf6c874027c0066bf6c878163b9fd9611f3abb.jpg]]

**原文题目**：

当含有内部羟基的烯烃用 Br₂ 处理时，发生分子内反应。提出机理。产物的 NMR 谱图显示较大的 J 偶合常数，解释这告诉你关于构象的什么信息，并确定 Br 和 Me 的位置。

## 参考答案

**Answer (English)**:

**Mechanism**: Br₂ approaches the double bond to form a **bromonium ion** intermediate. Instead of the external nucleophile (Br⁻) attacking, the **internal OH group** acts as the nucleophile and attacks the bromonium ion from the **more substituted carbon** (where the partial positive charge is larger). This intramolecular attack is faster than intermolecular attack due to the proximity effect (favourable entropy). The result is a cyclic ether (tetrahydrofuran or tetrahydropyran derivative) with the Br on the less substituted carbon — a bromo-ether.

**NMR interpretation**: Large J coupling constants (> 8–10 Hz) indicate **axial–axial** C–H coupling on a six-membered ring. This means the two coupled protons are both in axial positions (dihedral angle ≈ 180°, Karplus equation predicts maximum coupling).

This tells us:
- The ring is in a chair conformation.
- **Br and Me are both equatorial** — because the C–H bonds on the same carbons are axial (J is large for axial H coupling to adjacent axial H). If Br or Me were axial, the adjacent C–H would be equatorial, giving a small J value.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/a0c9292d64431b3d7c1f7059b7404c33aec5488b5c30001ac3529e5c06d36e1b.jpg]]

**中文解析**：

**机理**：Br₂ 与烯烃双键形成**溴鎓离子**中间体。此时分子内部的 OH 基团作为亲核试剂，从**取代程度更高的碳**一侧进攻溴鎓离子（部分正电荷更大的位置），发生**分子内开环**。分子内反应因距离优势（熵效应有利）比分子间反应更快，生成含氧杂环（四氢呋喃或四氢吡喃衍生物），Br 留在取代程度较低的碳上 → 溴代醚。

**NMR 偶合常数解读**：
- **大 J 值（> 8–10 Hz）**：表明两个 C-H 键处于**轴-轴**偶合关系（dihedral angle ≈ 180°，Karplus 方程预测最大偶合）。这说明环处于椅式构象，且偶合的两个质子都是轴向的。
- **推论**：既然相邻碳上的 C-H 是轴向的，那么 Br 和 Me 必须是**赤道位**的（因为同一碳上另一个键是赤道位）。若 Br 或 Me 为轴向，则相邻 C-H 将为赤道位，产生小 J 值。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[溴鎓离子]] | 分子内OH对溴鎓离子的亲核开环（分子内亲电加成） | 直接 |
| [[NMR谱学]] | Karplus方程：大J值→轴-轴偶合→赤道位取代基 | 直接 |
| [[亲电加成]] | 分子内vs分子间亲核试剂的竞争（熵效应） | 间接 |

## 解题思路

1. **读题定位**：内部OH+Br₂→分子内反应→需画机理+解读NMR偶合常数
2. **🔑 关键转换**：Br₂ → 溴鎓离子 → 内部OH进攻取代度高的碳（分子内环化）→ 溴代醚产物；NMR 大 J → 轴-轴 C-H → Br/Me 为赤道位
3. **验证**：检查环化是否经过溴鎓离子（非碳阳离子）；NMR 大 J 与椅式构象一致

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| OH进攻取代度低的碳 | 混淆了分子内和分子间反应的位点选择 | 溴鎓离子中部分正电荷集中在取代度高的碳→OH优先进攻 | 为什么部分正电荷偏向取代度高的碳？ |
| 大J值→赤道位质子 | Karplus方程的错误应用 | 大J→轴-轴偶合→质子为轴向→取代基为赤道位 | Karplus方程中偶合常数与二面角的关系？ |
| 忽略分子内vs分子间反应的速率差异 | 不理解邻近基团参与的熵优势 | 分子内反应因距离近（熵有利）远快于分子间反应 | 如果OH在分子另一端还能发生分子内反应吗？ |