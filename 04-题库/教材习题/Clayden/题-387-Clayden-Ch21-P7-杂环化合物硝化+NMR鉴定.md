---
title: 题-387-Clayden-Ch21-P7-杂环化合物硝化+NMR鉴定
type: 题目
fidelity: 原书逐字
submodule: 芳香亲电取代
exam_stage: 初赛
source_subject: 有机化学
difficulty: 4
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[芳香亲电取代]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch21-P7]
source: Clayden Organic Chemistry 2nd Ed. Chapter 21 Problem 7
cross_references: ["[[题-336-Clayden-Ch7-P1-共轭判断和弯曲箭头表示]]", "[[题-524-Clayden-Ch41-P1-循环中间体创建新手性中心]]", "[[题-525-Clayden-Ch41-P2-拆分法规划不对称合成入门]]", "[[题-337-Clayden-Ch7-P2-复杂化合物中共轭体系范围]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 模块习题集
---
# 题-387: 杂环化合物硝化+NMR鉴定

## 题目

**【中文】**用HNO₃/H₂SO₄对该杂环化合物硝化，得到单一硝化产物，其1H NMR谱如所示。建议形成了哪种产物以及为什么。

**【原文】**
Nitration of this heterocyclic compound with the usual HNO₃/H₂SO₄ mixture gives a single nitration product with the ¹H NMR spectrum shown below. Suggest which product is formed and why.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/4d8c1ce10957b7b854679ce4ff81456d463cb525a4af0c6485ee1d206e0d7509.jpg]]

δH: 3.04 (2H, t, J 7 Hz), 3.68 (2H, t, J 7 Hz), 6.45 (1H, d, J 8 Hz), 7.28 (1H, broad s), 7.81 (1H, d, J 1 Hz), 7.90 (1H, dd, J 8, 1 Hz)

## 参考答案

**Answer (English)**: The two 2H triplets and the broad NH signal show that the heterocyclic ring is intact. One nitro group has been added to the benzene ring. The proton at 7.81 with only one small (meta) coupling must be between the nitro group and the other ring and is marked on the two possible structures. You could argue that NH is ortho, para-directing and so the second structure is more likely. But this is a risky argument as the reaction is carried out in strong acid solution where the nitrogen will mostly be protonated. It is safer to use the predicted δH from tables.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/fe4d6ca3ea01c52abf76fc48d52a099b2bc7452f8330525f5c9736ebbf025928.jpg]]

**中文解析**：

本题考察杂环化合物的亲电取代位置和NMR分析的综合应用。

关键要点：
1. **杂环完整性**：两个2H三重峰（δ 3.04和3.68）和宽NH信号表明杂环（四氢异喹啉骨架）保持完整
2. **单硝基取代**：苯环上加了一个NO₂。δ 7.81的H只有一个小偶合（1 Hz，间位偶合），表明它位于NO₂和杂环之间
3. **两种可能结构**：硝化可能发生在苯环的不同位置
4. **NH的定位效应**：虽然NH可能直接定位，但在强酸中N会被质子化，使定位效应复杂化
5. **δH预测方法**：更可靠的方法是用化学位移表预测各H的δ值，与实测值比较

> **核心概念**：在强酸条件下，胺的质子化会改变其电子效应，因此不能简单地将-NH₂的定位规则直接应用于-NH₃⁺。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[芳香亲电取代]] | 杂环化合物的硝化位置选择性 | 直接 |
| [[NMR谱学]] | 利用化学位移和偶合常数推断取代位置 | 直接 |
| [[杂环化合物]] | 含氮杂环的电子效应与反应性 | 间接 |
| [[定位效应]] | 酸性条件下胺的质子化对定位的影响 | 间接 |

## 解题思路

1. **读题定位**：题目给出NMR数据，要求推断杂环化合物的硝化产物结构
2. **🔑 关键转换**：分析NMR→确认杂环完整→用δ 7.81的H定位NO₂→比较两种可能结构→用δH预测表选择更合理的结构
3. **验证**：检查预测的δH值与实测值是否一致；检查偶合常数是否匹配

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 简单用NH的定位效应判断 | 未考虑酸性条件下N被质子化 | 强酸中N大部分被质子化为NH⁺，不再是给电子基 | 质子化后-NH₃⁺是什么类型的定位基？ |
| 忽略δH预测方法 | 不知道如何用化学位移表验证结构 | 应使用取代基效应表预测各H的化学位移，与实测值比较 | 芳香H的化学位移受哪些因素影响？ |
| 未分析偶合常数 | 只看化学位移不看偶合模式 | 小偶合（1 Hz）=间位偶合，大偶合（8 Hz）=邻位偶合 | 如何区分邻位、间位和对位取代？ |