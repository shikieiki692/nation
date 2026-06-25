---
title: Boltzmann统计初步
aliases: [Boltzmann Statistics, 统计熵, 最概然分布]
type: 知识点
template_version: v1.3
subject: 决赛要求
module: 决赛要求
submodule: 物理化学深化
syllabus_stage: 决赛
parent_overview: 中国化学奥林匹克基本要求-总览
parent_module: 决赛要求-物理化学深化
syllabus_code: [决赛04]
syllabus_module: [物理化学深化]
tags: [化竞, 决赛, 物理化学, 统计热力学]
related: [化学热力学, 熵, 化学势与平衡]
prerequisite: [化学热力学]
problem_types: [题型-Boltzmann计算]
difficulty: 5
importance: 4
status: 已填充
stage: published
sources: []
source_type: []
source_notes: []
review_cycle: 30d
has_images: false
image_count: 0
images_priority: low
images_note: "当前以文字、公式或表格表达为主，暂未单独配置图像文件；后续备课如需增强直观性，再按需补图。"
teaching_ready: false
key_images: []
updated: 2026-06-14
---

# Boltzmann 统计初步

- 总览：[[中国化学奥林匹克基本要求-总览]]
- 所属模块：[[决赛要求-物理化学深化]]
- 对应考纲条目：[[决赛04-热力学]]

## 一、定义

Boltzmann 统计初步讨论大量粒子在不同能级上的分布规律，以及这种分布如何通向熵、配分函数和热力学量。它是“微观状态数如何长成宏观热力学”的起点。

## 二、考纲对应

- 对应 `[[决赛04-热力学]]` 中关于统计熵、Boltzmann 分布与配分函数初步的要求
- 决赛层面重点不是完整统计力学推导，而是能把 **分布公式、简并度、配分函数和热力学量** 连起来用

## 三、核心原理

- 系统的微观状态数 $W$ 决定统计熵：$S = k_B \ln W$
- 在定温条件下，粒子按最概然分布占据能级，得到 Boltzmann 分布
- 简并度 $g_i$ 会放大某一能级的总布居，因此“能级布居”不只由能量决定
- 配分函数 $q$ 是所有热可及状态的加权求和，几乎所有平均热力学量都可由它导出

## 四、关键结论

1. Boltzmann 分布的本质是“高能态可以占据，但要按指数权重付代价”
2. 判断布居时必须同时看**能量差**和**简并度**
3. 配分函数不是单独的物理量，而是组织所有统计信息的“总目录”
4. 统计热力学把熵从经验量变成了可由微观状态数解释的量

## 五、常见分类或情形

- **两能级布居比较**：最常见于转动、振动或电子能级相对布居计算
- **配分函数估算**：判断某运动模式在给定温度下是否被热激发
- **高温/低温极限分析**：看转动、振动等自由度在不同温区的贡献
- **简并度主导情形**：某高能级虽能量更高，但因简并度大而总布居不低

## 六、适用条件与限制

- 这里默认系统接近热平衡，非平衡激发体系不能直接套用最简单的 Boltzmann 分布
- 竞赛里通常讨论经典的 Maxwell-Boltzmann 统计，不涉及 Fermi-Dirac 与 Bose-Einstein 的完整量子统计区分
- 高温近似、连续近似和 Stirling 近似都各有适用范围，不能不加判断地通用
- 真正复杂多自由度体系中，配分函数往往只能分解近似，不能总是精确闭式求解

## 七、常见比较与易混点

- **状态布居 vs 能级布居**：前者看单一量子态，后者必须乘简并度 $g_i$
- **熵大 vs 能量低**：熵反映可实现方式多，不能简单理解为“体系更低能”
- **配分函数大 vs 分子更稳定**：$q$ 大说明热可及状态多，不是单纯“稳定性更强”
- **Boltzmann 因子 vs 配分函数**：前者给单态权重，后者是所有态权重总和

## 八、与其他知识点的联系

