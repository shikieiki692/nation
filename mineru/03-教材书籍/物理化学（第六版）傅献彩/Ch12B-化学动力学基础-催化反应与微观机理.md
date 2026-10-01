---
title: "傅献彩《物理化学》（第六版下册）-第十二章 化学动力学基础(四)：催化反应与微观机理"
type: 外部教材切片
source_book: "物理化学（第六版下册）-傅献彩"
syllabus_codes: [基础-12, 基础-15]
created: 2026-09-25
updated: 2026-09-25
status: 已填充
---

## 12.9 催化反应动力学

催化剂与催化作用

能加快反应的速率而不改变反应总的标准 (摩尔) Gibbs 自由能变化的物质称为催化剂 (catalyst), 相关过程称为催化作用 (catalysis), 有催化剂参与的反应称为催化反应 (catalyzed reaction)。能使反应速率变慢的物质称为抑制剂 (inhibitor)，相关过程称为抑制作用 (inhibition)。

催化剂在现代工业中的作用是毋庸赘述的, 尤其是在化工、医药、农药、染料等工业中, 80% 以上产品的生产过程都需要催化剂。许多熟知的工业反应如氮氢合成氨、 $SO_{2}(g)$ 氧化制 $SO_{3}(g)$ 、氨氧化制硝酸、尿素的合成、合成橡胶、高分子的聚合反应等, 都是采用催化剂的。在生命现象中大量存在着催化作用, 例如植物对 $CO_{2}(g)$ 的光合作用, 有机体内的新陈代谢, 蛋白质、糖类和脂肪的分解作用等基本上都是酶催化作用。在人体内酶催化作用的终止意味着生命的终止。

化学工业的发展和国民经济的需要都推动着对催化作用的研究, 生命科学的研究同样需要了解各种酶催化作用的机理。但是, 由于涉及的问题比较复杂, 催化理论的进展远远落后于生产实际。

催化反应通常可以分为均相催化反应和多相催化反应, 前者催化剂和反应物处于同一相, 如均为气态或液态, 后者则不处于同一相, 这时反应在两相界面上进行。工业上许多重要的催化反应都是多相催化反应, 且以催化剂是固态物质, 反应物是气态或液态者居多。

催化剂之所以能加快反应的速率, 是因为它参与具体的反应过程 (既是反应的反应物, 也是反应的产物), 改变了反应的途径, 降低了反应的活化能, 见表 12.4。如图 12.21 所示, 在有催化剂 K 存在的情况下, 反应沿着活化能较低的新途径进行, 图中的最高点相当于反应过程的中间状态。

表 12.4 催化反应和非催化反应的活化能

<table><tr><td rowspan="2">反应</td><td colspan="2"> $\frac{E_a}{kJ·mol^{-1}}$ </td><td rowspan="2">催化剂</td></tr><tr><td>非催化反应</td><td>催化反应</td></tr><tr><td>2HI  $\longrightarrow$  H2+I2</td><td>184.1</td><td>104.6</td><td>Au</td></tr><tr><td>2H2O  $\longrightarrow$  2H2+O2</td><td>244.8</td><td>136.0</td><td>Pt</td></tr><tr><td>蔗糖在盐酸溶液中的分解</td><td>107.1</td><td>39.3</td><td>转化酶</td></tr><tr><td>2SO2+O2  $\longrightarrow$  2SO3</td><td>251.0</td><td>62.8</td><td>Pt</td></tr><tr><td>3H2+N2  $\longrightarrow$  2NH3</td><td>334.7</td><td>167.4</td><td>Fe-Al2O3-K2O</td></tr></table>

设催化剂 K 能加速反应 A + B $\xrightarrow{K}$ AB, 设其机理为

$$
\mathrm{A} + \mathrm{K} \xrightarrow [ k _ {2} ]{k _ {1}} \mathrm{AK}\tag{1}
$$

$$
\mathrm{AK} + \mathrm{B} \xrightarrow {k _ {3}} \mathrm{AB} + \mathrm{K}\tag{2}
$$

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_200-399_images/7bd9f7fc680e3b70f571559310e5899e0c2540c0db33c8273fc8c2e0d0f675ca.jpg)  
图 12.21 催化反应的活化能与反应的途径

若第一个反应能很快达到平衡, 则用平衡假设近似法, 从反应 (1) 得

$$
k _ {1} c _ {\mathrm{K}} c _ {\mathrm{A}} = k _ {2} c _ {\mathrm{AK}}
$$

或

$$
c _ {\mathrm{AK}} = \frac {k _ {1}}{k _ {2}} c _ {\mathrm{K}} c _ {\mathrm{A}}
$$

但总反应速率由反应 (2) 决定, 即

$$
r = k _ {3} c _ {\mathrm{AK}} c _ {\mathrm{B}} = k _ {3} \frac {k _ {1}}{k _ {2}} c _ {\mathrm{B}} c _ {\mathrm{K}} c _ {\mathrm{A}} = k c _ {\mathrm{A}} c _ {\mathrm{B}}
$$

式中 k 称为表观速率常数 (apparent rate constant), $k = k_{3} \frac{k_{1}}{k_{2}} c_{K}$ 。上述各基元反应的速率常数可以用 Arrhenius 公式表示, 于是

$$
k = \frac {A _ {1} A _ {3}}{A _ {2}} c _ {\mathrm{K}} \exp \left(- \frac {E _ {1} + E _ {3} - E _ {2}}{R T}\right)
$$

故催化反应的表观活化能 $E_{\mathrm{a}} = E_{1} + E_{3} - E_{2}$ （能峰的示意图如图12.21所示）。而非催化反应（图12.21中用上面的一条曲线表示）要克服一个活化能为 $E_0$ 的较高的能峰，而在催化剂的存在下，反应的途径改变，只需要克服两个较小的能峰 $(E_{1}$ 和 $E_{3})$ 。

活化能的降低对于反应速率的影响是很大的, 如表 12.4 中 HI 的分解反应 (503 K), 在没有催化剂时活化能为 $184.1 \, kJ \cdot mol^{-1}$ , 若以 Au 为催化剂, 活化能降为 $104.6 \, kJ \cdot mol^{-1}$ 。则

$$
\frac {k _ {\mathrm{催}}}{k _ {\mathrm{非催}}} = \frac {A \exp \left(- \frac {1 0 4 . 6 \times 1 0 ^ {3}}{R T}\right)}{A ^ {\prime} \exp \left(- \frac {1 8 4 . 1 \times 1 0 ^ {3}}{R T}\right)}
$$

假定催化反应和非催化反应的指前因子 A 相等, 则

$$
\frac {k _ {\mathrm{催}}}{k _ {\mathrm{非催}}} = 1. 8 \times 1 0 ^ {8}
$$

人们曾经发现有些催化反应的活化能降低得不多, 但反应速率却改变很大; 也发现在不同催化剂上进行的同一反应, 其活化能相差不大, 但反应速率相差很大, 这些情况可由活化熵的改变来解释。

根据式 (12.50)，若活化熵 $\Delta_{r}^{\neq}S_{m}^{\ominus}$ 改变较大，则能强烈地影响速率常数 $k_{(r)}$ 。例如，乙烯的加氢反应，在金属 W 和 Pt 催化剂上反应的活化能相同，可是由于在 Pt 上反应的活化熵增大，导致指前因子 A 增加，所以反应速率加快。

## 综上所述可知:

(1) 催化剂能加快反应到达平衡的速率, 是由于改变了反应历程, 降低了活化能。至于它怎样降低活化能, 机理如何, 乃是催化研究领域的重要点之一。

(2) 催化剂在反应前后, 其化学性质没有改变, 但在反应过程中由于参与了反应 (可与反应物生成某种不稳定的中间化合物)。所以, 在反应前后, 催化剂本身的化学性质虽不变, 但常有物理性状的改变。例如, 催化 $\mathrm{KClO}_3$ 分解的 $\mathrm{MnO}_2$ 催化剂, 在作用进行后, 从块状变为粉末状。催化 $\mathrm{NH}_3$ 氧化的铂网, 经过几个星期后, 表面就变得比较粗糙。

(3) 催化剂不影响化学平衡。从热力学的观点来看, 催化剂不能改变反应系统的 $\Delta_{\mathrm{r}}G_{\mathrm{m}}^{\ominus}$ 。催化剂只能缩短达到平衡所需的时间, 而不能移动平衡点。对于业已平衡的反应, 不可能借加入催化剂来增加产物的比例。催化剂对正、逆反应都发生同样的影响, 所以正反应的优良催化剂也应为逆反应的催化剂。例如, 苯在 Pt 和 Pd 上容易氢化生成环己烷 (473 \~ 513 K), 而在 533 \~ 573 K 环己烷也能在上述催化剂上脱氢。又如, 在相同条件下, 水合反应的催化剂同时也是脱水反应的催化剂。这个原则很有用。例如, 用 CO 和 H₂ 为原料合成 CH₃OH 是一个很有经济价值的反应, 在常压下寻找甲醇分解反应的催化剂就可作为高压下合成甲醇的催化剂。而直接研究高压反应, 实验条件要麻烦得多。

催化剂不能实现热力学上不能发生的反应。因此，在寻找催化剂时，首先要尽可能根据热力学的原则，核算一下某种反应在该条件下发生的可能性。

(4) 催化剂有特殊的选择性。① 某一类反应只能用某些催化剂来进行催化，如环己烷的脱氢反应只能用 Pt, Pd, Ir, Rh, Cu, Co, Ni 等来催化。② 某一物质只在某一固定类型的反应中，才可以作为催化剂，如新鲜沉淀的氧化铝，对一般有机化合物的脱水都具有催化作用。③ 同一物质在不同催化剂上可得到不同的产物，如 $C_{2}H_{5}OH$ 在 $473 \sim 523 K$ 的金属铜上得到 $CH_{3}CHO + H_{2}$ ; 在 $623 \sim 633 K$ 的

$Al_{2}O_{3}$ (或 $TiO_{2}$ ) 上得到 $C_{2}H_{4} + H_{2}O$ ; 在 $673 \sim 723 K$ 的 ZnO, $Cr_{2}O_{3}$ 上得到丁二烯等。

(5) 有些反应其速率和催化剂的浓度成正比, 这可能是因为催化剂参加了反应成为中间化合物。对于气-固相催化反应, 增加催化剂的用量或增加催化剂的比表面, 都将增加单位时间内的反应量。

(6) 在催化剂或反应系统内加入少量的杂质常可以强烈地影响催化剂的作用, 这些杂质既可成为助催化剂也可成为反应的毒物 (poison)。这表明催化剂的表面并不全是等效的, 存在着具有一定结构的表面活性中心。

## 均相酸碱催化

酸碱催化可分为均相与多相两种。在历史上对均相酸碱催化研究得较多，而对于多相酸碱催化如前所述，由于对表面的吸附态及表面的活性中心研究得还很不充分，所以其理论没有前者的成熟。但均相酸碱催化的某些机理，也可供多相酸碱催化参考。

酸催化反应包含催化剂分子把质子转移给反应物的步骤。因此，催化剂的效率常与酸催化剂的酸强度有关。在酸催化时，酸失去质子的趋势可用它的解离常数 $K_{a}$ 来衡量：

$$
\mathrm{HA} + \mathrm{H} _ {2} \mathrm{O} = \mathrm{H} _ {3} \mathrm{O} ^ {+} + \mathrm{A} ^ {-}
$$

故酸催化反应的速率常数 $k_{a}$ 应与酸的解离常数 $K_{a}$ 成比例。实验表明，二者有如下的关系：

$$
k _ {\mathrm{a}} = G _ {\mathrm{a}} K _ {\mathrm{a}} ^ {\alpha}
$$

或

$$
\lg k _ {\mathrm{a}} = \lg G _ {\mathrm{a}} + \alpha \lg K _ {\mathrm{a}}\tag{12.80}
$$

式中 $G_{a}, \alpha$ 均为常数, 取决于反应的种类和反应条件。表 12.5 给出了以各种酸为催化剂时乙醛水合物 (在丙酮溶液中) 脱水反应的数据, 该反应为

