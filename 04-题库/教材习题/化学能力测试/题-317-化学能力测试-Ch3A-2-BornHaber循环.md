---
title: 题-317-化学能力测试-Ch3A-2-Born-Haber循环估算键能
type: 题目
aliases:
  - Born-Haber 循环
source_subject: 化学竞赛能力测试·第3章A卷
submodule: Born-Haber 循环与键能
subject_module: 化学原理
exam_stage: 初赛
question_type:
  - 计算
  - 推断
difficulty: 4
teaching_level: 竞赛
fidelity: 原书逐字
knowledge_points:
  - "[[Born-Haber循环]]"
  - "[[电离能]]"
  - "[[电子亲和能]]"
  - "[[晶格能]]"
concepts:
  - "NaCl 解离能 = 键能 − (IE + EA) = 464 − (496−360) = 328 kJ/mol"
  - "CaCl₂ 解离能：2 个 Ca—Cl 键（键长缩短 9%）+ 排斥校正"
  - "计算得 CaCl₂ 解离能 = 630 kJ/mol"
pack: 模块习题集
tags:
  - 化竞
  - 教材习题
  - 化学能力测试
  - 第3章
created: 2026-09-03
updated: 2026-09-03
source: 化学竞赛能力测试·第3章 晶体结构初步知识·A卷第2题
source_file: "[[化学竞赛教程/（已压缩）化学竞赛能力测试]]"
status: 已填充
used_in: "[[综合模拟卷III]]"
source_category: 竞赛导向·竞赛教辅
source_grade: A
---

# Born-Haber 循环估算键能

> **来源**：化学竞赛能力测试·第3章·A卷第2题（10 分）

盐类及晶体可经由一系列的过程来估计其能量，其中包括了一种简单的离子模型。模型中，离子具有一特定的半径以及价数。离子的价数等于一个整数乘上该元素的价数。此模型可应用于描述离子分子在气态时的解离作用。此类解离作用通常会直接导致中性原子的生成，但是解离能的计算可由假设的反应途径来完成，该途径包括了自由离子的解离，以及离子的中和反应，这就是 Born-Haber 循环。

下列为一些双原子物质的键能、电子亲和能及解离能，它们均经测量过：

NaCl 键能 = −464 kJ·mol⁻¹；Cl 的电子亲和能 = −360 kJ·mol⁻¹；KCl 键能 = −423 kJ·mol⁻¹；Na 的电离能 = 496 kJ·mol⁻¹；MgCl 键能 = −406 kJ·mol⁻¹；Ca 的第一电离能 = 592 kJ·mol⁻¹；CaCl 键能 = −429 kJ·mol⁻¹；Ca 的第二电离能 = 1148 kJ·mol⁻¹。

**2-1** 对于氯化钠解离成中性原子设计一个 Born-Haber 循环，并且计算氯化钠的解离能。假设氯化钠是完全的离子键。

**2-2** 对于氯化钙解离成三个中性原子设计一个 Born-Haber 循环，并且计算其解离能。假设三原子分子的键长比双原子分子短 9%。

<details>
<summary>📖 查看答案与解析</summary>

**2-1** NaCl 解离为 Na + Cl 的 Born-Haber 循环为：

$$\mathrm{NaCl} \longrightarrow \mathrm{Na^+} + \mathrm{Cl^-}\quad(\text{吸收键能 } 464\ \mathrm{kJ\cdot mol^{-1}})$$

$$\mathrm{Na^+} + \mathrm{Cl^-} \longrightarrow \mathrm{Na} + \mathrm{Cl}\quad(\text{放出 } |IE_{\mathrm{Na}} + EA_{\mathrm{Cl}}| = |496 - 360| = 136\ \mathrm{kJ\cdot mol^{-1}})$$

解离能 = $464 - 136 = 328\ \mathrm{kJ\cdot mol^{-1}}$（NaCl 固体的键能理解为气态离子对能量）。

**2-2** CaCl₂ 解离成 Ca + 2Cl 的 Born-Haber 循环：

$$\mathrm{CaCl_2} \longrightarrow \mathrm{Ca^{2+}} + 2\mathrm{Cl^-}$$

$$\mathrm{Ca^{2+}} + 2\mathrm{Cl^-} \longrightarrow \mathrm{Ca} + 2\mathrm{Cl}$$

Ca²⁺Cl⁻ 的（离子）键能 $E = -429\times 2/0.91 = -943\ \mathrm{kJ\cdot mol^{-1}}$（CaCl 的测量值为 −429，但 Ca 的电荷现在为 +2，键长减小了 9%，即乘 1/0.91）。

第一步吸收能量 = CaCl₂ 键能 $= 2\times 943$ 减去 Cl—Cl 排斥能。Cl—Cl 排斥能为 $(429/2)\times(1/0.91) = 236\ \mathrm{kJ\cdot mol^{-1}}$，因此第一步吸收能量 $= 2\times943 - 236 = 1650\ \mathrm{kJ\cdot mol^{-1}}$。

第二步放出能量为 $-(2\times EA_{\mathrm{Cl}} + IE_1 + IE_2) = -(2\times360 + 592 + 1148) = -1020\ \mathrm{kJ\cdot mol^{-1}}$。

解离能 = $1650 - 1020 = 630\ \mathrm{kJ\cdot mol^{-1}}$。

</details>

## 知识点映射

| 知识点 | 体现 |
|--------|------|
| Born-Haber 循环 | 离子键 → 中性原子分步 |
| 电离能/电子亲和能 | IE(Na/Ca) + EA(Cl) |
| 键长修正 | CaCl₂ 键长 = CaCl × 0.91 |

<!-- 校勘注：①2-1 键能取正值参与计算（464 kJ/mol 为 NaCl 离子对生成能，解离吸收）；Na 的电离能 496 + Cl 的电子亲和 −360 = 净 136 kJ/mol 放出；②2-2 键长短 9% → 键长比 0.91，库仑能 ∝ 1/r → 键能 × 1/0.91；Ca²⁺ 电荷 2 倍 → 键能 × 2（每根 Ca—Cl 键）：每键 −429×2/0.91 = −943；③Cl—Cl 排斥能按 CaCl 中 1 根键的一半 ×1/0.91 校正：−236 kJ/mol 计入吸收项（扣除排斥）；④第二电离能需在第一步放出能量项中一并加总：2×360+592+1148 = 2460？不——放出 1020 是「Ca 电离 + 2Cl 亲和」反向：离子化需吸收 592+1148 = 1740，亲和放出 2×360 = 720，净吸收 1020 → 第二步"放出"为负值即吸收。总：第一步净解离（吸）1650 − 第二步中和净吸收 1020 = 630？令逻辑：解离能 = 键解离 1650（吸）+（IE 需吸 1740 但 EA 放 720）→ 1650 − 1020 = 630 kJ/mol ✓（答案如此，照录）。⑤源数据含 KCl/MgCl 未用（干扰项）。 -->
