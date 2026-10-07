---
title: "题-HYS-02-05-稀磁半导体Dilutedma"
aliases: ["题-HYS-02-05·决赛夏季模拟2"]
type: 题目
fidelity: 原书逐字
difficulty: 4
teaching_level: 竞赛
source: "化英社 第40届化英社化学奥林匹克决赛夏季模拟2 第 5 题"
module: "2026机构初赛模拟题"
source_subject: 结构化学
syllabus_codes: [15, 12, 13]
knowledge_points:
  - "[[晶体结构]]"
  - "[[晶体场理论]]"
  - "[[高自旋与低自旋]]"
  - "[[磁矩]]"
  - "[[配位化学]]"
tags: [化竞, 题目, 初赛, 机构模拟题, 化英社]
updated: 2026-09-26
status: 已填充
exam_stage: 初赛
subject_module: 结构化学
pack: 综合模拟卷
submodule: 化英社
source_category: 竞赛导向·竞赛教辅
source_grade: A
source_tier: 2
source_norm: "化英社-第40届化英社化学奥林匹克决赛夏季模拟2"
source_file: "2026机构初赛模拟题/07-化英社/第40届化英社化学奥林匹克决赛夏季模拟试题2.md"
---

# 题-HYS-02-05-稀磁半导体Dilutedma

## 题目

### 第 5 题 稀磁半导体的研究（32 分，占 16%）

稀磁半导体（Diluted magnetic semiconductors，DMS）指通过磁性原子掺杂入非磁性半导体形成的磁性材料。由于掺杂浓度较低，其磁性相对较弱，兼具电荷调控与自旋操纵特性，相比传统的磁自旋器件更有优势。

5-1 制备 DMS 的典型方法是在非磁半导体里掺入过渡金属（Mn/Co/Fe 等）或稀土离子。传统的 GaAs（Fe/Mn 掺杂）材料机理研究透彻，至今仍是理解 DMS 的模板化合物，下以 Fe 原子掺杂 GaAs 为例。

![](images/f524708dde1824709c1bc5282149de5330669cba013d35bc0e16a54d0f3ff0cc.jpg)
Substitutional Site

GaAs 采取立方 ZnS 结构堆积, 网状大球为 Ga 原子, 白色小球为 As 原子, Fe 原子有可能取代其中部分 Ga 原子位置 (Substitutional Site), 也有可能直接进入晶胞内的间隙 (Interstitial Site, $1 / 2, 1 / 2, 1 / 2$ )。

5-1-1 理论分析表明，对于 Substitutional Fe 原子，其处于最邻近 As 原子的四面体配位环境中，因此 Fe 处于高自旋排布状态。然而对于 Interstitial Fe 原子，尽管其仍处于 As 原子四面体配位环境中，却处于低自旋排布状态，已知电负性标度：Fe 1.83 Ga 1.80 As

2.16, 尝试从晶体场理论的角度, 解释 Interstitial Fe 原子为低自旋排布的原因, 注意考虑次近原子与 $\mathrm{{Fe}}$ 的相互作用。

已知电负性 As > Fe > Ga，四面体配位的 As 与 Fe 作用，主要使 t 对称性轨道 $(d_{xy}, d_{xz}, d_{yz})$ 能级升高，Interstitial Fe 与次近的八面体 Ga 原子作用较为强烈，主要使 e 对称性轨道 $(d_{x}^{2}, d_{y}^{2}, d_{z}^{2})$ 能级降低，增大了 e 组轨道和 t 组轨道的分裂能，最终使 Interstitial Fe 原子为低自旋排布

(3 分, 指出 Interstitial Fe 原子和次近 Ga 原子存在作用得 2 分, 继续从晶体场角度分析得 3 分, 参考下图)

![](images/0b197dc029ee32d0038e91241b25135290a680390a64cea0453ef7b31de680d2.jpg)

5-1-2 杂质离子对半导体电子结构的贡献可用 Anderson 模型来描述。以禁带中心为能量原点，假设导带底 $E_{c} = +0.5 \, eV$ ，价带顶 $E_{v} = -0.5 \, eV$ ，孤立的杂质原子轨道能量 $\varepsilon = +0.2 \, eV$ 。Anderson 模型表明，实际杂质原子轨道的能级 $\omega$ 满足

其中