$$
\mathrm{CH} _ {3} \mathrm{CH(OH)} _ {2} \xrightarrow {\text {   催化剂   }} \mathrm{CH} _ {3} \mathrm{CHO} + \mathrm{H} _ {2} \mathrm{O}
$$

以 $\lg k_{a}$ 对 $\lg K_{a}$ ( $K_{a}$ 是在水溶液中测量的解离常数) 作图, 可得图 12.22, 图中的结果符合式 (12.80)。

对于碱催化反应, 碱的催化作用速率常数 $k_{b}$ 同样与它的解离常数 $K_{b}$ 有如下的关系:

$$
k _ {\mathrm{b}} = G _ {\mathrm{b}} K _ {\mathrm{b}} ^ {\beta}\tag{12.81}
$$

表 12.5 以各种酸为催化剂时乙醛水合物脱水反应的数据 (298 K)

<table><tr><td>序号</td><td>酸</td><td> $\frac{\text{催化反应速率常数 }k_a}{\mathrm{dm}^3 \cdot \mathrm{mol}^{-1} \cdot \mathrm{min}^{-1}}$ </td><td>解离常数  $K_a$ </td></tr><tr><td>1</td><td>酚</td><td>0.0181</td><td> $1.06 \times 10^{-10}$ </td></tr><tr><td>2</td><td>邻氯苯酚</td><td>0.112</td><td> $3.2 \times 10^{-9}$ </td></tr><tr><td>3</td><td>间硝基苯酚</td><td>0.160</td><td> $5.3 \times 10^{-9}$ </td></tr><tr><td>4</td><td>邻硝基苯酚</td><td>0.334</td><td> $6.8 \times 10^{-8}$ </td></tr><tr><td>5</td><td>对硝基苯酚</td><td>0.520</td><td> $6.75 \times 10^{-8}$ </td></tr><tr><td>6</td><td>2,4,6-三氯苯酚</td><td>1.53</td><td> $3.9 \times 10^{-7}$ </td></tr><tr><td>7</td><td>丙酸</td><td>18.0</td><td> $1.35 \times 10^{-5}$ </td></tr><tr><td>8</td><td>乙酸</td><td>19.2</td><td> $1.75 \times 10^{-5}$ </td></tr><tr><td>9</td><td>甲酸</td><td>43.5</td><td> $1.8 \times 10^{-4}$ </td></tr><tr><td>10</td><td>2,6-二硝基苯酚</td><td>91.0</td><td> $1.94 \times 10^{-4}$ </td></tr><tr><td>11</td><td>溴代乙酸</td><td>129</td><td> $7.94 \times 10^{-4}$ </td></tr><tr><td>12</td><td>2,4-二硝基苯酚</td><td>183</td><td> $8.32 \times 10^{-5}$ </td></tr><tr><td>13</td><td>苯基丙酸</td><td>225</td><td> $4.17 \times 10^{-5}$ </td></tr><tr><td>14</td><td>二氯乙酸</td><td>773</td><td> $5.50 \times 10^{-2}$ </td></tr></table>

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_200-399_images/7b52cd4e8f9a0fa5e450a199976cf9efe92da0394533333f5832df85f44a0f52.jpg)  
图 12.22 在乙醛水合物的脱水过程中, 各种酸的催化反应速率常数的 Brönsted 关系图 (图中数字即为表 12.5 中的序号)

式中 $G_{b}, \beta$ 均为常数, 也由反应的种类和反应条件决定。式 (12.80) 和式 (12.81) 中的 $\alpha, \beta$ 均为正值, 其值为 $0 \sim 1$ 。

在碱性溶液中碱的解离常数:

$$
\begin{array}{r l} \mathrm {B+ H_ {2} O\xlongequal {\quad} BH^ {+} + OH^ {-}} \\ K _ {\mathrm{b}} = \frac {[ \mathrm {BH^ {+}} ] [ \mathrm {OH^ {-}} ]}{[ \mathrm{B} ]} \end{array}\tag{12.82}
$$

式(12.80)和式(12.81)有时称为 Brönsted 关系式或 Brönsted 定律。如果催化剂是多元酸(或碱)，能解离(或接受)多于一个质子，例如丙二酸 $\mathrm{CH}_{2}(\mathrm{COOH})_{2}$ 或 $PO_{4}^{2-}$ 等，则 Brönsted 关系式应稍加修正。Brönsted 关系式对均相反应能相当好地符合，有时也可适用于非均相反应。

酸或碱催化反应常被解释为经过离子型的中间化合物, 即经过碳正离子或碳负离子而进行的。例如:

$$
\mathrm{S} (\text { 反应物 }) + \mathrm{HA} (\text { 酸催化剂 }) \longrightarrow \mathrm{SH} ^ {+} + \mathrm{A} ^ {-}
$$

$$
\mathrm{SH} ^ {+} + \mathrm{A} ^ {-} \longrightarrow \mathrm{产物} + \mathrm{HA}
$$

或

$$
\mathrm{S} (\text { 反应物 }) + \mathrm{B} (\text { 碱催化剂 }) \longrightarrow \mathrm{S} ^ {-} + \mathrm{HB} ^ {+}
$$

$$
\mathrm{S} ^ {-} + \mathrm{HB} ^ {+} \longrightarrow \text {产物} + \mathrm{B}
$$

具体的例子: 在催化剂 $AlCl_{3}$ 的作用下, 苯与卤代烃的反应称为 Friedel-Crafts 反应, 反应的机理是

$$
\mathrm{C} _ {5} \mathrm{H} _ {1 1}: \ddot {\mathrm{Cl}}: + \underset {\mathrm{Cl}} {\overset {\mathrm{Cl}} {\mathrm{A}}} \mathrm{Al}: \mathrm{Cl} \rightleftharpoons \mathrm{C} _ {5} ^ {+} \mathrm{H} _ {1 1} + [ \mathrm{AlCl} _ {4} ] ^ {-}
$$

$AlCl_{3}$ 是 Lewis 酸, 接受电子对产生碳正离子, 然后再按下式反应:

$$
\mathrm{C} _ {5} ^ {+} \mathrm{H} _ {1 1} \longrightarrow \mathrm{C} _ {5} ^ {-} \mathrm{H} _ {1 1} + \mathrm{H} ^ {+}
$$

$$
[ \mathrm{AlCl} _ {4} ] ^ {-} + \mathrm{H} ^ {+} \longrightarrow \mathrm{AlCl} _ {3} + \mathrm{HCl}
$$

络合催化

络合催化（coordination catalysis）又称为配位催化，泛指在反应过程中，催化剂与反应基团直接形成中间络合物，使反应基团活化。

络合催化是均相催化研究领域中的重点, 自 20 世纪 50 年代初期 Ziegler-Natta 型催化剂 $^{①}$ 出现以来, 以金属络合物为基础的催化剂研究有很大的发展。现在一些过渡金属络合物已成为加氢、脱氢、氧化、异构化、水合、羰基合成、高分子聚合等类型反应过程的重要催化剂。通过对这些催化过程的研究, 络合物催化剂的活性、选择性、稳定性等特点，已经逐渐在工业应用上显示出来。

络合活化催化作用（简称为络合催化）汲取了近代络合物化学和化学键理论方面的成就，并随着这些科学理论和研究方法的发展而兴盛起来。它在化学工业中的重大作用，又促进了络合物化学和化学键理论的进一步发展。尤其重要的是，发现许多具有催化性能的络合物还可以作为反应的中间体被分离出来。通过对这些分离出来的中间体的性质、结构等方面的研究，可以更深入地理解催化反应的机理，这对了解催化作用的本质是非常重要的，从而也对制备和筛选催化剂提供更多的科学依据。

金属特别是过渡金属有很强的络合能力 [过渡金属元素的价电子层有 5 个 $(n-1)$ d, 1 个 ns 和 3 个 np, 共有九个能量相近的原子轨道, 容易组合成 d, s, p 的杂化轨道。这些杂化轨道可以与配体以配键的方式结合而形成络合物]。凡是含有两个及两个以上孤对电子或 $\pi$ 键的分子或离子都可以作为配体, 能生成多种类型的络合物, 其催化活性都与过渡金属原子或离子的化学特性有关, 也就是与过渡金属原子 (或离子) 的电子结构、成键结构有关。同一类催化剂, 有时既可在溶液中起均相催化的作用, 也可以使之成为固体催化剂在多相催化中起作用。例如, 有人以 $PdCl_{2}$ 为催化剂, 在异辛烷溶液中通过均相催化过程将乙烯合成乙酸乙烯; 而负载于 $Al_{2}O_{3}$ 上的 $PdCl_{2}$ 也可用于多相催化过程, 且都是形成 $PdCl_{2}-C_{2}H_{4}$ 中间络合物, 其催化活性也几乎相同。因此, 对于络合催化的研究, 往往可以通过均相催化反应来认识多相催化活性中心的本质和催化作用的机理。

络合催化是 20 世纪中期以后发展起来的, 特别是近年来有很大的进展, 它以化学键理论作为考虑问题的出发点, 并在多相催化中同时考虑一些物理因素的影响。因此, 目前认为络合催化是极有前途的一种催化理论。

由于石油化工中基本有机原料的合成和材料合成工业 (包括高分子材料、复合材料、新型功能材料等), 主要建立在炔烃、烯烃化学的基础上, 并广泛地使用络合催化。所以, 随着我国石油化学工业的发展, 络合催化剂必将获得大量的使用。

络合催化的机理, 一般可表示为

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_200-399_images/9cffe9146bd6b13f9e285c26f4d57b421c0932fd77a5f5ab5a42e84ca8dc6c88.jpg)

式中 M 代表中心金属原子, Y 代表配体, X 代表反应分子。

首先, 反应分子可与配位数不饱和的络合物直接配位, 然后配体 (即反应分子 X) 随即转移插入相邻的 M—Y 键中, 形成 M—X—Y 键 (M—Y 键属于不稳定的配键), 插入反应又使空位恢复, 然后又可重新进行络合和插入反应。所以,络合催化过程中这种“空位中心”和固体催化剂的“表面活性中心”具有相同的作用。在解释催化的活性机理和中毒效应时都可使用这种概念。

以下以乙烯氧化制乙醛为例, 介绍络合催化过程的梗概。

乙烯在氯化钯及氯化铜溶液中氧化成乙醛的方法, 在 1959 年已用于生产, 至今仍不失为生产乙醛的好方法。这一反应可表示为

$$
\mathrm{C} _ {2} \mathrm{H} _ {4} + \mathrm{PdCl} _ {2} + \mathrm{H} _ {2} \mathrm{O} \longrightarrow \mathrm{CH} _ {3} \mathrm{CHO} + \mathrm{Pd} + 2 \mathrm{HCl}\tag{a}
$$

然后 $CuCl_{2}$ 将 Pd 氧化为 $PdCl_{2}$ ，而生成的 CuCl 可以较快地被氧化为 $CuCl_{2}$ ，即

$$
2 \mathrm{CuCl} _ {2} + \mathrm{Pd} \longrightarrow 2 \mathrm{CuCl} + \mathrm{PdCl} _ {2}\tag{b}
$$

$$
2 \mathrm{CuCl} + 2 \mathrm{HCl} + \frac {1}{2} \mathrm{O} _ {2} \longrightarrow 2 \mathrm{CuCl} _ {2} + \mathrm{H} _ {2} \mathrm{O}\tag{c}
$$

总反应式为

$$
\mathrm{C} _ {2} \mathrm{H} _ {4} + \frac {1}{2} \mathrm{O} _ {2} \longrightarrow \mathrm{CH} _ {3} \mathrm{CHO}
$$

当溶液中 $H^{+}$ 和 $Cl^{-}$ 为中等浓度时, 研究得知其动力学方程式为

$$
- \frac {\mathrm{d} [ \mathrm{C} _ {2} \mathrm{H} _ {4} ]}{\mathrm{d} t} = k \frac {[ \mathrm{Pd(II)} ] [ \mathrm{C} _ {2} \mathrm{H} _ {4} ]}{[ \mathrm{H} ^ {+} ] [ \mathrm{Cl} ^ {-} ] ^ {2}}
$$

即对 $[Pd(II)]$ 和 $[C_{2}H_{4}]$ 是一级的，对 $[H^{+}]$ 和 $[Cl^{-}]$ 分别是负一级和负二级。

