---
title: "傅献彩《物理化学》（第六版下册）-第十二章 化学动力学基础(三)：反应速率理论与单分子反应"
type: 外部教材切片
source_book: "物理化学（第六版下册）-傅献彩"
syllabus_codes: [基础-12, 决赛-07]
created: 2026-09-25
updated: 2026-09-25
status: 已填充
---

## 第十二章

## 化学动力学基础(二)

本章基本要求

(1) 了解目前较常用的反应速率理论。特别是对碰撞理论和过渡态理论要知道它们分别采用的模型、推导过程中引进的假定、计算速率常数的公式及理论的优缺点。会利用这两个理论来计算一些简单反应的速率常数，掌握活化能、阈能和活化焓等能量之间的关系。

(2) 了解微观反应动力学的发展概况、常用的实验方法和该研究在理论上的意义。

(3) 了解溶液反应的特点和溶剂对反应的影响，会判断离子强度对不同反应速率的影响（即原盐效应）。了解扩散对反应的影响。

(4) 了解较常用的测试快速反应的方法, 学会用弛豫法来计算简单快速对峙反应的两个速率常数。

(5) 了解光化学反应的基本定律、光化学平衡与热化学平衡的区别以及这类反应的发展趋势和应用前景。掌握量子产率的计算和会处理简单的光化学反应动力学问题。

(6) 了解化学激光的原理、发展趋势和应用前景。

(7) 了解催化反应特别是酶催化反应的特点、催化剂之所以能改变反应速率的本质和常用催化剂的类型。

(8) 了解自催化反应的特点和产生化学振荡的原因。

## 12.1 碰撞理论

Arrhenius 根据实验从宏观的角度总结出了化学反应的动力学基本规律, 即 Arrhenius 公式, 他认为反应的速率常数与温度的关系取决于活化能 ( $E_{a}$ ) 和指前因子 A [又称为频率因子 (frequency factor)]。Arrhenius 所提出的这些基本概念为后来建立反应速率理论作出了重要贡献。人们希望能从理论上或从微观的角度对定律作出解释, 并希望能从理论上预言反应在给定条件下的速率常数。

在本章中将简要地介绍碰撞理论、过渡态理论和单分子反应的 Lindemann (林德曼) 理论等。

## 12.1 碰撞理论

在反应速率理论的发展过程中, 先后形成了碰撞理论、过渡态理论和单分子反应理论等, 这些理论都是动力学研究中的基本理论。

碰撞理论是 20 世纪初在气体分子动理论的基础上发展起来的。该理论认为, 发生化学反应的先决条件是反应物分子的碰撞接触, 但并非每一次碰撞都能导致反应发生。在热平衡系统中, 分子的平动能符合 Boltzmann 分布。如果互碰分子对的平动能不够大, 则碰撞不会导致反应发生, 分子对碰撞后随即分离。只有那些相对平动能在分子连心线上的分量超过某一临界值的分子对, 才能把平动能转化为分子内部的能量, 使旧键破裂而发生原子间的重新组合。这种能导致旧键破裂的碰撞称为有效碰撞 (effective collision)。碰撞理论认为, 只要知道分子的碰撞频率 (Z), 再求出可导致旧键破裂的有效碰撞在总碰撞中的分数 (q), 则从 Z 和 q 的乘积即可求得反应速率 (r) 和速率常数 (k)。

简单碰撞理论 (simple collision theory) 以硬球碰撞为模型, 导出宏观反应速率常数的计算公式, 故又称为硬球碰撞理论 (hard-sphere collision theory)。

## 双分子的互碰频率和速率常数的推导

两个分子的碰撞过程实质上是在分子的作用力下, 两个分子先互相接近, 接近到一定距离时, 它们之间开始产生斥力, 斥力随分子间距离的减小而很快增大, 之后分子就改变原来的方向而相互远离, 于是就完成了一次碰撞过程。两个分子的质心在碰撞时所能达到的最短距离称为有效直径 (或称为碰撞直径), 其数值往往稍稍大于分子本身的直径。

假定 A 分子和 B 分子都是硬球, 所谓硬球碰撞是指想象中的两个硬球只作弹性碰撞, 且忽略分子的内部结构。设单位体积中 A 的分子数为 $n_{A}$ , B 的分子数为 $n_{B}$ , 则根据气体分子动理论 (见上册第一章 1.7 节), 运动着的 A 分子和 B 分子在单位时间内的碰撞频率为

$$
Z _ {\mathrm{AB}} = \pi d _ {\mathrm{AB}} ^ {2} \sqrt {\frac {8 R T}{\pi \mu}} n _ {\mathrm{A}} n _ {\mathrm{B}}
$$

式中 $d_{AB}$ 代表 A 分子和 B 分子的半径之和； $\pi d_{AB}^{2}$ 称为碰撞截面 (collision cross-section); $\mu$ 为折合摩尔质量 (reduced molar mass)。

将单位体积中的分子数换算成物质的浓度:

$$
n _ {\mathrm{A}} = \frac {N _ {\mathrm{A}}}{V} \qquad n _ {\mathrm{B}} = \frac {N _ {\mathrm{B}}}{V}
$$

则

$$
c _ {\mathrm{A}} = \frac {n _ {\mathrm{A}}}{L} \qquad c _ {\mathrm{B}} = \frac {n _ {\mathrm{B}}}{L}
$$

代入式 (1.59), 得 A 分子和 B 分子之间的碰撞频率, 即

$$
Z _ {\mathrm{AB}} = \pi d _ {\mathrm{AB}} ^ {2} L ^ {2} \sqrt {\frac {8 R T}{\pi \mu}} c _ {\mathrm{A}} c _ {\mathrm{B}}\tag{12.1}
$$

若系统中只有一种分子, 则 A 分子与 A 分子之间的碰撞频率为

$$
Z _ {\mathrm{AA}} = 2 \pi d _ {\mathrm{AA}} ^ {2} \sqrt {\frac {R T}{\pi M _ {\mathrm{A}}}} n _ {\mathrm{A}} ^ {2}\tag{12.2}
$$

式中 $d_{AA}$ 是两个 A 分子的半径之和, 即 A 分子的直径; $M_{A}$ 是 A 分子的摩尔质量; $n_{A}$ 是单位体积中的 A 分子数 [参见第一章的式 (1.58)]。若单位体积中的 A 分子数用物质的量浓度表示, $c_{A} = \frac{n_{A}}{L}$ , 则式 (12.2) 可改写为

$$
Z _ {\mathrm{AA}} = 2 \pi d _ {\mathrm{AA}} ^ {2} L ^ {2} \sqrt {\frac {R T}{\pi M _ {\mathrm{A}}}} c _ {\mathrm{A}} ^ {2}\tag{12.3}
$$

若 A 分子和 B 分子的每次碰撞都能起反应, 则反应 $A + B \longrightarrow P$ 的反应速率为

$$
- \frac {\mathrm{d} n _ {\mathrm{A}}}{\mathrm{d} t} = Z _ {\mathrm{AB}}
$$

改用物质的量浓度表示为

$$
\mathrm{d} n _ {\mathrm{A}} = \mathrm{d} c _ {\mathrm{A}} \cdot L
$$

## 12.1 碰撞理论

$$
\begin{array}{r l} - \frac {\mathrm{d} c _ {\mathrm{A}}}{\mathrm{d} t} & = - \frac {\mathrm{d} n _ {\mathrm{A}}}{\mathrm{d} t} \cdot \frac {1}{L} = \frac {Z _ {\mathrm{AB}}}{L} \\ & = \pi d _ {\mathrm{AB}} ^ {2} L \sqrt {\frac {8 R T}{\pi \mu}} c _ {\mathrm{A}} c _ {\mathrm{B}} \end{array}
$$

已知

$$
- \frac {\mathrm{d} c _ {\mathrm{A}}}{\mathrm{d} t} = k c _ {\mathrm{A}} c _ {\mathrm{B}}
$$

则得

$$
k = \pi d _ {\mathrm{AB}} ^ {2} L \sqrt {\frac {8 R T}{\pi \mu}}\tag{12.4}
$$

这就是根据简单碰撞理论所导出的速率常数 $(k)$ 。

在常温常压下, A 分子和 B 分子的碰撞频率的数值约为 $10^{35} \, m^{-3} \cdot s^{-1}$ , 所以按式 (12.4) 计算得到的速率常数值要比实验值大得多。由此可见, 并不是每次碰撞都能发生反应, 即 $Z_{AB}$ 中只有一部分碰撞是能发生反应的有效碰撞。令 q 代表有效碰撞在 $Z_{AB}$ 中所占的分数, 则

$$
r = - \frac {\mathrm{d} c _ {\mathrm{A}}}{\mathrm{d} t} = \frac {Z _ {\mathrm{AB}}}{L} \cdot q\tag{12.5}
$$

现在只要找出有效碰撞分数 q 的表示式, 就能计算出速率常数。

根据分子能量分布的近似公式, 即 Boltzmann 公式, 能量具有 E 的活性分子在总分子中所占的分数 q 为

$$
q = \mathrm{e} ^ {- \frac {E}{R T}}\tag{12.6}
$$

故式 $(12.5)$ 可写为

$$
r = - \frac {\mathrm{d} c _ {\mathrm{A}}}{\mathrm{d} t} = \frac {Z _ {\mathrm{AB}}}{L} \cdot \mathrm{e} ^ {- \frac {E}{R T}}
$$

将式 (12.1) 代入后, 得

$$
r = \pi d _ {\mathrm{AB}} ^ {2} L \sqrt {\frac {8 R T}{\pi \mu}} \mathrm{e} ^ {- \frac {E}{R T}} c _ {\mathrm{A}} c _ {\mathrm{B}} = k c _ {\mathrm{A}} c _ {\mathrm{B}}\tag{12.7}
$$

碰撞理论根据气体分子动理论及 Arrhenius 分子反应活化能的概念, 导出了速率常数 $(k)$ 和分子反应速率 $(r)$ 的表达式。

根据式 $(12.7)$ ，反应的速率常数k应为

$$
k = \pi d _ {\mathrm{AB}} ^ {2} L \sqrt {\frac {8 R T}{\pi \mu}} \mathrm{e} ^ {- \frac {E}{R T}} = A \mathrm{e} ^ {- \frac {E}{R T}}\tag{12.8}
$$

式中 $A = \pi d_{AB}^{2} L \sqrt{\frac{8RT}{\pi \mu}}$ ，所以将 A 称为频率因子。式 (12.8) 也可写为

$$
k = A ^ {\prime} T ^ {\frac {1}{2}} \mathrm{e} ^ {- \frac {E}{R T}}
$$

在 $A'$ 中已不包括温度项, 对上式两边取对数后, 得

$$
\ln k = \ln A ^ {\prime} + \frac {1}{2} \ln T - \frac {E}{R T}
$$

将上式对温度 T 微分, 得

$$
\frac {\mathrm{d} \ln k}{\mathrm{d} T} = \frac {E + \frac {1}{2} R T}{R T ^ {2}}
$$

在一般情况下， $\frac{1}{2} RT$ 比 $E$ 要小得多，故可略而不计，因此得

$$
\frac {\mathrm{d} \ln k}{\mathrm{d} T} = \frac {E}{R T ^ {2}}\tag{12.9}
$$

这就是 Arrhenius 经验公式。因此, 碰撞理论不但解释了 $\ln k$ 与 $\frac{1}{T}$ 之间的线性关系, 并指出, 若以 $\ln k$ 对 $\frac{1}{T}$ 作图, 则应能得到很好的直线。

## \*硬球碰撞模型——碰撞截面与反应阈能

初期的碰撞理论对碰撞过程的描述较为简单, 因而后来又提出碰撞截面的概念, 并对碰撞过程作较精确的描述。

设 A 和 B 为两个没有结构的硬球分子, 质量分别为 $m_{A}$ 和 $m_{B}$ , 分子折合质量为 $\mu$ , A 和 B 的运动速度分别为 $u_{A}$ 和 $u_{B}$ 。运动着的 A 和 B 分子的总能量 E 为

$$
E = \frac {1}{2} m _ {\mathrm{A}} u _ {\mathrm{A}} ^ {2} + \frac {1}{2} m _ {\mathrm{B}} u _ {\mathrm{B}} ^ {2}
$$

但总能量 E 也可以考虑为质心整体运动的动能 ( $\varepsilon_{g}$ ) 和分子间相对运动能 ( $\varepsilon_{r}$ ) 之和, 即

$$
E = \varepsilon_ {\mathrm{g}} + \varepsilon_ {\mathrm{r}} = \frac {1}{2} (m _ {\mathrm{A}} + m _ {\mathrm{B}}) u _ {\mathrm{g}} ^ {2} + \frac {1}{2} \mu u _ {\mathrm{r}} ^ {2}\tag{12.10}
$$

式中 $u_{g}$ 代表质心的速度； $u_{r}$ 代表相对速度。质心动能 $\varepsilon_{g}$ 是两个分子在空间整体运动的动能，它对发生化学反应所需的能量没有贡献。而能够精确衡量两个分子互相趋近时能量大小的是相对平动能 $\varepsilon_{r}$ 。

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_200-399_images/71fe06cbaf58f517d468d5dfec08a9cb137eb31c7fd70e2401e74b7be73da44c.jpg)  
图 12.1 硬球碰撞模型示意图

若用相对速度 $u_{r}$ 代替 A 分子和 B 分子的运动速度 $u_{A}$ 和 $u_{B}$ ，则两个硬球碰撞运动可看作一个分子不动（如 A 分子），而另一个具有相对速度 $u_{r}$ 的分子（如 B 分子）向 A 分子运动，如图 12.1 所示。相对速度 $(u_{\mathrm{r}})$ 与连心线 AB（即 $d_{AB}$ ）之间的夹角为 $\theta$ 。通过 A, B 分子的质心分别作与相对速度 $u_{r}$ 平行的线，平行线之间的距离为 b。此 b 称为碰撞参数（impact parameter），表示两个分子接近的程度。 $b = d_{AB}\sin\theta$ ，当两个分子迎头碰撞时， $\theta = 0, b = 0$ ；当 $b > d_{AB}$ 时，不会发生碰撞。所以碰撞截面（collision cross section） $\sigma_{c}$ 为

$$
\sigma_ {\mathrm{c}} = \int_ {0} ^ {b _ {\max}} 2 \pi b \mathrm{d} b = \pi b _ {\max} ^ {2} = \pi d _ {\mathrm{AB}} ^ {2}\tag{12.11}
$$

凡是落在这个截面内的分子, 都可能发生碰撞。

分子碰撞的相对平动能为 $\frac{1}{2}\mu u_{r}^{2}$ ，它在连心线上的分量为 $\varepsilon_{r}^{\prime}$ ，可表示为

$$
\begin{array}{r l} & \varepsilon_ {\mathrm{r}} ^ {\prime} = \frac {1}{2} \mu (u _ {\mathrm{r}} \cos \theta) ^ {2} = \frac {1}{2} \mu u _ {\mathrm{r}} ^ {2} (1 - \sin^ {2} \theta) \\ & \qquad = \varepsilon_ {\mathrm{r}} \left(1 - \frac {b ^ {2}}{d _ {\mathrm{AB}} ^ {2}}\right) \end{array}\tag{12.12}
$$

只有当 $\varepsilon_{\mathrm{r}}^{\prime}$ 的值超过某一规定值 $\varepsilon_{\mathrm{c}}$ 时，这样的碰撞才是有效的，才是能导致反应的碰撞。 $\varepsilon_{\mathrm{c}}$ 称为能发生化学反应的临界能或阈能（threshold energy）。对于不同的反应，显然 $\varepsilon_{\mathrm{c}}$ 的值是不同的。故发生反应的必要条件是 $\varepsilon_{\mathrm{r}}^{\prime} \geqslant \varepsilon_{\mathrm{c}}$ ，即

$$
\varepsilon_ {\mathrm{r}} \left(1 - \frac {b ^ {2}}{d _ {\mathrm{AB}} ^ {2}}\right) \geqslant \varepsilon_ {\mathrm{c}}\tag{12.13}
$$

从式 (12.13) 可知, 当碰撞参数 $b$ 等于某一数值 $b_{\mathrm{r}}$ 时, 它正好使相对动能 $\varepsilon_{\mathrm{r}}$ 在连心线上的分量 $\varepsilon_{\mathrm{r}}^{\prime}$ 等于 $\varepsilon_{\mathrm{c}}$ , 则

$$
\varepsilon_ {\mathrm{r}} \left(1 - \frac {b _ {\mathrm{r}} ^ {2}}{d _ {\mathrm{AB}} ^ {2}}\right) = \varepsilon_ {\mathrm{c}}
$$

或

$$
b _ {\mathrm{r}} ^ {2} = d _ {\mathrm{AB}} ^ {2} \left(1 - \frac {\varepsilon_ {\mathrm{c}}}{\varepsilon_ {\mathrm{r}}}\right)\tag{12.14}
$$

这样, 当 $\varepsilon_{\mathrm{c}}$ 值一定时, 凡是碰撞参数 $b \leqslant b_{\mathrm{r}}$ 的碰撞都是有效的。据此, 反应截面的定义为

$$
\sigma_ {\mathrm{r}} \stackrel {\text { def }} {=} \pi b _ {\mathrm{r}} ^ {2} = \pi d _ {\mathrm{AB}} ^ {2} \left(1 - \frac {\varepsilon_ {\mathrm{c}}}{\varepsilon_ {\mathrm{r}}}\right)\tag{12.15}
$$

当 $\varepsilon_{r} \leqslant \varepsilon_{c}$ 时, $\sigma_{r} = 0$ ; 当 $\varepsilon_{r} > \varepsilon_{c}$ 时, $\sigma_{r}$ 的值随 $\varepsilon_{r}$ 的增大而增大, 如图 12.2 所示。
又因为 $\varepsilon_{r}=\frac{1}{2}\mu u_{r}^{2}$ ，故 $\sigma_{r}$ 也是 $u_{r}$ 的函数，即

$$
\sigma_ {\mathrm{r}} (u _ {\mathrm{r}}) = \pi d _ {\mathrm{AB}} ^ {2} \left(1 - \frac {2 \varepsilon_ {\mathrm{c}}}{\mu u _ {\mathrm{r}} ^ {2}}\right)\tag{12.16}
$$

反应截面是微观反应动力学中的基本参数, 反应的速率常数 k 及实验活化能 $E_{a}$ 等是宏观反应动力学参数。如何从反应截面求速率常数 k 和实验活化能 $E_{a}$ ，反映了微观与宏观反应之间的联系。

设 A 和 B 为两束相互垂直交叉的粒子 (原子或分子) 流, 由于单位体积中粒子数很低, 在交叉区域只发生单次碰撞, 如图 12.3 所示。

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_200-399_images/653163373d1c3a66dd1d0cecb3b73e5e9d7f610bfb8c29cd2dc03c61293dae9d.jpg)  
图 12.2 反应截面与阈能的关系

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_200-399_images/a886b4ee31eca06a8c28f1201e7ae051fb2c2c461c03329b5b61c71e40127518.jpg)  
图 12.3 两束粒子交叉示意图

A 和 B 的相对速度为 $u_{r}$ ，A 束的强度可表示为

$$
I _ {\mathrm{A}} = u _ {\mathrm{r}} \frac {N _ {\mathrm{A}}}{V}\tag{12.17}
$$

当 A 通过交叉区域时, 由于与 B 束粒子碰撞而被散射出交叉区, 使 A 束的强度 $I_{A}$ 下降。通过 dx 距离以后, A 束的强度损失 $-dI_{A}$ 应当正比于 A 束入射的强度 $I_{\mathrm{A}}(x)$ 、B 束的粒子密度 $\frac{N_{B}}{V}$ 和间距 dx, 即

$$
- \mathrm{d} I _ {\mathrm{A}} = \sigma (u _ {\mathrm{r}}) I _ {\mathrm{A}} (x) \frac {N _ {\mathrm{B}}}{V} \mathrm{d} x\tag{12.18}
$$

式中比例系数 $\sigma(u_{\mathrm{r}})$ 与相对速度 $u_{r}$ 有关, 且是碰撞频率的一种量度, 它具有面积的单位, 也就是碰撞截面。式 (12.18) 中 $I_{A}$ 的下降是由反应碰撞和非反应碰撞两部分造成的。如果只考虑由于反应碰撞而使 A 束的强度 $I_{A}$ 下降, 则用反应截面得

$$
(- \mathrm{d} I _ {\mathrm{A}}) _ {\mathrm{r}} = \sigma_ {\mathrm{r}} (u _ {\mathrm{r}}) I _ {\mathrm{A}} (x) \frac {N _ {\mathrm{B}}}{V} \mathrm{d} x\tag{12.19}
$$

因为 $I_{A}=u_{r}\frac{N_{A}}{V}$ ， $dI_{A}=u_{r}d\left(\frac{N_{A}}{V}\right)$ ， $u_{r}=\frac{dx}{dt}$ ，代入式 (12.19) 后，得

$$
- \frac {\mathrm{d} \left(\frac {N _ {\mathrm{A}}}{V}\right)}{\mathrm{d} t} = u _ {\mathrm{r}} \sigma_ {\mathrm{r}} (u _ {\mathrm{r}}) \frac {N _ {\mathrm{A}}}{V} \frac {N _ {\mathrm{B}}}{V} = k (u _ {\mathrm{r}}) \frac {N _ {\mathrm{A}}}{V} \frac {N _ {\mathrm{B}}}{V}\tag{12.20}
$$

从式 (12.20) 可知, 微观反应速率常数 $k(u_{\mathrm{r}})$ 是由反应物的相对速度和反应截面所决定的。即在式 (12.20) 中:

$$
k (u _ {\mathrm{r}}) = u _ {\mathrm{r}} \sigma_ {\mathrm{r}} (u _ {\mathrm{r}})\tag{12.21}
$$

在宏观反应系统中, 从微观的角度看, 碰撞分子有各种可能的相对速度, 对每个相对速度都存在着像式 (12.21) 所表达的微观反应速率常数, 这些不同相对速度的反应碰撞以不同的权重对宏观反应有所贡献。它们的反应碰撞速率常数的加权总和构成了宏观反应速率常数 $k(T)$ , 即

$$
\begin{array}{r l} k (T) & = f _ {1} k (u _ {1}) + f _ {2} k (u _ {2}) + f _ {3} k (u _ {3}) + \dots \\ & = \int_ {0} ^ {\infty} f (u _ {\mathrm{r}}, T) u _ {\mathrm{r}} \sigma_ {\mathrm{r}} (u _ {\mathrm{r}}) \mathrm{d} u _ {\mathrm{r}} \end{array}\tag{12.22}
$$

式中 $f_{1}$ 表示具有相对速度 $u_{1}$ 的碰撞分子对占总碰撞分子的分数（相当于统计权重）； $f(u_{\mathrm{r}}, T)$ 是相对速度的分布函数，设相对速度分布也可以用 Maxwell-Boltzmann 分布来表示：

$$
f (u _ {\mathrm{r}}, T) = 4 \pi \left(\frac {\mu}{2 \pi k _ {\mathrm{B}} T}\right) ^ {\frac {3}{2}} \exp \left(- \frac {\mu u _ {\mathrm{r}} ^ {2}}{2 k _ {\mathrm{B}} T}\right) u _ {\mathrm{r}} ^ {2}\tag{12.23}
$$

式中 $k_{\mathrm{B}}$ 为Boltzmann常数。将式(12.23)代入式(12.22)，得

$$
k (T) = 4 \pi \left(\frac {\mu}{2 \pi k _ {\mathrm{B}} T}\right) ^ {\frac {3}{2}} \int_ {0} ^ {\infty} u _ {\mathrm{r}} ^ {3} \exp \left(- \frac {\mu u _ {\mathrm{r}} ^ {2}}{2 k _ {\mathrm{B}} T}\right) \sigma_ {\mathrm{r}} (u _ {\mathrm{r}}) \mathrm{d} u _ {\mathrm{r}}\tag{12.24}
$$

