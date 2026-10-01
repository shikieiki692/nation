---
title: "傅献彩《物理化学》（第六版下册）-第十一章 化学动力学基础(二)：典型复杂反应与温度效应"
type: 外部教材切片
source_book: "物理化学（第六版下册）-傅献彩"
syllabus_codes: [基础-12, 决赛-07]
created: 2026-09-25
updated: 2026-09-25
status: 已填充
---

## 11.5 几种典型的复杂反应

前面讨论的都是比较简单的反应。如果一个化学反应是由两个以上的基元反应以各种方式相互联系起来的，则这种反应就是复杂反应。一个总包反应是由许多基元反应组合起来的。原则上任一基元反应的速率常数仅取决于该反应的本性与温度，不受其他组分的影响，它所遵从的动力学规律也不因其他基元反应的存在而有所不同，速率常数不变。但由于其他组分的同时存在，影响了组分的浓度，所以反应的速率会受到影响。

以下只讨论几种典型的复杂反应——即对峙反应、平行反应和连续反应，这些都是基元反应的最简单的组合。链反应也是复杂反应，由于它具有特殊的规律，留待以后讨论。

对峙反应

在正、反两个方向上都能进行的反应秒为对峙反应 (opposing reaction), 亦称为可逆反应。例如:

$$
\begin{array}{r l} & \mathrm{A} \xrightarrow [ k _ {- 1} ]{k _ {1}} \mathrm{B} \\ & \mathrm{A} \xrightarrow [ k _ {- 2} ]{k _ {1}} \mathrm{B} + \mathrm{C} \\ & \mathrm{A} + \mathrm{B} \xrightarrow [ k _ {- 2} ]{k _ {2}} \mathrm{C} + \mathrm{D} \end{array}
$$

等等。现以最简单的 1-1 级对峙反应（即正、反两个方向的反应均为一级的反应）为例，讨论对峙反应的特点和处理方法。

$$
\begin{array}{l l l}&\mathrm{A}&\underset {k _ {- 1}} {\overset {k _ {1}} {\rightleftharpoons}} \mathrm{B}\\t = 0&a&0\\t = t&a - x&x\\t = t _ {\mathrm{e}}&a - x _ {\mathrm{e}}&x _ {\mathrm{e}}\end{array}
$$

下标“e”表示平衡。

净的右向反应速率取决于正向及逆向反应速率的总结果, 即

$$
r = \frac {\mathrm{d} x}{\mathrm{d} t} = r _ {\text {正}} - r _ {\text {逆}} = k _ {1} (a - x) - k _ {- 1} x\tag{11.42}
$$

根据式(11.42)，无法同时解出 $k_{1}$ 和 $k_{-1}$ 的值，还需一个联系 $k_{1}$ 和 $k_{-1}$ 的公式，这可以从平衡条件得到。当达到平衡时， $r = \frac{\mathrm{d}x}{\mathrm{d}t} = 0$ ，所以

$$
\begin{array}{l} k _ {1} (a - x _ {\mathrm{e}}) = k _ {- 1} x _ {\mathrm{e}} \\ \frac {x _ {\mathrm{e}}}{a - x _ {\mathrm{e}}} = \frac {k _ {1}}{k _ {- 1}} = K \end{array}\tag{11.43}
$$

或

$$
k _ {- 1} = k _ {1} \frac {a - x _ {\mathrm{e}}}{x _ {\mathrm{e}}}\tag{11.44}
$$

K 就是平衡常数。将式 (11.44) 代入式 (11.42)，得

$$
\frac {\mathrm{d} x}{\mathrm{d} t} = k _ {1} (a - x) - k _ {1} \frac {(a - x _ {\mathrm{e}})}{x _ {\mathrm{e}}} \cdot x = \frac {k _ {1} a (x _ {\mathrm{e}} - x)}{x _ {\mathrm{e}}}\tag{11.45}
$$

将式 $(11.45)$ 作定积分, 得

$$
k _ {1} = \frac {x _ {\mathrm{e}}}{t a} \ln \frac {x _ {\mathrm{e}}}{x _ {\mathrm{e}} - x}\tag{11.46}
$$

求出 $k_{1}$ 后再代入式 (11.44)，即可求出 $k_{-1}$ ，或从式 (11.43) 已知平衡常数 K 而求出 $k_{-1}$ 。

对于 2-2 级对峙反应 (或其他对峙反应), 处理的方法基本相同, 即

$$
\begin{array}{c c c c c} & \mathrm{A} + & \mathrm{B} & \frac {k _ {2}}{\overline {{k _ {- 2}}}} & \mathrm{C} + \mathrm{D} \\ t = 0 & a & b & 0 & 0 \\ t = t & a - x & b - x & x & x \\ t = t _ {\mathrm{e}} & a - x _ {\mathrm{e}} & b - x _ {\mathrm{e}} & x _ {\mathrm{e}} & x _ {\mathrm{e}} \end{array}
$$

设 $a = b$ ，则

## 11.5 几种典型的复杂反应

$$
r = \frac {\mathrm{d} x}{\mathrm{d} t} = k _ {2} (a - x) ^ {2} - k _ {- 2} x ^ {2}\tag{11.47}
$$

平衡时

$$
\begin{array}{r l} & k _ {2} (a - x _ {\mathrm{e}}) ^ {2} = k _ {- 2} x _ {\mathrm{e}} ^ {2} \\ & \frac {x _ {\mathrm{e}} ^ {2}}{(a - x _ {\mathrm{e}}) ^ {2}} = \frac {k _ {2}}{k _ {- 2}} = K \end{array}\tag{11.48}
$$

代入式 (11.47), 积分

$$
\int_ {0} ^ {x} \frac {\mathrm{d} x}{(a - x) ^ {2} - \frac {1}{K} x ^ {2}} = \int_ {0} ^ {t} k _ {2} \mathrm{d} t
$$

得

$$
k _ {2} t = \frac {\sqrt {K}}{2 a} \ln \frac {a + (\beta - 1) x}{a - (\beta + 1) x}\tag{11.49}
$$

式中

$$
\beta^ {2} = \frac {1}{K}
$$

## 例11.7

碘代甲烷 $CH_{3}I$ 和二甲基-对-甲苯胺（用 N-R 表示）在硝基苯溶液中形成季铵盐的反应是 2-2 级对峙反应：

$$
\mathrm{CH} _ {3} \mathrm{I} + \mathrm{N} - \mathrm{R} \underset {k _ {- 2}} {\overset {k _ {2}} {\rightleftharpoons}} \mathrm{CH} _ {3} - \stackrel {+} {\mathrm{N}} - \mathrm{R} + \mathrm{I}
$$

而反应物的起始浓度均为 $0.05 \, mol \cdot dm^{-3}$ ，实验数据如下：

<table><tr><td>反应时间 t/s</td><td>10.2</td><td>26.5</td><td>36.0</td><td>78.0</td></tr><tr><td>N-R 作用的分数</td><td>0.175</td><td>0.343</td><td>0.412</td><td>0.523</td></tr></table>

已知在实验温度下, 平衡常数 K = 1.43, 求速率常数 $k_{2}$ 和 $k_{-2}$ 。

解 已知 $a = 0.05 \mathrm{~mol} \cdot \mathrm{dm}^{-3}$ , $\beta = \frac{1}{\sqrt{K}} = \frac{1}{\sqrt{1.43}} = 0.836$ , 代入式 (11.49), 有

$$
k _ {2} = \frac {1}{t} \times \frac {\sqrt {1 . 4 3}}{2 \times 0 . 0 5} \ln \frac {0 . 0 5 \mathrm{mol} \cdot \mathrm{dm} ^ {- 3} - 0 . 1 6 4 x}{0 . 0 5 \mathrm{mol} \cdot \mathrm{dm} ^ {- 3} - 1 . 8 3 6 x}
$$

将对应的实验数据 t 和 $x(=0.05\ \text{mol}\cdot\text{dm}^{-3}\times y)$ 代入，即可求出 $k_{2}$ 值。不同反应时间对应的 $k_{2}$ 值分别为

<table><tr><td>反应时间 t/s</td><td>10.2</td><td>26.5</td><td>36.0</td><td>78.0</td></tr><tr><td> $k_{2}/(mol^{-1} \cdot dm^{3} \cdot s^{-1})$ </td><td>0.420</td><td>0.422</td><td>0.446</td><td>0.481</td></tr></table>

则

$$
\overline {{{{k}}}} _ {2} = 0. 4 4 2 \mathrm{mol} ^ {- 1} \cdot \mathrm{dm} ^ {3} \cdot \mathrm{s} ^ {- 1}
$$

所以

$$
\overline {{{{k}}}} _ {- 2} = \overline {{{{k}}}} _ {2} / K = 0. 3 0 9 \mathrm{mol} ^ {- 1} \cdot \mathrm{dm} ^ {3} \cdot \mathrm{s} ^ {- 1}
$$

## 平行反应

反应物同时平行地进行两个或两个以上不同反应的反应称为平行反应 (parallel reaction), 这种情况在有机反应中较多。通常将生成期望产物的反应称为主反应, 其余为副反应。组成平行反应的几个反应的级数可以相同, 也可以不同, 前者的数学处理较为简单。

先考虑最简单的情况, 即两个反应都是一级反应的平行反应:

$$
\mathrm{A} \xrightarrow {k _ {1}} \begin{array}{c} \text { B } \\ k _ {2} \end{array} \xrightarrow {} \mathrm{C}
$$

$$
\begin{array}{c c c c} & \text {[A]} & \text {[B]} & \text {[C]} \\ t = 0 & a & 0 & 0 \\ t = t & a - x _ {1} - x _ {2} & x _ {1} & x _ {2} \end{array}
$$

令 $x = x_{1} + x_{2}$ 。因为平行反应的总速率是两个平行反应的速率之和，所以

$$
\begin{array}{r l} & r = r _ {1} + r _ {2} = \frac {\mathrm{d} x}{\mathrm{d} t} = \frac {\mathrm{d} x _ {1}}{\mathrm{d} t} + \frac {\mathrm{d} x _ {2}}{\mathrm{d} t} = k _ {1} (a - x) + k _ {2} (a - x) \\ & = (k _ {1} + k _ {2}) (a - x) \end{array}\tag{11.50}
$$

对式 $(11.50)$ 进行定积分, 有

$$
\int_ {0} ^ {x} \frac {\mathrm{d} x}{a - x} = (k _ {1} + k _ {2}) \int_ {0} ^ {t} \mathrm{d} t
$$

得

$$
\ln \frac {a}{a - x} = (k _ {1} + k _ {2}) t\tag{11.51}
$$

由此可见，两个平行的一级反应的微分式和积分式，与简单一级反应的基本相同，仅是速率常数是两个平行反应的速率常数的加和。

两个反应都是二级反应的平行反应的例子有氯苯的再氯化, 得到的二氯苯产物有对位和邻位两种。设反应开始时 $C_{6}H_{5}Cl$ 和 $Cl_{2}$ 的浓度分别为 a 和 b, 且无产物存在, 反应到某时刻 t 时, 产物的浓度分别为 $x_{1}$ 和 $x_{2}$ , 则

$$
\begin{array}{c c}\mathrm{C} _ {6} \mathrm{H} _ {5} \mathrm{Cl}&+ \quad \mathrm{Cl} _ {2}\\a - x _ {1} - x _ {2}&b - x _ {1} - x _ {2}\end{array}\xrightarrow {\boxed {k _ {1}} \rightarrow}\begin{array}{c c}\text {对} - \mathrm{C} _ {6} \mathrm{H} _ {4} \mathrm{Cl} _ {2} + \mathrm{HCl}&x _ {1}\\k _ {2} \rightarrow&\text {邻} - \mathrm{C} _ {6} \mathrm{H} _ {4} \mathrm{Cl} _ {2} + \mathrm{HCl}&x _ {2}\end{array}
$$

$$
r _ {1} = \frac {\mathrm{d} x _ {1}}{\mathrm{d} t} = k _ {1} (a - x _ {1} - x _ {2}) (b - x _ {1} - x _ {2})\tag{11.52a}
$$

$$
r _ {2} = \frac {\mathrm{d} x _ {2}}{\mathrm{d} t} = k _ {2} (a - x _ {1} - x _ {2}) (b - x _ {1} - x _ {2})\tag{11.52b}
$$

由于两个反应同时进行, 反应的速率等于两个反应的速率之和, 所以

$$
r = r _ {1} + r _ {2} = (k _ {1} + k _ {2}) (a - x _ {1} - x _ {2}) (b - x _ {1} - x _ {2})
$$

令 $x = x_{1} + x_{2}$ ，则

$$
r = \frac {\mathrm{d} x}{\mathrm{d} t} = (k _ {1} + k _ {2}) (a - x) (b - x)
$$

移项作定积分, 得

$$
\frac {1}{a - b} \ln \frac {b (a - x)}{a (b - x)} = \left(k _ {1} + k _ {2}\right) t\tag{11.53}
$$

若将式 (11.52a) 与式 (11.52b) 相除, 则得

$$
\frac {\mathrm{d} x _ {1} / \mathrm{d} t}{\mathrm{d} x _ {2} / \mathrm{d} t} = \frac {k _ {1}}{k _ {2}}
$$

由于这两个反应是同时开始而分别进行的, 开始时均无产物存在, 因此两个反应的速率之比应等于产物的数量之比, 即

$$
\frac {\mathrm{d} x _ {1} / \mathrm{d} t}{\mathrm{d} x _ {2} / \mathrm{d} t} = \frac {x _ {1}}{x _ {2}}
$$

所以

$$
\frac {k _ {1}}{k _ {2}} = \frac {x _ {1}}{x _ {2}}\tag{11.54}
$$

只要知道起始浓度 $a$ 和 $b$ , 再知道反应经历的时间 $t$ , 产物的量 $x_{1}$ 和 $x_{2}$ , 则从式 (11.53) 可求得 $(k_{1} + k_{2})$ , 从式 (11.54) 可求得 $k_{1} / k_{2}$ , 将所得结果联立求解, 就能求得 $k_{1}$ 和 $k_{2}$ 。如果所求得的 $k_{1}$ 和 $k_{2}$ 相差很大, 则速率大的一般称为主反

应，而其余的则称为副反应。

从式 (11.54) 可以看出, 当温度一定时, $k_{1} / k_{2}$ 是一个定值, 也就是说产物中对位二氯苯和邻位二氯苯的比值是一定的。如果希望多获得某一种产品, 就要设法改变 $k_{1} / k_{2}$ 值。一种方法是选择适当的催化剂, 提高催化剂对某一反应的选择性以改变 $k_{1} / k_{2}$ 值。另一种方法是通过改变温度来改变 $k_{1} / k_{2}$ 值。例如甲苯的氯化, 可以直接在苯环上发生取代, 也可以在甲基上发生取代, 这两个反应可平行进行。实验表明, 在低温下 $(300 \sim 320 \mathrm{~K})$ 使用 $\mathrm{FeCl}_3$ 作催化剂时取代反应主要发生在苯环上; 而在较高温下 $(390 \sim 400 \mathrm{~K})$ 用光激发, 则取代反应主要发生在甲基上。

如果两个平行反应的级数不相同, 情况就复杂一些。例如, 两个平行反应的速率方程为

$$
r _ {1} = k c _ {\mathrm{A}} c _ {\mathrm{B}} \qquad r _ {2} = k ^ {\prime} c _ {\mathrm{B}} ^ {2}
$$

则

$$
\frac {r _ {1}}{r _ {2}} = \frac {k}{k ^ {\prime}} \cdot \frac {c _ {\mathrm{A}}}{c _ {\mathrm{B}}}
$$

如果反应 1 的产物是所需要的, 根据上式, 为了得到更多的反应 1 的产物, 并尽量抑制反应 2 的进行, 显然 $c_{A}$ 应控制得高些, $c_{B}$ 则以较低为宜。

连续反应

有很多化学反应是经过连续几步才完成的, 前一步的产物就是下一步的反应物, 如此依次连续进行, 这种反应就称为连续反应 (consecutive reaction), 也称为连串反应。例如苯的氯化, 产物氯苯能进一步与氯作用生成二氯苯、三氯苯等。

又如苯加乙烯制乙苯，在乙苯生成之后，还会在邻位上发生烷基化反应。

$$
\begin{array}{r l} & \mathrm{C} _ {6} \mathrm{H} _ {5} + \mathrm{CH} _ {2} = \mathrm{CH} _ {2} \xrightarrow {k _ {1}} \mathrm{C} _ {6} \mathrm{H} _ {5} \\ & \mathrm{C} _ {6} \mathrm{H} _ {5} + \mathrm{CH} _ {2} = \mathrm{CH} _ {2} \xrightarrow {k _ {2}} \mathrm{C} _ {6} \mathrm{H} _ {5} \end{array}
$$

开始时第二步的速率比较慢, 但当苯转化达 $70\% \sim 80\%$ 时, 第二步的反应就会以显著的速率进行 (若以生产乙基苯为目的, 则第二步的反应就是我们所不需要的反应)。

最简单的连续反应是两个单向连续的一级反应, 可一般地写作

$$
\begin{array}{l l l l} & \mathrm{A} \xrightarrow {k _ {1}} \mathrm{B} \xrightarrow {k _ {2}} \mathrm{C} \\ t = 0 & a & 0 & 0 \\ t = t & x & y & z \end{array}
$$

反应开始时, 设 A 的浓度为 a, B 与 C 的浓度为 0, 经过时间 t 后, A,B,C 的浓度分别为 x,y,z。生成 B 的净速率等于其生成速率与消耗速率之差。

$$
- \frac {\mathrm{d} x}{\mathrm{d} t} = k _ {1} x\tag{11.55}
$$

$$
\frac {\mathrm{d} y}{\mathrm{d} t} = k _ {1} x - k _ {2} y\tag{11.56}
$$

$$
\frac {\mathrm{d} z}{\mathrm{d} t} = k _ {2} y\tag{11.57}
$$

首先对式 (11.55) 求解, 这是一个典型的一级反应, 其积分公式为

$$
- \int_ {a} ^ {x} \frac {\mathrm{d} x}{x} = \int_ {0} ^ {t} k _ {1} \mathrm{d} t
$$

积分得

$$
\ln {\frac {a}{x}} = k _ {1} t \qquad {\text {或}} \qquad x = a \mathrm{e} ^ {- k _ {1} t}\tag{11.58}
$$

将式 $(11.58)$ 代入式 $(11.56)$ ，得

$$
\frac {\mathrm{d} y}{\mathrm{d} t} = k _ {1} a \mathrm{e} ^ {- k _ {1} t} - k _ {2} y
$$

这是一个 $\frac{\mathrm{dy}}{\mathrm{dx}} + Py = Q$ 型的一次线性微分方程, 该方程式的解为

$$
y = \frac {k _ {1} a}{k _ {2} - k _ {1}} \left(\mathrm{e} ^ {- k _ {1} t} - \mathrm{e} ^ {- k _ {2} t}\right)\tag{11.59}
$$

按照化学反应式, $a = x + y + z$ 或 $z = a - x - y$ , 将式 (11.58) 和式 (11.59) 代入后, 得

$$
z = a \left(1 - \frac {k _ {2}}{k _ {2} - k _ {1}} \mathrm{e} ^ {- k _ {1} t} + \frac {k _ {1}}{k _ {2} - k _ {1}} \mathrm{e} ^ {- k _ {2} t}\right)\tag{11.60}
$$

