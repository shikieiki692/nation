---
title: 题-439-Clayden-Ch24-P8-多步序列中区域和化学选择性
type: 题目
submodule: 区域选择性
exam_stage: 初赛
subject: 有机化学
difficulty: 3
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[区域选择性]]"]
tags: [化竞, Clayden, 有机化学, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch24-P8]
source: Clayden Organic Chemistry 2nd Ed. Chapter 24 Problem 8
cross_references: ["[[题-291-Clayden-Ch14-P1-五个分子手性判断]]", "[[题-609-Clayden-Ch36-P2-Beckmann重排立体化学和机理]]", "[[题-608-Clayden-Ch36-P1-原子编号追踪重排]]", "[[题-292-Clayden-Ch14-P2-旋光值区分]]"]
module: 有机化学
status: 已填充
---
# 题-439: 多步序列中区域和化学选择性

## 题目

Comment on the regioselectivity and chemoselectivity of the reactions in the sequence below.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/9fed04216a57280fc0dfc898f39a822a210097e01dc7d7d3351de8b7fe0cd769.jpg]]

**原文题目**：评论下列反应序列中各步反应的区域选择性和化学选择性。

## 参考答案

**Answer (English)**:

**Step 1**: Benzyl bromide is a good electrophile and reacts well with alkoxides to make ethers. With neutral alcohols, the substitution is very slow, so only the more nucleophilic (and more basic) pyridine nitrogen is attacked, to make a pyridinium salt.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/243ca4fe2162813cdbd67781ebea90f7493a28b0d6386c3c0af7faaeae9614cc.jpg]]

**Step 2**: The pyridinium salt is like an iminium ion, so sodium borohydride attacks it at the C=N+ bond to make a neutral enamine. The enamine is protonated to make another iminium, which can then be reduced. The final double bond is safe from attack, since it is an isolated, electron-rich alkene.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/d3d209ee6c2946857f42ef642e4faabeff4ed3bb6850501864ed32a2517a4252.jpg]]

**Step 3**: Methyl chloroformate reacts with the pyridine N (most nucleophilic atom). Then Cl- attacks the benzylic carbon (most susceptible to nucleophilic substitution due to the adjacent pi system), giving the final product.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/e911b465a16b4502ac7fcec05cd8f3099ffc33fffe4fec6141b8c77aa9be634c.jpg]]

**中文解析**：

**步骤1：苄基溴 + 吡啶醇 → 吡啶鎓盐**
- 化学选择性：苄基溴是好的亲电体，醇钠可以进攻→但中性醇的亲核取代很慢
- 选择性：吡啶氮比醇氧更亲核/更碱性→氮进攻苄基溴→形成N-苄基吡啶鎓盐
- 关键：碱性更强的氮原子被选择性地烷基化

**步骤2：NaBH4还原**
- NaBH4进攻C=N+双键（类似亚胺离子）→中性烯胺
- 烯胺被质子化→新的亚胺离子→再次被NaBH4还原
- 化学选择性：孤立的富电子C=C双键不被NaBH4还原
- 关键：NaBH4只还原亚胺离子（C=N+），不还原孤立烯烃

**步骤3：氯甲酸甲酯 + Cl-脱苄基**
- 化学选择性：吡啶N是最亲核的原子→进攻氯甲酸甲酯的C=O
- 区域选择性：Cl-选择性进攻苄基碳（苄基位最容易发生亲核取代，因相邻π体系加速）
- 关键：利用苄基的特殊反应性实现选择性脱保护

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[区域选择性]] | 多个亲核位点中的选择性进攻 | 直接 |
| [[化学选择性]] | NaBH4选择性还原C=N+而不还原C=C | 直接 |
| [[苄基化学]] | 苄基位的亲核取代特殊性 | 间接 |
| [[吡啶]] | 吡啶氮的亲核性和吡啶鎓盐的反应性 | 间接 |

## 解题思路

1. 读题定位：三步反应序列，每步都有多个可能的反应位点，需要分析每步的选择性
2. 关键转换：
   - 步骤1：N vs O竞争亲核性→N更强→N-烷基化
   - 步骤2：C=N+ vs C=C竞争NaBH4→只有C=N+被还原
   - 步骤3：N-酰基化 + Cl-选择性脱苄基（苄基位易取代）
3. 验证：最终产物中N上有甲氧羰基，苄基被移除

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 认为NaBH4能还原C=C | 混淆了NaBH4和LiAlH4的还原能力 | NaBH4只还原C=O和C=N+，不还原孤立C=C | 为什么NaBH4不能还原烯烃？ |
| 不理解为什么N比O先反应 | 没有比较亲核性 | 吡啶氮的亲核性远大于中性醇氧 | 为什么吡啶氮的亲核性这么强？ |
| 不理解Cl-脱苄基的机理 | 认为Cl-是离去基团而非亲核试剂 | Cl-在这里是亲核试剂，进攻苄基碳→SN2脱保护 | 什么使苄基位特别容易被亲核进攻？ |