若用碰撞的相对动能 $\varepsilon_{r}$ 来代替相对速度, 则

$$
\varepsilon_ {\mathrm{r}} = \frac {1}{2} \mu u _ {\mathrm{r}} ^ {2} \quad \mathrm{d} \varepsilon_ {\mathrm{r}} = \mu u _ {r} \mathrm{d} u _ {\mathrm{r}}
$$

代入式 (12.24), 得

$$
k (T) = \left(\frac {1}{\pi \mu}\right) ^ {\frac {1}{2}} \left(\frac {2}{k _ {\mathrm{B}} T}\right) ^ {\frac {3}{2}} \int_ {\varepsilon_ {\mathrm{c}}} ^ {\infty} \varepsilon_ {\mathrm{r}} \exp \left(- \frac {\varepsilon_ {\mathrm{r}}}{k _ {\mathrm{B}} T}\right) \sigma_ {\mathrm{r}} (\varepsilon_ {\mathrm{r}}) \mathrm{d} \varepsilon_ {\mathrm{r}}\tag{12.25}
$$

式 (12.24) 或式 (12.25) 将微观的反应截面 $\sigma_{\mathrm{r}}$ 与宏观的反应速率常数 $k(T)$ 这两个基本参数联系起来了。由微观反应截面的计算和测量, 可以得到宏观反应的速率常数, 实现了从微观向宏观的过渡。但是, 我们还无法从宏观反应的速率常数去推导有关反应截面的信息。

若将硬球碰撞模型的反应截面的表示式 (不同的碰撞模型, $\sigma_{r}$ 的表示式也不同), 即将式 (12.15) 代入式 (12.25), 则得到简单碰撞理论的反应速率常数 $k_{SCT}$ , 即

$$
\begin{array}{l} k _ {\mathrm{SCT}} (T) = \left(\frac {1}{\pi \mu}\right) ^ {\frac {1}{2}} \left(\frac {2}{k _ {\mathrm{B}} T}\right) ^ {\frac {3}{2}} \int_ {\varepsilon_ {\mathrm{c}}} ^ {\infty} \varepsilon_ {\mathrm{r}} \exp \left(- \frac {\varepsilon_ {\mathrm{r}}}{k _ {\mathrm{B}} T}\right) \pi d _ {\mathrm{AB}} ^ {2} \cdot \left(1 - \frac {\varepsilon_ {\mathrm{c}}}{\varepsilon_ {\mathrm{r}}}\right) \mathrm{d} \varepsilon_ {\mathrm{r}} \\ = \pi d _ {\mathrm{AB}} ^ {2} \sqrt {\frac {8 k _ {\mathrm{B}} T}{\pi \mu}} \exp \left(- \frac {\varepsilon_ {\mathrm{c}}}{k _ {\mathrm{B}} T}\right) \end{array} \tag {7}\tag{12.26}
$$

如果式 (12.20) 中 $\frac{N_{\mathrm{A}}}{V}$ 和 $\frac{N_{\mathrm{B}}}{V}$ 也用 $c_{\mathrm{A}}$ 和 $c_{\mathrm{B}}$ 表示, 则式 (12.26) 可写为

$$
k _ {\mathrm{SCT}} (T) = \pi d _ {\mathrm{AB}} ^ {2} L \sqrt {\frac {8 k _ {\mathrm{B}} T}{\pi \mu}} \exp \left(- \frac {\varepsilon_ {\mathrm{c}}}{k _ {\mathrm{B}} T}\right)\tag{12.27}
$$

对照式 (12.6) 可知, 有效的反应碰撞占总碰撞的分数为 $\exp \left(-\frac{\varepsilon_{\mathrm{c}}}{k_{\mathrm{B}}T}\right)$ , 对于 $1 \mathrm{~mol}$ 粒子, 则为 $\exp \left(-\frac{E_{\mathrm{c}}}{RT}\right)$ 。根据式 (12.26) 或式 (12.27) 就可以计算宏观反应速率常数 $k(T)$ 值。对于相同分子的双分子反应, 根据式 (12.3), 显然 $k_{\mathrm{SCT}}(T)$ 的表示式为

$$
k _ {\mathrm{SCT}} (T) = \frac {\sqrt {2}}{2} \pi d _ {\mathrm{AA}} ^ {2} L \sqrt {\frac {8 R T}{\pi M _ {\mathrm{A}}}} \exp \left(- \frac {\varepsilon_ {\mathrm{c}}}{k _ {\mathrm{B}} T}\right)\tag{12.28}
$$

\*反应阈能与实验活化能的关系

根据实验活化能的定义

$$
E _ {\mathrm{a}} = R T ^ {2} \frac {\mathrm{dln} k (T)}{\mathrm{d} T}
$$

将式 (12.27) 代入, 得

$$
E _ {\mathrm{a}} = R T ^ {2} \left(\frac {1}{2 T} + \frac {E _ {\mathrm{c}}}{R T ^ {2}}\right) = E _ {\mathrm{c}} + \frac {1}{2} R T\tag{12.29}
$$

如果 $E_{\mathrm{c}} \gg \frac{1}{2} RT$ ，则可认为 $E_{\mathrm{a}} \approx E_{\mathrm{c}}$ ，但两者的物理意义是不同的， $E_{\mathrm{c}}$ 才是与温度无关的常数。若用 $E_{\mathrm{a}}$ 代替 $E_{\mathrm{c}}$ ，则式 (12.27) 可改写为

$$
k (T) = \pi d _ {\mathrm{AB}} ^ {2} L \sqrt {\frac {8 k _ {\mathrm{B}} T \mathrm{e}}{\pi \mu}} \exp \left(- \frac {E _ {\mathrm{a}}}{R T}\right)\tag{12.30}
$$

式中 $\mathrm{e} = 2.718$ ，是自然对数的底数。对照 Arrhenius 公式，指前因子 $A$ 所代表的实际意义应是

$$
A = \pi d _ {\mathrm{AB}} ^ {2} L \sqrt {\frac {8 k _ {\mathrm{B}} T \mathrm{e}}{\pi \mu}}\tag{12.31}
$$

式 (12.31) 中的所有参数均不必从动力学实验中求得, 只要通过计算就可得到指前因子 $A$ 的值。如果将 $A$ 的计算值与实验结果进行比较, 可以检验碰撞理论模型的适用程度。

## 例12.1

在 600 K 时, 反应 $2NOCl \xlongequal{\quad} 2NO + Cl_{2}$ 的速率常数 k 值为 $60\ mol^{-1} \cdot dm^{3} \cdot s^{-1}$ , 实验活化能为 $105.5\ kJ \cdot mol^{-1}$ 。已知 NOCl 分子直径为 0.283 nm, 摩尔质量为 $65.5\ g \cdot mol^{-1}$ 。试计算反应在该温度下的速率常数。

解

$$
\begin{array}{r l} & E _ {\mathrm{c}} = E _ {\mathrm{a}} - \frac {1}{2} R T \\ & \quad = \left(1 0 5. 5 - \frac {1}{2} \times 8. 3 1 4 \times 6 0 0 \times 1 0 ^ {- 3}\right) \mathrm{kJ} \cdot \mathrm{mol} ^ {- 1} = 1 0 3. 0 \mathrm{kJ} \cdot \mathrm{mol} ^ {- 1} \\ & k (T) = 2 \pi d _ {\mathrm{AA}} ^ {2} L \sqrt {\frac {R T}{\pi M}} \exp \left(- \frac {E _ {\mathrm{c}}}{R T}\right) \\ & \quad = 2 \times 3. 1 4 \times (2. 8 3 \times 1 0 ^ {- 1 0} \mathrm{m}) ^ {2} \times 6. 0 2 2 \times 1 0 ^ {2 3} \mathrm{mol} ^ {- 1} \times \\ & \quad \sqrt {\frac {8 . 3 1 4 \times 6 0 0 \mathrm{J} \cdot \mathrm{mol} ^ {- 1}}{3 . 1 4 \times 6 5 . 5 \times 1 0 ^ {- 3} \mathrm{kg} \cdot \mathrm{mol} ^ {- 1}}} \exp \left(\frac {- 1 0 3 0 0 0 \mathrm{J} \cdot \mathrm{mol} ^ {- 1}}{8 . 3 1 4 \times 6 0 0 \mathrm{J} \cdot \mathrm{mol} ^ {- 1}}\right) \\ & \quad = 5. 0 9 \times 1 0 ^ {- 2} \mathrm{mol} ^ {- 1} \cdot \mathrm{m} ^ {3} \cdot \mathrm{s} ^ {- 1} = 5 0. 9 \mathrm{mol} ^ {- 1} \cdot \mathrm{dm} ^ {3} \cdot \mathrm{s} ^ {- 1} \end{array}
$$

计算结果与实验值符合得比较好。

概率因子

对于一些常见的反应, 用上述理论计算所得的 $k(T)$ 值和 $A$ 值与实验值基本相符。但也有不少反应, 理论计算所得的速率常数值要比实验值大, 有时甚至大很多。例如, 溶液中的一些反应, 计算结果比实验值约大 $10^{5}$ 倍, 使碰撞理论遇到了困难。有一个时期人们认为这是溶剂的影响所致, 但是后来发现有些气相反应的计算结果也偏高。为了解决这一困难, 人们又在公式中增加一个校正因子 $P$ , 即

$$
k (T) = P A \exp \left(- \frac {E _ {\mathrm{a}}}{R T}\right)\tag{12.32}
$$

式中 $P$ 称为概率因子 (probability factor) 或空间因子 (steric factor), $P$ 的数值可以从 $10^{-9}$ 变到大于 1, 见表 12.1。 $P$ 中包括了降低分子有效碰撞的所有各种因素, 例如对于复杂分子, 虽已活化, 但仅限于在某一特定的方位上相碰才是有效的碰撞, 因而降低了反应的速率。又如, 当两个分子相互碰撞时, 能量高的分子将一部分能量传给能量低的分子, 这种传递作用需要一定的碰撞延续时间。虽然碰撞分子有足够的能量, 但若分子碰撞的延续时间不够长, 则能量来不及彼此传递, 两个接触的分子就分开了, 因此使能量较低的分子达不到活化, 因而构成了无效的碰撞, 也就不可能引起反应。或者碰撞后分子虽获得了能量, 但还需要一定时间进行内部能量的传递以使最弱的键断裂, 但是在未达到这个时刻以前, 分子又与其他分子互碰而失去了活化能, 从而也构成无效碰撞, 影响了反应的速率。对于复杂的分子, 化学键必须从一定的部位断裂。倘若在该化学键的附近有较大的原子团, 则由于空间效应, 一定会影响该化学键与其他分子相碰撞的机会, 因而也降低了反应速率。以上种种理由只能说明，P 是碰撞数的一个校正项。但是为什么 P 的变化幅度有如此之大，则并无十分恰当的解释，因而 P 的物理意义显得并不十分明确。

表 12.1 某些双分子反应的活化能、指前因子和概率因子

<table><tr><td rowspan="2">反应</td><td rowspan="2"> $\frac{E_a}{kJ·mol^{-1}}$ </td><td colspan="2"> $\lg[A/(mol^{-1}·dm^3·s^{-1})]$ </td><td rowspan="2">概率因子P</td></tr><tr><td>计算值</td><td>实验值</td></tr><tr><td> $2NO_2 \longrightarrow 2NO + O_2$ </td><td>111.3</td><td>8.42</td><td>9.85</td><td>0.038</td></tr><tr><td> $2NOCl \longrightarrow 2NO + Cl_2$ </td><td>107.9</td><td>9.51</td><td>9.47</td><td>1.1</td></tr><tr><td> $NO + O_3 \longrightarrow NO_2 + O_2$ </td><td>9.6</td><td>7.80</td><td>9.90</td><td>0.008</td></tr><tr><td> $Br· + H_2 \longrightarrow HBr + H·$ </td><td>73.6</td><td>9.31</td><td>10.23</td><td>0.12</td></tr><tr><td> $·CH_3 + H_2 \longrightarrow CH_4 + H·$ </td><td>41.8</td><td>7.25</td><td>10.27</td><td> $9.5 × 10^{-4}$ </td></tr><tr><td> $·CH_3 + CHCl_3 \longrightarrow CH_4 + ·CCl_3$ </td><td>24.3</td><td>6.10</td><td>10.18</td><td> $8.3 × 10^{-5}$ </td></tr><tr><td>2-环戊二烯 → 二聚物</td><td>60.7</td><td>3.39</td><td>9.91</td><td> $3 × 10^{-7}$ </td></tr></table>

在碰撞理论中, 把分子看成没有结构的刚球, 模型过于简单, 这使这个理论的准确程度有一定的局限性 (以后虽对碰撞的模型作了一些修正, 但其基本情况仍没有多大改变)。碰撞理论对 Arrhenius 经验公式中的指数项、指前因子及阈能都提出了较明确的物理意义, 但却未能提出其计算方法, 因此用碰撞理论来计算速率常数 $k$ 值时, 阈能还必须由实验活化能求得, 这意味着应用碰撞理论的公式时, 只能以实验测定的活化能代替碰撞理论中的活化能, 而要求得实验中的活化能需先测定一系列温度下的速率常数。这是与能预言速率常数 (即从理论上计算速率常数) 相悖的, 因此这一理论也还是半经验的。虽然如此, 碰撞理论在反应理论中毕竟起了很大作用, 解释了一些实验事实, 它所提出的一些概念至今仍十分有用, 它为我们描绘了一幅虽然粗糙但十分明确的反应图像。

## 12.2 过渡态理论

碰撞理论采用硬球模型, 从经典力学的角度进行理论推导。外部运动的模型清晰, 但却忽视了分子的内部结构和内部运动, 因此所得到的结果必然过于简单。

过渡态理论 (transition state theory, TST) 又称为活化络合物理论, 这个理论是 1935 年后由 Eyring、Polanyi 等人在统计力学和量子力学发展的基础上提出来的。在理论形成的过程中曾引入了一些模型和假设, 它的大意是: 化学反应不是只通过简单碰撞就可完成的, 而是要经过一个由反应物分子以一定的构型存在的过渡态, 在形成过渡态的过程中要考虑分子的内部结构、内部运动, 并认为反应物分子不只是在碰撞接触瞬间, 而是在相互接触的全过程中都存在着相互作用, 系统的势能一直在变化。要形成这个过渡态需要一定的活化能, 故过渡态又称为活化络合物或活化复合物。活化络合物与反应物分子之间建立化学平衡, 反应的速率由活化络合物转化成产物的速率来决定。这个理论还认为, 反应物分子之间相互作用的势能是分子间相对位置的函数, 在反应物转变为产物的过程中, 系统的势能不断变化。可以画出反应过程中势能变化的势能面图, 从中找出最佳的反应途径。过渡态理论原则上提供了一种计算反应速率的方法, 只要知道分子的某些基本物性, 如振动频率、质量、核间距离等等, 即可计算某反应的速率常数, 故这个理论也称为绝对反应速率理论 (absolute rate theory, ART)。

势能面

原子间相互作用表现为原子间有势能 $E_{p}$ 存在, 势能 $E_{p}$ 的值是原子的核间距 r 的函数。

$$
E _ {\mathrm{p}} = E _ {\mathrm{p}} (r)\tag{12.33}
$$

势能函数的获得一般有两种方法: 一是原则上可用量子力学进行理论计算, 但这种方法即使是对最简单的双原子分子系统也是不容易的, 对多原子系统至今尚未获得较完整的势能表达式。二是用经验公式表示, 可以获得足够准确的势能数据。Morse 的势能 $E_{\mathrm{p}}(r)$ 公式是对双原子分子最常用的经验公式:

$$
E _ {\mathrm{p}} (r) = D _ {\mathrm{e}} \{\exp [ - 2 a (r - r _ {0}) ] - 2 \exp [ - a (r - r _ {0}) ] \}\tag{12.34}
$$

式中 $r_0$ 为分子中原子间的平衡核间距； $D_{\mathrm{e}}$ 为势能曲线的井深； $a$ 为与分子结构特性有关的常数。根据Morse经验公式可画出双原子分子的Morse势能曲线，如图12.4所示。系统的势能在平衡核间距 $r_0$ 处有最低点。当 $r < r_0$ 时，核间有排斥力，当 $r > r_0$ 时，核间有吸引力，即化学键力。如果分子处于振动基态，即振动量子数 $v = 0$ 的状态，这时要把基态分子解离为孤立原子需要的能量为 $D_0$ ，显然 $D_0 = D_{\mathrm{e}} - E_0$ （零点能）， $D_{0}$ 的值可从光谱数据得到。分子中的价电子所处的能级不同，则势能曲线也不同，一般考虑的都是电子处于基态的势能曲线。

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_200-399_images/a4958dc399dc7ab052e87395a7c3b1351505290e372b2fe849fd4841cf001271.jpg)  
图 12.4 双原子分子的 Morse 势能曲线

现以简单的反应为例:

$$
\mathrm{A} + \mathrm{B} - \mathrm{C} \rightleftharpoons [ \mathrm{A} - - - \mathrm{B} - - - \mathrm{C} ] ^ {\text {辛}} \longrightarrow \mathrm{A} - \mathrm{B} + \mathrm{C}
$$

式中 A 代表单原子分子; B—C 代表双原子分子。当 A 原子接近 B—C 分子时,就开始使 B—C 分子间的键减弱, 同时, 开始生成新的 A—B 键。而在这个过程未完成之前, 系统形成一个过渡态即活化络合物 $[A---B---C]^{\neq}$ , 此时前一个键尚未完全断开, 后一个键又未完全形成。在这个过程中, 反应系统的势能变化要用三个参数来描述, 即 $E_{\mathrm{p}} = E_{\mathrm{p}}(r_{\mathrm{AB}}, r_{\mathrm{BC}}, r_{\mathrm{AC}})$ ; 也可以是 $E_{\mathrm{p}} = E_{\mathrm{p}}(r_{\mathrm{AB}}, r_{\mathrm{BC}}, \angle ABC)$ , 参阅图 12.5。

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_200-399_images/7a89ce1d4df9d42a9eebd4ca6fbc2dac8cafbfe0d4f5ceb93ae129d55267e4fa.jpg)  
图 12.5 三原子系统的位置关系

其能量图要用四维空间中一个曲面来表示, 此曲面称为势能面 (potential energy surface, PES), 四维空间的图当然无法画出。如果表示势能面的三个参数中有一个被固定, 设 $\angle ABC = 180^{\circ}$ , 即通常所称的共线碰撞 (colinear collision), 此时活化络合物为线形分子, 则势能变化可用三维空间中的曲面表示, 如图 12.6 所示。随着 $r_{\mathrm{AB}}$ 和 $r_{\mathrm{BC}}$ 的不同, 势能值也不同, 这些不同的点在空间构成了高低不平的曲面, 犹如起伏的山峰。这个势能面有两个山谷, 山谷的两个低谷口分别相应于反应的始态和终态 (相应于图中的 $R$ 点和 $P$ 点)。连接这两个山谷间的山脊顶点 (即 $RP$ 连线中的最高点 $T^{\pm}$ ) 是势能面上的鞍点 (saddle point)。反应物从左山谷的谷底, 沿着山谷爬上鞍点, 这时形成活化络合物, 用 “ $T^{\pm}$ ” 表示, 然后再沿右边山谷下降到右边的谷底, 形成产物, 其所经路线如图中虚线 $R---T^{\pm}---P$ 所示。

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_200-399_images/eb4ff2d11682f004b183f01a7da0a9052c11ace2b3e2c5ab79c52aaa5005950b.jpg)  
图 12.6 A + B - C → A - B + C 反应势能面示意图

这是一条最低能量的反应途径, 称为反应坐标 (reaction coordinate)。与坐标原点 O 相对一侧的 D 点势能很高, 它相应于完全解离成原子的状态, 即 A + B +

C。图中 R 点代表反应的始态 (即 A + B — C)，在左前方的切面图上，R 是势能的最低点。在右前方的切面图上，P 是反应的终态 (即 AB + C)，P 点也是该势能切面的最低点。当反应开始进行后， $r_{AB}$ 和 $r_{BC}$ 开始变化，物系点沿 $R --- T^{\pm}$ 线上升，到达 $T^{\pm}$ 点后，又沿 $T^{\pm} --- P$ 线下降，直到 P 点。

如果把势能面上的等势能线 (类似于地图上的等高线) 投射到底面上, 就得到图 12.7。图中曲线代表相同能量的投影, 线上的数字表示每一条等势能曲线的能量数值, 数字越大, 则势能越高 (为了比较其大小, 图中的数字都是虚拟的数值)。作用前系统 (即 A + BC) 的能量处于图中的最低点 R 点, 反应产物 (AB + C) 的能量处于另一最低点 P 点, $T^{\neq}$ 点相当于活化络合物所在位置, D 点 (在图中右上方) 或更远处代表 A + B + C, O 点与 D 点的能量均比 $T^{\neq}$ 点的高。这个势能面模型, 很像一个马鞍, 原点 O 和 D 点相当于马鞍前后的两个高峰的切点, 如果连接 $O---T^{\neq}---D$ 三点, 则将是一条凹形曲线, $T^{\neq}$ 点是曲线的最低点。R 点和 P 点相当于两个脚蹬, $T^{\neq}$ 点相当于马鞍中心, 倘若连接 $R---T^{\neq}---P$ 线, 则是一条凸形曲线, $T^{\neq}$ 点是该曲线的最高点, 即 $T^{\neq}$ 点在 $R---T^{\neq}---P$ 线上是最高点, 在 $O---T^{\neq}---D$ 线上是最低点, 相当于马鞍的中心, 所以用 “马鞍点” 来表示活化络合物 $T^{\neq}$ 是一个十分形象化的表示。

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_200-399_images/ffd7f483ecd0c719785978c50cc107463eb72030f6de561dbf900e375f5149ef.jpg)  
图 12.7 势能面投影示意图

如果以反应坐标为横坐标, 势能为纵坐标, 作平行于反应进程的势能面的剖面图, 得图 12.8。从图 12.8 可以看出, 从反应物 A + BC 到产物 AB + C, 沿反应进程通过鞍点前进, 这是能量最低的通道, 但也必须越过势垒 $E_{b}, E_{b}$ 是活化络合物与反应物两者最低势能之差值, 两者零点能之间的差值为 $E_{0}$ 。势能垒的存在从理论上表明了实验活化能 $E_{a}$ 的实质。

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_200-399_images/b4a72f29b612b53936d56556ed315243fa59a632a2b5e6e49a93f4bf7a9a33a5.jpg)  
图12.8 势能面的剖面图

## 由过渡态理论计算反应速率常数

过渡态理论是以反应系统的势能面为基础, 并认为从反应物向产物转化的过程中必须获得一些能量, 以越过反应进程中的能垒而形成活化络合物 (即过渡态), 然后再通过活化络合物转化成产物。活化络合物的浓度可由它与反应物达成化学平衡的假设来求算。反应物一旦转变成活化络合物, 就会向产物转化, 也就是说过渡态是处于反应物向产物转化的一个无返回点 (point of no return) (对于某些反应, 活化络合物也有可能再分解回到反应物状态, 这时在计算时要乘上一个系数, 本书中暂不考虑这种情况)。活化络合物向产物转化是整个反应的决速步骤, 即活化络合物的分解速率可作为整个反应的速率。在这个基础上, 再来讨论如何计算速率常数。仍以反应 $A + B - C \longrightarrow A - B + C$ 为例:

$$
\begin{array}{r l} \mathrm{A} + \mathrm{B} - \mathrm{C} & \xrightarrow {K _ {c} ^ {\neq}} [ \mathrm{A} - \dots \mathrm{B} - \dots \mathrm{C} ] ^ {\neq} \longrightarrow \mathrm{A} - \mathrm{B} + \mathrm{C} \\ K _ {c} ^ {\neq} & = \frac {[ \mathrm{A} - \dots \mathrm{B} - \dots \mathrm{C} ] ^ {\neq}}{[ \mathrm{A} ] [ \mathrm{BC} ]} \end{array}\tag{12.35}
$$

设 $[\mathrm{A} - - \mathrm{B} - - \mathrm{C}]^{\text{※}}$ 为线形三原子分子, 它有 3 个平动自由度, 2 个转动自由度, 其振动自由度为 $3n - 5 = 4$ (式中 $n$ 为分子中的原子数, $n = 3$ ), 其中有两个是稳定的弯曲振动, 见图 12.9(c)(d), 一个是对称伸缩振动, 见图 12.9(a), 这些都不会导致活化络合物分解。而有一种不对称伸缩振动是无回收力的, 如图 12.9(b) 所示, 它将导致活化络合物分解, 则反应速率也就是活化络合物的分解速率, 可表示为

$$
\begin{array}{r l} r & = - \frac {\mathrm{d} [ \mathrm{A} - - \mathrm{B} - - \mathrm{C} ] ^ {\mp}}{\mathrm{d} t} = \nu [ \mathrm{A} - - \mathrm{B} - - \mathrm{C} ] ^ {\mp} \\ & = \nu K _ {c} ^ {\mp} [ \mathrm{A} ] [ \mathrm{BC} ] \end{array}\tag{12.36}
$$

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_200-399_images/fdf9e4c523a7851aa382b38af5f1cfc0eaf09d93490b68fb1958fa138eef0fa5.jpg)

又因

$$
r = k [ \mathrm{A} ] [ \mathrm{BC} ]
$$

则速率常数

$$
k = \nu K _ {c} ^ {\neq}
$$

式中 $\nu$ 为不对称伸缩振动的频率。如再知道平衡常数 $K_{c}^{\approx}$ 的值，就可算出速率常数 k 值。 $K_{c}^{\approx}$ 的值可以用统计热力学所给出的计算平衡常数的公式根据微观数据进行计算，也可以用热力学的方法，用热力学函数的变化值而求得。首先介绍前者。

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_200-399_images/998ef402082a85255f7c61a6520869cf53c70dd73f78e17c1e3656c056deecf8.jpg)

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_200-399_images/db5e4d4448f18b6f4214761919cb49a3263f3cc78f4504de07391de288d85dc9.jpg)

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_200-399_images/881b7083076e653bb94ce14cf0931f4a5a696ca6854ad9c61fd63b2b54925f1e.jpg)  
图 12.9 三原子系统的振动方式

根据统计热力学在化学平衡中的应用, 已知计算平衡常数的公式为

$$
K _ {c} ^ {\neq} = \frac {[ \mathrm{A} - - - \mathrm{B} - - - \mathrm{C} ] ^ {\neq}}{[ \mathrm{A} ] [ \mathrm{BC} ]} = \frac {q ^ {\neq}}{q _ {\mathrm{A}} q _ {\mathrm{BC}}} = \frac {f ^ {\neq}}{f _ {\mathrm{A}} f _ {\mathrm{BC}}} \exp \left(- \frac {E _ {0}}{R T}\right)\tag{12.37}
$$

式中 q 是不包括体积项 V 的分子总配分函数；f 是不包括零点能和体积项 V 的分子配分函数； $E_{0}$ 是活化络合物的零点能与反应物零点能之差。如果把活化络合物中相应于不对称伸缩振动的自由度再分出来，即令

$$
f ^ {\neq} = f ^ {\neq \prime} \frac {1}{1 - \exp \left(- \frac {h \nu}{k _ {\mathrm{B}} T}\right)}\tag{12.38}
$$

式中 $k_{B}$ 是 Boltzmann 常数。由于不对称伸缩振动不稳定，它对应的频率比一般的振动频率低，即 $h\nu \ll k_{B}T$ ，故可作如下近似：

$$
\frac {1}{1 - \exp \left(- \frac {h \nu}{k _ {\mathrm{B}} T}\right)} \approx \frac {k _ {\mathrm{B}} T}{h \nu}
$$

则式 (12.38) 为

$$
f ^ {\mp} = f ^ {\mp \prime} \frac {k _ {\mathrm{B}} T}{h \nu}\tag{12.39}
$$

将式 (12.39) 代入式 (12.37), 后再代入 $k = \nu K_{c}^{\pm}$ 的表示式, 得

$$
k = \nu K _ {c} ^ {\neq} = \nu \frac {k _ {\mathrm{B}} T}{h \nu} \frac {f ^ {\neq \prime}}{f _ {\mathrm{A}} f _ {\mathrm{BC}}} \exp \left(- \frac {E _ {0}}{R T}\right)
$$

$$
= \frac {k _ {\mathrm{B}} T}{h} \frac {f ^ {\neq \prime}}{f _ {\mathrm{A}} f _ {\mathrm{BC}}} \exp \left(- \frac {E _ {0}}{R T}\right)\tag{12.40}
$$

式 (12.40) 就是用统计热力学方法处理的过渡态理论计算速率常数的表示式, 式中 $\frac{k_{\mathrm{B}}T}{h}$ 在一定温度下为定值, 在常温下其数量级约为 $10^{13}$ , 单位是 $\mathrm{s}^{-1}$ 。这个公式也可以推广使用于其他基元反应, 一般可写为

$$
k = \frac {k _ {\mathrm{B}} T}{h} \frac {f ^ {\neq \prime}}{\prod_ {\mathrm{B}} f _ {\mathrm{B}}} \exp \left(- \frac {E _ {0}}{R T}\right)\tag{12.41}
$$

式中 $\prod_{B} f_{B}$ 表示所有反应物种 B 的配分函数 $f_{B}$ 的连乘积。

任何分子都有 3 个平动自由度, 双原子分子和由 n 个原子组成的线形多原子分子有 2 个转动自由度, $(3n-5)$ 个振动自由度。非线形多原子分子有 3 个转动自由度, $(3n-6)$ 个振动自由度。在活化络合物中, 有一个不对称伸缩振动自由度用于其分解, 则其总的振动自由度要比正常分子少一个。例如, 对于反应

$$
\mathrm{A} (\text {单原子}) + \mathrm{B} (\text {单原子}) \rightleftharpoons [ \mathrm{A} - - - \mathrm{B} ] ^ {\pm} (\text {双原子})
$$

$$
k = \frac {k _ {\mathrm{B}} T}{h} \frac {(f _ {\mathrm{t}} ^ {3} f _ {\mathrm{r}} ^ {2}) ^ {\mp}}{(f _ {\mathrm{t}} ^ {3}) _ {\mathrm{A}} (f _ {\mathrm{t}} ^ {3}) _ {\mathrm{B}}} \exp \left(- \frac {E _ {0}}{R T}\right)\tag{12.42}
$$

$[\mathrm{A} - - \mathrm{B}]^{\mp}$ 的振动自由度 $= (3\times 2 - 5) - 1 = 0$ ，即 $[\mathrm{A} - - \mathrm{B}]^{\mp}$ 仅有的一个振动自由度用于活化络合物的分解。若反应为

$$
\begin{array}{r l}&{\mathrm{A} (N _ {\mathrm{A}}, \text {非线形多原子分子}) + \mathrm{B} (N _ {\mathrm{B}}, \text {非线形多原子分子}) \rightleftharpoons}\\&{[ \mathrm{A} - - - \mathrm{B} ] ^ {\neq} (N _ {\mathrm{A}} + N _ {\mathrm{B}}, \text {非线形多原子分子})}\end{array}
$$

$N_{A}$ 和 $N_{B}$ 分别为 A 和 B 分子中的原子数, 则

$$
k = \frac {k _ {\mathrm{B}} T}{h} \frac {[ f _ {\mathrm{t}} ^ {3} f _ {\mathrm{r}} ^ {3} f _ {\mathrm{v}} ^ {3 (N _ {\mathrm{A}} + N _ {\mathrm{B}}) - 7} ] ^ {\neq}}{(f _ {\mathrm{t}} ^ {3} f _ {\mathrm{r}} ^ {3} f _ {\mathrm{v}} ^ {3 N _ {\mathrm{A}} - 6}) _ {\mathrm{A}} (f _ {\mathrm{t}} ^ {3} f _ {\mathrm{r}} ^ {3} f _ {\mathrm{v}} ^ {3 N _ {\mathrm{B}} - 6}) _ {\mathrm{B}}} \exp \left(- \frac {E _ {0}}{R T}\right)\tag{12.43}
$$

原则上只要知道分子的质量、转动惯量、振动频率等微观物理量 (有些可从光谱数据获得), 就可用统计热力学的方法求出配分函数, 从而计算速率常数 $k$ 值。但是, 由于还不可能直接获得过渡态的光谱数据, 所以只有在准确描绘势能面的基础上, 才有可能计算 $f^{\approx}$ 项。式中 $E_0$ 值也可从势能面上势垒的值 $E_b$ 及零点能求得:

$$
E _ {0} = E _ {\mathrm{b}} + \left[ \frac {1}{2} h \nu_ {0} ^ {\neq} - \frac {1}{2} h \nu_ {0} (\mathrm{反应物}) \right] L\tag{12.44}
$$

式中 $\nu_{0}^{\neq}$ 和 $\nu_{0}$ (反应物) 分别为活化络合物和反应物的基态振动频率。因此, 从式 (12.42) 或式 (12.43), 原则上可不通过动力学实验数据就能计算出速率常数的理论值, 这就是过渡态理论又被称为绝对反应速率理论 (absolute reaction rate theory) 的缘故。

过渡态理论的热力学处理方法是用反应物转变成活化络合物过程中的热力学函数的变化值 $\Delta_{r}^{\neq}G_{m}^{\ominus}, \Delta_{r}^{\neq}S_{m}^{\ominus}$ 和 $\Delta_{r}^{\neq}H_{m}^{\ominus}$ 来计算 $K_{c}^{\neq}$ ，进而计算速率常数 k 值。仍用上述例子来说明：

$$
\mathrm{A} + \mathrm{B} - \mathrm{C} \rightleftharpoons [ \mathrm{A} - - \mathrm{B} - - \mathrm{C} ] ^ {\neq} \longrightarrow \mathrm{A} - \mathrm{B} + \mathrm{C}
$$

根据过渡态理论的统计热力学表达方法已得式 (12.40), 式中除常数 $\frac{k_{\mathrm{B}} T}{h}$ 外的其余部分相当于平衡常数的统计力学表示形式, 仅在活化络合物的配分函数中扣除了沿反应坐标的一个振动配分函数, 令

$$
K _ {c} ^ {\mp} = \frac {f ^ {\mp \prime}}{f _ {\mathrm{A}} f _ {\mathrm{BC}}} \exp \left(- \frac {E _ {0}}{R T}\right)\tag{12.45) \( ^{①} \}
$$

这样, 式 (12.40) 可写成

$$
k = \frac {k _ {\mathrm{B}} T}{h} K _ {\mathrm{c}} ^ {\neq}\tag{12.46}
$$

由此可见, 只要用热力学方法求出 $K_{c}^{\approx}$ 的值, 就可计算速率常数 k 值。现以气相双分子基元反应为例:

$$
\begin{array}{r l}\mathrm {A(g) + B - C(g)}&\rightleftharpoons [ \mathrm{A} - - \mathrm{B} - - \mathrm{C} ] ^ {\mp} (\mathrm{g})\\K _ {c} ^ {\mp}&= \frac {[ \mathrm{A} - - \mathrm{B} - - \mathrm{C} ] ^ {\mp}}{[ \mathrm{A} ] [ \mathrm{BC} ]}\end{array}
$$

在动力学中, 反应速率通常是用物质的浓度随时间的变化率来表示的, 而气体的化学势一般都用压力表示, 若也用浓度表示, 则要作如下换算:

$$
\begin{array}{r l} & p _ {\mathrm{B}} = \frac {n _ {\mathrm{B}} R T}{V} = c _ {\mathrm{B}} R T \\ & \mu_ {\mathrm{B}} = \mu_ {\mathrm{B}} ^ {\ominus} (T, p ^ {\ominus}) + R T \ln \frac {p _ {\mathrm{B}}}{p ^ {\ominus}} \\ & \quad = \mu_ {\mathrm{B}} ^ {\ominus} (T, p ^ {\ominus}) + R T \ln \frac {c _ {\mathrm{B}} R T}{p ^ {\ominus}} \\ & \quad = \mu_ {\mathrm{B}} ^ {\ominus} (T, p ^ {\ominus}) + R T \ln \frac {R T c ^ {\ominus}}{p ^ {\ominus}} - R T \ln \frac {c _ {\mathrm{B}}}{c ^ {\ominus}} \end{array}
$$

当 $c_{B}=c^{\ominus}=1\ mol\cdot dm^{-3}$ 时, 有

$$
\begin{array}{r l} \mu_ {\mathrm{B}} (c _ {\mathrm{B}} = c ^ {\ominus}) & = \mu_ {\mathrm{B}} ^ {\ominus} (T, p ^ {\ominus}) + R T \ln \frac {R T c ^ {\ominus}}{p ^ {\ominus}} \\ & = \mu_ {\mathrm{B}} ^ {\ominus} (T, c ^ {\ominus}) \end{array}
$$

$\mu_{\mathrm{B}}^{\ominus}(T,c^{\ominus})$ 是气体 B 在温度为 T、浓度为 $1\ \mathrm{mol}\cdot\mathrm{dm}^{-3}$ 时的化学势。代入化学势的表示式后，则用浓度表示的气体化学势的表示式一般可写为

$$
\mu_ {\mathrm{B}} = \mu_ {\mathrm{B}} ^ {\ominus} (T, c ^ {\ominus}) + R T \ln \frac {c _ {\mathrm{B}}}{c ^ {\ominus}}\tag{12.47}
$$

根据热力学的基本关系式, 则应有

$$
\begin{array}{r l} \sum_ {\mathrm{B}} \nu_ {\mathrm{B}} \mu_ {\mathrm{B}} ^ {\ominus} (T, c ^ {\ominus}) & = \Delta_ {\mathrm{r}} G _ {\mathrm{m}} ^ {\ominus} (c ^ {\ominus}) \\ & = - R T \ln \prod_ {\mathrm{B}} \left(\frac {c _ {\mathrm{B}}}{c ^ {\ominus}}\right) _ {\mathrm{e}} ^ {\nu_ {\mathrm{B}}} \\ & = - R T \ln K _ {c} ^ {\ominus} \end{array}
$$

对于上述反应, 有

$$
K _ {c} ^ {\ominus} = \frac {[ \mathrm{A} - - \mathrm{B} - - \mathrm{C} ] ^ {\mp} / c ^ {\ominus}}{\frac {[ \mathrm{A} ]}{c ^ {\ominus}} \cdot \frac {[ \mathrm{BC} ]}{c ^ {\ominus}}} = K _ {c} ^ {\mp} (c ^ {\ominus}) ^ {2 - 1}
$$

对于一般反应, 则有

$$
K _ {c} ^ {\ominus} = K _ {c} ^ {\mp} (c ^ {\ominus}) ^ {n - 1}
$$

式中 n 为所有反应物的计量系数之和。因此，在形成活化络合物的过程中，以浓度为标度的标准摩尔活化 Gibbs 自由能 (standard molar Gibbs free energy of activation) $\Delta_{\mathrm{r}}^{\mp} G_{\mathrm{m}}^{\ominus}(c^{\ominus})$ 为

$$
\Delta_ {\mathrm{r}} ^ {\neq} G _ {\mathrm{m}} ^ {\ominus} (c ^ {\ominus}) = - R T \ln [ K _ {c} ^ {\neq} (c ^ {\ominus}) ^ {n - 1} ]
$$

或

$$
K _ {c} ^ {\neq} = (c ^ {\ominus}) ^ {1 - n} \exp \left[ - \frac {\Delta_ {\mathrm{r}} ^ {\neq} G _ {\mathrm{m}} ^ {\ominus} (c ^ {\ominus})}{R T} \right]\tag{12.48}
$$

将式 $(12.48)$ 代入式 $(12.46)$ ，得

$$
k = \frac {k _ {\mathrm{B}} T}{h} (c ^ {\ominus}) ^ {1 - n} \exp \left[ - \frac {\Delta_ {\mathrm{r}} ^ {\mp} G _ {\mathrm{m}} ^ {\ominus} (c ^ {\ominus})}{R T} \right]\tag{12.49}
$$

根据热力学函数之间的关系, 在等温时有 $\Delta G = \Delta H - T \Delta S$ , 代入式 (12.49), 得

$$
k = \frac {k _ {\mathrm{B}} T}{h} (c ^ {\ominus}) ^ {1 - n} \exp \left[ \frac {\Delta_ {\mathrm{r}} ^ {\mp} S _ {\mathrm{m}} ^ {\ominus} (c ^ {\ominus})}{R} \right] \exp \left[ - \frac {\Delta_ {\mathrm{r}} ^ {\mp} H _ {\mathrm{m}} ^ {\ominus} (c ^ {\ominus})}{R T} \right]\tag{12.50}
$$

式中 $\Delta_{\mathrm{r}}^{\mp}S_{\mathrm{m}}^{\ominus}(c^{\ominus})$ 和 $\Delta_{\mathrm{r}}^{\mp}H_{\mathrm{m}}^{\ominus}(c^{\ominus})$ 分别为各物质用浓度表示时的标准摩尔活化熵(standard molar entropy of activation)和标准摩尔活化焓（standard molar enthalpy of activation）。式(12.49)和式(12.50)即为过渡态理论用热力学方法计算反应速率常数的公式，它适用于任何形式的基元反应，只要能计算出活化熵、活化焓或活化Gibbs自由能，原则上就有可能计算反应的速率常数。从式(12.50)也可看出，反应速率不仅取决于活化焓，还与活化熵有关，两者对速率常数的影响刚好相反。这就是为什么有些反应虽然活化焓很大，但由于其活化熵也很大，所以仍能以较快的速率进行。例如，蛋白质的变性反应，其 $\Delta_{\mathrm{r}}^{\mp}H_{\mathrm{m}}^{\ominus}$ 值高达 $420\mathrm{kJ}\cdot \mathrm{mol}^{-1}$ ，但由于活化熵也很大，所以仍能以较快的速率进行。当然，也有些反应虽然活化焓很小，但只要活化熵是一个绝对值较大的负数，其反应速率也可能很小。

如果化学势仍用压力表示, 标准态为 $p^{\ominus} = 100 \, kPa$ , 则

$$
\begin{array}{r l} \sum_ {\mathrm{B}} \nu_ {\mathrm{B}} \mu_ {\mathrm{B}} ^ {\ominus} (T, p ^ {\ominus}) & = \Delta_ {\mathrm{r}} ^ {\mp} G _ {\mathrm{m}} ^ {\ominus} (p ^ {\ominus}) \\ & = - R T \ln \prod_ {\mathrm{B}} \left(\frac {p _ {\mathrm{B}}}{p ^ {\ominus}}\right) _ {\mathrm{e}} ^ {\nu_ {\mathrm{B}}} \\ & = - R T \ln K _ {p} ^ {\ominus} \end{array}
$$

因为 $p_{B}=c_{B}RT$ ，所以对于上述气相双分子基元反应，有

$$
\begin{array}{r l} K _ {c} ^ {\neq} & = \frac {[ \mathrm{A} - - - \mathrm{B} - - - \mathrm{C} ] ^ {\neq}}{[ \mathrm{A} ] [ \mathrm{BC} ]} = \frac {p _ {[ \mathrm{ABC} ]} ^ {\neq} / R T}{\frac {p _ {\mathrm{A}}}{R T} \cdot \frac {p _ {\mathrm{BC}}}{R T}} \\ & = \frac {p _ {[ \mathrm{ABC} ]} ^ {\neq} / p ^ {\ominus}}{\frac {p _ {\mathrm{A}}}{p ^ {\ominus}} \cdot \frac {p _ {\mathrm{BC}}}{p ^ {\ominus}}} \left(\frac {p ^ {\ominus}}{R T}\right) ^ {1 - 2} \\ & = K _ {p} ^ {\ominus} \left(\frac {p ^ {\ominus}}{R T}\right) ^ {1 - 2} \end{array}
$$

对于一般反应, 则有

$$
\begin{array}{r l} K _ {c} ^ {\mp} & = K _ {p} ^ {\ominus} \left(\frac {p ^ {\ominus}}{R T}\right) ^ {1 - n} \\ & = \left(\frac {p ^ {\ominus}}{R T}\right) ^ {1 - n} \exp \left[ - \frac {\Delta_ {\mathrm{r}} ^ {\mp} G _ {\mathrm{m}} ^ {\ominus} (p ^ {\ominus})}{R T} \right] \end{array}
$$

代入式 (12.46), 得

$$
k = \frac {k _ {\mathrm{B}} T}{h} \left(\frac {p ^ {\ominus}}{R T}\right) ^ {1 - n} \exp \left[ - \frac {\Delta_ {\mathrm{r}} ^ {\neq} G _ {\mathrm{m}} ^ {\ominus} (p ^ {\ominus})}{R T} \right]\tag{12.51}
$$

$$
k = \frac {k _ {\mathrm{B}} T}{h} \left(\frac {p ^ {\ominus}}{R T}\right) ^ {1 - n} \exp \left[ \frac {\Delta_ {\mathrm{r}} ^ {\mp} S _ {\mathrm{m}} ^ {\ominus} (p ^ {\ominus})}{R} \right] \exp \left[ - \frac {\Delta_ {\mathrm{r}} ^ {\mp} H _ {\mathrm{m}} ^ {\ominus} (p ^ {\ominus})}{R T} \right]\tag{12.52}
$$

显然, 用式 (12.49)、式 (12.50) 或用式 (12.51)、式 (12.52) 所计算得到的速率常数 $k$ 值是相同的。但是, $\Delta_{\mathrm{r}}^{\approx} G_{\mathrm{m}}^{\ominus}(c^{\ominus}) \neq \Delta_{\mathrm{r}}^{\approx} G_{\mathrm{m}}^{\ominus}(p^{\ominus}), \Delta_{\mathrm{r}}^{\approx} S_{\mathrm{m}}^{\ominus}(c^{\ominus}) \neq \Delta_{\mathrm{r}}^{\approx} S_{\mathrm{m}}^{\ominus}(p^{\ominus})$ 。从热力学数据表上所能查到的数值都是指标准态为 $p^{\ominus} = 100 \mathrm{kPa}$ 时的数值。

从以上所介绍的过渡态理论计算速率常数 $k$ 的两种方法看出，这个理论一方面与物质的结构相联系，另一方面也与热力学建立了联系，它明确指出反应速率不仅与活化能 $E_{\mathrm{a}}$ ( $E_{\mathrm{a}}$ 与 $\Delta_{\mathrm{r}}^{\mp}H_{\mathrm{m}}^{\ominus}$ 的关系见下部分内容)有关，而且与活化熵有关。在过渡态理论中不需引入概率因子 $P$ ，这些都是过渡态理论比碰撞理论优越的地方。虽然过渡态理论提供了一种计算反应速率的途径和方法，但在实际运算时，除了一些极为简单的反应系统之外，一般说来还有不少困难，例如量子力学对多质点系统的能量计算问题，确定活化络合物的几何构型问题等。另外，在过渡态理论中引入了不少假定，有的还不尽合理，如活化络合物与反应物达成平衡的假设就不一定确切。原则上，过渡态理论根据势能面的高度可以求得活化能，并从光谱数据中求得配分函数的值，进而求得速率常数 $k$ 值。虽然过渡态理论相对于碰撞理论有其优越性，但离准确地预言反应的速率常数 $k$ 值尚有很大的距离。因为除极简单的反应外，对绝大多数反应来说，很难得到其势能面，并且活化络合物的寿命很短，也很难得到它的光谱数据，因此活化络合物的构型常只能靠估计获得。同时，由于活化络合物的寿命很短，彼此碰撞的次数可能还不够多，未必能达到足以满足Boltzmann分布的要求。如此等等，表明过渡态理论仍要进行很多修正或补充。总之，在化学动力学的领域里还需要进一步做大量的实验和理论工作，逐步寻找各种因素与反应速率的定量关系，使反应速率理论更趋完善。