- 与[[化学热力学]]、[[熵]]直接相连，是熵统计定义的来源
- 与[[化学势与平衡]]相连，可进一步通向平衡常数和辅助函数表达式
- 与[[Arrhenius方程]]相连，后者中的指数因子可视作高能粒子比例的动力学影子
- 与分子光谱、转动振动能级和配分函数近似计算有天然联系

## 九、典型题型

1. **相对布居题**：比较两个能级或两组状态的布居数比
2. **简并度修正题**：判断为什么高能级总布居可能反而更大
3. **配分函数估算题**：在给定温度下判断转动/振动自由度是否显著贡献
4. **熵统计解释题**：由 $W$ 的变化方向解释熵增减趋势

## 十、例题



### 例题 1：计算转动能级的相对布居（Atkins 例题 13A.1）

**题目**：计算 $25^{\circ}\mathrm{C}$ 时，HCl 两个转动能级（$J = 1$ 和 $J = 0$）的相对布居数。已知对于 HCl，$\tilde{B} = 10.591 \, \mathrm{cm^{-1}}$。

**分析**：
- 基态 $J = 0$ 是非简并的（$g_0 = 1$）
- $J = 1$ 的能级是三重简并的（$M_J = 0, \pm 1$，$g_1 = 3$）
- 转动能级公式：$\varepsilon_J = hc\tilde{B}J(J+1)$
- 有用的关系式：在 $298.15 \, \mathrm{K}$ 时，$kT/hc = 207.22 \, \mathrm{cm^{-1}}$

**解答**：

$J = 1$ 与 $J = 0$ 的能量间隔为：

$$\varepsilon_1 - \varepsilon_0 = 2hc\tilde{B}$$

$J = 1$ 的单个状态与 $J = 0$ 的布居比为：

$$\frac{N_{1,M_J}}{N_0} = e^{-2hc\tilde{B}\beta}$$

考虑 $J = 1$ 的三重简并度，两个能级的相对布居为：

$$\frac{N_1}{N_0} = 3e^{-2hc\tilde{B}\beta}$$

代入数据：

$$\frac{hc\tilde{B}}{kT} = \frac{10.591 \, \mathrm{cm^{-1}}}{207.22 \, \mathrm{cm^{-1}}} = 0.0511$$

$$\frac{N_1}{N_0} = 3e^{-2 \times 0.0511} = 3e^{-0.1022} = 3 \times 0.903 = 2.708$$

**反思**：
- 尽管 $J = 1$ 的能量更高，但由于其简并度为 3，总布居反而高于基态
- 这说明了区分"状态布居"和"能级布居"的重要性
- 在计算光谱线强度时，必须考虑这种简并度效应

### 例题 2：计算振动配分函数（Atkins 例题 13B.2）

**题目**：已知 $\mathrm{H_2O}$ 分子的 3 个简正模式的波数分别为 $3656.7 \, \mathrm{cm^{-1}}$、$1594.8 \, \mathrm{cm^{-1}}$ 和 $3755.8 \, \mathrm{cm^{-1}}$，计算 $1500 \, \mathrm{K}$ 时 $\mathrm{H_2O}$ 分子的振动配分函数。

**分析**：
- 每个简正模式可视为独立的谐振子
- 各模式的振动配分函数：$q^{\mathrm{V}} = 1/(1 - e^{-\beta hc\tilde{\nu}})$
- 总振动配分函数为各模式配分函数的乘积
- $1500 \, \mathrm{K}$ 时，$kT/hc = 1042.6 \, \mathrm{cm^{-1}}$

**解答**：

| 模式 | $\tilde{\nu} / \mathrm{cm^{-1}}$ | $hc\tilde{\nu}/kT$ | $q^{\mathrm{V}}$ |
|-----|-------------------------------|-------------------|----------------|
| 1 | 3656.7 | 3.507 | 1.031 |
| 2 | 1594.8 | 1.530 | 1.276 |
| 3 | 3755.8 | 3.602 | 1.028 |

总振动配分函数：

$$q^{\mathrm{V}} = 1.031 \times 1.276 \times 1.028 = 1.352$$