这个反应的机理可能是, $\mathrm{PdCl}_{2}$ 在足够高浓度的 $\mathrm{Cl}^{-}$ 中以 $[\mathrm{PdCl}_4]^{2-}$ 存在, 它能强烈地与乙烯作用而生成 $[\mathrm{C}_2\mathrm{H}_4\mathrm{PdCl}_3]^{-}$ , 然后该离子与水作用, 发生配位基的置换, 即

$$
[ \mathrm{PdCl} _ {4} ] ^ {2 -} + \mathrm{C} _ {2} \mathrm{H} _ {4} \rightleftharpoons [ \mathrm{C} _ {2} \mathrm{H} _ {4} \mathrm{PdCl} _ {3} ] ^ {-} + \mathrm{Cl} ^ {-}
$$

$$
[ \mathrm{C} _ {2} \mathrm{H} _ {4} \mathrm{PdCl} _ {3} ] ^ {-} + \mathrm{H} _ {2} \mathrm{O} = [ \mathrm{PdCl} _ {2} (\mathrm{H} _ {2} \mathrm{O}) \mathrm{C} _ {2} \mathrm{H} _ {4} ] + \mathrm{Cl} ^ {-}
$$

$$
\left[ \mathrm{PdCl} _ {2} (\mathrm{H} _ {2} \mathrm{O}) \mathrm{C} _ {2} \mathrm{H} _ {4} \right] + \mathrm{H} _ {2} \mathrm{O} = \left[ \mathrm{PdCl} _ {2} (\mathrm{OH}) \mathrm{C} _ {2} \mathrm{H} _ {4} \right] ^ {-} + \mathrm{H} _ {3} \mathrm{O} ^ {+}
$$

反应 (1) 说明反应速率对于 $\left[\mathrm{Pd}(\mathrm{II})\right]$ 和 $\left[\mathrm{C}_{2} \mathrm{H}_{4}\right]$ 是一级的。从反应 (1), (2), (3) 可见, 反应对 $\left[\mathrm{Cl}^{-}\right]$ 是负二级, 而对 $\left[\mathrm{H}^{+}\right]$ 是负一级。

反应下一步是经过插入反应和 $\left[\mathrm{PdCl}_{2}(\mathrm{OH})\mathrm{C}_{2}\mathrm{H}_{4}\right]^{-}$ 的内部重排（即 $\pi$ 络合物 $\left[\mathrm{PdCl}_{2}(\mathrm{OH})\mathrm{C}_{2}\mathrm{H}_{4}\right]^{-}$ 转化为 $\sigma$ 络合物）。

$$
\left[ \begin{array}{c} \mathrm{Cl} \\ \mathrm{Cl} - \mathrm{Pd} - \mathrm {\text {   -   }} \\ \mathrm{OH} \end{array} \right] ^ {-} \Longleftrightarrow \left[ \begin{array}{c} \mathrm{Cl} \\ \mathrm{Cl} - \mathrm{Pd} - \mathrm{CH} _ {2} \mathrm{CH} _ {2} \mathrm{OH} \\ \square \end{array} \right] ^ {-} \tag {4}
$$

此步是乙烯插入金属氧键 (Pd—O) 中去, 所得到的中间体很不稳定, 迅速发生重

排而得到产物乙醛和不稳定的钯氢化合物，后者迅即分解产生金属钯。

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_200-399_images/6cc9c35894737f62aaf994e02480f62d9f044ceb03e772143376f4c9b3394653.jpg)

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_200-399_images/c7c2cb3a42bb5b65742071b5cc6ab1cdfeb23801245c5093d2b99a1ec97de6bc.jpg)

金属 Pd 经 $CuCl_{2}$ 氧化后得到 $PdCl_{2}$ [即反应 (b)], 再参与反应。而生成的 CuCl 又迅速被氧化为 $CuCl_{2}$ [即反应 (c)]。这样就构成循环, 反复使用。

此外, 还有一些重要的络合催化作用, 有些已用于工业生产, 如烯烃氢甲酰化反应 (以钴或铑含膦配位体的羰基化合物为催化剂)、 $\alpha$ -烯烃配位聚合 [以 $\mathrm{TiCl}_4 / \mathrm{Al}(\mathrm{C}_2\mathrm{H}_5)_3$ 为催化剂的乙烯聚合反应, 以及以 $\mathrm{TiCl}_4 / \mathrm{MgCl}_2$ 为催化剂的丙烯聚合反应]、烯烃氧化取代反应 (以 $\mathrm{PdCl}_2 / \mathrm{HCl}$ 为催化剂的乙烯氧化反应)、烯烃歧化反应 [一般用 Ziegler-Natta 型均相催化剂, 如 $\mathrm{WCl}_6 / \mathrm{C}_2\mathrm{H}_5\mathrm{AlCl}_2 / \mathrm{C}_2\mathrm{H}_5\mathrm{OH}, \mathrm{MoCl}_2(\mathrm{NO}_2)_2(\mathrm{Ph})_3 / (\mathrm{CH}_3)_3\mathrm{Al}_2\mathrm{Cl}_3]$ 、甲醇羰基化和甲酯羰基化反应 (催化剂都是铑的络合物) 等。

总之, 在络合催化过程中, 或者催化剂本身是络合物, 或者反应历程中催化剂与反应物生成了络合物, 因此在研究催化反应的历程时, 需要充分考虑到络合物的结构特点。

络合反应可以在单相中进行, 也可以在复相中进行。在单相中粒子的接触多, 因此在不太高的温度下就可具有较高的活性, 所以单相络合在化工生产中广泛应用于加氢、脱氢、异构化羟基合成、聚合反应等。其缺点是催化剂与反应混合物的分离问题, 这不仅在络合催化中, 即使在一般的均相催化中都存在这一问题。因此, 如何使均相催化多相化, 是值得进一步研究的课题。

## 酶催化反应

在生物体中进行的各种复杂的反应, 如蛋白质、脂肪、糖类的合成和分解等基本上都是酶催化作用 (enzyme catalysis)。绝大部分已知的酶本身也是一种蛋白质, 其质点的直径在 10 \~ 100 nm。因此, 酶催化作用可看作介于均相与非均相催化之间, 既可以看成反应物与酶形成了中间化合物, 也可以看成在酶的表面上首先吸附了底物 [在讨论酶催化作用时常将反应物叫作底物 (substrate)], 而后再进行反应。

实验证明, 酶催化作用的速率与酶、底物、温度、pH 及其他干扰物质有关。在定温下, 对于某一特定的酶催化作用, 典型的酶催化反应速率曲线如图 12.23 所示 (图中纵坐标为反应速率, 横坐标为底物的浓度 [S])。当底物的浓度 [S] 很大时, 反应速率 $\left(-\frac{\mathrm{d}[\mathrm{S}]}{\mathrm{d}t}\right)$ 与 [S] 无关 (水平线段), 只与酶的总浓度成正比。而当 [S] 的数值较小时, 反应速率与 [S] 成线性关系, 且与酶的总浓度也成正比。

Michaelis 和 Menten 研究了酶催化反应动力学, 提出了酶催化反应的历程, 即 Michaelis-Menten 机理, 指出酶 (E) 与底物 (S) 先形成中间化合物 (ES), 然后中间化合物 (ES) 再进一步分解为产物, 并释放出酶 (E):

$$
\mathrm{S} + \mathrm{E} \xrightarrow [ k _ {- 1} ]{k _ {1}} \mathrm{ES} \xrightarrow {k _ {2}} \mathrm{E} + \mathrm{P}
$$

ES 分解为产物 (P) 的速率很慢, 它控制着整个反应的速率。采用稳态近似法处理:

$$
\frac {\mathrm{d} [ \mathrm{ES} ]}{\mathrm{d} t} = k _ {1} [ \mathrm{S} ] [ \mathrm{E} ] - k _ {- 1} [ \mathrm{ES} ] - k _ {2} [ \mathrm{ES} ] = 0
$$

所以

$$
[ \mathrm{ES} ] = \frac {k _ {1} [ \mathrm{E} ] [ \mathrm{S} ]}{k _ {- 1} + k _ {2}} = \frac {[ \mathrm{E} ] [ \mathrm{S} ]}{K _ {\mathrm{M}}}\tag{12.83}
$$

式中 $K_{M} = \frac{k_{-1} + k_{2}}{k_{1}} = \frac{[E][S]}{[ES]}$ ，称为米氏常数 (Michaelis constant)，它实际上相当于反应 $E + S = ES$ 的不稳定常数。这个公式叫米氏公式。所以，反应速率为

$$
r = \frac {\mathrm{d} [ \mathrm{P} ]}{\mathrm{d} t} = k _ {2} [ \mathrm{ES} ]
$$

将 [ES] 的表示式代入后, 得

$$
r = k _ {2} [ \mathrm{ES} ] = \frac {k _ {2} [ \mathrm{E} ] [ \mathrm{S} ]}{K _ {\mathrm{M}}}\tag{12.84}
$$

若令酶的原始浓度为 $[\mathrm{E}_0]$ , 反应达稳态后, 它一部分变为中间化合物 [ES], 另一部分仍处于游离状态。所以

$$
[ \mathrm{E} _ {0} ] = [ \mathrm{E} ] + [ \mathrm{ES} ]
$$

或

$$
[ \mathrm{E} ] = [ \mathrm{E} _ {0} ] - [ \mathrm{ES} ]
$$

代入式 (12.83) 后, 得

$$
[ \mathrm{ES} ] = \frac {[ \mathrm{E} _ {0} ] [ \mathrm{S} ]}{K _ {\mathrm{M}} + [ \mathrm{S} ]}
$$

故

$$
r = k _ {2} [ \mathrm{ES} ] = \frac {k _ {2} [ \mathrm{E} _ {0} ] [ \mathrm{S} ]}{K _ {\mathrm{M}} + [ \mathrm{S} ]}\tag{12.85}
$$

如以反应速率 r 为纵坐标, 以底物浓度 [S] 为横坐标, 按式 (12.85) 作图, 则得图 12.23。当 [S] 很大时, $K_{M} \ll [S]$ , $r = k_{2}[E_{0}]$ , 即反应速率与酶的总浓度成正比, 而与 [S] 的浓度无关, 对 [S] 来说是零级反应。

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_200-399_images/c773f22331739a539e87c8d1ed1c394e495e2b5406c91f057716a274136215d4.jpg)  
图 12.23 典型的酶催化反应速率曲线

当 [S] 很小时, $K_{\mathrm{M}} + [\mathrm{S}] \approx K_{\mathrm{M}}$ , $r = \frac{k_2}{K_{\mathrm{M}}} [\mathrm{E}_0][\mathrm{S}]$ , 反应对 [S] 来说是一级反应。这一结论与实验事实是一致的。

当 $[\mathrm{S}] \to \infty$ 时, 速率趋于极大 $(r_{\mathrm{m}})$ , 即 $r_{\mathrm{m}} = k_{2}[\mathrm{E}_{0}]$ , 代入式 (12.85), 得

$$
\frac {r}{r _ {\mathrm{m}}} = \frac {[ \mathrm{S} ]}{K _ {\mathrm{M}} + [ \mathrm{S} ]}\tag{12.86}
$$

当 $r = \frac{r_{\mathrm{m}}}{2}$ 时， $K_{\mathrm{M}} = [\mathrm{S}]$ ，也就是说当反应速率达到最大速率的一半时，底物的浓度就等于米氏常数。

将式 $(12.86)$ 重排后, 可得

$$
\frac {1}{r} = \frac {K _ {\mathrm{M}}}{r _ {\mathrm{m}}} \cdot \frac {1}{[ \mathrm{S} ]} + \frac {1}{r _ {\mathrm{m}}}\tag{12.87}
$$

如将 $\frac{1}{r}$ 对 $\frac{1}{[\mathrm{S}]}$ 作图，从直线的斜率可得 $\frac{K_{\mathrm{M}}}{r_{\mathrm{m}}}$ ，从直线的截距可求得 $\frac{1}{r_{\mathrm{m}}}$ ，二者联立从而可解出 $K_{\mathrm{M}}$ 和 $r_{\mathrm{m}}$ 。

