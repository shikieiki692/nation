---
title: "题-CM-144-07-光氧化还原Photoredo"
aliases: ["题-CM-144-07"]
type: 题目
fidelity: 原书逐字
difficulty: 4
teaching_level: 竞赛
source: "chemy 第37届 初赛19 第 7 题"
module: "2026机构初赛模拟题"
source_subject: 有机化学
syllabus_codes: [8, 7]
knowledge_points:
  - "[[光氧化还原催化]]"
  - "[[标准电极电势]]"
  - "[[平衡常数]]"
  - "[[PCET（质子耦合电子转移）]]"
  - "[[自由基]]"
tags: [化竞, 题目, 初赛, 机构模拟题, chemy]
updated: 2026-10-04
status: 已填充
exam_stage: 初赛
subject_module: 有机化学
pack: 综合模拟卷
submodule: chemy
source_category: 竞赛导向·竞赛教辅
source_grade: A
source_tier: 2
source_norm: "chemy-第37届第0届初赛19"
source_file: "chemy试题/第37届Chemy题目合集..md"
---

# 题-CM-144-07-光氧化还原Photoredo

## 题目

### 第 7 题（10 分）

光氧化还原(Photoredox)反应是近年来有机合成方法学的核心研究领域。在这类反应中，通常需要用到光氧化还原催化剂(简写为 PC)。在光照条件下，PC 的 HOMO 轨道的一个电子会发生跃迁，转化为激发态 PC $^{*}$ ，从而在体系中发挥氧化剂/还原剂的作用。在光氧化还原的条件下，可以实现卤代烃的氢化还原反应，如下图所示。

![](images/c6b558751447559bc1131a0707f317bba73a86a113d1effce36180d898a4421c.jpg)

在上述反应中，底物 A 会被 PC\*还原为中间体 C，C 的 C-Cl 键发生断裂，形成苯基自由基中间体 D，D 最后结合氢转化为产物 B。

![](images/fb134cfff6a711fc29b2ceea57fbf21591afaa6baacf1f7fd5a2a9695466e7fd.jpg)

已知物理化学数据： $\varphi^{\theta}(\mathbf{PC}^{\cdot+}/\mathbf{PC})=0.80\ V;\ \varphi^{\theta}(\mathbf{PC}^{\cdot+}/\mathbf{PC}^{*})=-2.34\ V;\ \varphi^{\theta}(\mathbf{A}/\mathbf{C})=-2.08\ V;$ $pK_{a}(\mathbf{PC}^{\cdot+})=17.0;\ pK_{a}(\mathbf{X})=25.4$ 。以下各问中均令温度 T=298 K。

7-1 解释光氧化还原催化剂需要光照才能发挥作用的原因。

7-2 计算反应 $A + PC^{*} = C + PC^{\cdot+}$ 的平衡常数 $K^{\theta}$ 。

7-3 在碱 X 的存在下，该氧化还原过程中将包含一步酸碱反应，此时的半反应为：

![](images/a33473df67465fa655fb594e5dc0440dea2e39092fe780f11104c6ccefb69edf.jpg)

计算反应 $A + X + PC^{*} = C + M + XH^{+}$ 的平衡常数 $K^{\theta}$ 。

7-4 结合 7-2 和 7-3 的计算结果，说明碱在该体系中的作用。

7-5 在光氧化还原体系，通常会引入物理量 $E_{0,0}$ ，其定义为激发态和基态的最低振动能级之间的能隙，单位为 V。计算上述光氧化还原催化剂 PC 的 $E_{0,0}$ 。

有机化学中可能用到的缩写：DCM: 二氯甲烷；toluene: 甲苯；CSA: 樟脑磺酸；DBU: 1,8-二氮杂二环十一碳-7-烯；DCE: 1,2-二氯乙烷；TEA: 三乙胺；THF: 四氢呋喃。

## 参考答案

![](images/38836643ae780ea9548965d3892f4191da07303ca0e6553c36af0dfdddc049b1.jpg)

![](images/0cb59982f9a4feabe6a8aa27fe28355c458c1ecf1da87d0f4e99f866f77027c5.jpg)

![](images/2119189f45a7d074200c76f04e3cad995139a9fa1fe5f4344852c46264ee8019.jpg)

D

7-1 由于一般的 PC 催化剂氧化/还原电势比较低，氧化性/还原性较差（1 分）。而 PC 经光照转化为 PC\*之后，具有很高的氧化/还原电势（1 分），从而顺利的与氧化性/还原性较弱的有机物种发生反应。

由 $-RT\ln K^{\theta}=-nEF$ ，得 $K^{\theta}=\exp(nEF/RT)=2.50\times10^{4}$ （1分）

![](images/418a6070cf2c2c846970afe4fc181327983f612e97b3118211894e9ba13130b9.jpg)

7-3 记上述半反应的标准电极电势为 $\varphi_{0}$ ，则 $\varphi_{0}$ 满足如下关系式：

$$
\varphi_{0} = \varphi^{\theta} \left(\mathbf {PC} ^{\cdot +} / \mathbf {PC} ^{*}\right) + (R T / n F) \times 2.303 \times \left[ p K _{a} \left(\mathbf {PC} ^{\cdot +}\right) - p K _{a} (\mathbf {X}) \right]
$$

将数据带入上式得 $\varphi_{0} = -2.84 \, V$ （2 分）

记上述反应的电动势为 $E_{0}$ ，则 $E_{0} = \varphi^{\theta}(\mathbf{A} / \mathbf{C}) - \varphi_{0} = 0.76 \, \text{V}$ （1 分）

故反应平衡常数 $K^{\theta} = \exp (nE_{0}F / RT) = 7.1\times 10^{12}$ （1分）

7-4 碱的作用：碱可以通过攫取质子，从而增强激发态下的光催化剂的还原能力，增大反应的平衡常数，使得反应更容易发生（1分）。该过程实际上就是 Photoredox 反应中的 PCET 过程。

$$
7 - 5 E _{0, 0} = \varphi^{\theta} (\mathbf {PC} ^{\cdot +} / \mathbf {PC}) - \varphi^{\theta} (\mathbf {PC} ^{\cdot +} / \mathbf {PC} ^{*}) = 0.80 \mathrm{V} - (- 2.34 \mathrm{V}) = 3.14 \mathrm{V} (1 \text {分})
$$

## 知识点映射

- （待人工校准）
