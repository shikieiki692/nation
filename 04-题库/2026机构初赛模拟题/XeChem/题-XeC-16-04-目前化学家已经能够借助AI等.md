---
title: "题-XeC-16-04-目前化学家已经能够借助AI等"
aliases: ["题-XeC-16-04"]
type: 题目
fidelity: 原书逐字
difficulty: 4
teaching_level: 竞赛
source: "XeChem 第40届初赛模拟试题（16）第 4 题"
module: "2026机构初赛模拟题"
source_subject: 化学原理
syllabus_codes: [55, 56]
knowledge_points:
  - "[[高分子化学]]"
  - "[[超分子基础]]"
  - "[[化学平衡]]"
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
source_norm: "XeChem-16"
source_file: "2026机构初赛模拟题/03-XeChem/（已压缩）PDF合并_1-199.md"
---

# 题-XeC-16-04-目前化学家已经能够借助AI等

## 题目

### 第 4 题 药物递送高分子（22 分，占 11%）

目前,化学家已经能够借助 AI 等手段从细胞和分子水平针对性地进行药物设计,然而,缺乏合适的递送手段成为药物化学中新的瓶颈。对于疏水药物而言,设计合适的递送手段则尤为重要,因为其水溶液的极低浓度使得药物很难达到生理上有效的浓度。借助嵌段共聚物与药物分子形成胶束,可以有效提升药物的溶解度。有研究人员针对紫杉醇(记作 M, $M=854\ \text{g/mol}$ ,在水中溶解度仅为 $6.7\ \text{mg/L}$ )设计了一种嵌段共聚物 P 用于递送 M,其载药量

LC 达到了 45%。 $(LC = m_{\text{drug}}/(m_{\text{drug}} + m_{\text{polymer}}))$ 。

$$
\mathrm{HO} \xrightarrow {\text { RCN }} \mathrm{A1} \sim \mathrm{A3}
$$

$$
\mathrm{A1:} \mathrm{R} = \mathrm{Me} \quad \mathrm{A2:} \mathrm{R} = n - \mathrm{Bu} \quad \mathrm{A3:} \mathrm{R} = \mathrm{Bn}
$$

$$
\mathrm{A1} \xrightarrow [ (0.17 \mathrm{mol}) ]{\text { TsOMe } (0.93 \mathrm{g})} \mathrm{P1} \xrightarrow [ \mathrm{A3} (0.025 \mathrm{mol}) ]{\mathrm{A2} (0.065 \mathrm{mol})} \mathrm{P2} \xrightarrow [ \mathrm{A1} (0.17 \mathrm{mol}) ]{\mathrm{A1} (0.17 \mathrm{mol})} \mathrm{P3} \xrightarrow [ \mathrm{NH} ]{\text { }} \mathrm{P}
$$

4-1-1 画出嵌段共聚物 P 的结构(不同的烷基统一用 R 表示即可), 并计算各嵌段的聚合度。每步增长的高分子链视作一个嵌段

提示：TsOMe 是对甲苯苯磺酸甲酯，相对分子质量为 186。

4-1-2 画出中间体 A1 的结构。

4-1-3 阐述为何 P 形成的胶束可以包含 M。注意指出不同链段的性质。

4-2 计算胶束中 M 与 P 的摩尔比 n。估算时相对原子质量保留到整数即可。单体 A1, A2, A3 的相对分子质量分别为 85.05, 127.1, 161.08。

4-3 将某条件下制备的的 M-P 胶束溶液稀释 $1.77 \times 10^{7}$ 倍即可达到肿瘤细胞 PC3 的半数抑制浓度（IC50）0.37 nmol/L，计算该胶束制剂中 M 的表观溶解度（可溶载药浓度）。不考虑 M-P 胶束组成的变化。

可以使用简单的化学平衡模型估算 M-P 胶束形成。无 M 时，对于 P 胶束的形成，可以考虑这样的平衡：

$$
\mathbf {P} (\mathrm{aq}) \rightarrow \mathbf {P} (\text {胶束}) K
$$

以标准浓度聚合度为某一特定值的胶束为标准态，假定 P(胶束)中 P 的活度（即在平衡常数中应当带入的“浓度”）始终是 1，胶束得以形成时溶液中 P 的浓度被称为“临界胶束浓度”（CMC）。假定 M 的存在并不会影响 P 形成胶束。

