---
title: 题-617-Clayden-Ch36-P10-三元环扩张等于四元环收缩
type: 题目
submodule: 重排反应
exam_stage: 初赛
subject: 有机化学
difficulty: 3
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[重排反应]]"]
tags: [化竞, Clayden, 有机化学, 重排反应, 环张力, Pinacol重排]
updated: 2026-07-25
aliases: [Clayden-Ch36-P10]
source: Clayden Organic Chemistry 2nd Ed. Chapter 36 Problem 10
cross_references: ["[[题-515-Clayden-Ch40-P2-Heck反应机理步骤理解]]", "[[题-433-Clayden-Ch24-P2-不饱和羰基直接共轭加成区域选择性]]", "[[题-432-Clayden-Ch24-P1-氨基醇制备中区域选择性试剂选择]]", "[[题-514-Clayden-Ch40-P1-烯醇醚溴化WittigPd化学入门]]"]
module: 有机化学
status: 已填充
---
# 题-617: 三元环扩张 = 四元环收缩

## 题目

Give mechanisms for these reactions that explain any selectivity.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/a4f5bc835ed110fd2e7e740ff74b5c9e376ee7a271360958a529e7d20736b712.jpg]]

**原文题目**：给出这些反应的机理，解释任何选择性。

## 参考答案

**Answer (English)**: The first mechanism is a pinacol rearrangement and the compound is symmetrical so it doesn't matter which alcohol is protonated. Both three- and four-membered rings are strained and the σ-bonds are more reactive than normal (they have a high energy HOMO). This makes ring contraction an easy reaction even though the strain is not relieved.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/908122168a069e7b174b260cc33a545ae18ab8e833d1bc2510c507dda50a1a84.jpg]]

The second example looks at first to be a similar pinacol rearrangement. But the resulting ketone cannot easily be transformed into the product.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/69be23a54c1a9daa7451b992f9fe0129dd5cf2a0359e533e499f45f7b9fe8437.jpg]]

Breaking open one of the three-membered rings gets us off to a better start. This gives a hydroxy-ketone that can rearrange in a pinacol fashion with ring expansion of the remaining cyclopropane.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/ba1770da54e806149d0cc0a0b8b6c717e5a413df545007b51f6210c7caee70c7.jpg]]

**中文解析**：

**反应1——三元环的Pinacol重排（环收缩）**：
1. 对称分子，质子化任一OH均可
2. 失水形成碳正离子
3. 三元环的C-C键迁移 → 环收缩为二元环（环丙烷→环丙烷，实际上是三元环内的重排）
4. 关键点：三元环和四元环的σ键都很活泼（高能量HOMO），因此**环收缩也是容易的反应**——即使张力没有释放

**反应2——先开环再Pinacol重排（环扩张）**：
1. 直接Pinacol重排的产物无法合理转化为最终产物
2. 正确路径：先打开一个三元环 → 得到羟基酮
3. 羟基酮进行Pinacol重排 → 剩余的三元环扩张

> **核心教学点——三元环和四元环σ键的反应性**：
> - 三元环和四元环因环张力，σ键的HOMO能量高
> - 这使得σ键更容易参与迁移（无论环收缩还是环扩张）
> - 因此三元环→四元环（扩张）和四元环→三元环（收缩）**同样容易**
> - 这与直觉相反——通常认为只有释放张力的反应才容易

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[重排反应]] | Pinacol重排在小环中的应用 | 直接 |
| [[环张力]] | 小环σ键的高HOMO能量与反应性 | 直接 |
| [[1,2-迁移与重排]] | 环收缩和环扩张中的C-C键迁移 | 直接 |
| [[Pinacol重排]] | 对称二醇的频哪醇重排 | 直接 |

## 解题思路

1. **读题定位**：两个反应的机理 + 选择性解释。重点是理解小环的σ键反应性
2. **🔑 关键转换**：
   - 反应1：对称二醇 → Pinacol重排 → 环收缩（σ键活泼，即使不释放张力也容易）
   - 反应2：不能直接Pinacol → 先开环得羟基酮 → Pinacol重排 + 环扩张
3. **验证**：检查环收缩/扩张是否合理；检查σ键HOMO能量的解释是否自洽

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 认为环收缩不可能 | 直觉认为只有释放张力的反应才容易 | 三元环σ键的高HOMO能量使收缩同样容易 | 为什么三元环的σ键比正常σ键更活泼？ |
| 反应2走直接Pinacol路径 | 没有分析直接重排产物能否转化为最终产物 | 直接Pinacol重排产物无法转化为最终产物 → 需要先开环 | 如何判断一个重排路径是否可行？ |
| 混淆环扩张和环收缩的方向 | 没有明确标注环的大小变化 | 反应1：三元环内重排（收缩）；反应2：三元环→四元环（扩张） | 三元环→四元环是释放还是增加张力？ |