---
title: "傅献彩《物理化学》（第六版下册）-第十一章 化学动力学基础(一)：速率方程与简单级数"
type: 外部教材切片
source_book: "物理化学（第六版下册）-傅献彩"
syllabus_codes: [基础-07, 基础-12]
created: 2026-09-25
updated: 2026-09-25
status: 已填充
---

## 第十一章

## 化学动力学基础(一)

本章基本要求

(1) 掌握宏观动力学中的一些基本概念，如反应速率的表示法、基元反应和非基元反应。了解什么是反应级数、反应分子数和速率常数等。

(2) 掌握具有简单级数（如一级、二级和零级）反应的特点，不但会从实验数据利用各种方法判断反应级数，还要能熟练地利用速率方程计算速率常数、半衰期等。

(3) 掌握三种典型复杂反应（对峙反应、平行反应和连续反应）的特点，学会使用合理的近似方法，作一些简单的计算。

(4) 掌握温度对反应速率的影响，特别是在平行反应中如何进行温度调控，以提高所需产物的产量。

(5) 掌握 Arrhenius 公式的各种表示形式，知道活化能的含义及其对反应速率的影响，并掌握活化能的求算方法。

(6) 掌握链反应的特点，会用稳态近似、平衡假设和速控步等近似方法从复杂反应的机理推导出速率方程。

## 11.1 化学动力学的任务和目的

将化学反应应用于生产实践主要有两个方面的问题: 一是要了解反应进行的方向和最大限度, 以及外界条件对平衡的影响; 二是要知道反应进行的速率和反应的历程 (即机理)。人们把前者归属于化学热力学的研究范围, 把后者归属于化学动力学 (chemical kinetics) 的研究范围。热力学只能预言在给定的条件下, 反应发生的可能性, 即在给定条件下, 反应能不能发生, 以及发生到什么程度。至于如何把可能性变为现实性, 以及过程中进行的速率如何, 历程如何, 热力学不能给出回答。这是因为在经典热力学的研究方法中既没有考虑时间因素, 也没有考虑各种因素对反应速率的影响和反应进行的其他细节。例如, 合成氨的反应在 $3 \times 10^{7} \mathrm{~Pa}$ 和 $773 \mathrm{~K}$ 左右进行, 按热力学分析, 其最大可能转化率是 $26 \%$ 左右, 但是如果不加催化剂, 这个反应的速率是非常慢的, 根本不能应用于工业生产。因此, 必须对这个反应进行化学动力学方面的研究, 寻找合适的催化剂, 从而加快反应速率, 使反应能用于大规模工业生产。热力学计算还表明, 在常温常压下就有可能由氮和氢生成氨, 因此如何寻找新的催化剂, 选择合适的反应途径以实现热力学的预期目的是当前十分活跃的研究领域。又如, 在 $298 \mathrm{~K}$ 时:

$$
\mathrm{H} _ {2} (\mathrm{g}) + \frac {1}{2} \mathrm{O} _ {2} (\mathrm{g}) = \mathrm{H} _ {2} \mathrm{O} (\mathrm{l}) \quad \Delta_ {\mathrm{r}} G _ {\mathrm{m}} ^ {\ominus} = - 2 3 7. 1 3 \mathrm{kJ} \cdot \mathrm{mol} ^ {- 1}
$$

根据热力学的观点, 此反应向右进行的趋势理应是很大的。但热力学对于这个反应需要多长时间却不能提供任何启示。实际上, 在通常情况下, 若把氢和氧放在一起, 它们几乎不能发生反应。如果升高温度到 $1073 \mathrm{~K}$ 时, 该反应却以爆炸的方式瞬时完成。如果我们选用合适的催化剂 (如用钯作为催化剂), 则即使在常温常压下氢和氧也能以较快的速率化合成水, 同时还可以利用该反应所释放出来的能量 (这个反应已成功地设计成为氢氧电池)。反应进行速率问题的重要性, 在化工生产中是不言而喻的。在大多数情况下, 人们希望反应的速率加快, 但在另一些情况中, 人们也希望能降低反应的速率, 如防止金属的腐蚀、防止塑料老化、抑制反应中的某些副反应的发生等。

化学动力学的基本任务之一就是要了解反应的速率, 了解各种因素 (如分子结构、温度、压力、浓度、介质、催化剂等) 对反应速率的影响, 从而给人们提供选择反应条件、掌握控制反应进行的主动权, 使化学反应按人们所希望的速率进行。

化学动力学的另一个基本任务是研究反应历程 (mechanism)。所谓反应历程,就是反应物究竟按什么途径、经过哪些步骤才转化为最终产物。同时, 知道了这些反应历程, 可以找出决定反应速率的关键所在, 使主反应按照人们所希望的方向进行, 并使副反应以最小的速率进行, 从而在生产上达到多快好省的目的。

了解反应历程也可以帮助人们了解有关物质结构的知识, 因为化学变化从根本上来说, 就是旧键的破裂和新键的形成过程。反应的历程能够反映出物质结构和反应能力之间的关系, 从而可以加深人们对于物质运动形态的认识。当然用已知的有关物质结构的知识也可以推测一些反应的历程, 然而遗憾的是迄今为止, 真正弄清楚反应历程的反应为数还不多, 这方面的工作远远落后于实际。但是随着各种新型谱仪的出现和用激光、交叉分子束等试验手段对微观反应动力学的研究越来越深入, 人们对反应历程的研究已达到一个新的高度。

在实际生产中, 既要考虑热力学问题, 也要考虑动力学问题。如果一个反应在热力学上判断是可能发生的, 则如何使可能性变为现实性, 并使这个反应能以一定的速率进行, 就成为主要矛盾了。如果一个反应在热力学上判断为不可能, 当然就不再需要考虑速率问题了。一个化学反应系统内的许多性质和外界条件都能影响平衡和反应速率, 平衡问题和速率问题这两者是相互关联的。但限于人们目前的认识水平, 迄今还没有统一的定量处理方法把它们联系起来, 在很大程度上还需要分别研究化学反应平衡和化学反应速率。

从历史上来说, 化学动力学的发展比化学热力学的发展迟, 而且不具有热力学那样较完整的系统。

化学动力学的发展大体上可以分为几个阶段, 即 19 世纪后半叶的宏观动力学阶段; 20 世纪 50 年代以后的微观反应动力学 (microkinetics) 阶段。在这两个阶段之间, 即 20 世纪前叶, 则是宏观反应动力学向微观反应动力学的过渡阶段。在第一阶段中的主要成就是质量作用定律和 Arrhenius 公式的确立, 并由此提出了活化能的概念。由于这一时期测试手段的水平相对较低, 对反应动力学的研究基本上仍然是宏观的, 因而其结论也只使用于总包反应 $^{①}$ 。在第二阶段中, 主要是对反应速率从理论上进行了探讨, 提出了碰撞理论和过渡态理论, 并借助于量子力学计算了反应系统的势能面, 指出过渡态 (或活化络合物) 乃是势能面上的马鞍点。在这一阶段中, 一个重要的发现是链反应, 许多常见的反应如燃烧、有机物的分解、烯烃的聚合等都是链反应, 在反应的历程中存在自由基, 而且总包反应是由许多基元反应组成的。链反应的发现使化学动力学的研究从总包反应向基元反应深入, 即由宏观反应动力学向微观反应动力学过渡。在第二个阶段中, 由于分子束和激光技术的发展及应用, 从而开创了分子反应动态学 (或称微观反应动力学)。它深入研究态-态反应的层次, 即研究由不同量子态的反应物转化为不同量子态的产物的速率及反应的细节。物理化学家李远哲由于在交叉分子束研究中做出了卓越的贡献, 与 Herschbach 分享了 1986 年的诺贝尔化学奖。

近百年来化学动力学进展的速度很快, 这一方面应归功于相邻学科基础理论和技术上的进展, 另一方面归功于实验方法、检测手段的日新月异。例如, 用磁共振谱仪可以检测自由基的存在, 用闪光光解技术发现寿命特别短的自由基。又如, 时间在化学动力学中是极为重要的变量, 在 20 世纪 50 年代还认为 $10^{-3} \mathrm{~s}$ 以下的快速反应是无法测量的, 而到了 70 年代, 时间的分辨率已达到微秒 $(10^{-6} \mathrm{~s})$ 水平, 80 年代可达到皮秒 $(10^{-12} \mathrm{~s})$ 水平, 可以直接观测化学反应的最基本的动态历程。这一变量在测试精度上的大大提高, 为人们提供了许多前所未有的新的信息, 为深入研究反应的细节提供了依据。超短脉冲激光技术的开发, 更是打开了进入超短时间飞秒 $(10^{-15} \mathrm{~s})$ 分辨世界的门槛。各种先进波谱学仪器的出现, 使生物大分子及纳米分子的形貌和结构清晰可见。量子化学已经能够在实验手段相形见绌时计算出化学反应的反应物过渡态、中间物和产物的结构能谱和反应通道; 计算 (机) 化学各种方法和程序的发展, 使人们能够利用有限的已知的微观和宏观参数去设计预期功能的新产物、新流程, 以及进一步推测反应所经历的历程, 最大限度地减少条件实验的工作量。但是也应指出, 从总体上说化学动力学的发展虽相对较为迅速, 但所形成的理论与经典热力学相比尚不够完善, 要从定量的角度和从物质内部的结构即从原子、分子水平来说明或解决化学反应历程和相关的动力学问题, 还需要继续不断的努力。

## 11.2 化学反应速率的表示法

反应开始后, 反应物的数量 (或浓度) 不断降低, 产物的数量 (或浓度) 不断增加, 如图 11.1 所示。在大多数反应系统中, 反应物 (或产物) 的浓度随时间的变化关系往往不是线性关系, 开始时反应物的浓度较大, 反应较快, 单位时间内得到的产物较多。而在反应后期, 反应物的浓度变小, 反应较慢, 单位时间内得到的产物的数量较少。但也有些反应 (如链反应), 反应开始时需要有一定的诱导时间 (induction time), 反应很慢, 然后不断加快, 达到最大值后才由于反应物的消耗而逐渐变慢。一些自催化反应 (autocatalytic reaction) 也有类似的情况。因此, 从浓度随时间的变化曲线可以提供反应类型的信息。

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_1-199_images/17e3f8cb97dc73693a345a317aea1ec36bee13c746bfe4d20d86db7dbd466ffe.jpg)  
图11.1 反应物和产物的浓度随时间的变化

在物理学中, “速度 (velocity)” 是矢量, 有方向性, 而 “速率 (rate)” 是标量。本书一律采用标量 “速率” 来表示浓度随时间的变化率。为了描述化学反应的进展情况, 可以用反应物浓度随时间的不断降低来表示, 也可用产物浓度随时间的不断升高来表示。但由于在反应式中产物和反应物的化学计量数不尽一致, 所以用反应物或产物的浓度变化率来表示反应速率时, 其数值未必一致。但若采用反应进度 ( $\xi$ ) 随时间的变化率来表示反应速率, 则不会产生这种矛盾。

根据反应进度 $\xi$ 的定义, 设反应为

$$
\begin{array}{c c c} & \alpha \mathrm{R} \longrightarrow \beta \mathrm{P} \\ t = 0 & n _ {\mathrm{R}} (0) & n _ {\mathrm{P}} (0) \\ t = t & n _ {\mathrm{R}} (t) & n _ {\mathrm{P}} (t) \end{array}
$$