$$
\begin{array}{c} \omega = \varepsilon + \Sigma (\omega) \\ \Sigma (\omega) = \Delta \ln (\frac {\omega = E _ {c}}{E _ {v} - \omega}) \end{array}
$$

$\Sigma (\omega)$ 表示杂质原子轨道与能带杂化带来的能量贡献, $\Delta$ 是杂化强度, 用以衡量杂质原子与能带相互作用的能力, 分别计算 $\Delta_{1} = 0.10 eV$ 和 $\Delta_{2} = 0.60 eV$ 下的 $\omega$ (保留三位小数) 的大小, 比较哪种情况电子更局域在杂质原子周围。

代入相应数值，解方程：

$$
\omega = \varepsilon + \Delta \ln \left(\frac {\omega - E _ {c}}{E _ {v} - \omega}\right)
$$

$$
\begin{array}{r l} & \text {解得} \omega_ {1} = 0.142 \mathrm{eV}, \quad \omega_ {2} = 0.059 \mathrm{eV} \\ & \text {第一种情况} \end{array}
$$

(3 分, 结果各 1 分, 比较 1 分)

5-2 在外加磁场的存在下，电子自旋引起的稀磁系统往往具有 Schottky 热容行为。如下图，纵轴正比于热容 $C$ ，横轴正比于温度 $T$ 。

![](images/6fc27cceb83600a9b26c6e83503a73c06a1c97e3c5221fb098bf2ffba4c02755.jpg)

这种行为源自电子自旋的 Zeeman 效应带来的能级分裂。假设稀磁系统中的一个磁性粒子自旋 S 为 1/2，Zeeman 效应会使原本能级简并的两个自旋状态（根据磁矩大小，形象地理解为向上↑或向下↓，与电子行为类似）劈裂为两个能量不同的状态。自旋磁矩与外磁场取向平行时，能量 $\varepsilon_{1} = -\mu H$ ；与外磁场取向相反时，能量 $\varepsilon_{2} = \mu H$ 。（ $\mu$ 是粒子磁矩大小，H 是外加磁场强度）假设稀磁系统中的粒子自旋不发生角动量耦合，即粒子之间没有相互作用。

5-2-1 设 N 为粒子的总数，当存在外磁场时，考虑高温和低温两种状态的微观状态数，分别给出高温状态（ $T \rightarrow \infty$ ）和低温状态（ $T \rightarrow 0$ ）下稀磁系统的熵。

依据 Boltzmann 熵公式: $S = k \ln \Omega$ , $\Omega$ 为微观状态数, 高温状态下, Zeeman 效应给出的能级分裂的影响相比热运动可以忽略不计, 因此对于每个粒子可以取得微观状态数为 2 , 总的微观状态数为 $2^{N}$ , 因此 $S = N k \ln 2$ 。低温状态下, 所有粒子都倾向于处于低能量状态 (与外磁场自旋平行, 没有热运动), 因此总微观状态数为 1 , $S = 0$ 。

$$
(4 \text {分,各} 2 \text {分})
$$

5-2-2 已知 Boltzmann 分布公式:

$$
\frac {N _ {i}}{N} = \frac {\exp (- \frac {\varepsilon_ {i}}{k T})}{\sum_ {j} \exp (- \frac {\varepsilon_ {j}}{k T})}
$$

其中 $N_{i}$ 为处于i状态的粒子数， $\varepsilon_{i}$ 为处于i状态粒子的能量，已知N为稀磁系统的总粒子数，稀磁系统中的粒子有向上↑或向下↓两种状态。尝试用 $\mu$ 、H、N、k、T表示稀磁系统的总能量E。

$$
N _ {1} = N \cdot \frac {e ^ {\frac {\mu H}{k T}}}{e ^ {\frac {\mu H}{k T}} + e ^ {- \frac {\mu H}{k T}}}, N _ {2} = N \cdot \frac {e ^ {\frac {\mu H}{k T}}}{e ^ {\frac {\mu H}{k T}} + e ^ {- \frac {\mu H}{k T}}}
$$

$$
E = N _ {1} \varepsilon_ {1} + N _ {2} \varepsilon_ {2} = - N \mu H \frac {e ^ {\frac {\mu H}{k T}} - e ^ {- \frac {\mu H}{k T}}}{e ^ {\frac {\mu H}{k T}} + e ^ {- \frac {\mu H}{k T}}}
$$