许多酶催化反应都能满足式 (12.85)，但这并不能作为中间化合物存在的绝对证明。人们用吸收光谱的方法，曾经证明了对于一些酶催化反应在反应过程中

确实存在着中间化合物。

研究酶的抑制机理, 对于药学、生理学有重要的意义。通过对抑制作用的研究, 可以了解一些生理过程及药物的作用 (在人体内的化学反应, 绝大多数都是酶催化反应)。

抑制作用有很多种, 其中一种叫竞争性抑制作用 (competitive inhibition)。这类抑制剂与底物的分子结构及大小相似, 它可以占据酶上的活性位置, 因而与底物发生竞争。如以 I 代表抑制剂, 则

$$
\begin{array}{r l}\mathrm{E} + \mathrm{S}&\underset {k _ {- 1}} {\overset {k _ {1}} {\rightleftharpoons}} \mathrm{ES} \xrightarrow {k _ {2}} \mathrm{E} + \mathrm{P}\\&\mathrm{E} + \mathrm{I} \underset {k _ {- 3}} {\overset {k _ {3}} {\rightleftharpoons}} \mathrm{EI}\\&[ \mathrm{E} ] = [ \mathrm{E} _ {0} ] - [ \mathrm{ES} ] - [ \mathrm{EI} ]\end{array}\tag{12.88}
$$

令

$$
K _ {\mathrm{M}} = \frac {[ \mathrm{E} ] [ \mathrm{S} ]}{[ \mathrm{ES} ]} \quad K _ {\mathrm{I}} = \frac {[ \mathrm{E} ] [ \mathrm{I} ]}{[ \mathrm{EI} ]}
$$

则

$$
[ \mathrm{E} ] = \frac {K _ {\mathrm{M}} [ \mathrm{ES} ]}{[ \mathrm{S} ]} \quad [ \mathrm{EI} ] = \frac {[ \mathrm{E} ] [ \mathrm{I} ]}{K _ {\mathrm{I}}}
$$

代入式 (12.88), 整理后得

$$
[ \mathrm{ES} ] = \frac {[ \mathrm{E} _ {0} ]}{\frac {K _ {\mathrm{M}}}{[ \mathrm{S} ]} + 1 + \frac {K _ {\mathrm{M}} [ \mathrm{I} ]}{K _ {\mathrm{I}} [ \mathrm{S} ]}}
$$

反应速率

$$
r = k _ {2} [ \mathrm{ES} ] = \frac {k _ {2} [ \mathrm{E} _ {0} ]}{\frac {K _ {\mathrm{M}}}{[ \mathrm{S} ]} + 1 + \frac {K _ {\mathrm{M}} [ \mathrm{I} ]}{K _ {\mathrm{I}} [ \mathrm{S} ]}}
$$

当[S]很大时, $r_{m}=k_{2}[E_{0}]$ ,这和没有抑制作用时是一样的。上式也可以写作

$$
r = \frac {r _ {\mathrm{m}} [ \mathrm{S} ]}{[ \mathrm{S} ] + K _ {\mathrm{M}} \left(1 + \frac {[ \mathrm{I} ]}{K _ {\mathrm{I}}}\right)}
$$

或

$$
\frac {1}{r} = \frac {K _ {\mathrm{M}}}{r _ {\mathrm{m}}} \left(1 + \frac {[ \mathrm{I} ]}{K _ {\mathrm{I}}}\right) \frac {1}{[ \mathrm{S} ]} + \frac {1}{r _ {\mathrm{m}}}\tag{12.89}
$$

如将 $\frac{1}{r}$ 对 $\frac{1}{[\mathrm{S}]}$ 作图, 与式 (12.87) 相比较, 其截距与没有抑制作用时是一致的, 但直线的斜率却不同。

酶催化反应有以下突出的特点。

(1) 高度的选择性和单一性。一种酶通常只能催化一种反应, 而对其他反应不具有活性 (如脲酶只能将尿素转化为氨及 $CO_{2}$ )。

(2) 酶催化反应的催化效率非常高, 比一般的无机或有机催化剂可高出 $10^{8} \sim 10^{12}$ 倍。例如, 一个过氧化氢分解酶的分子能在 $1 \mathrm{~s}$ 内分解 $10^{5}$ 个 $\mathrm{H}_{2} \mathrm{O}_{2}$ 分子; 而石油裂解所使用的硅酸铝催化剂, 在 $773 \mathrm{~K}$ 下, 约 $4 \mathrm{~s}$ 才分解一个烃分子。

(3) 酶催化反应所需的条件温和, 一般在常温常压下即可进行。例如, 合成氨工业需高温 (约 $770 \mathrm{~K}$ ) 高压 (约 $3 \times 10^{6} \mathrm{~Pa}$ ), 且需特殊设备。而某些植物根部的生物固氮酶, 非但能在常温常压下固定空气中的氮, 而且能将它还原成氨。

(4) 酶催化反应同时具有均相反应和多相反应的特点。酶本身是呈胶体状而又分散的, 接近于均相, 但是酶催化的反应过程是反应物聚集 (或被吸附) 在酶的表面上进行的, 这又与多相反应类似。

(5) 酶催化反应的历程复杂 (从而速率方程复杂), 酶反应受 pH、温度及离子强度的影响较大。酶本身的结构极其复杂, 而且酶的活性是可以调节的, 如此等等, 这就增加了研究酶催化反应的难度。

酶催化反应越来越多地受到人们的重视, 不仅仅是由于发酵化工生产及污水处理等过程中需要借助于酶来完成, 更重要的是它在生物学中的重要性, 没有酶的存在, 几乎所有的生理反应和生命过程均将停止, 许多疾病的发生也源于酶反应的失调。人们需要深入研究酶反应的机理, 以解决许多疑难病症, 为人类造福。

酶反应的高效性和专一性是由酶分子本身的结构所决定的。在生物体内的酶是由20种氨基酸以不同的方式(即双螺旋结构)所组成的大分子,它盘旋、折叠构成了极其复杂的空间结构,酶催化的活性中心一般就位于表面具有特定的空间结构之中。

## \*自催化反应和化学振荡

在给定条件下的反应系统中, 反应开始后逐渐形成并积累了某种产物或中间体 (如自由基), 这些产物具有催化功能, 使反应经过一段诱导期后速率大大加快, 这种作用称为自 (动) 催化作用 (autocatalysis)。

简单的自催化反应, 常包含三个连续进行的动力学步骤, 例如:

$$
\mathrm{A} \xrightarrow {k _ {1}} \mathrm{B} + \mathrm{C}\tag{1}
$$

$$
\mathrm{A} + \mathrm{B} \xrightarrow {k _ {2}} \mathrm{AB}\tag{2}
$$

$$
\mathrm{AB} \xrightarrow {k _ {3}} 2 \mathrm{B} + \mathrm{C}\tag{3}
$$

在反应 (1) 中, 起始反应物较缓慢地分解为 B 和 C, 产物中 B 具有催化功能, 与反应物 A 络合, 如反应 (2) 所示。然后, AB 络合体再分解为产物 C, 同时释放出 B, 如反应 (3) 所示。在反应过程中, 一旦有 B 生成, 反应就自动加速。自催化反应多见于均相催化, 其特征之一是存在着初始的诱导期。

实践证明, 少量的抑制剂 (inhibitor) 就能有效地使自催化反应受到抑制。但是, 当抑制剂消耗完, 解除了抑制效应后, 自催化反应仍能继续进行。

油脂腐败、橡胶变质及塑料制品的老化等均属包含链反应的自氧化过程, 反应开始时进行得很慢, 但都能被其自身所产生的自由基所加速。因此, 大多数自氧化过程存在着自催化作用。

自催化反应在工业上有时也有实用价值, 可以不断地添加原料, 使产物与新添加的原料充分混合, 保持添加物的比例, 并控制一定的反应条件, 以使反应系统处于稳态而反应速率则始终保持最快。

有些自催化反应有可能使反应系统中某些物质的浓度随时间 (或空间) 发生周期性的变化, 即发生化学振荡 (chemical oscillation), 而发生化学振荡反应的必要条件之一是该反应必须是自催化反应。

现举两个化学振荡反应的例子。

(1) 在一个装有搅拌装置的烧杯中, 首先将 4.292 g 丙二酸和 0.175 g 硝酸铈铵溶于 $0.150 \, dm^{3}$ 、浓度为 $1.0 \, mol \cdot dm^{-3}$ 的硝酸溶液中。开始溶液呈黄色, 几分钟后变清。在溶液变清后加入 1.415 g NaBr, 溶液的颜色就会在黄色和无色之间振荡, 振荡周期约为 1 min。如果另外加入几毫升浓度为 $0.025 \, mol \cdot dm^{-3}$ 的试亚铁灵试剂 (ferroin, 又称为邻二氮菲亚铁离子), 则溶液的颜色会在红色和蓝色之间振荡, 可持续 1 h 左右。

(2) 先配制三种溶液: ① 将 $3.0 \mathrm{~cm}^{3}$ 浓硫酸和 $10 \mathrm{~g} \mathrm{NaBrO}_{3}$ 溶解在 $134 \mathrm{~cm}^{3}$ 水中, 得溶液 a; ② 将 $1 \mathrm{~g} \mathrm{NaBr}$ 溶解在 $10 \mathrm{~cm}^{3}$ 水中, 得溶液 b; ③ 将 $2 \mathrm{~g}$ 丙二酸溶解在 $20 \mathrm{~cm}^{3}$ 水中, 得溶液 c。在一个小烧杯中先加入 $6 \mathrm{~cm}^{3}$ 溶液 a, 再加入 $0.5 \mathrm{~cm}^{3}$ 溶液 b, 然后加入 $1.0 \mathrm{~cm}^{3}$ 溶液 c。等待几分钟, 溶液变清后再加入 $1.0 \mathrm{~cm}^{3}$ 浓度为 $0.025 \mathrm{~mol} \cdot \mathrm{dm}^{-3}$ 的试亚铁灵试剂, 充分混合后放入一个直径为 $0.09 \mathrm{~m}$ 的医用培养皿中并加上盖。此时溶液呈均匀的红色, 几分钟后溶液中出现蓝色, 并呈环状向外扩展, 形成各种同心圆形花纹。如果轻轻地倾斜培养皿, 破坏掉扩展的波前峰, 可形成螺旋状的花纹, 并且时空有序。

自从 1958 年 Belousov 首次报道, 在以金属铈离子作催化剂时, 柠檬酸被 HBrO₃ 氧化可呈现化学振荡现象之后, Zhabotinskii 等人已报道了有些反应系统可呈现空间有序。在这之后, 又发现了一批溴酸盐的类似反应。由于历史原因, 人们将此类反应统称为 B-Z 反应, 它们都是自催化反应。关于 B-Z 反应的机理, 虽然已经做了大量的研究, 提出了一些机理, 其中有些机理已为人们所接受, 但总的说来, 对于产生时空有序现象的详细机理, 还需要做进一步研究。

可以从动力学的角度来分析化学振荡反应。设系统是由 A, B 两组分所构成的，以 [A], [B] 表示其浓度，反应的速率方程设为

$$
\begin{array}{l} \frac {\mathrm{d} [ \mathrm{A} ]}{\mathrm{d} t} = f ([ \mathrm{A} ], [ \mathrm{B} ]) \\ \frac {\mathrm{d} [ \mathrm{B} ]}{\mathrm{d} t} = \phi ([ \mathrm{A} ], [ \mathrm{B} ]) \end{array}
$$

式中 $f, \phi$ 是 [A], [B] 的非线性函数。如果系统处于稳态，则

$$
f ([ \mathrm{A} ] _ {\mathrm{s}}, [ \mathrm{B} ] _ {\mathrm{s}}) = \phi ([ \mathrm{A} ] _ {\mathrm{s}}, [ \mathrm{B} ] _ {\mathrm{s}}) = 0
$$

式中下标“s”代表稳态。若偏离稳态，则可得

$$
\frac {\mathrm{d} [ \mathrm{A} ]}{\mathrm{d} [ \mathrm{B} ]} = \frac {f ([ \mathrm{A} ] , [ \mathrm{B} ])}{\phi ([ \mathrm{A} ] , [ \mathrm{B} ])}
$$