若反应开始时 $(t=0)$ ，反应物 R 和产物 P 的物质的量分别为 $n_{\mathrm{R}}(0)$ 和 $n_{\mathrm{P}}(0)$ ，当反应时间为 t 时，物质的量分别为 $n_{\mathrm{R}}(t)$ 和 $n_{\mathrm{P}}(t)$ ，则反应进度为

$$
\xi = \frac {n _ {\mathrm{R}} (t) - n _ {\mathrm{R}} (0)}{- \alpha} = \frac {n _ {\mathrm{P}} (t) - n _ {\mathrm{P}} (0)}{\beta}\tag{1.1.1}
$$

对反应物的计量系数 $(\alpha)$ 取负值, 产物的计量系数 $(\beta)$ 取正值。将式 (11.1) 对 $t$ 微分, 得到在某个时刻 $t$ 时反应进度的变化率, 即称为反应的转化速率 (conversion rate of reaction):

$$
\frac {\mathrm{d} \xi}{\mathrm{d} t} = \dot {\xi} = - \frac {1}{\alpha} \frac {\mathrm{d} n _ {\mathrm{R}} (t)}{\mathrm{d} t} = \frac {1}{\beta} \frac {\mathrm{d} n _ {\mathrm{P}} (t)}{\mathrm{d} t}\tag{11.2}
$$

化学反应速率 $r$ 可以定义为

$$
r \stackrel {\mathrm{def}} {=} \frac {1}{V} \frac {\mathrm{d} \xi}{\mathrm{d} t} = \frac {1}{V} \dot {\xi}\tag{11.3}
$$

式中 V 为反应系统的体积, 则上述反应的反应速率为

$$
r = - \frac {1}{V \alpha} \frac {\mathrm{d} n _ {\mathrm{R}} (t)}{\mathrm{d} t} = \frac {1}{V \beta} \frac {\mathrm{d} n _ {\mathrm{P}} (t)}{\mathrm{d} t}\tag{11.4}
$$

如果在反应过程中体积是恒定的, 则式 (11.4) 可写为

$$
\begin{array}{r l} r & = - \frac {1}{\alpha} \frac {\mathrm{d} [ n _ {\mathrm{R}} (t) / V ]}{\mathrm{d} t} = - \frac {1}{\alpha} \frac {\mathrm{d} c _ {\mathrm{R}}}{\mathrm{d} t} = - \frac {1}{\alpha} \frac {\mathrm{d} [ \mathrm{R} ]}{\mathrm{d} t} \\ & = \frac {1}{\beta} \frac {\mathrm{d} [ n _ {\mathrm{P}} (t) / V ]}{\mathrm{d} t} = \frac {1}{\beta} \frac {\mathrm{d} c _ {\mathrm{P}}}{\mathrm{d} t} = \frac {1}{\beta} \frac {\mathrm{d} [ \mathrm{P} ]}{\mathrm{d} t} \end{array}
$$

式中 [R] 表示反应物 R 的浓度 $c_{R}$ ，[P] 表示产物 P 的浓度 $c_{P}$ 。

对于任意反应:

$$
e \mathrm{E} + f \mathrm{F} = g \mathrm{G} + h \mathrm{H} \qquad \text {或} \qquad 0 = \sum_ {\mathrm{B}} \nu_ {\mathrm{B}} \mathrm{B}
$$

则有

$$
\begin{array}{r l} r & = - \frac {1}{e} \frac {\mathrm{d} [ \mathrm{E} ]}{\mathrm{d} t} = - \frac {1}{f} \frac {\mathrm{d} [ \mathrm{F} ]}{\mathrm{d} t} = \frac {1}{\mathrm{g}} \frac {\mathrm{d} [ \mathrm{G} ]}{\mathrm{d} t} = \frac {1}{h} \frac {\mathrm{d} [ \mathrm{H} ]}{\mathrm{d} t} \\ & = \frac {1}{\nu_ {\mathrm{B}}} \frac {\mathrm{d} [ \mathrm{B} ]}{\mathrm{d} t} \end{array}\tag{11.5}
$$

式中 $\nu_{B}$ 为化学反应式中物质 B 的计量系数, 对反应物取负值, 对产物取正值; r 的量纲为 [浓度]·[时间] $^{-1}$ 。例如, 对于五氧化二氮的分解反应:

$$
\mathrm{N} _ {2} \mathrm{O} _ {5} (\mathrm{g}) = \mathrm{N} _ {2} \mathrm{O} _ {4} (\mathrm{g}) + \frac {1}{2} \mathrm{O} _ {2} (\mathrm{g})
$$

反应速率既可以用 $N_{2}O_{5}$ 的浓度随时间变化率表示, 也可用 $N_{2}O_{4}$ 或 $O_{2}$ 的浓度随时间变化率表示, 即

$$
r = - \frac {\mathrm{d} [ \mathrm{N} _ {2} \mathrm{O} _ {5} ]}{\mathrm{d} t} = \frac {\mathrm{d} [ \mathrm{N} _ {2} \mathrm{O} _ {4} ]}{\mathrm{d} t} = 2 \frac {\mathrm{d} [ \mathrm{O} _ {2} ]}{\mathrm{d} t}
$$

对于气相反应, 压力比浓度更容易测定, 因此也可用参加反应的各物种的分压来代替浓度, 对上述反应有

$$
r ^ {\prime} = - \frac {\mathrm{d} p _ {\mathrm{N} _ {2} \mathrm{O} _ {5}}}{\mathrm{d} t} = \frac {\mathrm{d} p _ {\mathrm{N} _ {2} \mathrm{O} _ {4}}}{\mathrm{d} t} = 2 \frac {\mathrm{d} p _ {\mathrm{O} _ {2}}}{\mathrm{d} t}
$$

这时 $r'$ 的量纲为 [压力]·[时间] $^{-1}$ 。对于理想气体， $p_{B}=c_{B}RT$ ，所以 $r'=r(RT)$ 。

对于多相催化反应, 反应的速率可以定义为

$$
r \stackrel {\text { def }} {=} \frac {1}{Q} \frac {\mathrm{d} \xi}{\mathrm{d} t}\tag{11.6a}
$$

式中 Q 代表催化剂的用量。若 Q 用质量 m 表示, 则

$$
r _ {m} = \frac {1}{m} \frac {\mathrm{d} \xi}{\mathrm{d} t}\tag{11.6b}
$$

$r_{m}$ 称为在给定条件下催化剂的比活性, 其单位为 $mol \cdot kg^{-1} \cdot s^{-1}$ 。如果 Q 用催化剂的堆体积 V (包括粒子自身的体积和粒子间的空间) 表示, 则

$$
r _ {V} = \frac {1}{V} \frac {\mathrm{d} \xi}{\mathrm{d} t}\tag{11.6c}
$$

$r_{V}$ 为单位体积催化剂的反应速率, 其单位为 $mol \cdot m^{-3} \cdot s^{-1}$ 。如果 Q 用催化剂的表面积 A 表示, 则

$$
r _ {A} = \frac {1}{A} \frac {\mathrm{d} \xi}{\mathrm{d} t}\tag{11.6d}
$$

IUPAC 建议, 称 $r_{A}$ 为表面反应速率 (areal rate of reaction), 其单位为 $mol \cdot m^{-2} \cdot s^{-1}$ 。

要测定化学反应速率, 必须测出在不同反应时刻的反应物 (或产物) 的浓度, 绘制物质浓度随时间的变化曲线 (也称为动力学曲线), 然后从图上求出不同反应时间的速率 $\left(\frac{\mathrm{d}c}{\mathrm{d}t}\right)$ (即在时间 t 时作该曲线的切线), 就可以知道反应在 t 时的速率。在反应开始 $(t=0)$ 时的速率 $\left(\frac{\mathrm{d}c}{\mathrm{d}t}\right)_{t=0}$ 称为反应的初速, 在研究化学反应动力学时它是一个较为重要的参数。

测定反应物（或产物）在不同反应时间的浓度一般可采用化学方法和物理方法。化学方法是在某一时间取出一部分物质，并设法迅速使反应停止（用骤冷、冲稀、加阻化剂或除去催化剂等方法），然后进行化学分析，这样可直接得到不同时刻某物质浓度的数值，但实验操作则往往较烦琐；物理方法是在反应过程中，对某一种与物质浓度有关的物理量进行连续监测，获得一些原位（in situ）反应的数据。通常利用的物理性质和方法有测定压力、体积、旋光度、折射率、吸收光谱、电导、电动势、介电常数、黏度、热导率或进行比色等。对于不同的反应可选用不同方法和仪器，如色谱、质谱、色-质谱联用、红外光谱及磁共振谱等。由于物理方法不是直接测量物质的浓度，所以首先要知道浓度与这些物理量之间的依赖关系，当然最好是选择与浓度变化成线性关系的一些物理量。

对于一些反应时间很短 (在秒以下) 的快速反应, 必须采取某些特殊的装置才能进行测量, 否则在反应物尚未完全混匀之前, 已混合的部分反应已经开始甚至可能已经完成或接近尾声, 这给准确记录反应时间带来困难或根本无法计算反应时间。对这种快速反应常采用快速流动法进行测量, 在流动法中反应物迅速混合, 并在长管式反应器的一端以一定速度输入, 产物在反应器的另一端流出, 然后用物理方法测定在反应管不同位置上反应物的浓度, 也可获得绘制浓度随时间变化曲线的必要数据, 工业上常采用这种流动技术。

## 11.3 化学反应的速率方程

表示反应速率与浓度等参数之间的关系的方程或表示浓度等参数与时间关系的方程称为化学反应的速率方程 (rate equation)，也称为动力学方程 (kinetic equation)。速率方程可表示为微分式或积分式，其具体形式随不同反应而异，必须由实验来确定。基元反应的速率方程式是其中最为简单的。

## 基元反应和非基元反应

我们通常所写的化学方程式绝大多数并不代表反应的真正历程, 而仅代表反应的总结果, 所以它只是反应的化学计量式 (stoichiometric equation)。

例如, 在气相中氢分别与三种不同的卤素 $\left(\mathrm{Cl}_{2}, \mathrm{Br}_{2}, \mathrm{I}_{2}\right)$ 反应, 通常把反应的化学计量式写成

$$
\begin{array}{r l} & (1) \mathrm{H} _ {2} + \mathrm{I} _ {2} = 2 \mathrm{HI} \\ & (2) \mathrm{H} _ {2} + \mathrm{Cl} _ {2} = 2 \mathrm{HCl} \\ & (3) \mathrm{H} _ {2} + \mathrm{Br} _ {2} = 2 \mathrm{HBr} \end{array}
$$

这三个反应的化学计量式形式相似, 但它们的反应历程却大不相同。根据大量的实验结果, 现在知道 $H_{2}$ 和 $I_{2}$ 的反应历程为

$$
\begin{array}{r l}&(4) \mathrm{I} _ {2} + \mathrm{M} \rightleftharpoons 2 \mathrm{I} \cdot + \mathrm{M}\\&(5) \mathrm{H} _ {2} + 2 \mathrm{I} \cdot \longrightarrow 2 \mathrm{HI}\end{array}
$$

式中 M 是指反应器壁或其他第三体分子, 它们是惰性物质, 不参与反应而只具有传递能量的作用。