**反思**：
- 即使在 $1500 \, \mathrm{K}$ 的高温下，$\mathrm{H_2O}$ 的振动配分函数仍然接近 1
- 这说明大多数分子仍处在振动基态
- 对于大分子，虽然每个模式的贡献不大，但模式数多（$3N-6$），总贡献可能很可观

## 十一、易错点

- 忘记把简并度 $g_i$ 乘进去，只按 $e^{-\varepsilon_i/kT}$ 比布居
- 把“能量最高的态最少”误解成“高温时几乎没人占据高能态”
- 把配分函数当作“概率”，而不是归一化前的总权重
- 室温下对振动模式乱用高温近似，导致估计严重失真

## 十二、🎯 教学视角


### 9.1 学习路径

```
构型与权重 → Stirling近似 → Lagrange乘子法 → Boltzmann分布
    ↓
配分函数定义 → 分解性质 → 各运动模式配分函数
    ↓
平均能量公式 → 各模式能量贡献 → 能量均分原理
    ↓
内能表达式 → 熵（定域子/离域子） → 辅助函数 → 平衡常数
```

### 9.2 认知误区

1. **混淆状态与能级**：Boltzmann 分布给出的是状态布居，计算能级布居时必须乘上简并度 $g_i$。
2. **$T \to \infty$ 时的布居**：当 $T \to \infty$ 时，各状态的布居趋于**相等**，而非全部跑到最高能态。
3. **零点能的遗漏**：振动能量计算中，若以基态为能量零点，则实际能量需加上零点能 $\frac{1}{2}hc\tilde{\nu}$。
4. **定域子与离域子熵的区别**：气体分子不可分辨，熵公式中需包含 $qe/N$ 而非 $q$；晶体中分子可分辨，使用 $q$。
5. **高温近似的适用条件**：转动高温近似要求 $T \gg \theta^{\mathrm{R}}$，振动高温近似要求 $T \gg \theta^{\mathrm{V}}$。大多数分子在室温下振动不满足高温近似。

### 9.3 日常类比

- **配分函数 like 餐厅菜单**：$q$ 就像一家餐厅提供的可选菜品总数（热可及状态数）。温度越高（越有钱），你能点的菜越多（$q$ 越大）。
- **Boltzmann 分布 like 楼层人口**：一栋楼的低层（低能量）总是住着更多人，高层（高能量）人很少。温度就像"楼层间的吸引力"——温度越低，大家越挤在底层。
- **熵 like 房间混乱度**：$S = k \ln W$ 就像评估房间有多乱。东西摆放方式越多（$W$ 越大），房间越乱（$S$ 越大）。

## 十三、竞赛拓展

- 可继续连到正则系综、Helmholtz 自由能和统计热力学中的辅助函数
- 光谱线强度、转动布居峰和某些反应的温度敏感性，都能从布居分布得到直观解释
- 更高阶可继续区分 Maxwell-Boltzmann、Fermi-Dirac 与 Bose-Einstein 三类统计
- 在材料和固体问题中，能带占据与电子统计会把这套思想继续推广

## 十四、外部资料出处

- 可结合 Atkins 关于 Boltzmann distribution、partition function、entropy and ensembles 的章节阅读
- 与本库条目的直接关联：[[化学热力学]]、[[熵]]、[[化学势与平衡]]

## 十五、待完善项

- [ ] 后续补一张“布居分布 → 配分函数 → 热力学量”流程图

## 一、Boltzmann 熵公式

$$S = k_B \ln W$$

- $k_B = 1.38 \times 10^{-23} \, \mathrm{J \cdot K^{-1}}$（Boltzmann 常数）
- $W$：微观状态数（热力学概率）
- 解释了熵的统计本质：无序度的量度
- 当 $T \to 0$ 时，$W = 1$，故 $S \to 0$，与热力学第三定律一致

## 二、Boltzmann 最概然分布

