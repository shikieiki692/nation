---
title: 题-483-Clayden-Ch27-P7-同时制备E和Z异构体
type: 题目
fidelity: 原书逐字
submodule: 硫硅磷化学
exam_stage: 初赛
subject: 有机化学
difficulty: 3
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[Wittig反应]]"]
tags: [化竞, Clayden, 有机化学, 硫化学]
updated: 2026-07-25
aliases: [Clayden-Ch27-P7]
source: Clayden Organic Chemistry 2nd Ed. Chapter 27 Problem 7
cross_references: ["[[题-424-Clayden-Ch23-P1-溴代醛选择性转化为两个产物]]", "[[题-425-Clayden-Ch23-P2-内酯选择性开环]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 章节练习
---
# 题-483: 同时制备E和Z异构体

## 题目

How would you prepare samples of both geometrical isomers of this compound?

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/6273558e5681f61ee5c09014ba87cf04ee4428582fb0536ba06b0e17cfbbe355.jpg]]

**原文题目**：How would you prepare samples of both geometrical isomers of this compound?

## 参考答案

**Answer (English)**: There are many methods that can be used to tackle this question. The only snags are protecting the OH group if necessary and care in isolating the Z-compound as it may isomerize easily to the E-compound by reversible conjugate addition. One way to the Z-alkene uses reduction of an alkyne to control the stereochemistry.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/011d25bb56a91edd63277ddd42dd5a193b037efa8311075578285686b3822139.jpg]]

The E-alkene might be produced by reduction of the alkyne with an alkali metal in liquid ammonia but a Wittig reaction is probably easier. Either a phosphonium ylid or a phosphonate ester could be used.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/f5443693e005b0a8fdbbb25c0f9001079f062f650658f3585161d6f3febb3db9.jpg]]

**中文解析**：

关键步骤：
1. **Z-烯烃路线**：炔烃还原为Z-烯烃（Lindlar催化剂，H₂/Pd-BaSO₄），OH保护为苄醚（Bn），氢化同时脱保护和还原炔
2. **E-烯烃路线**：
   - 方法一：炔烃用Na/NH₃(l)还原→E-烯烃
   - 方法二（更优）：Wittig反应——稳定化叶立德或Horner-Wadsworth-Emmons磷酸酯→E-烯烃
3. **保护基策略**：OH需保护（酯或苄醚），避免干扰反应；最后统一水解

> **核心要点**：要得到两种异构体，需要两种不同的立体选择性方法——炔还原（Lindlar→Z，Na/NH₃→E）或Wittig（稳定化→E）。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| Wittig反应 | 稳定化叶立德/HWE反应制备E-烯烃 | 直接 |
| [[Julia成烯]] | 替代方案：Julia反应也可高E选择性 | 间接 |
| [[烯烃立体选择性]] | 不同方法的选择性对比和互补性 | 直接 |
| Lindlar还原 | 炔→Z-烯烃的立体选择性还原 | 间接 |

## 解题思路

1. **读题定位**：合成设计题——需分别制备E和Z异构体
2. **关键转换**：Z-烯烃→Lindlar炔还原；E-烯烃→Wittig/HWE或Na/NH₃还原
3. **验证**：检查保护基策略是否完整（OH保护→反应→脱保护）

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| Z-烯烃用Wittig制备 | 非稳定化Wittig虽然给Z但选择性不如Lindlar | Lindlar还原炔烃是更可靠的Z-烯烃方法 | Lindlar催化剂的组成是什么？ |
| 忽略OH保护 | 认为OH不干扰 | OH可能干扰Wittig/还原反应，需保护 | 常见醇保护基有哪些？ |
| Z-烯烃异构化 | Z-烯烃可能通过可逆共轭加成异构为E | 快速分离，避免长时间暴露 | Z-烯烃为什么不稳定？ |