(4 分, $N_{1}$ 和 $N_{2}$ 各 1 分, 能量表达式 2 分)

5-2-3 现认为稀磁系统的总能量 E 即为稀磁系统的内能 U，根据热容的定义，给出稀磁系统的热容 C 表达式。直接指出在 $T \rightarrow 0$ 和 $T \rightarrow \infty$ 时，热容 C 趋向于多少？

$$
C = \frac {\delta Q}{d T} = \frac {\partial E}{\partial T} = 4 N k \left(\frac {\mu H}{k T}\right) ^ {2} \cdot \frac {1}{\left(e ^ {- \frac {\mu H}{k T}} + e ^ {\frac {\mu H}{k T}}\right) ^ {2}}
$$

$T \rightarrow 0$ 时， $\left(\frac{\mu H}{kT}\right)^{2} \rightarrow \infty$ ，但 $e^{-\frac{2\mu H}{kT}} \rightarrow 0$ 且幅度更大（指数级＞幂级），因此 $C \rightarrow 0$

$$
T \to \infty \mathrm{时}, C \sim N k \Bigl (\frac {\mu H}{k T} \Bigr) ^ {2} \to 0
$$

(4 分, 热容表达式 2 分, 热容行为各 1 分)

5-2-4 稀磁半导体的热容并不十分符合上述行为，根据理想稀磁系统的假设和 5-1 中的结果，简要解释原因。

稀磁半导体中杂质原子的电子发生离域，即粒子间存在相互作用。

## 参考答案

(2 分)

5-3 DMS 的一个关键技术难题在于大多 DMS 材料的 Curie 温度（铁磁性物质从高温顺磁性状态自发磁化为低温铁磁性状态的转变温度）过低，这导致在室温环境下材料往往只有顺磁性，无法实现铁磁性的调控。一种新型的 DMS 材料通过磁性原子间更强的自旋相互作用达到了较高的 Curie 温度。其组成为 $(\mathrm{Ba}_{1-y}\mathrm{K}_{y})(\mathrm{Zn}_{1-x}\mathrm{Mn}_{x})_{2}\mathrm{As}_{2}$ ，其中 K 和 Mn 是掺杂原子，x 和 y 的值没有必然关系，下图是它的四方晶胞，大球为 Ba/K，中球为 Zn/Mn，小球为 As。

![](images/4c6bd3dcce38c496b4b77ceceed682a9ed5d306f42e199efd1be0dac87b6a054.jpg)

5-3-1 特殊的合成方法保证了 K 和 Mn 原子掺杂均匀。已知最近 Zn/Mn-As 键距离为 2.55 Å，最近的 Ba/K-As 距离为 3.46 Å，Zn/Mn 层生下最短 As-As 距离为 4.19 Å。计算晶胞参数 a 和 c。

设 Zn/Mn-As 键在 $c$ 轴投影长度为 $m$ , Ba/K-As 键在 $c$ 轴投影长度为 $n$ 。则有:

$$
m ^ {2} + (0.5 a) ^ {2} = 2.55 ^ {2}, \quad n ^ {2} + (\frac {\sqrt {2}}{2} a) ^ {2} = 3.46 ^ {2}
$$

$$
(2 m) ^ {2} + (\frac {\sqrt {2}}{2} a) ^ {2} = 4.19 ^ {2}, \quad 4 m + 4 n = c
$$

解得 $m = 1.51 \mathrm{~A}, n = 1.88 \mathrm{~A}, a = 4.11 \mathrm{~A}, c = 13.56 \mathrm{~A}$ (3 分, $a$ 和 $c$ 各 1 分, 计算过程 1 分)

5-3-2 科研人员制备了一系列不同掺杂组成的晶体, 其 $T_{C} - x$ 关系如下图, $T_{C}$ 表示 Curie 温度, 其中性能最好的晶体的密度为 $5.559 \mathrm{~g} \cdot \mathrm{cm}^{-3}$ 。尝试给出该新型 DMS 晶体的组成, 假设在一定掺杂范围内晶胞参数不发生改变。

![](images/a4297126efc023d60cdfd8af49d8c26c2530946650fe4b309cd2eda1bd1ee7c0.jpg)

读图可知 $x = 0.24$

$$
\rho = \frac {2 \times M}{a ^ {2} c \times N _ {A}}
$$