对于 M-P 胶束的形成，可以建立这样的模型：

$$
\mathbf {M} (\mathrm{aq}) \rightarrow \mathbf {M} (\text { 胶束 }) \quad K ^ {\prime} = x / [ \mathbf {M} (\mathrm{aq}) ]
$$

其中， $x$ 是 $\mathbf{M}$ 在胶束中的摩尔分数，聚合物中每个重复单元视作一个独立的分子。温度默认为 $298\mathrm{K}$ 。

4-4-1 已知对于嵌段共聚物 P 而言，CMC 为 $4.4 \mu mol/L$ ，估算 1 mol P 形成胶束的标准摩尔 Gibbs 自由能变。

4- 4- 2 假定载药量 LC 是在溶液中 M 的浓度达到饱和时测量得到的，计算 K 的值。

4-4-3 依据该模型, 首先向 $1 \mathrm{mmol} / \mathrm{L}$ 的 $\mathbf{P}$ 溶液中不断加入 $\mathbf{M}$ 至饱和, 过滤除去未溶固体后, 将溶液稀释 20 倍, 计算末态下胶束中 $\mathbf{M}$ 与 $\mathbf{P}$ 的摩尔比 $n$ 。

4-5-1\*（附加题，不计入总分）上述模型做的哪些假设可能是存在问题的？

4-5-2\*（附加题，不计入总分） 上述模型选取的热力学标准态是什么？

## 参考答案

目前,化学家已经能够借助 AI 等手段从细胞和分子水平针对性地进行药物设计,然而,缺乏合适的递送手段成为药物化学中新的瓶颈。对于疏水药物而言,设计合适的递送手段则尤为重要,因为其水溶液的极低浓度使得药物很难达到生理上有效的浓度。借助嵌段共聚物与药物分子形成胶束,可以有效提升药物的溶解度。有研究人员针对紫杉醇(记作 M, $M=854\ \text{g/mol}$ ,在水中溶解度仅为 $6.7\ \text{mg/L}$ )设计了一种嵌段共聚物 P 用于递送 M,其载药量 LC 达到了 45%。 $(LC=m_{\text{drug}}/(m_{\text{drug}}+m_{\text{polymer}}))$ 。

![](images/c8be64641c236cad9b82b32200a7ebe04668318b9a0c3bf67aad1e7851773652.jpg)

4-1-1 画出嵌段共聚物 P 的结构(不同的烷基统一用 R 表示即可), 并计算各嵌段的聚合度。每步增长的高分子链视作一个嵌段

提示：TsOMe 是对甲苯苯磺酸甲酯，相对分子质量为 186。

(2 分)  
![](images/53edf791f0015cde3e9d6371143c081bb36c35c4423988a9d13c4a113fabf227.jpg)  
(3 分, 封端错误扣 1 分)

活性中心摩尔量： $n=0.93/186\ mol=0.005\ mol$ （1分）
嵌段 1: 0.17/0.005 = 34，均由单体 A1 组成（1 分）
嵌段 2: $(0.065+0.025)/0.05=18$ ，由单体 A2 和单体 A3 组成（1 分）
嵌段 3: 0.17/0.005 = 34，均由单体 A1 组成（1 分）
(共 7 分)

4-1-2 画出中间体 A1 的结构。

![](images/e1569582ce54f557d807e3721588fdea45c7d5acec33c7969fec864e2563d383.jpg)

4-1-3 阐述为何 P 形成的胶束可以包含 M。注意指出不同链段的性质。

嵌段 1 和 3: Me 基团体积小, 链段整体呈现亲水性 (1 分), 使胶束可分散于水中。

嵌段 2: Bu 和 Bn 疏水体积大, 链段整体呈亲油性 (1 分), 使胶束可包含 M。4-2 计算胶束中 M 与 P 的摩尔比 n。估算时相对原子质量保留到整数即可。单体 A1, A2, A3 的相对分子质量分别为 85.05, 127.1, 161.08。

$$
\begin{array}{r l} \text { P   的分子量: } & m (\mathrm{pip-Me}) + 68 m (\mathbf {A 1}) + 13 m (\mathbf {A 2}) + 5 m (\mathbf {A 3}) = 8340 \\ & n = (0.45 / 854) \div (0.55 / 8340) = 8.00 (1 \text { 分 }) \end{array}
$$

