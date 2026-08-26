---
title: "题-有机-羰基-交叉Aldol缩合产物预测"
type: 题目
fidelity: 原书逐字
submodule: 羰基化学与缩合反应
exam_stage: 初赛
subject: 有机化学
difficulty: 4
teaching_level: 强化
syllabus_codes: ["42"]
knowledge_points: ["[[Aldol缩合]]", "[[羰基亲核加成]]"]
tags: [化竞, 题目, 有机化学, 第三轮]
updated: 2026-06-06
aliases: ["题-有机-羰基-01"]
source: "专题页提炼"
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 模块习题集
---
# 交叉 Aldol 缩合产物预测

## 题目

苯甲醛（$\mathrm{C_6H_5CHO}$）与丙酮（$\mathrm{CH_3COCH_3}$）在 $\mathrm{NaOH / H_2O}$ 中反应。

**(1)** 写出交叉 Aldol 缩合的主产物，并说明原因。

**(2)** 写出完整的反应机理（用箭头推电子法）。

**(3)** 如果使用苯乙酮（$\mathrm{C_6H_5COCH_3}$）代替丙酮，产物是什么？为什么？

**(4)** 如果使用过量的丙酮（如 3 当量）在 NaOH 中与 1 当量苯甲醛反应，产物是否相同？为什么？


![[base-catalysed-aldol.svg]]

## 参考答案

### (1) 主产物

交叉 Aldol 缩合的主产物是**二亚苄基丙酮**（dibenzalacetone，即 1,5-二苯基-1,4-戊二烯-3-酮）：

$$
\mathrm{C_6H_5CH\!=\!CHCOCH\!=\!CHC_6H_5}
$$

结构：苯环—CH=CH—C(=O)—CH=CH—苯环，两端均为 E 构型（反式）。

### 反应机理

**第一步：丙酮的去质子化（形成烯醇负离子）**

丙酮的 $\alpha$-H 的 $\mathrm{p}K_\mathrm{a} \approx 20$，在 NaOH 中部分去质子化形成烯醇负离子：

$$
\mathrm{CH_3COCH_3 + OH^- \rightleftharpoons {}^-CH_2COCH_3 + H_2O}
$$

（注意：苯甲醛**没有** $\alpha$-H，不能自缩合形成烯醇负离子。这是交叉 Aldol 成功的关键！）

**第二步：Aldol 加成**

烯醇负离子亲核进攻苯甲醛的羰基碳：

$$
\mathrm{PhCHO + {}^-CH_2COCH_3 \longrightarrow PhCH(O^-)CH_2COCH_3}
$$

**第三步：脱水**

碱催化下 $\beta$-羟基酮脱水，生成 $\alpha,\beta$-不饱和酮（脱水产物因共轭稳定而自发进行）：

$$
\mathrm{PhCH(O^-)CH_2COCH_3 \xrightarrow{OH^-,\;-H_2O} PhCH\!=\!CHCOCH_3}
$$

产物为亚苄基丙酮（benzalacetone，即 4-苯基-3-丁烯-2-酮）。

**第四步：第二次 Aldol 缩合**

亚苄基丙酮仍有一个 $\alpha$-甲基（与羰基相邻），在过量 NaOH 中继续去质子化：

$$
\mathrm{PhCH\!=\!CHCOCH_3 + OH^- \rightleftharpoons PhCH\!=\!CHCO{}^-CH_2 + H_2O}
$$

新的烯醇负离子进攻第二分子苯甲醛：

$$
\mathrm{PhCH\!=\!CHCO{}^-CH_2 + PhCHO \longrightarrow PhCH\!=\!CHCOCH_2CH(O^-)Ph}
$$

再次脱水：

$$
\mathrm{\xrightarrow{OH^-,\;-H_2O} PhCH\!=\!CHCOCH\!=\!CHPh}
$$

最终产物为二亚苄基丙酮（对称的 $\alpha,\beta$-不饱和酮，共轭体系贯穿整个分子）。

### (2) 反应成功的条件

**关键原因：苯甲醛没有 $\alpha$-H**。这意味着苯甲醛不能自身缩合（无法形成烯醇负离子），只能作为**亲电受体**被丙酮的烯醇负离子进攻。这是交叉 Aldol 缩合取得单一产物的经典策略：

- 一个组分有 $\alpha$-H（提供烯醇负离子，亲核组分）
- 另一个组分没有 $\alpha$-H（仅作为亲电受体）

其他常见的无 $\alpha$-H 醛：甲醛（$\mathrm{HCHO}$）、苯甲醛（$\mathrm{PhCHO}$）、糠醛等芳香醛。

### (3) 使用苯乙酮代替丙酮

苯乙酮 $\mathrm{PhCOCH_3}$ 仍然有 $\alpha$-H（甲基），可以形成烯醇负离子：

$$
\mathrm{PhCOCH_3 + OH^- \rightleftharpoons PhCO{}^-CH_2 + H_2O}
$$

苯乙酮的烯醇负离子进攻苯甲醛，经 Aldol 加成和脱水：

$$
\mathrm{PhCO{}^-CH_2 + PhCHO \longrightarrow PhCOCH_2CH(O^-)Ph \xrightarrow{-H_2O} PhCOCH\!=\!CHPh}
$$

产物为查耳酮（chalcone，即亚苄基苯乙酮，1,3-二苯基-2-丙烯-1-酮）。

只能发生**一次** Aldol 缩合，因为查耳酮的 $\alpha$-亚甲基已与苯环共轭，活性降低，且该亚甲基与羰基相邻的一侧被苯环取代，另一侧与双键相连，不易进一步去质子化。此外，苯乙酮也只有一个 $\alpha$-甲基。

**与丙酮的区别**：丙酮有两个 $\alpha$-甲基（可发生两次缩合），苯乙酮只有一个 $\alpha$-甲基（只能发生一次缩合）。

### (4) 过量丙酮 + 1 当量苯甲醛

当丙酮远过量时（如 3 当量），产物以**单缩合产物**亚苄基丙酮（$\mathrm{PhCH=CHCOCH_3}$）为主。

原因：过量丙酮的存在使得第一个 Aldol 产物（亚苄基丙酮）的浓度始终较低，第二个 Aldol 反应（需要第二分子苯甲醛与亚苄基丙酮缩合）被抑制。亚苄基丙酮的烯醇负离子更倾向于与大量存在的丙酮质子交换，而非进攻苯甲醛。

因此，控制**化学计量比**可以有效调控单缩合 vs 双缩合：

- 苯甲醛 : 丙酮 ≈ 2:1 → 双缩合产物（二亚苄基丙酮）
- 苯甲醛 : 丙酮 ≪ 1 → 单缩合产物（亚苄基丙酮）

## 知识点映射

- [[Aldol缩合]]
- [[羰基亲核加成]]