$$\frac{N_i}{N} = \frac{g_i \, e^{-\varepsilon_i / kT}}{\sum_j g_j \, e^{-\varepsilon_j / kT}} = \frac{g_i \, e^{-\varepsilon_i / kT}}{q}$$

- $N_i$：能级 $i$ 上的粒子数；$g_i$：简并度
- $q$：分子配分函数（partition function）
- 基态粒子最多，随能级升高指数衰减

## 三、构型与权重（13A 严格推导）

### 3.1 瞬态构型

任一分子可出现在能量为 $\varepsilon_0, \varepsilon_1, \cdots$ 的状态下。在任一瞬间，能量为 $\varepsilon_0$ 的状态上有 $N_0$ 个分子，能量为 $\varepsilon_1$ 的状态上有 $N_1$ 个分子，以此类推；$N_0 + N_1 + \cdots = N$。这种分布 $\{N_0, N_1, \cdots\}$ 称为系统的**瞬态构型**（configuration）。

### 3.2 构型的权重

实现一个构型 $\{N_0, N_1, N_2, \cdots\}$ 的方式数称为构型的**权重**（weight），用符号 $W$ 表示：

$$W = \frac{N!}{N_0! \, N_1! \, N_2! \cdots}$$

当 $N$ 很大时，使用 Stirling 近似：

$$\ln N! \approx N \ln N - N \quad [N \gg 1]$$

则：

$$\ln W = N \ln N - \sum_i N_i \ln N_i$$

### 3.3 最概然分布的推导

在以下两个限制条件下求 $W$ 的最大值：

- **能量限制**：$\sum_i N_i \varepsilon_i = E$
- **数目限制**：$\sum_i N_i = N$

采用 Lagrange 乘子法，引入常数 $\alpha$ 和 $-\beta$，可得 $W$ 取最大值的条件：

$$\frac{\partial \ln W}{\partial N_i} + \alpha - \beta \varepsilon_i = 0$$

代入 $\ln W$ 的表达式并求导，最终得到 **Boltzmann 分布**：

$$\frac{N_i}{N} = \frac{e^{-\beta \varepsilon_i}}{q}$$

其中配分函数：

$$q = \sum_i e^{-\beta \varepsilon_i}$$

### 3.4 温度的统计本质

通过用 Boltzmann 分布导出完美气体状态方程（$pV = nRT$），可正式确认：

$$\beta = \frac{1}{kT}$$

**核心结论**：对于一个处于热平衡的系统，温度是控制状态最概然布局的唯一参数。

### 3.5 状态的相对布局

两个状态的相对布居：

$$\frac{N_i}{N_j} = \frac{g_i}{g_j} e^{-\beta(\varepsilon_i - \varepsilon_j)}$$

- 对于给定的能量间隔，布居数之比随 $\beta$ 增加（即温度下降）而减少
- 当 $T = 0$（$\beta = \infty$）时，所有布居都在基态
- 当 $T \to \infty$（$\beta \to 0$）时，各状态布居趋于相等

> **注意**：Boltzmann 分布给出的是**状态**而非**能级**的相对布局。计算能级布局时必须考虑简并度 $g_i$。

## 四、分子配分函数（13B）

### 4.1 配分函数的物理意义

$$q = \sum_{\text{状态 } i} e^{-\beta \varepsilon_i} = \sum_{\text{能级 } i} g_i \, e^{-\beta \varepsilon_i}$$

配分函数表示在所研究的温度时，一个分子拥有的**热可及状态数目**。

- $T \to 0$ 时：$q \to g_0$（基态简并度）
- $T \to \infty$ 时：$q \to \infty$（无限多状态变得可及）

### 4.2 配分函数的分解

一个孤立分子的能量是各种运动方式贡献的加和：

$$\varepsilon_i = \varepsilon_i^{\mathrm{T}} + \varepsilon_i^{\mathrm{R}} + \varepsilon_i^{\mathrm{V}} + \varepsilon_i^{\mathrm{E}}$$

由于指数函数的乘法性质，配分函数可拆分为各种贡献的**乘积**：