根据式 (11.58)、式 (11.59)、式 (11.60) 绘图, 得图 11.5。由图可见, A 的浓度随时间单调降低, C 的浓度随时间单调升高, 而 B 的浓度则开始升高, 以后降低, 中间出现极大值。

中间产物 B 的浓度在反应过程中出现极大值, 是连续反应的突出特征。在反应前期, 反应物 A 的浓度较高, 因而生成 B 的速率较快, B 的数量不断增加。但是, 随着反应继续进行, A 的浓度逐渐降低, 相应地使生成 B 的速率减慢。同时, 由于 B 的浓度升高, 进一步生成最终产物的速率不断加快, 使 B 被大量消耗, 因而 B 的数量反而减少。当生成 B 的速率与消耗 B 的速率相等时, 就出现极大点。

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_200-399_images/cd8f41efef4c9f2d6ef3ae25ac2a44e4c65281039570e22d28676a8cea071b42.jpg)  
图 11.5 连续反应中浓度随时间变化的关系图

可以利用动力学方程式 (11.59), 求得 $y$ 为极大值时的参数。将式 (11.59) 对 $t$ 微分, 当 $y$ 有极大值时:

$$
\frac {\mathrm{d} y}{\mathrm{d} t} = 0
$$

相应的反应时间为 $t_{m}$ :

$$
\frac {\mathrm{d} y}{\mathrm{d} t} = \frac {k _ {1} a}{k _ {2} - k _ {1}} \left(k _ {2} \mathrm{e} ^ {- k _ {2} t} - k _ {1} \mathrm{e} ^ {- k _ {1} t}\right) = 0
$$

解得

$$
t _ {\mathrm{m}} = \frac {\ln k _ {2} - \ln k _ {1}}{k _ {2} - k _ {1}}
$$

再代入式 (11.59), 得

$$
y _ {\mathrm{m}} = a \left(\frac {k _ {1}}{k _ {2}}\right) ^ {\frac {k _ {2}}{k _ {2} - k _ {1}}}\tag{11.61}
$$

$y_{m}$ 就是 B 处于极大值时的浓度。 $y_{m}$ 显然与 a 及 $k_{1}$ 和 $k_{2}$ 的比值有关。如果 $k_{1} \gg k_{2}$ ， $y_{m}$ 出现较早，且数值也较大。如果 $k_{1} \ll k_{2}$ ，则 $y_{m}$ 出现较迟，而且数值较小。

对于一般的反应来讲, 反应的时间长些, 得到的最终产物总是多一些。但对连续反应, 如果我们需要的是中间产物 B, 由于它有一个浓度最高的反应时间 $t_{\mathrm{m}}$ , 超过这个时间, 反而引起所需产物浓度的降低和副产物的增加。生产上如果控制反应时间使其在 $t_{\mathrm{m}}$ 附近, 则可望得到中间产物浓度最高的产品, 这对于产品的后处理过程是有利的。

以上讨论的是 $k_{1}, k_{2}$ 相差不大即两个反应的速率大致相等的情况。如果第一步反应很快， $k_{1} \gg k_{2}$ ，原始反应物很快就都转化为 B，则生成最终产物 C 的速率主要取决于第二步反应。另一种极端情况，如第二步反应很快， $k_{1} \ll k_{2}$ ，中间产物 B 一旦生成立即转化为 C，因此反应的总速率（即生成产物 C 的速率）取决于第一步反应。在式 (11.60) 中，若令 $k_{1} \ll k_{2}$ ，则可简化为 $z = a(1 - \mathrm{e}^{-k_{1} t})$ ，这相当于在始态和终态之间进行一个一级反应，产物的浓度与 $k_{1}$ 有关。所以，连续反应不论分几步进行，常是最慢的一步控制着全局，这最慢的一步就称为速率控制步骤, 简称速控步, 可以用它的速率近似作为整个反应的速率。

对复杂的连续反应, 要从数学上严格求许多联立微分方程的解, 从而求出反应过程中出现的各物浓度与时间 t 的关系是十分困难的。所以, 在动力学中也常采用一些近似方法, 如速控步近似法、稳态近似法 (见链反应一节) 等。

## \*11.6 基元反应的微观可逆性原理

以简单的单分子反应 (如顺-丁烯二酸转化为反-丁烯二酸的重排反应) 为例, 其基元反应为

$$
\mathrm{A} \xrightarrow [ k _ {- 1} ]{k _ {1}} \mathrm{B}
$$

正向反应速率 $r_1$ 为

$$
r _ {1} = k _ {1} [ \mathrm{A} ]
$$

逆向反应速率 $r_{-1}$ 为

$$
r _ {- 1} = k _ {- 1} [ \mathrm{B} ]
$$

系统达到平衡时, $r_{1}=r_{-1}$ ，所以

$$
\frac {[ \mathrm{B} ]}{[ \mathrm{A} ]} = \frac {k _ {1}}{k _ {- 1}} = K
$$

推而广之, 对任一对峙反应, 平衡时其基元反应的正向反应速率与逆向逆反应速率必须相等。这一原理称为精细平衡原理 (principle of detailed balance)。从理论上讲, 精细平衡原理是微观可逆性 (microscopic reversibility) 对大量微观粒子构成的宏观系统相互制约的结果。所谓微观可逆性是指微观粒子系统具有时间反演的对称性。

分子的相互碰撞是力学行为, 它服从力学中的一条规律——“时间反演对称性”, 即在力学方程中, 如将时间 t 用 -t 代替, 则对正向运动方程的解和对逆向运动方程的解完全相同, 只是二者相差一个正负符号。反言之, 对于化学反应, 微观可逆性可以表述为: 基元反应的逆过程必然也是基元反应。而且逆过程就按原来的路程返回, 就像把电影胶片倒放一遍一样。因此, 从微观的角度看, 若正向反应是允许的, 则其逆向反应亦应该是允许的。

对含有大量分子的宏观系统而言, 当分子处于各种微观状态时, 分子所进行的每一个反应 (或每一个规程) 在正、逆两个方向进行反应时的速率相等, 如前所述, 这就是精细平衡原理。

根据精细平衡原理可以推出一个结论, 即在复杂反应 (即非基元反应) 中如果有一个速控步 (控制整个反应的步骤), 则它必然也是逆反应的速控步。微观可逆性与精细平衡原理之间的关系是因果关系, 但通常在化学反应动力学的讨论中不去区分两者之间的细微差别。

前面所讲的 $H_{2}$ 和 $Br_{2}$ 的复杂反应, 是由五个基元反应构成的, 由于达平衡时正、逆反应的速率相等, 且具有微观可逆性, 故而

$$
\begin{array}{r l r l} \mathrm{Br} _ {2} + \mathrm{M} & \xrightarrow [ k _ {- 1} ]{k _ {1}} 2 \mathrm{Br} \cdot + \mathrm{M} & K _ {1} = \frac {k _ {1}}{k _ {- 1}} \\ \mathrm{Br} \cdot + \mathrm{H} _ {2} & \xrightarrow [ k _ {- 2} ]{k _ {2}} \mathrm{HBr} + \mathrm{H} \cdot & K _ {2} = \frac {k _ {2}}{k _ {- 2}} \\ \mathrm{H} \cdot + \mathrm{Br} _ {2} & \xrightarrow [ k _ {- 3} ]{k _ {3}} \mathrm{HBr} + \mathrm{Br} \cdot & K _ {3} = \frac {k _ {3}}{k _ {- 3}} \\ \mathrm{H} \cdot + \mathrm{HBr} & \xrightarrow [ k _ {- 4} ]{k _ {4}} \mathrm{H} _ {2} + \mathrm{Br} \cdot & K _ {4} = \frac {k _ {4}}{k _ {- 4}} \\ \mathrm{Br} \cdot + \mathrm{Br} \cdot + \mathrm{M} & \xrightarrow [ k _ {- 5} ]{k _ {5}} \mathrm{Br} _ {2} + \mathrm{M} & K _ {5} = \frac {k _ {5}}{k _ {- 5}} \end{array}
$$

总反应的平衡常数为

$$
\begin{array}{r l} K & = K _ {1} \cdot K _ {2} \cdot K _ {3} \cdot K _ {4} \cdot K _ {5} \\ & = \frac {k _ {1} k _ {2} k _ {3} k _ {4} k _ {5}}{k _ {- 1} k _ {- 2} k _ {- 3} k _ {- 4} k _ {- 5}} \\ & = \prod_ {i} \frac {k _ {i}}{k _ {- i}} \end{array}
$$

## 11.7 温度对反应速率的影响

## 速率常数与温度的关系——Arrhenius 经验式

温度可以影响反应速率, 这是根据经验早已知道的事实。历史上, van't Hoff 曾根据实验事实总结出一条近似规律, 即温度每升高 10 K, 反应速率增加 2 \~ 4 倍, 用公式表示为

$$
\frac {k _ {T + 1 0 \mathrm{K}}}{k _ {T}} = 2 \sim 4
$$

如果不需要精确的数据或手边的数据不全, 则可根据这个规律大略地估计出温度对反应速率的影响, 这个规律有时称为 van't Hoff 近似规则。

## 例11.8

若某一反应 A $\longrightarrow$ B, 近似地满足于 van't Hoff 规则。今使这个反应在两个不同的温度下进行, 但起始浓度相同, 并达到同样的反应程度 (即相同的转化率)。当反应在 390 K 下进行时, 需时 10 min, 试估计在 290 K 进行时, 需要多少时间? 假定这个反应的速率方程式为

$$
- \frac {\mathrm{d} c}{\mathrm{d} t} = k c ^ {n}
$$

且假定在此温度区间内，反应的历程不变，且无副反应。

解 设在 $T_{1}$ 时的速率常数为 $k_{1}$ , 则

$$
- \int_ {c _ {0}} ^ {c} \frac {\mathrm{d} c}{c ^ {n}} = \int_ {0} ^ {t _ {1}} k _ {1} \mathrm{d} t
$$

在 $T_{2}$ 时的速率常数为 $k_{2}$ ，则

$$
- \int_ {c _ {0}} ^ {c} \frac {\mathrm{d} c}{c ^ {n}} = \int_ {0} ^ {t _ {2}} k _ {2} \mathrm{d} t
$$

由于起始浓度和反应程度都相同, 所以上两式左方积分的数值应相同。因此得到

$$
k _ {1} t _ {1} = k _ {2} t _ {2}\tag{11.62}
$$

所以

$$
\frac {k _ {3 9 0 \mathrm{K}}}{k _ {2 9 0 \mathrm{K}}} = \frac {t _ {2 9 0 \mathrm{K}}}{t _ {3 9 0 \mathrm{K}}}
$$

根据 van't Hoff 近似规则, 若速率的温度系数取其低限, 即

$$
\frac {k _ {T + 1 0 \mathrm{K}}}{k _ {T}} = 2
$$

则

$$
\begin{array}{r l} & {\frac {k _ {3 9 0 \mathrm{K}}}{k _ {2 9 0 \mathrm{K}}} = \frac {k _ {(2 9 0 \mathrm{K} + 1 0 \mathrm{K} \times 1 0)}}{k _ {2 9 0 \mathrm{K}}} = 2 ^ {1 0} = 1 0 2 4} \\ & {\qquad \frac {t _ {2 9 0 \mathrm{K}}}{t _ {3 9 0 \mathrm{K}}} = \frac {t _ {2 9 0 \mathrm{K}}}{1 0 \mathrm{min}} = 1 0 2 4} \end{array}
$$

$$
t _ {2 9 0 \mathrm{K}} = 1 0 2 4 \times 1 0 \mathrm{min} = 1 0 2 4 0 \mathrm{min} \approx 7 \mathrm{d}
$$

从上面估计可以看出, 在 390 K 时反应时间为 10 min, 而在 290 K 却要 7 d, 显然这样长的时间是没有工业生产价值的。反之, 如果某一反应在常温下不太快的话, 在升高温度后就有可能变得很快, 甚至导致无法控制, 这也是工业生产所禁忌的。由此可见, 温度的控制对于研究反应速率、反应历程以及化工生产是极为重要的。

Arrhenius 研究了许多气相反应的速率, 特别是对蔗糖在水溶液中的转化反应做了大量的研究工作。他提出了活化能的概念, 并揭示了反应的速率常数与温度的依赖关系, 即

$$
k = A \mathrm{e} ^ {- \frac {E _ {\mathrm{a}}}{R T}}\tag{11.63}
$$

式 (11.63) 称为 Arrhenius 公式。式中 $k$ 是温度为 $T$ 时反应的速率常数； $R$ 是摩尔气体常数； $A$ 是指前因子 (pre-exponential factor); $E_{\mathrm{a}}$ 是表观活化能 (apparent activation energy, 通常简称为活化能)。

Arrhenius 认为, 并不是反应分子之间的任何一次直接接触 (或碰撞) 都能发生反应, 只有那些能量足够高的分子之间的直接碰撞才能发生反应。那些能量高到能发生反应的分子称为 “活化分子” (activated molecule)。由非活化分子变成活化分子所要的能量称为 (表观) 活化能。其实, Arrhenius 当时对活化能并没有给出明确的定义, 他最初认为反应的活化能和指前因子只取决于反应物质的本性, 而与温度无关。

对式 $(11.63)$ 取对数, 得

$$
\ln k = \ln A - \frac {E _ {\mathrm{a}}}{R T}\tag{11.64}
$$

若假定 A 与 T 无关, 则得到微分形式:

$$
\frac {\mathrm{d} \ln k}{\mathrm{d} T} = \frac {E _ {\mathrm{a}}}{R T ^ {2}}\tag{11.65}
$$

根据式 (11.64), 若以 $\ln k$ 对 $1 / T$ 作图, 可得一直线, 由直线的斜率和截距, 可分别求得 $E_{\mathrm{a}}$ 和 $A$ 。

Arrhenius 公式在化学动力学的发展过程中所起的作用是非常重要的, 特别是他所提出的活化分子的活化能概念, 在反应速率理论的研究中起了很大的作用。

表 11.4 中列出了常温下一些反应的动力学参数。

表 11.4 常温下一些反应的动力学参数 $\left( {{E}_{\mathrm{a}}\text{ 和 }A}\right)$

<table><tr><td>反应</td><td>介质 $E_{\text{a}}/(kJ \cdot mol^{-1})$ </td><td colspan="2">lg[ $A/(mol^{-1} \cdot dm^{3} \cdot s^{-1})$ ]</td></tr><tr><td> $CH_3COOC_2H_5 + NaOH \longrightarrow CH_3COONa + C_2H_5OH$ </td><td>水</td><td>47.3</td><td>7.2</td></tr><tr><td> $n-C_5H_{11}Cl + KI \longrightarrow n-C_5H_{11}I + KCl$ </td><td>丙酮</td><td>77.0</td><td>8.0</td></tr><tr><td> $C_2H_5ONa + CH_3I \longrightarrow C_2H_5OCH_3 + NaI$ </td><td>乙醇</td><td>81.6</td><td>11.4</td></tr><tr><td> $C_2H_5Br + NaOH \longrightarrow C_2H_5OH + NaBr$ </td><td>乙醇</td><td>89.5</td><td>11.6</td></tr><tr><td> $CH_3I + HI \longrightarrow CH_4 + 2I \cdot$ </td><td>气相</td><td>139.7</td><td>12.2</td></tr><tr><td> $2HI \longrightarrow H_2 + I_2$ </td><td>气相</td><td>184.1</td><td>11.2</td></tr><tr><td> $H_2 + I_2 \longrightarrow 2HI$ </td><td>气相</td><td>165.3</td><td>11.2</td></tr><tr><td> $NH_4CNO \longrightarrow NH_2CONH_2$ </td><td>水</td><td>97.1</td><td>12.6</td></tr><tr><td> $N_2O_5 \longrightarrow N_2O_4 + \frac{1}{2}O_2$ </td><td>气相</td><td>103.3</td><td>13.7</td></tr><tr><td> $CH_3N_2CH_3 \longrightarrow C_2H_6 + N_2$ </td><td>气相</td><td>219.7</td><td>13.5</td></tr><tr><td> $CH_2-CH_2 \longrightarrow CH_3CH=CH_2$  $\backslash$  $CH_2$ </td><td>气相</td><td>272.0</td><td>12.2</td></tr><tr><td> $2NO + O_2 \longrightarrow 2NO_2$ </td><td>气相</td><td>-4.6</td><td>3.02</td></tr><tr><td> $Br \cdot + Br \cdot + M \longrightarrow Br_2 + M$ </td><td>气相</td><td>0</td><td> $9.60(M = H_2)$ </td></tr></table>

在讨论平衡常数与温度的关系时, 曾介绍过 van't Hoff 公式:

$$
\frac {\mathrm{d} \ln K ^ {\ominus}}{\mathrm{d} T} = \frac {\Delta_ {\mathrm{r}} H _ {\mathrm{m}} ^ {\ominus}}{R T ^ {2}}
$$

这个公式和式 (11.65) 很相似。van't Hoff 公式是从热力学角度说明温度对平衡常数的影响, 而 Arrhenius 公式则是从动力学的角度说明温度对反应速率常数的影响。

对于吸热反应, $\Delta_{\mathrm{r}}H_{\mathrm{m}}^{\ominus} > 0$ , $\frac{\mathrm{d}\ln K^{\ominus}}{\mathrm{d}T} > 0$ , 即平衡常数 $K^{\ominus}$ 随温度的上升而增大, 也就是平衡转化率随温度的升高而增加。而从 Arrhenius 公式知, 当温度上升时 $k$ 也增加, 因此无论从热力学还是动力学的角度, 温度升高对吸热反应有利。而对于放热反应, 因为 $\Delta_{\mathrm{r}}H_{\mathrm{m}}^{\ominus} < 0$ , 所以 $\frac{\mathrm{d}\ln K^{\ominus}}{\mathrm{d}T} < 0$ , 从热力学的角度看, 升高温度对放热反应不利。而从动力学角度看, 升高温度总是使反应加快。这里遇到了矛盾, 因此要作具体分析。一般来说, 只要一个反应的平衡转化率没有低到没有生产价值的情况下, 速率因素总是矛盾的主要方面。例如, 合成氨反应是一个放热放应, 在常温下的转化率理应比高温时高。但在常温下, 它的反应速率很慢 (迄今人们还没有找到合适的催化剂, 使反应速率提高到可在常温下能进行工业生产的程度)。如果适当地提高温度, 平衡转化率虽然有所下降, 但由于速率加快了, 在短时间内总是可以得到一定数量的产品, 而且没有反应掉的原料还可以循环使用。所以, 在工业生产中, 合成氨的反应温度一般控制在 773 K。在理论上可以用对反应速率求极值的办法, 求出最适宜温度 $T_{m}$ 。

实际生产中绝大部分反应都不可能达到平衡, 因为达到平衡需要时间, 所以实际转化率总比平衡转化率低。在平衡与速率二者之间, 从提高产量的角度来看我们希望它的速率快一些, 通过提高反应速率来弥补转化率低的不足。但是, 也不能盲目提高温度, 温度过高, 反应过快, 甚至可能发生局部过热、燃烧和爆炸等事故。同时还要考虑温度对副反应的影响, 对催化剂的影响 (如防止催化剂烧结而丧失活性) 等一系列问题。所以, 在工业化生产过程中必须全面考虑问题, 衡量各种利弊。

## 反应速率与温度关系的几种类型