## \*活化络合物的活化能 $E_{\mathrm{a}}$ 和指前因子 $\mathbf{A}$ 与诸热力学函数之间的关系

在上述讨论中曾引出了几个与能量有关的物理量, 如 $E_{c}, E_{0}, E_{b}$ 和 $\Delta_{r}^{\neq} H_{m}^{\ominus}$ 等, 它们的物理意义各不相同, 但数值上有一定的联系, 可以通过实验活化能 $E_{a}$ 或光谱数据等进行换算。

$E_{c}$ 是分子发生有效碰撞时其相对动能在连心线上的分量所必须超过的临界能, 故 $E_{c}$ 又称为阈能, 是与温度无关的量。 $E_{c}$ 与 $E_{a}$ 的关系已由式 (12.29) 给出, 即 $E_{c} = E_{a} - \frac{1}{2} RT$ 。

$E_{0}$ 是活化络合物的零点能与反应物零点能之间的差值, $E_{b}$ 是反应物形成活化络合物时所必须翻越的势垒高度, $E_{0}$ 与 $E_{b}$ 的关系已由式 (12.44) 给出。如将式 (12.40) 代入实验活化能 $E_{a}$ 的定义式, 得

$$
\begin{array}{r l} E _ {\mathrm{a}} & = R T ^ {2} \frac {\mathrm{dln} k}{\mathrm{d} T} \\ & = E _ {0} + m R T \end{array}\tag{12.53}
$$

式中 $m$ 包含了 $\frac{k_{\mathrm{B}}T}{h}$ 常数项中及配分函数项中所有与温度 $T$ 有关的因子，对一定的反应系统 $m$ 有定值。

将式 (12.46) 代入 $E_{\mathrm{a}}$ 的定义式, 得

$$
\begin{array}{r l} & E _ {\mathrm{a}} = R T ^ {2} \frac {\mathrm{d} \ln k}{\mathrm{d} T} \\ & \qquad = R T ^ {2} \left[ \frac {1}{T} + \left(\frac {\partial \ln K _ {c} ^ {\neq}}{\partial T}\right) _ {V} \right] \end{array}\tag{12.54}
$$

根据平衡常数与温度的关系式:

$$
\left(\frac {\partial \ln K _ {c} ^ {\neq}}{\partial T}\right) _ {V} = \frac {\Delta_ {\mathrm{r}} ^ {\neq} U _ {\mathrm{m}} ^ {\ominus}}{R T ^ {2}}\tag{12.55}
$$

则

$$
E _ {\mathrm{a}} = R T + \Delta_ {\mathrm{r}} ^ {\mp} U _ {\mathrm{m}} ^ {\ominus} = R T + \Delta_ {\mathrm{r}} ^ {\mp} H _ {\mathrm{m}} ^ {\ominus} - \Delta (p V) _ {\mathrm{m}}\tag{12.56}
$$

式中 $\Delta(pV)_{\mathrm{m}}$ 是反应进度为 1 mol 时，由反应物形成活化络合物时系统 pV 的改变值。对凝聚相反应， $\Delta(pV)_{\mathrm{m}}$ 的值很小，近似有 $\Delta_{r}^{\neq}U_{m}^{\ominus}\approx\Delta_{r}^{\neq}H_{m}^{\ominus}$ ，则

$$
E _ {\mathrm{a}} = R T + \Delta_ {\mathrm{r}} ^ {\neq} H _ {\mathrm{m}} ^ {\ominus}\tag{12.57}
$$

对于理想气体的反应, 有 pV = nRT, 则

$$
\Delta (p V) _ {\mathrm{m}} = \sum_ {\mathrm{B}} \nu_ {\mathrm{B}} ^ {\neq} R T\tag{12.58}
$$

式中 $\sum_{B}\nu_{B}^{\widetilde{z}}$ 是反应物形成活化络合物时, 参与反应的气态物质的计量系数的代数和。代入式 (12.56), 得

$$
E _ {\mathrm{a}} = \Delta_ {\mathrm{r}} ^ {\mp} H _ {\mathrm{m}} ^ {\ominus} + \left(1 - \sum_ {\mathrm{B}} \nu_ {\mathrm{B}} ^ {\mp}\right) R T\tag{12.59}
$$

从式 (12.57) 和式 (12.59) 可以看出, 在温度不太高时, 把 $E_{\mathrm{a}}$ 与 $\Delta_{\mathrm{r}}^{\neq} H_{\mathrm{m}}^{\ominus}$ 看作近似相等也不致引起很大的误差。

将式 $(12.59)$ 代入式 $(12.50)$ ，得

$$
k = \frac {k _ {\mathrm{B}} T}{h} \mathrm{e} ^ {n} (c ^ {\ominus}) ^ {1 - n} \exp \left[ \frac {\Delta_ {\mathrm{r}} ^ {\mp} S _ {\mathrm{m}} ^ {\ominus} (c ^ {\ominus})}{R} \right] \exp \left(- \frac {E _ {\mathrm{a}}}{R T}\right)\tag{12.60}
$$

与 Arrhenius 公式相比较, 因为 $1 - \sum_{\mathrm{B}} \nu_{\mathrm{B}}^{\neq} = n$ , 得

$$
A = \frac {k _ {\mathrm{B}} T}{h} \mathrm{e} ^ {n} (c ^ {\ominus}) ^ {1 - n} \exp \left[ \frac {\Delta_ {\mathrm{r}} ^ {\mp} S _ {\mathrm{m}} ^ {\ominus} (c ^ {\ominus})}{R} \right]\tag{12.61}
$$

从式 (12.61) 看出, 指前因子 $A$ 与形成过渡态的熵变有关。除了单分子反应外, 在由反应物形成活化络合物时, 分子数总是减少的, 则对熵贡献最大的平动自由度亦减少, 故总熵变 $\Delta_{\mathrm{r}}^{\cong} S_{\mathrm{m}}^{\ominus}$ 一般是负值。

## 12.3 单分子反应理论

单分子反应 (unimolecular reaction) 按照定义应该是由一个分子所实现的基元反应, 但是, 一个孤立地处于基态的分子不能自发地进行反应 (事实上它已处于平衡态)。实际上, 为使这类反应发生, 反应分子必须具有足够的能量。如果反应分子不以其他方式 (如获得辐射能等) 获得能量, 那只有通过分子间的碰撞来获得。碰撞理论认为每次碰撞至少要两个分子, 因此严格讲它就不是单分子反应, 而应称为准单分子反应 (pseudo-unimolecular reaction)。例如, 某些分子的分解反应或异构化反应就属于这种单分子反应。

1922 年, Lindemann 等人提出了单分子反应的碰撞理论, 认为单分子反应是经过相同分子间的碰撞而达到活化状态的。而获得足够能量的活化分子并不立即分解, 它需要一个分子内部能量的传递过程, 以便把能量聚集到要断裂的键上去。因此, 在碰撞之后与进行反应之间出现一段停滞时间 (time lag)。此时, 活化分子可能进行反应, 也可能消活化 (deactivation) 而再变回普通分子。在浓度不是很小的情况下, 这种活化与消活化之间存在一个平衡; 如果活化分子分解或转化为产物的速率比消活化的速率慢, 则上述平衡基本上可认为不受影响。单分子反应的机理可表示如下:

总反应为 A $\longrightarrow$ P
具体步骤为 (1) $A + A \xlongequal{k_{1}} A^{*} + A$ (2) $A^{*} \xrightarrow{k_{2}} P$

式中 A\* 为活化分子。式 (1) 并不是化学变化, 而仅是使分子活化的传能过程。分子活化的速率为

$$
\frac {\mathrm{d} [ \mathrm{A} ^ {*} ]}{\mathrm{d} t} = k _ {1} [ \mathrm{A} ] ^ {2}\tag{a}
$$

分子消活化的速率为

$$
- \frac {\mathrm{d} [ \mathrm{A} ^ {*} ]}{\mathrm{d} t} = k _ {- 1} [ \mathrm{A} ] [ \mathrm{A} ^ {*} ]\tag{b}
$$

活化分子变为产物的速率为

$$
\frac {\mathrm{d} [ \mathrm{P} ]}{\mathrm{d} t} = k _ {2} [ \mathrm{A} ^ {*} ]\tag{c}
$$

则分子活化的净速率为

$$
\frac {\mathrm{d} [ \mathrm{A} ^ {*} ]}{\mathrm{d} t} = k _ {1} [ \mathrm{A} ] ^ {2} - k _ {- 1} [ \mathrm{A} ] [ \mathrm{A} ^ {*} ] - k _ {2} [ \mathrm{A} ^ {*} ]
$$

当反应达稳态后, 活化分子的数目维持不变 (即产生和消耗 A\* 的速率相等), 则

$$
\frac {\mathrm{d} [ \mathrm{A} ^ {*} ]}{\mathrm{d} t} = 0
$$

由此解得

$$
[ \mathrm{A} ^ {*} ] = \frac {k _ {1} [ \mathrm{A} ] ^ {2}}{k _ {- 1} [ \mathrm{A} ] + k _ {2}}
$$

反应 (2) 的速率为产物的生成速率, 也就是实验上测得的总反应速率 $r$ , 代入 $[\mathrm{A}^{*}]$ 的表达式后, 得

$$
r = \frac {\mathrm{d} [ \mathrm{P} ]}{\mathrm{d} t} = k _ {2} [ \mathrm{A} ^ {*} ] = \frac {k _ {1} k _ {2} [ \mathrm{A} ] ^ {2}}{k _ {- 1} [ \mathrm{A} ] + k _ {2}}\tag{12.62}
$$

式 (12.62) 为 Lindemann 单分子反应理论所推出的结果, 按此结果对单分子反应中所出现的不同反应级数可作如下解释。

当 $\mathrm{A}^*$ 转化为产物的速率[式(c)]远大于 $\mathrm{A}^*$ 的消活化速率[式(b)]时，即 $k_{2}\gg k_{-1}[\mathrm{A}]$ ，则式(12.62)可近似写为

$$
r = k _ {1} [ \mathrm{A} ] ^ {2}
$$

反应表现为二级反应。

反之, 当 $\mathrm{A}^*$ 转化为产物的速率 [式 (c)] 远小于 $\mathrm{A}^*$ 的消活化速率 [式 (b)] 时, 即 $k_{2} \ll k_{-1}[\mathrm{A}]$ 时, 式 (12.62) 可近似写为

$$
r = \frac {k _ {2} k _ {1}}{k _ {- 1}} [ \mathrm{A} ] = k [ \mathrm{A} ]
$$

反应表现为一级反应。

对于某些气相反应, 在高压下, [A] 值很大, 分子的互撞机会多, 消活化的速率较快, 则反应表现为一级反应。对于同一反应, 如使之在低压下进行, 由于碰撞而消活化的机会较少, 相对而言, 活化分子转化为产物的速率快, 所以反应表现为二级反应。这个结论已为某些实验所证实, 例如环丙烷转化为丙烯的反应以及偶氮甲烷的分解反应就是这样的。

式 (12.62) 也可写作

$$
r = k ^ {\prime} [ \mathrm{A} ] \qquad \text {其中} k ^ {\prime} = \frac {k _ {1} k _ {2} [ \mathrm{A} ]}{k _ {1} [ \mathrm{A} ] + k _ {2}}
$$

603 K 时以偶氮甲烷分解反应的 $k'$ 对偶氮甲烷的压力 (p) 作图可得图 12.10, 这里的压力相当于上式中的浓度项。此反应在低压下为二级反应, 高压下为一级反应, 压力在 $1.3 \sim 26.7 \, kPa$ 的区间则为过渡区。

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_200-399_images/96f952b774b611aaacebf6083b7a69648f929353750431c2f3fe9e58ca9f1a33.jpg)  
图 12.10 偶氮甲烷分解反应的级数与压力的关系

Lindemann 单分子反应理论在定性上是基本符合实际的, 但在定量上往往和实验结果有偏差, 后来不少学者对其进行修正, 目前与实验符合得较好的单分子反应理论是 20 世纪 50 年代的 RRKM (Rice-Ramsperger-Kassel-Marcus) 理论, 这是 Marcus 把 20 年代的 RRK 理论与过渡态理论结合而提出的, RRKM 理论把 Lindemann 理论修正为

(1)

$$
\begin{array}{l} \mathrm {A+ A\xrightarrow [ k _ {- 1} ]{k_ {1}} A^ {*} + A} \\ \mathrm {A^ {*} \xrightarrow {k_ {2} (E^ {*})} A^ {\neq} \xrightarrow {k^ {\neq}} P} \end{array}\tag{2}
$$

$\mathrm{A}^{*}$ 是 $\mathrm{A}$ 与 $\mathrm{A}$ (或与其他惰性分子 $\mathrm{M}$ ) 碰撞而生成的活化分子, 但 $\mathrm{A}^{*}$ 要转化为产物, 必须再多吸收一些能量, 使分子转变成过渡态的构型 $\mathrm{A}^{\neq}$ , $\mathrm{A}^{\neq}$ 是富能分子 (energized molecule), 它能克服反应中的势垒 $(E_{\mathrm{b}})$ 而开始分解。Lindemann 理论中所提及的碰撞后与反应前的停滞时间就相当于 $\mathrm{A}^{*}$ 向 $\mathrm{A}^{\neq}$ 的转变过程。

RRKM 理论的核心是计算 $k_{2}$ 值, 该理论认为 $k_{2}$ 值是能量 $E^{*}$ 的函数, $A^{*}$ 所获得的能量 $E^{*}$ 越大, 反应速率就越快, 即当 $E^{*} < E_{b}, k_{2} = 0$ ; 当 $E^{*} > E_{b}, k_{2} = k_{2}(E^{*})$ 。当反应 (2) 达到稳定时, 有

$$
\frac {\mathrm{d} [ \mathrm{A} ^ {\mp} ]}{\mathrm{d} t} = k _ {2} (E ^ {*}) [ \mathrm{A} ^ {*} ] - k ^ {\mp} [ \mathrm{A} ^ {\mp} ] = 0
$$

则

$$
k _ {2} (E ^ {*}) = \frac {k ^ {\neq} [ \mathrm{A} ^ {\neq} ]}{[ \mathrm{A} ^ {*} ]}\tag{12.63}
$$

式 (12.63) 是 RRKM 理论计算 $k_{2}(E^{*})$ 的出发点, 假定 $k_{2}(E^{*})$ 与时间和活化方式无关, 分子内部能量传递比 $\mathrm{A}^{*}$ 分解的速率快得多, 然后采用统计力学的方法计算 $k_{2}(E^{*})$ , 于是就获得了与实验值符合较好的结果。

在研究单分子反应理论的过程中曾出现了许多理论, 如 Hinshelwood 理论、Slater 理论、RRK 理论、RRKM 理论等, 但 Lindemann 理论无疑是这些理论的基础。

## \*12.4 分子反应动态学简介

20 世纪 50 年代至 80 年代, 由于激光、分子束等实验技术的飞速发展, 计算机的广泛应用, 以及反应速率理论研究的逐步深入, 为从微观角度研究化学反应过程提供了良好的实验条件和一定的理论基础, 使人们有可能从化学反应的宏观领域深入微观领域, 去探索分子与分子 (或原子与原子) 间的反应和特征, 研究指定能态粒子之间反应 (即所谓态-态反应) 的规律, 揭示微观化学反应所经历的历程。这些研究不但对化学反应动力学理论有重要的贡献, 而且对应用研究也有一定的指导意义。由于微观地研究化学反应过程的实验和理论的迅速发展, 从而形成了化学反应动力学的一个新分支——分子反应动态学 (molecular reaction dynamics)。它从分子水平上研究分子在一次碰撞行为中的变化和基元反应的微观历程, 例如分子如何碰撞、如何进行能量交换, 旧键如何被破坏、新键如何形成的细节, 分子彼此碰撞的角度对反应速率的影响以及分子反应产物的角分布等, 进而了解化学反应过程中的各种动态性质。分子反应动态学又称为微观反应动力学 (microscopic reaction kinetics)。总之, 它研究的是基元反应的微观历程, 真正从分子水平上研究一次碰撞行为, 即研究分子的态对态 (state-to-state) 即态-态反应行为。限于篇幅也限于对本课程的基本要求, 在本节中只能对进行这方面研究所用的主要实验手段和已取得的实验结果以及一些进展概况作简单的介绍。

## 研究分子反应的实验方法

在微观化学反应研究中, 极为有用的实验方法主要有交叉分子束、红外化学发光和激光诱导荧光三种。

交叉分子束 (crossed molecular beam) 技术是目前分子反应碰撞研究中最强有力的工具。常用的交叉分子束反应装置如图 12.11 所示。它是由束源、准直狭缝、速度选择器、散射室、检测器和产物速度分析器等主要部分组成的。分子束形成的必要条件是在所研究的系统中有足够低的背景压力，一般小于 $10^{-4}$ Pa。因为在这样低的压力下，分子的平均自由程约为 50 m，远大于装置的尺寸，故分子间的相互碰撞可以忽略。此时的束流是自由分子流，称为分子束 (molecular beam)。来自束源的分子通过一系列狭缝，可以得到一束准直的分子束。分子束沿着直线方向运动，在运动过程中它的速度和内部量子态不会发生变化。D. R. Herschbach 和李远哲在分子束实验研究中曾作出杰出的贡献，并因此而共同获得 1986 年诺贝尔化学奖。

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_200-399_images/11e016ffa68e10127c262c958282225613d3ad76c8016560c9133a38ba17f906.jpg)  
图 12.11 交叉分子束反应装置示意图

分子束是在高真空的容器中飞行的一束分子, 它是由束源中发射出来的。早期使用的束源是由加热炉产生的溢流束。例如, 金属钾原子束是由加热炉把金属钾汽化为钾蒸气, 从束源的小孔中溢出, 经过几个狭缝准直地进入高真空的散射室而形成的。由于此种分子束是由分子的热运动扩散而形成的，故称为溢流束或扩散束，束中分子的速度遵从 Boltzmann 分布。产生束源的设备常简称为“炉子”，一般控制炉内压力使其低于 13 Pa，以使炉内的分子平均自由程远大于炉子小孔的尺寸和狭缝的宽度，使分子无碰撞地自由流出。这种束源结构简单，易控制，适用于各种反应，但缺点是束流强度低、速度分布较宽。

近年来常使用超声喷嘴束源, 源内压力可高于大气压力的几十倍, 突然以超声速绝热向真空膨胀, 分子由随机的热运动转变为定向的有序束流, 它具有较大的平动能, 同时由于绝热膨胀后温度很低可使转动和振动处于基态。这种分子束的速度分布比较窄, 不需要外加速度选择器, 喷嘴源本身通过压力的调节就起着速度选择作用。

速度选择器 (图 12.11 中未画出) 是由一系列带有齿孔的圆盘组成的, 这些圆盘装在一个与分子束前进方向平行的转动轴上, 每个盘上刻有数目不等的齿孔。由于从溢流束源产生的分子束中分子的速度遵从 Boltzmann 分布, 为了得到一个速度范围很窄的分子束, 故让它在进入散射室之前先经过速度选择器, 让分子束中具有所选择速度的分子恰好相继通过各个圆盘上的齿孔而到达散射室, 速度不符合要求的分子都被圆盘挡掉。改变转轴速度, 可以控制分子束的速度以达到选择反应分子平动能量的要求 (参见本书第一章)。这种速度选择器的缺点是大大降低了分子束的强度。

散射室又称主室或反应室, 两束分子在那里正交发生反应散射。散射室要求保持很高的真空度, 散射室周围可以设置多个窗口, 以便让探测激光束进入反应散射区域进行检测, 同时通过窗口接收来自产物粒子辐射的光学信号, 以分析产物的量子态。

检测器的灵敏度是分子束实验成功与否的关键因素之一。因为稀薄的两束分子在散射室里交叉，只有其中一小部分发生碰撞，而反应碰撞又只是全部碰撞中的很小部分，因此在某立体角内要测量的产物强度是非常低的。正因为如此，直到20世纪后半期，当高灵敏度检测器出现后，分子束的研究才得以迅速发展。例如，电子轰击式电离四极质谱仪及速度分析器常被用来测量分子束反应产物的角分布、平动能分布及分子内部能量的分布。

处于振动、转动激发态的化学反应产物向低能态跃迁时所发出的辐射称为红外化学发光 (infrared chemiluminescence, 简称 IRC), 记录分析这些光谱, 可以得到初生产物在振动、转动态上的分布。分子束实验一般只能确定反应释放能量在产物平动能和内部能之间的分配, 而红外化学发光技术可以得到产物转动能、振动能及平动能之间的相对分布。红外化学发光实验研究的开拓者是

J. C. Polanyi。

激光诱导荧光 (laser-induced fluorescence, 简称 LIF) 方法是 20 世纪 70 年代由 R. N. Zare 发展起来的, 并得到了广泛的应用。这种方法是用一束可调激光, 将初生产物分子的电子从处于某振转态的基态激发到高电子态的某一振转能级, 并检测高电子态发出的荧光。让激光束在电子基态诸能级上扫描, 由测得的荧光强度及两电子态之间电子的跃迁情况, 可以确定产物分子在振动能级上的初始分布情况。

## 分子碰撞与态-态反应

凡涉及两个粒子间的反应必然经历碰撞过程。例如，对于一个双分子基元反应 $\mathrm{A} + \mathrm{BC}\longrightarrow \mathrm{AB} + \mathrm{C},$ 宏观上该反应的速率可表示为 $r = k[\mathrm{A}][\mathrm{BC}]$ ，式中速率常数 $k$ 可用Arrhenius公式表达，即 $k = A\exp \left(-\frac{E_{\mathrm{a}}}{RT}\right)$

宏观动力学的主要任务之一就是在一定温度范围内, 测定 k 的值并求出反应的活化能 $E_{a}$ 和指前因子 A。但是, 所得到的结果都是在热平衡条件下的平均值。反应前 A 分子和 BC 分子可以各自具有各种不同的平动能、内部能量 (包括转动、振动和电子能量等) 以及各种不同的方位。反应产物也经历了多次碰撞, 并且具有不同的能量, 它们完全失去了初生时的特征和能量, 因而所得结果是大量分子的平均行为和总包反应的规律。而从微观的角度去研究反应, 就要知道从确定能态的反应物到确定能态的产物的反应特征。对上述反应来说, 就是要知道从量子态为 i 的 A 分子与量子态为 j 的 BC 分子发生反应, 生成量子态分别为 m 和 n 的 AB 分子和 C 分子, 可表示为

$$
\mathrm{A} (i) + \mathrm{BC} (j) \longrightarrow \mathrm{AB} (m) + \mathrm{C} (n)
$$

这种反应称为态-态反应 (state-to-state reaction), 这样的反应只能靠个别分子的单次碰撞来完成, 需要从分子水平上考虑问题。