对这一微分方程求解, 就得到一个联系 [A], [B] 的公式, 称为反应轨迹曲线 (因为若以 [A], [B] 为坐标, 根据公式就可描绘出一条反应过程中 A, B 浓度的变化曲线)。如果轨迹是封闭曲线, 则 A 与 B 的浓度就能沿曲线稳定地周期性变化, 反应便呈振荡现象。

曾经提出过不少模型来研究化学振荡反应的机理, 如 Lotka-Volterra 的自催化模型:

$$
\begin{array}{l l} \text {(1) A + X} \xrightarrow {k _ {1}} 2 \mathrm{X} & r _ {1} = - \frac {\mathrm{d} [ \mathrm{A} ]}{\mathrm{d} t} = k _ {1} [ \mathrm{A} ] [ \mathrm{X} ] \\ \text {(2) X + Y} \xrightarrow {k _ {2}} 2 \mathrm{Y} & r _ {2} = - \frac {\mathrm{d} [ \mathrm{X} ]}{\mathrm{d} t} = k _ {2} [ \mathrm{X} ] [ \mathrm{Y} ] \\ \text {(3) Y} \xrightarrow {k _ {3}} \mathrm{E} & r _ {3} = \frac {\mathrm{d} [ \mathrm{E} ]}{\mathrm{d} t} = k _ {3} [ \mathrm{Y} ] \end{array}
$$

其净反应则是 A $\longrightarrow$ E。对这一组微分方程求解 (过程从略)，得到

$$
k _ {2} [ \mathrm{X} ] - k _ {3} \mathrm{ln} [ \mathrm{X} ] + k _ {2} [ \mathrm{Y} ] + k _ {1} [ \mathrm{A} ] \mathrm{ln} [ \mathrm{Y} ] = \text {常数}
$$

这一方程的具体解, 可用两种方法表示, 一种是用 [X] 和 [Y] 对时间 t 作图, 得图 12.24, 其浓度随时间呈周期性变化; 另一种是以 [X] 对 [Y] 作图, 得图 12.25, 表明反应轨迹为一封闭椭圆曲线。

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_200-399_images/43d55010c13d6286bdfa65e766a41da9ec3bb25ed0f12efa4a7f5bfe1eda8ecf.jpg)  
图 12.24 [X] 和 [Y] 随时间的周期性变化

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_200-399_images/0d7e0aa37c0ac6c7f4fd3556016e63a5d90f95b9c5e465892629241ca9664da1.jpg)  
图 12.25 不同起始反应物浓度出现的不同封闭轨迹

如果系统是敞开系统, 在反应过程中不断地提供 A (如在流动系统中不断加入 A), 最终产物 E 对反应无多大影响, 移去与否均可。由于 A 的不断补充, 系统总是远离平衡态, 始终保持 $\Delta_{r}G_{m}$ 为较负的值, 以便有足够的驱动力使反应自发进行。倘若不补充 A, A 不断消耗, 反应的振荡是不会维持多久的。

中间产物 X, Y 的浓度的周期性变化可以解释为: 反应开始时其速率可能并不快, 但由于反应 (1) 生成了 X, 而 X 又能自催化反应 (1), 所以 X 骤增。随着 X 的生成, 使反应 (2) 发生。开始 Y 的量可能是很少的, 故反应 (2) 较慢, 但反应 (2) 生成的 Y 又能自催化反应 (2), 使 Y 的量骤增。但是, 在增加 Y 的同时是要消耗 X 的, 则反应 (1) 的速率变慢, 生成 X 的量减少。而 X 量减少又导致反应 (2) 的速率变慢。随着 Y 量的减少, 消耗 X 的量也减少, 从而使 X 的量再次增加。如此反复进行, 表现为 X, Y 浓度的周期性变化。

Lotka 是美国生态学家, Volterra 是意大利数学家, 他们最初为模拟生态现象而提出上述动力学模型, 在自然界中有些动物的数量并不总是单调地变化, 而是可以随时间振荡。例如, 在亚得里亚海中有两种鱼类常常交替出现。假如把 X 和 Y 看作两种鱼类, A 是某种营养物质, 则前述 Lotka-Volterra 模型可代表鱼 X 吃了营养物质 A 而增殖, 鱼 Y 吃了鱼 X 而增殖, 同时鱼 Y 会自然死亡变成 E。这个模型也可以模拟其他生态过程, 例如可以把 A 看作草, X 看作鹿, Y 看作狼, 于是鹿吃草而增殖, 狼吃鹿而增殖, 同时狼自然死亡。

另一个有趣的振荡反应模型称为 Brusselator 振荡器 (是由 Prigogine 的研究组在 Brussels 提出来的), 这个模型由如下几步构成:

$$
\begin{array}{l l} \text {(1) A} \xrightarrow {k _ {1}} \mathrm{X} & \frac {\mathrm{d} [ \mathrm{X} ]}{\mathrm{d} t} = k _ {1} [ \mathrm{A} ] \\ \text {(2) 2X + Y} \xrightarrow {k _ {2}} 3 \mathrm{X} & - \frac {\mathrm{d} [ \mathrm{Y} ]}{\mathrm{d} t} = k _ {2} [ \mathrm{X} ] ^ {2} [ \mathrm{Y} ] \\ \text {(3) B + X} \xrightarrow {k _ {3}} \mathrm{Y+C} & \frac {\mathrm{d} [ \mathrm{Y} ]}{\mathrm{d} t} = k _ {3} [ \mathrm{B} ] [ \mathrm{X} ] \\ \text {(4) X} \xrightarrow {k _ {4}} \mathrm{D} & - \frac {\mathrm{d} [ \mathrm{X} ]}{\mathrm{d} t} = k _ {4} [ \mathrm{X} ] \end{array}
$$

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_200-399_images/ec119642eb99ec7df1d40ddf6d44a99f084b8cfc2c54eaa5ad2fec9ca21bc78b.jpg)  
图 12.26 极限环示意图 (1)

反应物 A 和 B 的浓度仍以不断供给的方式维持为定值 (敞开系统)。在上列一组微分方程中, 只有 [X], [Y] 两个变数。采用稳态处理法可以解出 [X], [Y] 的值。计算结果用图 12.26 表示。有趣的是不管系统中 A, B 的起始浓度如何 (也即不管 X 和 Y 的起始浓度如何), 反应的结果, 系统中 X, Y 的浓度变化总是会进入同一个封闭轨迹。这个封闭轨迹称为极限环 (limit cycle), 如图 12.26 所示, 循环周期则与反应的速率常数有关。

对于前面所举的 B-Z 反应的第一个实例, $Br^{-}$ 和 $Ce^{4+}$ , $Ce^{3+}$ 浓度呈周期性变化, 其反应历程也是十分复杂的。Noyes

曾提出过一个较为合理的反应模型, 其中包括 18 个基元反应和 21 种物质, 其主要步骤可用如下的简化模型表示:

(1) $\mathrm{A} + \mathrm{Y}\longrightarrow \mathrm{X}$

(2) $\mathrm{X} + \mathrm{Y}\longrightarrow \mathrm{C}$

(3) $\mathrm{B} + \mathrm{X}\longrightarrow 2\mathrm{X} + \mathrm{Z}$

(4) $2\mathrm{X}\longrightarrow \mathrm{D}$

(5) Z $\longrightarrow$ Y

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_200-399_images/cce79c1e8bd8b449f660e3c0b8cf0bacfb19b1a3179cfcd1267978a1af1377f3.jpg)  
图 12.27 极限环示意图 (2)

这种简化模型又称为 Oregonator (是由 Noyes 及其研究组在 Oregon 研究出来的)。反应式中 X 表示 $HBrO_{2}$ ，Y 表示 $Br^{-}$ ，Z 表示 $2Ce^{4+}$ ，[A]，[B]，[C]，[D] 在反应过程中保持恒定，其中步骤 (3) 是自催化反应。根据上述模型，可写出一个微分方程组，解这方程组就可得到 X，Y 和 Z 浓度的周期性变化情况，如图 12.27 所示。

综上所述, 振荡现象的发生必须满足如下几个条件: ① 反应必须是敞开系统, 且远离平衡态; ② 反应历程中应包含有自催化的步骤; ③ 系统必须有两个稳态存在, 即具

有双稳定性 (bistability) (可形象化地用钟摆比喻, 在给定条件下, 当钟摆摆动到右方最高点后, 它就会自动地摆向左方的最高点; 当化学反应中红色的组分增加到一定程度后, 它就会自动地向产生蓝色组分的方向变化)。

振荡现象在生物化学中有很多例子, 如动物心脏有节律地跳动; 在新陈代谢过程中占重要地位的糖酵解反应中, 许多中间化合物和酶的浓度是随时间而周期性变化的 (振荡周期为几分钟的数量级)。所谓的生物钟 (biological bell), 也是一种生物振荡现象。

生物的有序不仅表现在时间上, 也表现在空间特性上。例如, 许多树叶的形状、蝴蝶翅膀上的花纹、动物的皮毛等都呈现出很漂亮的规则图案, 这些现象是无法用 Boltzmann 的有序原理来解释的, 甚至可以说是背道而驰的。按照达尔文的生物进化论以及社会学家关于人类社会的进化学说, 发展过程趋向于种类繁多, 结构和功能变得复杂。但无论是生物系统还是社会系统, 总是趋于更加有序, 更加有组织, 而不像物理学家和化学家所预言的总是趋向于平衡和无序。这两种观念是截然不同的, 直到 20 世纪 60 年代末, Prigogine 学派对不可逆过程热力学取得重大成就后才有所了解。振荡反应必然是耗散结构, 化学振荡的动力学具有非线性的微分速率方程。Prigogine 把那种在开放和远离平衡的条件下, 在与外界环境交换物质和能量的过程中, 通过采用适当的有序结构状态来耗散环境传来的能量与物质 (由于它是敞开系统, 因此不能像封闭系统那样采取无序的结构来耗散环境传来的能量), 在耗散过程中, 以内部的非线性动力学机制来形成和维持的宏观时空有序结构称为 “耗散结构” (dissipative structure)。

## 拓展学习资源

<table><tr><td>重点内容及公式总结</td><td><img src="images/8034f2947044d49eed1bfcdbe36e158bf93000cdcbb2a5372daef992609de674.jpg"/></td></tr><tr><td>课外参考读物</td><td><img src="images/c434652f228439d06999cc655268201507d77568b71bd3b9e76a59a65f91c428.jpg"/></td></tr><tr><td>相关科学家简介</td><td><img src="images/be19e704c15117e9ebea04134591ff45c417922fb1bdfe7d26182c006c4e5526.jpg"/></td></tr><tr><td>教学课件</td><td><img src="images/72260ddabac1e1208a451f99b430af85627f928dafe74fe44f81fe8c2e437051.jpg"/></td></tr></table>

12.1 简述碰撞理论和过渡态理论所用的模型、基本假设和优缺点。

12.2 碰撞理论中的阈能 $E_{\mathrm{c}}$ 的物理意义是什么？与Arrhenius活化能 $E_{\mathrm{a}}$ 在数值上有何关系？

12.3 碰撞理论中为什么要引入概率因子 $P? P$ 一般小于1的主要原因是什么？

12.4 有一双分子气相反应 A(g) + B(g) $\longrightarrow$ P(g)，如用简单碰撞理论计算其指前因子，所得的数量级约为多少？

12.5 过渡态理论中的活化焓 $\Delta_{r}^{\neq}H_{m}^{\ominus}$ 与 Arrhenius 活化能 $E_{a}$ 在物理意义和数值上各有何不同？如有一气相反应 A(g) + BC(g) $\longrightarrow$ AB(g) + C(g)，试导出 $\Delta_{r}^{\neq}H_{m}^{\ominus}$ 与 $E_{a}$ 之间的关系。若反应为 A(g) + B(l) $\longrightarrow$ P(g)，则 $\Delta_{r}^{\neq}H_{m}^{\ominus}$ 与 $E_{a}$ 之间的关系又将如何？

12.6 在常温下, 过渡态理论中的普适因子 $\frac{k_{\mathrm{B}} T}{h}$ 的单位是什么? 数量级约为多少?