总包反应是许多简单反应的综合。因此，总包反应的反应速率与温度之间的关系是比较复杂的。实验表明，总包反应的反应速率 $(r)$ 与温度 $(T)$ 之间的关系，大致可用图11.6所示的几种示意图来表示。

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_200-399_images/5f53a3bcbee2c381f97b363030006ccfaaf14b0cf1d656cd766fe3a066569a19.jpg)  
(a)

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_200-399_images/8ccc976387679f93e87a4d0d834802e2eb9b0d58039f7e6058b1fbc9288ff23a.jpg)  
(b)

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_200-399_images/e4aa9b481b052d44661746c7866d8d1fce679da008e75a6202e7bd2967737c6c.jpg)  
(c)

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_200-399_images/4fb62ee678f6920ab103724c7adaae1c8ee0f10d409e0939a55c0f2cac8359bd.jpg)  
(d)

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_200-399_images/32fe456bf7386926836e59a480cf9b681f9414c3fd755ecdec1811f19a88f772.jpg)  
(e)

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_200-399_images/92b718c5a75988ed4804282c35fab80fb7033356c9744f8a927120820817a89c.jpg)  
(f)  
图 11.6 总包反应的反应速率 (r) 与温度 (T) 之间的关系示意图

图 11.6(a) 是根据 Arrhenius 公式所得的 S 形曲线, 当 $T \rightarrow 0$ 时, $r \rightarrow 0$ ; 当 $T \rightarrow \infty$ 时, r 有定值 (这是一个在全温度范围内的图形)。由于一般实验都是在常温的有限温度区间中进行, 所得的曲线由图 11.6(b) 来表示。它实际上是 (a) 在有限的温度范围内 [即 (a) 中用虚线框表示部分] 的放大图。(a) 和 (b) 都遵守 Arrhenius 公式。图 11.6(c) 对应的是总包反应中含有爆炸型的反应, 在低温时, 反应速率较慢, 基本上符合 Arrhenius 公式。但当温度升高到某一临界值时, 反应速率迅速增大, 甚至趋于无限, 以致引起爆炸。第四种类型 (d) [图 11.6(d)] 常在一些受吸附速率控制的多相催化反应 (如加氢反应) 中出现。在温度不太高的情况下, 反应速率随温度升高而加快, 但达到某一高度以后若再升高温度, 将使反应速率变慢。这可能是高温对催化剂的性能有不利的影响所致。由酶催化的一些反应多属于这一类型, 因为当温度升高到一定程度时, 酶的活性开始丧失。第五种类型 (e)[图 11.6(e)] 是在碳的氢化反应中观察到的, 当温度升高时可能有副反应发生而复杂化, 曲线出现最高点和最低点。也可能是总包反应中出现了 (c), (d) 类型的反应所致。第六种类型 (f) [图 11.6(f)] 是反常的, 温度升高, 反应速率反而变慢, 如一氧化氮氧化成二氧化氮的反应就属于这一类型。由于第二种类型 (b) 最为常见, 所以通常所讨论的反应大多数是指这一类型。

## \* 反应速率与活化能之间的关系

反应的速率 $r \propto k$ 。在 Arrhenius 公式 $k = A \exp \left(-\frac{E_{\mathrm{a}}}{RT}\right)$ 中，把活化能 $E_{\mathrm{a}}$ 看作与温度无关的常数，这在一定的温度范围内与实验结果基本上是相符的。

如以 $\ln k$ 对 $\frac{1}{T}$ 作图，根据Arrhenius公式，直线的斜率为 $-\frac{E_{\mathrm{a}}}{R}$ 。图11.7是一个示意图，图中纵坐标数字刻度采用自然对数，所以其读数就是 $k$ 的数值。 $E_{\mathrm{a}}$ 越大，则斜率（指绝对值）也越大，所以图中I，II，III三个反应的活化能 $E_{\mathrm{a}}(\mathrm{III}) > E_{\mathrm{a}}(\mathrm{II}) > E_{\mathrm{a}}(\mathrm{I})$ 。

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_200-399_images/d68aa1404c3f4fbe4f10f34c04b385cc7da0952a245b22779d88f14928412deb.jpg)  
图 11.7 $\ln k$ 对 $\frac{1}{T}$ 作图 (示意图)

对于一个给定的反应, 在低温范围内反应的速率随温度的变化更敏感。例如反应 II, 在温度由 376 K 增加到 463 K, 即增加 87 K 时, k 值由 10 增加到 20,就增加一倍。而在高温范围内, 若要 k 增加一倍 (即由 100 增至 200), 温度要由 1000 K 变成 2000 K (即增加 1000 K) 才行。

对于活化能不同的反应, 当温度增加时, $E_{a}$ 大的反应速率增加的倍数比 $E_{a}$ 小的反应速率增加的倍数大。例如反应Ⅲ和Ⅱ, 因为 $E_{\mathrm{a}}(\mathrm{III}) > E_{\mathrm{a}}(\mathrm{II})$ , 当温度从 1000 K 变成 2000 K 时, $k(\mathrm{II})$ 从 100 增加到 200, 增大了一倍, 而 $k(\mathrm{III})$ 却从 10 变成了 200, 增加了 19 倍。所以, 若几个反应同时发生时, 升高温度对 $E_{a}$ 大的反应有利。这种关系也可用如下的关系式来说明, 根据式 (11.65):

$$
\begin{array}{r l} & {\frac {\mathrm{d} \ln k _ {1}}{\mathrm{d} T} = \frac {E _ {\mathrm{a,1}}}{R T ^ {2}}} \\ & {\frac {\mathrm{d} \ln k _ {2}}{\mathrm{d} T} = \frac {E _ {\mathrm{a,2}}}{R T ^ {2}}} \end{array}
$$

两式相减, 得

$$
\frac {\mathrm{d} \ln (k _ {1} / k _ {2})}{\mathrm{d} T} = \frac {E _ {\mathrm{a,1}} - E _ {\mathrm{a,2}}}{R T ^ {2}}
$$

若 $E_{a,1} > E_{a,2}$ ，当温度升高时， $\frac{k_{1}}{k_{2}}$ 值增大，即 $k_{1}$ 随温度的增加倍数大于 $k_{2}$ 随温度的增加倍数。反之，若 $E_{a,1} < E_{a,2}$ ，则温度升高时， $\frac{k_{1}}{k_{2}}$ 值减小，即 $k_{1}$ 随温度的增加倍数小于 $k_{2}$ 随温度的增加倍数。由此可见，高温有利于活化能较大的反应，低温有利于活化能较低的反应。如果两个反应在系统中都可以发生，则它们可以看成一对竞争反应。对于复杂反应，可以根据上述温度对竞争反应速率的影响的一般规则来寻找较适宜的操作温度。

对连续反应:

$$
\mathrm{A} \xrightarrow [ E _ {\mathrm{a,1}} ]{k _ {1}} \mathrm{P} \xrightarrow [ E _ {\mathrm{a,2}} ]{k _ {2}} \mathrm{S}
$$

如果 P 是所需要的产物, 而 S 是副产物, 则希望 $k_{1}/k_{2}$ 值越大越有利于 P 的生成。因此, 若 $E_{a,1} > E_{a,2}$ , 则宜用较高的反应温度; 若 $E_{a,1} < E_{a,2}$ , 则宜用较低的反应温度。

对平行反应:

$$
\mathrm{A} \xrightarrow [ k _ {2} , E _ {\mathrm{a} , 2} ]{k _ {1} , E _ {\mathrm{a} , 1}} \mathrm{P} (\text {产物})
$$

同样希望 $k_{1}/k_{2}$ 值越大越有利 P 的生成, 若 $E_{a,1} > E_{a,2}$ , 则宜用较高的反应温度; 若 $E_{a,1} < E_{a,2}$ , 则宜用较低的反应温度。

对于反应都是一级的平行反应:

$$
\mathrm{A} \xrightarrow { \begin{array}{c} k _ {1} , E _ {\mathrm{a} , 1} \\ k _ {2} , E _ {\mathrm{a} , 2} \\ k _ {3} , E _ {\mathrm{a} , 3} \end{array} } \mathrm{P} (\text {产物})   \mathrm{S} _ {1} (\text {副产物})   \mathrm{S} _ {2} (\text {副产物})
$$

这类反应在有机反应如硝化、氯化中是常见的。若设 $E_{a,3} > E_{a,1} > E_{a,2}$ ，这时就需要寻找一个最有利于产物 P 生成的中间温度。同样采用求极值的方法（证明从略），可得出此中间温度应满足如下公式：

$$
T = \frac {E _ {\mathrm{a,3}} - E _ {\mathrm{a,2}}}{R \ln \left(\frac {E _ {\mathrm{a,3}} - E _ {\mathrm{a,1}}}{E _ {\mathrm{a,1}} - E _ {\mathrm{a,2}}} \cdot \frac {A _ {3}}{A _ {2}}\right)}
$$

当然, 若能寻找一个合适的催化剂, 降低 $E_{\mathrm{a},1}$ , 增大 $k_{1}$ , 则反应对主要产物 $\mathbf{P}$ 的选择性同样会大大提高。

## \*11.8 关于活化能

## 活化能概念的进一步说明

在 Arrhenius 公式中, 把 $E_{\mathrm{a}}$ 看作与温度无关的常数, 这在一定的温度范围内与实验结果是相符的。但是, 如果实验温度范围适当放宽或对于较复杂的反应, 则 $\ln k$ 对 $\frac{1}{T}$ 作的图就不是一条很好的直线, 这表明 $E_{\mathrm{a}}$ 与温度有关, 而且 Arrhenius 经验式对某些历程复杂的反应不适用。例如, 对于烯烃在 Bi-Mo 型催化剂上的催化氧化反应, 由于几个同时发生的平行反应的 $E_{\mathrm{a}}$ 相差较大, 且受温度影响的程度各不相同, 在平行反应之间发生竞争, 因而 $\ln k$ 对 $\frac{1}{T}$ 作图得到的是一条折线。

对于基元反应, $E_{\mathrm{a}}$ 可赋予较明确的物理意义。分子相互作用的首要条件是它们必须“接触”，虽然分子彼此碰撞的频率很高，但并不是所有的碰撞都是有效的，只有少数能量较高的分子碰撞后才能起作用， $E_{\mathrm{a}}$ 表征了反应分子能发生有效碰撞的能量要求。Tolman曾证明：

$$
E _ {\mathrm{a}} = \overline {{{{E}}}} ^ {*} - \overline {{{{E}}}} _ {\mathrm{R}}\tag{11.66}
$$

式中 $\overline{E}^{*}$ 表示能发生反应分子的平均能量, $\overline{E}_{R}$ 表示所有反应物分子的平均能量,其单位都是 $J \cdot mol^{-1}$ 。 $E_{a}$ 是这两个统计平均能量的差值。如对一个分子而言，将式 (11.66) 除以 Avogadro 常数，则

$$
\varepsilon_ {\mathrm{a}} = \frac {\overline {{{E}}} ^ {*} - \overline {{{E}}} _ {\mathrm{R}}}{L} = \overline {{{\varepsilon}}} ^ {*} - \overline {{{\varepsilon}}} _ {\mathrm{R}}\tag{11.67}
$$

$\varepsilon_{\mathrm{a}}$ 就是一个具有平均能量 $\overline{\varepsilon}_{\mathrm{R}}$ 的反应物分子要变成具有平均能量 $\overline{\varepsilon}^{*}$ 的活化分子必须获得的能量, $E_{\mathrm{a}} = \varepsilon_{\mathrm{a}} \cdot L$ , 式中 $E_{\mathrm{a}}$ 称为实验活化能, 简称活化能 (activation energy)。

设反应为

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_200-399_images/c1e7fcaae53c5925e2e049ef65da011ee7106584ae89e2db838b4b5830f9db35.jpg)  
图 11.8 基元反应活化能示意图

$$
\mathrm{A} \longrightarrow \mathrm{P}
$$

反应物 A 必须获得能量 $E_{a}$ 变成活化状态 $A^{*}$ ，才能越过能垒变成产物 P。同理，对逆反应，P 必须获得 $E_{a}^{\prime}$ 的能量才能越过能垒变成 A（参阅图 11.8）。上述活化能与活化状态的概念和图示，对反应速率理论的发展起了很大的作用。

对于非基元反应, $E_{\mathrm{a}}$ 就没有明确的物理意义了, 它实际上是组成该总包反应的各种基元反应活化能的特定组合。仍以如下反应为例:

$$
\mathrm{H} _ {2} + \mathrm{I} _ {2} \xrightarrow {k} 2 \mathrm{HI}
$$

该反应的总速率表示式为

$$
\begin{array}{r l} & r = - \frac {\mathrm{d} [ \mathrm{H} _ {2} ]}{\mathrm{d} t} = k [ \mathrm{H} _ {2} ] [ \mathrm{I} _ {2} ] \\ & k = A \exp \left(- \frac {E _ {\mathrm{a}}}{R T}\right) \end{array}
$$

已知其反应历程为

(1)

$$
\begin{array}{r l} & \mathrm {I_ {2}} + \mathrm{M} \xrightarrow [ k _ {- 1} ]{k _ {1}} 2 \mathrm{I} \cdot + \mathrm{M} \\ & \mathrm {H_ {2}} + 2 \mathrm{I} \cdot \xrightarrow {k _ {2}} 2 \mathrm{HI} \end{array}\tag{2}
$$

对反应 (1), 有

$$
\overrightarrow {r _ {1}} = k _ {1} [ \mathrm{I} _ {2} ] [ \mathrm{M} ] \quad k _ {1} = A _ {1} \exp \left(- \frac {E _ {\mathrm{a} , 1}}{R T}\right)\tag{1}
$$

$$
\overleftarrow {r _ {- 1}} = k _ {- 1} [ \mathrm{I} \cdot ] ^ {2} [ \mathrm{M} ] \quad k _ {- 1} = A _ {- 1} \exp \left(- \frac {E _ {\mathrm{a} , - 1}}{R T}\right)\tag{2}
$$

平衡时， $\overrightarrow{r_1} = \overleftarrow{r_{-1}}$ ，则有

$$
[ \mathrm{I} \cdot ] ^ {2} = \frac {k _ {1} [ \mathrm{I} _ {2} ]}{k _ {- 1}}\tag{3}
$$

对反应 (2), 有

$$
r _ {2} = - \frac {\mathrm{d} [ \mathrm{H} _ {2} ]}{\mathrm{d} t} = k _ {2} [ \mathrm{H} _ {2} ] [ \mathrm{I} \cdot ] ^ {2} \quad k _ {2} = A _ {2} \exp \left(- \frac {E _ {\mathrm{a} , 2}}{R T}\right)\tag{4}
$$

将式 (3) 代入速率表示式, 得

$$
\begin{array}{r l} r & = \frac {k _ {2} k _ {1}}{k _ {- 1}} [ \mathrm{H} _ {2} ] [ \mathrm{I} _ {2} ] \\ & = k [ \mathrm{H} _ {2} ] [ \mathrm{I} _ {2} ] \qquad \left(\text {令} \frac {k _ {2} k _ {1}}{k _ {- 1}} = k\right) \end{array}
$$

所以, 将式 (1), (2), (4) 的速率常数表示式代入, 得

$$
\begin{array}{r l} k & = \frac {k _ {2} k _ {1}}{k _ {- 1}} = \frac {A _ {2} A _ {1}}{A _ {- 1}} \exp \left(- \frac {E _ {\mathrm{a,2}} + E _ {\mathrm{a,1}} - E _ {\mathrm{a,-1}}}{R T}\right) \\ & = A \exp \left(- \frac {E _ {\mathrm{a}}}{R T}\right) \end{array}
$$

式中 $A = \frac{A_2A_1}{A_{-1}}, E_{\mathrm{a}} = E_{\mathrm{a},2} + E_{\mathrm{a},1} - E_{\mathrm{a}, - 1}$

由此可见, Arrhenius 活化能 $E_{a}$ 在复杂反应中仅是各基元反应活化能的组合, 没有明确的物理意义。这时 $E_{a}$ 称为该总包反应的表观活化能, A 称为表观指前因子 (apparent pre-exponential factor)。

## 活化能与温度的关系

很多反应若按 Arrhenius 公式, 以 $\ln k$ 对 $1 / T$ 作图, 常得到的图形是一条曲线, 而不是直线, 这表明表观活化能不是一个常数。在第十二章讨论反应的速率理论时将会指出, $k$ 与 $T$ 的关系可以写成

$$
k = A _ {0} T ^ {m} \exp \left(- \frac {E _ {0}}{R T}\right)\tag{11.68}
$$

式中多了一个 $T^{m}$ 项, 现在我们可以暂时把它看成对 Arrhenius 公式的一个修正项, 成为含有三个参量的经验公式。式中 $A_{0}$ 是与温度无关的常数, $m$ 是绝对值不大于 4 的整数或半整数。式 (11.68) 也可以写成

$$
\ln \frac {k}{T ^ {m}} = \ln A _ {0} - \frac {E _ {0}}{R T}
$$

或

$$
\ln k = \ln A _ {0} + m \ln T - \frac {E _ {0}}{R T}\tag{11.69}
$$

此式表明, 无论以 $\ln \frac{k}{T^m}$ 对 $1 / T$ 作图, 或以 $\ln k$ 对 $1 / T$ 作图都可大致得到一条直线, 只不过所得直线的截距不同而已。

Arrhenius 公式中的 $E_{a}$ 应是温度的函数, 考虑到温度的影响, 可以将 Arrhenius 公式写成

$$
E _ {\mathrm{a}} = R T ^ {2} \frac {\mathrm{dln} k}{\mathrm{d} T}
$$

将式 (11.69) 对 $T$ 微分后, 代入上式, 得到 $E_{\mathrm{a}}$ 与 $T$ 之间关系的表达式:

$$
E _ {\mathrm{a}} = E _ {0} + m R T\tag{11.70}
$$

在式(11.69)中， $A_{0}, m, E_{0}$ 都要由实验确定。式中 $\ln k$ 与 1/T 偏离线性关系的程度取决于 $m \ln T$ 项数值的大小。由于通常一般反应的 m 值较小，所以不少系统的实验值仍与 Arrhenius 公式的经验式相符合。

## 活化能的估算

除了用各种实验方法来获得 $E_{a}$ 的数值外, 人们还提出了一些从理论上来预测或估计活化能的方法。一般从反应所涉及的化学键的键能来估算, 这些估计方法还只能是经验的, 所得结果也比较粗糙, 但在分析反应速率问题时, 仍然是有帮助的。

(甲) 对于基元反应

$$
\mathrm{A-A+B-B} \longrightarrow 2 \mathrm{A-B}
$$

这里需要改组的化学键为 A-A（键能 $\varepsilon_{A-A}$ ）和 B-B（键能为 $\varepsilon_{B-B}$ ）。分子反应的首要条件是“接触”，在“接触”过程中有一部分分子取得一些能量，否则化学键的改组就不可能进行。但是，分子并不需要全部拆散才发生反应，而是先形成一个活化体，活化体的寿命很短，一经形成就很快转化为产物。所以，通常基元反应所需的活化能约占这些待破化学键键能的 30%。

$$
\begin{array}{r l} & \mathrm{A-A+B-B} \longrightarrow \begin{array}{c c c} \mathrm{A-}\dots \mathrm{A} \\ | & | & 2 \mathrm{A-B} \\ \mathrm{B-}\dots \mathrm{B} \end{array} \\ & E _ {\mathrm{a}} = (\varepsilon_ {\mathrm{A-A}} + \varepsilon_ {\mathrm{B-B}}) L \times 30 \% \end{array}
$$