$$q = q^{\mathrm{T}} \cdot q^{\mathrm{R}} \cdot q^{\mathrm{V}} \cdot q^{\mathrm{E}}$$

### 4.3 平动配分函数

对于在体积 $V$ 的三维容器中自由运动的分子：

$$q^{\mathrm{T}} = \frac{V}{\Lambda^3}, \quad \Lambda = \frac{h}{(2\pi m kT)^{1/2}}$$

其中 $\Lambda$ 称为**热波长**（thermal wavelength）。室温下，对于 $100 \, \mathrm{cm^3}$ 容器中的 $\mathrm{O_2}$ 分子，$q^{\mathrm{T}} \approx 2 \times 10^{28}$，说明大量平动状态是热可及的。

### 4.4 转动配分函数

**线形分子**（高温近似 $T \gg \theta^{\mathrm{R}}$）：

$$q^{\mathrm{R}} = \frac{kT}{\sigma hc\tilde{B}} = \frac{T}{\sigma \theta^{\mathrm{R}}}$$

- $\sigma$：对称数（异核双原子分子 $\sigma = 1$；同核双原子分子或对称线形分子 $\sigma = 2$）
- $\theta^{\mathrm{R}} = hc\tilde{B}/k$：转动特征温度

**非线形分子**（高温近似）：

$$q^{\mathrm{R}} = \frac{1}{\sigma} \left(\frac{kT}{hc}\right)^{3/2} \left(\frac{\pi}{\tilde{A}\tilde{B}\tilde{C}}\right)^{1/2}$$

### 4.5 振动配分函数

谐振子近似下：

$$q^{\mathrm{V}} = \frac{1}{1 - e^{-\beta hc\tilde{\nu}}}$$

- $\theta^{\mathrm{V}} = hc\tilde{\nu}/k$：振动特征温度
- 高温近似（$T \gg \theta^{\mathrm{V}}$）：$q^{\mathrm{V}} \approx kT/hc\tilde{\nu}$
- 大多数分子在室温下 $q^{\mathrm{V}} \approx 1$（振动基本不激发）

多原子分子中，每个简正模式拥有其自身的配分函数，总振动配分函数是各模式配分函数的乘积。

### 4.6 电子配分函数

电子激发态与基态的能量间隔通常很大，故大多数情况下：

$$q^{\mathrm{E}} = g^{\mathrm{E}}$$

其中 $g^{\mathrm{E}}$ 为电子基态的简并度（通常为 1，碱金属原子为 2）。

## 五、分子能量（13C）

### 5.1 基本公式

一个分子的平均能量可由配分函数计算：

$$\langle \varepsilon \rangle = \varepsilon_{\mathrm{gs}} - \frac{1}{q}\left(\frac{\partial q}{\partial \beta}\right)_V = \varepsilon_{\mathrm{gs}} - \left(\frac{\partial \ln q}{\partial \beta}\right)_V$$

其中 $\varepsilon_{\mathrm{gs}}$ 为基态能量（若以基态为能量零点，则 $\varepsilon_{\mathrm{gs}} = 0$）。

### 5.2 各种运动模式的贡献

**平动**：

$$\langle \varepsilon^{\mathrm{T}} \rangle = \frac{3}{2} kT$$

**转动**（线形分子，$T \gg \theta^{\mathrm{R}}$）：

$$\langle \varepsilon^{\mathrm{R}} \rangle = kT$$

非线形分子：$\langle \varepsilon^{\mathrm{R}} \rangle = \frac{3}{2} kT$

**振动**（谐振子近似）：

$$\langle \varepsilon^{\mathrm{V}} \rangle = \frac{hc\tilde{\nu}}{e^{\beta hc\tilde{\nu}} - 1}$$

高温近似（$T \gg \theta^{\mathrm{V}}$）：$\langle \varepsilon^{\mathrm{V}} \rangle \approx kT$

**电子**：

$$\langle \varepsilon^{\mathrm{E}} \rangle = 0$$

（大多数情况仅基态被占据）