12.7 试证明气相基元反应 A(g) + B(g) → 2C(g) 的指前因子为

$$
A = \frac {k _ {\mathrm{B}} T}{h} \mathrm{e} ^ {2} (c ^ {\ominus}) ^ {- 1} \exp \left(\frac {\Delta_ {\mathrm{r}} ^ {\mp} S _ {\mathrm{m}} ^ {\ominus}}{R}\right)
$$

若气相基元反应为 $2\mathrm{A}(\mathrm{g}) \longrightarrow \mathrm{C}(\mathrm{g})$ 或 $\mathrm{A}(\mathrm{g}) + 2\mathrm{B}(\mathrm{g}) \longrightarrow \mathrm{C}(\mathrm{g})$ ，A 的表示式又将如何？

12.8 溶剂对化学反应的速率有哪些影响 (包括物理方面和化学方面)? 所谓 “笼效应” 和 “遭遇” 其含义是什么? 原盐效应与离子所带电荷及离子强度有何关系? 对下述几个反应, 若增加溶液中的离子强度, 则其反应速率常数增大、减小还是不变?

(1) $\mathrm{NH_4^+ + CNO^- = CO(NH_2)_2}$

(2) $\mathrm{CH}_3\mathrm{COOC}_2\mathrm{H}_5 + \mathrm{OH}^-\longrightarrow \mathrm{P}$

(3) $\mathrm{S}_2\mathrm{O}_3^{2-} + \mathrm{I}^- \longrightarrow \mathrm{P}$

12.9 常用的测试快速反应的方法有哪些？用弛豫法测定快速反应的速率常数，实验中主要是测定什么数据？弛豫时间的含意是什么？试推导对峙反应 $\mathrm{A(g) + B(g)}\xrightarrow[k_{-2}]k_2}\mathrm{G(g) + H(g)}$ 的弛豫时间 $\tau$ 与 $k_{2},k_{-2}$ 之间的关系。

12.10 化学反应动力学分为总包反应、基元反应和态-态反应三个层次, 何谓态-态反应？它与宏观反应动力学的主要区别是什么？当前研究分子反应动态学的主要实验方法有哪几种？

12.11 何谓通-速-角等高图 [参见正文图 12.12(b) 和图 12.13(b)]? 在质心坐标系中, 相对于入射分子束的方向, 产物分子散射的角度分布有哪几种基本类型? 从产物的角度分布可获得哪些关于微观反应的信息?

12.12 通过交叉分子束实验可研究态-态反应, 其装置主要由哪几部分组成? 何谓红外化学发光和激光诱导荧光? 它们在化学反应动力学的研究中有何作用?

12.13 何谓受激单重态和三重态？荧光与磷光有何异同？电子激发态和能量衰减通常有多少种方式？

12.14 何谓量子产率？光化学反应与热反应相比有哪些不同之处？有一光化学初级反应为 $A + h\nu \longrightarrow P$ ，设单位时间、单位体积吸光的强度为 $I_{a}$ ，试写出该初级反应的速率表示式。若 A 的浓度增加一倍，速率表示式有何变化？

12.15 与非催化反应相比, 催化反应有哪些特点? 某一反应在一定条件下的平衡转化率为 $25.3\%$ , 当有某催化剂存在时, 反应速率增加了 20 倍。若保持其他条件不变, 问转化率为多少? 催化剂能加速反应的本质是什么?

12.16 溴和丙酮在水溶液中发生如下反应:

$$
\mathrm{CH} _ {3} \mathrm{COCH} _ {3} (\mathrm{aq}) + \mathrm{Br} _ {2} (\mathrm{aq}) \longrightarrow \mathrm{CH} _ {3} \mathrm{COCH} _ {2} \mathrm{Br} (\mathrm{aq}) + \mathrm{HBr} (\mathrm{aq})
$$

实验得出的动力学方程对 $Br_{2}$ 为零级, 所以说反应中 $Br_{2}$ 起了催化剂作用。这种说法对不对? 为什么? 如何解释这样的实验事实。

12.17 简述酶催化反应的一般历程、动力学处理方法和特点。

12.18 何谓自催化反应和化学振荡？化学振荡反应的发生有哪几个必要条件？化学振荡反应有何特点？

习题

12.1 当温度为 298 K, 压力为 (1) $10p^{\ominus}$ , (2) $p^{\ominus}$ , (3) $10^{-6}p^{\ominus}$ 时, 一个氩原子在 1 s 内受到多少次碰撞 (碰撞截面 $\sigma$ 可视为 $36\ nm^{2}$ )?

12.2 对 HI 的热分解反应进行动力学研究, 当 $T = 300^{\circ}C$ , 在 $1 \, m^{3}$ 容器中存在 $1 \, mol \, HI$ 时, 求碰撞频率。已知 HI 分子的碰撞直径为 $0.35 \, nm$ 。

12.3 恒容下, $300 \mathrm{~K}$ 时, 温度每升高 $10 \mathrm{~K}$ :

(1) 计算碰撞频率增加的分数;

(2) 计算碰撞时在分子连心线上的相对平动能超过 $E_{c} = 80 \, kJ \cdot mol^{-1}$ 的活化分子对增加的分数;

(3) 由上述计算结果可得出什么结论?

12.4 在 300 K 时, A 和 B 反应的速率常数 $k = 1.18 \times 10^{5} \, mol^{-1} \cdot cm^{-3} \cdot s^{-1}$ , 反应的活化能 $E_{a} = 40 \, kJ \cdot mol^{-1}$ 。

(1) 用简单碰撞理论估算具有足够能量值引起反应的碰撞数占总碰撞数的分数;

(2) 估算反应的概率因子的值。

已知 A 和 B 分子的直径分别为 0.3 nm 和 0.4 nm, 假定 A 和 B 的相对分子质量都为 50。

12.5 有基元反应 $\mathrm{Cl(g) + H_2(g)}\longrightarrow \mathrm{HCl(g) + H(g)}$ ，已知它们的摩尔质量和直径分别为 $M_{\mathrm{Cl}} = 35.45\mathrm{g}\cdot \mathrm{mol}^{-1}, M_{\mathrm{H_2}} = 2.016\mathrm{g}\cdot \mathrm{mol}^{-1}, d_{\mathrm{Cl}} = 0.20\mathrm{nm},$ $d_{\mathrm{H_2}} = 0.15\mathrm{nm}$ 。

(1) 根据碰撞理论计算该反应的指前因子 A (令 $T = 350 \, K$ );

(2) 在 $250 \sim 450 \, K$ 的温度范围内, 实验测得 $\lg [A / (\mathrm{mol}^{-1} \cdot \mathrm{dm}^{3} \cdot \mathrm{s}^{-1})] = 10.08$ , 求概率因子 P。

12.6 某气相双分子反应 $2\mathrm{A}(\mathrm{g}) \longrightarrow \mathrm{B}(\mathrm{g}) + \mathrm{C}(\mathrm{g})$ ，能发生反应的临界能为 $1 \times 10^{5} \, J \cdot mol^{-1}$ ，已知 A 的相对分子质量为 60，分子的直径为 0.35 nm，试计算在 300 K 时，该分解作用的速率常数 k 值。

12.7 对于反应 $\mathrm{CH}_3 + \mathrm{CH}_3 \longrightarrow \mathrm{C}_2\mathrm{H}_6, d = 308\mathrm{pm}, \mathrm{d}[\mathrm{C}_2\mathrm{H}_6] / \mathrm{dt} = k[\mathrm{CH}_3]^2$ ，试求：

(1) 室温下反应的最大二级速率常数 $k_{max}$ ;

(2) 已知 298 K, 100 kPa 下, $V = 1 \, dm^{3}$ 的乙烷样品有 10% 分解。那么, 90% 甲基复合所需的最少时间是多少?

12.8 已知液态松节油萜的消旋作用是一级反应, 在 458 K 和 510 K 时的速率常数分别为 $k(458\ \text{K}) = 2.2 \times 10^{-5} \min^{-1}$ 和 $k(510\ \text{K}) = 3.07 \times 10^{-3} \min^{-1}$ 。试求反应的实验活化能 $E_{a}$ ，以及在平均温度时的活化焓 $\Delta_{r}^{\pm} H_{m}$ 、活化熵 $\Delta_{r}^{\pm} S_{m}$ 和活化 Gibbs 自由能 $\Delta_{r}^{\pm} G_{m}$ 。

12.9 在 298 K 时, 某化学反应加了催化剂后, 其活化熵和活化焓比不加催化剂时分别下降了 $10 \, J \cdot mol^{-1} \cdot K^{-1}$ 和 $10 \, kJ \cdot mol^{-1}$ 。试求在加催化剂前后两个速率常数的比值。

12.10 对于乙酰胆碱及乙酸乙酯在水溶液中的碱性水解反应, $298 \mathrm{~K}$ 下, 实验测得其活化焓分别为 $48.5 \mathrm{~kJ} \cdot \mathrm{mol}^{-1}$ 和 $49.0 \mathrm{~kJ} \cdot \mathrm{mol}^{-1}$ , 活化熵分别为 $-85.8 \mathrm{~J} \cdot \mathrm{mol}^{-1} \cdot \mathrm{K}^{-1}$ 和 $-109.6 \mathrm{~J} \cdot \mathrm{mol}^{-1} \cdot \mathrm{K}^{-1}$ 。试问何者水解速率更大? 大多少倍? 由此可说明什么问题?

12.11 若两个反应级数相同, 活化能相等的反应, 其活化熵相差 $50 \, J \cdot mol^{-1} \cdot K^{-1}$ , 求 $300 \, K$ 时此两反应速率常数之比。

12.12 水溶液中研究酯类水解, 在实验条件相同时, 298 K 时获得实验结果如下:

<table><tr><td>反应物</td><td> $E_{\text{a}}/(kJ \cdot mol^{-1})$ </td><td> $k/(mol^{-1} \cdot dm^{3} \cdot s^{-1})$ </td></tr><tr><td>甲酸甲酯 (A)</td><td>38.5</td><td>38.4</td></tr><tr><td>乙酸甲酯 (B)</td><td>37.7</td><td> $1.3930 \times 10^{4}$ </td></tr></table>

(1) 计算活化熵差;

(2) 根据计算结果, 对反应速率的影响因素可得什么启示?

12.13 NO 高温均相分解是二级反应: $2 \mathrm{NO}(\mathrm{g}) \longrightarrow \mathrm{N}_{2}(\mathrm{~g}) + \mathrm{O}_{2}(\mathrm{~g})$ , 实验测得 $1423 \mathrm{~K}$ 时速率常数为 $1.843 \times 10^{-3} \mathrm{~mol}^{-1} \cdot \mathrm{dm}^{3} \cdot \mathrm{s}^{-1}$ , $1681 \mathrm{~K}$ 时速率常数为 $5.743 \times 10^{-2} \mathrm{~mol}^{-1} \cdot \mathrm{dm}^{3} \cdot \mathrm{s}^{-1}$ 。试求:

(1) 反应活化熵 $\Delta_{\mathrm{r}}^{\neq} S_{\mathrm{m}}$ 和活化焓 $\Delta_{\mathrm{r}}^{\neq} H_{\mathrm{m}}$ ;

(2) 反应在 1500 K 时的速率常数。

已知 $k_{\mathrm{B}} = 1.38\times 10^{-23}\mathrm{J}\cdot \mathrm{K}^{-1},h = 6.626\times 10^{-34}\mathrm{J}\cdot \mathrm{s}_{\circ}$

12.14 有一单分子重排反应 A $\longrightarrow$ P, 实验测得在 393 K 时速率常数为 $1.806 \times 10^{-4} \, s^{-1}$ , 413 K 时速率常数为 $9.14 \times 10^{-4} \, s^{-11}$ 。试计算该基元反应的 Arrhenius 活化能及 393 K 时的活化熵和活化焓。

12.15 在 1000 K 时, 实验测得气相反应 $\mathrm{C}_{2}\mathrm{H}_{6}(\mathrm{~g}) \longrightarrow 2\cdot\mathrm{CH}_{3}$ 的速率常数的表达式为 $k/s^{-1}=2.0\times10^{17}\exp\left(-\frac{3.638\times10^{5}\mathrm{J}\cdot\mathrm{mol}^{-1}}{RT}\right)$ ，设这时 $\frac{k_{B}T}{h}=2.0\times10^{13}s^{-1}$ 。试计算:

(1) 反应的半衰期 $t_{1/2}$ ;

(2) $C_{2}H_{6}(g)$ 分解反应的活化熵 $\Delta_{r}^{\neq}S_{m}$ ;

(3) 已知 1000 K 时该反应的标准熵变 $\Delta_{r}S_{m}^{\ominus}=74.1\ J\cdot mol^{-1}\cdot K^{-1}$ ，试将此值与 (2) 中所得的 $\Delta_{r}^{=}S_{m}$ 值比较，定性地讨论该反应的活化络合物的性质。

12.16 对于氢离子催化三磷酸腺苷的水解反应, 实验测得下列数据:

$$
T _ {1} = 3 1 3. 1 \mathrm{K} \text {时}, \qquad k _ {1} = 4. 6 7 \times 1 0 ^ {- 6} \mathrm{s} ^ {- 1};
$$

$$
T _ {2} = 3 2 3. 2 \: \mathrm{K} \: \text {时}, \qquad k _ {2} = 1 3. 9 \times 1 0 ^ {- 6} \: \mathrm{s} ^ {- 1}
$$

试计算该反应在 313.2 K 时的 $\Delta_{r}^{\neq}G_{m}, \Delta_{r}^{\neq}H_{m}$ 和 $\Delta_{r}^{\neq}S_{m}$ 。

12.17 某物质分解遵守一级反应规律, 实验测得不同温度下的速率常数:

$$
T _ {1} = 2 9 3. 2 \: \mathrm{K} \: \text { 时 }, \qquad k _ {1} = 7. 6 2 \times 1 0 ^ {- 6} \: \mathrm{s} ^ {- 1};
$$

$$
T _ {2} = 3 0 3. 2 \: \mathrm{K} \text {   时,   } \qquad k _ {2} = 2. 4 1 \times 1 0 ^ {- 6} \: \mathrm{s} ^ {- 1}
$$

求该反应的实验活化能 $E_{\mathrm{a}}$ ， $298.2\mathrm{K}$ 时的指前因子 $A$ ，以及 $\Delta_{\mathrm{r}}^{\mp}G_{\mathrm{m}}$ ， $\Delta_{\mathrm{r}}^{\mp}H_{\mathrm{m}}$ 和 $\Delta_{\mathrm{r}}^{\mp}S_{\mathrm{m}}$ 。

12.18 某基元反应 $\mathrm{A(g) + B(g)}\longrightarrow \mathrm{P(g)}$ ，设在 $298\mathrm{K}$ 时的速率常数为 $k_{p}(298\mathrm{K}) = 2.777\times 10^{-5}\mathrm{Pa}^{-1}\cdot \mathrm{s}^{-1},308\mathrm{K}$ 时的速率常数为 $k_{p}(308\mathrm{K}) = 5.55\times$ $10^{-5}\mathrm{Pa}^{-1}\cdot \mathrm{s}^{-1}$ 。若 $\mathrm{A(g)}$ 和 $\mathrm{B(g)}$ 的原子半径和摩尔质量分别为 $r_{\mathrm{A}} = 0.36~\mathrm{nm}$ $r_{\mathrm{B}} = 0.41~\mathrm{nm},M_{\mathrm{A}} = 28\mathrm{g}\cdot \mathrm{mol}^{-1},M_{\mathrm{B}} = 71\mathrm{g}\cdot \mathrm{mol}^{-1}$ 。试求在 $298\mathrm{K}$ 时：

(1) 该反应的概率因子 P;

(2) 反应的活化焓 $\Delta_{r}^{\neq}H_{m}$ 、活化熵 $\Delta_{r}^{\neq}S_{m}$ 和活化 Gibbs 自由能 $\Delta_{r}^{\neq}G_{m}$ 。

12.19 对于基元反应 $\mathrm{Cl(g) + ICl(g)}\longrightarrow \mathrm{Cl}_2(\mathrm{g}) + \mathrm{I(g)}$ ，由简单碰撞理论及实验数据求得 $A(\mathrm{SCT})\approx 10^{11}\mathrm{mol}^{-1}\cdot \mathrm{dm}^3\cdot \mathrm{s}^{-1},P = 0.005;$ 若以每个运动自由度的配分函数而言， $f_{\mathrm{t}}\approx 10^{10}m^{-1},f_{\mathrm{r}}\approx 10,f_{\mathrm{v}}\approx 1,$ 试判断该反应过渡态的构型是线形还是非线形？

12.20 对于反应 $H_{2}+Cl \longrightarrow HCl+H$ ，实验测得 $\lg\left[A/(mol^{-1}\cdot dm^{3}\cdot s^{-1})\right]=10.9, E_{a}=23.0\ kJ\cdot mol^{-1}$ 。

(1) 求该反应的 $\Delta_{r}^{\cong}H_{m}, \Delta_{r}^{\cong}S_{m}, \Delta_{r}^{\cong}G_{m} (T = 298 \, \text{K})$ 。过渡态结构较反应物有什么变化？

(2) 如果各种运动形式配分函数的每个自由度的数量级, $f_{\mathrm{t}}$ 的约为 $10^{10}$ (以 $\mathrm{m}^{-1}$ 为量纲), $f_{\mathrm{r}}$ 的约为 $10, f_{\mathrm{v}}$ 的约为 1, 试问与实验的 $A$ 值相对照, 生成的过渡态的构型可能是线形还是非线形?

12.21 已知两个非线形分子 A 和 B 反应, 生成非线形活化络合物 AB $^{※}$ , 设形成活化络合物后全部转变成产物, $\frac{k_{B}T}{h}=1.0\times10^{13}\ s^{-1}$ , 每个运动自由度的配分函数的近似值分别为 $f_{t}=10^{8}\ cm^{-1}$ , $f_{r}=10$ , $f_{v}=1.1$ , 不考虑电子配分函数的贡献, 求证该反应的速率常数为 $k/(mol^{-1}\cdot cm^{3}\cdot s^{-1})=9.7\times10^{9}\exp\left(-\frac{E_{0}}{RT}\right)$ 。

## 12.22 丁二烯气相二聚反应的速率常数 $k$ 为

$$
k / (\mathrm{mol} ^ {- 1} \cdot \mathrm{dm} ^ {3} \cdot \mathrm{s} ^ {- 1}) = 9. 2 \times 1 0 ^ {9} \exp \left(- \frac {1 . 9 9 2 \times 1 0 ^ {5} \mathrm{J} \cdot \mathrm{mol} ^ {- 1}}{R T}\right)
$$

(1) 用过渡态理论计算该反应在 600 K 时的指前因子, 已知 $\Delta_{r}^{\neq} S_{m} = -60.8 J \cdot mol^{-1} \cdot K^{-1}$ ;

(2) 若有效碰撞直径 $d = 0.5 \, nm$ ，用简单碰撞理论计算该反应的指前因子；

(3) 通过计算讨论概率因子 $P$ 与活化熵 $\Delta_{\mathrm{r}}^{\neq} S_{\mathrm{m}}$ 的关系。

12.23 对于基元反应 $\mathrm{O}_{3}(\mathrm{~g})+\mathrm{NO}(\mathrm{~g})\longrightarrow\mathrm{NO}_{2}(\mathrm{~g})+\mathrm{O}_{2}(\mathrm{~g})$ ，在 $220\sim320K$ 时实验测得 $E_{a}=20.8kJ\cdot mol^{-1}, A=6.0\times10^{8}\ mol^{-1}\cdot dm^{3}\cdot s^{-1}$ 。

(1) 以 $c^{\ominus} = 1.0 \, \text{mol} \cdot \text{dm}^{-3}$ 为标准态, 求该反应在 $270 \, \text{K}$ 时的活化焓 $\Delta_{\text{r}}^{\neq} H_{\text{m}}$ 、活化熵 $\Delta_{\text{r}}^{\neq} S_{\text{m}}$ 和活化 Gibbs 自由能 $\Delta_{\text{r}}^{\neq} G_{\text{m}}$ 。

(2) 若以 $p^{\ominus} = 100 \mathrm{kPa}$ 为标准态, 则 $\Delta_{\mathrm{r}}^{\mp} S_{\mathrm{m}}$ 又为何值? $\Delta_{\mathrm{r}}^{\mp} H_{\mathrm{m}}$ 和 $\Delta_{\mathrm{r}}^{\mp} G_{\mathrm{m}}$ 又将如何?

12.24 对于双原子气体反应 A(g) + B(g) $\longrightarrow$ AB(g), 分别用碰撞理论和过渡态理论的统计方法写出速率常数的计算式。在什么条件下两者完全相等？是否合理？

12.25 Lindemann 单分子反应理论认为, 单分子反应的历程为

① A + M $\xrightarrow{k_{1}}$ A\* + M

② $\mathrm{A}^{*} + \mathrm{M}\xrightarrow{k_{2}}\mathrm{A} + \mathrm{M}$

③ $A^{*} \xrightarrow{k_{3}} P$

(1) 试推导反应速率方程 $r = \frac{k_1k_3[\mathrm{A}][\mathrm{M}]}{k_2[\mathrm{M}] + k_3}$ ;

(2) 试应用简单碰撞理论计算 $469^{\circ} \mathrm{C}$ 时的 $k_{1}$ , 已知 2-丁烯的 $d = 0.5 \mathrm{~nm}$ , $E_{\mathrm{a}} = 263 \mathrm{~kJ} \cdot \mathrm{mol}^{-1}$ ;

(3) 若反应速率方程写成 $r = k_{\mathrm{u}}[\mathrm{A}]$ , 且 $k_{\infty}$ 为高压极限时的表观速率常数, 试计算 $k_{\mathrm{u}} = \frac{k_{\infty}}{2}$ 时的压力 $p_{1/2}$ , 已知 $k_{\infty} = 1.9 \times 10^{-5} \mathrm{~s}^{-1}$ ;

(4) 实验测得丁烯异构化反应在 $469^{\circ}C$ 时的 $p_{1/2} = 0.532 \, Pa$ ，试比较理论计算的 $p_{1/2}$ 与实验得到的 $p_{1/2}$ 之间的差异，对此你有何评论？

12.26 298 K 时, 反应 $\mathrm{N}_{2}\mathrm{O}_{4}(\mathrm{~g}) \xrightarrow{k_{1}} 2\mathrm{NO}_{2}(\mathrm{~g})$ 的速率常数 $k_{1} = 4.80 \times 10^{4} \, s^{-1}$ , 已知 $\mathrm{N}_{2}\mathrm{O}_{4}(\mathrm{~g}), \mathrm{NO}_{2}(\mathrm{~g})$ 的标准摩尔生成 Gibbs 自由能分别为

$\Delta_{\mathrm{f}}G_{\mathrm{m}}^{\ominus}(\mathrm{N}_{2}\mathrm{O}_{4},\mathrm{g})=99.8\ \mathrm{kJ}\cdot\mathrm{mol}^{-1},\quad\Delta_{\mathrm{f}}G_{\mathrm{m}}^{\ominus}(\mathrm{NO}_{2},\mathrm{g})=51.31\ \mathrm{kJ}\cdot\mathrm{mol}^{-1}$ 试计算:

(1) 298 K 时, 若 $\mathrm{N}_{2}\mathrm{O}_{4}(\mathrm{~g})$ 的起始压力为 100 kPa, $\mathrm{NO}_{2}(\mathrm{~g})$ 的平衡分压;

(2) 该反应的弛豫时间 $\tau$ 。

12.27 反应 $HIn^{-}\xlongequal{k_{1}}H^{+}+In^{2-}$ ， $HIn^{-}$ 为溴甲酚绿，弛豫时间与反应浓度间关系如下：

<table><tr><td> $\tau^{-1}/(10^{6} \text{ s}^{-1})$ </td><td>1.01</td><td>1.16</td><td>3.13</td></tr><tr><td> $([H^{+}] + [In^{2-}])/(10^{-6} \text{ mol } \cdot \text{ dm}^{-3})$ </td><td>4.30</td><td>6.91</td><td>38.94</td></tr></table>