(乙) 对于有自由基参加的基元反应, 例如:

$$
\mathrm{H} \cdot + \mathrm{Cl} - \mathrm{Cl} \longrightarrow \mathrm{H} - \mathrm{Cl} + \mathrm{Cl} \cdot
$$

由于反应物中有一个活性很大的原子或自由基, 正反应为放热反应, 所需活化能约为需被改组化学键键能的 5.5%, 如对于上述反应, 有

$$
E _ {\mathrm{a}} = \varepsilon_ {\mathrm{Cl-Cl}} L \times 5.5
$$

(丙) 对于分子裂解成两个原子或自由基的反应, 例如:

$$
\mathrm{Cl} - \mathrm{Cl} + \mathrm{M} \longrightarrow 2 \mathrm{Cl} \cdot + \mathrm{M}
$$

在这样的基元反应中需要解开 Cl—Cl 键, 而无须再形成新的化学键, 所以 $E_{a} = \varepsilon_{Cl-Cl} L$ 。

(丁) 对于自由基的复合反应, 例如:

$$
\mathrm{Cl} \cdot + \mathrm{Cl} \cdot + \mathrm{M} \longrightarrow \mathrm{Cl} _ {2} + \mathrm{M}
$$

这类反应的 $E_{a}=0$ ，因为自由基本来是很活泼的，复合时不需要破坏化学键，故不必吸收额外的能量。有时处于激发态的自由基在复合成分子时回到基态，还会释放出能量，使表观活化能出现负值。

上述的估计比较粗糙, 仅能作为参考。

## 11.9 链反应

在化学动力学中有一类特殊的反应, 只要用热、光、辐射或其他方法使反应引发, 它便能通过活性组分 (自由基或原子) 相继发生一系列的连续反应, 像链条一样使反应自动发展下去, 这类反应称为链反应 (chain reaction)。工业上很多重要的工艺过程, 如橡胶的合成, 塑料、高分子化合物的制备, 石油的裂解, 碳氢化合物的氧化等, 都与链反应有关。所有的链反应都是由下列三个基本步骤组成的:

(1) 链的开始 (或链的引发, chain initiation) 即开始时分子借助光、热等外因生成自由基的反应。在这个反应过程中需要断裂分子中的化学键, 因此它所需要的活化能与断裂化学键所需的能量是同一个数量级。

(2) 链的传递 (或链的增长, chain propagation) 即自由原子或自由基与饱和分子作用生成新的分子和新的自由基 (或原子), 这样不断交替。若不受阻, 反应就一直进行下去, 直至反应物被耗尽为止。由于自由原子或自由基有较强的反应能力, 故所需活化能一般小于 $40 \mathrm{~kJ} \cdot \mathrm{mol}^{-1}$ 。

(3) 链的终止 (chain termination) 当自由基被消除时, 链就终止。断链的方式可以是两个自由基结合成分子, 也可以是与器壁碰撞时, 器壁吸收自由基的能量而断链, 例如:

$$
\mathrm{Cl} \cdot + \text {   器壁   } \longrightarrow \text {   断链   }
$$

因此, 改变反应器的形状或表面涂料等都可能影响反应速率, 这种器壁效应是链反应的特点之一。

根据链的传递方式不同, 可将链反应分为直链反应 (straight chain reaction) 和支链反应 (branched chain reaction)。

## 直链反应 ( $H_{2}$ 和 $Cl_{2}$ 反应的历程)——稳态近似法

$H_{2}(g)$ 和 $Cl_{2}(g)$ 反应的净结果是

$$
\mathrm{H} _ {2} (\mathrm{g}) + \mathrm{Cl} _ {2} (\mathrm{g}) \longrightarrow 2 \mathrm{HCl} (\mathrm{g})
$$

根据很多人的研究, 生成 $\mathrm{HCl(g)}$ 的速率既与 $[\mathrm{Cl}_2]^{\frac{1}{2}}$ 成正比, 又与 $[\mathrm{H}_2]$ 成正比, 即

$$
r = \frac {1}{2} \frac {\mathrm{d} [ \mathrm{HCl} ]}{\mathrm{d} t} = k [ \mathrm{Cl} _ {2} ] ^ {\frac {1}{2}} [ \mathrm{H} _ {2} ]
$$

据此, 人们推测反应的历程和相应的活化能如表 11.5 所示。

表 11.5 ${\mathrm{H}}_{2}$ 和 ${\mathrm{{Cl}}}_{2}$ 反应的历程和相应的活化能

<table><tr><td colspan="2">反应历程</td><td> $E_{\text{a}}/(kJ \cdot mol^{-1})$ </td></tr><tr><td>(1)  $Cl_{2} + M \xrightarrow{k_{1}} 2Cl \cdot + M$ </td><td>链的开始</td><td>242</td></tr><tr><td>(2)  $Cl \cdot + H_{2} \xrightarrow{k_{2}} HCl + H \cdot$ </td><td>链的传递</td><td>24</td></tr><tr><td>(3)  $H \cdot + Cl_{2} \xrightarrow{k_{3}} HCl + Cl \cdot$ </td><td></td><td>13</td></tr><tr><td>......</td><td>......</td><td>......</td></tr><tr><td>(4)  $2Cl \cdot + M \xrightarrow{k_{4}} Cl_{2} + M$ </td><td>链的终止</td><td>0</td></tr></table>

这个反应的速率可以用 HCl 生成的速率来表示。在 (2), (3) 步中都有 HCl 分子生成, 所以

$$
\frac {\mathrm{d} [ \mathrm{HCl} ]}{\mathrm{d} t} = k _ {2} [ \mathrm{Cl} \cdot ] [ \mathrm{H} _ {2} ] + k _ {3} [ \mathrm{H} \cdot ] [ \mathrm{Cl} _ {2} ]\tag{a}
$$

这个速率方程中不但涉及反应物 $H_{2}$ 和 $Cl_{2}$ 的浓度, 而且涉及活性很大的自由基原子 $Cl\cdot$ 和 $H\cdot$ 的浓度。由于 $Cl\cdot$ 和 $H\cdot$ 等中间产物十分活泼, 它们只要碰上任何分子或其他的自由基都将立即反应, 所以在反应过程中它们的浓度很低, 并且寿命很短, 用一般的实验方法难以测定它们的浓度。同时, 在反应过程中会出现许多中间化合物和许多复杂的连续反应, 如果需严格地找出反应系统中各物种的浓度与时间的关系 (即 c-t 关系), 则需要给出许多微分方程, 然后联立求解。这是很难办到的, 即使有了高速计算机也是十分麻烦而且并非必要的。采用稳态近似法可把问题简化, 它能够以少数几个代数方程代替许多微分方程。

由于自由基等中间产物极活泼, 它们参加许多反应, 但浓度低、寿命又短, 所以可以近似地认为在反应达到稳定状态后, 它们的浓度基本上不随时间而变化, 即

$$
\frac {\mathrm{d} [ \mathrm{Cl} \cdot ]}{\mathrm{d} t} = 0 \quad \frac {\mathrm{d} [ \mathrm{H} \cdot ]}{\mathrm{d} t} = 0
$$

这样处理的方法叫作稳态近似法 (steady state approximation method, 简称 SS 近似法)。因为只有在流动的敞开系统中, 控制必要的条件, 才有可能使反应系统中各物种的浓度保持一定, 不随时间而变化。而在封闭系统中, 由于反应物浓度不断下降, 产物浓度不断增高, 要保持中间产物浓度不随时间而变化, 严格讲是不大可能的。所以, 稳态近似法只是一种近似方法, 但确能解决很多问题。

根据上述 $H_{2}$ 和 $Cl_{2}$ 反应的历程, 用稳态近似法, 得

$$
\begin{array}{r l} & {\frac {\mathrm{d} [ \mathrm{Cl} \cdot ]}{\mathrm{d} t} = 2 k _ {1} [ \mathrm{Cl} _ {2} ] [ \mathrm{M} ] - k _ {2} [ \mathrm{Cl} \cdot ] [ \mathrm{H} _ {2} ] + k _ {3} [ \mathrm{H} \cdot ] [ \mathrm{Cl} _ {2} ] - 2 k _ {4} [ \mathrm{Cl} \cdot ] ^ {2} [ \mathrm{M} ] = 0} \\ & {\frac {\mathrm{d} [ \mathrm{H} \cdot ]}{\mathrm{d} t} = k _ {2} [ \mathrm{Cl} \cdot ] [ \mathrm{H} _ {2} ] - k _ {3} [ \mathrm{H} \cdot ] [ \mathrm{Cl} _ {2} ] = 0} \end{array}\tag{b}
$$

(c)

将式 (c) 代入式 (b), 得

$$
\begin{array}{l} 2 k _ {1} [ \mathrm{Cl} _ {2} ] = 2 k _ {4} [ \mathrm{Cl} \cdot ] ^ {2} \\ [ \mathrm{Cl} \cdot ] = \left(\frac {k _ {1}}{k _ {4}} [ \mathrm{Cl} _ {2} ]\right) ^ {\frac {1}{2}} \end{array}\tag{d}
$$

将式 (c), (d) 代入式 (a), 得

$$
\frac {\mathrm{d} [ \mathrm{HCl} ]}{\mathrm{d} t} = 2 k _ {2} \left(\frac {k _ {1}}{k _ {4}}\right) ^ {\frac {1}{2}} [ \mathrm{Cl} _ {2} ] ^ {\frac {1}{2}} [ \mathrm{H} _ {2} ]
$$

所以

$$
\frac {1}{2} \frac {\mathrm{d} [ \mathrm{HCl} ]}{\mathrm{d} t} = k [ \mathrm{Cl} _ {2} ] ^ {\frac {1}{2}} [ \mathrm{H} _ {2} ]\tag{e}
$$

式中 $k = k_{2}\left(\frac{k_{1}}{k_{4}}\right)^{\frac{1}{2}}$ 。根据这个速率方程， $\mathrm{Cl}_2$ 和 $\mathrm{H}_{2}$ 的反应是1.5级反应。根据Arrhenius公式：

$$
\begin{array}{l} k _ {1} = A _ {1} \exp \left(- \frac {E _ {\mathrm{a,1}}}{R T}\right) \\ k _ {2} = A _ {2} \exp \left(- \frac {E _ {\mathrm{a,2}}}{R T}\right) \\ k _ {4} = A _ {4} \exp \left(- \frac {E _ {\mathrm{a,4}}}{R T}\right) \end{array}
$$

则

$$
\begin{array}{r l} k & = A _ {2} \left(\frac {A _ {1}}{A _ {4}}\right) ^ {\frac {1}{2}} \exp \left[ - \frac {E _ {\mathrm{a,2}} + \frac {1}{2} (E _ {\mathrm{a,1}} - E _ {\mathrm{a,4}})}{R T} \right] \\ & = A \exp \left(- \frac {E _ {\mathrm{a}}}{R T}\right) \end{array}
$$

所以, $H_{2}$ 和 $Cl_{2}$ 的总反应的表观指前因子和表观活化能分别为

$$
\begin{array}{r l} & A = A _ {2} \left(\frac {A _ {1}}{A _ {4}}\right) ^ {\frac {1}{2}} \\ & E _ {\mathrm{a}} = E _ {\mathrm{a,2}} + \frac {1}{2} \left(E _ {\mathrm{a,1}} - E _ {\mathrm{a,4}}\right) \\ & \quad = \left[ 2 4 + \frac {1}{2} \times (2 4 2 - 0) \right] \mathrm{kJ} \cdot \mathrm{mol} ^ {- 1} = 1 4 5 \mathrm{kJ} \cdot \mathrm{mol} ^ {- 1} \end{array}
$$

若 $\mathrm{H}_{2}$ 和 $\mathrm{Cl}_{2}$ 的反应是由若干个基元反应组合而成的，而不是依照链反应的方式进行，则按照 $30\%$ 规则估计其活化能约为

$$
\begin{array}{r l} E _ {\mathrm{a}} & = 0. 3 0 \left(\varepsilon_ {\mathrm{H-H}} + \varepsilon_ {\mathrm{Cl-Cl}}\right) L \\ & = 0. 3 0 \times (4 3 6 + 2 4 2) \mathrm {kJ\cdot mol^ {-1}} \\ & = 2 0 3 \mathrm {kJ\cdot mol^ {-1}} \end{array}
$$

显然反应会选择活化能较低的链反应方式进行。又由于 $\varepsilon_{Cl-Cl} < \varepsilon_{H-H}$ ，故一般链引发总是从 $Cl_{2}$ 开始而不是从 $H_{2}$ 开始。同理， $H_{2}$ 与 $Br_{2}$ 或 $H_{2}$ 与 $I_{2}$ 的反应之所以有它们自己所特有的历程，也因为按照那种历程所需的活化能最低。在反应物分子和产物分子之间往往可以存在若干不同的平行通道，而起主要作用的通道总是活化能最低而反应速率最快的捷径。

## 支链反应—— $H_{2}$ 和 $O_{2}$ 反应的历程

$H_{2}$ 和 $O_{2}$ 的混合气在一定的条件下会发生爆炸, 由于造成爆炸的原因不同, 爆炸可分为两种类型, 即热爆炸 (thermal explosion) 和支链爆炸 (branched chain explosion)。

当 $H_{2}$ 和 $O_{2}$ 发生支链反应时:

链的开始

$$
\mathrm{H} _ {2} \longrightarrow \mathrm{H} \cdot + \mathrm{H} \cdot\tag{1}
$$

直链反应

$$
\mathrm{H} \cdot + \mathrm{O} _ {2} + \mathrm{H} _ {2} \longrightarrow \mathrm{H} _ {2} \mathrm{O} + \mathrm{OH} \cdot\tag{2}
$$

$$
\mathrm{OH} \cdot + \mathrm{H} _ {2} \longrightarrow \mathrm{H} _ {2} \mathrm{O} + \mathrm{H} \cdot\tag{3}
$$

支链反应

$$
\mathrm{H} \cdot + \mathrm{O} _ {2} \longrightarrow \mathrm{OH} \cdot + \mathrm{O} \cdot\tag{4}
$$

$$
\mathrm{O} \cdot + \mathrm{H} _ {2} \longrightarrow \mathrm{OH} \cdot + \mathrm{H} \cdot\tag{5}
$$

链在气相中的中断

$$
2 \mathrm{H} \cdot + \mathrm{M} \longrightarrow \mathrm{H} _ {2} + \mathrm{M}\tag{6}
$$

$$
\mathrm{OH} \cdot + \mathrm{H} \cdot + \mathrm{M} \longrightarrow \mathrm{H} _ {2} \mathrm{O} + \mathrm{M}\tag{7}
$$

$$
\mathrm{链在器壁上的中断} \quad \mathrm{H} \cdot + \mathrm{器壁} \longrightarrow \mathrm{销毁}\tag{8}
$$

$$
\mathrm{OH} \cdot + \text { 器壁 } \longrightarrow \text { 销毁 }\tag{9}
$$

在支链反应中若每一个自由原子参加反应后可以产生两个自由原子（如图 11.9 所示），而由于这些自由原子又可以再参加直链反应或支链反应，所以反应的速率迅速加快，最后可以达到支链爆炸的程度。

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_200-399_images/98602a7a2aab590d6c27feac27bcc362a18e8d50697d135c256ada4e622fbec4.jpg)  
图11.9 支链反应

当一个放热反应在无法散热的情况下进行时, 反应热使反应系统的温度猛烈上升, 而温度又使这个放热反应的速率按指数规律加快, 放出的热量也跟着增多, 这样的循环很快使反应速率几乎毫无止境地加快, 最后就会发生爆炸。这样发生的爆炸就是热爆炸。

爆炸反应通常都有一定的爆炸区, 当反应达到燃烧或爆炸的压力范围时, 反应的速率由平稳而突然加快。图 11.10 是氢氧混合系统的爆炸界限与温度、压力的关系。

当总压力低于 $p_1$ [见图11.10(a)]时，即 $AB$ 段，反应进行得平稳。当压力在 $p_1$ 至 $p_2$ 之间时，反应的速率很快，自动地加速，发生爆炸或燃烧。当压力超过 $p_2$ ，一直到 $p_3$ 的阶段，即 $CD$ 段，反应速率反而减慢。当压力超过 $p_3$ 时，又发生爆炸。

上述系统中两个压力限与温度的关系, 可用图 11.10(b) 来表示。图中 ab 为低爆炸界限, bc 为高爆炸界限, cd 代表第三爆炸界限。第三爆炸界限以上的爆炸是热爆炸 (对于 $H_{2}$ 和 $O_{2}$ 的反应来说, 存在 cd 线。但是否所有的爆炸反应都有

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_200-399_images/adff3d20e0f9cd0c28515e3e40f5f8d9b2c448a8dc259dd6a3c785cb89781a93.jpg)  
(a)

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_200-399_images/5a4900a227eda1090319d40da66d0eb3b7128c7905113c1e81c5a34e6366a4c5.jpg)  
(b)  
图 11.10 氢氧混合系统的爆炸界限与温度、压力的关系

第三爆炸界限, 则尚不能肯定)。

发生上述现象是因为在反应中有链发展和链中断步骤。若链中断的概率大, 则链发展就不会很快。在压力很低时, 系统中自由原子很容易扩散到容器壁上而销毁, 因此减少了链的传递者, 反应不会进行得太快。当压力逐渐增大后, 在容器中分子有效的碰撞次数增加, 因此链的发展速率大大增加, 直至发生爆炸。当压力超过 $p_{2}$ 时, 反应反而变慢, 这是因为系统内分子的浓度增加, 容易发生三分子的碰撞而使自由原子消失。例如:

$$
\begin{array}{l} \mathrm {O\cdot + O\cdot + M\longrightarrow O_ {2} + M} \\ \mathrm {O\cdot + O_ {2} + M\longrightarrow O_ {3} + M} \end{array}
$$

很多可燃气体都有一定的爆炸界限。表 11.6 列出了在常温常压下一些可燃气体在空气中的爆炸界限, 因此在使用这些气体时应十分注意。为避免发生爆炸,在化工生产过程中常在反应器的适当位置上, 安装带有化学传感器的警报设备, 可随时告知或自动记录反应系统中易爆物的成分、压力等参数, 以避免发生事故。

表 11.6 常温常压下一些可燃气体在空气中的爆炸界限 (用体积分数 ${\varphi }_{\mathrm{B}}$ 表示)

<table><tr><td>可燃气体</td><td>爆炸界限  $\varphi_{B}$ </td><td>可燃气体</td><td>爆炸界限  $\varphi_{B}$ </td></tr><tr><td> $H_{2}$ </td><td>0.04 ~ 0.742*</td><td>CO</td><td>0.125 ~ 0.742*</td></tr><tr><td> $NH_{3}$ </td><td>0.155 ~ 0.27*</td><td> $CH_{4}$ </td><td>0.05 ~ 0.15</td></tr><tr><td> $CS_{2}$ </td><td>0.119 ~ 0.285*</td><td> $C_{2}H_{6}$ </td><td>0.03 ~ 0.155</td></tr><tr><td> $C_{2}H_{4}$ </td><td>0.027 ~ 0.36</td><td> $C_{6}H_{6}$ </td><td>0.013 ~ 0.071</td></tr><tr><td> $C_{2}H_{2}$ </td><td>0.025 ~ 1.0</td><td> $CH_{3}OH$ </td><td>0.067 ~ 0.36</td></tr><tr><td> $C_{3}H_{8}$ </td><td>0.021 ~ 0.095</td><td> $C_{2}H_{5}OH$ </td><td>0.033 ~ 0.19</td></tr><tr><td> $C_{4}H_{10}$ </td><td>0.019 ~ 0.085</td><td> $(C_{2}H_{5})_{2}O$ </td><td>0.017 ~ 0.49*</td></tr><tr><td> $C_{5}H_{12}$ </td><td>0.014 ~ 0.078</td><td> $CH_{3}COOC_{2}H_{5}$ </td><td>0.022 ~ 0.11</td></tr></table>