$H_{2}$ 和 $Cl_{2}$ 的反应由下面几步构成:

$$
\mathrm{Cl} _ {2} + \mathrm{M} \longrightarrow 2 \mathrm{Cl} \cdot + \mathrm{M} \tag {6}
$$

(7) $\mathrm{Cl} \cdot + \mathrm{H}_{2} \longrightarrow \mathrm{HCl} + \mathrm{H} \cdot$

(8) $\mathrm{H}\cdot +\mathrm{Cl}_2\longrightarrow \mathrm{HCl} + \mathrm{Cl}\cdot$

$$
\mathrm{Cl} \cdot + \mathrm{Cl} \cdot + \mathrm{M} \longrightarrow \mathrm{Cl} _ {2} + \mathrm{M} \tag {9}
$$

$H_{2}$ 和 $Br_{2}$ 的反应由如下几步构成:

$$
(1 0) \mathrm{Br} _ {2} + \mathrm{M} \longrightarrow 2 \mathrm{Br} \cdot + \mathrm{M}
$$

(11) $\mathrm{Br}\cdot +\mathrm{H}_2\longrightarrow \mathrm{HBr} + \mathrm{H}\cdot$

(12) $\mathrm{H}\cdot +\mathrm{Br}_2\longrightarrow \mathrm{HBr} + \mathrm{Br}\cdot$

(13) $\mathrm{H}\cdot +\mathrm{HBr}\longrightarrow \mathrm{H}_2 + \mathrm{Br}\cdot$

(14) $\mathrm{Br}\cdot +\mathrm{Br}\cdot +\mathrm{M}\longrightarrow \mathrm{Br}_2 + \mathrm{M}$

方程式 (1), (2), (3) 只表示这三个反应的总结果。

如果一个化学反应, 总是经过若干个简单的反应步骤, 最后才转化为产物分子, 这种反应称为非基元反应。所谓简单步骤是指分子经一次碰撞后, 在一次化学行为中就能完成反应, 这种反应称为基元反应 (elementary reaction), 有时也简称为元反应。简言之, 基元反应就是一步能完成的反应。上述反应 (4) \~ (14) 都是基元反应, 而反应 (1) \~ (3) 是非基元反应。非基元反应是许多基元反应的总和, 亦称为总包反应或简称为总反应 (overall reaction)。一个复杂反应是经过若干个基元反应才能完成的反应, 这些基元反应代表了反应所经过的途径, 在动力学上就称其为反应机理或反应历程 (reaction mechanism)。故方程式 (4) \~ (5), (6) \~ (9) 和 (10) \~ (14) 分别代表了三种卤素与 $\mathrm{H}_{2}$ 的反应历程。

经验证明, 基元反应的速率方程比较简单, 即基元反应的速率与反应物浓度 (含有相应的指数) 的乘积成正比, 其中各浓度的指数就是反应式中各反应物质的计量系数。例如, 对于 $(5) \sim (14)$ 反应, 有

$$
r _ {5} \propto [ \mathrm{H} _ {2} ] [ \mathrm{I} \cdot ] ^ {2} \qquad {\text {或}} \qquad r _ {5} = k _ {5} [ \mathrm{H} _ {2} ] [ \mathrm{I} \cdot ] ^ {2}\tag{11.7}
$$

$$
r _ {6} \propto [ \mathrm{Cl} _ {2} ] [ \mathrm{M} ] \qquad {\text {或}} \qquad r _ {6} = k _ {6} [ \mathrm{Cl} _ {2} ] [ \mathrm{M} ]\tag{11.8}
$$

其余类推。

基元反应的这个规律称为质量作用定律 (law of mass action), 是 19 世纪中期由挪威化学家 Guldberg 和 Waage 在总结前人的大量工作并结合他们自己的实验的基础上提出来的, 即 “化学反应速率与反应物的有效质量成正比” (这里的质量其原意是指浓度)。质量作用定量只适用于基元反应。

从总包反应的化学计量式不能直接得到动力学方程。动力学方程往往是一个较复杂的函数关系, 这些关系可通过实验、设计反应历程而获得。例如, 反应(1) \~ (3) 的速率方程为 (得到这些公式的过程, 将在 “复杂反应” 一节中介绍)

$$
r _ {1} = k _ {1} \left[ \mathrm{H} _ {2} \right] \left[ \mathrm{I} _ {2} \right]\tag{11.9}
$$

$$
r _ {2} = k _ {2} \left[ \mathrm{H} _ {2} \right] \left[ \mathrm{Cl} _ {2} \right] ^ {1 / 2}\tag{11.10}
$$

$$
r _ {3} = \frac {k [ \mathrm{H} _ {2} ] [ \mathrm{Br} _ {2} ] ^ {1 / 2}}{1 + k ^ {\prime} [ \mathrm{HBr} ] / [ \mathrm{Br} _ {2} ]}\tag{11.11}
$$

## 反应的级数、反应分子数和反应的速率常数

在化学反应的速率方程中, 各物浓度项的指数之代数和就称为该反应的级数 (order of reaction), 用 n 表示。例如, 根据实验结果归纳得出的某反应的速率方程可用下式表示:

$$
r = k [ \mathrm{A} ] [ \mathrm{B} ]
$$

则根据速率方程中各浓度项的相应指数, 该反应对反应物 A 而言是一级, 对反应物 B 也是一级, 故总反应为二级。我们通常所说的该反应的级数都是指总级数而言的。例如, 光气的合成反应:

$$
\mathrm{CO(g)} + \mathrm {Cl_ {2} (g)} \longrightarrow \mathrm {COCl_ {2} (g)}
$$

实验表明该反应的速率方程为

$$
r = k [ \mathrm{CO} ] [ \mathrm{Cl} _ {2} ] ^ {3 / 2}
$$

则该反应对 $\mathrm{CO(g)}$ 来说是一级, 对 $\mathrm{Cl}_{2}(\mathrm{~g})$ 来说是 3/2 级, 总反应是 2.5 级。

又如, 前面所说的反应 (3) $H_{2} + Br_{2} = 2HBr$ , 其反应的速率方程如式 (11.11) 所示, 式中 $k, k'$ 都是实验值 (是经验常数), 该反应对 $H_{2}$ 是一级, 而对 $Br_{2}$ 和 HBr 就不具有简单的关系, 因此该反应也就没有简单的总级数。

反应的分子数 (这里所说的反应分子数实际上是指参加反应的物种粒子数, 即 molecularity) 与反应的级数不同, 从微观的角度看, 参加基元反应的分子数只可能是 1, 2 或 3。对于基元反应或简单反应, 通常其反应级数和反应的分子数是相同的。例如, 反应 $\mathrm{I}_2 \longrightarrow 2\mathrm{I}$ 是单分子反应, 也是一级反应; 反应 $\mathrm{Br} \cdot + \mathrm{H}_2 \longrightarrow \mathrm{HBr} + \mathrm{H}$ 是双分子反应, 也是二级反应。但也有些基元反应表现出的反应级数与反应分子数不一致, 例如, 乙醚在 $500^{\circ}\mathrm{C}$ 左右的热分解反应是单分子反应, 也是一级反应, 但在低压下则表现为二级反应。这是实验结果, 反映出该反应在不同压力下有不同的反应级数。又如双分子反应, 通常情况下是二级反应, 但在某种情况下也可以使其成为一级反应。

总之, 反应的级数和分子数是属于不同范畴的概念, 反应级数是就宏观的总包反应而言的, 而反应分子数则系对微观的基元反应来说的。反应级数可以是整数、分数、零或负数等, 有时甚至无法用简单数字来表示。而反应分子数的值只能是不大于 3 的正整数。尽管在通常情况下二者常具有相同的数值, 但其意义是有区别的。对于一个指定的基元反应, 反应分子数有定值, 但其反应的级数由于反应的条件不同而可能不同。

在式 (11.7) 至式 (11.11) 中, 都有一个比例系数 $k$ , 这是一个与浓度无关的量, 称为速率常数 (rate constant), 也称为速率系数 (rate coefficient) $^{①}$ 。由于在数值上它相当于参加反应的物质都处于单位浓度时的反应速率, 故又称为反应的比速率 (specific reaction rate)。不同反应有不同的速率常数, 速率常数与反应温度、反应介质 (溶剂)、催化剂等有关, 甚至会随反应器的形状、性质而异。

速率常数 $k$ 是化学动力学中一个重要物理量, 其数值直接反映了速率的快慢。要获得化学反应的速率方程, 首先需要收集大量的实验数据, 然后再经归纳整理而得。它是确定反应历程的主要依据, 在化学工程中, 它又是设计合理的反应器的重要依据。

## 11.4 具有简单级数的反应

以下讨论的是具有简单级数的反应, 介绍其速率方程的微分式、积分式以及它们的速率常数 k 的单位和半衰期等各自的特征。具有简单级数的反应并不一定就是基元反应, 但只要该反应具有简单的级数, 它就具有该级数反应的所有特征。

## 一级反应

凡是反应速率只与物质浓度的一次方成正比者称为一级反应 (first order reaction), 如放射性元素镭的蜕变反应及五氧化二氮的分解反应等。

$$
\begin{array}{r l} & _ {8 8} ^ {2 2 6} \mathrm{Ra} \longrightarrow_ {8 6} ^ {2 2 2} \mathrm{Rn} + _ {2} ^ {4} \mathrm{He} \\ & \mathrm {N_ {2} O_ {5} (g)} = \mathrm {N_ {2} O_ {4} (g)} + \frac {1}{2} \mathrm {O_ {2} (g)} \end{array}
$$

其他如分子重排反应 (如顺丁烯二酸转化为反丁烯二酸)、蔗糖水解反应等都是一级反应 (严格讲蔗糖水解是准一级反应, 但可以按一级反应处理)。

设有某一级反应:

$$
\begin{array}{c c c} & \mathrm{A} & \xrightarrow {k _ {1}} \quad \mathrm{P} \\ t = 0 & c _ {\mathrm{A}} ^ {0} = a & c _ {\mathrm{P}} ^ {0} = 0 \\ t = t & c _ {\mathrm{A}} = a - x & c _ {\mathrm{P}} = x \end{array}
$$

反应速率方程的微分式为

$$
\begin{array}{r l} & {r = -  \frac {\mathrm{d} c _ {\mathrm{A}}}{\mathrm{d} t} =  \frac {\mathrm{d} c _ {\mathrm{P}}}{\mathrm{d} t} = k _ {1} c _ {\mathrm{A}}} \\ & {-  \frac {\mathrm{d} (a - x)}{\mathrm{d} t} = k _ {1} (a - x) \qquad \text {或} \qquad  \frac {\mathrm{d} x}{\mathrm{d} t} = k _ {1} (a - x)} \end{array}\tag{11.12}
$$

或

$$
\frac {\mathrm{d} x}{a - x} = k _ {1} \mathrm{d} t\tag{11.13}
$$

对式 $(11.13)$ 作不定积分, 则得

$$
\ln (a - x) = - k _ {1} t + \mathrm{常数}\tag{11.14}
$$

若以 $\ln(a-x)$ 对时间 t 作图, 应得斜率为 $-k_{1}$ 的直线, 这是一级反应的特征。若对式 (11.13) 作定积分:

$$
\int_ {0} ^ {x} \frac {\mathrm{d} x}{(a - x)} = \int_ {0} ^ {t} k _ {1} \mathrm{d} t
$$

