---
title: 题-424-Clayden-Ch23-P1-溴代醛选择性转化为两个产物
type: 题目
fidelity: 原书逐字
submodule: 化学选择性与保护基
exam_stage: 初赛
source_subject: 有机化学
difficulty: 2
teaching_level: 巩固
syllabus_codes: ["21"]
knowledge_points: ["[[化学选择性]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch23-P1]
source: Clayden Organic Chemistry 2nd Ed. Chapter 23 Problem 1
cross_references: ["[[题-478-Clayden-Ch27-P2-硫叶立德化学区域和立体化学]]", "[[题-477-Clayden-Ch27-P1-分子内硫叶立德共轭加成环丙烷化]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 章节练习
source_category: 教材课后习题
---
# 题-424: 溴代醛选择性转化为两个产物

## 题目

How would you convert this bromo-aldehyde chemoselectively into the two products shown?

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/e907f7def4f01bf52eef5fece17c3fd69ac494f436dc44b551991fa68a0a161c.jpg]]

## 参考答案

**Answer (English)**: For the product to the right, no protection is needed — a Grignard reagent will add directly to the aldehyde:

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/ce42e38666a2fd98874c5cd7254dc661ea8015e0553da0ac772b2dd0489827e4.jpg]]

For the other product, the aldehyde needs to be protected as an acetal before making the Grignard reagent from the aryl bromide. Then add to RCHO, and deprotect with acid:

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/657560b43dbd425ae1cf12705c75697b155c0484ba8b83477bb93639281e6c52.jpg]]

**中文解析**：

关键要点：
1. **无需保护的路径**（→右侧产物）：格氏试剂直接加成到醛基，不需要保护——醛基比C-Br键更活泼
2. **需要保护的路径**（→左侧产物）：需要先将醛基保护为缩醛，然后从芳基溴制备格氏试剂，再与另一个醛加成，最后酸性脱保护
3. **化学选择性核心**：格氏试剂同时与醛和C-Br反应——保护醛基后才能安全制备格氏试剂

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[化学选择性]] | 同一分子中不同官能团的选择性反应 | 直接 |
| [[保护基]] | 缩醛保护醛基防止与格氏试剂反应 | 直接 |
| NaBH4还原 | 醛基的亲核加成反应 | 间接 |
| [[格氏试剂]] | 格氏试剂的制备和与醛的加成 | 间接 |

## 解题思路

1. **读题定位**：题目要求将溴代醛选择性转化为两个不同产物——核心是化学选择性和保护策略
2. **🔑 关键转换**：右侧产物：格氏试剂直接加成到醛（无需保护）；左侧产物：先缩醛保护醛→制备格氏试剂→加成→脱保护
3. **验证**：检查每步反应的选择性是否正确，保护/脱保护条件是否兼容

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 忘记格氏试剂会与醛反应 | 不了解格氏试剂的反应性 | 格氏试剂是强亲核试剂，会进攻醛/酮 | 格氏试剂还能与哪些官能团反应？ |
| 保护条件选择不当 | 不了解缩醛的形成条件 | 醇+酸催化形成缩醛，碱性条件稳定 | 缩醛在什么条件下稳定/不稳定？ |
| 脱保护与产物不兼容 | 没有考虑脱保护条件的影响 | 酸性水解脱保护，需确认不影响其他官能团 | 除了酸性水解，还有什么脱保护方法？ |