### 5.3 能量均分原理与量子效应

在高温极限下，各运动模式对能量的贡献与经典**能量均分原理**一致：每个平方项贡献 $\frac{1}{2}kT$。

| 运动模式 | 活泼模式数 | 高温能量贡献 | 室温是否活泼 |
|---------|-----------|-------------|-------------|
| 平动 | 3 | $\frac{3}{2}kT$ | 是 |
| 转动（线形） | 2 | $kT$ | 是 |
| 转动（非线形） | 3 | $\frac{3}{2}kT$ | 是 |
| 振动 | $3N-6$（或 $3N-5$）| $kT$（每个模式）| 通常否 |

**零点能**：谐振子基态能量为 $\frac{1}{2}hc\tilde{\nu}$，这是量子力学效应，经典物理中不存在。在计算实际能量时，需要将零点能加入。

## 六、正则系综（13D，拓展）

### 6.1 系综的概念

**系综**是想象的、具有相同温度的大量实际系统复制品的集合。三种重要系综：

| 系综 | 相同性质 |
|-----|---------|
| 微正则系综 | $V, E, N$ |
| 正则系综 | $V, T, N$ |
| 巨正则系综 | $V, T, \mu$ |

### 6.2 正则配分函数

正则系综中，成员出现在能量为 $E_i$ 的状态上的概率：

$$\tilde{p}_i = \frac{e^{-\beta E_i}}{Q}, \quad Q = \sum_i e^{-\beta E_i}$$

其中 $Q$ 称为**正则配分函数**（canonical partition function），含有系统所有的热力学信息，且允许分子之间有相互作用。

### 6.3 $Q$ 与 $q$ 的关系

- 可分辨的独立分子（如晶格中的粒子）：$Q = q^N$
- 不可分辨的独立分子（如气体）：$Q = q^N / N!$

## 七、内能和熵（13E）

### 7.1 内能

由 $N$ 个独立分子组成的系统：

$$U(T) = U(0) - \frac{N}{q}\left(\frac{\partial q}{\partial \beta}\right)_V = U(0) - N\left(\frac{\partial \ln q}{\partial \beta}\right)_V$$

或转化为对温度的偏导：

$$U(T) - U(0) = NkT^2 \left(\frac{\partial \ln q}{\partial T}\right)_V$$

对于相依分子系统，用 $Q$ 代替 $q$：

$$U(T) = U(0) - \left(\frac{\partial \ln Q}{\partial \beta}\right)_V$$

### 7.2 热容

定容热容：

$$C_V = Nk\beta^2 \left(\frac{\partial^2 \ln q}{\partial \beta^2}\right)_V$$

高温极限下（均分原理适用）：

$$C_{V,\mathrm{m}} = \frac{1}{2}(3 + v^{\mathrm{R}*} + 2v^{\mathrm{V}*})R$$

其中 $v^{\mathrm{R}*}$ 和 $v^{\mathrm{V}*}$ 分别为活泼的转动和振动模式数。

### 7.3 熵

**Boltzmann 公式**：

$$S = k \ln W$$

其中 $W$ 为最概然构型的权重。$T \to 0$ 时 $W = 1$，$S \to 0$，符合热力学第三定律。

**用配分函数表示熵**：

- **定域子**（可分辨分子，如晶体）：

$$S = \frac{U(T) - U(0)}{T} + Nk \ln q$$

- **离域子**（不可分辨分子，如气体）：

$$S = \frac{U(T) - U(0)}{T} + Nk \ln \frac{qe}{N}$$

- **相依分子**：

$$S = \frac{U(T) - U(0)}{T} + k \ln Q$$

### 7.4 Sackur-Tetrode 公式

单原子完美气体的摩尔熵：

$$S_{\mathrm{m}} = R \ln \frac{V_{\mathrm{m}} e^{5/2}}{N_A \Lambda^3}$$

标准摩尔熵：

$$S_{\mathrm{m}}^{\ominus} = R \ln \frac{kT e^{5/2}}{p^{\ominus} \Lambda^3}$$