注: 本表数据摘自《石油化工可燃气体和有毒气体检测报警设计标准》(GB 50493—2019)。其中标注 \* 的数据摘自 Jame G Speight. Lange's Handbook of Chemistry. 17th ed. New York: MCGraw-Hill Education, 2017: Table 1.14.

## \*11.10 拟定反应历程的一般方法

今以石油裂解中一个重要反应——乙烷热分解的反应历程为例，说明确定反应历程（机理）的一般过程。

乙烷热分解发生在 $823 \sim 923$ K, 由实验室测得其主要产物是氢和乙烯（此外还有少量的甲烷), 反应方程式可以写为

$$
\mathrm{C} _ {2} \mathrm{H} _ {6} (\mathrm{g}) \longrightarrow \mathrm{C} _ {2} \mathrm{H} _ {4} (\mathrm{g}) + \mathrm{H} _ {2} (\mathrm{g})
$$

实验得出, 在较高的压力下, 它是一级反应, 其反应速率方程式为

$$
- \frac {\mathrm{d} [ \mathrm{C} _ {2} \mathrm{H} _ {6} ]}{\mathrm{d} t} = k [ \mathrm{C} _ {2} \mathrm{H} _ {6} ]
$$

由实验测得反应的活化能为 $284.5 \, kJ \cdot mol^{-1}$ 左右, 根据质谱仪 (mass spectrometer) 和其他实验技术证明, 在乙烷的热分解过程中有自由基 $\cdot CH_{3}$ 和 $\cdot C_{2}H_{5}$ 生成。根据这些实验事实, 有人认为该反应是按下列的链反应机理进行的:

$$
\begin{array}{l l} \text {(1) C} _ {2} \mathrm{H} _ {6} \xrightarrow {k _ {1}} 2 \cdot \mathrm{CH} _ {3} & E _ {1} = 3 5 1. 5 \mathrm{kJ} \cdot \mathrm{mol} ^ {- 1} \\ \text {(2) } \cdot \mathrm{CH} _ {3} + \mathrm{C} _ {2} \mathrm{H} _ {6} \xrightarrow {k _ {2}} \mathrm{CH} _ {4} + \cdot \mathrm{C} _ {2} \mathrm{H} _ {5} & E _ {2} = 3 3. 5 \mathrm{kJ} \cdot \mathrm{mol} ^ {- 1} \\ \text {(3) } \cdot \mathrm{C} _ {2} \mathrm{H} _ {5} \xrightarrow {k _ {3}} \mathrm{C} _ {2} \mathrm{H} _ {4} + \mathrm{H} \cdot & E _ {3} = 1 6 7 \mathrm{kJ} \cdot \mathrm{mol} ^ {- 1} \\ \text {(4) H} \cdot + \mathrm{C} _ {2} \mathrm{H} _ {6} \xrightarrow {k _ {4}} \mathrm{H} _ {2} + \cdot \mathrm{C} _ {2} \mathrm{H} _ {5} & E _ {4} = 2 9. 3 \mathrm{kJ} \cdot \mathrm{mol} ^ {- 1} \\ \text {(5) H} \cdot + \cdot \mathrm{C} _ {2} \mathrm{H} _ {5} \xrightarrow {k _ {5}} \mathrm{C} _ {2} \mathrm{H} _ {6} & E _ {5} = 0 \mathrm{kJ} \cdot \mathrm{mol} ^ {- 1} \end{array}
$$

在反应中，(1) 是链的开始，(2)，(3)，(4) 是链的传递，(5) 是链的终止。

上述乙烷热分解的链反应机理是否正确还需要予以检验。首先必须按上述反应机理找出反应速率和反应物浓度的关系，检验其是否与实验结果一致，还要根据各基元反应的活化能来估算总的活化能，看所得到的活化能是否和实验值相符。此外，如果还有其他实验事实，则所提出的机理也应能给予说明。

根据上述机理, 反应的速率为

$$
- \frac {\mathrm{d} [ \mathrm{C} _ {2} \mathrm{H} _ {6} ]}{\mathrm{d} t} = k _ {1} [ \mathrm{C} _ {2} \mathrm{H} _ {6} ] + k _ {2} [ \cdot \mathrm{CH} _ {3} ] [ \mathrm{C} _ {2} \mathrm{H} _ {6} ] + k _ {4} [ \mathrm{C} _ {2} \mathrm{H} _ {6} ] [ \mathrm{H} \cdot ] - k _ {5} [ \mathrm{H} \cdot ] [ \cdot \mathrm{C} _ {2} \mathrm{H} _ {5} ]\tag{a}
$$

上式中各个自由基的浓度 $[\cdot CH_{3}]$ , $[H\cdot]$ , $[\cdot C_{2}H_{5}]$ 在反应过程中很难直接测定, 可以通过稳态近似法求出它们与反应物浓度 $[C_{2}H_{6}]$ 之间的关系。

$$
\frac {\mathrm{d} [ \cdot \mathrm{CH} _ {3} ]}{\mathrm{d} t} = 2 k _ {1} [ \mathrm{C} _ {2} \mathrm{H} _ {6} ] - k _ {2} [ \mathrm{C} _ {2} \mathrm{H} _ {6} ] [ \cdot \mathrm{CH} _ {3} ] = 0\tag{b}
$$

$$
\frac {\mathrm{d} \left[ \cdot \mathrm{C} _ {2} \mathrm{H} _ {5} \right]}{\mathrm{d} t} = k _ {2} \left[ \cdot \mathrm{CH} _ {3} \right] \left[ \mathrm{C} _ {2} \mathrm{H} _ {6} \right] - k _ {3} \left[ \cdot \mathrm{C} _ {2} \mathrm{H} _ {5} \right] +
$$

$$
k _ {4} \left[ \mathrm{H} \cdot \right] \left[ \mathrm{C} _ {2} \mathrm{H} _ {6} \right] - k _ {5} \left[ \mathrm{H} \cdot \right] \left[ \cdot \mathrm{C} _ {2} \mathrm{H} _ {5} \right] = 0\tag{c}
$$

$$
\frac {\mathrm{d} [ \mathrm{H} \cdot ]}{\mathrm{d} t} = k _ {3} [ \cdot \mathrm{C} _ {2} \mathrm{H} _ {5} ] - k _ {4} [ \mathrm{H} \cdot ] [ \mathrm{C} _ {2} \mathrm{H} _ {6} ] - k _ {5} [ \mathrm{H} \cdot ] [ \cdot \mathrm{C} _ {2} \mathrm{H} _ {5} ] = 0\tag{d}
$$

以上三式相加, 得

$$
2 k _ {1} \left[ \mathrm{C} _ {2} \mathrm{H} _ {6} \right] - 2 k _ {5} \left[ \mathrm{H} \cdot \right] \left[ \cdot \mathrm{C} _ {2} \mathrm{H} _ {5} \right] = 0
$$

所以

$$
[ \mathrm{H} \cdot ] = \left(\frac {k _ {1}}{k _ {5}}\right) \frac {[ \mathrm{C} _ {2} \mathrm{H} _ {6} ]}{[ \cdot \mathrm{C} _ {2} \mathrm{H} _ {5} ]}\tag{e}
$$

从式 (b) 可得

$$
[ \cdot \mathrm{CH} _ {3} ] = \frac {2 k _ {1}}{k _ {2}}\tag{f}
$$

把式 (e) 代入式 (d), 得

$$
[ \cdot \mathrm{C} _ {2} \mathrm{H} _ {5} ] ^ {2} - \left(\frac {k _ {1}}{k _ {3}}\right) [ \mathrm{C} _ {2} \mathrm{H} _ {6} ] [ \cdot \mathrm{C} _ {2} \mathrm{H} _ {5} ] - \left(\frac {k _ {1} k _ {4}}{k _ {3} k _ {5}}\right) [ \mathrm{C} _ {2} \mathrm{H} _ {6} ] ^ {2} = 0
$$

这是一个以 $\left[\cdot C_{2}H_{5}\right]$ 为变数的一元二次方程式, 其解为

$$
[ \cdot \mathrm{C} _ {2} \mathrm{H} _ {5} ] = [ \mathrm{C} _ {2} \mathrm{H} _ {6} ] \left[ \frac {k _ {1}}{2 k _ {3}} \pm \sqrt {\left(\frac {k _ {1}}{2 k _ {3}}\right) ^ {2} + \frac {k _ {1} k _ {4}}{k _ {3} k _ {5}}} \right]
$$

$k_{1}$ 是链引发步骤的速率常数, 一般不是很大, 可略去不计。同时, 负值为不合理解, 也不予考虑。所以, 上式可简化为

$$
[ \cdot \mathrm{C} _ {2} \mathrm{H} _ {5} ] = \left(\frac {k _ {1} k _ {4}}{k _ {3} k _ {5}}\right) ^ {\frac {1}{2}} [ \mathrm{C} _ {2} \mathrm{H} _ {6} ]\tag{g}
$$

再代入式 (e), 得

$$
[ \mathrm{H} \cdot ] = \left(\frac {k _ {1} k _ {3}}{k _ {4} k _ {5}}\right) ^ {\frac {1}{2}}\tag{h}
$$

将式 (f), (g), (h) 代入式 (a), 整理后得

$$
- \frac {\mathrm{d} [ \mathrm{C} _ {2} \mathrm{H} _ {6} ]}{\mathrm{d} t} = \left[ 2 k _ {1} + \left(\frac {k _ {1} k _ {3} k _ {4}}{k _ {5}}\right) ^ {\frac {1}{2}} \right] [ \mathrm{C} _ {2} \mathrm{H} _ {6} ]
$$

在括号中, 相对说可以略去 $2k_{1}$ , 故得

$$
- \frac {\mathrm{d} [ \mathrm{C} _ {2} \mathrm{H} _ {6} ]}{\mathrm{d} t} = \left(\frac {k _ {1} k _ {3} k _ {4}}{k _ {5}}\right) ^ {\frac {1}{2}} [ \mathrm{C} _ {2} \mathrm{H} _ {6} ] = k [ \mathrm{C} _ {2} \mathrm{H} _ {6} ]\tag{i}
$$

即反应对 $\left[\mathrm{C}_{2} \mathrm{H}_{6}\right]$ 为一级。由于反应的活化能越大, 速率常数越小。基元反应 (1) 的活化能比其他几个基元反应的活化能都大, 故相对来说略去 $2k_{1}$ 及高次方项, 不致引入很大的误差。

由此可见, 按照上述反应机理导出的反应速率方程式, 即式 (i), 说明此反应是一个一级反应, 与实验所得结果基本上是一致的。

再看如何由基元反应的活化能来估计总的活化能。在式 (i) 中:

$$
k = \left(\frac {k _ {1} k _ {3} k _ {4}}{k _ {5}}\right) ^ {\frac {1}{2}}
$$

根据速率常数与温度的关系, $k = A \exp \left( -\frac{E_{\mathrm{a}}}{RT} \right)$ , 可以得出

$$
A \exp \left(- \frac {E _ {\mathrm{a}}}{R T}\right) = \left(\frac {A _ {1} A _ {3} A _ {4}}{A _ {5}}\right) ^ {\frac {1}{2}} \exp \left[ - \frac {1}{2} \left(\frac {E _ {1} + E _ {3} + E _ {4} - E _ {5}}{R T}\right) \right]
$$

$$
\begin{array}{r l} E _ {\mathrm{a}} & = \frac {1}{2} (E _ {1} + E _ {3} + E _ {4} - E _ {5}) \\ & = \frac {1}{2} \times (3 5 1. 5 + 1 6 7 + 2 9. 3 - 0) \mathrm{kJ} \cdot \mathrm{mol} ^ {- 1} \\ & = 2 7 4 \mathrm{kJ} \cdot \mathrm{mol} ^ {- 1} \end{array}
$$

这个数值与实验直接测得的表观活化能 $284.5\mathrm{kJ}\cdot \mathrm{mol}^{-1}$ 也是接近的。

由于反应级数和活化能的数值都基本上与实验结果大致相符, 这表明上述机理在实验的条件下基本上是合理的。关于乙烷的热分解反应有不少人进行过研究, 在较低的压力和较高的温度下, 实验测得反应为 2/3 级, 这主要是因为当反应的条件不同时, 链终止的步骤有所不同。

在处理复杂反应的历程时, 除了稳态近似法以外, 还有速控步近似和平衡假设两种方法。适当采用可以免去解复杂的联立微分方程, 使稳态近似不致引入很大误差。

在一系列的连续反应中, 若其中有一步反应的速率最慢, 它控制了总反应的速率, 使反应的速率基本等于最慢一步的速率, 则这最慢的一步反应称为速控步 (rate controlling step) 或决速步 (rate determining step)。

例如, 有反应

$$
\mathrm{H} ^ {+} + \mathrm{HNO} _ {2} + \mathrm{C} _ {6} \mathrm{H} _ {5} \mathrm{NH} _ {2} \xrightarrow {\mathrm{Br} ^ {-} (\mathrm{催化剂})} \mathrm{C} _ {6} \mathrm{H} _ {5} \mathrm{N} _ {2} ^ {+} + 2 \mathrm{H} _ {2} \mathrm{O}
$$

实验得出的速率方程为

$$
r = k [ \mathrm{H} ^ {+} ] [ \mathrm{HNO} _ {2} ] [ \mathrm{Br} ^ {-} ]
$$

而 $\left[C_{6}H_{5}NH_{2}\right]$ 对反应速率无影响, 未出现在速率方程式中。因此, 该反应的可能历程是

$$
\begin{array}{l l}{(1) \mathrm {H^ {+} + HNO_ {2} \underset {k _ {- 1}} {\overset {k _ {1}} {\rightleftharpoons}} H_ {2} NO_ {2} ^ {+}}}&{\text {快速平衡}}\\{(2) \mathrm {H_ {2} NO_ {2} ^ {+} + Br^ {-} \xrightarrow {k_ {2}} ONBr+ H_ {2} O}}&{\text {慢}}\\{(3) \mathrm {ONBr+ C_ {6} H_ {5} NH_ {2} \xrightarrow {k_ {3}} C_ {6} H_ {5} N_ {2} ^ {+} + H_ {2} O+ Br^ {-}}}&{\text {快}}\end{array}
$$

第(2)步是总反应的速控步, 因此总反应的速率为

$$
r = k _ {2} [ \mathrm{H} _ {2} \mathrm{NO} _ {2} ^ {+} ] [ \mathrm{Br} ^ {-} ]
$$

中间产物的浓度 $\left[H_{2}NO_{2}^{+}\right]$ 可从快速平衡反应 (1) 中求得:

$$
\left[ \mathrm{H} _ {2} \mathrm{NO} _ {2} ^ {+} \right] = \frac {k _ {1}}{k _ {- 1}} [ \mathrm{H} ^ {+} ] [ \mathrm{HNO} _ {2} ] = K [ \mathrm{H} ^ {+} ] [ \mathrm{HNO} _ {2} ]
$$

代入总反应速率方程, 得

$$
r = \frac {k _ {1} k _ {2}}{k _ {- 1}} [ \mathrm{H} ^ {+} ] [ \mathrm{HNO} _ {2} ] [ \mathrm{Br} ^ {-} ] = k [ \mathrm{H} ^ {+} ] [ \mathrm{HNO} _ {2} ] [ \mathrm{Br} ^ {-} ]
$$

这与实验结果一致。表观速率常数 $k=\frac{k_{1}k_{2}}{k_{-1}}$ ，不包括速控步以下的快反应的速率常数 $k_{3}$ ，但包括了速控步及以前所有反应的速率常数。由于反应物 $C_{6}H_{5}NH_{2}$ 是出现在速控步以后的快反应中，所以它的浓度对总反应基本无影响，故不出现在速率方程中。

从上例中可以看到, 在一个含有对峙反应的连续反应中, 如果存在速控步, 则总反应速率及表观速率常数仅取决于速控步及其以前的平衡过程, 与速控步以后的各快反应无关。另外, 因速控步反应很慢, 假定快速平衡反应不受其影响, 各正、逆反应间的平衡关系仍然存在, 则可以利用平衡常数 K 及反应物浓度求出中间产物的浓度, 这种处理方法称为平衡假设 (equilibrium hypothesis)。之所以称为假设是因为在化学反应进行的系统中, 完全平衡是达不到的, 这也仅是一种近似的处理方法。

设某总反应为 $A + B \longrightarrow P$ ，总反应速率用 $r = \frac{d[P]}{dt}$ 表示，其一种反应历程为

$$
\mathrm{A} \xrightarrow [ k _ {- 1} ]{k _ {1}} \mathrm{C}\tag{i}
$$

$$
\mathrm{C} + \mathrm{B} \xrightarrow {k _ {2}} \mathrm{P}\tag{ii}
$$

则 $r = \frac{\mathrm{d}[\mathrm{P}]}{\mathrm{d}t} = k_2[\mathrm{C}][\mathrm{B}]$ 。究竟用何种近似方法来消去中间产物的浓度项[C]，则要视具体情况而定，也就是说稳态近似法、速控步及平衡假设的使用是有一定的前提的。

(1) 如果 $k_{-1} + k_{2}[B] \gg k_{1}$ ，中间产物 C 一旦产生，马上会被消耗掉，这时可以对中间产物 C 作稳态近似：

$$
\frac {\mathrm{d} [ \mathrm{C} ]}{\mathrm{d} t} = k _ {1} [ \mathrm{A} ] - k _ {- 1} [ \mathrm{C} ] - k _ {2} [ \mathrm{B} ] [ \mathrm{C} ] = 0\tag{a}
$$

$$
[ \mathrm{C} ] = \frac {k _ {1} [ \mathrm{A} ]}{k _ {- 1} + k _ {2} [ \mathrm{B} ]}\tag{b}
$$

$$
r = \frac {k _ {1} k _ {2} [ \mathrm{A} ] [ \mathrm{B} ]}{k _ {- 1} + k _ {2} [ \mathrm{B} ]}\tag{c}
$$

如果 $k_{-1} \ll k_2[\mathrm{B}]$ , 则 $k_{-1} + k_2[\mathrm{B}] \approx k_2[\mathrm{B}]$ , 则总速率为

$$
r = k _ {1} [ \mathrm{A} ]\tag{d}
$$

因这时反应 (i) 是速控步, 反应物 B 参加速控步后面的快反应, 因此不影响反应速率。

(2) 如果 $k_{-1} \gg k_{2}[B]$ ，这时反应 (ii) 为速控步。要反应 (i) 的平衡能维持，还需要 $k_{-1} \gg k_{1}$ ，使平衡能很快建立，这时才能用平衡假设。当 (i) 处于平衡时 [根据式 (b)，略去 $k_{2}[B]$ 项]，得

$$
[ \mathrm{C} ] = \frac {k _ {1}}{k _ {- 1}} [ \mathrm{A} ] = K [ \mathrm{A} ]\tag{e}
$$