分子的碰撞可以区分为弹性碰撞、非弹性碰撞和反应碰撞。前两种碰撞不引起化学变化，后一种碰撞则引起化学反应。在弹性碰撞过程中，分子之间可以交换平动能，所以碰撞前后分子的速度发生了变化，但总的平动能是守恒的，且在弹性碰撞中，分子内部的能量（如转动、振动及电子能量等）保持不变。分子间平动能的交换速率很快，在大量分子的平衡中，分子的能量和速度分布遵从Maxwell-Boltzmann分布定律。在非弹性碰撞过程中，分子平动能可以与其内部的能量互相交换（虽然这种交换的速率是比较慢的），因而在非弹性碰撞前后平动能不守恒，而分子的转动能之间的交换速率较快，大约在几次碰撞（甚至是每次碰撞) 中就有一次碰撞有转动能的交换。因此, 分子的转动、振动及电子态之间的 Boltzmann 分布靠分子的非弹性碰撞维持。在反应碰撞中, 不但有平动能与内部能量的交换, 同时分子的完整性也由于发生了化学反应而产生变化, 如果化学反应的速率很快, 系统就可能来不及维持平衡态的 Boltzmann 分布。

在微观反应动力学研究中, 需要知道特定的态与态之间的反应, 这在宏观动力学实验中是办不到的。因为在通常的条件下, 反应物和产物的能态并不单一, 而是呈 Boltzmann 分布。为了选择分子的某一特定的量子态, 需要一些特殊的装置 (如激光、产生分子束的装置), 同时对于产物的能态也需要用特殊的检测器进行检测分析。

## 直接反应碰撞和形成络合物的碰撞

在分子束实验中, 主要测量的量是产物分子的角分布和速度分布, 从这两个量可以得到经典动力学实验不能得到的关于基元反应的微观反应历程的信息。

实验测得的产物角分布因反应不同而不同, 呈明显的特征。在质心坐标系中(质心坐标系是指以互撞分子的质心作为原点而作图, 如果设想观察者坐在质心上观察两个分子的碰撞, 则他将看到两个分子总是沿着一条通过质心的直线从相反的方向趋近), 反应产物有的集中在前半球, 有的集中在后半球, 也有的对称地分布在前后半球中, 不同的角分布对应于不同类型的反应碰撞。

反应产物的角分布在某些方向特别集中, 这是由于反应碰撞时间很短, 小于转动周期 $(1 \times 10^{-12} \text{ s})$ , 正在碰撞的反应物没有足够的时间完成数次转动, 反应过程却早已结束, 这种碰撞就是直接反应碰撞。例如:

$$
\mathrm{K} + \mathrm{I} _ {2} \longrightarrow \mathrm{KI} + \mathrm{I} \cdot
$$

以该反应为例, 收集反应过程中的产物密度分布图。该图是以质心为原点的角度坐标图, 规定 K 原子的入射方向为 $0^{\circ}$ , $I_{2}$ 分子的入射方向为 $180^{\circ}$ , 对所有的反应散射作出相应的标记点。先作出产物密度点, 然后将产物密度相等的点用一条线联结起来, 即得到密度的 “等值线”。图 12.12(b) 中就是产物 KI 的等密度线, 它反映了产物的角度分布, 即 “最概然的散射方向”。若产物 KI 分子出现的方向与碰撞前 K 原子的方向一致, 即称为 “正向散射或向前散射”。从等密度图也可以了解产物分子的相对速度和相对平动能的分布。

产物 KI 分子的散射方向与 K 原子的入射方向一致 (参见图 12.12), 在检测器中捕捉到的产物主要分布在 K 原子前进的方向, 犹如 K 原子在前进方向上与 $I_{2}$ 分子相遇时, 摘取了一个 I 原子而继续向前。因此, 这种向前散射的直接反应碰撞的动态模型称为抢夺模型 (stripping model)。

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_200-399_images/589e125be88ef41d6f9753ec71187e60cdd40cbfa7065ee2d7e2525f49eb29d1.jpg)  
图 12.12 向前散射示意图

对于反应:

$$
\mathrm{K} + \mathrm{CH} _ {3} \mathrm{I} \longrightarrow \mathrm{KI} + \cdot \mathrm{CH} _ {3}
$$

其产物 KI 分子的分布却与上面的反应不同, KI 分子的散射优势方向与 K 原子入射方向相反, 这是一种向后散射的直接反应模型, 称为回弹模型 (rebound model), 如图 12.13 所示。

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_200-399_images/7d56be516e5a0338ed0d19a33299d0485562e5c299d7c818dc4ed4626d233ae4.jpg)  
图 12.13 向后散射示意图

还有一种形成中间络合物的反应,例如反应:

$$
\mathrm{Cs} + \mathrm{RbCl} \longrightarrow \mathrm{CsCl} + \mathrm{Rb}
$$

$$
\mathrm{O} \cdot + \mathrm{Br} _ {2} \longrightarrow \mathrm{OBr} + \mathrm{Br} \cdot
$$

其产物的角分布前后都有, 在空间中呈各向同性的散射, 如图 12.14 所示。这是由于在反应过程中形成了中间络合物, 它的寿命比转动的周期大好几倍, 因而产物分子呈随机散射状, 而不会形成在空间某些方向的特别优势。

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_200-399_images/e34430e12deaa8d9ef32291abd92bf8fe58b651c81f2f539cdf8f1b6b4a1f02d.jpg)  
图 12.14 形成中间络合物的散射示意图

K 和 $I_{2}$ 的反应可以推广到碱金属 M 和卤素 $X_{2}$ 的反应, 该反应过程实际是一个电子转移的过程。因为卤素原子的电子亲和势较大, 而碱金属的电离势值又不是很大, 所以在 M 原子与 $X_{2}$ 分子相距较远时, 电子转移就可能完成:

$$
\mathrm{M} + \mathrm{X} _ {2} \longrightarrow \mathrm{M} ^ {+} \cdot \mathrm{X} _ {2} ^ {-}
$$

碱金属 M 很容易抛出价电子给卤素分子, 就像把鱼叉投向鱼一样把电子抛向一个卤素分子, 从而形成离子对 $M^{+} \cdot X_{2}^{-}$ 。由于电子质量很小, 这种电子转移即使在反应物相距 0.1 nm 以上时也是可能发生的。然后, 库仑引力 (像一根绳子) 将一个 $X^{-}$ (鱼) 拉回来, 形成稳定的 MX 分子, 而推斥另一个 X 原子, 这种机理被称为鱼叉机理 (harpoon mechanism)。

我们不可能定量地叙述反应过程的细节, 仅从以上的定性叙述中, 也可以看出产物的角分布与基元反应的微观历程之间是密切联系的。

## 12.5 在溶液中进行的反应

溶液中的反应与气相反应相比, 最大的不同是溶剂分子的存在。同一个反应在气相中进行和在溶液中进行则有不同的速率, 甚至有不同的历程, 生成不同的产物, 这些都是溶剂效应引起的。在溶液中, 溶剂对反应物的影响大致有解离作用、传能作用和溶剂的介电性质等的影响。在电解质溶液中, 还有离子与离子、离子与溶剂分子间的相互作用等的影响, 这些都属于溶剂的物理效应。溶剂也可以对反应起催化作用, 甚至溶剂本身也可以参加反应, 这些属于溶剂的化学效应。显然, 溶液中的反应要比气相反应复杂得多, 现在已逐渐形成专门研究溶液中反应的一个学科分支——溶液反应动力学。本节仅对溶剂的几个影响因素作简要的介绍。

## 溶剂对反应速率的影响——笼效应

在均相反应中, 溶液中的反应远比气相反应多得多 (有人粗略估计有 90% 以上均相反应是在溶液中进行的), 但研究溶液中反应的动力学要考虑溶剂分子所起的物理的或化学的影响。另外, 在溶液中有离子参加的反应常常是瞬间完成的, 这也造成了观测动力学数据的困难。最简单的情况是溶剂仅起介质作用的情况。

在溶液中起反应的分子要通过扩散穿过周围的溶剂分子之后, 才能彼此接近而发生接触, 反应后产物分子也要穿过周围的溶剂分子通过扩散而离开。这里所谓扩散, 就是对周围溶剂分子的反复挤撞。从微观的角度, 可以认为周围溶剂分子形成了一个笼 (cage), 而反应分子则处于笼中。分子在笼中持续时间比气体分子互相碰撞的持续时间长 $10 \sim 100$ 倍, 这相当于分子在笼中可以经历反复的多次碰撞。所谓笼效应 (cage effect) 就是指反应分子在溶剂分子形成的笼中进行的多次反复的碰撞 (或 “振动”, 这当然是指分子外部的反复移动, 而不是指分子内部的振动)。这种连续的反复碰撞一直持续到反应分子从笼中挤出, 这种在笼中连续的反复碰撞则称为反应分子的一次遭遇 (encounter)。所以, 溶剂分子的存在虽然限制了反应分子作远距离的移动, 减少了与远距离分子的碰撞机会, 但却增加了近距离反应分子的重复碰撞, 因而总的碰撞频率并未降低。据粗略估计, 在水溶液中, 对于一对无相互作用的分子, 在一次遭遇中它们在笼中的时间为 $10^{-12} \sim 10^{-11}$ s, 在这段时间内要进行 $100 \sim 1000$ 次的碰撞。然后, 分子偶尔有机会跃出这个笼子, 扩散到别处, 又进入另一个笼中。可见, 溶液中分子的碰撞与气体中分子的碰撞不同, 后者的碰撞是连续进行的, 而前者则是间断式进行的, 一次遭遇相当于一批碰撞, 它包含着多次的碰撞。而就单位时间内总碰撞次数而论, 两者大致相同, 不会有数量级上的变化。所以, 溶剂的存在不会使活化分子减少。A 和 B 发生反应必须通过扩散进入同一笼中, 反应物分子通过溶剂分子所构成的笼所需要的活化能一般不超过 $20\mathrm{kJ} \cdot \mathrm{mol}^{-1}$ , 而分子碰撞进行反应的活化能一般在 $40 \sim 400\mathrm{kJ} \cdot \mathrm{mol}^{-1}$ 。由于扩散作用的活化能小得多, 所以扩散作用一般不会影响反应的速率。但也有不少反应的活化能很小, 例如自由基的复合反应、水溶液中的离子反应等, 则反应速率取决于分子的扩散速度, 即与分子在笼中时间成反比。

在溶液中, 溶剂对反应速率的影响是一个极其复杂的问题, 一般说来有以下几方面。

(1) 溶剂的介电常数对于有离子参加的反应的影响 因为溶剂的介电常数越大, 离子间的引力越弱, 所以介电常数比较大的溶剂常不利于离子间的化合反应。

(2) 溶剂的极性对反应速率的影响 如果产物的极性比反应物的极性大, 则在极性溶剂中反应速率比较快; 反之, 如果反应物的极性比产物的极性大, 则在极性溶剂中的反应速率必变慢。例如, 使反应

$$
\mathrm{C} _ {2} \mathrm{H} _ {5} \mathrm{I} + (\mathrm{C} _ {2} \mathrm{H} _ {5}) _ {3} \mathrm{N} \longrightarrow (\mathrm{C} _ {2} \mathrm{H} _ {5}) _ {4} \mathrm{N} ^ {+} \mathrm{I} ^ {-}
$$

在各种不同的溶剂中进行, 由于产物 $\left(\mathrm{C}_{2} \mathrm{H}_{5}\right)_{4} \mathrm{~N}^{+} \mathrm{I}^{-}$ 是一种盐类, 其极性远较反应物的大, 所以随着溶剂极性的增加, 反应速率也变快。

(3) 溶剂化的影响 一般来说, 作用物与产物在溶液中都能或多或少地形成溶剂化物。这些溶剂化物若与任一种反应分子生成不稳定的中间化合物而使活化能降低, 则可以使反应速率变快。如果溶剂分子与作用物生成比较稳定的化合物, 则一般常能使活化能升高, 而使反应速率变慢。如果活化络合物溶剂化后的能量降低, 则活化能降低, 就会使反应速率变快。

(4) 离子强度的影响 在稀溶液中, 如果作用物都是电解质, 则反应的速率与溶液的离子强度有关, 这种效应则称为原盐效应 (primary salt effect)。

原盐效应

早在 20 世纪 20 年代, Bjerrum 等人已假设溶液中反应离子在转化成产物之前要经过一个中间体, 并导出了速率常数与离子活度因子之间的关系式。这个中间体相当于过渡态, 后来人们用过渡态理论也导出了类似的关系式。

设在溶液中离子 $A^{z_{A}}$ 和 $B^{z_{B}}$ 的反应为

$$
\mathrm{A} ^ {z _ {\mathrm{A}}} + \mathrm{B} ^ {z _ {\mathrm{B}}} \rightleftharpoons [ (\mathrm{A} - - - \mathrm{B}) ^ {z _ {\mathrm{A}} + z _ {\mathrm{B}}} ] ^ {\neq} \xrightarrow {k} \mathrm{P}
$$

式中 $z_{A}$ 和 $z_{B}$ 分别为离子 A, B 的电价。根据过渡态理论的热力学处理方法，有

$$
k = \frac {k _ {\mathrm{B}} T}{h} K _ {c} ^ {\neq}
$$

考虑到在通常的溶液浓度范围内, $K_{c}^{\neq}$ 并不是常数,而 $K_{a}^{\neq}$ 才是常数,即

$$
\begin{array}{r l} K _ {a} ^ {\mp} & = \frac {a ^ {\mp}}{a _ {\mathrm{A}} a _ {\mathrm{B}}} = \frac {c ^ {\mp} / c ^ {\ominus}}{\frac {c _ {\mathrm{A}}}{c ^ {\ominus}} \frac {c _ {\mathrm{B}}}{c ^ {\ominus}}} \cdot \frac {\gamma^ {\mp}}{\gamma_ {\mathrm{A}} \gamma_ {\mathrm{B}}} \\ & = K _ {c} ^ {\mp} \cdot (c ^ {\ominus}) ^ {n - 1} \frac {\gamma^ {\mp}}{\gamma_ {\mathrm{A}} \gamma_ {\mathrm{B}}} \end{array}\tag{12.64}
$$

式中 n 为反应离子的计量系数之和。因此

$$
\begin{array}{r l} k & = \frac {k _ {\mathrm{B}} T}{h} (c ^ {\ominus}) ^ {1 - n} K _ {a} ^ {\neq} \cdot \frac {\gamma_ {\mathrm{A}} \gamma_ {\mathrm{B}}}{\gamma^ {\neq}} \\ & = k _ {0} \frac {\gamma_ {\mathrm{A}} \gamma_ {\mathrm{B}}}{\gamma^ {\neq}} \end{array}\tag{12.65}
$$

从式(12.65)看出,速率常数 k 与活度因子有关。 $k_{0}$ 值一般可由实验测定,在溶液中离子反应常选无限稀释的溶液为参考态,这时 $\gamma_{i}=1,k=k_{0},\gamma^{\neq}$ 是活化络合物的活度因子。不同的过渡态有不同的 $\gamma^{\neq}$ 值,它不能用一般的方法测定,而要与相同结构的分子进行比较而估计得到。

将式 $(12.65)$ 取对数, 得

$$
\lg \frac {k}{k _ {0}} = \lg \gamma_ {\mathrm{A}} + \lg \gamma_ {\mathrm{B}} - \lg \gamma^ {\neq}\tag{12.66}
$$

根据 Debye-Hückel 极限公式:

$$
\lg \gamma_ {i} = - A z _ {i} ^ {2} \sqrt {I}
$$

代入式 (12.66), 得

$$
\begin{array}{r l} \lg \frac {k}{k _ {0}} & = - A [ z _ {\mathrm{A}} ^ {2} + z _ {\mathrm{B}} ^ {2} - (z _ {\mathrm{A}} + z _ {\mathrm{B}}) ^ {2} ] \sqrt {I} \\ & = 2 z _ {\mathrm{A}} z _ {\mathrm{B}} A \sqrt {I} \end{array}\tag{12.67}
$$

以 $\lg k$ 或 $\lg \frac{k}{k_0}$ 对 $\sqrt{I}$ 作图, 则应得到直线, 直线的斜率与 $z_{\mathrm{A}}$ 和 $z_{\mathrm{B}}$ 有关。图12.15中直线是根据式(12.67)绘制的, 图中的圆点是实验值。

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_200-399_images/4a3d387c4637a03e3fa570e09af3549320c56194b8cf2095b620ac5fa78edb18.jpg)  
图 12.15 原盐效应

从式 (12.67) 可知, 如果作用物之一是非电解质, 则 $z_{\mathrm{A}} z_{\mathrm{B}} = 0$ , 即原盐效应等于零。也就是说, 非电解质之间反应的速率以及非电解质与电解质之间反应的速率与溶液中的离子强度无关 (这个结论是由 Debye-Hückel 极限公式得来的, 当浓度较高时, 这个结论就不正确了)。例如, 反应:

$$
\mathrm{CH} _ {2} \mathrm{ICOOH} + \mathrm{SCN} ^ {-} \longrightarrow \mathrm{CH} _ {2} (\mathrm{SCN}) \mathrm{COOH} + \mathrm{I} ^ {-}
$$

就属于这一类型。对于反应:

$$
\mathrm{CH} _ {2} \mathrm{BrCOO} ^ {-} + \mathrm{S} _ {2} \mathrm{O} _ {3} ^ {2 -} \longrightarrow \mathrm{CH} _ {2} (\mathrm{S} _ {2} \mathrm{O} _ {3}) \mathrm{COO} ^ {2 -} + \mathrm{Br} ^ {-}
$$

$z_{A}z_{B}=+2$ , 产生正的原盐效应, 即反应的速率随离子强度 I 的增大而变快。对于反应:

$$
[ \mathrm{CO} (\mathrm{NH} _ {3}) _ {5} \mathrm{Br} ] ^ {2 +} + \mathrm{OH} ^ {-} \longrightarrow [ \mathrm{CO} (\mathrm{NH} _ {3}) _ {5} \mathrm{OH} ] ^ {2 +} + \mathrm{Br} ^ {-}
$$

$z_{A}z_{B}=-2$ ，产生负的原盐效应，即反应的速率随离子强度I的增大而变慢。

## \*由扩散控制的反应

溶液中所进行的反应是由相互遭遇的分子进行的。反应物分子 A, B 在一定黏度的介质中做布朗运动，则反应速率一定与 A, B 通过扩散进而形成“遭遇对”AB 的速率有关。特别是对反应活化能不大的反应，则反应速率将受扩散的控制（例如有自由基参加的反应、酸碱中和反应等一般都受扩散的控制）。

对溶液中 A 和 B 所进行的反应, 可表示为如下的机理:

$$
\mathrm{A} + \mathrm{B} \xrightarrow [ k _ {- \mathrm{d}} ]{k _ {\mathrm{d}}} \mathrm{AB} \xrightarrow {k _ {\mathrm{r}}} \mathrm{P}
$$

式中 AB 表示 “遭遇对”; $k_{d}$ 为形成遭遇对的速率常数; $k_{-d}$ 是遭遇对分离为 A, B 的速率常数; $k_{r}$ 为遭遇对进行反应的速率常数。利用稳态处理法, 即认为反应达稳态时, 遭遇对的浓度不随时间改变而改变, 则

$$
\frac {\mathrm{d} [ \mathrm{AB} ]}{\mathrm{d} t} = k _ {\mathrm{d}} [ \mathrm{A} ] [ \mathrm{B} ] - k _ {- \mathrm{d}} [ \mathrm{AB} ] - k _ {\mathrm{r}} [ \mathrm{AB} ] = 0
$$

解得

$$
[ \mathrm{AB} ] = \frac {k _ {\mathrm{d}} [ \mathrm{A} ] [ \mathrm{B} ]}{k _ {- \mathrm{d}} + k _ {\mathrm{r}}}
$$

反应的总速率取决于 [AB], 即

$$
r = k _ {\mathrm{r}} [ \mathrm{AB} ]
$$

代入上式后得

$$
r = k _ {\mathrm{r}} \frac {k _ {\mathrm{d}} [ \mathrm{A} ] [ \mathrm{B} ]}{k _ {- \mathrm{d}} + k _ {\mathrm{r}}} = k [ \mathrm{A} ] [ \mathrm{B} ]
$$

式中

$$
k = \frac {k _ {\mathrm{r}} k _ {\mathrm{d}}}{k _ {- \mathrm{d}} + k _ {\mathrm{r}}}
$$

从上式可知, 反应可能有两种情况:

(1) 若在黏度较大的溶剂中, 遭遇对分离为 A 和 B 较难, 或者是反应的活化能很小, 此时 $k_{r} \gg k_{-d}$ , 则 $k = k_{d}$ , 即

$$
r = k _ {\mathrm{d}} [ \mathrm{A} ] [ \mathrm{B} ]\tag{12.68}
$$

这时反应主要由扩散控制。

(2) 若遭遇对反应变为产物的活化能大, 则反应为活化过程所控制, $k_{r} \ll k_{-d}$ , 则

$$
k = k _ {\mathrm{r}} \frac {k _ {\mathrm{d}}}{k _ {- \mathrm{d}}} = k _ {\mathrm{r}} K\tag{12.69}
$$

式中 K 为反应物分子形成遭遇对的平衡常数。式 (12.69) 表明, 反应的总速率由形成遭遇对的平衡常数以及遭遇对越过反应势垒变为产物的速率所决定。

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_200-399_images/02f6a621ce3318575b9b04cc4bc7a755ee355f915e3e368847f72d9ec40aee4c.jpg)  
图 12.16 扩散控制反应的模型

