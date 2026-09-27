---
title: "题-UChO-10thZCHEM-UChO-06-DNA是一种由核苷酸组成的长"
aliases: ["题-UChO-10thZCHEM-UChO-06"]
type: 题目
fidelity: 原书逐字
difficulty: 4
teaching_level: 竞赛
source: "质心UChO 10thZCHEM-UChO 第 6 题"
module: "2026机构初赛模拟题"
source_subject: 化学原理
syllabus_codes: []
knowledge_points: []
tags: [化竞, 题目, 初赛, 机构模拟题, 质心UChO]
updated: 2026-09-26
status: 已填充
exam_stage: 初赛
subject_module: 化学原理
pack: 综合模拟卷
submodule: 质心UChO
source_category: 竞赛导向·竞赛教辅
source_grade: A
source_norm: "质心UChO-10thZCHEM-UChO"
source_file: "2026机构初赛模拟题/02-质心UChO/10thZCHEM-UChO.md"
---

# 题-UChO-10thZCHEM-UChO-06-DNA是一种由核苷酸组成的长

## 题目

### 第 6 题 DNA computing(占 11%)

DNA 是一种由核苷酸组成的长链聚合物，由两条核苷酸链通过碱基互补配对组成。脱氧核糖核苷酸的基本结构如下：

![](images/39058abf84cdae53dd44539755bef7831093ae55c5bc9433ffbe5d310a060c53.jpg)

其中 Base 代表碱基 A/T/G/C， $O_{1}$ 代表前一个脱氧核糖核苷酸羟基的氧原子， $P_{2}$ 代表后一个脱氧核糖核苷酸的磷原子，数字为五碳糖的碳原子编号。

6-1 解释为何 DNA 在生理条件下通常带负电。

6-2 如果在 DNA 合成过程中混入了核糖核苷酸可能会有什么影响？

6-3 假定 DNA 双链解螺旋为配对的直线链需要的能量为 $E_{1}$ ，DNA 双链解开为两条单链的需要的能量为 $E_{2}$ ，则 $E_{1}$ 与 $E_{2}$ 的大小关系是怎样的（ $E_{2} > E_{1}$ 、 $E_{2} < E_{1}$ 或不好确定）？为什么？

6-4 DNA 解链温度/融解温度 $T_{m}$ 是评估 DNA 稳定性的重要参数，其定义为当 50% DNA 解开为单链的温度，为了较准确的根据序列计算 DNA 的 $T_{m}$ ，Donald Hicks 提出了一个最近邻模型来描述 DNA 形成双链的热力学参数如下

<table><tr><td>最近邻碱基对 (5'→3')</td><td> $\Delta H^{\circ}$ (kJ mol $^{-1}$ )</td><td> $\Delta S^{\circ}$ (J K $^{-1}$  mol $^{-1}$ )</td></tr><tr><td>AA/TT</td><td>-31.80</td><td>-89.12</td></tr><tr><td>AT/TA</td><td>-30.12</td><td>-85.35</td></tr><tr><td>TA/AT</td><td>-30.12</td><td>-89.12</td></tr><tr><td>CA/GT</td><td>-35.56</td><td>-94.97</td></tr><tr><td>GT/CA</td><td>-35.15</td><td>-93.72</td></tr><tr><td>CT/GA</td><td>-32.64</td><td>-87.86</td></tr><tr><td>GA/CT</td><td>-34.31</td><td>-92.89</td></tr><tr><td>CG/GC</td><td>-44.35</td><td>-113.80</td></tr><tr><td>GC/CG</td><td>-41.00</td><td>-102.09</td></tr><tr><td>GG/CC</td><td>-33.47</td><td>-83.26</td></tr><tr><td>Initiation correction</td><td>+0.84</td><td>-23.85</td></tr><tr><td>Terminal A/T correction</td><td>+9.20</td><td>+28.87</td></tr><tr><td>Symmetry correction</td><td>0.00</td><td>-5.86</td></tr></table>

其中 Initiation correction 用于校正起始端，Terminal correction 用于校正链末端为 A/T 配对的情况，Symmetry correction 用于校正单链 DNA 解折叠，对于如下两条配对的 DNA 链，假定两条链的总浓度为 2.00 μM，计算 $T_{m}$

$\mathrm{S}_{1}$ 链： $5^{\prime}-$ [FAM] - TCT AGC TTA GGT CAG - (a) $-3^{\prime}$

$S_{2}$ 链：5'-TTA GGC CCT GAC CTA AGC - (b) - [DABCYL] -3'

其中FAM和DABCYL是两端两个取代的小分子，本题中不用考虑其影响，a、b处的空缺请根据碱基互补配对原则进行填充。

6-5 在上述序列中，FAM 是荧光素，是一个荧光基团，DABCYL 是一个荧光淬灭基团。对 $S_{1}-S_{2}$ 配对链（称为 G）测定了荧光强度，发现 37 度下荧光很弱，加热到 90 度则荧光较强，请根据你了解的荧光光谱知识解释原因。（提示：DABCYL 被光激发时的荧光很弱）

6-6 现在有 A、B 两条单链 DNA，如果在 37 度将 G、A、B 混合，会发现有荧光，这是为什么？
6-7 对 G、A、B 混合体系的研究表明里面发生了如下反应，r 为生成 P 的速率，G 浓度固定为 50.0 nM $G+A \rightarrow I$ (对应 $k_{1}$ ， $k_{-1}$ )

$I+B \rightarrow P$ (对应 $k_{2}$ )

<table><tr><td>实验编号</td><td> $[A]_0/nm$ </td><td> $[B]_0/nm$ </td><td> $r_0/nm s^{-1}$ </td></tr><tr><td>1</td><td>500.0</td><td>500.0</td><td>0.227</td></tr><tr><td>2</td><td>1000.0</td><td>500.0</td><td>0.455</td></tr><tr><td>3</td><td>500.0</td><td>1000.0</td><td>0.241</td></tr></table>

6-7-1 根据表中数据，尝试推导生成 P 的速率方程。

6-7-2 根据上表数据是否可以计算 $k_{1}$ 、 $k_{-1}$ 、 $k_{2}$ ？如不能，计算其中可以计算的。

6-8 实际上 A 和 B 是癌症的肿瘤标志物，而 G 就是被设计用来检测 A 和 B 的，假定此时存在一个单碱基突变的单链 DNA 为 A'，37 度下 A 与 G 的结合自由能变分别为 -40.0 kJ mol $^{-1}$ ，A' 与 G 的结合自由能变分别为 -28.0 kJ mol $^{-1}$ ，假定现在有一个被污染的样品，存在 1.0 nM G、50.0 nM A 和 500 nM A'，计算平衡后 G-A' 占 G-A 和 G-A' 总的浓度的百分比。

## 参考答案

⛔ 答案缺失（源答案文件未含该题号，需人工补）

## 知识点映射

- （待人工校准）


> ⚠️ **自动拆卡标记**：`subject_module`/`difficulty` 为关键词粗判，答案数值与单位**尚未经人工复核**（OCR 原文逐字转录，可能保留原卷笔误）。