则

$$
r = \frac {k _ {1} k _ {2}}{k _ {- 1}} [ \mathrm{A} ] [ \mathrm{B} ]\tag{f}
$$

对照式 (c), 只有在 $k_{-1} \gg k_2[\mathrm{B}]$ 时, 两式基本相等。所以, 使用平衡假设是有条件的, 只有第一个平衡是快速平衡, 第二步是慢反应, 作为速控步, 这时才可以采用平衡假设这一近似方法。

有了以上三种近似处理方法, 在推导复杂反应的速率方程时就要简便得多了。

化学反应的反应机理并不是凭空想象出来的, 也不是先有一套假设再逐步验证的, 而是要首先掌握足够的实验数据, 从实验中找出反应速率与浓度的关系、活化能, 以及判断在分解过程中是否有自由基存在等, 然后根据这些事实来考虑其历程。而所设想的历程即使在理论上符合逻辑, 也必须经过实验的检验, 整个过程就是实践、认识、再实践、再认识的过程。只有这样循环往复，逐步深入，才可能得出一个正确的结论，这就是辩证唯物主义的认识过程。

一般说来, 拟定反应机理大致要经过下列几个步骤:

(1) 初步的观察和分析 根据对反应系统所观察到的现象, 初步了解反应是复相还是均相反应, 反应是否受光的影响; 注意反应过程中有无颜色的改变, 有无热量放出, 有无副产物生成, 以及其他可能观察到的现象。根据对现象的分析, 再有计划地进行系统性实验。

(2) 收集定量的数据 ① 测定反应速率与各个反应物浓度的关系, 确定反应的总级数。② 测定反应速率与温度的关系, 确定反应的活化能。③ 测定有无逆反应或其他可能的复杂反应, 反应过程中的主反应是什么? 副反应又是什么? ④ 中间产物的寿命可能很短, 数量也可能不多, 因此对它们的检验常常必须用特殊的方法 (如用淬冷法或原位磁共振谱、色谱-质谱联合谱仪、闪光光解等测试手段)。但是, 一旦检验出有某种中间产物存在, 则对于反应机理的确定往往起着很重要的作用。 $O_{2}$ , $Cl_{2}O$ , NO 等具有未成对的电子, 易于捕获自由基。在反应系统中加入这些物质, 观察反应速率是否下降, 以判断系统中是否有自由基存在。而自由基的存在常能导致链反应。

可以有计划地设计实验, 用各种物理的或化学的测试手段来检验中间产物。

(3) 拟定反应机理 根据所观察到的事实和收集到的数据, 提出可能的反应步骤, 然后逐步排除那些与活化能大小不相符的反应步骤或与事实有抵触的反应步骤。对所提出的机理必须进行多方面的考验。除了根据反应级数、速率方程式、活化能考验之外, 还可以按具体情况进行具体分析。例如, 可用同位素来判别机理, 也可以根据对物质结构已有的常识来判断。如能就机理中的中间步骤单独进行实验, 则更为有效。整个机理的速率方程式应经过逐步检验, 必须与观测到的全部实验事实一致, 这个反应机理才能初步确定下来。通过对势能面的量化计算, 也可以了解反应过程中最可能经过的途径等 (但势能面的计算是相当复杂的问题)。

如果发现有新的实验事实, 则所提出的反应机理必须能够说明新的实验事实, 否则必须对反应机理进行修正或者重新考虑。

以上提到的只是拟定反应机理的一般过程, 并不是对任何一个反应所有的研究步骤都必须用到, 也可能还有其他研究步骤需要补充, 这完全要对具体问题做具体分析并从整体上综合考虑。

## 拓展学习资源

<table><tr><td>重点内容及公式总结</td><td><img src="images/94449b792b37533ea33c5025f8a957ede60cea37f57f9c46faf7044a63478122.jpg"/></td></tr><tr><td>课外参考读物</td><td><img src="images/620792de1f17a45e831f0905658e83f9de00e20a89a63917ff1725b47bf163c1.jpg"/></td></tr><tr><td>相关科学家简介</td><td><img src="images/9bc9ccb5597d696e61992dbc3d0a819f551ae709b631d59bf0586b59cdd59803.jpg"/></td></tr><tr><td>教学课件</td><td><img src="images/276926fff04784b43986e2ec73337c6de6901591de78439a69ce83d68f2d5f99.jpg"/></td></tr></table>

## 复习题

11.1 根据质量作用定律, 写出下列基元反应的反应速率表示式 (试用各种物质分别表示)。

(1) $\mathrm{A} + \mathrm{B} = 2\mathrm{P}$

(2) $2\mathrm{A} + \mathrm{B} = 2\mathrm{P}$

(3) $\mathrm{A} + 2\mathrm{B} = \mathrm{P} + 2\mathrm{S}$

(4) $2\mathrm{Cl} + \mathrm{M} = \mathrm{Cl}_2 + \mathrm{M}$

11.2 零级反应是否是基元反应？具有简单级数的反应是否一定是基元反应？反应 $\mathrm{Pb}(\mathrm{C}_{2}\mathrm{H}_{5})_{4}=\mathrm{Pb}+4\mathrm{C}_{2}\mathrm{H}_{5}$ 是否可能为基元反应？

11.3 在气相反应动力学中,往往可以用压力来代替浓度,若反应 $aA \longrightarrow P$ 为 n 级反应, 当 $k_{p}$ 是以压力表示的反应速率常数, $p_{A}$ 是 A 的分压, 所有气体可看作理想气体时, 试证明: $k_{p} = k_{c}(RT)^{1-n}$ 。

11.4 对于一级反应, 列式表示当反应物反应掉 $\frac{1}{n}$ 所需要的时间 t。试证明一级反应的转化率分别达到 50%, 75%, 87.5% 时所需的时间分别为 $t_{1/2}$ , $2t_{1/2}$ ,

$3t_{1/2}\circ$

11.5 对于反应 A $\longrightarrow$ P, 若 A 反应掉 $\frac{3}{4}$ 所需时间为 A 反应掉 $\frac{1}{2}$ 所需时间的 3 倍, 该反应是几级反应? 若 A 反应掉 $\frac{3}{4}$ 所需时间为 A 反应掉 $\frac{1}{2}$ 所需时间的 5 倍, 该反应又是几级反应? 试用计算式说明。

11.6 某一反应进行完全所需时间是有限的, 且等于 $\frac{c_0}{k}$ ( $c_0$ 为反应物起始浓度), 则该反应是几级反应?

11.7 零级反应、一级反应和二级反应各有哪些特征？平行反应、对峙反应和连续反应又有哪些特征？

11.8 某总包反应速率常数 $k$ 与各基元反应速率常数的关系为 $k = k_{2}\left(\frac{k_{1}}{2k_{4}}\right)^{\frac{1}{2}}$ 则该反应的表观活化能 $E_{\mathrm{a}}$ 和指前因子与各基元反应活化能和指前因子的关系如何？

11.9 某定容基元反应的热效应为 $100 \, kJ \cdot mol^{-1}$ ，则该正反应的实验活化能 $E_{a}$ 值将大于、等于还是小于 $100 \, kJ \cdot mol^{-1}$ ？或是不能确定？如果反应热效应为 $-100 \, kJ \cdot mol^{-1}$ ，则 $E_{a}$ 值又将如何？

11.10 某反应的 $E_{a}$ 值为 $190 \, kJ \cdot mol^{-1}$ ，加入催化剂后活化能降为 $136 \, kJ \cdot mol^{-1}$ 。设加入催化剂前后指前因子 A 值保持不变，则在 $773 \, K$ 时，加入催化剂后反应的速率常数是原来的多少倍？

11.11 根据 van't Hoff 经验规则: 温度每升高 10 K, 反应速率增加到原来的 2～4 倍, 则在 298～308 K 温度区间内, 服从此规则的化学反应的活化能 $E_{a}$ 值的范围为多少? 为什么有的反应温度升高, 反应速率反而下降?

11.12 某温度时, 有一气相一级反应 A(g) $\longrightarrow$ 2B(g) + C(g), 在恒温恒容下进行。设反应开始时, 各物质的浓度分别为 a, b, c, 气体总压力为 $p_{0}$ , 经 t 时间及当 A 完全分解时的总压力分别为 $p_{t}$ 和 $p_{\infty}$ , 试证明该分解反应的速率常数为

$$
k = \frac {1}{t} \ln \frac {p _ {\infty} - p _ {0}}{p _ {\infty} - p _ {t}}
$$

11.13 已知平行反应 A $\xrightarrow{E_{a,1}}$ B 和 A $\xrightarrow{E_{a,2}}$ C, 且 $E_{a,1} > E_{a,2}$ , 为提高 B 的产量, 应采取什么措施?

11.14 从反应机理推导速率方程时通常有哪几种近似方法？各有什么适用条件？

习题

11.1 有反应 A $\longrightarrow$ P, 实验测得是 $\frac{1}{2}$ 级反应, 试证明:

(1) $[\mathrm{A}]_0^{1 / 2} - [\mathrm{A}]^{1 / 2} = \frac{1}{2} kt;$

(2) $t_{1 / 2} = \frac{\sqrt{2}}{k}\left[\sqrt{2} -1\right]\left[\mathrm{A}\right]_{0}^{1 / 2}$

11.2 一级反应和二级反应极难由反应百分数对时间图的形状来分辨, 对于半衰期相等的一级反应、二级反应 (两种反应物起始浓度相等), 当 $t = \frac{1}{2} t_{1/2}$ 时, 求两者未反应的百分数。

11.3 蔗糖在稀酸溶液中按下式水解:

$$
\mathrm{C} _ {1 2} \mathrm{H} _ {2 2} \mathrm{O} _ {1 1} (\text {蔗糖}) + \mathrm{H} _ {2} \mathrm{O} = \mathrm{C} _ {6} \mathrm{H} _ {1 2} \mathrm{O} _ {6} (\text {葡萄糖}) + \mathrm{C} _ {6} \mathrm{H} _ {1 2} \mathrm{O} _ {6} (\text {果糖})
$$

当温度和酸的浓度一定时, 已知反应的速率与蔗糖的浓度成正比。今有某一溶液, 蔗糖和 HCl 的浓度分别为 $0.3 \, mol \cdot dm^{-3}$ 和 $0.01 \, mol \cdot dm^{-3}$ , 在 $48^{\circ}C$ 下, 20 min 内有 32% 的蔗糖水解 (由旋光仪测定旋光度而推知)。已知该反应为一级反应。

(1) 计算反应的速率常数 k 和反应开始时及反应 20 min 时的反应速率。

(2) 计算 40 min 时, 蔗糖的水解速率。

11.4 在 298 K 时, 用旋光仪测定蔗糖的转化速率, 在不同时间所测得的旋光度 $\alpha_{t}$ 如下:

<table><tr><td>t/min</td><td>0</td><td>10</td><td>20</td><td>40</td><td>80</td><td>180</td><td>300</td><td>∞</td></tr><tr><td> $\alpha_t/(^\circ)$ </td><td>6.60</td><td>6.17</td><td>5.79</td><td>5.00</td><td>3.71</td><td>1.40</td><td>-0.24</td><td>-1.98</td></tr></table>

试求该反应的速率常数 k 值。

11.5 一个二级反应, 其反应式为 $2\mathrm{A} + 3\mathrm{B} \longrightarrow \mathrm{P}$ , 求反应速率常数的积分表达式。已知 $298\mathrm{K}$ 时, $k = 2.00 \times 10^{-4}\mathrm{dm}^3 \cdot \mathrm{mol}^{-1} \cdot \mathrm{s}^{-1}$ , 开始时反应混合物中 A 的摩尔分数为 $20\%$ , B 的摩尔分数为 $80\%$ , $p_0 = 202.65\mathrm{kPa}$ , 计算 $1\mathrm{h}$ 后 A, B 各反应了多少。

11.6 在 298 K 时, 测定乙酸乙酯皂化反应速率。反应开始时, 溶液中酯与碱的浓度均为 $0.01 \, mol \cdot dm^{-3}$ , 每隔一定时间, 用标准酸溶液滴定其中碱的含量, 实验所得结果如下:

<table><tr><td>t/min</td><td>3</td><td>5</td><td>7</td><td>10</td><td>15</td><td>21</td><td>25</td></tr><tr><td> $[OH^{-}]/(10^{-3} \text{ mol } \cdot \text{ dm}^{-3})$ </td><td>7.40</td><td>6.34</td><td>5.50</td><td>4.64</td><td>3.63</td><td>2.88</td><td>2.54</td></tr></table>

(1) 证明该反应为二级反应, 并求出速率常数 k 值;

(2) 若酯与碱的浓度均为 $0.002 \, mol \cdot dm^{-3}$ ，试计算该反应完成 95% 时所需的时间及该反应的半衰期。

11.7 含有相同物质的量的 A, B 溶液, 等体积相混合, 发生反应 A+B $\longrightarrow$ C, 在反应经过 1.0 h 后, A 已消耗了 75%; 当反应时间为 2.0 h 时, 在下列情况下, A 还有多少未反应?

(1) 该反应对 A 为一级, 对 B 为零级;

(2) 该反应对 A, B 均为一级;

(3) 该反应对 A, B 均为零级。

11.8 气相基元反应 $2\mathrm{A(g)} \longrightarrow \mathrm{B(g)}$ 在恒温为 500 K 的恒容反应器中进行, 其反应速率可表示为 $-\frac{\mathrm{dc}_{\mathrm{A}}}{\mathrm{dt}} = k_{c}[\mathrm{A}]^{2}$ , 也可表示为 $-\frac{\mathrm{dp}_{\mathrm{A}}}{\mathrm{dt}} = k_{p}p_{\mathrm{A}}^{2}$ 。已知 $k_{c} = 8.205 \times 10^{-3} \, dm^{3} \cdot (\mathrm{mol} \cdot \mathrm{s})^{-1}$ , 求 $k_{p}$ (压力单位为 Pa)。

11.9 反应 A $\longrightarrow$ 2B 在恒容反应器中进行, 反应温度为 373 K, 实验测得系统总压数据如下:

<table><tr><td>t/s</td><td>0</td><td>5</td><td>10</td><td>25</td><td>∞</td></tr><tr><td> $p_{\text{总}}/\text{kPa}$ </td><td>35.6</td><td>40.0</td><td>42.7</td><td>46.7</td><td>53.3</td></tr></table>

已知 $t = \infty$ 为 A 全部转化的时刻, 该反应对 A 为二级反应, 试导出以总压表示的反应速率方程, 并求速率常数。

11.10 反应 A $\longrightarrow$ P 为 n 级反应 $(n \neq 1)$ ，其速率方程可写为 $-\frac{dc_{A}}{dt} = kc_{A}^{n}$ ，若 a 为 A 的起始浓度，x 为 t 时刻变化的量（单位 mol·dm $^{-3}$ ），试导出 k 及 n 级反应半衰期的表达式。

11.11 设反应为 A $\longrightarrow$ P, 反应对 A 为 n 级反应, 定义 $[A]/[A]_{0}=1-\alpha$ , 则其半衰期 $t_{1/2}$ 与其四分之三衰期 $t_{3/4}$ 之比仅是 n 的函数, 试求该函数表达式, 并说明此式对于 n=1 是否适用。

11.12 大气中 $CO_{2}$ 含量较少, 但可鉴定出放射性同位素 ${}^{14}C$ , 一旦 $CO_{2}$ 由光合作用 “固定”, 从大气中拿走 ${}^{14}C$ , 而新 ${}^{14}C$ 又不再加入, 那么放射量会以半衰期为 5770 年的一级过程减少。现从加利福尼亚圣灵山脉的古代松树的木髓中取样, 测定其 ${}^{14}C$ 含量是大气中 $CO_{2}$ 的 ${}^{14}C$ 含量的 54.9%, 求该树的大约年龄。

## 11.13 某天然矿含放射性元素铀 (U), 其蜕变反应可简单表示为

$$
\mathrm{U} \xrightarrow {k (\mathrm{U})} \mathrm{Ra} \xrightarrow {k (\mathrm{Pb})} \mathrm{Pb}
$$

设已达稳态放射蜕变平衡, 测得镭与铀的浓度比保持为 $[Ra]/[U] = 3.47 \times 10^{-7}$ , 稳定产物铅与铀的浓度比为 $[Pb]/[U] = 0.1792$ , 已知镭的半衰期为 1580 年。

(1) 求铀的半衰期;

(2) 估计此矿的地质年龄 (计算时可作适当近似)。

11.14 在水溶液中, 金属离子 $\mathrm{M}^{2+}$ 与四苯基卟啉 (H $_2$ TPP) 生成的金属卟啉化合物在催化及生物化学方面具有多种功能, 设该反应速率方程为 $r = k[\mathrm{M}^{2+}]^a [\mathrm{H}_2\mathrm{TPP}]^b$ , 试设计测定 $\alpha, \beta$ 的实验方案, 并写出反应级数与所测实验数据之间的关系式 (提示: 反应式为 $\mathrm{M}^{2+} + \mathrm{H}_2\mathrm{TPP} \longrightarrow \mathrm{MTPP} + 2\mathrm{H}^+$ )。

11.15 反应 $\mathrm{H}_2(\mathrm{g}) + \mathrm{D}_2(\mathrm{g})\longrightarrow 2\mathrm{HD}(\mathrm{g})$ 在恒容下，按计量数进料，获得以下数据：

<table><tr><td>T/K</td><td colspan="2">1008</td><td colspan="3">946</td></tr><tr><td> $p_0/Pa$ </td><td>400</td><td>800</td><td>450</td><td>800</td><td>3200</td></tr><tr><td> $t_{1/2}/s$ </td><td>196</td><td>135</td><td>1330</td><td>1038</td><td>546</td></tr></table>

试求该反应级数。

11.16 物质 A 的热分解反应 $\mathrm{A(g)} \longrightarrow \mathrm{B(g)} + \mathrm{C(g)}$ 在密闭容器中恒温下进行, 测得其总压变化如下:

<table><tr><td>t/min</td><td>0</td><td>10</td><td>30</td><td> $\infty$ </td></tr><tr><td>p/(10 $^{6}$ Pa)</td><td>1.30</td><td>1.95</td><td>2.28</td><td>2.60</td></tr></table>

(1) 确定反应级数;

(2) 计算速率常数 k;

(3) 计算反应经过 40 min 时的转化率。

11.17 在一抽干的刚性容器中, 引入一定量纯气体 A(g), 发生如下反应:

$$
\mathrm{A(g)} \longrightarrow \mathrm{B(g)} + 2 \mathrm{C(g)}
$$

设反应能进行完全, 在 323 K 下恒温一定时间后开始计时, 测定系统的总压随时间的变化情况, 实验数据如下:

<table><tr><td>t/min</td><td>0</td><td>30</td><td>50</td><td>∞</td></tr><tr><td> $p_{\text{总}}/\text{kPa}$ </td><td>53.33</td><td>73.33</td><td>80.00</td><td>106.66</td></tr></table>

求该反应的级数及速率常数。

11.18 乙烯热分解反应 $\mathrm{C}_2\mathrm{H}_4(\mathrm{g}) \longrightarrow \mathrm{C}_2\mathrm{H}_2(\mathrm{g}) + \mathrm{H}_2(\mathrm{g})$ 为一级反应, 在 $1073\mathrm{K}$ 时, 反应经过 $10\mathrm{h}$ 时有 $50\%$ 乙烯分解, 已知该反应的活化能 $E_{\mathrm{a}} = 250.8\mathrm{kJ}\cdot \mathrm{mol}^{-1}$ , 求此反应在 $1573\mathrm{K}$ 时, 乙烯分解 $50\%$ 需多少时间?