得

$$
\ln {\frac {a}{a - x}} = k _ {1} t\tag{11.15}
$$

$$
k _ {1} = \frac {1}{t} \ln \frac {a}{a - x}\tag{11.16}
$$

从反应物起始浓度 a 和 t 时刻的浓度 $(a - x)$ 即可算出速率常数 $k_{1}$ ，一级反应速率常数的量纲为 $[时间]^{-1}$ ，时间可以用秒 (s)、分 (min)、小时 (h)、天 (d) 或年 (a) 表示。

动力学的微分式 (11.12) 或式 (11.13) 只能告诉我们反应的速率随组分浓度的递变情况。为了求得浓度和时间的函数关系, 必须对微分式进行积分, 从而得到速率方程的积分式, 即式 (11.15)。根据定积分式, 在 $k_{1}, x, t$ 三个变量中, 只要知道其中任意两个就可求出第三个量 (当然反应物起始浓度 $a$ 应是已知的)。

式 (11.15) 也可写成

$$
(a - x) = a \exp (- k _ {1} t)\tag{11.17}
$$

反应物的浓度 $c_{A}$ 随时间 t 呈指数性下降, 当 $t \to \infty$ 时, $(a - x) \to 0$ , 所以一级反应需用无限长的时间才能反应完全。

若令 y 为时间 t 时反应物已作用的分数, 即

$$
y = \frac {x}{a}\tag{11.18}
$$

代入式 (11.16), 得

$$
t = \frac {1}{k _ {1}} \ln \frac {1}{1 - y}\tag{11.19}
$$

若令 $y = \frac{x}{a} = \frac{1}{2}$ 时的时间为 $t_{1/2}$ ，即反应物消耗了一半所需的时间，这个时间称为半衰期 (half life)，则

$$
t _ {1 / 2} = \frac {\ln 2}{k _ {1}} = \frac {0 . 6 9 3 1}{k _ {1}}\tag{11.20}
$$

从式 (11.20) 可知, 一级反应的半衰期与反应的速率常数 $k_{1}$ 成反比, 而与反应物的起始浓度无关。对于一个给定的一级反应, 由于 $k_{1}$ 有定值, 所以 $t_{1/2}$ 也有定值。这是一级反应的另一特点, 据此可判断一个反应是否是一级反应。

## 例11.1

某金属钚的同位素进行 $\beta$ 放射, 经 $14 \mathrm{~d}(1 \mathrm{~d} = 1$ 天) 后, 同位素的活性降低 $6.85\%$ 。试求此同位素的蜕变常数和半衰期; 要分解 $90.0\%$ , 需经过多长时间?

解 设反应开始时物质的量为 100%, 14 d 后剩余未分解者为 100% - 6.85%, 代入式 (11.16), 有

$$
\begin{array}{r l} & k _ {1} = \frac {1}{t} \ln \frac {a}{a - x} = \frac {1}{1 4 \mathrm{d}} \ln \frac {1 0 0 \%}{1 0 0 \% - 6. 8 5 \%} \\ & = 0. 0 0 5 0 7 \mathrm{d} ^ {- 1} \end{array}
$$

代入式 (11.20), 得

$$
t _ {1 / 2} = \frac {\ln 2}{0 . 0 0 5 0 7 \mathrm{d} ^ {- 1}} = 1 3 7 \mathrm{d}
$$

代入式 (11.19), 得

$$
\begin{array}{r l} t & = \frac {1}{k _ {1}} \ln \frac {1}{1 - y} \\ & = \frac {1}{0 . 0 0 5 0 7 \mathrm{d} ^ {- 1}} \ln \frac {1}{1 - 0 . 9} = 4 5 4 \mathrm{d} \end{array}
$$

## 二级反应

反应速率和物质浓度的二次方成正比者称为二级反应 (second order reaction)。

二级反应最为常见, 例如乙烯、丙烯和异丁烯的二聚作用, 乙酸乙酯的皂化, 碘化氢、甲醛的热分解等都是二级反应。二级反应的通式可以写为

(甲)

(乙)

$$
\begin{array}{l l} \mathrm{A} + \mathrm{B} \longrightarrow \mathrm{P} + \dots & r = k _ {2} [ \mathrm{A} ] [ \mathrm{B} ] \\ 2 \mathrm{A} \longrightarrow \mathrm{P} + \dots & r = k _ {2} [ \mathrm{A} ] ^ {2} \end{array}
$$

对于反应 (甲), 若以 $a, b$ 代表 A 和 B 的起始浓度, 经 $t$ 时间后有浓度为 $x$ 的 A 和等量的 B 起了作用, 则在 $t$ 时, A 和 B 的浓度分别为 $(a - x)$ 和 $(b - x)$ 。

$$
\begin{array}{r l} & \mathrm{A} + \mathrm{B} \xrightarrow {k _ {2}} \mathrm{P} + \dots \\ t = 0 & a b 0 \\ t = t & a - x b - x x \\ - \frac {\mathrm{d} c _ {\mathrm{A}}}{\mathrm{d} t} = - \frac {\mathrm{d} c _ {\mathrm{B}}}{\mathrm{d} t} = - \frac {\mathrm{d} (a - x)}{\mathrm{d} t} = - \frac {\mathrm{d} (b - x)}{\mathrm{d} t} \\ & = k _ {2} (a - x) (b - x) \end{array}\tag{11.21}
$$

或

$$
\frac {\mathrm{d} x}{\mathrm{d} t} = k _ {2} (a - x) (b - x)\tag{11.22}
$$

物质 A 和 B 的起始浓度可以相同也可以不相同。

(1) 若 A 和 B 的起始浓度相同, 即 a = b, 则反应 (甲) 的速率方程可以写成

$$
\frac {\mathrm{d} x}{\mathrm{d} t} = k _ {2} (a - x) ^ {2}\tag{11.23}
$$

移项作不定积分:

$$
\int {\frac {\mathrm{d} x}{(a - x) ^ {2}}} = \int k _ {2} \mathrm{d} t
$$

得

$$
\frac {1}{a - x} = k _ {2} t + \mathrm{常数}\tag{11.24}
$$

根据式 (11.24), 若以 $\frac{1}{a - x}$ 对 $t$ 作图, 则应得一条直线, 直线的斜率即为 $k_{2}$ , 这是利用作图法求二级反应速率常数的一种方法。

## 11.4 具有简单级数的反应

若作定积分:

$$
\int_ {0} ^ {x} \frac {\mathrm{d} x}{(a - x) ^ {2}} = \int_ {0} ^ {t} k _ {2} \mathrm{d} t
$$

则得

$$
\frac {1}{a - x} - \frac {1}{a} = k _ {2} t\tag{11.25a}
$$

或

$$
k _ {2} = \frac {1}{t} \frac {x}{a (a - x)}\tag{11.25b}
$$

如今 y 代表时间 t 后, 原始反应物已分解的分数, 即以 $y = \frac{x}{a}$ 代入式 (11.25), 则得

$$
\frac {y}{1 - y} = k _ {2} t a\tag{11.26}
$$

当原始反应物消耗一半时, $y=\frac{1}{2}$ ,则

$$
t _ {1 / 2} = \frac {1}{k _ {2} a}\tag{11.27}
$$

二级反应的半衰期与一级反应不同, 它与反应物的起始浓度成反比, 二级反应的速率常数 $k_{2}$ 的量纲为 $[\text{浓度}]^{-1} \cdot [\text{时间}]^{-1}$ , 这是二级反应的特点之一。

在 SI 单位中, 浓度的单位用 $mol \cdot m^{-3}$ , 时间的单位用 s, 而习惯上浓度的单位常用 $mol \cdot dm^{-3}$ , 时间的单位可用 s, min, h, d 等形式表示, 所以不同的单位显然会影响 k 的数值, 要注意其间的换算关系。例如, 若 k 的单位分别用 $(\mathrm{mol} \cdot \mathrm{dm}^{-3})^{-1} \cdot \min^{-1}$ 和 $(\mathrm{mol} \cdot \mathrm{m}^{-3})^{-1} \cdot \mathrm{s}^{-1}$ 表示, 则两者的数值之比为 60000。

(2) 若 A 和 B 的起始浓度不相同, 即 $a \neq b$ , 则

$$
\begin{array}{l} \frac {\mathrm{d} x}{\mathrm{d} t} = k _ {2} (a - x) (b - x) \\ \int \frac {\mathrm{d} x}{(a - x) (b - x)} = \int k _ {2} \mathrm{d} t \end{array}
$$

作不定积分后, 得

$$
\frac {1}{a - b} \mathrm{ln} \frac {a - x}{b - x} = k _ {2} t + \mathrm{常数}\tag{11.28}
$$

若作定积分, 则得

$$
k _ {2} = \frac {1}{t (a - b)} \ln \frac {b (a - x)}{a (b - x)}\tag{11.29}
$$

因为 $a \neq b$ ，所以半衰期对 A 和 B 而言是不一样的，没有统一的表示式。对于反应 (乙):

$$
\begin{array}{c c c} & 2 \mathrm{A} & \xrightarrow {k _ {2}} \mathrm{P} \\ t = 0 & a & 0 \\ t = t & a - 2 x & x \\ \frac {\mathrm{d} x}{\mathrm{d} t} = k _ {2} (a - 2 x) ^ {2} \end{array}
$$

按照前面所述的方法进行积分, 可得相应的结果。

与一级反应不同, 在二级反应中用浓度表示的速率常数和用压力表示的速率常数, 在数值上不相等。设反应 (乙) 为气相反应, 其速率方程为

$$
r = - \frac {1}{2} \frac {\mathrm{d[A]}}{\mathrm{dt}} = k _ {2} [ \mathrm{A} ] ^ {2}
$$

式中 [A] 代表 A 的浓度。若 A 是理想气体, 则有

$$
[ \mathrm{A} ] = \frac {p _ {\mathrm{A}}}{R T}
$$

或

$$
\mathrm{d} [ \mathrm{A} ] = \frac {1}{R T} \mathrm{d} p _ {\mathrm{A}}
$$

式中 $p_{A}$ 是 A 的分压, 代入速率方程, 得

$$
- \frac {1}{2 R T} \frac {\mathrm{d} p _ {\mathrm{A}}}{\mathrm{d} t} = k _ {2} \left(\frac {p _ {\mathrm{A}}}{R T}\right) ^ {2}
$$

即

$$
- \frac {1}{2} \frac {\mathrm{d} p _ {\mathrm{A}}}{\mathrm{d} t} = \frac {k _ {2}}{R T} p _ {\mathrm{A}} ^ {2} = k _ {p} p _ {\mathrm{A}} ^ {2}
$$

显然 $k_{2}$ 和 $k_{p}$ 之间差一个 $\frac{1}{RT}$ 项， $k_{2}$ 的量纲为 $[\text{浓度}]^{-1} \cdot [\text{时间}]^{-1}$ ，而 $k_{p}$ 的量纲为 $[\text{压力}]^{-1} \cdot [\text{时间}]^{-1}$ ，两者的数值也不相等。

例11.2

在 791 K 时, 在定容下乙醛的分解反应为

$$
2 \mathrm{CH} _ {3} \mathrm{CHO(g)} = 2 \mathrm{CH} _ {4} (\mathrm{g}) + 2 \mathrm{CO(g)}
$$