5-3-3 注意到 $\mathrm{Zn} / \mathrm{Mn}$ 原子构成一个层状结构, 近邻的 $\mathrm{Mn}$ 原子间存在自旋相互作用, 系统的 Hamiltonian (可认为是稀磁系统的能量) 为 (截断到 $J_{3}$ )

$$
H = - \sum_ {\langle i, j \rangle} J _ {1} S _ {i} \cdot S _ {j} - \sum_ {\langle i, j \rangle} J _ {2} S _ {i} \cdot S _ {j} - \sum_ {\left\langle (\langle i, j \rangle) \right\rangle} J _ {3} S _ {i} \cdot S _ {j} - \sum_ {(i, j)} J _ {\perp} S _ {i} \cdot S _ {i}
$$

$J$ 为耦合常数, $J$ 从1\~3分别表示 $\mathrm{Zn/Mn}$ 原子层中最近邻、次近邻、第三近的一个自旋电子对的耦合常数大小 (设对所有 $J_{n}$ , 只要 $n$ 一致则 $J_{n}$ 不变), $S_{i}$ 为原子 $i$ 的自旋量子数, 该Hamiltonian实际给出了自旋系统相互作用能大小。 $J_{\perp}$ 是要考虑沿c轴方向最近的Mn-Mn自旋相互作用。设自旋朝上的自旋量子数均为 $S$ , 自旋朝下的自旋量子数均为 $-S$ 。

![](images/27925b73860ebf31b51fa7947775e781e8559b8ae2fd49fcc8f237b7f93a48fa.jpg)

以上图所示画圈的粒子 $i$ 为例, 上图为三维正方晶胞, 对于粒子 $i$ , 其 Hamiltonian $H_{i} = -2J_{1}S^{2} + 2J_{2}S^{2} + 2J_{3}S^{2}$ ( $J_{1}$ 项来自相邻四个粒子的作用, $J_{2}$ 项来自四个对角线粒子的作用, $J_{3}$ 项来自二倍晶胞参数位置四个粒子的相互作用)。

计算 $H$ 的大小不得不计算 $J_{n}$ 。由于 $J_{n}$ 局域化的特点， $J_{n}$ 可通过设计如下两种 $\mathrm{x} = 0.25$ 时的晶胞 $(\mathrm{Ba}_{1 - y}\mathrm{K}_y)_8\mathrm{Zn}_{12}\mathrm{Mn}_4\mathrm{As}_{16}$ 来计算。已知深色球为 Mn，白色球为 Zn，下图为 Zn/Mn 层的 c 轴投影，下图的晶胞实际为 5-3 中晶胞扩大四倍的结果。

第一种晶体用于计算 $J_{1} 、 J_{2}$ , 以 $\mathrm{Ba/K}$ 为晶胞顶点, $\mathrm{Zn/Mn}$ 层处于 $\mathrm{c}=1/4$ 和 $3/4$ 处, 其中可以测得 $H$ 的三种自旋情况如下三幅图:

![](images/d5b3c67deaf42aa845b677ef5464276516aff399cf7543ad32c9c82d5e8a2e24.jpg)

第二种晶体用于计算 $J_{3} 、 J_{\perp}$ , 以 $\mathrm{Zn/Mn}$ 为晶胞顶点, $\mathrm{Zn/Mn}$ 层处于 $\mathrm{c}=0$ 和 $1/2$ 处, 其中可以测得 $H$ 的三种自旋情况如下三幅图:

![](images/10666a2a3e3feba0b1f90d7d5843941e027823801a27236ac7d09c87545b5055.jpg)

用 $J_{1}$ 、 $J_{2}$ 、S表示上方三种情况的H，用 $J_{3}$ 、 $J_{\perp}$ 、S表示下方三种情况的H（在实验中测得H的值后可以反解出J的值），注意相邻晶胞间相互作用的归属。

对于上方三种情况:

$$
\begin{array}{c} H _ {1} = - 4 J _ {1} S ^ {2} - 4 J _ {2} S ^ {2} \\ H _ {2} = 4 J _ {2} S ^ {2} \\ H _ {3} = 4 J _ {1} S ^ {2} - 4 J _ {2} S ^ {2} \end{array}
$$

对于下方三种情况:

$$
H _ {4} = - 8 J _ {3} S ^ {2} - 4 J _ {\perp} S ^ {2}
$$

$$
H _ {5} = - 8 J _ {3} S ^ {2} + 4 J _ {\perp} S ^ {2}
$$

$$
H _ {6} = 8 J _ {3} S ^ {2} - 4 J _ {\perp} S ^ {2}
$$

(6分，各1分)

> ⛔ 校勘（2026-10-07）：源卡**题面区混入解答**（原题面 7425 字），已按「答案起点」截断，混入部分**移入本答案区**；截断判据＝首个评分标注/「解：」。



稀磁半导体（Diluted magnetic semiconductors，DMS）指通过磁性原子掺杂入非磁性半导体形成的磁性材料。由于掺杂浓度较低，其磁性相对较弱，兼具电荷调控与自旋操纵特性，相比传统的磁自旋器件更有优势。

5-1 制备 DMS 的典型方法是在非磁半导体里掺入过渡金属（Mn/Co/Fe 等）或稀土离子。传统的 GaAs（Fe/Mn 掺杂）材料机理研究透彻，至今仍是理解 DMS 的模板化合物，下以 Fe 原子掺杂 GaAs 为例。

![](images/b1ab7f14abe61eefab76418daa67ade946f80d41899628396d1a9fe7067d9c5b.jpg)
Substitutional Site

GaAs 采取立方 ZnS 结构堆积，网状大球为 Ga 原子，白色小球为 As 原子，Fe 原子有可能取代其中部分 Ga 原子位置（Substitutional Site），也有可能直接进入晶胞内的间隙（Interstitial Site，1/2，1/2，1/2）。

5-1-1 理论分析表明，对于 Substitutional Fe 原子，其处于最邻近 As 原子的四面体配位环境中，因此 Fe 处于高自旋排布状态。然而对于 Interstitial Fe 原子，尽管其仍处于 As 原子四面体配位环境中，却处于低自旋排布状态，已知电负性标度：Fe 1.83 Ga 1.80 As

2.16，尝试从晶体场理论的角度，解释 Interstitial Fe 原子为低自旋排布的原因，注意考虑次近原子与 Fe 的相互作用。

已知电负性 As > Fe > Ga，四面体配位的 As 与 Fe 作用，主要使 t 对称性轨道 $(d_{xy}, d_{xz}, d_{yz})$ 能级升高，Interstitial Fe 与次近的八面体 Ga 原子作用较为强烈，主要使 e 对称性轨道 $(d_{x^{2}}^{2}, d_{y^{2}}, d_{z^{2}})$ 能级降低，增大了 e 组轨道和 t 组轨道的分裂能，最终使 Interstitial Fe 原子为低自旋排布

（3分，指出InterstitialFe原子和次近Ga原子存在作用得2分，继续从晶体场角度分析得3分，参考下图）

![](images/6d8d805ee5272806d85a4d368cb83022f5992422a53eea6f418d0a5577a79f5c.jpg)

5-1-2 杂质离子对半导体电子结构的贡献可用 Anderson 模型来描述。以禁带中心为能量原点，假设导带底 $E_{c} = +0.5 \, eV$ ，价带顶 $E_{v} = -0.5 \, eV$ ，孤立的杂质原子轨道能量 $\varepsilon = +0.2 \, eV$ 。Anderson 模型表明，实际杂质原子轨道的能级 $\omega$ 满足

其中

![](images/26a12de3912818a5473a0f6d3add288eca4b2e97984b2fad53709afcfde84829.jpg)

$\Sigma (\omega)$ 表示杂质原子轨道与能带杂化带来的能量贡献， $\Delta$ 是杂化强度，用以衡量杂质原子与能带相互作用的能力，分别计算 $\Delta_{1} = 0.10eV$ 和 $\Delta_{2} = 0.60eV$ 下的 $\omega$ （保留三位小数）的大小，比较哪种情况电子更局域在杂质原子周围。

代入相应数值，解方程：

$$
\omega = \varepsilon + \Delta \ln (\frac {\omega - E _ {c}}{E _ {v} - \omega})
$$

$$
\begin{array}{r l} \text {解得} \omega_ {1} & = 0.142 \mathrm{eV}, \omega_ {2} = 0.059 \mathrm{eV} \\ & \text {第一种情况} \end{array}
$$