11.19 反应 $\left[\mathrm{Co}(\mathrm{NH}_3)_3\mathrm{F}\right]^{2+} + \mathrm{H}_2\mathrm{O} \longrightarrow \left[\mathrm{Co}(\mathrm{NH}_3)_3\mathrm{H}_2\mathrm{O}\right]^{3+} + \mathrm{F}^-$ 是一个酸催化反应, 若反应的速率方程为 $r = k\left[\mathrm{Co}(\mathrm{NH}_3)_3\mathrm{F}^{2+}\right]^{\alpha}\left[\mathrm{H}^{+}\right]^{\beta}$ , 在指定温度和起始浓度条件下, 络合物反应掉 $\frac{1}{2}$ 和 $\frac{3}{4}$ 所用的时间分别是 $t_{1/2}$ 和 $t_{3/4}$ , 实验数据如下:

<table><tr><td>实验编号</td><td> $\frac{\left[Co(NH_3)_3F^{2+}\right]_0}{mol\cdot dm^{-3}}$ </td><td> $\frac{\left[H^+\right]_0}{mol\cdot dm^{-3}}$ </td><td>T/K</td><td> $t_{1/2}/h$ </td><td> $t_{3/4}/h$ </td></tr><tr><td>1</td><td>0.10</td><td>0.01</td><td>298</td><td>1.0</td><td>2.0</td></tr><tr><td>2</td><td>0.20</td><td>0.02</td><td>298</td><td>0.5</td><td>1.0</td></tr><tr><td>3</td><td>0.10</td><td>0.01</td><td>308</td><td>0.5</td><td>1.0</td></tr></table>

试根据实验数据求:

(1) 反应的级数 $\alpha$ 和 $\beta;$

(2) 不同温度时的反应速率常数 k;

(3) 反应实验活化能 $E_{a}$ 。

11.20 溶液中反应 $2Fe^{2+} + 2Hg^{2+} \longrightarrow Hg_{2}^{2+} + 2Fe^{3+}$ 在 353 K 下进行，测得下列两组实验数据：

<table><tr><td colspan="2">I组</td><td colspan="2">II组</td></tr><tr><td colspan="2"> $[Fe^{2+}]_0=0.1\ mol\cdot dm^{-3}$  $[Hg^{2+}]_0=0.1\ mol\cdot dm^{-3}$ </td><td colspan="2"> $[Fe^{2+}]_0=0.1\ mol\cdot dm^{-3}$  $[Hg^{2+}]_0=0.001\ mol\cdot dm^{-3}$ </td></tr><tr><td>t/(105s)</td><td>A(吸光度)</td><td>t/(105s)</td><td> $[Hg^{2+}]/(10^{-3}\ mol\cdot dm^{-3})$ </td></tr><tr><td>0</td><td>0.100</td><td>0</td><td>1.000</td></tr><tr><td>1</td><td>0.400</td><td>0.5</td><td>0.585</td></tr><tr><td>2</td><td>0.500</td><td>1.0</td><td>0.348</td></tr><tr><td>3</td><td>0.550</td><td>1.5</td><td>0.205</td></tr><tr><td>∞</td><td>0.700</td><td>2.0</td><td>0.122</td></tr><tr><td></td><td></td><td>∞</td><td>0</td></tr></table>

若反应速率方程为 $r = k[\mathrm{Fe}^{2+}]^{\alpha}[\mathrm{Hg}^{2+}]^{\beta}$ , 试求 $\alpha, \beta$ 和 $k$ 的值。

11.21 当有 $I_{2}$ 存在作为催化剂时, 氯苯 $\left(\mathrm{C}_{6}\mathrm{H}_{5}\mathrm{Cl}\right)$ 与 $Cl_{2}$ 在 $\mathrm{CS}_{2}(l)$ 溶液中发生如下的平行反应 (均为二级反应):

习题

$$
\mathrm{C} _ {6} \mathrm{H} _ {6} \mathrm{Cl} + \mathrm{Cl} _ {2} - \xrightarrow [ k _ {2} ]{k _ {1}} o - \mathrm{C} _ {6} \mathrm{H} _ {4} \mathrm{Cl} _ {2} + \mathrm{HCl}
$$

设在温度和 $I_{2}$ 的浓度一定时， $C_{6}H_{5}Cl$ 与 $Cl_{2}$ 在 $CS_{2}(l)$ 溶液中的起始浓度均为 $0.5\ mol\cdot dm^{-3}$ ，30 min 后，有 15% 的 $C_{6}H_{4}Cl$ 转变为 $o-C_{6}H_{4}Cl_{2}$ ，有 25% 的 $C_{6}H_{6}Cl$ 转变为 $p-C_{6}H_{4}Cl_{2}$ ，试计算两个速率常数 $k_{1}$ 和 $k_{2}$ 。

11.22 有正、逆反应均为一级的对峙反应:

$$
\mathrm{D} - \mathrm{R} _ {1} \mathrm{R} _ {2} \mathrm{R} _ {3} \mathrm{CBr} \underset {k _ {- 1}} {\overset {k _ {1}} {\rightleftharpoons}} \mathrm{L} - \mathrm{R} _ {1} \mathrm{R} _ {2} \mathrm{R} _ {3} \mathrm{CBr}
$$

正、逆反应的半衰期均为 $t_{1/2} = 10 \, min$ 。若起始时 $D - R_{1}R_{2}R_{3}CBr$ 的物质的量为 1 mol，试计算在 10 min 后，生成 $L - R_{1}R_{2}R_{3}CBr$ 的物质的量。

11.23 在 321 K 时, 在 200 mL 的 $0.1 \, mol \cdot dm^{-3}$ d-莰酮-3-羧酸的酒精溶液中, 发生下列两个反应:

$$
\mathrm{C} _ {1 0} \mathrm{H} _ {1 0} \mathrm{COOH} \xrightarrow {k _ {1}} \mathrm{C} _ {1 0} \mathrm{H} _ {1 0} \mathrm{O} + \mathrm{CO} _ {2}\tag{1}
$$

$$
\mathrm{C} _ {2} \mathrm{H} _ {5} \mathrm{OH} + \mathrm{C} _ {1 0} \mathrm{H} _ {1 0} \mathrm{COOH} \xrightarrow {k _ {2}} \mathrm{C} _ {1 0} \mathrm{H} _ {1 0} \mathrm{COOC} _ {2} \mathrm{H} _ {5} + \mathrm{H} _ {2} \mathrm{O}\tag{2}
$$

测量中和 $20 \, mL \, 0.1 \, mol \cdot dm^{-3}$ 原酸需 $0.05 \, mol \cdot dm^{-3} \, \mathrm{Ba(OH)}_{2}$ 溶液的体积, 以及产生 $CO_{2}$ 的质量, 得到如下结果:

<table><tr><td>t/min</td><td>0</td><td>10</td><td>20</td><td>30</td></tr><tr><td>Ba(OH)2溶液的体积/mL</td><td>20</td><td>16.26</td><td>13.25</td><td>10.68</td></tr><tr><td>产生CO2的质量/g</td><td>—</td><td>0.0841</td><td>0.1545</td><td>0.2095</td></tr></table>

试求 $k_{1}$ 和 $k_{2}$ 。

11.24 某反应在 300 K 时进行, 完成 40% 需 24 min。如果保持其他条件不变, 在 340 K 时进行, 同样完成 40%, 需时 4 min, 求该反应的实验活化能。

11.25 某一气相反应 $\mathrm{A(g)} \xrightarrow{k_{1}} \mathrm{B(g)} + \mathrm{C(g)}$ ，已知在 $298\mathrm{K}$ 时， $k_{1} = 0.21\mathrm{s}^{-1}$ ， $k_{-2} = 5 \times 10^{-9}\mathrm{Pa}^{-1} \cdot \mathrm{s}^{-1}$ ；当温度由 $298\mathrm{K}$ 升到 $310\mathrm{K}$ 时，其 $k_{1}$ 和 $k_{-2}$ 的值均增加1倍，试求：

(1) 298 K 时, 反应平衡常数 $K_{p}$ ;

(2) 正、逆反应的实验活化能 $E_{a}$ ;

(3) 298 K 时, 反应的 $\Delta_{r}H_{m}$ 和 $\Delta_{r}U_{m}$ ;

(4) 298 K 时, A 的起始压力为 100 kPa, 若使总压达到 152 kPa 时, 所需的时间。

11.26 某溶液中含有 $\mathrm{NaOH}$ 及 $\mathrm{CH}_3\mathrm{COOC}_2\mathrm{H}_5$ ，浓度均为 $0.01\mathrm{mol}\cdot \mathrm{dm}^{-3}$ 在 298 K 时, 反应经 10 min 有 39% 的 $CH_{3}COOC_{2}H_{5}$ 分解, 而在 308 K 时, 反应 10 min 有 55% 的 $CH_{3}COOC_{2}H_{5}$ 分解。该反应速率方程为

$$
r = k [ \mathrm{NaOH} ] [ \mathrm {CH_ {3} COOC_ {2} H_ {5}} ]
$$

试计算:

(1) 298 K 和 308 K 时, 反应的速率常数;

(2) $288 \mathrm{~K}$ 时, 反应 $10 \mathrm{~min}, \mathrm{CH}_{3} \mathrm{COOC}_{2} \mathrm{H}_{5}$ 分解的分数;

(3) $293 \mathrm{~K}$ 时, 若有 $50 \%$ 的 $\mathrm{CH}_{3} \mathrm{COOC}_{2} \mathrm{H}_{5}$ 分解所需的时间。

11.27 在 673 K 时, 设反应 $\mathrm{NO}_{2}(\mathrm{~g}) \longrightarrow \mathrm{NO}(\mathrm{~g}) + \frac{1}{2}\mathrm{O}_{2}(\mathrm{~g})$ 可以完全进行, 并设产物对反应速率没无影响, 经实验证明该反应是二级反应, 速率方程可表示为 $-\frac{\mathrm{d}[\mathrm{NO}_{2}]}{\mathrm{d}t} = k[\mathrm{NO}_{2}]^{2}$ , 速率常数 k 与反应温度 T 之间的关系为

$$
\ln \frac {k}{(\mathrm{mol} \cdot \mathrm{dm} ^ {- 3}) ^ {- 1} \cdot \mathrm{s} ^ {- 1}} = - \frac {1 2 8 8 6 . 7}{T / \mathrm{K}} + 2 0. 2 7
$$

试计算:

(1) 该反应的 A 及实验活化能 $E_{a}$ ;

(2) 若 673 K 时, 将 $\mathrm{NO}_{2}(\mathrm{~g})$ 通入反应器, 使其压力为 26.66 kPa, 发生上述反应, 当反应器中的压力达到 32.0 kPa 时所需的时间 (设气体为理想气体)。

11.28 某溶液中的反应 $\mathrm{A} + \mathrm{B} \longrightarrow \mathrm{P}$ , 当 $\mathrm{A}$ 和 $\mathrm{B}$ 的起始浓度 $[\mathrm{A}]_0 = 1 \times 10^{-4} \mathrm{~mol} \cdot \mathrm{dm}^{-3}$ , $[\mathrm{B}]_0 = 0.001 \mathrm{~mol} \cdot \mathrm{dm}^{-3}$ 时, 实验测得不同温度下吸光度随时间的变化如下:

<table><tr><td>t/min</td><td>0</td><td>57</td><td>130</td><td>∞</td></tr><tr><td>298 K时A的吸光度</td><td>1.390</td><td>1.030</td><td>0.706</td><td>0.100</td></tr><tr><td>308 K时A的吸光度</td><td>1.460</td><td>0.542</td><td>0.210</td><td>0.110</td></tr></table>

当固定 $[A]_{0}=1\times10^{-4}\ mol\cdot dm^{-3}$ ，改变 $[B]_{0}$ 时，实验测得在 298 K 时， $t_{1/2}$ 随 $[B]_{0}$ 的变化如下：

<table><tr><td> $[B]_0/(mol·dm^{-3})$ </td><td>0.01</td><td>0.02</td></tr><tr><td> $t_{1/2}/s$ </td><td>120</td><td>30</td></tr></table>

设速率方程为 $r = k[\mathrm{A}]^{\alpha}[\mathrm{B}]^{\beta}$ ，试计算 $\alpha, \beta$ ，速率常数 $k$ 和实验活化能 $E_{\mathrm{a}}$ 。

11.29 通过测量系统的电导率, 可以跟踪如下反应:

$$
\mathrm{CH} _ {3} \mathrm{CONH} _ {2} + \mathrm{HCl} + \mathrm{H} _ {2} \mathrm{O} \longrightarrow \mathrm{CH} _ {3} \mathrm{COOH} + \mathrm{NH} _ {4} \mathrm{Cl}
$$

在 $63^{\circ}$ C 时, 等体积混合浓度均为 $2.0 \, mol \cdot dm^{-3}$ 的 $CH_{3}CONH_{2}$ 和 HCl 溶液后, 在不同时刻观测到下列电导率数据:

<table><tr><td>t/min</td><td>0</td><td>13</td><td>34</td><td>50</td></tr><tr><td> $\kappa/(S·m^{-1})$ </td><td>40.9</td><td>37.4</td><td>33.3</td><td>31</td></tr></table>

已知该温度时, 各离子的摩尔电导率分别为 $\Lambda_{\mathrm{m}}(\mathrm{H}^{+}) = 0.0515 \mathrm{~S} \cdot \mathrm{m}^{2} \cdot \mathrm{mol}^{-1}$ , $\Lambda_{\mathrm{m}}(\mathrm{Cl}^{-}) = 0.0133 \mathrm{~S} \cdot \mathrm{m}^{2} \cdot \mathrm{mol}^{-1}$ 和 $\Lambda_{\mathrm{m}}(\mathrm{NH}_{4}^{+}) = 0.0137 \mathrm{~S} \cdot \mathrm{m}^{2} \cdot \mathrm{mol}^{-1}$ , 不考虑非理想性的影响, 确定反应级数并计算反应的速率常数。

11.30 433 K 时, 气相反应 $N_{2}O_{5} \longrightarrow 2NO_{2} + \frac{1}{2}O_{2}$ 是一级反应。已知反应活化能为 $103\ kJ \cdot mol^{-1}$ 。

(1) 在恒容容器中最初引入纯的 $N_{2}O_{5}$ ，3 s 后容器压力增大一倍。

① 求此时 $N_{2}O_{5}$ 的分解分数;

② 求速率常数。

(2) 若反应发生在同样容器中, 但温度为 $T_{2}$ , 在 $3 \mathrm{~s}$ 后容器的压力增大到最初的 1.5 倍。

① 求温度 $T_{2}$ 时反应的半衰期;

② 求温度 $T_{2}$ 。

11.31 反应 $\mathrm{A(g) + 2B(g)}\longrightarrow \mathrm{P(g)}$ 的速率方程为 $r = -\mathrm{dp}_{\mathrm{A}} / \mathrm{dt} = kp_{\mathrm{A}}^{\alpha}p_{\mathrm{B}}^{\beta}$ 经实验发现：当B的起始量远远大于A的起始量时， $\frac{\mathrm{d}\ln p_{\mathrm{A}} / kp_{\mathrm{A}}}{\mathrm{dt}} = \mathrm{C},$ 其中C为常数；当A与B进料比为 $1:2$ 时，反应速率 $r$ 与 $p_{\mathrm{A}}p_{\mathrm{B}}$ 之比也是一常数，在 $500\mathrm{K}$ 时其值为 $9.87\times 10^{-4}\mathrm{kPa}^{-1}\cdot \mathrm{min}^{-1}$ ，在 $510\mathrm{K}$ 时其值为 $1.974\times 10^{-3}\mathrm{kPa}^{-1}\cdot \mathrm{min}^{-1}$ 试确定该反应的反应级数及反应活化能。

11.32 气相反应 $2NO + H_{2} \longrightarrow N_{2}O + H_{2}O$ 能进行完全, 且具有速率方程 $r = k p_{NO}^{\alpha} p_{H_{2}}^{\beta}$ , 实验结果如下:

<table><tr><td> $p_{\text{NO}}^0/\text{kPa}$ </td><td>80</td><td>80</td><td>1.3</td><td>2.6</td><td>80</td></tr><tr><td> $p_{\text{H}_2^0}/\text{kPa}$ </td><td>1.3</td><td>2.6</td><td>80</td><td>80</td><td>1.3</td></tr><tr><td> $t_{1/2}/\text{s}$ </td><td>19.2</td><td>19.2</td><td>830</td><td>415</td><td>10</td></tr><tr><td>T/K</td><td>1093</td><td>1093</td><td>1093</td><td>1093</td><td>1113</td></tr></table>

求该反应级数 $\alpha$ 及 $\beta$ ，并计算实验活化能 $E_{a}$ 。

11.33 有一个涉及一种反应物种 (A) 的二级反应, 此反应速率常数可用下式表示:

$$
k / \left(\mathrm{dm} ^ {3} \cdot \mathrm{mol} ^ {- 1} \cdot \mathrm{s} ^ {- 1}\right) = 4. 0 \times 1 0 ^ {1 0} (T / \mathrm{K}) ^ {1 / 2} \exp \left(- \frac {1 4 5 2 0 0 \mathrm{J} \cdot \mathrm{mol} ^ {- 1}}{R T}\right)
$$

(1) 600 K 时, 当反应物 A 的初始浓度为 $0.1 \, mol \cdot dm^{-3}$ 时, 此反应的半衰期为多少?

(2) $300 \mathrm{~K}$ 时, 此反应的活化能 $E_{\mathrm{a}}$ 为多少?

(3) 如果上述反应是通过下列历程进行的:

$$
\mathrm{A} \xrightarrow [ k _ {- 1} ]{k _ {1}} \mathrm{B}
$$

$$
\mathrm{B} + \mathrm{A} \xrightarrow {k _ {2}} \mathrm{C}
$$

$$
\mathrm{C} \xrightarrow {k _ {3}} \mathrm{P}
$$

其中 B 和 C 是活性中间物, P 为最终产物。试分析反应速率方程在什么条件下对这个反应能给出二级速率方程。

11.34 已知气相反应 $3H_{2} + N_{2} \longrightarrow 2NH_{3}$ 的下列速率数据 (723 K):

<table><tr><td>实验编号</td><td> $p_{\mathrm {H}_{2}}^{0}/\mathrm {kPa}$ </td><td> $p_{\mathrm {N}_{2}}^{0}/\mathrm {kPa}$ </td><td> $\frac{-dp_{总}}{dt}/(\mathrm {kPa}\cdot\mathrm {h}^{-1})$ </td></tr><tr><td>1</td><td>13.2</td><td>0.132</td><td>0.00132</td></tr><tr><td>2</td><td>26.4</td><td>0.132</td><td>0.00528</td></tr><tr><td>3</td><td>52.8</td><td>0.660</td><td>0.1056</td></tr></table>

$-\frac{dp_{总}}{dt}=kp_{H_{2}}^{x}p_{N_{2}}^{y},$ 试求:

(1) $x, y$ 的值;

(2) 实验 1 中 $p_{N_{0}}$ 降到 0.066 kPa 所需时间;