若乙醛的起始压力 $p_0$ 为 $48.4\mathrm{kPa}$ , 经一定时间 $t$ 后, 容器内的总压力 $p_{\text{总}}$ 数据如下:

<table><tr><td>t/s</td><td>42</td><td>105</td><td>242</td><td>384</td><td>665</td><td>1070</td></tr><tr><td> $p_{\text{总}}/\text{kPa}$ </td><td>52.9</td><td>58.3</td><td>66.3</td><td>71.6</td><td>78.3</td><td>83.6</td></tr></table>

试证明该反应为二级反应。

证明 已知乙醛的起始压力为 $p_{0}$ ，则

$$
\begin{array}{r l r} & {2 \mathrm{CH} _ {3} \mathrm{CHO(g)} = 2 \mathrm{CH} _ {4} (\mathrm{g}) + 2 \mathrm{CO(g)}} \\ {t = 0} & {\quad p _ {0}} & {0 \qquad 0} \\ {t = t} & {\quad p _ {0} - p} & {p \qquad p} \\ & {\quad p _ {\text {总}} = p _ {0} + p \text {或} p = p _ {\text {总}} - p _ {0}} \\ & {\frac {\mathrm{d} p}{\mathrm{d} t} = 2 k _ {p} (p _ {0} - p) ^ {2} = k _ {p} ^ {\prime} (p _ {0} - p) ^ {2}} \end{array}
$$

上式积分后, 得

$$
k _ {p} ^ {\prime} = \frac {1}{t} \frac {p}{p _ {0} (p _ {0} - p)}
$$

代入不同 t 时刻的 p 值, 计算所得的 $k_{p}^{\prime}$ 值确为常数, 其平均值 $k_{p}^{\prime} = 5.04 \times 10^{-5} (\text{kPa})^{-1} \cdot \text{s}^{-1}$ , 表明该反应为二级反应。计算结果如下:

<table><tr><td>t/s</td><td>42</td><td>105</td><td>242</td><td>384</td><td>665</td><td>1070</td></tr><tr><td>p/kPa</td><td>4.5</td><td>9.9</td><td>17.9</td><td>23.2</td><td>29.9</td><td>35.2</td></tr><tr><td> $\frac{{k}_{p}^{\prime }}{10^{-5}\left( {\mathrm{{kPa}}}\right) ^{-1} \cdot {\mathrm{s}}^{-1}}$ </td><td>5.04</td><td>5.06</td><td>5.01</td><td>4.95</td><td>5.02</td><td>5.15</td></tr></table>

## 例11.3

乙酸乙酯的皂化, 经研究确定是二级反应。

$$
\mathrm{CH} _ {3} \mathrm{COOC} _ {2} \mathrm{H} _ {5} + \mathrm{OH} ^ {-} \rightleftharpoons \mathrm{CH} _ {3} \mathrm{COO} ^ {-} + \mathrm{C} _ {2} \mathrm{H} _ {5} \mathrm{OH}
$$

可以用酸碱滴定法或测定混合溶液的电导率的方法来求反应物的浓度随时间的变化, 从而计算 $k_{2}$ 值。实验数据列于下表中左边三列。试分别用计算法和作图法求 $k_{2}$ 值。表中 $a$ 和 $b$ 分别表示 $\mathrm{NaOH}$ 和 $\mathrm{CH}_{3} \mathrm{COOC}_{2} \mathrm{H}_{5}$ 的起始浓度, $a = 9.80 \mathrm{~mol} \cdot \mathrm{m}^{-3}, b = 4.86 \mathrm{~mol} \cdot \mathrm{m}^{-3}$ 。

解 (1) 计算法: 因反应物起始浓度不等 $(a \neq b)$ , 所以用式 (11.29) 计算 $k_{2}$ 值, 计算结果列于表中最右一列, 平均值 $k_{2} = 1.08 \times 10^{-4} \mathrm{~mol}^{-1} \cdot \mathrm{m}^{3} \cdot \mathrm{s}^{-1}$ 。

(2) 绘图法: 根据式 (11.28), 若以 $\frac{1}{a - b} \ln \frac{a - x}{b - x}$ 对 $t$ 作图, 则应是一条直线, 直线的斜率即为 $k_{2}$ 。为此, 先计算获得不同时间的 $\frac{1}{a - b} \ln \frac{a - x}{b - x}$ 值 (结果列于表中第四列), 然后对 $t$ 作图 (见图 11.2)。

<table><tr><td>t/s</td><td> $\frac{a - x}{\mathrm{{mol}} \cdot {\mathrm{m}}^{-3}}$ </td><td> $\frac{b - x}{\mathrm{{mol}} \cdot {\mathrm{m}}^{-3}}$ </td><td> $\frac{\frac{1}{a - b}\lg\frac{a - x}{b - x}}{{\mathrm{{mol}}}^{-1} \cdot {\mathrm{m}}^{3}}$ </td><td> $\frac{{k}_{2}}{{10}^{-4}{\mathrm{\;{mol}}}^{-1} \cdot {\mathrm{m}}^{3} \cdot {\mathrm{s}}^{-1}}$ </td></tr><tr><td>0</td><td>9.80</td><td>4.86</td><td>—</td><td>—</td></tr><tr><td>178</td><td>8.92</td><td>3.98</td><td>0.1634</td><td>1.202</td></tr><tr><td>273</td><td>8.64</td><td>3.70</td><td>0.1717</td><td>1.088</td></tr><tr><td>531</td><td>7.92</td><td>2.97</td><td>0.1986</td><td>1.065</td></tr><tr><td>866</td><td>7.24</td><td>2.30</td><td>0.2321</td><td>1.041</td></tr><tr><td>1510</td><td>6.45</td><td>1.51</td><td>0.2939</td><td>1.006</td></tr><tr><td>1918</td><td>6.03</td><td>1.09</td><td>0.3463</td><td>1.064</td></tr><tr><td>2401</td><td>5.74</td><td>0.80</td><td>0.3989</td><td>1.070</td></tr></table>

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_200-399_images/909805be2d0bc3b6bed910b3b800b01b35d8495fa8eb61e6e9da63fe04278ed9.jpg)  
图 11.2 $CH_{3}COOC_{2}H_{5}$ 的水解数据图

直线的斜率为 $1.06 \times 10^{4} \mathrm{~mol}^{-1} \cdot \mathrm{m}^{3} \cdot \mathrm{s}^{-1}$ , 也即

$$
k _ {2} = 1. 0 6 \times 1 0 ^ {- 4} \mathrm{mol} ^ {- 1} \cdot \mathrm{m} ^ {3} \cdot \mathrm{s} ^ {- 1}
$$

两种方法得到基本相同的结果。

## 三级反应

反应速率与物质浓度的三次方成正比者称为三级反应 (third order reaction), 三级反应可有下列几种形式:

$$
\mathrm{A} + \mathrm{B} + \mathrm{C} \longrightarrow \text { 产   物 }\tag{11.30}
$$

$$
2 \mathrm{A} + \mathrm{B} \longrightarrow \text { 产   物 }\tag{11.31}
$$

$$
3 \mathrm{A} \longrightarrow \text { 产   物 }\tag{11.32}
$$

可分以下几种情况来讨论:

(1) 在式 (11.30) 中, 若反应物的起始浓度相同, a = b = c, 则动力学方程可

写为

$$
\frac {\mathrm{d} x}{\mathrm{d} t} = k _ {3} (a - x) ^ {3}
$$

移项作不定积分, 得

$$
\frac {1}{2 (a - x) ^ {2}} = k _ {3} t + \mathrm{常数}
$$

若作定积分, 则得

$$
k _ {3} = \frac {1}{2 t} \left[ \frac {1}{(a - x) ^ {2}} - \frac {1}{a ^ {2}} \right]\tag{11.33}
$$

如令 y 代表原始反应物的分解分数, 即 $y = \frac{x}{a}$ , 代入式 (11.33), 得

$$
\frac {y (2 - y)}{(1 - y) ^ {2}} = 2 k _ {3} a ^ {2} t
$$

当 $y = \frac{1}{2}$ 时, 其半衰期为

$$
t _ {1 / 2} = \frac {3}{2 k _ {3} a ^ {2}}\tag{11.34}
$$

(2) 在式 (11.30) 中, 若 $a = b \neq c$ , 则其动力学方程为

$$
\frac {\mathrm{d} x}{\mathrm{d} t} = k _ {3} (a - x) ^ {2} (c - x)
$$

作定积分后, 得

$$
\frac {1}{(c - a) ^ {2}} \left[ \ln \frac {(a - x) c}{(c - x) a} + \frac {x (c - a)}{a (a - x)} \right] = k _ {3} t\tag{11.35}
$$

(3) 在式 (11.30) 中, 当 $a \neq b \neq c$ 时, 其动力学方程为

$$
\frac {\mathrm{d} x}{\mathrm{d} t} = k _ {3} (a - x) (b - x) (c - x)
$$

上式经积分, 得

$$
\frac {1}{(a - b) (a - c)} \ln \frac {a}{a - x} + \frac {1}{(b - c) (b - a)} \ln \frac {b}{b - x} + \frac {1}{(c - a) (c - b)} \ln \frac {c}{c - x} = k _ {3} t\tag{11.36}
$$

(4) 对于式 (11.31), $2A + B \longrightarrow$ 产物, 有

$$
\frac {\mathrm{d} x}{\mathrm{d} t} = k _ {3} (a - 2 x) ^ {2} (b - x)
$$

积分的结果为

$$
k _ {3} = \frac {1}{t (2 b - a) ^ {2}} \left[ \frac {2 x (2 b - a)}{a (a - 2 x)} + \ln \frac {b (a - 2 x)}{a (b - x)} \right]\tag{11.37}
$$

三级反应在气相和液相中为数不多。在气相反应中，目前人们熟知的有五个反应属于三级反应，而且都与 NO 有关。这五个反应是：两个分子的 NO 和一个分子的 $Cl_{2}$ ， $Br_{2}$ ， $O_{2}$ ， $H_{2}$ 及 $D_{2}$ 的反应。即

$$
\begin{array}{r l} & 2 \mathrm{NO} + \mathrm{H} _ {2} \longrightarrow \mathrm{N} _ {2} \mathrm{O} + \mathrm{H} _ {2} \mathrm{O} \\ & 2 \mathrm{NO} + \mathrm{O} _ {2} \longrightarrow 2 \mathrm{NO} _ {2} \\ & 2 \mathrm{NO} + \mathrm{Cl} _ {2} \longrightarrow 2 \mathrm{NOCl} \\ & 2 \mathrm{NO} + \mathrm{Br} _ {2} \longrightarrow 2 \mathrm{NOBr} \\ & 2 \mathrm{NO} + \mathrm{D} _ {2} \longrightarrow \mathrm{N} _ {2} \mathrm{O} + \mathrm{D} _ {2} \mathrm{O} \end{array}
$$

上述几个三级反应, 有人认为就是三分子反应, 但后来也有人认为每个反应可能是由两个连续的双分子反应所构成的。例如:

$$
\begin{array}{r l r} {2 \mathrm{NO} \xrightarrow [ k _ {- 1} ]{k _ {1}} \mathrm{N} _ {2} \mathrm{O} _ {2}} & & {(\text { 很快 }, \text { 迅即达到平衡 })} \\ {\mathrm{N} _ {2} \mathrm{O} _ {2} + \mathrm{O} _ {2} \xrightarrow {k _ {2}} 2 \mathrm{NO} _ {2}} & & {(\text { 慢 })} \end{array}
$$

