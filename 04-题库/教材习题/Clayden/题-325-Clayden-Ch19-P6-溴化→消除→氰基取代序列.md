---
title: 题-325-Clayden-Ch19-P6-溴化→消除→氰基取代序列
type: 题目
fidelity: 原书逐字
submodule: 烯烃的亲电加成
exam_stage: 初赛
subject: 有机化学
difficulty: 4
teaching_level: 拓展
syllabus_codes: ["2.3", "3.1", "3.2"]
knowledge_points: ["[[亲电加成]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch19-P6]
source: Clayden Organic Chemistry 2nd Ed. Chapter 19 Problem 6
cross_references: ["[[题-321-Clayden-Ch19-P2-两个烯烃溴化机理和产物]]", "[[题-326-Clayden-Ch19-P7-内部OH亲核的溴化机理和NMR偶合]]", "[[题-400-Clayden-Ch22-P10-环戊烯酮还原共轭vs直接加成顺序]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 模块习题集
---
# 题-325: 溴化→消除→氰基取代序列

## 题目

Propose mechanisms for the following three-step sequence:

1. An alkene reacts with Br₂ → trans-dibromide
2. The dibromide is treated with base → allylic bromide (via E2 elimination)
3. The allylic bromide reacts with NaCN → substitution product with a new C-C bond

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/ebb02885fd1a54221876a3f90531acb3c0ce1945c41a33b4ef50b4989896cdd4.jpg]]

**原文题目**：

为以下三步反应序列提出机理：

1. 烯烃与 Br₂ 反应 → 反式二溴化物
2. 二溴化物用碱处理 → 烯丙基溴化物（经 E2 消除）
3. 烯丙基溴化物与 NaCN 反应 → 含新 C-C 键的取代产物

## 参考答案

**Answer (English)**:

**Step 1 — Bromination**: Br₂ adds across the double bond via a bromonium ion intermediate → anti addition gives the trans-dibromide (e.g., cyclohexene → trans-1,2-dibromocyclohexane).

**Step 2 — E2 elimination**: Strong base (e.g., NaOH or NaOEt) abstracts a proton from a carbon adjacent to one of the C-Br bonds. The anti-periplanar requirement of E2 means only a hydrogen that is **trans-diaxial** (anti) to the departing Br can be eliminated. This gives an allylic bromide (e.g., 3-bromocyclohexene). Note: only the H that is anti to Br can be abstracted — this regioselectivity is dictated by stereoelectronic requirements.

**Step 3 — SN2 with CN⁻**: Cyanide ion (NaCN) is a good nucleophile. It performs an SN2 attack on the allylic bromide at the carbon bearing Br. Allylic substrates are especially reactive in SN2 due to transition state stabilization by the adjacent π-system. The product is an allylic nitrile with a new C-C bond.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/1d04af6956e08b71f329ceb14f00a192d311f1fd5fbe8bdc87ac7ab5a464ab00.jpg]]

**中文解析**：

**步骤 1（溴化）**：Br₂ 通过溴鎓离子中间体对烯烃进行反式加成。以环己烯为例，生成 *trans*-1,2-二溴环己烷（两个 Br 分别在环的两侧）。

**步骤 2（E2 消除）**：强碱夺取与 C-Br 相邻碳上的 H。E2 反应要求 **反式共平面（anti-periplanar）** 的几何构型——H 和 Br 必须处于反式位置（即反式双直立键）。在 trans-1,2-二溴环己烷中，只有一种 H 满足此立体电子要求。消除后得到**烯丙基溴化物**（如 3-溴环己烯）。

**步骤 3（SN2 取代）**：CN⁻ 是优秀的亲核试剂，对烯丙基溴化物进行 SN2 进攻。烯丙基底物在 SN2 反应中特别活泼（过渡态中相邻 π 系统提供额外稳定化）。产物是烯丙基腈，引入了一个新的 C-C 键。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[亲电加成]] | Br₂ 通过溴鎓离子的反式加成生成二溴化物 | 直接 |
| [[消除反应]] | E2 消除的反式共平面要求及烯丙基溴化物的生成 | 直接 |
| [[亲核取代]] | CN⁻ 对烯丙基溴的 SN2 取代（引入 C-C 键） | 间接 |

## 解题思路

1. **读题定位**：三步合成序列——加成 → 消除 → 取代，每步都有明确的立体化学要求
2. **🔑 关键转换**：反式二溴化物 → E2 只能消除反式共平面的 H → 烯丙基溴 → SN2 活性增强 → CN⁻ 取代引入 C-C 键
3. **验证**：步骤 2 必须满足 anti-periplanar 几何；步骤 3 烯丙基底物 SN2 加速效应

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| E2消除不考虑立体化学 | 忽视了anti-periplanar的严格要求 | 只有与Br反式共平面的H才能被消除 | 为什么E2必须要求反式共平面？ |
| 步骤3写成SN1机理 | 忽视了烯丙基底物SN2活性特别高 | 烯丙基碳正离子虽稳定，但CN⁻是强亲核试剂且SN2更快 | 烯丙基SN2的过渡态如何被稳定？ |
| 认为E2可以消除任意β-H | 不理解立体电子效应的控制 | 反式双直立键是唯一满足条件的构象 | 如果β-H全部不是反式的会怎样？ |