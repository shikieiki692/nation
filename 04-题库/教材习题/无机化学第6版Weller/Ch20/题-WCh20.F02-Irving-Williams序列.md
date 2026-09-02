---
title: "题-WCh20.F02-Irving-Williams序列"
type: 题目
source: "无机化学第6版Weller Ch20 辅导性作业20.2"
source_file: "06-外部资料导入/无机化学Weller/无机化学第6版Welle19-21章.md"
source_subject: 无机和结构化学
year: 2023
difficulty: 4
teaching_level: 拓展
knowledge_points: ["[[配位化学]]", "[[晶体场理论]]"]
status: 已补全答案
tags: [化竞, 无机化学, Weller, 晶体场理论]
created: 2026-08-27
updated: 2026-08-30
subject_module: 结构化学
pack: 模块习题集
fidelity: 原书逐字
exam_stage: 初赛
used_in: "[[结构化学阶段测试卷]]"
---

# Irving-Williams序列

> **来源**：无机化学第6版（Weller等著，中文版）Ch20 辅导性作业20.2
> **难度**：⭐⭐⭐⭐

## 题目

在辅导性作业 7.12 中我们看到了三种不同金属与 1,2-乙二胺形成络合物的逐级形成常数。用相同的数据讨论金属对形成常数的影响。如何利用 Irving-Williams 序列理解这些形成常数？

## 参考答案

乙二胺是中性双齿配体，置换水分子形成螯合物时提供的配体场比水强，因此 LFSE 对络合物稳定性的贡献比水合络合物更显著。若三种金属均为第一过渡系 $M^{2+}$，其逐级形成常数的大小应直接按 Irving-Williams 序列排序：

$$
\mathrm{Mn^{2+}} < \mathrm{Fe^{2+}} < \mathrm{Co^{2+}} < \mathrm{Ni^{2+}} < \mathrm{Cu^{2+}} > \mathrm{Zn^{2+}}
$$

### 1. 静电基线

同一周期从左到右离子半径减小、电荷密度增大，金属与乙二胺 N 原子的静电吸引增强，形成常数相应增大。这一反相关关系构成了序列上升的基线。

### 2. LFSE 叠加

相对于水合离子，乙二胺配体使 $d^6$ 至 $d^9$ 离子的额外 LFSE 明显增强。高自旋八面体组态的 CFSE 为：

- $Fe(II)$（$d^6$）：$-0.4\Delta_o$
- $Co(II)$（$d^7$）：$-0.8\Delta_o$
- $Ni(II)$（$d^8$）：$-1.2\Delta_o$
- $Cu(II)$（$d^9$）：$-0.6\Delta_o$

因此 $Co$、$Ni$、$Cu$ 的形成常数显著高于纯静电估计；$Mn(II)$ 的 $d^5$ 高自旋组态 CFSE 为零，不获得额外稳定化。

### 3. 两个例外

$Cu(II)$ 虽然比 $Ni(II)$ 多一个反键 $e_g$ 电子，形成常数反而最大，这是因为 Jahn-Teller 效应使 $Cu(II)$ 发生四方畸变，处于同一平面上的四个配体结合力增强，额外稳定化补偿了反键电子的不利影响。$Zn(II)$ 既无 LFSE 也无 Jahn-Teller 增强，故其形成常数高于 $Mn(II)$、$Fe(II)$，但低于 $Co(II)$、$Ni(II)$、$Cu(II)$。

将辅导性作业 7.12 中三种金属的逐级形成常数按上述位置排列即可：若三种金属落在 $Mn$ 至 $Zn$ 区间内，由早过渡到晚过渡金属逐级增大；若其中包含 $Cu(II)$，它应位于峰值；若包含 $Zn(II)$，它应低于 $Co/Ni/Cu$。