整个反应的速率取决于最慢的一步, 所以反应的速率方程为

$$
\frac {\mathrm{d} x}{\mathrm{d} t} = k _ {2} \left[ \mathrm{N} _ {2} \mathrm{O} _ {2} \right] \left[ \mathrm{O} _ {2} \right]
$$

在第一个反应中

$$
\frac {[ \mathrm{N} _ {2} \mathrm{O} _ {2} ]}{[ \mathrm{NO} ] ^ {2}} = \frac {k _ {1}}{k _ {- 1}} = K
$$

所以

$$
[ \mathrm{N} _ {2} \mathrm{O} _ {2} ] = \frac {k _ {1}}{k _ {- 1}} [ \mathrm{NO} ] ^ {2}
$$

代入反应速率方程中, 得

$$
\frac {\mathrm{d} x}{\mathrm{d} t} = \frac {k _ {1} k _ {2}}{k _ {- 1}} [ \mathrm{NO} ] ^ {2} [ \mathrm{O} _ {2} ] = k _ {3} [ \mathrm{NO} ] ^ {2} [ \mathrm{O} _ {2} ]
$$

所以整个反应是三级反应。

基元反应呈三级很少见的原因是三个分子同时碰撞的机会不多。在气相中一些游离原子的化合可以看作三分子反应,例如:

$$
\mathrm{X} \cdot + \mathrm{X} \cdot + \mathrm{M} \longrightarrow \mathrm{X} _ {2} + \mathrm{M}
$$

式中 X·代表 I·, Br·或 H·; M 代表杂质或器壁分子或第三种惰性分子, M 的作用只是吸收反应所释放的热量。由于 M 的浓度并没有发生变化, 所以这些三分子反应表现为二级反应。在溶液中, 由于几个双分子的连续反应, 最后其速率方程也可能呈现三级反应的形式。例如, 在乙酸或硝基苯溶液中, 含不饱和 C=C 键化合物的加成作用就常是三级反应。此外, 在水溶液中 $FeSO_{4}$ 的氧化, $Fe^{3+}$ 和 $I^{-}$ 的作用, 以及在乙醚中苯酰氯与乙醇的作用, 均是三级反应。

## 零级反应和准级反应

## 1. 零级反应

反应速率与物质的浓度无关者称为零级反应 (zeroth order reaction)。其速率可表示为

$$
r = - \frac {\mathrm{d} c _ {\mathrm{A}}}{\mathrm{d} t} = k _ {0} \qquad \text {或} \qquad r = \frac {\mathrm{d} x}{\mathrm{d} t} = k _ {0}\tag{11.38}
$$

上式经移项积分, 得

$$
x = k _ {0} t\tag{11.39}
$$

当 $x = \frac{a}{2}$ 时， $t_{1/2} = \frac{a}{2k_0}$ 。

反应总级数为零的反应并不多, 已知的零级反应中最多的是表面催化反应。例如, 氨在金属钨上的分解反应:

$$
2 \mathrm{NH} _ {3} (\mathrm{g}) \xrightarrow {\mathrm{W催化剂}} \mathrm{N} _ {2} (\mathrm{g}) + 3 \mathrm{H} _ {2} (\mathrm{g})
$$

由于反应只在催化剂表面上进行, 反应速率只与表面状态有关。若金属 W 表面已被吸附的 $NH_{3}$ 所饱和, 再增加 $NH_{3}$ 的浓度对反应速率不再有影响, 此时反应对 $NH_{3}$ 呈零级反应。

## 2. 准级反应

设某反应的速率方程为

$$
r = k c _ {\mathrm{A}} ^ {\alpha} c _ {\mathrm{B}} ^ {\beta}
$$

该反应的级数显然应是 $(\alpha + \beta)$ 。如果大大增加 B 的浓度，以致在反应过程中 B 的浓度变化很小或基本不变，则可把 $c_{B}^{\beta}$ 当作常数并入速率常数 k 中，得

$$
r = k ^ {\prime} c _ {\mathrm{A}} ^ {\alpha}
$$

于是该反应就变成 $\alpha$ 级反应, 由于 $k' = kc_{B}^{\beta}$ , 显然 $k'$ 与 k 的单位不同。 $\alpha$ 级反应的结论是在特殊情况下形成的, 故称为准 $\alpha$ 级反应 (pseudo $\alpha$ order reaction)。

例如, 蔗糖转化为葡萄糖和果糖的反应:

$$
\begin{array}{c c c} \mathrm{C} _ {1 2} \mathrm{H} _ {2 2} \mathrm{O} _ {1 1} + \mathrm{H} _ {2} \mathrm{O} & \xrightarrow {\mathrm{H} _ {3} \mathrm{O} ^ {+}} \mathrm{C} _ {6} \mathrm{H} _ {1 2} \mathrm{O} _ {6} + \mathrm{C} _ {6} \mathrm{H} _ {1 2} \mathrm{O} _ {6} \\ \text {蔗糖} & & \text {果糖} \quad \text {葡萄糖} \end{array}
$$

该反应的速率方程早在 1850 年就由 Wilhelmy 所建立, 这个反应是化学动力学中最早经过定量研究的, 其速率方程为

$$
r = - \frac {\mathrm{d} [ \mathrm{S} ]}{\mathrm{d} t} = k [ \mathrm{S} ]
$$

式中 [S] 代表蔗糖的浓度。速率方程中不出现水的浓度 $\left[\mathrm{H}_{2} \mathrm{O}\right]$ 项, 是因为在反应中水分子的消耗相对于水的浓度 $\left(\left[\mathrm{H}_{2} \mathrm{O}\right] = \frac{1000 \mathrm{~g} \cdot \mathrm{dm}^{-3}}{18 \mathrm{~g} \cdot \mathrm{mol}^{-1}} = 55.56 \mathrm{~mol} \cdot \mathrm{dm}^{-3}\right)$ 来说是微不足道的。设 $[\mathrm{S}] = 0.1 \mathrm{~mol} \cdot \mathrm{dm}^{-3}$ , 即使蔗糖全部转化, 水浓度的变化也只不过是 $\frac{0.1}{55.56}$ , 还不到 $0.2\%$ , 故水的浓度可视为不变, 而已并入速率常数 $k$ 中, 所以在速率方程中只出现蔗糖的浓度 [S] 项, 故当时称此类反应为准单分子反应 (pseudo unimolecular reaction)。此后, 在对反应的级数和反应分子数有了明确的界定之后, 此类反应均称为准一级反应 (pseudo first order reaction)。

后来, 又有人研究了蔗糖在酸性溶液中的催化转化反应, 其速率方程应为

$$
r = - \frac {\mathrm{d} [ \mathrm{S} ]}{\mathrm{d} t} = k [ \mathrm{S} ] [ \mathrm{H} _ {2} \mathrm{O} ] [ \mathrm{H} ^ {+} ]
$$

同样, 由于反应中 $\left[\mathrm{H}_{2} \mathrm{O}\right]$ 和 $\left[\mathrm{H}^{+}\right]$ 基本上不变, 故得

$$
r = - \frac {\mathrm{d} [ \mathrm{S} ]}{\mathrm{d} t} = k ^ {\prime} [ \mathrm{S} ]
$$

显然, 在酸性溶液中蔗糖的转化反应依然是准一级反应 (至于某种反应物的浓度大到什么程度方可以认为其浓度不变, 并没有统一的标准。通常认为, 为了保证反应是准一级的, 至少需要过量 40 倍以上)。

## 例11.4

蔗糖的转化是一级反应:

$$
\begin{array}{c c c} \mathrm{C} _ {1 2} \mathrm{H} _ {2 2} \mathrm{O} _ {1 1} + \mathrm{H} _ {2} \mathrm{O} & \xrightarrow {\mathrm{H} _ {3} \mathrm{O} ^ {+}} & \mathrm{C} _ {6} \mathrm{H} _ {1 2} \mathrm{O} _ {6} + \mathrm{C} _ {6} \mathrm{H} _ {1 2} \mathrm{O} _ {6} \\ \text {蔗糖} & & \text {果糖} \quad \text {葡萄糖} \end{array}
$$

$H_{3}O^{+}$ 在反应中只起催化剂的作用。蔗糖是右旋的，设起始旋光度为 $\alpha_{0}$ 。水解后所得到的葡萄糖是右旋的，果糖是左旋的。由于后者的旋光度大，所以水解后的混合物呈左旋，故蔗糖的水解作用又称为转化反应 (inversion reaction)。设 $\alpha$ 为反应进行到 t 时刻混合物的旋光度， $\alpha_{\infty}$ 为水解完毕时的旋光度。试根据表 11.1 所列的实验数据（一、二、三列），求该反应的速率常数及其平均值。

表 11.1 ${298}\mathrm{\;K}$ 时,质量分数为 0.2 的蔗糖溶液在有 ${0.5}\mathrm{{mol}} \cdot  {\mathrm{{dm}}}^{-3}$ 乳酸存在时的水解数据

<table><tr><td>t/min</td><td> $\alpha/(^{\circ})$ </td><td> $(\alpha-\alpha_{\infty})/(^{\circ})$ </td><td> $k_1(计算值)/(10^{-5} min^{-1})$ </td></tr><tr><td>0</td><td>34.50</td><td>45.27</td><td>—</td></tr><tr><td>1435</td><td>31.10</td><td>41.87</td><td>5.441</td></tr><tr><td>4315</td><td>25.00</td><td>35.77</td><td>5.459</td></tr><tr><td>7070</td><td>20.16</td><td>30.93</td><td>5.388</td></tr><tr><td>11360</td><td>13.98</td><td>24.75</td><td>5.315</td></tr><tr><td>14170</td><td>10.61</td><td>21.38</td><td>5.294</td></tr><tr><td>16935</td><td>7.57</td><td>18.34</td><td>5.335</td></tr><tr><td>19815</td><td>5.08</td><td>15.85</td><td>5.296</td></tr><tr><td>29925</td><td>-1.65</td><td>9.12</td><td>5.354</td></tr><tr><td>∞</td><td>-10.77</td><td>0.00</td><td>—</td></tr></table>

解 因在式 (11.16) 中用到了浓度比 $\frac{a}{a - x}$ , 所以任何与浓度成比例的量 (如旋光度、分压等) 均可用来代替公式中的浓度项, 而不会影响 $k_{1}$ 的计算值。设用 $(\alpha_{0} - \alpha_{\infty})$ 代表蔗糖的起始量, 用 $(\alpha - \alpha_{\infty})$ 代表 $t$ 时刻蔗糖的量, 则代入式 (11.16), 得

$$
k _ {1} = \frac {1}{t} \ln \frac {\alpha_ {0} - \alpha_ {\infty}}{\alpha - \alpha_ {\infty}}
$$

计算结果列表于 11.1 中最后一列, 其平均值为

$$
k _ {1} = 5. 3 6 0 \times 1 0 ^ {- 5} \mathrm{min} ^ {- 1}
$$

为了便于查阅, 将上述几种具有简单级数反应的速率方程和特征列于表 11.2 中, 人们常用这些特征来判别反应的级数。

表 11.2 具有简单级数反应的速率方程和特征

