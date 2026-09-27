---
title: "题-HZ-03-06-麦克斯韦妖Maxwellsd"
aliases: ["题-HZ-03-06"]
type: 题目
fidelity: 原书逐字
difficulty: 4
teaching_level: 竞赛
source: "汇智 汇智起航五一初赛模拟3 第 6 题"
module: "2026机构初赛模拟题"
source_subject: 化学原理
syllabus_codes: []
knowledge_points: []
tags: [化竞, 题目, 初赛, 机构模拟题, 汇智]
updated: 2026-09-26
status: 已填充
exam_stage: 初赛
subject_module: 化学原理
pack: 综合模拟卷
submodule: 汇智
source_category: 竞赛导向·竞赛教辅
source_grade: A
source_norm: "汇智-汇智起航五一初赛模拟3"
source_file: "2026机构初赛模拟题/08-汇智/汇智起航五一初赛模拟3试卷.md"
---

# 题-HZ-03-06-麦克斯韦妖Maxwellsd

## 题目

### 第 6 题 Maxwell 妖分子识别实验(22 分，占 10%)

麦克斯韦妖(Maxwell's demon)的假说，是由麦克斯韦为探讨热力学第二定律的一个可能反例而提出。一个绝热容器被分成相等的两格，中间是由“妖”控制的一扇小“门”，容器中的空气分子作无规则热运动时会向门上撞击，“门”可以选择性的将速度较快的分子放入一格，而较慢的分子放入另一格，这样，其中的一格就会比另外一格温度高，可以利用此温差，驱动热机做功，也即违反了第二热力学原理。

为此，研究人员为构造这一理论实验，在 U 形管两臂的水相之间设置含 FeII4L6 配位笼的膜相作为“分子闸门”，以可光致异构的 o-氟偶氮苯（FAB）为被运输分子，通过差异光照建立厘米尺度可逆的浓度梯度，构筑 maxwell 妖级别的分子识别。

在 $298 \mathrm{~K}$ 的 U 形管装置中, 两臂各含 $50 \mathrm{~mL}$ 水溶液, 中

间为含配位笼的膜相作为跨膜“闸门”。已知 cis-FAB 对配位笼的亲和力显著高于 trans-FAB。左臂光照（530 nm）将 trans 构型转变为 cis 构型，右臂关照（400 nm）将 cis 构型转变为 trans 构型，从而在光场“信息”辅助下实现定向净转运。

给定光强下的稳态组成为，左臂 cis-FAB 占比 $\alpha_{L}=0.80$ ，右臂 cis-FAB 占比 $\alpha_{R}=0.10$ 。配位笼对不同异构体的结合常数： $K_{cis}=2.0\times10^{5}\ M^{-1}$ ， $K_{trans}=2.0\times10^{3}\ M^{-1}$ （水相中，298 K）。初始 FAB 总浓度两臂相同，照射后达稳态时测得：左臂 $C_{L}=8.5\ mM$ ，右臂 $C_{R}=11.5\ mM$ 。设跨膜转运仅在

![](images/02f2b415c4302e526e1d801a248ef4756cf062815e355915c5876b01fcfb82aa.jpg)

“笼-客体”复合物状态发生，传递步骤快于水相扩散；忽略热致异构。

6-1 在解答 6-1 时不区分 cis 与 trans

6-1-1 计算稳态下 FAB 从左端运输到右端的吉布斯自由能 $\Delta G$ 。

6-1-2 估算用 $530 \mathrm{~nm}$ 光的热力学下限“光子耗量”：每从左端泵送 $1 \mathrm{~mol} \mathrm{FAB}$ 至右臂，至少消耗多少 mol 光子。

6-2-1 在稳态条件下左臂界面附近的 $c_{\mathrm{cis}}^{(L)} = f_L C_L$ ， $c_{\mathrm{trans}}^{(L)} = (1 - f_L) C_L$ 。计算此处单个结合位点被 cis-FAB 占据的概率 $p_{\mathrm{cis}}^{(L)}$ 与空位概率 $p_0^{(L)}$ 。

提示：单位结合位点的兰姆缪尔统计分配函数

$$
Z = 1 + K _ {\mathrm{cis}} c _ {\mathrm{cis}} + K _ {\mathrm{trans}} c _ {\mathrm{trans}} + K _ {N} c _ {N}
$$

其中各状态概率 $p_{i}=(对应项)/Z$ 。

6-2-2 当右臂加入萘至 $C_{N}^{(R)} = 5.0 \mathrm{mM}$ (左臂无萘), $\mathrm{K}_{\mathrm{N}} = 10^{6}$ , 计算右臂界面的 $p_{N}^{(R)}$ 与“活性笼”分数 $a^{(R)} = 1 - p_{N}^{(R)}$ (活性笼指未被萘占据的位点)。

6-2-3 结合结果解释为何加入萘可同时放大 FAB 梯度并诱发萘的反向泵送。

6-3-1 设计一个最简单的动力学循环（左水相 trans $\xrightarrow{光530nm}$ 左水相 cis $\rightleftharpoons$ 左侧笼-cis $\xrightarrow{跨膜}$ 右侧笼-cis $\rightleftharpoons$ 右水相 cis $\xrightarrow{光400nm}$ 右水相 trans $\rightleftharpoons$ 左水相 trans）。给定光稳态下

$$
\frac {k _ {t \rightarrow c} ^ {(L)}}{k _ {c \rightarrow t} ^ {(L)}} = 9, \frac {k _ {c \rightarrow t} ^ {(R)}}{k _ {t \rightarrow c} ^ {(R)}} = 9, \frac {K _ {\mathrm{cls}}}{K _ {\mathrm{trans}}} = 100,
$$

写出该闭合循环的热力学亲和

$$
\mathcal {A} = k _ {B} T \mathrm{ln} \left(\frac {\prod \text {正向速率常数}}{\prod \text {反向速率常数}}\right),
$$

并数值估算 $\mathcal{A}$ （单位 $\mathrm{kJ} \, \mathrm{mol}^{-1}$ ）。说明 $\mathcal{A} > 0$ 的物理含义及其与外场（光）供能的关系。6-3-2 实际上的稳态动力学循环如下图所示：

![](images/55cd3c5ebadf987a6ed2fdbce40be14935bc8b2123307849c785f213ed5549b6.jpg)

试说明 6-3-1 中的忽略条件以及忽略的合理性。

思考题:

麦克斯韦妖虽然在实际情况中不存在，但麦克斯韦设想涉及到信息的作用、以及信息和能量的关系。此争论促进了信息论的建立和发展，加深了对热力学第二定律的认识。

在信息热力学中，比特重置的一个典型例子是在温度为 $T$ 的热浴中，把一个逻辑比特“不可逆地复位”到确定状态（比如从 0/1 随机变成固定 0），至少要耗散的热量为 $k_{B} T \ln 2$ ，单位为 J/bite）。

若把右臂 cis→trans 的“遗忘”看作一次“比特重置”。使用 6-1-1 中所计算的数据，估算每泵送 1 mol FAB 至右臂所需“最小信息代价”（以 bite/分子计）。讨论为何实验中实际代价远高于该下限。

## 参考答案

<table><tr><td>6-1-1 ΔG = RT ln(CR/Cl) = 8.314 ×298 × ln(11.5/8.5) J mol-1 = 7.5 × 102 J mol-1(2分)</td></tr><tr><td>6-1-2530 nm 光子摩尔能量 EpH = NAhc/λ = 226 kJ mol-1。最小光子耗量νmIn = ΔG/Eph = 0.748 kJ mol-1/226 kJ mol-1 = 3.3 × 10-3mol photon/mol(热力学下限,实际远高于此。)(3分)</td></tr><tr><td>6-2-1 左臂: cLcIs = 0.80 × 8.5 mM = 6.8 mM, cLtrans = 1.7 mM。Z(L) = 1 + KcIs cLcIs + Ktrans cLtrans ≈ 1 + 2.0 × 105 × 6.8 × 10-3 + 2.0 × 103 × 1.7 × 10-3≈ 1 + 1360 + 3.4 ≈ 1364.4(1分)pLcIs ≈ 1360/1364.4 ≈ 0.997, pL0 ≈ 1/1364.4 = 7.3 × 10-4(每个1分)共3分</td></tr><tr><td>6-2-2 右臂: c(RcIs = 0.10 × 11.5 mM = 1.15 mM, c(Rtrans = 10.35 mM, c(RN = 5.0 mM。Z(R)= 1 + KcIs c(RcIs + Ktrans c(R) trans + KNC(N = 1 + 2.0 × 105 × 1.15 × 10-3 + 2.0 × 103 × 10.35 × 10-3 + 106 × 5 × 10-3= 1 + 230 + 20.7 + 5000 = 5251.7(1分)p(RN = 5000/5251.7 = 0.952(2分),故活性笼a(R) = 1 - p(RN = 0.048(1分)共4分</td></tr><tr><td>6-2-3 右臂高亲和客体萘占位阻断回流通道促进FAB释放,从而放大FAB梯度;同时萘被“反向泵送”(由右向左)体现耦合运输。(2分)</td></tr><tr><td>6-3-1 A = kB Tln [(k(Lt→c)/k(Lt→t))·(KcIs/Ktrans)·(k(Rt→t)/k(Rt→c)] = kB Tln (9 × 100 × 9) = kB Tln (8100) = (2.477 kJ mol-1) × 8.999 ≈ 22.3 kJ mol-1.(2分)A &gt;0 表明存在驱动循环的外部功(光供能)(1分),系统维持稳态平衡外部吸能并持续产熵(1分)。</td></tr><tr><td>6-3-2 忽略了活性笼中的trans异构体的吸附与传输以及自然条件下cis和trans异构体互变。(2分)合理性:由于笼具有选择性识别功能,trans异构体过大无法吸附运输,因此合理。(1分)实现偶氮化合物的cis-trans异构本身就需要较大能量,可以不考虑该异构化的情况。(1分)思考题(不计分):若每闭环泵送1个FAB伴随一次“重置”,最小散热Qmin = kB Tln 2 /bite,对应最小信息代价 = ΔG/(kB Tln 2 * NA) = 0.75×103/(2.477×103)ln 2 ≈ 0.44 bit/分子。实际体系因非理想耦合、非选择性吸收与竞争占位等原因,代价远高于下限。</td></tr></table>

## 知识点映射

- （待人工校准）


> ⚠️ **自动拆卡标记**：`subject_module`/`difficulty` 为关键词粗判，答案数值与单位**尚未经人工复核**（OCR 原文逐字转录，可能保留原卷笔误）。