求 $k_{1}, k_{2}$ 及 $K$ 。

12.28 茜素黄 G 是一种酸碱指示剂, 其反应可表示为 $HG^{-} + OH^{-} \xlongequal{k_{f}} G^{2-} + H_{2}O$ ; 当 pH = 10.88, $[HG^{-}] = 1.90 \times 10^{-4} \, mol \cdot dm^{-3}$ 时, 测得弛豫时间 $\tau = 20 \, \mu s$ , 上述反应的平衡常数 $K = 5.90 \times 10^{2} \, mol^{-1} \cdot dm^{3}$ , 计算反应的 $k_{f}$ 和 $k_{b}$ 。

12.29 在光的影响下, 葱聚合为二蒽。由于二蒽的热分解作用而达到光化学平衡。光化学反应的温度系数 (即温度每升高 10 K 反应速率所增加的倍数) 是 1.1, 热分解的温度系数是 2.8, 当达到光化学平衡时, 温度每升高 10 K, 二蒽的产量是原来的多少倍?

12.30 用波长为 313 nm 的单色光照射气态丙酮, 发生下列分解反应:

$$
(\mathrm{CH} _ {3}) _ {2} \mathrm{CO(g)} + h \nu \longrightarrow \mathrm{C} _ {2} \mathrm{H} _ {6} (\mathrm{g}) + \mathrm{CO(g)}
$$

若反应池的容量是 $0.059 \, dm^{3}$ ，丙酮吸收入射光的分数为 0.915，在反应过程中，得到下列数据：

反应温度: $840 \mathrm{~K}$

照射时间: $7.0 \mathrm{~h}$

入射能: $48.1 \times 10^{-4} \, J \cdot s^{-1}$

起始压力: 102.16 kPa

终了压力: 104.42 kPa

计算此反应的量子效率。

12.31 为了测定藻类的光合成效率, 用功率为 $10 \mathrm{~W}$ 和平均波长为 $550 \mathrm{~nm}$ 的光照射一株藻类 $100 \mathrm{~s}$ , 所产生的氧气是 $5.75 \times 10^{-4} \mathrm{~mol}$ , 计算 $\mathrm{O}_{2}$ 生成的量子效率。

12.32 用 $\lambda = 400\mathrm{nm}$ 单色光照含有 $\mathrm{H}_{2}$ 和 $\mathrm{Cl}_2$ 的反应池, 被 $\mathrm{Cl}_2$ 吸收的光强为 $I_{\mathrm{a}} = 11\times 10^{-7}\mathrm{J}\cdot \mathrm{s}^{-1}$ , 照射 $1\mathrm{min}$ 后, $p_{\mathrm{Cl}_2}$ 由 $27.3\mathrm{kPa}$ 降为 $20.8\mathrm{kPa}$ (已校正为 $273\mathrm{K}$ 时的压力)。求量子产率 $\phi$ (反应池体积为 $100~\mathrm{cm}^3$ ), 并由 $\phi$ 对反应历程提出你的分析。

12.33 $2HI + h\nu \longrightarrow H_{2} + I_{2}, \lambda = 207 nm,$ 当 1 J 能量能使 $440 \mu g HI$ 分解, 求总反应的量子产率, 并提出一个与此结果相符合的光解机理。

12.34 反应物 A 的光二聚反应历程为

$$
\mathrm{A} + h \nu \xrightarrow {k _ {1}} \mathrm{A} ^ {*}
$$

$$
\mathrm{A} ^ {*} + \mathrm{A} \xrightarrow {k _ {2}} \mathrm{A} _ {2}
$$

$$
\mathrm{A} ^ {*} \xrightarrow {k _ {3}} \mathrm{A} + h \nu_ {\mathrm{f}}
$$

试推导 $\Phi_{A_{2}}$ 及 $\Phi_{f}$ (荧光量子效率) 的表达式。

12.35 $\mathrm{O}_3$ 的光化分解反应历程如下:

① $\mathrm{O}_3 + h\nu \xrightarrow{k_1} \mathrm{O}_2 + \mathrm{O}^*$

② $\mathrm{O}^{*} + \mathrm{O}_{3}\xrightarrow{k_{2}}2\mathrm{O}_{2}$

③ $\mathrm{O}^{*}\xrightarrow{k_{3}}\mathrm{O} + h\nu$

④ $\mathrm{O} + \mathrm{O}_2 + \mathrm{M}\xrightarrow{k_4}\mathrm{O}_3 + \mathrm{M}$

设单位时间、单位体积中吸收光为 $I_{a}$ ， $\varphi$ 为过程①的量子产率， $\phi = \frac{d[O_{2}]/dt}{I_{a}}$ 为总反应的量子产率。

(1) 试证明 $\frac{1}{\phi} = \frac{1}{3\varphi} \left(1 + \frac{k_{3}}{k_{2}[O_{3}]} \right)$ ;

(2) 若以 $250.7 \mathrm{~nm}$ 的光照射, $\frac{1}{\phi} = 0.588 + 0.81 \frac{1}{[O_3]}$ , 试求 $\varphi$ 及 $\frac{k_2}{k_3}$ 的值。

12.36 有一酸催化反应 $\mathrm{A} + \mathrm{B}\xrightarrow{\mathrm{H}^{+}}\mathrm{C} + \mathrm{D},$ 已知该反应的速率方程为

$$
\frac {\mathrm{d} [ \mathrm{C} ]}{\mathrm{d} t} = k [ \mathrm{H} ^ {+} ] [ \mathrm{A} ] [ \mathrm{B} ]
$$

当 $[A]_{0} = [B]_{0} = 0.01 \, mol \cdot dm^{-3}$ ，在 pH = 2 的条件下，298 K 时的反应半衰期为 1 h，若其他条件均不变，在 288 K 时 $t_{1/2} = 2 \, h$ 。试计算在 298 K 时：

(1) 反应的速率常数 k 值;

(2) 反应的活化 Gibbs 自由能、活化焓和活化熵 $\left(\text{设 }\frac{k_{\mathrm{B}}T}{h}=10^{13}\mathrm{s}^{-1}\right)$ 。

12.37 乙酸乙酯 (E) 水解能被盐酸催化, 且反应能进行到底, 其速率方程为 $r = k[\mathrm{E}][\mathrm{HCl}]$ , 当 $[\mathrm{E}] = 0.100 \mathrm{~mol} \cdot \mathrm{dm}^{-3}$ , $[\mathrm{HCl}] = 0.010 \mathrm{~mol} \cdot \mathrm{dm}^{-3}$ , $298.2 \mathrm{~K}$ 测得 $k = 2.80 \times 10^{-5} \mathrm{~mol}^{-1} \cdot \mathrm{dm}^{3} \cdot \mathrm{s}^{-1}$ , 求反应的 $t_{1/2}$ 。

12.38 关于氨在石英表面上的分解, Hinshelwood 和 Burk 曾得到如下实验数据:

<table><tr><td>T/K</td><td colspan="2">1267</td><td colspan="2">1220</td></tr><tr><td> $p_0$ /kPa</td><td>7.13</td><td>18.33</td><td>15.60</td><td>39.73</td></tr><tr><td> $t_{1/2}$ /s</td><td>43</td><td>44</td><td>19</td><td>191</td></tr></table>

(1) 试问该反应的级数是多少？如果假定该表面反应是单分子反应，则在高压极限条件下，该反应级数是多少？

(2) 该反应的活化能是多少?

12.39 对于遵守 Michaelis 历程的酶催化反应, 实验测得不同底物浓度时的反应速率 r, 今取其中二组数据如下:

<table><tr><td>[S]/(10-3mol·dm-3)</td><td>2.0</td><td>20.0</td></tr><tr><td>r/(10-5mol·dm-3·s-1)</td><td>13</td><td>38</td></tr></table>

当 $[\mathrm{E}]_0 = 2.0\mathrm{g}\cdot \mathrm{dm}^{-3},M_{\mathrm{E}} = 50\times 10^{3}\mathrm{g}\cdot \mathrm{mol}^{-1}$ 时，试计算 $K_{\mathrm{M}}$ 、最大反应速率 $r_{\mathrm{m}}$ 和 $k_{2}(\mathrm{ES}\xrightarrow{k_{2}}\mathrm{P} + \mathrm{E})$ 。

12.40 在不同底物浓度 [S] 时测定酶催化反应速率 r，今取其中二组数据：

<table><tr><td>[S]/(10-3mol·dm-3)</td><td>1.00</td><td>10.00</td></tr><tr><td>r(任意单位)</td><td>4.78</td><td>12.50</td></tr></table>

该反应符合 Michaelis 历程, 求 Michaelis 常数 $K_{M}$ 。

12.41 在某些生物体中, 存在一种超氧化物歧化酶 (E), 它可将有害的 $O_{2}^{-}$ 变为 $O_{2}$ , 反应如下:

$$
2 \mathrm{O} _ {2} ^ {-} + 2 \mathrm{H} ^ {+} \xrightarrow {\mathrm{E}} \mathrm{O} _ {2} + \mathrm{H} _ {2} \mathrm{O} _ {2}
$$

今 $\mathrm{pH} = 9.1$ ，酶的初始浓度 $[\mathrm{E}]_0 = 4\times 10^{-7}\mathrm{mol}\cdot \mathrm{dm}^{-3}$ ，测得下列实验数据：

<table><tr><td> $r/(mol \cdot dm^{-3} \cdot s^{-1})$ </td><td> $3.85 \times 10^{-3}$ </td><td> $1.67 \times 10^{-2}$ </td><td>0.1</td></tr><tr><td> $[O_{2}^{-}]/(mol \cdot dm^{-3})$ </td><td> $7.69 \times 10^{-6}$ </td><td> $3.33 \times 10^{-5}$ </td><td> $2.00 \times 10^{-4}$ </td></tr></table>

r 是以产物 $O_{2}$ 表示的反应速率。设此反应的机理为

(1) $\mathrm{E} + \mathrm{O}_2^- \xrightarrow{k_1} \mathrm{E}^- + \mathrm{O}_2$

(2) $\mathrm{E}^{-} + \mathrm{O}_{2}^{-} + 2\mathrm{H}^{+}\xrightarrow{k_{2}}\mathrm{E} + \mathrm{H}_{2}\mathrm{O}_{2}$

式中 $E^{-}$ 为中间物, 可看作自由基, 已知 $k_{2}=2k_{1}$ , 计算 $k_{1}$ 和 $k_{2}$ 。

12.42 有一酶催化反应 $\mathrm{CO}_{2}(\mathrm{aq}) + \mathrm{H}_{2}\mathrm{O}\xrightarrow{\mathrm{E}}\mathrm{H}^{+} + \mathrm{HCO}_{3}^{-}$ ，设 $\mathrm{H}_2\mathrm{O}$ 大大过量，溶液的 $\mathrm{pH} = 7.1$ ，温度为 $0.5^{\circ}\mathrm{C}$ ，酶的初始浓度 $[\mathrm{E}]_0 = 2.8\times 10^{-9}\mathrm{mol}\cdot \mathrm{dm}^{-3}$ 。实验测得反应初速率 $r_0$ 随 $\mathrm{CO}_{2}(\mathrm{g})$ 的初始浓度 $[\mathrm{CO}_{2}]_{0}$ 的变化如下所示：

<table><tr><td> $[CO_2]_0/(mmol \cdot dm^{-3})$ </td><td>1.25</td><td>2.50</td><td>5.00</td><td>20.0</td></tr><tr><td> $r_0/(mmol \cdot dm^{-3} \cdot s^{-1})$ </td><td>0.028</td><td>0.048</td><td>0.080</td><td>0.155</td></tr></table>

(1) 试求 Michaelis 常数 $K_{\mathrm{M}}$ 及最大反应速率 $r_{\mathrm{m}}$ ;

(2) 试求中间络合物生成产物的速率常数 $k_{2}$ ;

(3) 从速率方程如何理解 $K_{\mathrm{M}}$ 是反应速率为最大反应速率 $r_{\mathrm{m}}$ 的一半时的底物浓度, 即 $r = \frac{1}{2} r_{\mathrm{m}}$ 时, $K_{\mathrm{M}} = [\mathrm{S}]$ 。