<table><tr><td>级数</td><td>反应类型</td><td>速率方程的定积分式</td><td>浓度与时间的线性关系</td><td>半衰期 $t_{1/2}$ </td><td>速率常数k的量纲</td></tr><tr><td>一级</td><td>A→产物</td><td> $\ln\frac{a}{a-x}=k_1t$ </td><td> $\ln\frac{1}{a-x}\sim t$ </td><td> $\frac{\ln 2}{k_1}$ </td><td>[时间] $^{-1}$ </td></tr><tr><td rowspan="2">二级</td><td>A+B→产物(a=b)</td><td> $\frac{1}{a-x}-\frac{1}{a}=k_2t$ </td><td> $\frac{1}{a-x}\sim t$ </td><td> $\frac{1}{k_2a}$ </td><td rowspan="2">[浓度] $^{-1}$ .[时间] $^{-1}$ </td></tr><tr><td>A+B→产物(a≠b)</td><td> $\frac{1}{a-b}\ln\frac{b(a-x)}{a(b-x)}=k_2t$ </td><td> $\ln\frac{b(a-x)}{a(b-x)}\sim t$ </td><td> $t_{1/2}(A)\neq t_{1/2}(B)$ </td></tr><tr><td>三级</td><td>A+B+C→产物(a=b=c)</td><td> $\frac{1}{2}\left[\frac{1}{(a-x)^2}-\frac{1}{a^2}\right]=k_3t$ </td><td> $\frac{1}{(a-x)^2}\sim t$ </td><td> $\frac{3}{2}\frac{1}{k_3a^2}$ </td><td>[浓度] $^{-2}$ .[时间] $^{-1}$ </td></tr><tr><td>零级</td><td>表面催化反应</td><td> $x=k_0t$ </td><td> $x\sim t$ </td><td> $\frac{a}{2k_0}$ </td><td>[浓度] $^{\cdot}$ [时间] $^{-1}$ </td></tr><tr><td>n级 $n\neq 1$ </td><td>反应物→产物</td><td> $\frac{1}{n-1}\left[\frac{1}{(a-x)^{n-1}}-\frac{1}{a^{n-1}}\right]=kt$ </td><td> $\frac{1}{(a-x)^{n-1}}\sim t$ </td><td> $A\frac{1}{a^{n-1}}$ (A为常数)</td><td>[浓度] $^{1-n}$ .[时间] $^{-1}$ </td></tr></table>

## 反应级数的测定法

动力学方程都是根据大量的实验数据或用拟合法来确定的。设化学反应的速率方程可写为如下形式:

$$
r = k c _ {\mathrm{A}} ^ {\alpha} c _ {\mathrm{B}} ^ {\beta} \dots
$$

有些复杂反应的速率方程有时也可简化为这样的形式。在化工生产中，在不知其准确的反应历程的情况下，也常常采用这样的形式作为经验公式用于化工设计中。确定动力学方程的关键是确定 $\alpha, \beta, \cdots$ 的数值，这些数值不同，其速率方程的积分形式也不同。确定反应级数和速率常数的常用方法有如下几种。

(1) 积分法 例如一个反应的速率方程可表示为

$$
\begin{array}{r l} & r = - \frac {1}{a} \frac {\mathrm{d} [ \mathrm{A} ]}{\mathrm{d} t} = k [ \mathrm{A} ] ^ {\alpha} [ \mathrm{B} ] ^ {\beta} \\ & \frac {\mathrm{d} [ \mathrm{A} ]}{[ \mathrm{A} ] ^ {\alpha} [ \mathrm{B} ] ^ {\beta}} = - a k \mathrm{d} t \end{array}
$$

通常可先假定一组 $\alpha$ 和 $\beta$ 值, 求出这个积分项, 然后对 t 作图。例如, 设 $\beta = 0, \alpha = 1$ , 即反应为一级, 根据一级反应的特征, 以 $\ln \frac{1}{a - x}$ 对 t 作图, 如果得到的是直线, 则该反应就是一级反应。

如果设 $\beta = 1, \alpha = 1$ ，且 $a \neq b$ ，则根据二级反应的特点，以 $\frac{1}{a - b} \ln \frac{a - x}{b - x}$ 对 t 作图，若得一直线，则该反应就是二级反应。

这种方法实际上是一个尝试的过程 [所以也叫尝试法 (trial method)]。如果尝试成功，则所设的 $\alpha, \beta$ 值就是正确的。如果得到的不是直线，则须重新假设 $\alpha, \beta$ 的值，重新进行尝试，直到得到直线为止。当然也可以不用作图法，而直接进行计算，即将实验数据（各不同的时间 t 和相应的浓度 x）代入表 11.2 中速率方程的积分公式, 分别按一、二、三级反应的公式计算速率常数 $k$ 。如果各组实验数据代入一级反应的方程式, 得到的 $k$ 是一个常数, 则该反应就是一级反应。如果代到二级的公式中得到的 $k$ 是一个常数, 则该反应就是二级反应, 依此类推。如果代入表11.2中的积分公式, 所算出的 $k$ 都不是一个常数, 或者作图时得不到直线, 则该反应就不是具有简单整数级数的反应。尝试法的缺点是不够灵敏, 而且如果实验的浓度范围不够大, 则很难明显区别出究竟是几级 (这种方法的计算工作量较大, 但在有了计算机程序之后, 这也是轻而易举的事)。积分法一般对反应级数是简单整数的反应的结果较好。当级数是分数时, 很难尝试成功, 最好用微分法。

(2) 微分法 为简便, 先讨论一个简单反应:

$$
\mathrm{A} \longrightarrow \text { 产   物 }
$$

在 t 时 A 的浓度为 c, 该反应的速率方程设为

$$
r = - \frac {\mathrm{d} c}{\mathrm{d} t} = k c ^ {n}
$$

等式双方取对数后得

$$
\lg r = \lg \left(- \frac {\mathrm{d} c}{\mathrm{d} t}\right) = \lg k + n \lg c\tag{11.40}
$$

先根据实验数据, 将浓度 c 对时间 t 作图, 然后在不同的浓度 $c_{1}, c_{2}, \cdots$ 各点上求曲线的斜率 $r_{1}, r_{2}, \cdots$ 再以 lg r 对 lg c 作图。若所设速率方程式是对的, 则应得一直线, 该直线的斜率 n 即为反应级数。或者将一系列的 $r_{i}$ 和 $c_{i}$ 代入式 (11.40), 例如取 $r_{1}, c_{1}$ 和 $r_{2}, c_{2}$ 两组数据, 可得

$$
\begin{array}{l} \lg r _ {1} = \lg k + n \lg c _ {1} \\ \lg r _ {2} = \lg k + n \lg c _ {2} \end{array}
$$

将两式相减, 得

$$
n = \frac {\lg r _ {1} - \lg r _ {2}}{\lg c _ {1} - \lg c _ {2}}
$$

用上述方法求出若干个 n，然后求出平均值。

也可先假设一个 $n$ 值, 把一系列的 $r_i$ 和 $c_i$ 代入式 (11.40), 算出一系列的 $k$ 值。如果假设正确, 则 $k$ 值基本上应为一差异不大的常数。

若某反应的动力学方程为

$$
r = k c _ {\mathrm{A}} ^ {\alpha} c _ {\mathrm{B}} ^ {\beta} c _ {\mathrm{C}} ^ {\gamma}
$$

等式双方取对数后, 得

$$
\lg r = \lg k + \alpha \lg c _ {\mathrm{A}} + \beta \lg c _ {\mathrm{B}} + \gamma \lg c _ {\mathrm{C}}
$$

或

$$
\lg r = \lg k + \alpha \left(\lg c _ {\mathrm{A}} + \frac {\beta}{\alpha} \lg c _ {\mathrm{B}} + \frac {\gamma}{\alpha} \lg c _ {\mathrm{C}}\right)
$$

可以通过一组实验数据, 由解联立方程式获得 $\alpha, \beta, \gamma$ 值。或者以 $\lg r$ 对 $\lg c_{\mathrm{A}}$ 作图, 如得一直线, 则 $\beta$ 和 $\gamma$ 等于零, 从直线斜率求出 $\alpha$ 值。如果得不到一直线, 可以改变 $\frac{\beta}{\alpha}$ 和 $\frac{\gamma}{\alpha}$ 的比值, 以 $\left(\lg c_{\mathrm{A}} + \frac{\beta}{\alpha} \lg c_{\mathrm{B}} + \frac{\gamma}{\alpha} \lg c_{\mathrm{C}}\right)$ 对 $\lg r$ 作图。经过多次变更 $\frac{\beta}{\alpha}$ 和 $\frac{\gamma}{\alpha}$ 的值 (当然这个比值只能是简单的整数或分数), 直到得到直线为止, 就可分别得 $\alpha, \beta, \gamma$ 值。这样定级数的方法如果采用普通计算方法显然是比较麻烦的, 可借助于计算机解决问题。

由于在绘图或计算中所用到的数据是 $r$ （即 $-\frac{\mathrm{d}c}{\mathrm{d}t}$ ），故此法称为微分法。用此法求级数，不仅可处理级数为整数的反应，也可以处理级数为分数的反应。

用微分法时, 最好使用开始时的反应速率值, 即用一系列不同的起始浓度 $c_{0}$ , 作不同的时间 t 对浓度 c 的曲线, 然后在不同的起始浓度 $c_{0}$ 处求出相应的斜率 $\left(-\frac{\mathrm{d}c}{\mathrm{d}t}\right)$ , 以后的处理方法与上面相同。采用起始浓度法的优点是可以避免反应产物的干扰。

(3) 半衰期法 从半衰期与浓度的关系可知, 若反应物的起始浓度都相同, 则

$$
t _ {1 / 2} = A \frac {1}{a ^ {n - 1}}\tag{11.41}
$$

式中 $n(n \neq 1)$ 为反应级数, 对同一反应 A 为常数。如以两个不同的起始浓度 a 和 $a'$ 进行实验, 则

$$
\frac {t _ {1 / 2}}{t _ {1 / 2} ^ {\prime}} = \left(\frac {a ^ {\prime}}{a}\right) ^ {n - 1}
$$

上式取对数后, 得

$$
n = 1 + \frac {\lg \frac {t _ {1 / 2}}{t _ {1 / 2} ^ {\prime}}}{\lg \frac {a ^ {\prime}}{a}}
$$

由两组数据就可以求出 n，如数据较多，也可以用作图法。将式 (11.41) 取对数， $\lg t_{1/2} = (1 - n)\lg a + \lg A$ 。将 $\lg t_{1/2}$ 对 lga 作图，从斜率可求出 n。

这个方法并不限定反应一定要进行到 $\frac{1}{2}$ , 也可以取反应进行到 $\frac{1}{4}, \frac{1}{8}$ 等的时间来计算。

## (4) 改变物质数量比例的方法 设速率方程式为

$$
r = k c _ {\mathrm{A}} ^ {\alpha} c _ {\mathrm{B}} ^ {\beta} c _ {\mathrm{C}} ^ {\gamma}
$$

若设法保持 A 和 C 的浓度不变, 而将 B 的浓度加大一倍, 若反应速率也比原来加大一倍, 则可确定 $c_{B}$ 的方次 $\beta = 1$ 。同理, 若保持 B 和 C 的浓度不变, 而把 A 的浓度加大一倍, 若速率增加为原来的 4 倍, 则可确定 $c_{A}$ 的方次 $\alpha = 2$ 。这种方法可应用于较复杂的反应。