4-3 将某条件下制备的的 M-P 胶束溶液稀释 $1.77 \times 10^{7}$ 倍即可达到肿瘤细胞 PC3 的半数抑制浓度（IC50）0.37 nmol/L，计算该胶束制剂中 M 的表观溶解度（可溶载药浓度）。不考虑 M-P 胶束组成的变化。

$$
1.77 \times 10 ^ {7} \times 0.37 \times 10 ^ {- 9} \times 854 \mathrm{g/L} = 5.6 \mathrm{g/L(1分)}
$$

可以使用简单的化学平衡模型估算 M-P 胶束形成。无 M 时，对于 P 胶束的形成，可以考虑这样的平衡：

$$
\mathbf {P} (\mathrm{aq}) \rightarrow \mathbf {P} (\text {胶束}) K
$$

以标准浓度聚合度为某一特定值的胶束为标准态，假定 P(胶束)中 P 的活度（即在平衡常数中应当带入的 “浓度”）始终是 1，胶束得以形成时溶液中 P 的浓度被称为 “临界胶束浓度”（CMC）。假定 M 的存在并不会影响 P 形成胶束。

对于 M-P 胶束的形成，可以建立这样的模型：

$$
\mathbf {M} (\mathrm{aq}) \rightarrow \mathbf {M} (\text { 胶束 }) K ^ {\prime} = x / [ \mathbf {M} (\mathrm{aq}) ]
$$

其中， $x$ 是 $\mathbf{M}$ 在胶束中的摩尔分数，聚合物中每个重复单元视作一个独立的分子。温度默认为 $298\mathrm{K}$ 。

4-4-1 已知对于嵌段共聚物 P 而言，CMC 为 $4.4 \mu mol/L$ ，估算 1 mol P 形成胶束的标准摩尔 Gibbs 自由能变。

$$
\begin{array}{r l} & K ^ {\circ} = c ^ {\circ} / \mathrm{CMC} = 2.273 \times 10 ^ {5} \\ & \Delta G ^ {\circ} = - R T \ln K ^ {\circ} = - 30.6 \mathrm{kJ/mol(2分)} \end{array}
$$

4- 4- 2 假定载药量 LC 是在溶液中 M 的浓度达到饱和时测量得到的，计算 K 的值。

$$
\begin{array}{r l} x & = 8 / (8 + 68 + 13 + 5) = 0.0851 \text {(1分)} \\ [ \mathbf {M} (\mathrm{aq}) ] & = 6.7 \times 10 ^ {- 3} / 854 \mathrm{mol/L} = 7.845 \times 10 ^ {- 6} \mathrm{mol/L(1分)} \\ K ^ {\prime} & = 10847 \mathrm{L/mol(1分)} \\ & (\text {共} 3 \text {分}) \end{array}
$$

4-4-3 依据该模型,首先向 1 mmol/L 的 P 溶液中不断加入 M 至饱和,过滤除去未溶固体后,将溶液稀释 20 倍,计算末态下胶束中 M 与 P 的摩尔比 n。

初态下总 M 浓度: $[M(aq)] + ([P]_{0} - [P]_{aq}) \times 8.00 = 7.973 \times 10^{-3} \, \text{mol/L}$ (1 分)
稀释后， $[M]_{0}=3.986\times10^{-4}\ mol/L,\quad[P]_{0}=5\times10^{-5}\ mol/L$

溶液中 $[\mathbf{P}]_{\mathrm{aq}} = 4.4\times 10^{-6}\mathrm{mol / L}$ ，若M未沉淀，假设溶液中M的浓度为 $c$ 。 $x = K^{\prime}c = n / (n + 86)$ （1分） $c + n([{\bf P}]_0 - [\bf P]_{\mathrm{aq}}) = [\bf M]_0$ （1分）解得 $n = 8.56$ ，超过了最大可承载量

因此 M 沉淀，溶液中 M 的浓度为 $7.845 \times 10^{-6} \, mol/L$ ，n = 8（1 分）
(共 4 分)

4-5-1\*（附加题，不计入总分） 上述模型做的哪些假设可能是存在问题的？
4-5-2\*（附加题，不计入总分） 上述模型选取的热力学标准态是什么？

## 知识点映射

- （待人工校准）


> ⚠️ **自动拆卡标记**：`subject_module`/`difficulty` 为关键词粗判，答案数值与单位**尚未经人工复核**。