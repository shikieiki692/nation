---
title: 题-533-Clayden-Ch41-P10-可不对称合成的结构特征识别
type: 题目
fidelity: 原书逐字
submodule: 不对称合成
exam_stage: 决赛
source_subject: 有机化学
difficulty: 3
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[不对称合成]]", "[[立体化学]]"]
tags: [化竞, Clayden, 有机化学, 不对称合成, 信息素]
updated: 2026-07-25
aliases: [Clayden-Ch41-P10]
source: Clayden Organic Chemistry 2nd Ed. Chapter 41 Problem 10
cross_references: ["[[题-477-Clayden-Ch27-P1-分子内硫叶立德共轭加成环丙烷化]]", "[[题-291-Clayden-Ch14-P1-五个分子手性判断]]", "[[题-478-Clayden-Ch27-P2-硫叶立德化学区域和立体化学]]", "[[题-292-Clayden-Ch14-P2-旋光值区分]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 章节练习
---
# 题-533: 可不对称合成的结构特征识别

## 题目

The triatomine bug which causes Chagas' disease can be trapped by using synthetic samples of its communication pheromone, which consists of a 4:1 mixture of the enantiomers of this heterocycle. How would you synthesize the required mixture of enantiomers? Why would the other diastereoisomer of this compound be more of a challenge to make?

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/3aa2f72c8e02cfa05b0fd391fdbbf65d969338d6dafa3fe240d923dbfb859554.jpg]]

**原文题目**：The triatomine bug which causes Chagas' disease can be trapped by using synthetic samples of its communication pheromone, which consists of a 4:1 mixture of the enantiomers of this heterocycle. How would you synthesize the required mixture of enantiomers? Why would the other diastereoisomer of this compound be more of a challenge to make?

## 参考答案

**Answer (English)**: To make a 4:1 mixture of enantiomers you need either to mix them in the right proportions, or to mix equal amounts of racemic mixture and a single enantiomer. In either case you need an asymmetric synthesis. The target compound is an acetal that can be made from a chiral diol, so you should immediately consider asymmetric dihydroxylation. The advantage of Sharpless' asymmetric dihydroxylation is that it can very easily give either enantiomer: in fact, it is one reaction where the enantioselective version is better than the racemic one, so you would be advised to make the two enantiomers using the two alternative chiral ligands, mix them in the correct proportions, then form the acetal. Note that the starting alkene is trans.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/441ea4f25e4368f2fc37155b153475e4918570f46d9ba6b734ee69c7441b8ada.jpg]]

Making the other diastereoisomer would require the cis alkene. This is not a problem in itself, but more of a challenge for the catalyst, because now it has to distinguish between two similar groups (Et and Me) in order to oxidize one face of the alkene enantioselectively (for the trans alkene, the selection is between either Et and H or Me and H; switching Et for Me makes no difference to the outcome).

**中文解析**：

**整体策略分析**：
本题考查三个核心能力：(1) 从外消旋混合物制备特定比例的对映体混合物的策略；(2) 识别目标分子结构特征并匹配不对称合成方法；(3) 理解不对称催化反应中底物结构对选择性的影响。

**目标分子分析**：
- 目标化合物是一个缩醛（acetal），可以从手性1,2-二醇制备
- 需要的是4:1的对映体混合物（非单一对映体！）
- 缩醛的前体是trans-烯烃

**合成策略**：

1. **制备4:1对映体混合物的策略**：
   - 方案A：分别合成两种对映体，按4:1比例混合
   - 方案B：混合等量的外消旋体和单一对映体（得到3:1比例，不完全匹配4:1）
   - **推荐方案A**——更精确控制比例

2. **Sharpless不对称双羟化（AD）构建手性二醇**：
   - 目标缩醛的前体是手性1,2-二醇
   - Sharpless AD可以高效构建手性邻二醇
   - **关键优势**：使用两种替代手性配体（(DHQD)2PHAL和(DHQ)2PHAL），可以非常方便地获得两种对映体
   - AD反应的对映选择性版本甚至比消旋版本更好——这是一个罕见的"不对称版本优于消旋版本"的例子

3. **具体路线**：
   - 从trans-烯烃出发
   - 用(DHQD)2PHAL配体进行AD→得到一种对映体的二醇（主要产物）
   - 用(DHQ)2PHAL配体进行AD→得到另一种对映体的二醇
   - 按4:1比例混合两种二醇
   - 形成缩醛→目标产物

**为什么另一个非对映异构体更难合成**：
- 另一个非对映异构体需要从**cis-烯烃**出发
- cis-烯烃中，两个取代基（Et和Me）相似——催化剂需要区分Et和Me来选择氧化面
- 而在trans-烯烃中，选择是Et对H或Me对H——区分大基团和小氢原子（H）比区分两个烷基（Et和Me）容易得多
- 因此cis-烯烃的不对称双羟化ee值会显著低于trans-烯烃

**参考文献**：C. R. Unelius et al., Org. Lett. 2010, 12, 5601。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[不对称合成]] | 制备特定比例对映体混合物的策略 | 直接 |
| [[立体化学]] | trans/cis烯烃对不对称双羟化选择性的影响 | 直接 |
| [[合成设计]] | 从目标缩醛倒推到手性二醇再到烯烃 | 直接 |
| [[不对称双羟化]] | Sharpless AD反应的底物适用范围和选择性 | 间接 |

## 解题思路

1. **读题定位**：题目要求设计4:1对映体混合物的合成，并解释另一个非对映异构体为何更难。关键词：4:1混合物、Chagas病信息素、非对映异构体
2. **🔑 关键转换**：缩醛←手性二醇←Sharpless AD←trans-烯烃；两种配体给出两种对映体→按比例混合。cis-烯烃中Et/Me相似→催化剂难以区分→选择性低
3. **验证**：(a) AD反应的ee值通常>90%；(b) 4:1比例可通过精确称量控制；(c) cis-烯烃的选择性问题来自底物对称性

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 试图用单一不对称反应直接得到4:1混合物 | 不对称反应通常给出>50% ee，不会给出20% ee | 需要分别合成两种对映体再按比例混合 | 不对称反应能直接给出20% ee吗？ |
| 混淆非对映异构体和对映异构体 | 基本概念不清 | 题目问的是"另一个非对映异构体"——指缩醛的另一个立体异构体，不是对映异构体 | 非对映异构体和对映异构体有什么区别？ |
| 不理解为什么cis-烯烃更难 | 没有分析催化剂的面选择性要求 | trans-烯烃：选择Et/H或Me/H（大小差异大）；cis-烯烃：选择Et/Me（大小差异小） | 催化剂如何区分烯烃的不同面？ |
| 忘记缩醛化是最后一步 | 没有进行逆合成分析 | 二醇是中间体，缩醛化是最后一步——两种对映体的二醇分别缩醛化再混合 | 缩醛化的条件是什么？ |