## 例11.5

## 草酸钾与氯化高汞的反应方程式为

$$
2 \mathrm{HgCl} _ {2} + \mathrm{K} _ {2} \mathrm{C} _ {2} \mathrm{O} _ {4} = 2 \mathrm{KCl} + 2 \mathrm{CO} _ {2} + \mathrm{Hg} _ {2} \mathrm{Cl} _ {2}
$$

已知在 $373 \, K$ 时, $Hg_{2}Cl_{2}$ 从起始浓度不同的反应物溶液中沉淀的数据如下所示:

<table><tr><td>实验次数</td><td> $\frac{{c}_{0}\left( {{\mathrm{K}}_{2}{\mathrm{C}}_{2}{\mathrm{O}}_{4}}\right) }{\mathrm{{mol}} \cdot {\mathrm{{dm}}}^{-3}}$ </td><td> $\frac{{c}_{0}\left( {\mathrm{{HgCl}}}_{2}\right) }{\mathrm{{mol}} \cdot {\mathrm{{dm}}}^{-3}}$ </td><td> $\frac{t}{\min }$ </td><td> $\frac{x\left( {{\mathrm{{Hg}}}_{2}{\mathrm{{Cl}}}_{2}}\right) }{\mathrm{{mol}} \cdot {\mathrm{{dm}}}^{-3}}$ </td></tr><tr><td>1</td><td>0.0836</td><td>0.404</td><td>65</td><td>0.0068</td></tr><tr><td>2</td><td>0.0836</td><td>0.202</td><td>120</td><td>0.0031</td></tr><tr><td>3</td><td>0.0418</td><td>0.404</td><td>62</td><td>0.0032</td></tr></table>

试求反应的级数。

解 设用平均速率代表瞬时速率 (这只有在反应速率较慢, 或者反应时间较短时才是可行的, 否则误差较大), $Hg_{2}Cl_{2}$ 的生成速率在 1,2 两次实验中分别为

$$
\left(\frac {\Delta x}{\Delta t}\right) _ {1} = \frac {0 . 0 0 6 8}{6 5} \mathrm{mol} \cdot \mathrm{dm} ^ {- 3} \cdot \mathrm{min} ^ {- 1}
$$

和

$$
\left(\frac {\Delta x}{\Delta t}\right) _ {2} = \frac {0 . 0 0 3 1}{1 2 0} \mathrm{mol} \cdot \mathrm{dm} ^ {- 3} \cdot \mathrm{min} ^ {- 1}
$$

又反应速率可写为

$$
\frac {\Delta x}{\Delta t} = k [ \mathrm{HgCl} _ {2} ] ^ {n} [ \mathrm{K} _ {2} \mathrm{C} _ {2} \mathrm{O} _ {4} ] ^ {m}
$$

若选择 1, 2 两次实验的数据, 可得

$$
\frac {\left(\frac {\Delta x}{\Delta t}\right) _ {1}}{\left(\frac {\Delta x}{\Delta t}\right) _ {2}} = \frac {k (0 . 0 8 3 6) ^ {m} (0 . 4 0 4) ^ {n}}{k (0 . 0 8 3 6) ^ {m} (0 . 2 0 2) ^ {n}} = \frac {\frac {0 . 0 0 6 8}{6 5}}{\frac {0 . 0 0 3 1}{1 2 0}}
$$

在两次实验中反应物 $K_{2}C_{2}O_{4}$ 的起始浓度是一样的, 可以从比值中消去, 由此可解得 n=2。同理, 用 1,3 两次实验数据可求得 m=1, 故此反应是三级反应。

$$
r = k _ {3} [ \mathrm{HgCl} _ {2} ] ^ {2} [ \mathrm{K} _ {2} \mathrm{C} _ {2} \mathrm{O} _ {4} ]
$$

## 例11.6

三甲基胺与溴化正丙烷溶于溶剂苯中, 其起始浓度均为 $0.1 \, mol \cdot dm^{-3}$ , 将反应物分别放入几个玻璃瓶中, 封口后, 浸于 412.6 K 的恒温槽中, 每经历一定时间, 取出一瓶快速冷却, 使反应 “停止”, 然后分析其成分, 结果如下表中的前三列所示:

<table><tr><td>瓶号</td><td>经历时间 t/s</td><td>反应物起作用的摩尔分数</td><td> $\frac{x}{10^{-2} \text{ mol} \cdot \text{dm}^{-3}}$ </td><td> $\frac{k_1}{10^{-4} \text{ s}^{-1}}$ </td><td> $\frac{k_2}{10^{-3} \text{ mol}^{-1} \cdot \text{dm}^3 \cdot \text{s}^{-1}}$ </td></tr><tr><td>1</td><td>780</td><td>0.112</td><td>1.12</td><td>1.52</td><td>1.62</td></tr><tr><td>2</td><td>2040</td><td>0.257</td><td>2.57</td><td>1.46</td><td>1.70</td></tr><tr><td>3</td><td>3540</td><td>0.367</td><td>3.67</td><td>1.29</td><td>1.64</td></tr><tr><td>4</td><td>7200</td><td>0.552</td><td>5.52</td><td>1.12</td><td>1.71</td></tr></table>

试判断此反应是二级还是一级反应, 并求出其速率常数 k 值 (假定在实验的范围内反应只向右进行)。

解 反应可以写作

$$
\begin{array}{r l r l r l} & \mathrm {N(C H_ {3}) _ {3}} + \mathrm {CH_ {3} CH_ {2} CH_ {2} Br} & \longrightarrow & (\mathrm {CH_ {3}) _ {3} (C_ {3} H_ {7}) N^ {+}} + \mathrm {Br^ {-}} \\ t = 0 & a & b & 0 & 0 \\ t = t & a - x & b - x & x & x \end{array}
$$

可以用两种方法求解:

(1) 积分法 若设反应对三甲基胺是一级, 对溴化正丙烷是零级 (若设反应对溴化正丙烷是一级时, 其情况与此相同), 则

$$
\frac {\mathrm{d} x}{\mathrm{d} t} = k _ {1} (a - x)
$$

移项作定积分, 得

$$
k _ {1} = \frac {1}{t} \ln \frac {a}{a - x}
$$

已知 $a = 0.1 \, mol \cdot dm^{-3}$ ，在不同的时间 t 时的 x 值列于上表第四列。将第 1 瓶的数据代入 $k_{1}$ 的计算式中：

$$
\begin{array}{r l} k _ {1} & = \frac {1}{7 8 0 \mathrm{s}} \ln \frac {0 . 1}{0 . 1 - 0 . 0 1 1 2} \\ & = 1. 5 2 \times 1 0 ^ {- 4} \mathrm{s} ^ {- 1} \end{array}
$$

同法可求得其他瓶号的 $k_{1}$ 值, 列于上表第五列。显然, $k_{1}$ 不为常数, 所以该反应不是一级反应。

若设反应为二级反应 $(a = b)$ , 则

$$
\frac {\mathrm{d} x}{\mathrm{d} t} = k _ {2} (a - x) ^ {2}
$$

移项作定积分, 得

$$
k _ {2} = \frac {1}{t} \frac {x}{a (a - x)}
$$

代入各瓶号的实验数据, 得到的 $k_{2}$ 值列于上表第六列。 $k_{2}$ 值近似为一常数, 所以该反应为二级反应, 其速率常数为

$$
k _ {2} = 1. 6 7 \times 1 0 ^ {- 3} \mathrm{mol} ^ {- 1} \cdot \mathrm{dm} ^ {3} \cdot \mathrm{s} ^ {- 1}
$$

(2) 微分法 以 $x$ 对 $t$ 作图, 在曲线上任一点的斜率 $\frac{\mathrm{d}x}{\mathrm{d}t}$ 就是该反应的速率

$$
r = - \frac {\mathrm{d} (a - x)}{\mathrm{d} t} = \frac {\mathrm{d} x}{\mathrm{d} t}
$$

图 11.3 是在 $(\mathrm{CH}_{3})_{3}\mathrm{N}$ 和 $CH_{3}CH_{2}CH_{2}Br$ 反应系统中浓度 x 与时间 t 的关系图。从图中可找出不同浓度时曲线的斜率，列于表 11.3。

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_200-399_images/57a1c91a43049b7e6aa41e348b7f104172e818423d4f52cdb5b617708c346969.jpg)  
图 11.3 在 $(\mathrm{CH}_{3})_{3}\mathrm{N}$ 和 $CH_{3}CH_{2}CH_{2}Br$ 反应系统中浓度 x 与时间 t 的关系图

表 11.3 图 11.3 中不同浓度时曲线的斜率

<table><tr><td colspan="2">浓度 $c/(mol·dm^{-3})$ </td><td rowspan="2">反应速率 $r\left(= \frac{dx}{dt}\right)$  $10^{-5} mol·dm^{-3}·s^{-1}$ </td></tr><tr><td>x</td><td>a-x</td></tr><tr><td>0.0</td><td>0.10</td><td>1.58</td></tr><tr><td>0.01</td><td>0.09</td><td>1.38</td></tr><tr><td>0.02</td><td>0.08</td><td>1.14</td></tr><tr><td>0.03</td><td>0.07</td><td>0.79</td></tr><tr><td>0.04</td><td>0.06</td><td>0.64</td></tr><tr><td>0.05</td><td>0.05</td><td>0.45</td></tr></table>

若反应是一级的, 则

$$
r = \frac {\mathrm{d} x}{\mathrm{d} t} = k _ {1} (a - x)
$$

或

$$
\lg r = \lg k _ {1} + \lg (a - x)
$$

如以 $\lg r$ 对 $\lg (a - x)$ 作图, 则所得直线的斜率应等于1。

若反应是二级的, 则

$$
r = \frac {\mathrm{d} x}{\mathrm{d} t} = k _ {2} (a - x) (b - x) = k _ {2} (a - x) ^ {2}
$$

或

$$
\lg r = \lg k _ {2} + 2 \lg (a - x)
$$

以 $\lg r$ 对 $\lg(a-x)$ 作图, 则所得直线的斜率应等于 2。

根据表 11.3 中的实验数据, 作图如图 11.4。

![](物理化学下（第六版）傅献彩z-library.sk,1lib.sk,z-lib.sk_200-399_images/299e7cfe6885a925cfd5650bc89312363e823ab5f0e0462c239b961174695f15.jpg)  
图 11.4 在 $(\mathrm{CH}_{3})_{3}\mathrm{N}$ 和 $CH_{3}CH_{2}CH_{2}Br$ 反应系统中 $\lg r$ 与 $\lg(a-x)$ 的关系图

所得的实验点均落在斜率等于 2.0 的直线上。该直线的截距为 -2.76，故直线的方程式为

$$
\lg r = - 2. 7 6 + 2. 0 \lg (a - x)
$$

$$
\lg k _ {2} = - 2. 7 6
$$

$$
k _ {2} = 1. 7 4 \times 1 0 ^ {- 3} \mathrm{mol} ^ {- 1} \cdot \mathrm{dm} ^ {3} \cdot \mathrm{s} ^ {- 1}
$$

斜率等于 1.0 的直线在图中用虚线标出, 它显然与实验值相差太远了。

以上无论用微分法还是用积分法都证明反应是二级的。从上述的例子可以看出，微分法更易于判断反应的级数。