现在讨论第一种情况, 即反应受扩散控制, 反应的总速率等于扩散速率。可设想如下的模型: A 分子不动, 任何 B 分子只要进入以 A 分子为中心, 以 $r_{\mathrm{AB}}(r_{\mathrm{AB}} = r_{\mathrm{A}} + r_{\mathrm{B}})$ 为半径的球内时, 即可与 A 分子反应。由于反应速率很快, 所以在 A 分子邻近的区域中 B 分子的浓度降低, 形成一个浓度梯度 (见图 12.16)。根据菲克第一定律 (Fick's first law), 单位时间内通过单位截面的物质的流量 $J$ 与浓度梯度成正比 (参见 14.3 节), 即

$$
J = - D _ {\mathrm{B}} \frac {\mathrm{d} N _ {\mathrm{B}}}{\mathrm{d} r}\tag{12.70}
$$

式中比例系数 $D_{B}$ 是 B 分子的扩散系数, 可以看作单位浓度梯度时的流量; $N_{B}$ 为 B 分子的浓度 (单位体积中的分子数), $\frac{dN_{B}}{dr}$ 是在距离为 r 处的浓度梯度; 式中负号表示扩散的方向与浓度增大的方向相反 (即与 r 的增加方向相反)。

因此通过以 A 分子为球心, 以 r 为半径的球面的 B 分子的流量为

$$
I _ {\mathrm{B}} = 4 \pi r ^ {2} J = - 4 \pi r ^ {2} D _ {\mathrm{B}} \frac {\mathrm{d} N _ {\mathrm{B}}}{\mathrm{d} r}
$$

或

$$
\frac {I _ {\mathrm{B}}}{r ^ {2}} \mathrm{d} r = - 4 \pi D _ {\mathrm{B}} \mathrm{d} N _ {\mathrm{B}}\tag{12.71}
$$

当 $r = r_{\mathrm{AB}}$ 时， $N_{\mathrm{B}} = 0$ 。当 $r = \infty$ 时， $N_{\mathrm{B}} = N_{\mathrm{B}}^{0}$ ( $N_{\mathrm{B}}^{0}$ 是 B 的本体浓度)。对式 (12.71) 积分，则

$$
\begin{array}{r} \int_ {r _ {\mathrm{AB}}} ^ {\infty} \frac {I _ {\mathrm{B}}}{r ^ {2}} \mathrm{d} r = \int_ {0} ^ {N _ {\mathrm{B}} ^ {0}} - 4 \pi D _ {\mathrm{B}} \mathrm{d} N _ {\mathrm{B}} \\ I _ {\mathrm{B}} = 4 \pi D _ {\mathrm{B}} r _ {\mathrm{AB}} N _ {\mathrm{B}} ^ {0} \end{array}
$$

若是单位时间, $I_{\mathrm{B}}$ 就是对于1个A分子而言, 在单位时间内与B分子的反应速率。实际上A分子不止一个(设A的本体浓度为 $N_{\mathrm{A}}^{0}$ ), 故假设A分子不动时, 与扩散进来的B分子发生反应的速率 $r_{(\mathrm{A}\text{与B})}$ 为

$$
r _ {(\mathrm{A} \mathrm{与} \mathrm{B})} = 4 \pi D _ {\mathrm{B}} r _ {\mathrm{AB}} N _ {\mathrm{B}} ^ {0} N _ {\mathrm{A}} ^ {0}
$$

同理, 若设 B 分子不动, 与扩散进来的 A 分子发生反应的速率 $r_{(B \text{ 与 } A)}$ 为

$$
r _ {(\mathrm{B} \mathrm{与} \mathrm{A})} = 4 \pi D _ {\mathrm{A}} r _ {\mathrm{AB}} N _ {\mathrm{B}} ^ {0} N _ {\mathrm{A}} ^ {0}
$$

事实上, A 和 B 都有明显的扩散倾向。所以, 单位体积内发生反应的总速率 $r_{D}$ 为

$$
r _ {\mathrm{D}} = r _ {(\mathrm{A} \mathrm{与} \mathrm{B})} + r _ {(\mathrm{B} \mathrm{与} \mathrm{A})} = 4 \pi (D _ {\mathrm{A}} + D _ {\mathrm{B}}) r _ {\mathrm{AB}} N _ {\mathrm{A}} ^ {0} N _ {\mathrm{B}} ^ {0}\tag{12.72}
$$

再对照式 (12.68), 可得

$$
k = k _ {\mathrm{d}} = 4 \pi (D _ {\mathrm{A}} + D _ {\mathrm{B}}) r _ {\mathrm{AB}}\tag{12.73}
$$

根据 Stokes-Einstein 扩散系数公式 (参见 14.3 节)

$$
D = \frac {k _ {\mathrm{B}} T}{6 \pi \eta r}\tag{12.74}
$$

式中 $k_{B}$ 为 Boltzmann 常数; $\eta$ 为黏度; r 为扩散粒子的半径。将式 (12.74) 代入式 (12.73) (式中 $r_{AB} = r_{A} + r_{B}$ ), 得

$$
\begin{array}{r l} & k _ {\mathrm{d}} = 4 \pi (r _ {\mathrm{A}} + r _ {\mathrm{B}}) \frac {k _ {\mathrm{B}} T}{6 \pi \eta} \left(\frac {1}{r _ {\mathrm{A}}} + \frac {1}{r _ {\mathrm{B}}}\right) \\ & = \frac {2 k _ {\mathrm{B}} T}{3 \eta} \frac {(r _ {\mathrm{A}} + r _ {\mathrm{B}}) ^ {2}}{r _ {\mathrm{A}} r _ {\mathrm{B}}} \end{array}
$$

当 $r_{\mathrm{A}} \approx r_{\mathrm{B}}$ 时, 有

$$
k _ {\mathrm{d}} = \frac {8 k _ {\mathrm{B}} T}{3 \eta}\tag{12.75}
$$

而溶剂黏度 $\eta$ 与温度的关系所遵循的公式与Arrhenius公式类似，即

$$
\eta = A \exp \left(\frac {E _ {\mathrm{a}}}{R T}\right)
$$

式中 $E_{a}$ 是扩散过程的活化能。将上式代入式 (12.75)，得

$$
k _ {\mathrm{d}} = \frac {8 k _ {\mathrm{B}} T}{3 A} \exp \left(- \frac {E _ {\mathrm{a}}}{R T}\right)\tag{12.76}
$$

根据式 (12.76), 可以计算当反应为扩散控制时的活化能。对于大多数有机溶剂, $E_{\mathrm{a}}$ 约为 $10 \mathrm{~kJ} \cdot \mathrm{mol}^{-1}$ 。显然, 扩散活化能越低, 扩散控制的反应速率越快, 低活化能是扩散控制反应的特点。

## \*12.6 快速反应的几种测试手段

对单分子反应来说, 速率常数的极限值可达 $10^{12} \sim 10^{14} \mathrm{~s}^{-1}$ , 双分子反应的速率常数值亦可大到 $10^{11} \mathrm{~mol}^{-1} \cdot \mathrm{dm}^{3} \cdot \mathrm{s}^{-1}$ 。例如, 1955 年 Eigen 等人用解离场效应方法, 测得酸碱中和的正向反应速率常数约为 $1.4 \times 10^{11} \mathrm{~mol}^{-1} \cdot \mathrm{dm}^{3} \cdot \mathrm{s}^{-1}$ , 而传统测量反应速率的物理化学方法则不能测量如此快速反应的速率, 可见对于快速反应 (fast reaction) 要求用特殊的测量方法。随着科学技术的发展, 特别是时间分辨技术的提高 (目前对时间可精确测至 $10^{-15} \mathrm{~s}$ ), 对快速反应动力学的研究已有不少实验方法, 如表 12.2 所示。

表 12.2 快速反应的实验方法及其应用范围

<table><tr><td>实验方法</td><td>适用的半衰期范围/s</td></tr><tr><td>传统方法</td><td> $10^{0} \sim 10^{8}$ </td></tr><tr><td>流动法</td><td> $10^{-3} \sim 10^{2}$ </td></tr><tr><td>弛豫法</td><td> $10^{-10} \sim 1$ </td></tr><tr><td>跳浓弛豫法</td><td> $10^{-6} \sim 1$ </td></tr><tr><td>跳温弛豫法</td><td> $10^{-7} \sim 1$ </td></tr><tr><td>场脉冲法</td><td> $10^{-10} \sim 10^{-4}$ </td></tr><tr><td>激波管法</td><td> $10^{-9} \sim 10^{-3}$ </td></tr><tr><td>动力学波谱法</td><td> $< 10^{-10}$ </td></tr></table>

本节仅对弛豫法和闪光光解法作简单介绍。

弛豫法

弛豫是指一个平衡系统因受外来因素快速扰动而偏离平衡位置，在新条件下趋向新平衡的过程。弛豫法（relaxation method）包括快速扰动方法和快速监测扰动后的不平衡态趋近于新平衡态的速度或时间。快速扰动的方法可以用脉冲激光使反应系统温度在 $10^{-6}$ s 时间内突然升高几摄氏度 (温度跳跃)，或突然改变系统的压力 (压力跳跃)，也可用冲稀扰动，即突然改变系统的浓度 (浓度跳跃)，等等。由于弛豫时间与速率常数、平衡常数和物种平衡浓度有一定的函数关系，因此如能用实验测出弛豫时间，就可根据该关系式求出反应的速率常数。弛豫法是在 20 世纪 50 年代由 Eigen 等人发展起来的。对峙反应的平衡常数一般借助于热力学方法比较容易得到，因此，借助于弛豫过程的动力学研究测定其弛豫时间或弛豫速率常数，即可求得正向反应和逆向反应的速率常数。这对于测定对峙反应尤其是快速进行的对峙反应是很有效的。现以一级快速对峙反应为例，求弛豫时间与速率常数的关系。设一级快速对峙反应为

$$
\mathrm{A} \xrightarrow [ k _ {- 1} ]{k _ {1}} \mathrm{P}\tag{1}
$$

令 a 是 A 的原始浓度, x 为 P 的浓度, 则在 t 时的速率方程为

$$
\frac {\mathrm{d} x}{\mathrm{d} t} = k _ {1} (a - x) - k _ {- 1} x\tag{2}
$$

若式中 $k_{1}$ 或 $k_{-1}$ 是很大的, 不可能用通常的方法来测定。如果先让此系统在某一温度下达成平衡, 然后用特殊方法使温度发生突变 (温度跳跃), 原平衡被破坏, 系统向新条件下的平衡转移。若在新平衡条件下产物的平衡浓度为 $x_{e}$ , 则有

$$
k _ {1} (a - x _ {\mathrm{e}}) = k _ {- 1} x _ {\mathrm{e}}\tag{3}
$$

系统在发生突变后, 产物的浓度 x 与新的平衡浓度 $x_{e}$ 之差为 $\Delta x$ , 则

$$
\Delta x = x - x _ {\mathrm{e}} \qquad \text {或} \qquad x = \Delta x + x _ {\mathrm{e}}\tag{4}
$$

对产物 P 如有正的偏离, 则对反应物 A 应有负的偏离, 反之亦然。根据式 (2) 和式 (4), 可得

$$
\begin{array}{r l} \frac {\mathrm{d} (\Delta x)}{\mathrm{d} t} & = \frac {\mathrm{d} x}{\mathrm{d} t} = k _ {1} (a - x) - k _ {- 1} x \\ & = k _ {1} [ (a - x _ {\mathrm{e}}) - \Delta x ] - k _ {- 1} (\Delta x + x _ {\mathrm{e}}) \end{array}\tag{5}
$$

将式 (3) 代入式 (5), 整理得

$$
\frac {\mathrm{d} (\Delta x)}{\mathrm{d} t} = - (k _ {1} + k _ {- 1}) \Delta x\tag{6}
$$

因此, 与新平衡的偏离值 $\Delta x$ 随时间的变化率 $\frac{\mathrm{d}(\Delta x)}{\mathrm{d}t}$ (即为系统向新平衡位置的转移速率) 与一级对峙反应中浓度随时间的变化规律相似。将式 (6) 移项积分, 当“刺激”刚停止时, 也就开始计算时间, 这时 $t = 0$ , $\Delta x = (\Delta x)_0$ 。显然起始时$(\Delta x)_{0}$ 的值是偏离新平衡的最大值, 当时间为 $t$ 时, 偏离值为 $\Delta x$ , 则

$$
\int_ {(\Delta x) _ {0}} ^ {\Delta x} \frac {\mathrm{d} (\Delta x)}{\Delta x} = \int_ {0} ^ {t} - (k _ {1} + k _ {- 1}) \mathrm{d} t
$$

$$
\ln \frac {(\Delta x) _ {0}}{\Delta x} = (k _ {1} + k _ {- 1}) t\tag{7}
$$

式中常数 $(k_{1} + k_{-1})$ 的量纲是[时间]^{-1}, 若令 $\frac{1}{k_1 + k_{-1}} = \tau$ , 则 $\ln \frac{(\Delta x)_0}{\Delta x} = \frac{t}{\tau}$ 。当 $\frac{(\Delta x)_0}{\Delta x} = e$ (e 是自然对数的底数, $e = 2.718$ ), 或 $\Delta x = \frac{(\Delta x)_0}{e} = 0.3679(\Delta x)_0$ 时, 有

$$
\ln \frac {(\Delta x) _ {0}}{\Delta x} = \mathrm{lne} = 1
$$

则

$$
\tau = t = \frac {1}{k _ {1} + k _ {- 1}}\tag{8}
$$

此时 $\tau$ 即为 $\Delta x$ (系统的浓度与平衡浓度之差) 达到 $(\Delta x)_0$ (起始时的最大偏离值) 的 $36.79\%$ 所需的时间, 称为弛豫时间 (time of relaxation)。因此, 如能用实验的方法精确测定弛豫时间 $\tau$ , 则可求得 $(k_1 + k_{-1})$ 的值, 再结合平衡常数 $K = \frac{k_1}{k_{-1}}$ , 就能分别求得 $k_1$ 和 $k_{-1}$ 的值。现代的一些实验手段, 例如有自动记录设备的核磁共振 (NMR) 谱仪、电子自旋共振 (ESR) 谱仪及用振荡器跟踪电导的变化等能在极短时间内反映出系统发生变化的信息。

对于其他级数的快速对峙反应, 可用同样的方法导出弛豫时间 $\tau$ 的表示式, 现仅将其结果列于表 12.3。

表 12.3 几种简单快速对峙反应弛豫时间的表示式

<table><tr><td>对峙反应</td><td> $\frac{1}{\tau}$ 的表示式</td></tr><tr><td>A  $\xrightarrow[k_{-1}] {k_1}$  P</td><td> $(k_1 + k_{-1})$ </td></tr><tr><td>A + B  $\xrightarrow[k_{-1}] {k_2}$  P</td><td> $k_2([A]_e + [B]_e) + k_{-1}$ </td></tr><tr><td>A  $\xrightarrow[k_{-2}] {k_1}$  G + H</td><td> $k_1 + 2k_{-2}x_e$ </td></tr><tr><td>A + B  $\xrightarrow[k_{-2}] {k_2}$  G + H</td><td> $k_2([A]_e + [B]_e) + k_{-2}([G]_e + [H]_e)$ </td></tr></table>

## 例12.2

在一个很小的电导池中放纯水试样, 用微波脉冲辐射突然使温度从 $288 \mathrm{~K}$ 升到 $298 \mathrm{~K}$ , 测得弛豫时间为 $\tau = 3.6 \times 10^{-5} \mathrm{~s}$ 。已知 $298 \mathrm{~K}$ 时, 水的解离常数 $K_{\mathrm{w}} = 1.0 \times 10^{-14}$ , 求水解离反应 $\mathrm{H}_{2} \mathrm{O} \xrightarrow{k_{1}} \mathrm{H}^{+} + \mathrm{OH}^{-}$ 的速率常数 $k_{1}$ 和 $k_{-2}$ 。

解

$$
\begin{array}{r l} & K = \frac {k _ {1}}{k _ {- 2}} = \frac {[ \mathrm{H} ^ {+} ] [ \mathrm{OH} ^ {-} ]}{[ \mathrm{H} _ {2} \mathrm{O} ]} \\ & = \frac {1 . 0 \times 1 0 ^ {- 1 4} (\mathrm{mol} \cdot \mathrm{dm} ^ {- 3}) ^ {2}}{5 5 . 5 \mathrm{mol} \cdot \mathrm{dm} ^ {- 3}} = 1. 8 \times 1 0 ^ {- 1 6} \mathrm{mol} \cdot \mathrm{dm} ^ {- 3} \end{array}
$$

$$
\begin{array}{r l} & x _ {\mathrm{e}} = \sqrt {K _ {\mathrm{w}}} = 1. 0 \times 1 0 ^ {- 7} \mathrm{mol} \cdot \mathrm{dm} ^ {- 3} \\ & \tau = \frac {1}{k _ {1} + 2 k _ {- 2} x _ {\mathrm{e}}} \\ & = \frac {1}{1 . 8 \times 1 0 ^ {- 1 6} k _ {- 2} \mathrm{mol} \cdot \mathrm{dm} ^ {- 3} + 2 k _ {- 2} \times 1 . 0 \times 1 0 ^ {- 7} \mathrm{mol} \cdot \mathrm{dm} ^ {- 3}} \end{array}
$$

解得

$$
\begin{array}{r l} & k _ {- 2} = 1. 4 \times 1 0 ^ {1 1} \mathrm{mol} ^ {- 1} \cdot \mathrm{dm} ^ {3} \cdot \mathrm{s} ^ {- 1} \\ & k _ {1} = K k _ {- 2} = 1. 8 \times 1 0 ^ {- 1 6} \mathrm{mol} \cdot \mathrm{dm} ^ {- 3} \times 1. 4 \times 1 0 ^ {1 1} \mathrm{mol} ^ {- 1} \cdot \mathrm{dm} ^ {3} \cdot \mathrm{s} ^ {- 1} \\ & = 2. 5 \times 1 0 ^ {- 5} \mathrm{s} ^ {- 1} \end{array}
$$

可以看出, $k_{-2}$ 是一个很大的数值, 它就是酸碱中和的速率常数。

## 闪光光解法

自从 20 世纪 40 年代末问世以来, 闪光光解 (flash photolysis) 技术已经发展成为一种测定快速反应的十分有效的手段。实验装置的基本原理是: 将反应物放在一长石英管中 (一般可长至 1 m), 管两端有平面窗口, 与反应管平行有一石英制闪光管, 它能产生能量高、持续时间很短的强烈闪光。在这种闪光被反应物吸收的瞬间, 会引起反应物中的电子激发, 发生化学反应。对这种光解产物 (主要是自由原子或自由基碎片) 通过窗口用光谱技术 (如紫外、可见吸收光谱, 磁共振谱等) 进行测定, 并监测这些碎片随时间的衰变行为。由于所用的闪光强度很高, 可以产生比一般反应历程中生成的碎片浓度高得多的自由基。所以, 闪光光解技术对鉴定寿命极短的自由基特别有用。

闪光光解的时间分辨率取决于闪光灯的闪烁时间, 若闪烁时间为 $20 \mu s$ 左右, 则测一级反应的半衰期可达 $10^{-6} s$ 。如果用激光器 (用超短脉冲激光) 代替闪光管, 则可产生持续时间在 $10^{-9} s$ 甚至 $10^{-15} s$ 的激光脉冲, 可以大大提高测量时间的分辨率。

## 12.7 光化学反应

闪光光解法的主要优点是可利用闪烁时间比要检测的物种的寿命短得多的强闪光灯，因而曾发现了许多反应的中间产物（自由基），并能有效地研究反应极快的原子复合反应动力学。另外所用反应管较长，也为光谱检测提供了一个很长的光程。

## 12.7 光化学反应

## 光化学反应与热化学反应的区别

只有在光的作用下才能进行的化学反应或由于化学反应产生的激发态粒子在跃迁到基态时能放出光辐射的反应都称为光化学反应（photochemical reaction）。光化学现象虽早为人们所知，但光化学（photochemistry）成为有理论基础的科学还只是近几十年的事。

光是一种电磁辐射, 具有波动和微粒的二重性。光化学既与电磁辐射有关, 又与物质的相互作用有关。所以, 光化学处于化学和物理的交汇点, 在讨论光化学过程的同时, 有必要简单介绍一些光的吸收和发射等物理过程。

可见光的波长范围是 $400 \sim 750 \, nm$ ，紫外光的波长范围为 $150 \sim 400 \, nm$ ，近红外光的波长范围为 $750 \sim 3 \times 10^{3} \, nm$ 。在光化学中，人们关注波长在 $100 \sim 1000 \, nm$ 的光波（其中包括紫外光、可见光和红外光）。光子的能量随光的波长的增大而下降，因为一个光子的能量 $\varepsilon$ 为

$$
\varepsilon = h \nu
$$

而波长

$$
\lambda = \frac {c}{\nu}
$$

则

$$
\varepsilon = h \frac {c}{\lambda}
$$

式中 h 为 Planck 常量; c 为光速; $\nu$ 为频率。在光谱学习中习惯用波数 (wave number) $\sigma$ 即波长的倒数 $\left(\sigma = \frac{1}{\lambda}\right)$ 来表示光子的能量。对光化学反应有效的光是可见光和紫外光, 红外光由于能量较低, 不足以引发化学反应 (但红外激光是可

以引发化学反应的)。

相对于光化学反应来讲, 平常的那些反应可称为热反应。光化学反应与热反应有许多不同的地方。例如, 在等温等压下, 热反应总是向系统的 Gibbs 自由能降低的方向进行。但有许多光化学反应 (并不是所有的光化学反应) 却能使系统的 Gibbs 自由能升高, 如在光的作用下氧转变为臭氧、氨的分解, 植物中 $\mathrm{CO}_{2}(\mathrm{~g})$ 与 $\mathrm{H}_{2}\mathrm{O}(\mathrm{l})$ 合成糖类并放出氧气等, 都是 Gibbs 自由能升高的例子。但如果把辐射的光源切断, 则该反应仍旧向 Gibbs 自由能降低的方向进行, 而力图恢复原来的状态。但这个反向反应在寻常的温度下, 有可能进行得很慢, 以致觉察不出。例如, 糖类和氧气在同样的条件下再变为 $\mathrm{CO}_{2}(\mathrm{~g})$ 和 $\mathrm{H}_{2}\mathrm{O}(\mathrm{l})$ 的反应就是如此。

热反应的活化能来源于分子碰撞, 而光化学反应的活化能来源于光子的能量 (光化学反应的活化能通常为 $30 \, kJ \cdot mol^{-1}$ 左右, 小于一般热反应的活化能)。热反应的反应速率受温度影响大, 而光化学反应的温度系数较小。这些都是热反应与光化学反应的主要不同之处。但初始光化学过程的速率常数也随温度而变, 且也遵从 Arrhenius 公式。这和普通的化学反应是一致的。

当系统吸收了光子的能量而成为激发态后, 激发态的寿命是很短暂的 (一般在 $10^{-7} \mathrm{~s}$ 左右), 在此期间激发态的变化有两种可能: ① 进行后续的光化学反应; ② 激发态自我衰变, 如以辐射方式放出荧光或磷光等。这两种可能形成竞争形式。因此, 只有活化能较小, 反应速率快者才能取得优势, 并按第一种可能进行光化学反应。这也是我们所观察到的光化反应其活化能均较小的原因。而热反应的初始过程, 反应分子都处于基态, 能量较低, 具有较高的活化能, 反应速率相对较慢。

光化学反应和热反应之间的主要区别, 即在光作用下的化学反应是激发态分子的反应, 而在非光作用下的化学反应通常是基态分子的反应 (有时也称为暗反应, 即一般的热反应)。因此, 用 “光催化” 一词来描述光化学反应, 是不确切的。催化剂在反应结束后, 催化剂的化学组成没有发生变化, 而光化学反应后, 光却被吸收掉了, 二者有本质上的不同。

研究光化学的重要性是不言而喻的, 植物的叶绿素能利用日光把 $\mathrm{CO}_{2}(\mathrm{~g})$ 和 $\mathrm{H}_{2}\mathrm{O}(\mathrm{l})$ 转变成糖类和氧气。这种光合作用是绿色植物的特有本领, 地球上多数生命的生存全仰仗于它。人类当今的重要能源 (煤、石油、天然气) 则是古代光合作用留给我们的遗产。随着粮食、能源、污染问题的日益尖锐, 对光合作用的研究不仅有重要的科学意义, 而且有巨大的经济意义。例如, 结合太阳能的利用, 人们正在进行着光电转换及光化学能转换的研究。

光合作用的化学模拟研究如模拟植物利用阳光把 $\mathrm{CO}_{2}(\mathrm{~g})$ 和 $\mathrm{H}_{2}\mathrm{O}(\mathrm{l})$ 合成糖类和氧气的过程, 若这一模拟成功, 就可以实现人造粮食的理想。光解水制氢的研究模拟光合作用中分解水放出氧和氢, 如这一模拟成功, 就能从水中获得廉价的氢。

与热反应相比, 光化学反应具有许多独特的优点, 所以在科学研究、医学、化工生产和军事应用等方面都得到广泛的应用。

## 光化学反应的初级过程和次级过程

光化学反应是从物质（即反应物）吸收光子开始的，此过程统称为光化反应的初级过程，它使反应物分子或原子中的电子能态由基态跃迁到较高能量的激发态（“\*”表示激发态）。若光子能量很高也可使分子解离，如

$$
\begin{array}{r l} & \mathrm {Hg(g) + h\nu \longrightarrow Hg^ {*} (g)} \\ & \mathrm {Br_ {2} (g) + h\nu \longrightarrow 2Br^ {*} (g)} \end{array}
$$

这两个过程都是初级过程 (primary process), 初级过程的产物还可以进行一系列的次级过程 (secondary process), 如发生猝灭 (quenching)、荧光 (fluorescence) 或磷光 (phosphorescence) 等。猝灭是激发态分子 (A\*) 与其他分子或器壁碰撞后失去能量, 而荧光和磷光则是激发态原子或分子再跃迁回到基态时所发出的光。猝灭使次级反应停止。

原子或分子吸收光子后, 被激发到较高能级的激发态; 由于激发态不稳定而进行辐射跃迁, 直接回到基态时所发生的光称为荧光。激发态的寿命是很短的, 一般只有 $10^{-8} \mathrm{~s}$ ; 由于寿命很短, 所以切断光源, 荧光立即停止。但也有一些被光照射的物质, 在切断光源后, 仍能继续发光, 可延续到若干秒, 甚至更长, 此种光称为磷光。其原因是激发态分子在跃迁回到基态时, 常需经过介稳状态。

激发态分子与其他分子碰撞, 可能将过剩的能量传给被碰撞的分子, 使其激发甚至解离, 也可能与相撞的分子发生反应等, 例如:

$$
\begin{array}{r l} & \mathrm {Hg^ {*} + Tl\longrightarrow Hg+ Tl^ {*}} \\ & \mathrm {Hg^ {*} + H_ {2} \longrightarrow Hg + 2H^ {*}} \\ & \mathrm {Hg^ {*} + O_ {2} \longrightarrow HgO+ O^ {*}} \end{array}
$$

这些都是激发态分子 (或原子) 的次级过程。

## 光化学基本定律

只有被分子吸收的光才能引起分子的光化学反应, 这是 19 世纪时由 Grotthus 和 Draper 总结出来的, 故称为 Grotthus-Draper 定律, 又称为光化学第一定律。根据这个定律, 在进行光化学反应研究时要注意光源、反应器材料及溶剂等的选择。

光化学第二定律是指在初级反应中, 一个反应分子吸收一个光子而被活化。这是 20 世纪初由 Stark 和 Einstein 提出来的, 故称为 Stark-Einstein 定律, 又称为光化学第二定律 (在大多数光化反应中, 光源强度范围为 $10^{14} \sim 10^{18}$ 光子 $\cdot \mathrm{s}^{-1}$ , 这时该定律是有效的。但激光被使用后, 由于光强度超过了上述范围, 人们发现有的分子可吸收两个或更多的光子, 故光化学第二定律对光强度很大、激发态分子寿命较长的情况不适用)。根据该定律, 如要活化 $1\mathrm{mol}$ 分子则要吸收 $1\mathrm{mol}$ 光子。 $1\mathrm{mol}$ 光子的能量称为摩尔光量子能量, 用符号 $E_{\mathrm{m}}$ 表示, 则

$$
\begin{array}{r l} E _ {\mathrm{m}} & = L h \nu = \frac {L h c}{\lambda} \\ & = \frac {6 . 0 2 2 \times 1 0 ^ {2 3} \mathrm{mol} ^ {- 1} \times 6 . 6 2 6 \times 1 0 ^ {- 3 4} \mathrm{J} \cdot \mathrm{s} \times 3 . 0 \times 1 0 ^ {8} \mathrm{m} \cdot \mathrm{s} ^ {- 1}}{\lambda} \\ & = \frac {0 . 1 1 9 7}{\lambda} \mathrm{J} \cdot \mathrm{m} \cdot \mathrm{mol} ^ {- 1} \end{array}
$$

平行的单色光通过一均匀吸收介质时, 未被吸收的透射光强度 $I_{t}$ 与入射光强度 $I_{0}$ 的关系为

$$
I _ {\mathrm{t}} = I _ {0} \exp (- \kappa d c)\tag{12.77}
$$

式中 d 是介质厚度；c 是吸收质的浓度 (用 $mol \cdot dm^{-3}$ 表示)； $\kappa$ 为摩尔吸收系数，其值与入射光的波长、温度、溶剂等性质有关。式 (12.77) 就称为 Lambert-Beer （朗伯－比尔）定律。

量子产率

光化学反应是从物质（即反应物）吸收光子开始的。所以，光的吸收过程是光化学反应的初级过程。光化学第二定律只适用于初级过程，该定律也可用下式表示：

$$
\mathrm{A} + h \nu \longrightarrow \mathrm{A} ^ {*}
$$

A\* 为 A 的电子激发态, 即活化分子。活化分子有可能直接变为产物, 也可能和低能量分子相撞而失活, 或者引发其他次级反应 (如引发一个链反应等)。为了衡量光化学反应的效率, 引入量子产率 (quantum yield) 的概念, 用 $\phi$ 表示。对于指定的反应, 有

$$
\phi = \frac {\mathrm{反应物分子消失数目}}{\mathrm{吸收光子数目}} = \frac {\mathrm{反应物消失的物质的量}}{\mathrm{吸收光子物质的量}}\tag{12.78a}
$$

由上式所定义的 $\phi$ 是反应物消耗的量子产率。也可根据生成的产物分子数目来定义量子产率:

$$
\phi^ {\prime} = \frac {\mathrm{产物分子生成数目}}{\mathrm{吸收光子数目}} = \frac {\mathrm{产物生成的物质的量}}{\mathrm{吸收光子物质的量}}\tag{12.78b}
$$

由于受化学反应式中计量系数的影响, $\phi$ 和 $\phi'$ 的数值很可能是不相等的, 例如:

$$
2 \mathrm{HBr} + h \nu (\lambda = 2 0 0 \mathrm{nm}) \longrightarrow \mathrm{H} _ {2} + \mathrm{Br} _ {2}
$$

显然 $\phi = 2$ ，而 $\phi' = 1$ 。但如用反应速率 $(r)$ 和吸收光子的速率 $(I_{\mathrm{a}})$ 来定义量子产率 $(\phi)$ ，并令

$$
\phi = \frac {r}{I _ {\mathrm{a}}}\tag{12.78c}
$$

则不会引起混淆 $^{①}$ 。反应速率 (r) 可用任何动力学方法测量, 吸收光子的速率 ( $I_{a}$ ) 可用化学光量计 (chemical actinometer) 测量。因此, 量子产率可由实验测定。如果一个光化学过程只包含初级过程, 则问题较为简单。如果初级过程之后接着进行次级过程, 则由于活化分子所进行的次级过程不同, $\phi$ 值可以小于 1, 也可以大于 1。若引发一个链反应, 则 $\phi$ 值甚至可达 $10^{6}$ 。

初级过程的量子产率在理论上具有重要意义。但是, 当初级过程的产物是自由基或自由原子时, 它们的浓度难以测定, 量子产率就难以估算。所以, 最常采用的是求总量子产率, 因为稳定的最终产物其浓度是可以测定的。例如, HI(g) 的光解反应:

$$
\begin{array}{l l} \text {初级过程(光化学反应)} & \mathrm{HI+h} \nu \longrightarrow \mathrm{H} \cdot + \mathrm{I} \cdot \\ \text {次级过程(热反应)} & \left\{ \begin{array}{l} \mathrm{H} \cdot + \mathrm{HI} \longrightarrow \mathrm{H} _ {2} + \mathrm{I} \cdot \\ \mathrm{I} \cdot + \mathrm{I} \cdot \longrightarrow \mathrm{I} _ {2} \end{array} \right. \\ \text {总过程} & 2 \mathrm{HI} \xrightarrow {h \nu} \mathrm{H} _ {2} + \mathrm{I} _ {2} \end{array}
$$

即一个光子可使两个 HI 分子分解, 故 $\phi = 2$ 。若次级过程为链反应, 则 $\phi$ 可能很大。例如, $\mathrm{H}_{2}$ 和 $\mathrm{Cl}_{2}$ 的反应, $\phi$ 值可高达 $10^{4} \sim 10^{6}$ 。若次级过程中包括消活化作用, 则 $\phi$ 可以小于 1 。例如, $\mathrm{CH}_{3} \mathrm{I}$ 的光解反应, $\phi = 0.01$ 。

## \*分子中的能态——Jablonski 图

分子内部各种能级的大小以转动能级为最小, 然后振动能级、电子能级、核能级依次增大。基态分子吸收光子后就被激发, 激发转动、振动能级所需的能量较小, 但分子处于转动或振动激发态时仍不会发生化学变化。只有用较高的能量,使分子出现电子激发态时, 激发态电子的得失, 才能引发光化学反应。

分子激发时的多重性 (multiplicity) $M$ 的定义为

$$
M = 2 s + 1\tag{12.79}
$$

式中 s 为分子中电子的总自旋量子数。如果一对电子是自旋反平行的，则 s = 0；如果是自旋平行的，则 s = 1。多重性 M 代表分子中电子的总自旋角动量在 z 轴方向的分量的多重可能值（简称多重性）。当 s = 0 时，M = 1，在 z 轴方向只有一种分量，这种状态称为单重态，即 S 态。当 s = 1 时，M = 3，即电子总自旋角动量在磁场 z 方向的投影，可以有三个不同的分量，故称为激发三重态，简称 T 态，如图 12.17 所示。

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_200-399_images/c67356535a2aca33dac6412510286f4c256d2374769b34006c9b79cce383b903.jpg)  
图 12.17 分子的多重性

分子吸收光子被激发后的各种光物理过程可用 Jablonski 图 (图 12.18) 来示意说明。

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_200-399_images/51aa5de027582d227db541f0da7ec4680177900f62017bcd8b5321a468ee019b.jpg)  
图 12.18 Jablonski 图