(3 分, 结果各 1 分, 比较 1 分)

5-2 在外加磁场的存在下，电子自旋引起的稀磁系统往往具有 Schottky 热容行为。如下图，纵轴正比于热容 $C$ ，横轴正比于温度 $T$ 。

![](images/a47daca456d5e26ee82d89c57ba87d8dfd3c2f41b5b7f22d780a3717fbd6a385.jpg)

这种行为源自电子自旋的 Zeeman 效应带来的能级分裂。假设稀磁系统中的一个磁性粒子自旋 S 为 1/2，Zeeman 效应会使原本能级简并的两个自旋状态（根据磁矩大小，形象地理解为向上↑或向下↓，与电子行为类似）劈裂为两个能量不同的状态。自旋磁矩与外磁场取向平行时，能量 $\varepsilon_{1} = -\mu H$ ；与外磁场取向相反时，能量 $\varepsilon_{2} = \mu H$ 。（ $\mu$ 是粒子磁矩大小，H 是外加磁场强度）假设稀磁系统中的粒子自旋不发生角动量耦合，即粒子之间没有相互作用。

5-2-1 设 N 为粒子的总数，当存在外磁场时，考虑高温和低温两种状态的微观状态数，分别给出高温状态（ $T \rightarrow \infty$ ）和低温状态（ $T \rightarrow 0$ ）下稀磁系统的熵。

依据 Boltzmann 熵公式: $S = k \ln \Omega$ , $\Omega$ 为微观状态数, 高温状态下, Zeeman 效应给出的能级分裂的影响相比热运动可以忽略不计, 因此对于每个粒子可以取得微观状态数为 2 , 总的微观状态数为 $2^{\mathrm{N}}$ , 因此 $S = N k \ln 2$ 。

低温状态下，所有粒子都倾向于处于低能量状态（与外磁场自旋平行，没有热运动），因此总微观状态数为 1，S=0。

$$
(4 \text {分,各} 2 \text {分})
$$

5-2-2 已知 Boltzmann 分布公式:

$$
\frac {N _ {i}}{N} = \frac {e x p (- \frac {\varepsilon_ {i}}{k T})}{\sum_ {j} e x p (- \frac {\varepsilon_ {j}}{k T})}
$$

其中 $N_{i}$ 为处于i状态的粒子数， $\varepsilon_{i}$ 为处于i状态粒子的能量，已知N为稀磁系统的总粒子数，稀磁系统中的粒子有向上↑或向下↓两种状态。尝试用 $\mu$ 、H、N、k、T表示稀磁系统的总能量E。

$$
N _ {1} = N \cdot \frac {e ^ {\frac {\mu H}{k T}}}{e ^ {\frac {\mu H}{k T}} + e ^ {\frac {\mu H}{k T}}}, N _ {2} = N \cdot \frac {e ^ {- \frac {\mu H}{k T}}}{e ^ {\frac {\mu H}{k T}} + e ^ {- \frac {\mu H}{k T}}}
$$

$$
E = N _ {1} \varepsilon_ {1} + N _ {2} \varepsilon_ {2} = - N \mu H \frac {\frac {\mu H}{e ^ {k T}} - e ^ {- \frac {\mu H}{k T}}}{\frac {\mu H}{e ^ {k T}} + e ^ {- \frac {\mu H}{k T}}}
$$

(4 分, $N_{1}$ 和 $N_{2}$ 各 1 分, 能量表达式 2 分)

5-2-3 现认为稀磁系统的总能量 E 即为稀磁系统的内能 U，根据热容的定义，给出稀磁系统的热容 C 表达式。直接指出在 $T \rightarrow 0$ 和 $T \rightarrow \infty$ 时，热容 C 趋向于多少？

$$
C = \frac {\delta Q}{d T} = \frac {\partial E}{\partial T} = 4 N k \left(\frac {\mu H}{k T}\right) ^ {2} \cdot \frac {1}{\left(e ^ {- \frac {\mu H}{k T}} + e ^ {\frac {\mu H}{k T}}\right) ^ {2}}
$$

$T \to 0$ 时， $\left(\frac{\mu H}{kT}\right)^2 \to \infty$ ，但 $e^{\frac{2\mu H}{kT}} \to 0$ 且幅度更大（指数级 $>$ 幂级），因此 $C \to 0$

