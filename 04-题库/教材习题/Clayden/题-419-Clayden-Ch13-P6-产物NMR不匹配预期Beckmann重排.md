---
title: 题-419-Clayden-Ch13-P6-产物NMR不匹配预期Beckmann重排
type: 题目
submodule: NMR谱学
exam_stage: 初赛
subject: 有机化学
difficulty: 4
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[NMR谱学]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch13-P6]
source: Clayden Organic Chemistry 2nd Ed. Chapter 13 Problem 6
cross_references: ["[[题-561-Clayden-Ch30-P2-不熟悉杂环合成和芳香性判断]]", "[[题-536-Clayden-Ch18-P1-C6H5FO的13C NMR C-F偶合结构确定]]", "[[题-560-Clayden-Ch30-P1-吡咯并吡啶三环芳香杂环合成]]", "[[题-537-Clayden-Ch18-P2-Bullatenone结构A预测NMR并纠正]]"]
module: 有机化学
status: 已填充
---
# 题-419: 产物NMR不匹配预期——Beckmann重排还是碎片化？

## 题目

The reaction below was expected to give the product A and did indeed give a compound with the correct molecular formula by its mass spectrum. However the NMR spectrum of this product was:

δ_H (ppm) 1.27 (6H, s), 1.70 (4H, m), 2.88 (2H, m), 5.4–6.1 (2H, broad s, exchanges with D₂O) and 7.0–7.5 (3H, m).

Though the detail is missing from this spectrum, how can you already tell that this is not the expected product?

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/ee8e207681de93bcc21ee1d7e2372ac471ddc348fe2444ea33b8514b6c754e39.jpg]]

## 参考答案

**Answer (English)**: The spectrum is all wrong. There are only three aromatic Hs instead of the four expected. There are two exchanging hydrogens, presumably in NH₂ and not the one expected. The only thing that is expected is the chain of three CH₂ groups.

This surprising result was reported by B. Amit and A. Hassner, Synthesis, 1978, 932. The expected reaction was a Beckmann rearrangement but what actually happened was a Beckmann fragmentation followed by intramolecular Friedel-Crafts alkylation:

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/66bf92fed38b2916a1c676c3afdeb7c91574f419efcb9912b7c1e82ffb35c962.jpg]]

Now you know the structure of the product, you should be able to assign the spectrum and confirm the result.

**中文解析**：

关键要点：
1. **NMR与预期不符的证据**：
   - 芳香H只有3个（δ 7.0–7.5, 3H, m），而预期产物应有4个芳香H
   - 有两个可交换的H（D₂O交换，5.4–6.1 ppm宽单峰），说明是NH₂而非预期的NH
   - 分子中仍有三个CH₂链（与预期一致）
2. **实际反应**：不是Beckmann重排，而是Beckmann碎片化+分子内Friedel-Crafts烷基化
3. **Beckmann碎片化**：肟在酸性条件下不发生迁移而是C–C键断裂，生成腈+碳正离子，碳正离子再进行Friedel-Crafts环化

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[NMR谱学]] | 通过NMR数据判断反应是否按预期进行 | 直接 |
| [[Beckmann重排]] | 肟在酸性条件下的重排反应 | 直接 |
| Friedel-Crafts反应 | 碳正离子对芳环的亲电取代 | 间接 |
| D₂O交换 | 通过D₂O交换识别活泼H（OH/NH） | 间接 |

## 解题思路

1. **读题定位**：题目给出反应和产物NMR，要求判断为什么产物与预期不符——核心是比对预期和实际NMR
2. **🔑 关键转换**：预期产物A应有4个芳香H和1个NH，但实际只有3个芳香H和2个NH₂→说明发生了Beckmann碎片化而非重排→碎片化产生碳正离子→分子内Friedel-Crafts环化
3. **验证**：检查碎片化产物的NMR是否与实际数据一致（3个芳香H、2个可交换H、三个CH₂）

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 忽略D₂O交换信息 | 没有理解宽峰+D₂O交换的含义 | D₂O交换说明是活泼H（OH/NH），不是碳上的H | 如何通过D₂O交换区分OH和NH？ |
| 不注意芳香H数目 | 没有比对积分与预期 | 预期4个芳香H但只有3个，说明芳环被部分还原或取代模式改变 | Beckmann重排和碎片化的区别是什么？ |
| 跳过NMR验证直接猜测产物 | 没有用数据驱动的方法 | 应先从NMR数据推断结构，再解释反应机理 | 为什么Beckmann碎片化会产生NH₂？ |