图 12.18 中, 垂直向上代表能量逐步增加, 水平方向没有物理意义。 $S_{0}$ 表示电子基态, 当一个电子被激发时, 激发态 S 中两电子保持自旋反平行, 仍属 S 态, 图 12.18 中 $S_{1}$ 和 $S_{2}$ 分别表示第一和第二激发单重态。当激发电子为自旋平行时, 称为激发三重态。图中 $T_{1}$ 和 $T_{2}$ 表示第一和第二激发三重态 (由图可见, T 态的能量总比相应的 S 态的能量低, 这是因为在三重态中, 两个处于不同轨道的电子自旋平行, 其轨道在空间的重叠较少, 电子的平均间距较长, 相互排斥作用减弱, 因此 T 态的能量总比相应的 S 态的能量低)。图中水平方向每一组线表示一个电子能级, 每个电子能级上有若干个振动能级 (转动能级应在振动能级之间, 图中未标出)。

当分子吸收较强的光子, 其电子从基态被激发至高能级上时可获得分子吸收光谱, 由于在电子被激发的同时, 振动和转动也被激发, 所以分子吸收光谱有相当宽的吸收带。

原则上每一个激发态都可以通过发射光子降低自身的能量而退活化 (deactivation) 到基态。对于孤立原子, 发射波长和吸收波长是相同的。在实际中, 激发分子的退活化过程有许多途径, 主要有辐射跃迁 (radiation transition)、无辐射跃迁 (radiationless transition) 和分子间传能 (intermolecular energy transfer) 三种。前两种是分子内部的传能过程, 第三种则是分子间的传能过程。图 12.18 中向下的实线箭头表示有辐射步骤。当激发态分子从激发单重态 $S_1$ 上的某一能态跃迁到基态 $S_0$ 上的某一能态时所发射的辐射称为荧光 (fluorescence), 即 $S_1 \longrightarrow S_0 + h\nu$ , 这种辐射的寿命很短, 大约只有 $10^{-8} \mathrm{~s}$ 的数量级, 所以一旦切断光源, 荧光立即停止。当激发态分子从 $T_1$ 态跃迁到 $S_0$ 态时, 即 $T_1 \longrightarrow S_0 + h\nu'$ , 所发射的辐射称为磷光 (phosphorescence), 它发生在多重性不同的态间向基态的跃迁。磷光发射寿命较长, 有时可保持数秒。由于从 $S_0$ 态激发到 $S_1, S_2$ 态是自旋允许的, 所以在 $S_1, S_2$ 态上的分子多, 也使得荧光强度较强。而激发到 $T_1, T_2$ 态是自旋禁阻的, 所以在 $T_1, T_2$ 态上的分子少, 使得磷光比较弱。

无辐射跃迁是指发生在激发态分子内部的不发射光子的能量衰变过程。这种能量衰变过程有如下几种形式。

(1) 内转变 (internal conversion, IC), 是多重性相同的电子能态之间的无辐射跃迁, 如 $S_{2} \sim \sim \rightarrow S_{1}^{\nu'}$ (在图 12.18 中用水平波纹线表示), 这种转变是等能的。

(2) 系间窜跃 (inter-system crossing, ISC), 是在多重性不同的态间的无辐射跃迁, 如 $S_{1} \sim \sim \rightarrow T_{1}^{\nu}$ 或 $T_{1} \sim \sim \rightarrow S_{1}^{\nu}$ 。

(3) 振动弛豫 (vibration relaxation), 也属于无辐射跃迁, 即在同一电子能级中, 由较高的振动能级将振动能量变成平动能, 或快速地传递给介质而回到较低的振动能级 (在图 12.18 中用垂直波纹线表示)。当电子被激发到 $\mathrm{S}_2$ 的高振动态

$S_{2}^{\nu}$ 后, 由于振动弛豫非常快 (经过几次分子碰撞即可完成), 则系统很快将一部分能量变为平动能而退活化到 $S_{2}$ 的 v = 0 的振动能级, 故称为振动弛豫。

激发态分子也可以经过分子与分子自身之间的碰撞或与溶剂及杂质分子之间的碰撞, 放出能量 (热) 而导致退活化, 这种过程称为猝灭 (quenching)。例如:

$$
\text {溶剂} (S) \text {猝灭} \quad A ^ {*} + S \longrightarrow A + S + \text {热}
$$

$$
\mathrm{自身猝灭} \qquad \mathrm {A^ {*} + A\longrightarrow2A + \mathrm{热}}
$$

$$
\text { 杂质 } (\mathrm{M}) \text { 猝灭 } \quad \mathrm{A} ^ {*} + \mathrm{M} \longrightarrow \mathrm{A} + \mathrm{M} + \text { 热 }
$$

$$
\text { 电子能量转移 } \quad \mathrm{A} ^ {*} + \mathrm{B} \longrightarrow \mathrm{A} + \mathrm{B} ^ {*}
$$

以上所述都是光的物理过程, 在过程中分子本身保持完整。

如果系统吸收光子后, 分子被激发到能量很高的激发态, 在激发态中有未填满的电子轨道, 则激发态分子的电子有可能失去, 也有可能接受其他分子的电子, 因而引发分子的解离、异构化或与其他分子发生反应, 这就构成光化学反应过程。

## 光化学反应动力学

光化学反应的速率方程较热反应的复杂一些, 它的初级过程与入射光的频率、强度 $(I_{0})$ 有关。因此, 首先要了解其初级过程, 然后还要知道哪几步是次级过程。要确定反应历程, 仍然要依靠实验数据, 测定某些物质的生成速率或某些物质的消耗速率。各种分子光谱在确定初级过程时常是有力的实验工具。

举简单反应 $A_{2}$ $\longrightarrow$ 2A 为例。设其历程为

$$
\begin{array}{l l} (1) \mathrm{A} _ {2} + h \nu \xrightarrow {I _ {\mathrm{a}}} \mathrm{A} _ {2} ^ {*} & (\text {激发活化}) \\ (2) \mathrm{A} _ {2} ^ {*} \xrightarrow {k _ {2}} 2 \mathrm{A} & (\text {解离}) \text {退活化} \\ (3) \mathrm{A} _ {2} ^ {*} + \mathrm{A} _ {2} \xrightarrow {k _ {3}} 2 \mathrm{A} _ {2} & (\text {能量转移而失活}) \end{array} \quad \begin{array}{l l} & \text {初级过程} \\ & \text {次级过程} \\ & \text {次级过程} \end{array}
$$

产物 A 的生成速率为

$$
\frac {\mathrm{d} [ \mathrm{A} ]}{\mathrm{d} t} = 2 k _ {2} [ \mathrm{A} _ {2} ^ {*} ]\tag{a}
$$

光化学反应初级过程的反应速率一般只与入射光的强度有关, 而与反应物浓度无关。因为反应物一般总是过量的, 所以初级光化学反应对反应物呈零级反应。根据光化学第二定律, 则初级过程的反应速率就等于吸收光子的速率 $I_{\mathrm{a}}$ (即单位时间、单位体积中吸收光子的数目或“Einstein”数)。若入射光 $I_{0}$ 没有被全部吸收, 而有一部分变成了透射 (或反射) 光, 设吸收光占入射光的分数为 $a(a = I_{\mathrm{a}} / I_{0})$ , 则 $I_{\mathrm{a}} = aI_{0}$ 。对于上例, 根据反应 (1), $\mathrm{A}_{2}^{*}$ 的生成速率就等于 $I_{\mathrm{a}}$ , 而 $\mathrm{A}_{2}^{*}$ 的消耗速率则由反应 (2), (3) 决定。对 $\mathrm{A}_{2}^{*}$ 作稳态近似, 有

$$
\frac {\mathrm{d} [ \mathrm{A} _ {2} ^ {*} ]}{\mathrm{d} t} = I _ {\mathrm{a}} - k _ {2} [ \mathrm{A} _ {2} ^ {*} ] - k _ {3} [ \mathrm{A} _ {2} ^ {*} ] [ \mathrm{A} _ {2} ] = 0
$$

$$
[ \mathrm{A} _ {2} ^ {*} ] = \frac {I _ {\mathrm{a}}}{k _ {2} + k _ {3} [ \mathrm{A} _ {2} ]}\tag{b}
$$

将式 (b) 代入式 (a), 得

$$
\frac {\mathrm{d} [ \mathrm{A} ]}{\mathrm{d} t} = \frac {2 k _ {2} I _ {\mathrm{a}}}{k _ {2} + k _ {3} [ \mathrm{A} _ {2} ]}\tag{c}
$$

该反应的量子效率为

$$
\phi = \frac {r}{I _ {\mathrm{a}}} = \frac {\frac {1}{2} \frac {\mathrm{d} [ \mathrm{A} ]}{\mathrm{d} t}}{I _ {\mathrm{a}}} = \frac {k _ {2}}{k _ {2} + k _ {3} [ \mathrm{A} _ {2} ]}
$$

例12.3

有人曾测得氯仿在光照下的氯化反应:

$$
\mathrm{CHCl} _ {3} + \mathrm{Cl} _ {2} + h \nu \longrightarrow \mathrm{CCl} _ {4} + \mathrm{HCl}
$$

它的速率方程为

$$
\frac {\mathrm{d} [ \mathrm{CCl} _ {4} ]}{\mathrm{d} t} = k [ \mathrm{Cl} _ {2} ] ^ {1 / 2} I _ {\mathrm{a}} ^ {1 / 2}
$$

为解释此速率方程, 提出了如下的反应机理:

(1) $\mathrm{Cl}_2 + h\nu \xrightarrow{I_{\mathrm{a}}} 2\mathrm{Cl}\cdot$

(2) $\mathrm{Cl}\cdot +\mathrm{CHCl}_3\xrightarrow{k_2}\cdot \mathrm{CCl}_3 + \mathrm{HCl}$

(3) $\cdot \mathrm{CCl}_3 + \mathrm{Cl}_2\xrightarrow{k_3}\mathrm{CCl}_4 + \mathrm{Cl}\cdot$

(4) $2\cdot \mathrm{CCl}_3 + \mathrm{Cl}_2\xrightarrow{k_4} 2\mathrm{CCl}_4$

验证按此机理所导出的速率方程与实验所得的速率方程的一致性。

解 在反应 (3), (4) 中有 $\mathrm{CCl}_4$ 生成, 所以

$$
\frac {\mathrm{d} [ \mathrm{CCl} _ {4} ]}{\mathrm{d} t} = k _ {3} [ \cdot \mathrm{CCl} _ {3} ] [ \mathrm{Cl} _ {2} ] + 2 k _ {4} [ \cdot \mathrm{CCl} _ {3} ] ^ {2} [ \mathrm{Cl} _ {2} ]\tag{a}
$$

对反应过程中产生的自由基 $\cdot CCl_{3}$ 和 Cl·作稳态近似, 有

$$
\frac {\mathrm{d} [ \cdot \mathrm{CCl} _ {3} ]}{\mathrm{d} t} = k _ {2} [ \mathrm{Cl} \cdot ] [ \mathrm{CHCl} _ {3} ] - k _ {3} [ \cdot \mathrm{CCl} _ {3} ] [ \mathrm{Cl} _ {2} ] - 2 k _ {4} [ \cdot \mathrm{CCl} _ {3} ] ^ {2} [ \mathrm{Cl} _ {2} ] = 0
$$

$$
\frac {\mathrm{d} [ \mathrm{Cl} \cdot ]}{\mathrm{d} t} = 2 I _ {\mathrm{a}} - k _ {2} [ \mathrm{Cl} \cdot ] [ \mathrm{CHCl} _ {3} ] + k _ {3} [ \cdot \mathrm{CCl} _ {3} ] [ \mathrm{Cl} _ {2} ] = 0
$$

上两式相加得

$$
[ \cdot \mathrm{CCl} _ {3} ] = \left(\frac {2 I _ {\mathrm{a}}}{2 k _ {4} [ \mathrm{Cl} _ {2} ]}\right) ^ {1 / 2}\tag{b}
$$

将式 (b) 代入式 (a), 得

$$
\frac {\mathrm{d} [ \mathrm{CCl} _ {4} ]}{\mathrm{d} t} = k _ {3} \left(\frac {2 I _ {\mathrm{a}} [ \mathrm{Cl} _ {2} ]}{2 k _ {4}}\right) ^ {1 / 2} + 2 I _ {\mathrm{a}} = k I _ {\mathrm{a}} ^ {1 / 2} [ \mathrm{Cl} _ {2} ] ^ {1 / 2} + 2 I _ {\mathrm{a}}\tag{c}
$$

式中 $k = k_{3}\left(\frac{1}{k_{4}}\right)^{1 / 2}$ 。一般在光化学反应中，反应物的分子数总是比吸收的光子数多得多，所以式(c)中略去第二项，即得

$$
\frac {\mathrm{d} [ \mathrm{CCl} _ {4} ]}{\mathrm{d} t} = k I _ {\mathrm{a}} ^ {1 / 2} [ \mathrm{Cl} _ {2} ] ^ {1 / 2}
$$

## 光化学平衡和热化学平衡

设反应物 A, B 在吸收光能的条件下进行如下的反应:

$$
\mathrm{A} + \mathrm{B} \xrightarrow {h \nu} \mathrm{C} + \mathrm{D}
$$

若产物对光不敏感, 则它将按热反应又回到原态, 即

$$
\mathrm{A} + \mathrm{B} \underset {\mathrm{热反应}} {\overset {h \nu} {\rightleftharpoons}} \mathrm{C} + \mathrm{D}\tag{1}
$$

当正、逆反应的速率相等时, 达到稳态, 称为光稳定态 (photo stationary state)。在没有光的存在下, 上述反应也能达到平衡。

$$
\mathrm{A} + \mathrm{B} \xrightarrow [ \text {热反应} ]{\text {热反应}} \mathrm{C} + \mathrm{D}\tag{2}
$$

则这样的平衡就是热力学平衡。光稳定态和热力学平衡态是不同的，光稳定态的平衡常数（有时称为光化学平衡常数）与热力学平衡常数也是不同的。如果反应(1)已达平衡，当移去光源后，系统将重新建立如式(2)所示的平衡。

以葱的二聚为例:

$$
2 \mathrm{C} _ {1 4} \mathrm{H} _ {1 0} (\text { 葱 }) \underset {\text { 热 }} {\overset {\text { 光 }} {\rightleftharpoons}} \mathrm{C} _ {2 8} \mathrm{H} _ {2 0} (\text { 二聚体 })
$$

这个反应的机理其实并不如此简单, 但为了简化, 用上式来讨论, 并简写为

$$
2 \mathrm{A} \xrightarrow [ k _ {- 1} ]{I _ {\mathrm{a}}} \mathrm{A} _ {2}
$$

正向反应速率

$$
r _ {\mathrm{f}} = I _ {\mathrm{a}}
$$

逆向反应速率

$$
r _ {\mathrm{b}} = k _ {- 1} [ \mathrm{A} _ {2} ]
$$

平衡时, $r_{f}=r_{b}$ ,即

$$
I _ {\mathrm{a}} = k _ {- 1} [ \mathrm{A} _ {2} ]
$$

或

$$
[ \mathrm{A} _ {2} ] = I _ {\mathrm{a}} / k _ {- 1}
$$

平衡浓度 $\left[\mathrm{A}_{2}\right]$ 取决于吸收光的强度 $I_{\mathrm{a}}$ ，即与吸收光的强度 $I_{\mathrm{a}}$ 成正比。当 $I_{\mathrm{a}}$ 一定时，则双葱的浓度为一常数（即光化学平衡常数），而与反应物蒽的浓度无关。

也有些光化学反应, 其正、逆反应都对光敏感, 例如:

$$
2 \mathrm{SO} _ {3} \xrightarrow [ h \nu^ {\prime} ]{h \nu} 2 \mathrm{SO} _ {2} + \mathrm{O} _ {2}
$$

热力学计算表明, 在 900 K 和 101.325 kPa 下, 平衡时有 30% 的 $SO_{3}$ 分解。但在光化学反应的情况下, 在 318 K 时, 就有 35% 的 $SO_{3}$ 分解, 而且当光强度一定时, 在 323 \~ 1073 K 内其平衡常数都不会改变。

通常的化学反应, 温度每升高 10 K, 反应速率增加 2 \~ 4 倍。而温度对光化学反应速率的影响一般都不大, 这是由于光化学的初级过程与吸收光的强度有关, 而次级过程中又常涉及自由基反应, 这些反应的活化能不大, 所以温度对反应速率影响不大。但也有些光化学反应的温度系数很大, 有的甚至可为负值, 这是由于有次级过程存在, 在总的速率常数中可能包括中间步骤的速率常数或平衡常数。一种简单的情况: 若总的速率常数中包含某一步骤的速率常数 $k_{1}$ 和平衡常数 $K^{\ominus}$ , 并设有如下的关系:

$$
k = k _ {1} K ^ {\ominus}
$$

则

$$
\begin{array}{r l} \frac {\mathrm{d} \ln k}{\mathrm{d} T} & = \frac {\mathrm{d} \ln k _ {1}}{\mathrm{d} T} + \frac {\mathrm{d} \ln K ^ {\ominus}}{\mathrm{d} T} \\ & = \frac {E _ {\mathrm{a}}}{R T ^ {2}} + \frac {\Delta_ {\mathrm{r}} H _ {\mathrm{m}} ^ {\ominus}}{R T ^ {2}} \\ & = \frac {E _ {\mathrm{a}} + \Delta_ {\mathrm{r}} H _ {\mathrm{m}} ^ {\ominus}}{R T ^ {2}} \end{array}
$$

如果 $\Delta_{\mathrm{r}}H_{\mathrm{m}}^{\ominus}$ 为负值，且其绝对值大于 $E_{\mathrm{a}}$ ，则 $\frac{\mathrm{d}\ln k}{\mathrm{d}T} < 0$ ，即增加温度，反应速率反而变慢，苯的氯化反应就属于这一类型。

总之，光化学反应与热反应的主要区别可归纳为如下几点：

(1) 在热反应中, 反应分子靠频繁的互相碰撞而获得克服势垒所需要的活化

能, 而在光化学反应中, 分子靠吸收外来光能后激发而克服势垒。

(2) 在定温定压下, 自发进行的热反应必是 $(\Delta_{\mathrm{r}}G)_{T,p} \leqslant 0$ 的反应, 但光化学反应可以是 $(\Delta_{\mathrm{r}}G)_{T,p} \leqslant 0$ 的反应, 也可以是 $(\Delta_{\mathrm{r}}G)_{T,p} > 0$ 的反应。例如, $\mathrm{CO}_{2}(\mathrm{~g})$ 及 $H_{2}O$ 在阳光的照射下, 以叶绿素作催化剂而合成糖类的反应就是 $(\Delta_{\mathrm{r}}G)_{T,p} > 0$ 的反应:

$$
6 \mathrm{CO} _ {2} (\mathrm{g}) + 6 \mathrm{H} _ {2} \mathrm{O} \xrightarrow [ \mathrm{阳光} ]{\mathrm{叶绿素}} \mathrm{C} _ {6} \mathrm{H} _ {1 2} \mathrm{O} _ {6} + 6 \mathrm{O} _ {2} (\mathrm{g})
$$

(3) 热反应的反应速率受温度的影响比较明显。在光化学反应中, 分子吸收光子而激发的步骤, 其速率与温度无关, 而受激发后的反应步骤, 又常是活化能很小的步骤, 故一般来说, 光化学反应的温度系数较小。

(4) 在对峙反应中, 在正、逆反应中只要有一个是光化学反应, 则当正、逆反应的速率相等时就建立了“光稳定态”(也称为光化学平衡态)。同一对峙反应, 若既可按热反应方式进行, 又可按光化学反应进行, 则热反应的平衡常数及平衡组成与光化学反应的“平衡常数”及光稳定态的组成并不相同。对于光化学反应, 并不存在 $\Delta_{\mathrm{r}}G_{\mathrm{m}}^{\ominus} = -RT\ln K^{\ominus}$ 的关系。

## 感光反应、化学发光

有些物质不能直接吸收某种波长的光而进行光化学反应, 即对光不敏感。但如果在系统中加入另外一种物质, 它能吸收这样的辐射, 然后把光能传递给反应物, 使反应物发生作用, 而本身在反应的前后并不发生变化, 则这样的外加物质就叫作感光剂 (或光敏剂, photosensitizer), 相应的反应就是感光反应 (或光敏反应, photosensitized reaction)。

例如, 用波长为 $253.7 \mathrm{~nm}$ 的紫外光照射氢气时, 氢气并不解离。该紫外光 $1 \mathrm{~mol}$ 光子的能量为

$$
\begin{array}{r l} E _ {\mathrm{m}} & = \frac {L h c}{\lambda} \\ & = \frac {6 . 0 2 2 \times 1 0 ^ {2 3} \mathrm{mol} ^ {- 1} \times 6 . 6 2 6 \times 1 0 ^ {- 3 4} \mathrm{J} \cdot \mathrm{s} \times 3 . 0 \times 1 0 ^ {8} \mathrm{m} \cdot \mathrm{s} ^ {- 1}}{2 5 3 . 7 \times 1 0 ^ {- 9} \mathrm{m}} \\ & = 4 7 2 \mathrm{kJ} \cdot \mathrm{mol} ^ {- 1} \end{array}
$$

而 $1 \, \text{mol H}_{2}(\text{g})$ 分子的解离能为 $436 \, kJ \cdot mol^{-1}$ ，照理反应应该可以发生，但实际上 $\mathrm{H}_{2}(\mathrm{~g})$ 并不解离。在 $\mathrm{H}_{2}(\mathrm{~g})$ 中混入少量汞蒸气后， $\mathrm{Hg}(\mathrm{g})$ 受光活化成为 $\mathrm{Hg}^{*}(\mathrm{g})$ ，它能使氢分子立刻分解，则汞蒸气就是该反应的感光剂。上述过程可定性地表示为

$$
\begin{array}{r l} & \mathrm {Hg(g) + h\nu \longrightarrow Hg^ {*} (g)} \\ & \mathrm {Hg^ {*} (g) + H_ {2} (g) \longrightarrow Hg(g)+ H_ {2} ^ {*} (g)} \\ & \mathrm {H_ {2} ^ {*} (g) \longrightarrow 2H\cdot} \end{array}
$$

另一个常见的例子是植物的光合作用 (photosynthesis)。 $CO_{2}(g)$ 及 $H_{2}O$ 都不能直接吸收阳光 ( $\lambda = 380 \sim 760 nm$ )，而叶绿素却能吸收阳光并将 $CO_{2}(g)$ 和 $H_{2}O$ 转化为葡萄糖：

$$
6 \mathrm{CO} _ {2} (\mathrm{g}) + 6 \mathrm{H} _ {2} \mathrm{O} \xrightarrow [ h \nu ]{\mathrm{叶绿素}} \mathrm{C} _ {6} \mathrm{H} _ {1 2} \mathrm{O} _ {6} + 6 \mathrm{O} _ {2} (\mathrm{g})
$$

因此，叶绿素就是植物光合作用的感光剂。

卤化银能吸收自然光里的短波辐射 (绿光、紫光、紫外光) 而发生分解, 如

$$
\mathrm{AgBr} \xrightarrow {h \nu} \mathrm{Ag} + \mathrm{Br} \cdot
$$

这个反应是照相技术的基础。但卤化银却不受长波辐射 (红光、荧光) 的影响, 故冲洗相片的暗房里可用红灯照射。如果在 AgBr 中加入某种染料, 则它在红光下也会分解, 这种染料就是感光剂。

二氧铀草酸盐光量计, 可以用来测定紫外光的强度, 即是根据上面的原理设计的。仪器的主要部分含有一定浓度的 $\mathrm{UO}_{2} \mathrm{SO}_{4}$ 和草酸溶液, $\mathrm{UO}_{2}^{2+}$ 对紫外光敏感, 它吸收紫外光成为激发态, 并把能量传递给草酸, 使草酸分解, 从草酸的分解量可以测知紫外光的强度。

选择对不同波长的光所发生的感光反应, 可以设计测定不同波长光的强度的仪器, 这种设备称为化学光量计。

化学发光 (chemiluminescence) 是化学反应过程中发出的光, 可看成光化学反应的逆过程。光化学反应是分子吸收光子变为激发态后再进行的反应, 而化学发光则由于在化学反应过程中产生了激发态分子, 这些激发态分子回到基态的同时放出了辐射。由于产生化学发光的温度一般在 800 K 以下, 故有时又称为化学冷光 (cold light)。例如, CO(g) 燃烧时能形成激发态的 $\mathrm{CO}_{2}^{*}(g)$ 和 $\mathrm{O}_{2}^{*}(g)$ , 这些激发态分子能放出光:

$$
\begin{array}{r l} & \mathrm {O_ {2} ^ {*}} \longrightarrow \mathrm {O_ {2}} + h \nu \\ & \mathrm {CO_ {2} ^ {*}} \longrightarrow \mathrm {CO_ {2}} + h \nu^ {\prime} \end{array}
$$

其他如细菌对朽木的氧化、萤火虫的发光及黄磷的发光等, 所发出的光都是可见的 (当然也有些只是在夜间可见的)。

有些化学发光是肉眼不可见的, 如红外化学发光。例如, 热反应:

$$
\mathrm{H} + \mathrm{X} _ {2} \longrightarrow \mathrm{X} + \mathrm{HX} ^ {*}
$$

激发态 HX\* 可以放出红外辐射, 在化学反应动态学中, 人们通过研究这种红外辐射, 可以了解能量在初生态产物中的分配。

## \*12.8 化学激光简介

激光的英文名称 laser 是英文 “light amplification by stimulated emission of radiation” 的缩写, 意思是 “由受激发射辐射而强化的光”。激光是一种单色、亮度高、相干性好、方向性好的相干光束。

受激辐射、受激吸收及自动辐射等是电磁波与物质相互作用的三种基本现象, 激光的产生即由此而来。

## 受激辐射、受激吸收和自动辐射

受激辐射、受激吸收和自动辐射三种情况的对比见图 12.19。每一个能级上的粒子是很多的，图中只给出了一个有变动的粒子（用“○”表示）。

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_200-399_images/ebf39b74a662ece17c36dccf9a416ee04483fb96e5abcf726edc08db6cc3b62c.jpg)  
图 12.19 受激辐射、受激吸收和自动辐射三种情况的对比

