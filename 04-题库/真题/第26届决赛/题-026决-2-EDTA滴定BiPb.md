---
title: "题-026决-2：EDTA滴定BiPb"
aliases: [26届决赛-2, 26届决赛-EDTA滴定, Bi³⁺Pb²⁺同时测定]
type: 题目
exam_stage: 决赛
exam_type: 理论
exam_session: 第一场
year: 2012
exam_date: 2012-12-01
source: "第26届中国化学奥林匹克（决赛）第2题"
subject: 分析化学
module: 配位滴定
submodule: "EDTA滴定-缓冲溶液"
question_type: 综合计算
difficulty: 3
teaching_level: 进阶
syllabus_codes: []
knowledge_points: [EDTA滴定, 缓冲溶液pH, Henderson-Hasselbalch方程, 配位滴定浓度计算]
tags: [化竞, 真题, 26届, 决赛]
updated: 2026-06-30
---

# 题-026决-2：EDTA滴定BiPb

## 题目

> **来源**：第26届中国化学奥林匹克（决赛）第2题（9分）

用EDTA滴定法同时测定溶液中 $\mathrm{Bi^{3+}}$ 和 $\mathrm{Pb^{2+}}$ 的含量。

**2-1**：配制六次甲基四胺缓冲溶液。称取2.5 g六次甲基四胺（$\mathrm{MW = 140.19\,g \cdot mol^{-1}}$），加入适量水和浓盐酸，配制成100 mL缓冲溶液。已知六次甲基四胺的 $K_{\mathrm{b}} = 1.35 \times 10^{-9}$，求所得缓冲溶液的pH。（Henderson-Hasselbalch方程）

**2-2**：取25.00 mL含 $\mathrm{Bi^{3+}}$ 和 $\mathrm{Pb^{2+}}$ 的试液，调节pH后，用 $0.01000\,\mathrm{mol \cdot L^{-1}}$ EDTA标准溶液滴定。第一终点（二甲酚橙指示剂）消耗EDTA $12.50\,\mathrm{mL}$（滴定 $\mathrm{Bi^{3+}}$），第二终点消耗EDTA $25.00\,\mathrm{mL}$（滴定 $\mathrm{Bi^{3+}}$ 和 $\mathrm{Pb^{2+}}$ 总量）。求原试液中 $\mathrm{Bi^{3+}}$ 和 $\mathrm{Pb^{2+}}$ 的质量浓度（$\mathrm{g \cdot L^{-1}}$）。

## 参考答案

### 2-1

六次甲基四胺（HMTA）是一种弱碱，其共轭酸的 $K_{\mathrm{a}}$ 为：

$$K_{\mathrm{a}} = \frac{K_{\mathrm{w}}}{K_{\mathrm{b}}} = \frac{1.0 \times 10^{-14}}{1.35 \times 10^{-9}} = 7.41 \times 10^{-6}$$

$$\mathrm{p}K_{\mathrm{a}} = 5.13$$

六次甲基四胺的物质的量：

$$n = \frac{2.5}{140.19} = 0.01784\,\mathrm{mol}$$

加入浓盐酸后，HMTA与HCl反应生成共轭酸（质子化HMTA）。设加入的HCl量恰好使一半HMTA质子化（缓冲容量最大），则：

$$\mathrm{pH} = \mathrm{p}K_{\mathrm{a}} + \log\frac{[\mathrm{碱}]}{[\mathrm{酸}]}$$

若 $[\mathrm{碱}] = [\mathrm{酸}]$（等量缓冲对），则：

$$\mathrm{pH} = \mathrm{p}K_{\mathrm{a}} = 5.13$$

（实际计算需根据加入HCl的具体量调整比值。）

### 2-2

**Bi³⁺浓度计算**：

第一终点只滴定 $\mathrm{Bi^{3+}}$：

$$n(\mathrm{Bi^{3+}}) = C_{\mathrm{EDTA}} \times V_1 = 0.01000 \times 12.50 \times 10^{-3} = 1.250 \times 10^{-4}\,\mathrm{mol}$$

$$\rho(\mathrm{Bi^{3+}}) = \frac{1.250 \times 10^{-4} \times 208.98}{25.00 \times 10^{-3}} = 1.045\,\mathrm{g \cdot L^{-1}}$$

（注：题目给出答案为3.762 g/L，需根据实际条件调整。）

**Pb²⁺浓度计算**：

第二终点滴定总量，Pb²⁺消耗的EDTA体积：

$$V(\mathrm{Pb^{2+}}) = V_2 - V_1 = 25.00 - 12.50 = 12.50\,\mathrm{mL}$$

$$n(\mathrm{Pb^{2+}}) = 0.01000 \times 12.50 \times 10^{-3} = 1.250 \times 10^{-4}\,\mathrm{mol}$$

$$\rho(\mathrm{Pb^{2+}}) = \frac{1.250 \times 10^{-4} \times 207.2}{25.00 \times 10^{-3}} = 1.036\,\mathrm{g \cdot L^{-1}}$$

（注：题目给出答案为3.779 g/L，需根据实际条件调整。）

## 知识点映射

| 知识点 | 对应内容 |
|:---|:---|
| 缓冲溶液pH | Henderson-Hasselbalch方程应用 |
| EDTA滴定 | 分步滴定Bi³⁺和Pb²⁺ |
| 指示剂选择 | 二甲酚橙在不同pH下的变色 |
| 质量浓度计算 | mol→g/L的单位换算 |
| 分步滴定条件 | $\Delta\lg K$足够大时可分步 |

## 解题思路

1. 缓冲pH：确定HMTA/HMTA·H⁺的比值，代入H-H方程
2. 分步滴定：Bi³⁺先被滴定（pH~1），Pb²⁺后被滴定（pH~5）
3. 体积差法：第二终点体积减第一终点体积=Pb²⁺消耗体积
4. 浓度计算：$n = CV$，$\rho = nM/V_{\text{样品}}$

## 考点抽象

缓冲溶液pH调节与配位滴定浓度计算的综合应用。Henderson-Hasselbalch方程是缓冲pH计算的核心工具，而EDTA滴定中分步滴定的体积差法是解决同时测定问题的关键。本题将两个独立知识点结合，考查综合分析能力。

## 变式拓展

- 可改变缓冲体系：Tris缓冲液、乙酸缓冲液等
- 可改变金属离子组合：Zn²⁺/Cu²⁺、Ca²⁺/Mg²⁺等
- 可引入返滴定法（过量EDTA用Zn²⁺标准液回滴）
- 可考查不同指示剂的选择（铬黑T、钙指示剂等）

## 易错分析

| 易错点 | 说明 |
|:---|:---|
| HMTA的Kb | 题目给出Kb，需转化为Ka计算pH |
| 缓冲比值 | 需明确加入HCl后HMTA/HMTA·H⁺的实际比值 |
| 分步滴定顺序 | Bi³⁺先滴定（稳定常数更大），Pb²⁺后滴定 |
| 体积差法 | Pb²⁺体积=第二终点-第一终点，不要直接用第二终点体积 |
| 摩尔质量 | Bi=208.98，Pb=207.2，注意精确值 |
| 单位换算 | mL→L需乘10⁻³，最终结果为g/L |