(3) 若反应在 823 K 进行, 实验 1 的初始速率 (假定活化能为 $189 \, kJ \cdot mol^{-1}$ )。

11.35 设有一反应 $2\mathrm{A}(\mathrm{g}) + \mathrm{B}(\mathrm{g}) \longrightarrow \mathrm{G}(\mathrm{g}) + \mathrm{H}(\mathrm{s})$ 在某恒温密闭容器中进行, 开始时 A 和 B 的物质的量之比为 2:1, 起始总压为 3.0 kPa, 在 400 K 时, 60 s 后容器中总压为 2.0 kPa, 设该反应的速率方程为 $-\frac{dp_{B}}{dt} = k_{p} p_{A}^{3/2} p_{B}^{1/2}$ , 实验活化能 $E_{a} = 100 kJ \cdot mol^{-1}$ 。试求:

(1) 在 $400 \, K$ 时, $150 \, s$ 后容器中 B 的分压;

(2) 在 500 K 时, 重复上述实验, 求 50 s 后 B 的分压。

11.36 气相反应合成 $\mathrm{HBr:H_2(g) + Br_2(g)}\longrightarrow 2\mathrm{HBr(g)}$ ，其反应历程为

① $\mathrm{Br}_2 + \mathrm{M}\xrightarrow{k_1} 2\mathrm{Br}\cdot +\mathrm{M}$

② $Br\cdot + H_{2} \xrightarrow{k_{2}} HBr + H\cdot$

习题

③ $H\cdot + Br_{2} \xrightarrow{k_{3}} HBr + Br\cdot$

④ $\mathrm{H}\cdot +\mathrm{HBr}\xrightarrow{k_4}\mathrm{H}_2 + \mathrm{Br}\cdot$

⑤ $\mathrm{Br}\cdot +\mathrm{Br}\cdot +\mathrm{M}\xrightarrow{k_5}\mathrm{Br}_2 + \mathrm{M}$

(1) 试推导 HBr 生成反应的速率方程;

(2) 已知如下键能数据, 估算各基元反应的活化能。

<table><tr><td>化学键</td><td>Br—Br</td><td>H—Br</td><td>H—H</td></tr><tr><td> $E/(kJ \cdot mol^{-1})$ </td><td>192</td><td>364</td><td>435</td></tr></table>

11.37 反应 $OCl^{-} + I^{-} \longrightarrow OI^{-} + Cl^{-}$ 的可能机理如下:

$$
(1) \mathrm{OCl} ^ {-} + \mathrm{H} _ {2} \mathrm{O} \xrightarrow [ k _ {- 1} ]{k _ {1}} \mathrm{HOCl} + \mathrm{OH} \quad \text { 快速平衡 } \left(K = \frac {k _ {1}}{k _ {- 1}}\right)
$$

$$
(2) \mathrm{HOCl} + \mathrm{I} ^ {-} \xrightarrow {k _ {2}} \mathrm{HOI} + \mathrm{Cl} ^ {-} \quad \text { 速控步 }
$$

$$
(3) \mathrm{OH} ^ {-} + \mathrm{HOI} \xrightarrow {k _ {3}} \mathrm{H} _ {2} \mathrm{O} + \mathrm{OI} ^ {-} \quad \text { 快速反应 }
$$

试推导出反应的速率方程，并求表观活化能与各基元反应活化能之间的关系。

11.38 反应 $2NO + O_{2} \longrightarrow 2NO_{2}$ 的反应机理如下:

$$
\mathrm{NO} + \mathrm{NO} \xrightarrow {k _ {1}} \mathrm{N} _ {2} \mathrm{O} _ {2} \quad E _ {1} = 7 9. 5 \mathrm{kJ} \cdot \mathrm{mol} ^ {- 1}
$$

$$
\mathrm{N} _ {2} \mathrm{O} _ {2} \xrightarrow {k _ {2}} 2 \mathrm{NO} \quad E _ {2} = 2 0 5 \mathrm{kJ} \cdot \mathrm{mol} ^ {- 1}
$$

$$
\mathrm{N} _ {2} \mathrm{O} _ {2} + \mathrm{O} _ {2} \xrightarrow {k _ {3}} 2 \mathrm{NO} _ {2} \quad E _ {3} = 8 4 \mathrm{kJ} \cdot \mathrm{mol} ^ {- 1}
$$

(1) 对 $N_{2}O_{2}$ 作稳态处理, 导出以 $\frac{d[NO_{2}]}{dt}$ 表示的速率方程;

(2) 第一步生成的 $N_{2}O_{2}$ 只有极少量用于第三步生成产物, 而绝大部分转化为第二步 NO, 据此事实计算反应活化能。

11.39 多数烃类气相热分解反应的表观速率方程对反应物级数为 0.5, 1.0 和 1.5 等整数或半整数。这可以用自由基链反应机理来解释。设 A 为反应物， $R_{1}, R_{2}, \cdots, R_{6}$ 为产物分子， $X_{1}, X_{2}$ 为活性自由基。

$$
\text { 链的开始 } \quad \mathrm{A} \xrightarrow {k _ {0}} \mathrm{R} _ {1} + \mathrm{X} _ {1} \quad \text { 慢 }\tag{1}
$$

$$
\text { 链的传递 } \quad \mathrm{A} + \mathrm{X} _ {1} \xrightarrow {k _ {1}} \mathrm{R} _ {2} + \mathrm{X} _ {2}\tag{2}
$$

$$
\mathrm{X} _ {2} \xrightarrow {k _ {2}} \mathrm{R} _ {3} + \mathrm{X} _ {1}\tag{3}
$$

$$
\mathrm{链的终止} \qquad 2 \mathrm{X} _ {1} \xrightarrow {k _ {4}} \mathrm{R} _ {4}\tag{4}
$$

$$
\mathrm{X} _ {1} + \mathrm{X} _ {2} \xrightarrow {k _ {5}} \mathrm{R} _ {5}\tag{5}
$$

$$
2 \mathrm{X} _ {2} \xrightarrow {k _ {6}} \mathrm{R} _ {6}\tag{6}
$$

假设链的终止步骤分别为 (4), (5), (6) 三种情况, 试按上述机理推求 A 的分解速率方程。

11.40 对光气合成提出如下机理:

① $\mathrm{Cl}_2\xrightarrow{k_1} 2\mathrm{Cl}$

② $2\mathrm{Cl}\xrightarrow{k_{-1}}\mathrm{Cl}_{2}$

③ $\mathrm{Cl} + \mathrm{CO}\xrightarrow{k_2}\mathrm{COCl}$

④ COCl $\xrightarrow{k_{-2}}$ Cl + CO

⑤ $\mathrm{COCl} + \mathrm{Cl}_2\xrightarrow{k_3}\mathrm{COCl}_2 + \mathrm{Cl}$

(1) 应用稳态法推导出 $COCl_{2}$ 生成速率方程;

(2) 当反应 ①～④ 比反应 ⑤ 进行较快时, 试问 (1) 中结果可否简化?

(3) 若反应 ① 和 ②, ③ 和 ④ 达成平衡, 试证 (2) 的结果。

11.41 $\mathrm{O}_3$ 分解反应动力学得到如下规律:

(1) 在反应初始阶段对 $[O_{3}]$ 为一级反应;

(2) 在反应后期, 对 $[O_{3}]$ 为二级反应, 对 $[O_{2}]$ 为负一级反应;

(3) 在反应过程, 检测到的唯一中间物为自由原子 O。

试根据以上事实, 推测 $O_{3}$ 分解反应历程。

11.42 硝酰胺 $NO_{2}NH_{2}$ 在缓冲介质 (水溶液) 中缓慢分解: $NO_{2}NH_{2} \longrightarrow N_{2}O(g) + H_{2}O$ , 实验找到如下规律:

(a) 恒温下, 在硝酰胺溶液上部固定体积中, 用测定 $N_{2}O$ 气体的分压 p 来研究分解反应, 据 p-t 曲线可得

$$
\lg \frac {p _ {\infty}}{p _ {\infty} - p} = k ^ {\prime} t
$$

(b) 改变缓冲介质, 使在不同的 pH 下进行实验, 作 $\lg t_{1/2} - pH$ 图, 得一直线, 斜率为 -1, 截距为 $\lg(0.693/k)$ 。

回答下列问题:

(1) 写出该反应的速率方程, 并说明为什么。

(2) 有人提出如下两种反应历程:

$$
\begin{array}{r l r} & {\mathrm {①NO_ {2} NH_ {2} \xrightarrow {k_ {1}} N_ {2} O(g)+ H_ {2} O}} \\ & {\mathrm {②NO_ {2} NH_ {2} + H_ {3} O\xrightarrow [ k _ {- 2} ]{k_ {2}} NO_ {2} NH_ {3} ^ {+} + H_ {2} O}} & {\text {瞬间达平衡}} \\ & {\mathrm {NO_ {2} NH_ {3} ^ {+} \xrightarrow {k_ {3}} N_ {2} O+ H_ {3} O^ {+}}} & {\text {速控步}} \end{array}
$$

你认为上述反应历程是否与事实相符,为什么?

(3) 请提出你认为比较合理的反应历程, 并求其速率方程。

习题

11.43 合成氨的反应机理如下:

(1) $\mathrm{N}_2 + 2(\mathrm{Fe}) \xrightarrow{k_1} 2\mathrm{N}(\mathrm{Fe})$ 速控步

(2) $\mathrm{N(Fe)} + \frac{3}{2}\mathrm{H}_{2} \xrightarrow[k_{3}]{k_{2}} \mathrm{NH}_{3} + (\mathrm{Fe})$ 对峙反应

试证明：

$$
- \frac {\mathrm{d} [ \mathrm{N} _ {2} ]}{\mathrm{d} t} = \frac {k [ \mathrm{N} _ {2} ]}{\left(1 + \frac {K [ \mathrm{NH} _ {3} ]}{[ \mathrm{H} _ {2} ] ^ {3 / 2}}\right) ^ {2}}
$$

11.44 反应 $\mathrm{A(g) + 2B(g)}\longrightarrow \frac{1}{2}\mathrm{C(g) + D(g)}$ 在一密闭容器中进行, 假设速率方程的形式为 $r = k_{p}p_{\mathrm{A}}^{\alpha}p_{\mathrm{B}}^{\beta}$ , 实验发现: (a) 当反应物的起始分压分别为 $p_{\mathrm{A}}^{0} = 26.664\mathrm{kPa}, p_{\mathrm{B}}^{0} = 106.66\mathrm{kPa}$ 时, 反应中 $\ln p_{\mathrm{A}}$ 随时间变化率与 $p_{\mathrm{A}}$ 无关; (b) 当反应物的起始分压分别为 $p_{\mathrm{A}}^{0} = 53.328\mathrm{kPa}, p_{\mathrm{B}}^{0} = 106.66\mathrm{kPa}$ 时, $\frac{r}{p_{\mathrm{A}}^{2}}$ 为常数, 并测得 $500\mathrm{K}$ 和 $510\mathrm{K}$ 时, 该常数分别为 $1.974\times 10^{-3}(\mathrm{kPa}\cdot \min)^{-1}$ 和 $3.948\times 10^{-3}(\mathrm{kPa}\cdot \min)^{-1}$ 。试确定:

(1) 速率方程中的 $\alpha$ 和 $\beta$ 的值;

(2) 反应在 500 K 时的速率常数;

(3) 反应的活化能。

11.45 当用无水乙醇作溶剂时, $d$ -樟脑-3-羧酸 (A) 发生如下两个反应: (a) A 直接分解为樟脑 (B) 和 $\mathrm{CO}_{2}(\mathrm{~g})$ ; (b) A 与溶剂乙醇反应, 生成樟脑羧酸乙酯 (C) 和 $\mathrm{H}_{2} \mathrm{O}(\mathrm{l})$ 。在反应体积为 $0.2 \mathrm{dm}^{3}$ 时, 生成的 $\mathrm{CO}_{2}(\mathrm{~g})$ 用碱液吸收并计算其质量, A 的浓度用碱滴定求算。在 $321 \mathrm{~K}$ 时, 实验数据如下:

<table><tr><td>t/min</td><td>0</td><td>10</td><td>20</td><td>30</td><td>40</td><td>50</td><td>60</td></tr><tr><td> $[A]/(mol·dm^{-3})$ </td><td>0.100</td><td>0.0813</td><td>0.0663</td><td>0.0534</td><td>0.0437</td><td>0.0294</td><td>0.0200</td></tr><tr><td> $m(CO_2)/g$ </td><td>0</td><td>0.0841</td><td>0.1545</td><td>0.2095</td><td>0.2482</td><td>0.3045</td><td>0.3556</td></tr></table>

如忽略逆反应, 求这两个反应的速率常数。

11.46 473 K 时, 有反应 A + 2B → 2C + D, 其速率方程可写成 r = k[A]^{x}[B]^{y}。实验 (a): 当 A, B 的初始浓度分别为 [A]\_{0} = 0.01 mol·dm^{-3} 和 [B]\_{0} = 0.02 mol·dm^{-3} 时, 测得反应物 B 在不同时刻的浓度数据如下:

<table><tr><td>t/h</td><td>0</td><td>90</td><td>217</td></tr><tr><td> $[B]/(mol \cdot dm^{-3})$ </td><td>0.020</td><td>0.010</td><td>0.005</td></tr></table>

实验 (b): 当 A, B 的初始浓度相等, $[A]_{0} = [B]_{0} = 0.02 \, \text{mol} \cdot \text{dm}^{-3}$ 时, 测得初始反应速率为实验 (a) 的 1.4 倍, 即 $\frac{r_{0,b}}{r_{0,a}} = 1.4$ 。

(1) 求该反应的总级数 $x + y$ ;

(2) 分别求对 A, B 的反应级数 x, y;

(3) 计算速率常数 k。

11.47 在 298 K 时, 下列反应可进行到底: $\mathrm{N}_{2}\mathrm{O}_{5}(\mathrm{~g}) + \mathrm{NO}(\mathrm{g}) \longrightarrow k3\mathrm{NO}_{2}(\mathrm{~g})$ 。在 $\mathrm{N}_{2}\mathrm{O}_{5}(\mathrm{~g})$ 和 $\mathrm{NO}(\mathrm{g})$ 的初始压力分别为 $p_{\mathrm{N}_{2}\mathrm{O}_{5}}^{0} = 133.32 \, \mathrm{Pa}, p_{\mathrm{NO}}^{0} = 13332 \, \mathrm{Pa}$ 时, 用 $p_{\mathrm{N}_{2}\mathrm{O}_{5}}$ 对时间 t 作图, 得一直线, 相应的半衰期为 2.0 h, 当 $\mathrm{N}_{2}\mathrm{O}_{5}(\mathrm{~g})$ 和 $\mathrm{NO}(\mathrm{g})$ 的初始压力均为 6666 Pa 时, 得如下实验数据:

<table><tr><td> $p_{\text{总}}/\text{Pa}$ </td><td>13332</td><td>15332</td><td>16665</td><td>19998</td></tr><tr><td>t/h</td><td>0</td><td>1</td><td>2</td><td>∞</td></tr></table>

(1) 若反应的速率常数方程可表示为 $r = k p_{N_{2}O_{5}}^{x} p_{NO}^{y}$ ，从上面给出的数据求速率常数 k 和反应级数 x, y 的值；

(2) 如果 $N_{2}O_{5}(g)$ 和 $NO(g)$ 的初始压力分别为 $p_{N_{2}O_{5}}^{0}=13332\ Pa, p_{NO}^{0}=133.32\ Pa$ 时，求半衰期 $t_{1/2}$ 的值。

11.48 有正、逆反应均为一级的对峙反应 A $\xrightarrow{k_{1}}$ B, 已知其速率常数和平衡常数与温度的关系式分别为

$$
\begin{array}{r l} & \lg (k _ {1} / \mathrm{s} ^ {- 1}) = - \frac {2 0 0 0}{T / \mathrm{K}} + 4. 0 \\ & \lg K = \frac {2 0 0 0}{T / \mathrm{K}} - 4. 0 \qquad K = k _ {1} / k _ {- 1} \end{array}
$$

反应开始时， $[\mathrm{A}]_0 = 0.5\mathrm{mol}\cdot \mathrm{dm}^{-3},[\mathrm{B}]_0 = 0.05\mathrm{mol}\cdot \mathrm{dm}^{-3}$ ，试计算：

(1) 逆反应的活化能;

(2) 400 K 时, 反应 10 s 后, A 和 B 的浓度;

(3) 400 K 时, 反应达平衡时, A 和 B 的浓度。

11.49 反应物 A 同时生成主产物 B 及副产物 C, 反应均为一级反应:

$$
\mathrm{A} \xrightarrow {k _ {1}} \mathrm{B}   \xrightarrow {k _ {2}} \mathrm{C}
$$

已知 $k_{1}=1.2\times10^{3}\exp\left(-\frac{90\ \mathrm{kJ}\cdot\mathrm{mol}^{-1}}{RT}\right)$ ， $k_{2}=8.9\exp\left(-\frac{80\ \mathrm{kJ}\cdot\mathrm{mol}^{-1}}{RT}\right)$ 。

(1) 使 B 含量大于 90% 及大于 95% 时, 求各需的反应温度 $T_{1}$ 和 $T_{2}$ ;

(2) 可否得到含 B 为 99.5% 的产品?

11.50 已知乙烯氧化制环氧乙烷, 可发生下列两个反应:

$$
\mathrm{C} _ {2} \mathrm{H} _ {4} (\mathrm{g}) + \frac {1}{2} \mathrm{O} _ {2} (\mathrm{g}) \xrightarrow {k _ {1}} \mathrm{C} _ {2} \mathrm{H} _ {4} \mathrm{O} (\mathrm{g})
$$

$$
② \mathrm{C} _ {2} \mathrm{H} _ {4} (\mathrm{g}) + 3 \mathrm{O} _ {2} (\mathrm{g}) \xrightarrow {k _ {2}} 2 \mathrm{CO} _ {2} (\mathrm{g}) + 2 \mathrm{H} _ {2} \mathrm{O} (\mathrm{g})
$$

在 298 K 时, 物质的标准摩尔生成 Gibbs 自由能数据如下:

<table><tr><td>物质</td><td> $C_{2}H_{4}O(g)$ </td><td> $C_{2}H_{4}(g)$ </td><td> $CO_{2}(g)$ </td><td> $H_{2}O(g)$ </td></tr><tr><td> $\Delta_{f}G_{m}^{\ominus}/(kJ\cdot mol^{-1})$ </td><td>-13.0</td><td>68.4</td><td>-394.4</td><td>-228.6</td></tr></table>

当在银催化剂上, 研究上述反应时得到反应 ① 及反应 ② 的反应级数完全相同, $E_{1} = 63.6 \mathrm{~kJ} \cdot \mathrm{mol}^{-1}$ , $E_{2} = 82.8 \mathrm{~kJ} \cdot \mathrm{mol}^{-1}$ , 而且可以控制 $\mathrm{C}_{2} \mathrm{H}_{4} \mathrm{O}(\mathrm{g})$ 的进一步氧化的速率极低。

(1) 从热力学观点, 讨论乙烯氧化生产环氧乙烷之可能性;

(2) 求 $T_{1}=298\ K$ , $T_{2}=503\ K$ 时, 两反应的速率之比值 $r_{1}/r_{2}$ ;

(3) 从动力学观点, 讨论乙烯氧化生产环氧乙烷是否可行, 并据计算结果讨论应如何选择反应温度。