### 7.5 残余熵

即使在 $T = 0$ 时，固体中仍可能存在一定的无序，导致熵大于零，称为**残余熵**（residual entropy）。

对于在 $T = 0$ 时可采取 $s$ 种等价取向的分子：

$$S_{\mathrm{m}}(0) = R \ln s$$

例如，CO 的残余熵约为 $R \ln 2 \approx 5.8 \, \mathrm{J \cdot K^{-1} \cdot mol^{-1}}$，冰的残余熵约为 $R \ln(3/2) \approx 3.4 \, \mathrm{J \cdot K^{-1} \cdot mol^{-1}}$。

## 八、辅助函数与平衡常数（13F，拓展）

### 8.1 Helmholtz 能

$$A(T) = A(0) - kT \ln Q$$

对于独立分子组成的气体（$Q = q^N/N!$）：

$$A(T) = A(0) - NkT \ln q + kT \ln N!$$

### 8.2 Gibbs 能

$$G(T) = G(0) - kT \ln Q + kTV\left(\frac{\partial \ln Q}{\partial V}\right)_T$$

对于气体（$pV = nRT$）：

$$G(T) = G(0) - nRT \ln \frac{q}{N}$$

### 8.3 用配分函数计算平衡常数

对于气相反应 $a\mathrm{A} + b\mathrm{B} \longrightarrow c\mathrm{C} + d\mathrm{D}$：

$$K = \left[\prod_j \left(\frac{q_{j,\mathrm{m}}^{\ominus}}{N_A}\right)^{\nu_j}\right] e^{-\Delta_{\mathrm{r}}E_0 / RT}$$

其中 $\Delta_{\mathrm{r}}E_0$ 是反应物与产物的摩尔基态能量之差，可由键的解离能计算。

**物理图像**：平衡常数的大小反映了能量间隔和状态密度之间的竞争。即使产物的基态能量较高，如果其拥有很高的状态密度（即很大的配分函数），产物仍可能在平衡时占据多数。这正是熵驱动反应的本质。

## 十一、核心公式速查

| 性质 | 公式 | 说明 |
|-----|------|------|
| Boltzmann 分布 | $\dfrac{N_i}{N} = \dfrac{e^{-\beta \varepsilon_i}}{q}$ | $\beta = 1/kT$ |
| 配分函数 | $q = \sum_i e^{-\beta \varepsilon_i}$ | 对状态加和 |
| 平动配分函数 | $q^{\mathrm{T}} = V/\Lambda^3$ | $\Lambda = h/(2\pi mkT)^{1/2}$ |
| 转动配分函数（线形） | $q^{\mathrm{R}} = kT/\sigma hc\tilde{B}$ | $T \gg \theta^{\mathrm{R}}$ |
| 振动配分函数 | $q^{\mathrm{V}} = 1/(1 - e^{-\beta hc\tilde{\nu}})$ | 谐振子近似 |
| 平均能量 | $\langle \varepsilon \rangle = -(\partial \ln q/\partial \beta)_V$ | 以基态为零点 |
| 内能 | $U(T) - U(0) = NkT^2 (\partial \ln q/\partial T)_V$ | 独立分子 |
| 熵（定域子） | $S = [U(T)-U(0)]/T + Nk \ln q$ | 可分辨分子 |
| 熵（离域子） | $S = [U(T)-U(0)]/T + Nk \ln(qe/N)$ | 气体 |
| Helmholtz 能 | $A(T) = A(0) - kT \ln Q$ | 普遍适用 |
| 平衡常数 | $K = \prod_j (q_{j,\mathrm{m}}^{\ominus}/N_A)^{\nu_j} e^{-\Delta_{\mathrm{r}}E_0/RT}$ | 气相反应 |

## 关联题库

```dataview
TABLE file.name AS "文件名", year AS "年份", type AS "题型", difficulty AS "难度"
FROM "04-题库"
WHERE contains(knowledge_points, "Boltzmann统计初步")
SORT year DESC, difficulty ASC
```