$$
T \to \infty \mathrm{时}, C \sim N k \Big (\frac {\mu H}{k T} \Big) ^ {2} \to 0
$$

(4 分, 热容表达式 2 分, 热容行为各 1 分)

5-2-4 稀磁半导体的热容并不十分符合上述行为，根据理想稀磁系统的假设和 5-1 中的结果，简要解释原因。

5-3 DMS 的一个关键技术难题在于大多 DMS 材料的 Curie 温度（铁磁性物质从高温顺磁性状态自发磁化为低温铁磁性状态的转变温度）过低，这导致在室温环境下材料往往只有顺磁性，无法实现铁磁性的调控。一种新型的 DMS 材料通过磁性原子间更强的自旋相互作用达到了较高的 Curie 温度。其组成为 $(\mathrm{Ba}_{1-x}\mathrm{K}_{y})(\mathrm{Zn}_{1-x}\mathrm{Mn}_{x})_{2}\mathrm{As}_{2}$ ，其中 K 和 Mn 是掺杂原子，x 和 y 的值没有必然关系，下图是它的四方晶胞，大球为 Ba/K，中球为 Zn/Mn，小球为 As。

![](images/d2d828f7e5ed1d1732c1c67487937bc5ba93bb523bc477e9cd7e6e3e8d5a1c50.jpg)

5-3-1 特殊的合成方法保证了 K 和 Mn 原子掺杂均匀。已知最近 Zn/Mn-As 键距离为 2.55 Å，最近的 Ba/K-As 距离为 3.46 Å，Zn/Mn 层生下最短 As-As 距离为 4.19 Å。计算晶胞参数 a 和 c。

设 $\mathrm{Zn / Mn - As}$ 键在 $c$ 轴投影长度为 $m$ ，Ba/K-As键在 $c$ 轴投影长度为 $n$ 。则有：

$$
m ^ {2} + (0.5 a) ^ {2} = 2.55 ^ {2}, n ^ {2} + (\frac {\sqrt {2}}{2} a) ^ {2} = 3.46 ^ {2}
$$

$$
(2 m) ^ {2} + (\frac {\sqrt {2}}{2} a) ^ {2} = 4.19 ^ {2}, \quad 4 m + 4 n = c
$$

解得 $m=1.51\ \text{A},\ n=1.88\ \text{A},\ a=4.11\ \text{A},\ c=13.56\ \text{A}$ (3 分, a 和 c 各 1 分, 计算过程 1 分)

5-3-2 科研人员制备了一系列不同掺杂组成的晶体, 其 $T_{C}-x$ 关系如下图, $T_{C}$ 表示 Curie 温度, 其中性能最好的晶体的密度为 $5.559 \mathrm{~g} \cdot \mathrm{cm}^{-3}$ 。尝试给出该新型 DMS 晶体的组成, 假设在一定掺杂范围内晶胞参数不发生改变。

![](images/9e218995de05abbfae24842ea5f323d6dfe556cd53a4126e2a993f95afb10672.jpg)

读图可知 $x = 0.24$

$$
\rho = \frac {2 \times M}{a ^ {2} c \times N _ {A}}
$$

$$
\begin{array}{r l} & {\text {其中} M = 137.3 \times (1 - y) + 39.1 \times y + 65.38 \times (2 - 2 x) + 54.94 \times 2 x + 74.92 \times 2} \\ & {\qquad \qquad \qquad \qquad \text {解得} y = 0.30} \end{array}
$$

所以组成为 $(\mathrm{Ba}_{0.70}\mathrm{K}_{0.30})(\mathrm{Zn}_{0.76}\mathrm{Mn}_{0.24})_{2}\mathrm{As}_{2}$ （3分，组成2分，计算过程1分）

5-3-3 注意到 $\mathrm{Zn} / \mathrm{Mn}$ 原子构成一个层状结构, 近邻的 $\mathrm{Mn}$ 原子间存在自旋相互作用, 系统的 Hamiltonian (可认为是稀磁系统的能量) 为 (截断到 $J_{3}$ )

$$
H = - \sum_ {\langle i, j \rangle} J _ {1} S _ {i} \cdot S _ {j} - \sum_ {\langle i, j \rangle} J _ {2} S _ {i} \cdot S _ {j} - \sum_ {\left\langle (i, j)\right)} J _ {3} S _ {i} \cdot S _ {j} - \sum_ {(i, l)} J _ {\perp} S _ {i} \cdot S _ {l}
$$