处于激发态的粒子其能量较高, 会自发从高能级跃迁到低能级, 而放出能量为 $E_{1} - E_{0} = h\nu$ 的辐射。在跃迁过程中, 每一个原子或分子都可以当作一个独立发射光的光源, 因而发射的光指向各个方向, 是无序的, 即具有不同的偏振方向, 在光学上称这种光具有非相干性 (noncoherence)。此过程称为自动辐射, 图 12.19(b) 就属于这种情况。

图 12.19(a) 是处于低能级 (能量为 $E_{0}$ ) 的原子 (或分子) 吸收了外来的能量 $h\nu$ ，而从低能级跃迁到高能级的过程，称为受激吸收。一旦撤去激励光源，则受激吸收过程立刻停止。

图 12.19(c) 则是一种较特殊的过程, 它首先要求处于高能级的粒子数要多于低能态的粒子数 (即粒子数分布呈反转状态)。受激辐射是指处于较高能级的激发态分子 (或原子) 受光的激励而回到低能级的过程; 与此同时, 发射出与激励光源同频率、同位相、同方向、同偏振的辐射。受激辐射出的波的能量比入射波的能量增加了一倍 (即产生了光的倍增效应), 这就是激光的来源。

## 粒子数反转

在通常的情况下, 将适当能量的光子射入含有某物质的容器中, 不能发生上述第三种情况即受激辐射, 而只能发生受激吸收。这是因为在通常的热平衡状态下, 在能级 $E_0$ 和 $E_1$ 上的粒子数 $N_0$ 和 $N_1$ 服从 Boltzmann 分布定律, 即

$$
\frac {N _ {1}}{N _ {0}} = \exp \left(- \frac {E _ {1} - E _ {0}}{k T}\right)
$$

式中 $E_{1} > E_{0}$ 。若两个能级的能量差（或能量间隙）为 kT （在室温时，kT 值约为 0.025 eV），高能级的粒子数约为低能级粒子数的 1/e（或 0.37）。而对发生可见光子的能级转变来说，激发态和基态之间的能量间隙约为 1.25 eV（这个数值与 0.025 eV 相差甚远，即在受激辐射过程中，高能级的能量远远高于第一激发态的能量 $E_{1}$ ）。所以在通常的平衡状况下，在室温时处于该激发态的粒子数将是微不足道的。因此，任何可见光的光子很可能被吸收而不引起受激辐射。

要使受激辐射占优势, 必须增加激发态的粒子数, 并使之多于低能级的粒子数, 这种情况就称为粒子数反转 (population inversion)。但在热平衡下, Boltzmann 分布公式表明, 对于二能级系统, 即使温度无限高, 也只能使两个能级的粒子数相等。在常温下, 要实现粒子数反转只能在非平衡状况下进行, 此时 Boltzmann 分布定律已不适用, 代之而起支配作用的是非平衡态即不可逆过程热力学的规律。

激光器是一个远离平衡的开放系统, 它与外界不断交换能量, 从外界输入足够强的光波 (或适当的电能), 使其中的粒子从低能级激发到高能级, 或直接利用化学反应使产物处于激发态, 以实现粒子数反转, 这一过程统称为泵浦 (pumping, 也称为抽运或抽送)。

## 三能级系统和四能级系统的粒子数反转

任何物质的能级结构都极为复杂, 但与激光器运转过程直接有关的能级结构只有两种, 即三能级系统和四能级系统 (如上所述, 对二能级系统不管用什么手段, 只能发生受激吸收而不能发生受激辐射)。

在三能级系统中 [如图 12.20(a)], 粒子通过适当的方法 (泵浦), 从基态 (能级 0) 提升到能级 2, 如果该系统有这样的性质, 即处在能级 2 的粒子是很不稳定的, 它很快跃迁 (或蜕变) 到能级 1, 这样就可能在能级 1 和 0 之间出现粒子数反转。

在图 12.20(b) 所示的四能级系统中, 在外界的激励下, 基态 (能级 0) 上有大量的粒子被泵浦到能级 3 上。能级 3 上的粒子迅速地跃迁到能级 2 上, 能级 2 是亚稳态的, 寿命较长。而能级 1 的寿命较短, 到能级 1 上的粒子很快回到基态。于是在能级 2 与能级 1 之间非常容易实现粒子数反转。

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_200-399_images/69346183f5d8d65b1d0b2d6b490335dc6124345ee973636ca295de384181daa8.jpg)

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_200-399_images/6073fe13667a544dd7ba2ac646fefe152faff95d0dff55e54cf6e184bac9cc95.jpg)  
图 12.20 三能级系统和四能级系统

## 化学激光

化学激光 (chemical laser) 就是通过化学反应, 直接产生非 Boltzmann 分布的激发态工作粒子 (原子、分子、自由基等), 构成粒子数反转从而得到的激光。或者说, 化学激光是指激活介质的粒子数反转是通过化学反应的热效应, 把能量转变为粒子的振动能和转动能而实现的激光系统。产生化学激光必须具备的条件是

(1) 在化学反应中一定要释放出能量, 这是化学激光的能源;

(2) 化学反应所释放的能量要能转化为产物分子的热力学能, 使其形成激发态粒子;

(3) 要求化学反应达到特定能级的反应速率快 (即泵浦速率快), 使生成的激发态粒子不致在发生激光之前由于自发辐射衰减或分子间碰撞传能而被消耗, 这样才能保证达到上、下能级粒子数的反转 (即粒子能在高能级上发生积累);

(4) 要求激发态粒子自动辐射的寿命极短, 有足够的跃迁概率。

第一台化学激光器是氯化氢化学激光器, 是在 1965 年由美国加州大学伯克利分校的 J. Kasper (当时他是研究生) 与他的导师 G. Pimentel 共同研制的, 他们利用光引发 $\mathrm{H}_{2}(\mathrm{~g})$ 与 $\mathrm{Cl}_{2}(\mathrm{~g})$ 的混合气体爆炸而获得激光, 其反应机理如下:

(1) $Cl_{2} + h\nu \longrightarrow 2Cl\cdot$ 光解引发链反应

(2) $\mathrm{Cl}\cdot +\mathrm{H}_{2}\longrightarrow \mathrm{HCl}(v = 0) + \mathrm{H}\cdot$

$$
E _ {\mathrm{a}} = 2 3 \mathrm{kJ} \cdot \mathrm{mol} ^ {- 1}, \Delta_ {\mathrm{r}} H _ {\mathrm{m}} = 4. 1 8 \mathrm{kJ} \cdot \mathrm{mol} ^ {- 1}
$$

(3) $\mathrm{H}\cdot +\mathrm{Cl}_2\longrightarrow \mathrm{HCl}^* (v = 1\sim 6) + \mathrm{Cl}\cdot$

$$
E _ {\mathrm{a}} = 7. 5 \mathrm{kJ} \cdot \mathrm{mol} ^ {- 1}, \Delta_ {\mathrm{r}} H _ {\mathrm{m}} = - 1 8 8. 5 \mathrm{kJ} \cdot \mathrm{mol} ^ {- 1}
$$

(4) $\mathrm{HCl}^{*}(v=1\sim6)\longrightarrow\mathrm{HCl}(v=0)+h\nu(\lambda=3.7\sim3.8\mu\mathrm{m})$

由于反应 (2) 的活化能较高而又不是放热反应, 所以相对而言反应速率偏慢, 产生的 HCl 粒子都处于振动的基态 (振动量子数 v = 0)。因此, 这一步不可能产生激光。而反应 (3) 的活化能小, 而又放出大量的热, 反应速率极快, 成为产生激光的泵浦反应, 使能级上粒子数反转。受激粒子中的振动量子数 v 值在 1 \~ 6, 产生的激光波长为 $\lambda = 3.7 \sim 3.8 \mu m$ 。

这是第一台化学激光器, 也是第一台运转在振动量子数由 2—1 和由 1—0 的化学激光器, 这样的反应机理对以后其他化学激光的研制产生了极大的影响和指导作用。但由于反应 (2) 中产生的处于基态的 HCl 会将 (3) 中产生的激发态的 HCl\* “稀释”, 所以希望在反应中有更多的 H 原子。但 $\mathrm{H}_{2}$ 的解离能大, 至今无很好的办法来解决。另外, 该激光器在反应气 $\mathrm{H}_{2}(\mathrm{~g})$ 与 $\mathrm{Cl}_{2}(\mathrm{~g})$ 的预混时, 见光容易发生爆炸。所以, 后来这类激光器逐渐被 HF/DF 化学激光器代替。

HF/DF 化学激光器是将分别注入的氧化剂和燃料, 经过超声速混合喷管进入光腔, 与反应物一旦混合就产生一个快速强放能的泵浦反应, 产生处于振动激发态的 $\mathrm{HF}^{*}(v)$ ; 当粒子形成部分反转时, 就会发射出波长在 $2.7 \sim 3.1 \mu \mathrm{m}$ 的激光。

在 20 世纪 70 年代, 激光技术已开始用于工业加工, 当时主要用 $\mathrm{CO}_{2}(\mathrm{~g})$ 激光器和钕玻璃固体激光器, 它们的能源都是电能, 操作比较简单, 而化学激光器的操作相对比较复杂。但当需要高功率激光时, 由于化学激光器的放大性能好, 可放大至几十万瓦甚至百万瓦, 可以用来切割钢板、铝板等, 不但切割速度快, 而且质量好, 所以化学激光器就优于电能激光器。另外, 氧碘化学激光的波长为 $1.315 \mu m$ , 很适合用光纤传输, 便于远距离操作, 如对核反应堆的检修和拆除等; 再加上氧碘化学激光器的波长短, 光束发射角仅是 $\mathrm{CO}_{2}(\mathrm{~g})$ 激光器的 1/8, 所以可以聚焦成很小的光斑, 提高加工精度。

化学激光是利用化学反应释放的能量而产生的激光, 所以不受电源的限制, 可以制备成由飞机运载的机载激光器, 或制备成由卫星运载的星载激光器, 以及其他高功率的车载、舰载激光武器等，所以化学激光器在军事工业上备受重视。

激光作为一种特殊的光源, 其用途非常广泛。激光光源具有单色性好、亮度高、方向性强和相干性高等特点, 是用来研究光与物质的相互作用, 从而辨认物质及其所在系统的结构、组成、状态及其变化的较理想的光源。激光的出现, 使原有的光谱技术在灵敏度和分辨率方面得到很大的提高。激光光谱学已经成为和物理学、化学、生物学及材料科学等密切相关的新领域。

激光可用于同位素的分离。人们早已知道可以利用单色光对准一种同位素的谱线位置，将它光解或激发至激发态进行反应，而其余的同位素不被光解或激发而留存于原料之中，达到同位素分离的目的。用激光的方法已经成功地分离了氢、硼、氮、碳、氯、硫、钠、锂、溴、钙、钡、铁等的同位素，难度最大的 $^{235}$ U 和 $^{238}$ U 的分离也获得了成功。

在常温常压下不能进行的反应, 通过激光的照射可诱发其发生反应, 这开拓了激光诱导化学反应的新领域。例如, 激光法生产氯乙烯:

$$
\begin{array}{r l} & \mathrm {C_ {2} H_ {4} Cl_ {2}} \xrightarrow {h \nu} \cdot \mathrm {C_ {2} H_ {4} Cl} + \mathrm{Cl} \cdot \\ & \mathrm {C_ {2} H_ {4} Cl_ {2}} + \mathrm{Cl} \cdot \longrightarrow \cdot \mathrm {C_ {2} H_ {3} Cl_ {2}} + \mathrm{HCl} \\ & \cdot \mathrm {C_ {2} H_ {3} Cl_ {2}} \xrightarrow {\mathrm{M}} \mathrm {C_ {2} H_ {3} Cl} + \mathrm{Cl} \cdot \end{array}
$$

又如, 激光诱发 $BCl_{3} + H_{2}S$ 的反应, 在常温常压下二者不发生反应, 但在二氧化碳激光辐射之下, $BCl_{3}$ 分子的 $\nu_{3}$ 振动频率与 10.55 $\mu m$ 红外光子共振, 使 B—Cl 键被激发, 发生下述反应过程:

$$
\begin{array}{r l} & \mathrm {BCl_ {3}} + \mathrm {H_ {2} S} \xrightarrow {h \nu} \mathrm {BCl_ {3} ^ {*}} + \mathrm {H_ {2} S} \longrightarrow \mathrm {BCl_ {2} SH} + \mathrm{HCl} \\ & 3 \mathrm {BCl_ {2} SH} \longrightarrow (\mathrm{BClS}) _ {3} + 3 \mathrm{HCl} \\ & (\mathrm{BClS}) _ {3} \longrightarrow \mathrm {B_ {2} S_ {3}} + \mathrm {BCl_ {3}} \end{array}
$$

