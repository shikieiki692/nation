---
title: 题-537-Clayden-Ch18-P2-Bullatenone结构A预测NMR并纠正
type: 题目
fidelity: 原书逐字
submodule: 波谱综合解析
exam_stage: 决赛
subject: 有机化学
difficulty: 3
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[波谱综合解析]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch18-P2]
source: Clayden Organic Chemistry 2nd Ed. Chapter 18 Problem 2
cross_references: ["[[题-414-Clayden-Ch13-P1-五个化合物1H NMR信号和化学位移预测]]", "[[题-415-Clayden-Ch13-P2-酐加MeMgBr产物用IR 13C 1H NMR区分]]", "[[题-561-Clayden-Ch30-P2-不熟悉杂环合成和芳香性判断]]", "[[题-560-Clayden-Ch30-P1-吡咯并吡啶三环芳香杂环合成]]"]
module: 有机化学
status: 已填充
---
# 题-537: Bullatenone 结构A预测NMR并纠正

## 题目

The natural product bullatenone was isolated in the 1950s from a New Zealand myrtle and assigned the structure A. Then authentic compound A was synthesized and found not to be identical to natural bullatenone. Predict the expected ¹H NMR spectrum of A. Given the full spectroscopic data, not available in the 1950s, say why A is definitely wrong and suggest a better structure for bullatenone.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/5e07a8f97e825d9626dc2c4a767f1c82351404d81cd6f8e289234ad0b67fd0fd.jpg]]

Spectra of isolated bullatenone:

Mass spectrum: m/z 188 (10%) (high resolution confirms C₁₂H₁₂O₂), 105 (20%), 102 (100%), and 77 (20%)

Infrared: 1604 and 1705 cm⁻¹

¹H NMR: δH (ppm) 1.43 (6H, s), 5.82 (1H, s), 7.35 (3H, m), and 7.68 (2H, m).

**Purpose of the problem**: Detecting wrong structures teaches us to be alert to what the spectra are telling us rather than what we expect or want.

## 参考答案

**Answer (English)**: The mass spectrum and IR are all right for A but the NMR shows at once that the structure is wrong. There is a monosubstituted benzene ring all right, but the aliphatic protons are a 6H singlet, presumably a CMe₂ group, and a 1H singlet in the alkene region at 5.82 ppm.

The fragments we have are Ph, carbonyl, a CMe₂ group, and an alkene with one proton on it. That adds up to C₁₂H₁₂O leaving only one oxygen to fit in somewhere. There must still be a ring or there would not be enough hydrogen atoms and the ring must be five-membered (just try other possibilities yourself). There are three ring systems we can choose and each can have the Ph group at either end of the alkene, making six possibilities in all.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/b987ce591318df6888921741fcb8eae5ca8f54ece4eae33d03cd70067684e052.jpg]]

The last four are esters (cyclic esters or lactones) and they would have a C=O frequency at 1745–1780 cm⁻¹ so D–G are all wrong. The hydrogen on the alkene cannot be next to oxygen as it would have a very large chemical shift indeed whereas it is close to the 'normal' alkene shift of 5.25 ruling out structure C. Structure B is correct and the spectrum can be assigned. Compound B has now been synthesized and proved identical to natural bullatenone.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/0371787ea97a55d5c4090a3d151f9353d7dddb7b9f82700386eae0bb21821ad5.jpg]]

**中文解析**：

关键解析步骤：

1. **验证结构 A 的问题**：结构 A 含有两个 CH₃ 和一个烯烃 CH₂（=CH₂），预测 ¹H NMR 应有：两个不同的 CH₃（非等价）和两个烯烃质子（各约 5 ppm，有偕偶合）。但实际谱图只显示一个 6H 单峰（等价的 CMe₂）和一个 1H 单峰（烯烃上只有一个 H），与 A 完全不符
2. **碎片组装**：Ph + C=O + CMe₂ + =CH → 总计 C₁₂H₁₂O，仅剩一个 O 需要安置 → 必须成环（否则 H 数不够），且为五元环
3. **排除法**：
   - D–G 为环酯（内酯），C=O 应在 1745–1780 cm⁻¹，但 IR 显示 1705 cm⁻¹ → 排除
   - C 中烯烃 H 与 O 相连（烯醇醚），化学位移应 >> 6 ppm，但实际 5.82 ppm → 排除
   - **B（二氢苯并呋喃酮）** 完美匹配所有数据

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[波谱综合解析]] | 从 NMR 数据反驳已知结构并推导正确结构 | 直接 |
| [[NMR谱学]] | 化学位移判断烯烃 H 的位置（是否邻氧） | 直接 |
| [[IR光谱]] | C=O 伸缩频率区分酮（1705）与内酯（1745–1780） | 直接 |
| [[天然产物化学]] | 天然产物结构修正的历史案例 | 间接 |

## 解题思路

1. **读题定位**：题目要求先预测结构 A 的 NMR，再用实际数据否定 A，最后提出正确结构
2. **🔑 关键转换**：IR 1705 cm⁻¹ → 非共轭酮（排除内酯 1745+）；¹H NMR 只有一个烯烃 H（5.82 ppm, s）→ =CH 而非 =CH₂；6H 单峰 → CMe₂（对称）
3. **验证**：结构 B（3,3-二甲基-2-苯基-2,3-二氢苯并呋喃-4-酮）的所有 NMR 信号均与实验数据一致

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 接受结构 A 不加验证 | 相信原始文献不质疑 | 合成的"标准品"与天然物不一致说明结构有误 | 如何用 NMR 快速判断 A 是否正确？ |
| 将 5.82 ppm 信号归属为 =CH₂ | 未注意 =CH₂ 应有两个质子且有偕偶合 | 5.82 ppm 是单峰（1H）→ =CH 上只有一个质子 | =CH₂ 的两个 H 在 NMR 中应如何表现？ |
| 选结构 C（烯醇醚） | 忽略化学位移判断 | 烯烃 H 直接连在 O 上时 δ > 6 ppm，5.82 ppm 不支持 | 烯醇醚的 ¹H NMR 特征是什么？ |