J 为耦合常数，J 从 1\~3 分别表示 Zn/Mn 原子层中最近邻、次近邻、第三近的一个自旋电子对的耦合常数大小（设对所有 $J_{n}$ ，只要 n 一致则 $J_{n}$ 不变）， $S_{i}$ 为原子 i 的自旋量子数，该 Hamiltonian 实际给出了自旋系统相互作用能大小。 $J_{\perp}$ 是要考虑沿 c 轴方向最近的 Mn-Mn 自旋相互作用。设自旋朝上的自旋量子数均为 S，自旋朝下的自旋量子数均为 -S。

![](images/9d14b94e61b05232aff4c9481f9289e64872ade8c87267ee7df7ae78d3e20de8.jpg)

以上图所示画圈的粒子 $i$ 为例, 上图为三维正方晶胞, 对于粒子 $i$ , 其 Hamiltonian $H_{i} = -2J_{1}S^{2} + 2J_{2}S^{2} + 2J_{3}S^{2}$ ( $J_{1}$ 项来自相邻四个粒子的作用, $J_{2}$ 项来自四个对角线粒子的作用, $J_{3}$ 项来自二倍晶胞参数位置四个粒子的相互作用)。

计算 $H$ 的大小不得不计算 $J_{n}$ 。由于 $J_{n}$ 局域化的特点， $J_{n}$ 可通过设计如下两种 $\mathrm{x} = 0.25$ 时的晶胞 $(\mathrm{Ba}_{1 - \mathrm{y}}\mathrm{K}_{\mathrm{y}})_{8}\mathrm{Zn}_{12}\mathrm{Mn}_{4}\mathrm{As}_{16}$ 来计算。已知深色球为 Mn，白色球为 Zn，下图为 Zn/Mn 层的 c 轴投影，下图的晶胞实际为 5-3 中晶胞扩大四倍的结果。

第一种晶体用于计算 $J_{1}$ 、 $J_{2}$ , 以 $\mathrm{Ba} / \mathrm{K}$ 为晶胞顶点, $\mathrm{Zn} / \mathrm{Mn}$ 层处于 $\mathrm{c} = 1 / 4$ 和 $3 / 4$ 处, 其中可以测得 $H$ 的三种自旋情况如下三幅图:

![](images/99517b6e4b1deb178307e53c40da7fdcd6714aca8a2022f2922a0aaac16c1fb2.jpg)

第二种晶体用于计算 $J_{3}$ 、 $J_{\perp}$ ，以 $\mathrm{Zn / Mn}$ 为晶胞顶点， $\mathrm{Zn / Mn}$ 层处于 $\mathbf{c} = 0$ 和1/2处，其中可以测得 $H$ 的三种自旋情况如下三幅图：

![](images/e4d972668184c1d5cfe0531713c179d02de3a65a497c97a997e28b02ed78158a.jpg)

用 $J_{1}$ 、 $J_{2}$ 、S表示上方三种情况的H，用 $J_{3}$ 、 $J_{\perp}$ 、S表示下方三种情况的H（在实验中测得H的值后可以反解出J的值），注意相邻晶胞间相互作用的归属。

对于上方三种情况:

$$
\begin{array}{c} H _ {1} = - 4 J _ {1} S ^ {2} - 4 J _ {2} S ^ {2} \\ H _ {2} = 4 J _ {2} S ^ {2} \\ H _ {3} = 4 J _ {1} S ^ {2} - 4 J _ {2} S ^ {2} \end{array}
$$

对于下方三种情况:

$$
H _ {4} = - 8 J _ {3} S ^ {2} - 4 J _ {\perp} S ^ {2}
$$

$$
H _ {5} = - 8 J _ {3} S ^ {2} + 4 J _ {\perp} S ^ {2}
$$

$$
H _ {6} = 8 J _ {3} S ^ {2} - 4 J _ {\perp} S ^ {2}
$$

$$
(6 \text {分,各} 1 \text {分})
$$

## 知识点映射

- （待人工校准）


> ⚠️ **自动拆卡标记**：`subject_module`/`difficulty` 为关键词粗判，答案数值与单位**尚未经人工复核**（OCR 原文逐字转录，可能保留原卷笔误）。