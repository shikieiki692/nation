---
title: 题-525-Clayden-Ch41-P2-拆分法规划不对称合成入门
type: 题目
submodule: 不对称合成
exam_stage: 决赛
subject: 有机化学
difficulty: 3
teaching_level: 巩固
syllabus_codes: ["21"]
knowledge_points: ["[[不对称合成]]", "[[拆分技术]]"]
tags: [化竞, Clayden, 有机化学, 不对称合成]
updated: 2026-07-25
aliases: [Clayden-Ch41-P2]
source: Clayden Organic Chemistry 2nd Ed. Chapter 41 Problem 2
cross_references: ["[[题-291-Clayden-Ch14-P1-五个分子手性判断]]", "[[题-292-Clayden-Ch14-P2-旋光值区分]]", "[[题-477-Clayden-Ch27-P1-分子内硫叶立德共轭加成环丙烷化]]", "[[题-478-Clayden-Ch27-P2-硫叶立德化学区域和立体化学]]"]
module: 有机化学
status: 已填充
---
# 题-525: 拆分法规划不对称合成入门

## 题目

This is a synthesis of the racemic drug tazodolene. If the enantiomers of the drug are to be evaluated for biological activity, they must be separated. At which stage would you recommend separating the enantiomers and how would you do it?

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/e9821760813490d2c58cda81ba6541d811c0cf44666f833c0454ef82d0847daa.jpg]]

**原文题目**：This is a synthesis of the racemic drug tazodolene. If the enantiomers of the drug are to be evaluated for biological activity, they must be separated. At which stage would you recommend separating the enantiomers and how would you do it?

## 参考答案

**Answer (English)**: You need to ask: which is the first chiral intermediate? Can it be conveniently resolved? Will the chirality survive subsequent steps? The first intermediate is chiral but it enolizes very readily and the enol is achiral, so that's no good. The second intermediate is chiral but it has three chiral centres and these are evidently not controlled. We would have to separate the diastereoisomers before resolution and that would be a waste of time and material since all of them give the next intermediate anyway. The next intermediate, the amino alcohol is ideal: it has only one chiral centre and that is not affected by the last reaction. It has two 'handles' for resolution—the amine and the alcohol. We might make a salt with tartaric acid or an ester of the alcohol with some chiral acid. Alternatively we could resolve tazodolene itself: it still has an amino group and we could form a salt with a suitable acid.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/685d5c19d33967d0836dd2ed7b9e8c5c6b6c73267051e17932fe441eb0ee124f.jpg]]

**中文解析**：

**整体策略分析**：
本题考查的是在合成路线中选择最佳拆分时机的能力。拆分（resolution）是获取对映体纯化合物的经典方法之一，关键在于选择合适的中间体进行拆分——需要同时满足三个条件：(1) 只有一个手性中心；(2) 手性中心在后续步骤中不受影响；(3) 有便于形成非对映体盐/酯的官能团。

**逐步分析每个中间体的可拆分性**：

1. **第一个手性中间体**：虽然是手性的，但很容易发生烯醇化（enolization），烯醇是无手性的——拆分后会通过烯醇化重新消旋化，因此不适合拆分
2. **第二个手性中间体**：有三个手性中心，但这些手性中心的立体化学"未受控"（non-selective）。所有非对映异构体在下一步都会给出相同产物，因此先分离非对映体再拆分纯属浪费时间和原料
3. **第三个中间体（氨基醇）——最佳选择**：
   - 只有**一个手性中心**
   - 最后一步反应不影响该手性中心
   - 有两个可用于拆分的"把手"（handles）：胺基和羟基
   - 可以用酒石酸成盐拆分（胺基），或者用手性酸酯化拆分（羟基）

4. **也可拆分最终产物tazodolene本身**：产物仍有氨基，可以和合适的酸形成非对映体盐进行拆分

**拆分方法的化学原理**：
- 形成非对映体盐：胺 + 酒石酸 → (R)-胺·酒石酸盐和(S)-胺·酒石酸盐（非对映体，溶解度不同，可分级结晶分离）
- 形成非对映体酯：醇 + 手性酸 → (R)-酯和(S)-酯（非对映体，可通过色谱分离）

**参考文献**：此合成路线来自Upjohn公司专利文献（Chem. Abstr., 1984, 100, 6311）。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[不对称合成]] | 拆分法作为获取单一对映体的策略 | 直接 |
| [[拆分技术]] | 选择拆分时机的三个判断标准 | 直接 |
| [[手性中心]] | 手性中心数量和稳定性对拆分可行性的影响 | 间接 |
| [[非对映体]] | 通过形成非对映体盐/酯实现物理分离 | 间接 |

## 解题思路

1. **读题定位**：题目要求在给出的外消旋合成路线中选择最佳拆分步骤和方法。关键词：外消旋药物、对映体分离、最佳时机
2. **🔑 关键转换**：逐一评估每个中间体——(a) 是否容易消旋化？(b) 手性中心数量是否可控？(c) 是否有合适的官能团用于拆分？第三中间体（氨基醇）同时满足三个条件
3. **验证**：氨基醇只有一个手性中心，不受最后一步影响；胺基可与酒石酸成盐，羟基可酯化——两种拆分"把手"都可用

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 选择第一个中间体拆分 | 只看到"有手性中心"就认为可拆分 | 第一个中间体极易烯醇化导致消旋化，拆分后手性信息会丢失 | 为什么烯醇化会导致手性信息丢失？ |
| 选择第二个中间体拆分 | 没注意到有三个未控手性中心 | 三个手性中心的立体化学不受控，非对映体混合物需要先分离再拆分，效率极低 | 为什么说"所有非对映体给出同一产物"意味着不需要拆分？ |
| 只想到成盐拆分 | 拆分方法思维定式 | 氨基醇有两个把手：胺基可成盐，羟基可酯化，两种方法都可行 | 酒石酸拆分胺的化学原理是什么？ |
| 忽略最终产物也可拆分 | 认为必须在中间体拆分 | tazodolene本身有氨基，也可以用合适酸成盐拆分 | 为什么在中间体拆分有时比拆分最终产物更好？ |