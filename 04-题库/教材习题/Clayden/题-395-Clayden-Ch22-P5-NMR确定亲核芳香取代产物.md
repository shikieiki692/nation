---
title: 题-395-Clayden-Ch22-P5-NMR确定亲核芳香取代产物
type: 题目
submodule: 共轭加成
exam_stage: 初赛
subject: 有机化学
difficulty: 3
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[芳香亲核取代]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch22-P5]
source: Clayden Organic Chemistry 2nd Ed. Chapter 22 Problem 5
cross_references: ["[[题-629-Clayden-Ch38-P2-另一种卡宾方法→天然抗生素]]", "[[题-321-Clayden-Ch19-P2-两个烯烃溴化机理和产物]]", "[[题-628-Clayden-Ch38-P1-碱引发两个简单卡宾反应]]", "[[题-320-Clayden-Ch19-P1-HCl对三个烯烃加成方向]]"]
module: 有机化学
status: 已填充
---
# 题-395: NMR确定亲核芳香取代产物

## 题目

What is the structure of the product of this reaction and how is it formed? It has δC 191, 164, 132, 130, 115, 64, 41, 29 and δH 2.32 (6H, s), 3.05 (2H, t, J 6 Hz), 4.20 (2H, t, J 6 Hz), 6.97 (2H, d, J 7 Hz), 7.82 (2H, d, J 7 Hz), 9.97 (1H, s). You should obviously interpret the spectra to get the structure.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/8d0bc0b23f642578383e9f188c6a7aa6cd0c0c5c97fa519006a1d3fe5394d7e5.jpg]]

**原文题目**：Determine the structure of the SNAr product using ¹H and ¹³C NMR data. The reaction involves nucleophilic aromatic substitution with an amino alcohol on a fluorinated benzaldehyde.

## 参考答案

**Answer (English)**: Summing the formulae of the two starting materials shows that this is a substitution of fluoride (the product is the sum of the starting materials less HF). The aldehyde is still there (from the IR and the proton at 10 ppm) so the spectra are best interpreted by this structure:

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/a5d5381e4766fc69ad9a86c5f2dc387149aedf4d464bc1c9d0fd048bd9d0c8b1.jpg]]

That suggests a simple nucleophilic aromatic substitution by the addition-elimination mechanism with both F and CHO assisting the first step.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/e66ed62a71929723a32cd3e967253c979018442d185b45e733ae731f3c18a075.jpg]]

**中文解析**：

关键步骤：
1. **分子式分析**：两个起始原料的分子式之和减去HF，得到产物分子式。这表明发生了氟的亲核取代（SNAr）
2. **NMR解析**：
   - δH 9.97 (1H, s)：醛基质子（-CHO），说明醛基保留
   - δH 6.97和7.82 (各2H, d)：苯环上的AA'BB'系统，说明是对位二取代苯环
   - δH 4.20 (2H, t)和3.05 (2H, t)：-OCH₂CH₂N-片段
   - δH 2.32 (6H, s)：两个N-CH₃基团
   - δC 191：醛基碳
3. **机理**：SNAr通过加成-消除机制进行，F和CHO都是活化基团，协助亲核进攻形成Meisenheimer复合物

> **核心概念**：SNAr反应中，吸电子基团（如F、CHO）通过稳定Meisenheimer复合物中的负电荷来活化苯环。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[芳香亲核取代]] | SNAr反应的加成-消除机理 | 直接 |
| [[NMR谱学]] | 利用¹H和¹³C NMR确定SNAr产物结构 | 直接 |
| SNAr反应 | Meisenheimer复合物的形成和离去基团的消除 | 间接 |

## 解题思路

1. **读题定位**：题目给出反应和NMR数据，要求推断产物结构——识别这是SNAr反应（含F的芳环+亲核试剂）
2. **🔑 关键转换**：分子式分析→减去HF→产物含N原子→NMR验证醛基保留+苯环对位取代+胺基片段
3. **验证**：检查NMR数据是否与推断结构一致——化学位移、积分、偶合常数是否匹配

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 忘记计算分子式差值 | 没有从分子式入手分析反应类型 | 两个原料之和减去HF，确认是取代反应 | 为什么是取代HF而不是加成？ |
| 错误解读NMR偶合模式 | 对AA'BB'系统不熟悉 | 两个双峰（d）且J值相同是对位二取代苯环的典型特征 | 为什么对位取代苯环显示两个双峰？ |
| 忽略醛基质子信号 | 对特征化学位移不熟 | δH 9.97是醛基质子的特征信号（9-10 ppm） | 醛基质子的化学位移范围是多少？ |