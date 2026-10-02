---
title: "题-XeC-18-06-逻辑门LogicGates是"
aliases: ["题-XeC-18-06"]
type: 题目
fidelity: 原书逐字
difficulty: 4
teaching_level: 竞赛
source: "XeChem 第40届初赛模拟试题（18）第 6 题"
module: "2026机构初赛模拟题"
source_subject: 化学原理
syllabus_codes: [56, 10]
knowledge_points:
  - "[[超分子基础]]"
  - "[[有机光化学]]"
tags: [化竞, 题目, 初赛, 机构模拟题, XeChem]
updated: 2026-09-26
status: 已填充
exam_stage: 初赛
subject_module: 化学原理
pack: 综合模拟卷
submodule: XeChem
source_category: 竞赛导向·竞赛教辅
source_grade: A
source_tier: 2
source_norm: "XeChem-18"
source_file: "2026机构初赛模拟题/03-XeChem/（已压缩）PDF合并_1-199.md"
---

# 题-XeC-18-06-逻辑门LogicGates是

## 题目

### 第 6 题0100100001001001……（15分，占 $7\%$ ）

逻辑门（Logic Gates）是电路通信中的一个非常基础的概念。不同的逻辑门可以控制不同的输入与输出情况，以此达到进行逻辑运算的目的，下面是一些输入一个或者两个信号的逻辑门运算的结论表格，其中“1”表示该路导通，“0”表示该路关闭。

<table><tr><td>逻辑门</td><td>符号</td><td>输入</td><td>输出</td></tr><tr><td rowspan="2">与门</td><td rowspan="2">AND</td><td>两个信号均为1</td><td>1</td></tr><tr><td>其他</td><td>0</td></tr><tr><td rowspan="2">或门</td><td rowspan="2">OR</td><td>两个信号均为0</td><td>0</td></tr><tr><td>其他</td><td>1</td></tr><tr><td rowspan="2">非门(只输入一个信号)</td><td rowspan="2">NOT</td><td>1</td><td>0</td></tr><tr><td>0</td><td>1</td></tr><tr><td rowspan="2">与非门</td><td rowspan="2">NAND</td><td>两个信号均为1</td><td>0</td></tr><tr><td>其他</td><td>1</td></tr><tr><td rowspan="2">或非门</td><td rowspan="2">NOR</td><td>两个信号均为0</td><td>1</td></tr><tr><td>其他</td><td>0</td></tr><tr><td rowspan="2">异或门</td><td rowspan="2">XOR</td><td>输入的两个信号相同</td><td>0</td></tr><tr><td>输入的两个信号不同</td><td>1</td></tr><tr><td rowspan="2">同或门</td><td rowspan="2">XNOR</td><td>输入的两个信号相同</td><td>1</td></tr><tr><td>输入的两个信号不同</td><td>0</td></tr></table>

传统的逻辑门通常采用电流作为信号导入导出的媒介。但是总会有一些思路清奇的化学家去思考：这样有用的东西，能不能应用在分子层面上呢？

2000 年, 第一个分子逻辑门由 Silva 课题组制得, 其使用 $\mathrm{Ca}^{2+}$ 与 $\mathrm{H}^{+}$ 作为信号输入源 (记加入某一物质为“01”, 不加入某一物质为“00”), 通过调节受体分子的结构从而达到输出不同光强的目的, 如下是 Silva 制备出的两种不同的分子逻辑门:

![](images/427795230907742718cb863c86dfa6a047df99992eee171bcbcd6be335f148f1.jpg)  
二者分别对应的吸收光谱与荧光发射光谱如下:

![](images/df4a965734e83c90283a01f430735495b7b09ebfa2a0d186729cea22b88944f6.jpg)

![](images/d66c100cf1ee64927170740d3b6104f2b49102b09018ff9d7c03308c01aa3fa3.jpg)

其中左侧为 A 的吸收光谱，右侧为 B 的荧光发射光谱，其中 A 表示吸光度， $I_{F}$ 为荧光发光光强。

6- 1- 1 指出 A 结合 $Ca^{2+}$ 与 $H^{+}$ 的位点，需要表示出所有的配位原子与配位原子个数。

6-1-2 以 $390 \mathrm{~nm}$ 处的吸光度 A 为标准（即存在吸光为“1”、不存在吸光为“0”），指出 A 的逻辑门符号（该种输出方式记作输出方式 I）。

6-1-3 以 $390 \mathrm{~nm}$ 处的透光率 I 为标准（即光透过为“1”、不透光为“0”），指出 A 的逻辑门符号（该种输出方式记作输出方式 II）。

6-1-4 以 $419 \mathrm{~nm}$ 处荧光光强 $\mathrm{I}_{\mathrm{F}}$ 为标准（即发生荧光为“1”、不发生荧光为“0”），指出 B 的逻辑门符号。

通过如上两种分子, 可以通过调控 $\mathrm{Ca}^{2+}$ 与 $\mathrm{H}^{+}$ 的加入情况, 完成简单的二进制加法。向 $\mathbf{A}$ 与 $\mathbf{B}$ 的溶液中分别加入需要输入的字符所代表的溶液 (例如输入“01+01”, 则需要分别向 $\mathbf{A}$ 与 $\mathbf{B}$ 的溶液中同时加入 $\mathrm{H}^{+}$ 与 $\mathrm{Ca}^{2+}$ 溶液, 输入“01+00”则只需要分别向 $\mathbf{A}$ 与 $\mathbf{B}$ 的溶液中加入 $\mathrm{H}^{+}$ 或 $\mathrm{Ca}^{2+}$ 溶液即可), 两份溶液的结果将用来表示输出字符的两位。

6-2-1 用二进制表示 $(01)_2 + (01)_2$ 的计算结果（提示：二进制中的3可以表示为 $(11)_2$ ）。

6-2-2 若想使该加法计算器成立:

6-2-2-1 指出 A 与 B 的溶液哪个代表高位哪个代表低位（提示： $(10)_{2}$ 中 1 代表高位，0 代表低位）

6-2-2-2 指出 A 的溶液输出方式为输出方式 I 还是输出方式 II。

## 参考答案

⛔ 答案缺失（源合并本未含该题号，需人工补）

## 知识点映射

- （待人工校准）


> ⚠️ **自动拆卡标记**：`subject_module`/`difficulty` 为关键词粗判，答案数值与单位**尚未经人工复核**。