---
title: 题-390-Clayden-Ch21-P10-考虑定位效应的合成路线选择
type: 题目
fidelity: 原书逐字
submodule: 芳香亲电取代
exam_stage: 初赛
source_subject: 有机化学
difficulty: 3
question_type: [合成]
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[芳香亲电取代反应]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch21-P10]
source: Clayden Organic Chemistry 2nd Ed. Chapter 21 Problem 10
cross_references: ["[[题-525-Clayden-Ch41-P2-拆分法规划不对称合成入门]]", "[[题-336-Clayden-Ch7-P1-共轭判断和弯曲箭头表示]]", "[[题-337-Clayden-Ch7-P2-复杂化合物中共轭体系范围]]", "[[题-524-Clayden-Ch41-P1-循环中间体创建新手性中心]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 章节练习
source_category: 教材课后习题
source_grade: B
---
# 题-390: 考虑定位效应的合成路线选择

## 题目

How would you make each of the following compounds from benzene?

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/feca147ce9cea6c9773051efcc379bcb927fdee9f7a91b13de821871de45290f.jpg]]

**原文题目**：你如何从苯合成下列每种化合物？

## 参考答案

**Answer (English)**: The first compound has a ketone substituent, which is electron-withdrawing and therefore meta-directing, and an amino group, which is electron-donating and therefore ortho,para-directing. Aromatic amino groups are best made by reduction of nitro groups, which are also meta directing, so there are two possibilities. We can either start with a Friedel-Crafts acylation of benzene to give the ketone, which we can nitrate in the meta position and then reduce, or we can start by nitrating benzene, then do the acylation and then reduce. Either is a reasonable solution.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/887db45757386e56643ccf9ee76f235fbb3db507979c4ece044b29cf32ed0b40.jpg]]

The second compound has a bromo substituent, which is ortho, para-directing, and a meta-directing nitro group. We need the para relationship, so we must put the bromine in first, then nitrate.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/79c277b5f08cbdff63d909b71e15c15f8605172144b4a8ed53c6b84885ad3c8a.jpg]]

Finally, a compound with two para-directors arranged meta to one another. This may seem a problem, but we must introduce the alkyl group by Friedel-Crafts acylation and reduction, since primary alkyl groups cannot be introduced by Friedel-Crafts alkylation. The acyl group will be meta directing, so that solves both problems. First acylate, then brominate, then reduce.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/f6c6a8ad763687f5bcacd650dbdc14834ec3a703443498f94ad5771089f722f2.jpg]]

**中文解析**：

本题考察从苯出发的合成路线设计，核心是利用定位效应控制取代基的引入顺序。

关键要点：
1. **第一个目标分子（间氨基苯乙酮）**：含酮基（吸电子、间位定位）和氨基（给电子、邻对位定位）。两个可能路线：
   - 路线A：苯 → Friedel-Crafts酰基化 → 硝化（间位）→ 还原NO₂为NH₂
   - 路线B：苯 → 硝化 → Friedel-Crafts酰基化 → 还原
2. **第二个目标分子（对硝基溴苯）**：含Br（邻对位定位）和NO₂（间位定位），需要对位关系。必须先Br后NO₂——因为Br是邻对位定位基，引导NO₂到对位
3. **第三个目标分子**：两个邻对位定位基处于间位。必须通过Friedel-Crafts酰基化+还原来引入烷基（伯烷基不能直接FC烷基化）。酰基是间位定位，可以同时解决两个问题：先酰基化→溴化（间位到酰基）→还原酰基为烷基

> **合成设计核心原则**：反应顺序由定位效应决定。先引入能引导后续取代到正确位置的基团。注意Friedel-Crafts烷基化不能引入伯烷基（重排问题）。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[芳香亲电取代]] | 多步合成中每步的亲电取代反应 | 直接 |
| [[合成设计]] | 利用定位效应设计合成路线 | 直接 |
| [[定位效应]] | 取代基引入顺序对产物结构的决定性影响 | 间接 |
| Friedel-Crafts反应 | FC酰基化与FC烷基化的区别（重排问题） | 间接 |

## 解题思路

1. **读题定位**：题目要求从苯合成三个目标分子——需设计多步合成路线
2. **🔑 关键转换**：分析目标分子中各取代基的定位效应→确定引入顺序（先引入能正确引导后续取代的基团）→注意FC烷基化的限制（伯烷基需通过酰基化+还原引入）
3. **验证**：检查每步反应的区域选择性是否正确；检查最终产物的取代基位置是否与目标一致

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 引入顺序错误导致异构体 | 未考虑定位效应对后续反应的影响 | 先引入能引导取代到正确位置的基团 | 如何判断两个基团谁先引入？ |
| 试图用FC烷基化引入伯烷基 | 不了解FC烷基化的重排限制 | 伯烷基应通过FC酰基化+还原引入 | 为什么FC烷基化会发生重排？ |
| 忽略-NO₂的间位定位效应 | 对定位基分类不熟 | -NO₂是强吸电子基，间位定位 | 如何同时利用多个定位基的效应？ |
| 未考虑还原步骤的选择性 | 不知道如何将NO₂转化为NH₂ | 芳香硝基化合物可通过催化加氢或Fe/HCl还原为胺 | 还原条件会影响其他官能团吗？ |