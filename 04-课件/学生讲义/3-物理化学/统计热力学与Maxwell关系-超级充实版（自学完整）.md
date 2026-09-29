---
title: 学生讲义-统计热力学与Maxwell关系（超级充实版·自学完整）
type: 学生讲义
template_version: 自学完整版 v2.0
version: v2.0
source_book: "物理化学（第六版下册）-傅献彩等 Ch03, Ch07; Atkins《物理化学》第11版 Ch03, Ch13; 全国决赛真题"
chapter: 第四轮·4-7（物化线）
serve_rounds: [第四轮, 冲刺轮]
serve_topics: [热力学四大基本方程, Legendre变换, Maxwell关系, Born方阵, 热力学状态方程, 内压力, 普适热容差公式, Joule-Thomson系数, 节流转化温度, Gibbs-Helmholtz方程, van't Hoff方程, Nernst热定理, 热力学第三定律, Boltzmann分布微观推导, 最概然分布, Lagrange乘子法, 分子配分函数母机, 各模式解耦, 热波长, 对称数, 量子谐振子, 定域与离域系综, 全同粒子不可区分性, Gibbs悖论, Sackur-Tetrode方程, 残余熵, Pauling冰熵理论, Debye低温T3定律, 统计平衡常数]
difficulty_level: 基础~进阶~挑战（决赛级）
exercise_count: 11
exercise_levels:
  - "平铺连续编号 1~25 题（涵盖四大基本方程微观微商、Maxwell关系推导、理想与范德华状态方程验算、热容差与节流反转推导、Gibbs-Helmholtz变温平衡计算、Nernst极限证明、三能级构型数、Boltzmann能级分配、热波长判据、转动对称数、振动配分与零点能、微观导出理想状态方程、离域熵差与Gibbs悖论、Sackur-Tetrode绝对熵计算、CO与N2O残余熵、Pauling冰残余熵几何推导、Debye声子比热积分、同位素交换常数、Saha电离方程、碘热解离平衡、高压气体维里修正综合建模）"
has_images: true
image_count: 6
syllabus_codes: ["基础-06", "决赛-04"]
prep_notes: ["[[2026-06-02-热力学初步-基础班]]", "[[2026-06-06-热力学与平衡深化-提高班]]"]
sources:
  - "[[mineru/03-教材书籍/物理化学/物理化学/物理化学（第11版）第13章 统计热力学544-585]]"
  - "[[mineru/03-教材书籍/物理化学（第六版）傅献彩/Ch03B-热力学第二定律-Maxwell关系与规定熵]]"
  - "[[mineru/03-教材书籍/物理化学（第六版）傅献彩/Ch07-统计热力学基础]]"
tags: [学生讲义, 超级充实版, 物理化学, 第四轮, 统计热力学, Maxwell关系, 自学完整]
created: 2026-08-04
updated: 2026-09-29
last_audit: "2026-09-29 口径升级：去 H1；「学习目标」改为「学习目标与考纲锚点」并补齐六行三线表；正文节号统一 §1~§9（§9 经典示范例题）；练习区改为 §10 竞赛思考强化题与微观机理精解，题量按实际可用题源收编为 11 题（Ch05 熵的状态函数性与微观状态数判据 3 题 ＋ Ch06 ΔG—K 互算与 Gibbs-Helmholtz 相变类 8 题），不另补自编题；配图逐张目检均为教材原书图；四闸门机检闭环；2026-09-29 口径 v4（教师版＝学生版＋答案）：删「学习目标与考纲锚点」节（考纲码保留于 FM syllabus_codes），练习区统一改「§N 课后习题」并删导语，删花活栏目（知识网络与方法论／本节总结速查／赛场高频失分命题陷阱清单／命题陷阱与失分误区清单／失分陷阱子节）并重编节号，去 AI 修辞与来源署名，图注保留编号只留一句事实，并列项与小标题行前补空行（修 docx 并段）"
stage: published
related:
  - "[[03-知识点/决赛要求/物理化学深化/麦克斯韦关系式]]"
  - "[[03-知识点/决赛要求/物理化学深化/Boltzmann统计初步]]"
  - "[[03-知识点/决赛要求/物理化学深化/热力学四大基本方程]]"
  - "[[03-知识点/决赛要求/物理化学深化/吉布斯-亥姆霍兹方程]]"
  - "[[04-课件/学生讲义/3-物理化学/物化综合计算-超级充实版（自学完整）]]"
  - "[[04-课件/学生讲义/3-物理化学/胶体与表面物理化学-超级充实版（自学完整）]]"
status: 已填充
---

## §1 热力学四大基本方程与 Legendre 变换

在经典热力学体系中，热力学第一定律与第二定律的可逆过程综合式是全部状态函数演绎的起点。对于仅做体积功的封闭均匀单相体系，第一定律微分式为 $dU = \delta q_\mathrm{rev} + \delta w_\mathrm{rev}$。根据 Clausius 熵定义，可逆过程吸收热量为 $\delta q_\mathrm{rev} = T\,dS$；可逆体积功为 $\delta w_\mathrm{rev} = -p\,dV$。将二者代入第一定律，即得到热力学第一基本方程：

$$dU = T\,dS - p\,dV$$

从微观统计物理的视角审视，内能方程具有精微的物理诠释。宏观体系的内能是所有微观能级平均能量的总和，即 $U = \sum_i N_i \varepsilon_i$。对其取全微分可得 $dU = \sum_i \varepsilon_i\,dN_i + \sum_i N_i\,d\varepsilon_i$。对比热力学基本方程，第一项 $\sum_i \varepsilon_i\,dN_i$ 对应体系微观能级粒子占据数分布的变化，粒子在固定能级间的跃迁直接宏观表现为热交换 $T\,dS$；第二项 $\sum_i N_i\,d\varepsilon_i$ 对应于外部体积改变引发的量子势阱尺寸变化，进而引起单粒子能级本征值的升降，能级位移在宏观上直接表现为体积功 $-p\,dV$。

由此式可知，内能 $U$ 的特征变量（即自然变量）为熵 $S$ 与体积 $V$。只要获知了内能关于自然变量的函数关系 $U = U(S, V)$，通过一次偏导数运算即可求出体系的压强 $p = -(\partial U/\partial V)_S$ 与绝对温度 $T = (\partial U/\partial S)_V$，进而求得体系的全部平衡热力学性质。然而在实验室真实测量中，熵 $S$ 无法由仪表直接读取或精确控制，体积 $V$ 在高压或凝聚态实验中同样难以维持严格等容。化学家迫切需要以易于测量的强大量（如温度 $T$、压强 $p$）作为独立自变量的热力学函数。

将多变量函数中的某个独立变量替换为其共轭变量、同时完整保留原函数全部信息的数学方法称为 Legendre 变换。设函数 $y = f(x_1, x_2)$，其全微分为 $dy = u_1\,dx_1 + u_2\,dx_2$，其中共轭变量定义为偏导数 $u_1 = (\partial f/\partial x_1)_{x_2}$。若欲将自变量 $x_1$ 变换为 $u_1$，定义新函数 $g(u_1, x_2) = y - u_1 x_1$。对新函数求全微分可得：

$$dg = dy - u_1\,dx_1 - x_1\,du_1 = (u_1\,dx_1 + u_2\,dx_2) - u_1\,dx_1 - x_1\,du_1 = -x_1\,du_1 + u_2\,dx_2$$

新函数 $g$ 的自然变量自然转变为 $(u_1, x_2)$。将这一精巧的数学变换应用于内能母方程，即可系统生成其余三大热力学特征函数：

第一，欲将自然变量中的体积 $V$ 替换为共轭量压强 $p$。由于 $(\partial U/\partial V)_S = -p$，其共轭乘积为 $(-p)V$。根据 Legendre 变换构造新函数 $H = U - (-p)V = U + pV$，该函数定义为焓（Enthalpy）。对焓求全微分：

$$dH = dU + p\,dV + V\,dp = (T\,dS - p\,dV) + p\,dV + V\,dp = T\,dS + V\,dp$$

焓 $H$ 的自然变量为 $(S, p)$。由全微分直接可得温度 $T = (\partial H/\partial S)_p$ 与体积 $V = (\partial H/\partial p)_S$。在等压可逆过程中，$dp = 0$，体系吸收的热量直接表现为焓的增量，即 $dH = \delta q_p$。

第二，欲将自然变量中的熵 $S$ 替换为共轭量绝对温度 $T$。由于 $(\partial U/\partial S)_V = T$，其共轭乘积为 $TS$。构造新函数 $A = U - TS$，该函数定义为 Helmholtz 自由能（亦称等温等容位）。对 $A$ 求全微分：

$$dA = dU - T\,dS - S\,dT = (T\,dS - p\,dV) - T\,dS - S\,dT = -S\,dT - p\,dV$$

Helmholtz 自由能 $A$ 的自然变量为 $(T, V)$。由全微分直接可得熵 $S = -(\partial A/\partial T)_V$ 与压强 $p = -(\partial A/\partial V)_T$。在等温等容可逆过程中，体系所能输出的最大功等于 Helmholtz 自由能的减少量，即 $-dA = \delta w_\mathrm{max}$。

第三，若同时将自变量 $(S, V)$ 分别变换为 $(T, p)$，则构造新函数 $G = U - TS - (-p)V = H - TS = A + pV$，该函数定义为 Gibbs 自由能（亦称等温等压位）。对 $G$ 求全微分：

$$dG = dH - T\,dS - S\,dT = (T\,dS + V\,dp) - T\,dS - S\,dT = -S\,dT + V\,dp$$

Gibbs 自由能 $G$ 的自然变量为 $(T, p)$。由全微分直接可得熵 $S = -(\partial G/\partial T)_p$ 与体积 $V = (\partial G/\partial p)_T$。由于绝大多数化学反应都在敞口容器（恒定大气压）及恒温水浴中进行，自变量恰好为 $(T, p)$ 的 Gibbs 自由能成为了化学热力学判据与化学平衡计算中应用最广泛的核心函数。在等温等压可逆过程中，体系对外所能输出的最大非体积功（有效功）等于 Gibbs 自由能的减少量，即 $-\Delta G = w'_\mathrm{max}$。

为便于记忆四大基本方程的微分结构及其偏导数，Born（波恩）与 Koenig 提出了热力学方阵图谱。

![[5a259a1a2556c1039502504d17ef6c4b671b5e842a75bff80ad1532cec23af54.jpg]]
> 图 10-1：热力学特征函数方阵与自然变量对应关系

由 Born 方阵读出基本方程的具体法则如下：方阵四条边中央分别安放四大特征函数 $U, H, G, A$；方阵的四个顶角分别安放四个自然变量 $V, T, p, S$。每个函数的自然变量即为其两肩所紧邻的两个顶角变量。例如，$U$ 位于 $S$ 与 $V$ 之间，故 $U = U(S, V)$；$G$ 位于 $T$ 与 $p$ 之间，故 $G = G(T, p)$。微分系数由对角线两端的共轭变量确定：从顶角出发沿箭头方向指向对角顶角时取正号，反箭头方向时取负号。例如对 $dG$，其自然自变量为 $dT$ 与 $dp$；$T$ 的对角顶角为 $S$（沿反向箭头，取 $-S$），$p$ 的对角顶角为 $V$（沿同向箭头，取 $+V$），立即得到 $dG = -S\,dT + V\,dp$。

---

## §2 Maxwell 关系式与偏导数变换艺术

热力学状态函数的一大基本数学属性是其微分均为全微分。根据高等微积分中的 Schwarz 定理，若多元函数具有连续的二阶偏导数，则该函数对两个不同自变量的二阶混合偏导数与求导的先后顺序无关，即：

$$\frac{\partial^2 z}{\partial x\,\partial y} = \frac{\partial^2 z}{\partial y\,\partial x}$$

将该定理严格应用于四大热力学基本方程，即催生了热力学中深刻且威力强大的四大 Maxwell 关系式。

第一式：考察内能母方程 $dU = T\,dS - p\,dV$。由于 $dU$ 是全微分，有 $(\partial U/\partial S)_V = T$ 以及 $(\partial U/\partial V)_S = -p$。内能对 $S$ 和 $V$ 的二阶混合偏导数必须相等：

$$\frac{\partial}{\partial V}\left[\left(\frac{\partial U}{\partial S}\right)_V\right]_S = \frac{\partial}{\partial S}\left[\left(\frac{\partial U}{\partial V}\right)_S\right]_V \implies \left(\frac{\partial T}{\partial V}\right)_S = -\left(\frac{\partial p}{\partial S}\right)_V$$

第二式：考察焓的基本方程 $dH = T\,dS + V\,dp$。由 $(\partial H/\partial S)_p = T$ 以及 $(\partial H/\partial p)_S = V$，利用焓对 $S$ 和 $p$ 的二阶混合偏导数相等：

$$\frac{\partial}{\partial p}\left[\left(\frac{\partial H}{\partial S}\right)_p\right]_S = \frac{\partial}{\partial S}\left[\left(\frac{\partial H}{\partial p}\right)_S\right]_p \implies \left(\frac{\partial T}{\partial p}\right)_S = \left(\frac{\partial V}{\partial S}\right)_p$$

第三式：考察 Helmholtz 自由能方程 $dA = -S\,dT - p\,dV$。由 $(\partial A/\partial T)_V = -S$ 以及 $(\partial A/\partial V)_T = -p$，利用 $A$ 对 $T$ 和 $V$ 的二阶混合偏导数相等：

$$\frac{\partial}{\partial V}\left[\left(\frac{\partial A}{\partial T}\right)_V\right]_T = \frac{\partial}{\partial T}\left[\left(\frac{\partial A}{\partial V}\right)_T\right]_V \implies -\left(\frac{\partial S}{\partial V}\right)_T = -\left(\frac{\partial p}{\partial T}\right)_V \implies \left(\frac{\partial S}{\partial V}\right)_T = \left(\frac{\partial p}{\partial T}\right)_V$$

第四式：考察 Gibbs 自由能方程 $dG = -S\,dT + V\,dp$。由 $(\partial G/\partial T)_p = -S$ 以及 $(\partial G/\partial p)_T = V$，利用 $G$ 对 $T$ 和 $p$ 的二阶混合偏导数相等：

$$\frac{\partial}{\partial p}\left[\left(\frac{\partial G}{\partial T}\right)_p\right]_T = \frac{\partial}{\partial T}\left[\left(\frac{\partial G}{\partial p}\right)_T\right]_p \implies -\left(\frac{\partial S}{\partial p}\right)_T = \left(\frac{\partial V}{\partial T}\right)_p \implies \left(\frac{\partial S}{\partial p}\right)_T = -\left(\frac{\partial V}{\partial T}\right)_p$$

在化学竞赛与热力学研究中，第三式和第四式的使用频率远高于前两式。其根本原因在于：体系的熵 $S$ 无法直接用温度计或压力表测定，因而形如 $(\partial S/\partial V)_T$ 与 $(\partial S/\partial p)_T$ 的偏导数属于不可直接测量的物理量；而 Maxwell 第三、第四关系式精巧地将不可测的熵偏导数，转化为可完全由体系 $p-V-T$ 状态方程直接求导得出的宏观物理量 $(\partial p/\partial T)_V$ 与 $(\partial V/\partial T)_p$。

在运用 Maxwell 关系进行复杂的偏导数化简时，经常需要配合多元微积分的偏导数循环法则（Euler 链式法则）。设体系存在状态方程 $F(x, y, z) = 0$，将 $x$ 视为 $y, z$ 的函数，取全微分 $dx = (\partial x/\partial y)_z\,dy + (\partial x/\partial z)_y\,dz$。当体系处于等 $x$ 约束过程（$dx = 0$）时，两端除以 $dy$ 并固定 $x$，可得：

$$\left(\frac{\partial x}{\partial y}\right)_z \left(\frac{\partial y}{\partial z}\right)_x \left(\frac{\partial z}{\partial x}\right)_y = -1$$

结合偏导数倒数关系 $(\partial x/\partial y)_z = [(\partial y/\partial x)_z]^{-1}$，循环法则常用于将难解的等容偏导数转化为容易求导的等压或等温偏导数。

利用 Maxwell 第三与第四关系式，能够严格推导出热力学第一与第二状态方程。热力学第一状态方程旨在考察内能随体积的等温变化率 $(\partial U/\partial V)_T$（在物理上称为体系的内压力 $\pi_T$）。从内能母方程 $dU = T\,dS - p\,dV$ 两端同除以 $dV$ 并在恒温 $T$ 条件下求导：

$$\left(\frac{\partial U}{\partial V}\right)_T = T\left(\frac{\partial S}{\partial V}\right)_T - p$$

将 Maxwell 第三关系式 $(\partial S/\partial V)_T = (\partial p/\partial T)_V$ 代入上式，立即获得普适的热力学第一状态方程：

$$\left(\frac{\partial U}{\partial V}\right)_T = T\left(\frac{\partial p}{\partial T}\right)_V - p$$

同理，考察焓随压强的等温变化率 $(\partial H/\partial p)_T$。从焓方程 $dH = T\,dS + V\,dp$ 出发，两端同除以 $dp$ 并在恒温 $T$ 下求导：

$$\left(\frac{\partial H}{\partial p}\right)_T = T\left(\frac{\partial S}{\partial p}\right)_T + V$$

代入 Maxwell 第四关系式 $(\partial S/\partial p)_T = -(\partial V/\partial T)_p$，即获得普适的热力学第二状态方程：

$$\left(\frac{\partial H}{\partial p}\right)_T = V - T\left(\frac{\partial V}{\partial T}\right)_p$$

对于摩尔状态方程为 $p V_\mathrm{m} = RT$ 的理想气体，有 $(\partial p/\partial T)_V = R/V_\mathrm{m}$ 以及 $(\partial V/\partial T)_p = R/p$。代入上述两个状态方程：

$$\left(\frac{\partial U_\mathrm{m}}{\partial V_\mathrm{m}}\right)_T = T\left(\frac{R}{V_\mathrm{m}}\right) - p = p - p = 0$$

$$\left(\frac{\partial H_\mathrm{m}}{\partial p}\right)_T = V_\mathrm{m} - T\left(\frac{R}{p}\right) = V_\mathrm{m} - V_\mathrm{m} = 0$$

这表明，对于理想气体，无论体积或压强如何改变，其内能与焓均保持恒定。这严格从热力学基本定律证明了 Joule 实验定律：理想气体的内能与焓纯粹只是温度的单变量函数，即 $U = U(T)$ 与 $H = H(T)$。

而对于遵循 van der Waals 状态方程的真实气体 $(p + a/V_\mathrm{m}^2)(V_\mathrm{m} - b) = RT$，将压强表示为 $p = \frac{RT}{V_\mathrm{m} - b} - \frac{a}{V_\mathrm{m}^2}$。对温度求偏导：$(\partial p/\partial T)_V = \frac{R}{V_\mathrm{m} - b}$。代入热力学第一状态方程：

$$\left(\frac{\partial U_\mathrm{m}}{\partial V_\mathrm{m}}\right)_T = T\left(\frac{R}{V_\mathrm{m} - b}\right) - \left(\frac{RT}{V_\mathrm{m} - b} - \frac{a}{V_\mathrm{m}^2}\right) = \frac{a}{V_\mathrm{m}^2}$$

这一结果优美地揭示了分子间引力的微观本质：项 $a/V_\mathrm{m}^2$ 正是克服分子间范德华吸引力所需的内压力。当气体等温膨胀（$dV_\mathrm{m} > 0$）时，分子间距增大，分子势能升高，导致体系内能相应增加。

---

## §3 宏观热力学响应函数与节流效应

在实验热物理中，直接测量状态函数对坐标的导数十分困难，实验物理学家定义了一系列易于精确测量的宏观热力学响应系数，用以表征物质对温度与压强扰动的力学及热学响应：

第一，等压体膨胀系数 $\alpha$（Thermal Expansion Coefficient）：表征在恒定压强下，温度每升高 1 开尔文引起体系相对体积的膨胀率，定义为：

$$\alpha = \frac{1}{V}\left(\frac{\partial V}{\partial T}\right)_p$$

第二，等温压缩率 $\kappa_T$（Isothermal Compressibility）：表征在恒定温度下，外压每增加 1 个单位引起体系相对体积的收缩率（因体积随压强增加而减小，式中冠以负号使其恒为正值），定义为：

$$\kappa_T = -\frac{1}{V}\left(\frac{\partial V}{\partial p}\right)_T$$

第三，等容压强系数 $\beta_V$（Isochoric Pressure Coefficient）：表征在恒定体积下，温度每升高 1 开尔文引起体系相对压强的增长率，定义为：

$$\beta_V = \frac{1}{p}\left(\frac{\partial p}{\partial T}\right)_V$$

应用偏导数循环法则，考察自变量组 $(p, V, T)$：

$$\left(\frac{\partial p}{\partial T}\right)_V \left(\frac{\partial T}{\partial V}\right)_p \left(\frac{\partial V}{\partial p}\right)_T = -1 \implies \left(\frac{\partial p}{\partial T}\right)_V = -\frac{(\partial V/\partial T)_p}{(\partial V/\partial p)_T} = -\frac{\alpha V}{-\kappa_T V} = \frac{\alpha}{\kappa_T}$$

由此可知，等容条件下压强随温度的变化率 $(\partial p/\partial T)_V$ 可完全由等压膨胀系数 $\alpha$ 与等温压缩率 $\kappa_T$ 之比直接算出。

在物理化学中，一个极具代表性的偏导推导典范是普适热容差公式 $C_p - C_V$ 的推导。定压热容 $C_p$ 与定容热容 $C_V$ 分别定义为恒压与恒容下体系焓和内能对温度的偏导数，即 $C_p = (\partial H/\partial T)_p = T(\partial S/\partial T)_p$，$C_V = (\partial U/\partial T)_V = T(\partial S/\partial T)_V$。为建立两者的内在联系，将体系的熵选定为以温度 $T$ 和体积 $V$ 为独立变量的函数 $S = S(T, V)$，展开其全微分：

$$dS = \left(\frac{\partial S}{\partial T}\right)_V dT + \left(\frac{\partial S}{\partial V}\right)_T dV = \frac{C_V}{T}\,dT + \left(\frac{\partial S}{\partial V}\right)_T dV$$

利用 Maxwell 第三关系式 $(\partial S/\partial V)_T = (\partial p/\partial T)_V$ 代换第二项：

$$dS = \frac{C_V}{T}\,dT + \left(\frac{\partial p}{\partial T}\right)_V dV$$

将体系置于恒定压强 $p$ 下，两端同除以 $dT$ 并在偏导数中注明恒压条件：

$$\left(\frac{\partial S}{\partial T}\right)_p = \frac{C_V}{T} + \left(\frac{\partial p}{\partial T}\right)_V \left(\frac{\partial V}{\partial T}\right)_p$$

两端同时乘以绝对温度 $T$，并将 $T(\partial S/\partial T)_p$ 替换为定压热容 $C_p$：

$$C_p = C_V + T\left(\frac{\partial p}{\partial T}\right)_V \left(\frac{\partial V}{\partial T}\right)_p \implies C_p - C_V = T\left(\frac{\partial p}{\partial T}\right)_V \left(\frac{\partial V}{\partial T}\right)_p$$

代入前面导出的响应函数关系式 $(\partial p/\partial T)_V = \alpha/\kappa_T$ 以及 $(\partial V/\partial T)_p = \alpha V$，即得著名的普适热容差公式：

$$C_p - C_V = \frac{\alpha^2 T V}{\kappa_T}$$

该公式具有深远的热力学哲学意义。根据热力学力学稳定性准则，外界对体系加压，其体积必趋于缩小（即 $-(\partial V/\partial p)_T > 0$），因此对于任何稳定存在的宏观均匀相物质，等温压缩率必严格大于零（$\kappa_T > 0$）。又因绝对温度 $T > 0$ 且体系体积 $V > 0$，项 $\alpha^2$ 为平方实数必非负，故恒有：

$$C_p \ge C_V$$

这表明在任何物理条件下，物质的定压热容绝不可能小于定容热容。当且仅当体膨胀系数 $\alpha = 0$ 时，两者严格相等（$C_p = C_V$）。纯液态水在标准大气压、温度为 3.98 ℃（约 277.13 K）时达到最大密度点，此时液态水的体积随温度的变化率 $(\partial V/\partial T)_p = 0$，因而膨胀系数 $\alpha = 0$。在此特定温度下，纯水的定压热容严格等于定容热容。对于理想气体，$\alpha = 1/T$，$\kappa_T = 1/p$，代入公式立即得到 $C_p - C_V = \frac{(1/T)^2 T V}{1/p} = \frac{pV}{T} = nR$，这正是众所周知的 Mayer 公式。

另一个展现偏导数变换威力的经典应用是工业气体液化与制冷领域的核心——Joule-Thomson 效应（节流过程）。高压气体经多孔塞或绝热缩径阀门连续流向低压区，整个过程满足绝热且对外无轴功输入。由于进气端环境对其做功为 $p_1 V_1$，出气端对环境做功为 $p_2 V_2$，由能量守恒定律知 $U_1 + p_1 V_1 = U_2 + p_2 V_2$，即 $H_1 = H_2$。因此，节流膨胀是一个严格的等焓过程（$dH = 0$）。

定义衡量节流过程中温度随压强变化灵敏度的物理量为 Joule-Thomson 系数 $\mu_{JT} = (\partial T/\partial p)_H$。应用偏导数循环法则：

$$\left(\frac{\partial T}{\partial p}\right)_H \left(\frac{\partial p}{\partial H}\right)_T \left(\frac{\partial H}{\partial T}\right)_p = -1 \implies \mu_{JT} = -\frac{(\partial H/\partial p)_T}{(\partial H/\partial T)_p} = -\frac{1}{C_p}\left(\frac{\partial H}{\partial p}\right)_T$$

将前述热力学第二状态方程 $(\partial H/\partial p)_T = V - T(\partial V/\partial T)_p$ 代入上式，并利用膨胀系数 $\alpha$ 展开：

$$\mu_{JT} = \frac{1}{C_p}\left[T\left(\frac{\partial V}{\partial T}\right)_p - V\right] = \frac{V}{C_p}(\alpha T - 1)$$

当 $\mu_{JT} > 0$ 时，节流降压（$dp < 0$）导致体系温度下降（$dT < 0$），表现为节流致冷效应；当 $\mu_{JT} < 0$ 时，节流降压反而导致气体升温，表现为节流致热效应。使致冷与致热发生反转的边界条件称为节流转化状态，其转化温度（Inversion Temperature $T_\mathrm{inv}$）由 $\mu_{JT} = 0$ 确定，即：

$$\alpha T_\mathrm{inv} = 1 \iff \left(\frac{\partial V}{\partial T}\right)_p = \frac{V}{T_\mathrm{inv}}$$

对于理想气体，由于 $\alpha = 1/T$，恒有 $\alpha T - 1 = 0$，故 $\mu_{JT} \equiv 0$，理想气体经节流膨胀后温度保持绝对不变。而对于 van der Waals 真实气体，在低压区忽略二阶微量后，其转化温度满足 $T_\mathrm{inv} \approx \frac{2a}{Rb}$。在室温下，氧气、氮气等绝大多数气体的转化温度显著高于室温，节流可直接获得显著致冷；然而氢气与氦气的范德华引力常数 $a$ 极小，室温处于其转化温度上限之上（常温下氢气的 $\mu_{JT} < 0$），常温节流不仅不会降温反而急剧自燃爆炸。因此，氢气与氦气在工业液化前，必须预先利用液氮进行深度预冷至转化温度以下。

---

## §4 Gibbs-Helmholtz 方程与变温化学平衡

在化学热力学中，考察 Gibbs 自由能与化学反应平衡常数对温度的依赖关系具有极端重要的实用价值。根据 Gibbs 自由能的基本方程 $dG = -S\,dT + V\,dp$，在恒定压强（$dp = 0$）下，有：

$$\left(\frac{\partial G}{\partial T}\right)_p = -S$$

将定义式 $G = H - TS$ 改写为 $-S = \frac{G - H}{T}$，代入上式即得：

$$\left(\frac{\partial G}{\partial T}\right)_p = \frac{G - H}{T}$$

为构造关于温度导数的更紧凑微分形式，对商式 $G/T$ 在恒压下求导：

$$\left[\frac{\partial (G/T)}{\partial T}\right]_p = \frac{1}{T}\left(\frac{\partial G}{\partial T}\right)_p - \frac{G}{T^2} = \frac{1}{T}\left(\frac{G - H}{T}\right) - \frac{G}{T^2} = -\frac{H}{T^2}$$

若引入倒数温度变量 $\tau = 1/T$，由于 $d(1/T) = -dT/T^2$，微分算符变换为 $\partial / \partial (1/T) = -T^2 (\partial / \partial T)$，上式可写为更加典雅对称的微分形式：

$$\left[\frac{\partial (G/T)}{\partial (1/T)}\right]_p = H$$

上述两式统称为 Gibbs-Helmholtz 方程。将其应用于恒温恒压下进行的任意化学反应，各状态函数替换为反应前后的增量 $\Delta_r$：

$$\left[\frac{\partial (\Delta_r G^\theta/T)}{\partial T}\right]_p = -\frac{\Delta_r H^\theta}{T^2} \qquad \text{或} \qquad \left[\frac{\partial (\Delta_r G^\theta/T)}{\partial (1/T)}\right]_p = \Delta_r H^\theta$$

Gibbs-Helmholtz 方程奠定了现代化学热力学变温计算的基石。在较小的温度变动区间内，若反应焓变 $\Delta_r H^\theta$ 随温度变化很小，可近似视为常数。在温度 $T_1$ 至 $T_2$ 之间分离变量积分：

$$\int_{T_1}^{T_2} d\left(\frac{\Delta_r G^\theta}{T}\right) = \int_{T_1}^{T_2} \Delta_r H^\theta\,d\left(\frac{1}{T}\right) \implies \frac{\Delta_r G^\theta(T_2)}{T_2} - \frac{\Delta_r G^\theta(T_1)}{T_1} = \Delta_r H^\theta\left(\frac{1}{T_2} - \frac{1}{T_1}\right)$$

结合等温化学反应基本关系式 $\Delta_r G^\theta = -RT\ln K^\theta$，将 $\Delta_r G^\theta / T = -R\ln K^\theta$ 代入微分式，两端同除以 $-R$，立即严格导出了支配化学平衡移动方向的 van't Hoff（范特霍夫）等压方程：

$$\frac{d\ln K^\theta}{dT} = \frac{\Delta_r H^\theta}{RT^2} \qquad \text{或} \qquad \frac{d\ln K^\theta}{d(1/T)} = -\frac{\Delta_r H^\theta}{R}$$

若反应体系经历宽阔的变温区间，热容变 $\Delta_r C_p^\theta$ 不可忽略，则必须引入 Kirchhoff 定律对反应焓变进行修正。已知定压下 $(\partial \Delta_r H^\theta/\partial T)_p = \Delta_r C_p^\theta$，在定标温度 $T^\theta = 298.15\ \mathrm{K}$ 下的反应焓变与任意温度 $T$ 下的关系为：

$$\Delta_r H^\theta(T) = \Delta_r H^\theta(T^\theta) + \int_{T^\theta}^T \Delta_r C_p^\theta\,dT$$

将温度依赖的 $\Delta_r H^\theta(T)$ 重新代回 Gibbs-Helmholtz 方程进行二次解析积分，即可精确预测冶金、化工催化等高温高压极端工况下的化学反应自由能与平衡转化率。

对 Gibbs-Helmholtz 方程进行深层次的物理挖掘，必然导向热力学第三定律与绝对零度极限行为。1906 年，Walther Nernst（能斯特）在探索电化学电池与凝聚态相平衡变温行为时，注意到了一个极具启发性的实验事实：在接近绝对零度的深冷区，化学反应的 Gibbs 自由能变化 $\Delta G$ 与焓变 $\Delta H$ 不仅数值越来越趋近，而且两条曲线的切线斜率均同步趋近于零。

![[da7ca24ace5670e0e1a89107a8740153e92416b9a06f0e6972905441e274473a.jpg]]
> 图 10-2：绝对零度极限下自由能与焓变曲线相切图景

由 Gibbs-Helmholtz 微分形式 $\left(\frac{\partial \Delta G}{\partial T}\right)_p = \frac{\Delta G - \Delta H}{T}$，当 $T \to 0$ 时，右端呈现 $0/0$ 型未定式。应用 L'Hôpital 法则对分子分母求导：

$$\lim_{T \to 0}\left(\frac{\partial \Delta G}{\partial T}\right)_p = \lim_{T \to 0} \frac{(\partial \Delta G/\partial T)_p - (\partial \Delta H/\partial T)_p}{1}$$

移项整理可知：$\lim_{T \to 0} (\partial \Delta H/\partial T)_p = 0$。根据基本热力学关系，$(\partial \Delta G/\partial T)_p = -\Delta S$，$(\partial \Delta H/\partial T)_p = \Delta C_p$。Nernst 由此正式提出了 Nernst 热定理：在绝对零度极限下，凝聚体系发生任何等温物理化学变化时，其熵变与定压热容差均趋向于零，即：

$$\lim_{T \to 0} \Delta S = 0, \qquad \lim_{T \to 0} \Delta C_p = 0$$

随后，Max Planck（普朗克）将 Nernst 热定理推向了最纯粹的微观绝对基准，确立了经典热力学第三定律的标准表述：在绝对零度时，任何纯物质完美晶体的熵值规定为零，即 $S(0\ \mathrm{K}) = 0$。这一伟大基准的确立，使得物理学家彻底挣脱了第一、第二定律只能测量熵差（$\Delta S$）的束缚，通过从 $0\ \mathrm{K}$ 到温度 $T$ 的低温比热积分 $S(T) = \int_0^T \frac{C_p}{T}\,dT$，成功建立起物质的标准摩尔绝对熵数据表。

---

## §5 Boltzmann 分布微观推导链与配分函数母机

宏观经典热力学通过状态函数与唯象定律精妙地给出了物理化学变化的判据与约束，但其根本无法解释宏观性质背后的微观本源。统计热力学以量子力学所揭示的微观能级为底层基石，通过概率论与统计平均方法，将微观粒子的量子态与宏观可观测的热力学性质完美贯通。

考察由 $N$ 个全同且弱相互作用粒子组成的孤立宏观体系，其体积固定为 $V$，总能量守恒为 $E$。在统计物理中，最核心的先验假设是等概率原理：对于处于热力学平衡状态的孤立系统，其体系一切可能实现的量子微观状态出现的概率均完全相等。

设单粒子具有一组离散的本征能级系列 $\varepsilon_0, \varepsilon_1, \varepsilon_2, \dots, \varepsilon_i$，各个能级对应的量子简并度为 $g_0, g_1, g_2, \dots, g_i$。将 $N$ 个粒子分配到这组能级上，若处于能级 $\varepsilon_i$ 的粒子数为 $N_i$，这一组特定的占据数集合 $\{N_0, N_1, N_2, \dots\}$ 即构成了体系的一个宏观构型（Macro-distribution）。假定粒子在晶格等定域点位上是相互可分辨的，根据排列组合原理，将 $N$ 个全同粒子分配至各个能级组的组合数为 $N! / \prod_i N_i!$。而在特定能级 $\varepsilon_i$ 内部，每个粒子均有 $g_i$ 种不同的独立微观量子态可供选择，$N_i$ 个粒子共有 $g_i^{N_i}$ 种选择方式。因此，对应于占据数集合 $\{N_i\}$ 的总微观状态数（又称热力学概率或构型权重 $W$）为：

$$W = N! \prod_i \frac{g_i^{N_i}}{N_i!}$$

对于由阿伏伽德罗常数数量级（$N \sim 10^{23}$）微观粒子构成的宏观系统，微观状态数 $W$ 是一个极端庞大的天文数字。由于 $N_i$ 普遍非常巨大，可以对阶乘项应用 Stirling（斯特林）渐近公式：$\ln n! \approx n\ln n - n$。对构型权重取对数展开：

$$\ln W = \ln N! + \sum_i N_i\ln g_i - \sum_i \ln N_i! \approx N\ln N - N + \sum_i N_i\ln g_i - \sum_i (N_i\ln N_i - N_i)$$

由于总粒子数守恒条件 $\sum_i N_i = N$，式中 $-N$ 与 $\sum_i N_i$ 相互抵消，得到：

$$\ln W = N\ln N - \sum_i N_i \ln\left(\frac{N_i}{g_i}\right)$$

在平衡态下，根据等概率原理，实际被观测到的宏观平衡态必然对应于微观状态数最多（即对数权重 $\ln W$ 达到全局极大值）的构型，这一构型被称为最概然分布（Most Probable Distribution）。寻找最概然分布数学上属于在特定物理约束下的多元函数条件极值问题。体系受制于两个刚性守恒约束：

$$\text{粒子总数守恒：} \quad \sum_i N_i = N \implies \sum_i dN_i = 0$$

$$\text{总能量守恒：} \quad \sum_i N_i \varepsilon_i = E \implies \sum_i \varepsilon_i\,dN_i = 0$$

采用 Lagrange 未定乘子法，引入两个待定参数 $\alpha$ 与 $\beta$，构造辅助无约束泛函变分：

$$d\left[\ln W - \alpha\sum_i N_i - \beta\sum_i N_i \varepsilon_i\right] = 0$$

展开对数微分，由于 $d\ln W = -\sum_i [\ln(N_i/g_i) + 1]\,dN_i$，将各约束微分项合并：

$$\sum_i \left[-\ln\left(\frac{N_i}{g_i}\right) - 1 - \alpha - \beta \varepsilon_i\right] dN_i = 0$$

由于引入了两个独立的未定乘子，各个能级占据数的变分 $dN_i$ 相互独立，上式方括号内的系数对于每一个能级 $i$ 均必须严格恒等于零。移项整理：

$$\ln\left(\frac{N_i}{g_i}\right) = -(1 + \alpha) - \beta \varepsilon_i \implies N_i = g_i\, e^{-(1+\alpha)}\, e^{-\beta \varepsilon_i}$$

对所有能级占据数求和，利用粒子数守恒条件消去乘子 $\alpha$：

$$\sum_i N_i = e^{-(1+\alpha)} \sum_i g_i\, e^{-\beta \varepsilon_i} = N \implies e^{-(1+\alpha)} = \frac{N}{\sum_i g_i\, e^{-\beta \varepsilon_i}}$$

将上式代回 $N_i$ 的表达式，立即导出统计物理中最核心的著名定律——Maxwell-Boltzmann 分布律：

$$\frac{N_i}{N} = \frac{g_i\, e^{-\beta \varepsilon_i}}{q}$$

式中分母 $q$ 定义为体系的单分子配分函数（Molecular Partition Function）：

$$q = \sum_i g_i\, e^{-\beta \varepsilon_i}$$

接下来必须揭示未定乘子 $\beta$ 的真实物理身份。由 Ludwig Boltzmann 提出的著名统计熵公式 $S = k \ln W$，将最概然分布的占据数代入 $\ln W$ 展开式中：

$$S = k\left[N\ln N - \sum_i N_i \left(-\ln q - \beta \varepsilon_i + \ln N\right)\right] = k\left(N\ln q + \beta\sum_i N_i \varepsilon_i\right) = Nk\ln q + k\beta E$$

在恒容（$dV = 0$）可逆过程中，能级 $\varepsilon_i$ 不发生位移，体系吸收的热量全部用于提高能级占据数，使得内能改变 $dE = \delta q_\mathrm{rev} = T\,dS$。由热力学第二定律知：

$$\frac{1}{T} = \left(\frac{\partial S}{\partial E}\right)_V = k\beta \implies \beta = \frac{1}{kT}$$

这一精辟的微观认证宣告：Lagrange 未定乘子 $\beta$ 的微观物理本质正是绝对温度与 Boltzmann 常数乘积的倒数（$\beta = 1/kT$）。温度在微观统计中并非某种玄虚的属性，而是衡量微观粒子在不同能级间按指数衰减布居陡峭程度的统计标度参数。

配分函数 $q = \sum_i g_i e^{-\varepsilon_i/kT}$ 不仅仅是一个归一化分母常数，它是统计热力学中的总母机与生成元。配分函数的微观物理图像可直观理解为：在温度 $T$ 下，一个分子在量子世界中所能“有效接触并热占据”的微观量子状态总数的无量纲度量。

![[e2dca534a248ed1c527ac74194db3316cc7c0f127946784a3e731f8b0e6fe649.jpg]]
> 图 10-3：双能级体系配分函数随温度演化曲线

考察非简并基态（$\varepsilon_0 = 0, g_0 = 1$）与一个非简并激发态（$\varepsilon_1 = \varepsilon, g_1 = 1$）构成的典型双能级体系。其配分函数为 $q = 1 + e^{-\varepsilon/kT}$。当处于绝对零度极限（$T \to 0$）时，指数因子 $e^{-\varepsilon/kT} \to 0$，配分函数退化为 $q = 1$，所有粒子全部不可动摇地处于能量最低的基态；当温度极高（$kT \gg \varepsilon$）时，指数因子 $e^{-\varepsilon/kT} \to 1$，配分函数趋于饱和值 $q \to 2$，两个能级被等概率均分占据。

---

## §6 分子配分函数的微观解耦与各模式展开

在实际多原子分子体系中，单分子的微观运动状态复杂，包含了在三维空间中的质心平动、绕惯性主轴的分子整体转动、各化学键与键角的骨架振动以及分子内部电子态与原子核自旋的取向跃迁。根据量子力学的 Born-Oppenheimer 近似与刚性转子-简谐振子近似，不同空间坐标与时间尺度的运动模式在很大程度上是相互独立的。分子的总能量可以高度精确地写为各独立运动模式能量的代数加和：

$$\varepsilon = \varepsilon^T + \varepsilon^R + \varepsilon^V + \varepsilon^E$$

利用指数函数的代数性质，能量加和在指数项中自然转化为指数项的连乘积：$e^{-\beta \varepsilon} = e^{-\beta \varepsilon^T} \cdot e^{-\beta \varepsilon^R} \cdot e^{-\beta \varepsilon^V} \cdot e^{-\beta \varepsilon^E}$。将多重求和分离，单分子配分函数 $q$ 严格呈现各运动自由度配分函数的连乘形式：

$$q = q^T \cdot q^R \cdot q^V \cdot q^E$$

第一，平动配分函数 $q^T$。将质量为 $m$ 的单分子置于宏观体积为 $V = L_x L_y L_z$ 的三维三维方势阱中。由量子力学薛定谔方程，分子在三个正交方向上的平动能级完全解耦：$\varepsilon^T = \frac{h^2}{8m}\left(\frac{n_x^2}{L_x^2} + \frac{n_y^2}{L_y^2} + \frac{n_z^2}{L_z^2}\right)$，其中量子数 $n_x, n_y, n_z = 1, 2, 3, \dots$。由于宏观容器线度 $L \sim 10^{-1}\ \mathrm{m}$，相邻能级间隔微小（$\Delta\varepsilon \sim 10^{-38}\ \mathrm{J} \ll kT \sim 10^{-21}\ \mathrm{J}$），分立求和可精确地转变为连续积分。以 $x$ 方向为例：

$$q_x^T = \sum_{n_x=1}^\infty e^{-\frac{\beta h^2 n_x^2}{8m L_x^2}} \approx \int_0^\infty e^{-\frac{\beta h^2 n_x^2}{8m L_x^2}}\,dn_x = \frac{\sqrt{2\pi m k T}}{h} L_x$$

三个独立方向配分函数连乘，并乘以容器体积 $V = L_x L_y L_z$，得到著名的三维平动配分函数公式：

$$q^T = q_x^T q_y^T q_z^T = \frac{(2\pi m k T)^{3/2}}{h^3} V = \frac{V}{\Lambda^3}$$

式中引入了重要的微观特征尺度——热 de Broglie 波长 $\Lambda$：

$$\Lambda = \frac{h}{\sqrt{2\pi m k T}}$$

从物理图像上看，$\Lambda^3$ 代表了单个分子由于量子热起伏所占据的有效“量子体积”。$q^T = V/\Lambda^3$ 的物理意义在于：体系宏观体积 $V$ 能够容纳的热量子波包总数。当宏观分子数密度远小于量子饱和密度（即单分子所占平均空间体积 $V/N \gg \Lambda^3$ 时），经典 Maxwell-Boltzmann 统计成立；反之，若在极低温度或极高密度下 $V/N \sim \Lambda^3$，则波函数发生严重交叠，体系必须转向 Bose-Einstein 统计或 Fermi-Dirac 统计。

第二，转动配分函数 $q^R$。考察质量集中在惯性主轴上的刚性双原子转子。转动薛定谔方程给出转动量子能级为 $\varepsilon_J = J(J+1)hc\tilde{B}$，对应简并度为 $g_J = 2J+1$，其中 $J = 0, 1, 2, \dots$ 为转动量子数，$\tilde{B} = \frac{h}{8\pi^2 c I}$ 为转动常数（单位通常为 $\mathrm{cm}^{-1}$），$I$ 为转动惯量。转动配分函数为：

$$q^R = \sum_{J=0}^\infty (2J+1) e^{-\beta J(J+1)hc\tilde{B}}$$

在室温绝大多数情况下，分子的转动特征温度 $\Theta_R = \frac{hc\tilde{B}}{k}$ 仅为数开尔文（例如氮气 $\Theta_R \approx 2.88\ \mathrm{K}$，氧气 $\Theta_R \approx 2.08\ \mathrm{K}$），远低于实验温度（$T \gg \Theta_R$）。此时转动能级准连续分布，可进行积分化简：

$$q^R \approx \int_0^\infty (2J+1) e^{-\frac{hc\tilde{B}}{kT} J(J+1)}\,dJ = \frac{kT}{hc\tilde{B}}$$

当考虑分子的核空间对称性时，若分子在空间旋转过程中能够出现不可分辨的等价空间构型，则会导致同一种微观构型在经典求和中被重复计算。必须在分母引入空间对称数 $\sigma$（Symmetry Number）予以校正：

$$q^R = \frac{kT}{\sigma hc\tilde{B}} = \frac{T}{\sigma \Theta_R}$$

对称数 $\sigma$ 由分子的点群严格决定：对于无空间反演轴的异核双原子分子或不对称线型分子（如 $\mathrm{CO}, \mathrm{NO}, \mathrm{HCl}, \mathrm{HCN}$），空间翻转 $180^\circ$ 产生完全不同的构型，故 $\sigma = 1$；对于中心对称的同核双原子或线型分子（如 $\mathrm{N}_2, \mathrm{O}_2, \mathrm{CO}_2, \mathrm{C}_2\mathrm{H}_2$），绕垂直于键轴旋转 $180^\circ$ 呈现完全不可分辨的构型，故 $\sigma = 2$。对于非线性多原子多轴分子，例如水分子 $\mathrm{H}_2\mathrm{O}$（$C_{2v}$ 点群）$\sigma = 2$；氨分子 $\mathrm{NH}_3$（$C_{3v}$ 点群）$\sigma = 3$；甲烷分子 $\mathrm{CH}_4$（$T_d$ 点群）$\sigma = 12$；苯分子 $\mathrm{C}_6\mathrm{H}_6$（$D_{6h}$ 点群）$\sigma = 12$。

第三，振动配分函数 $q^V$。在简谐振子近似下，单个振动模的量子能级本征值为 $\varepsilon_v = (v + 1/2)hc\tilde{\nu}$，其中 $v = 0, 1, 2, \dots$ 为振动量子数，$\tilde{\nu}$ 为振动基本波数，能级简并度为 $g_v \equiv 1$。若选取 $v=0$ 的零点振动能能级作为能量参考零点，则振动能级差为 $\varepsilon_v - \varepsilon_0 = vhc\tilde{\nu}$。求公比为 $e^{-\beta hc\tilde{\nu}}$ 的等比无穷级数之和：

$$q^V = \sum_{v=0}^\infty e^{-v \beta hc\tilde{\nu}} = \frac{1}{1 - e^{-\beta hc\tilde{\nu}}} = \frac{1}{1 - e^{-\Theta_V/T}}$$

式中定义振动特征温度 $\Theta_V = \frac{hc\tilde{\nu}}{k}$。化学键的力常数极大，通常多原子分子的特征振动温度高达上千开尔文（例如氮气 $\Theta_V \approx 3374\ \mathrm{K}$，一氧化碳 $\Theta_V \approx 3120\ \mathrm{K}$，水分子伸缩振动 $\Theta_V \approx 5300\ \mathrm{K}$）。在室温（$T \approx 300\ \mathrm{K}$）下，$\Theta_V/T \gg 1$，指数项 $e^{-\Theta_V/T} \approx 0$，导致分母接近 1，即 $q^V \approx 1$。这意味着在常温常压下，绝大多数分子的化学键骨架振动均处于深度冻结状态，仅停留在基态而无法被热激发。

![[45d5e5f3be2bb30bea78ad397179f9243c7f890aa8a057b2cef13d11c29280a3.jpg]]
> 图 10-4：量子谐振子能级占据直方图随温度演化特征

第四，电子配分函数 $q^E$。绝大多数稳定分子的基态电子层均为闭壳层构型，基态电子自旋单态（$S=0, g_0 = 1$），而第一激发电子态能级差通常在数个电子伏特（$1\ \mathrm{eV} \sim 11600\ \mathrm{K}$）以上，在热力学温度下完全不可激发。因此电子配分函数通常直接退化为基态简并度 $q^E = g_0$。对于闭壳层分子（如 $\mathrm{N}_2, \mathrm{CO}_2, \mathrm{CH}_4$），$g_0 = 1$；对于含单电子的自由基（如 $\mathrm{NO}_2$），自旋双重态 $g_0 = 2S + 1 = 2$；对于基态具有开壳层三线态的氧气分子 $\mathrm{O}_2$（基态为 $^3\Sigma_g^-$），$g_0 = 3$。特例是 $\mathrm{NO}$ 分子，其基态 $^2\Pi_{1/2}$ 与低激发态 $^2\Pi_{3/2}$ 之间的自旋-轨道耦合分裂能仅为 $121\ \mathrm{cm}^{-1}$（相当于约 $174\ \mathrm{K}$），在常温下两能级均有显著占据，此时必须采用 $q^E = 2 + 2e^{-174/T}$ 进行双重态求和。

---

## §7 从分子配分函数桥接宏观热力学量

获知了单分子配分函数 $q$ 之后，接下来的核心命题是如何建立宏观多粒子体系总配分函数 $Q$ 并由此推导宏观热力学量。必须对体系的粒子可分辨性做严格区分：

其一为定域粒子系统（Localized Systems）：例如晶体点阵中的原子或配位分子。每个粒子被束缚在明确的空间晶格坐标上，空间位置的差异赋予了每个粒子天然的可分辨标记。对于 $N$ 个独立的定域粒子，体系总微观状态数直接为各个粒子状态数的乘积，体系总配分函数为：

$$Q = q^N$$

其二为离域粒子系统（Delocalized Systems）：例如气相中的气体分子。粒子在整个容器内高速无规则运动，属于完全相同的全同粒子，在量子力学上是绝对不可区分的。若依然直接写成 $q^N$，则任何一种微观状态中全同粒子的不同位置排列都会被重复计数 $N!$ 次。为了消除这种由全同不可区分性带来的非物理重复计数，体系总配分函数必须除以 $N!$ 进行校正：

$$Q = \frac{q^N}{N!}$$

这一因子 $1/N!$ 的引入具有重要的历史意义，正是它彻底化解了困扰古典热力学数十年的“Gibbs 悖论”（即同种气体等温等压虚构扩散混合时熵变不为零的逻辑谬误）。

一旦获得体系的总配分函数 $Q = Q(T, V, N)$，全部经典热力学平衡函数均可作为其解析偏导数直接导出。

首先导出体系内能（以内能基态零点能 $U(0)$ 为基准）：

$$U - U(0) = \sum_i N_i \varepsilon_i = \sum_i \frac{N \varepsilon_i g_i e^{-\beta \varepsilon_i}}{q} = -\frac{N}{q}\frac{\partial}{\partial \beta}\left(\sum_i g_i e^{-\beta \varepsilon_i}\right) = -N\left(\frac{\partial \ln q}{\partial \beta}\right)_V$$

利用链式求导法则 $\frac{\partial}{\partial \beta} = \frac{\partial T}{\partial \beta}\frac{\partial}{\partial T} = -kT^2\frac{\partial}{\partial T}$，可写为温度导数形式：

$$U - U(0) = NkT^2\left(\frac{\partial \ln q}{\partial T}\right)_V = kT^2\left(\frac{\partial \ln Q}{\partial T}\right)_V$$

其次导出 Helmholtz 自由能 $A$。由热力学基本方程 $A = U - TS$，结合统计熵公式，经过系统的热力学关系对合，可严格证明 Helmholtz 自由能正是体系总配分函数的对数表象：

$$A - A(0) = -kT\ln Q$$

对于定域子系统：$A - A(0) = -NkT\ln q$。
对于气相离域子系统，代入 $Q = q^N / N!$ 并利用 Stirling 公式 $\ln N! \approx N\ln N - N$：

$$A - A(0) = -kT\ln\left(\frac{q^N}{N!}\right) = -kT(N\ln q - N\ln N + N) = -NkT\left[\ln\left(\frac{q}{N}\right) + 1\right] = -NkT\ln\left(\frac{qe}{N}\right)$$

再由 Helmholtz 自由能全微分 $dA = -S\,dT - p\,dV$，立即导出宏观压强 $p$ 的统计微观表达式：

$$p = -\left(\frac{\partial A}{\partial V}\right)_T = kT\left(\frac{\partial \ln Q}{\partial V}\right)_T = NkT\left(\frac{\partial \ln q}{\partial V}\right)_T$$

由于单分子配分函数中仅有平动部分 $q^T = \frac{(2\pi m k T)^{3/2}}{h^3} V$ 显式依赖于体积 $V$（转动、振动与电子模式均只依赖分子内坐标而与宏观体积无关），因此 $\ln q = \ln V + f(T)$。代入压强公式：

$$p = NkT\left(\frac{\partial \ln V}{\partial V}\right)_T = \frac{NkT}{V} \implies pV = NkT = nRT$$

这是物理化学史上最重要的结果之一：无需引入任何唯象的气体实验定律，仅凭三维量子方势阱能级积分与全同粒子不可区分性，统计热力学从第一性原理直接严格推导出了理想气体状态方程。

最后导出体系的统计熵 $S$。根据热力学关系 $S = -\left(\frac{\partial A}{\partial T}\right)_V = \frac{U - A}{T}$：

定域子系统的统计熵公式：

$$S = \frac{U - U(0)}{T} + Nk\ln q$$

离域气相系统的统计熵公式：

$$S = \frac{U - U(0)}{T} + Nk\ln\left(\frac{qe}{N}\right) = \frac{U - U(0)}{T} + Nk\ln\left(\frac{q}{N}\right) + Nk$$

对比定域子与离域子两式可知，对于完全相同的一组微观能级分布，离域全同粒子的摩尔统计熵比定域粒子严格低了一个确定项：

$$\Delta S_\mathrm{m} = S_{\mathrm{m},\text{离域}} - S_{\mathrm{m},\text{定域}} = R\ln\left(\frac{e}{N_A}\right) = R(1 - \ln N_A)$$

代入常数 $R = 8.314\ \mathrm{J\cdot K^{-1}\cdot mol^{-1}}$ 与 $N_A = 6.022\times 10^{23}\ \mathrm{mol}^{-1}$（$\ln N_A \approx 54.75$）：

$$\Delta S_\mathrm{m} = 8.314 \times (1 - 54.75) = -446.9\ \mathrm{J\cdot K^{-1}\cdot mol^{-1}}$$

这表明在相同的内部自由度激发条件下，定域由于粒子处于可区分的定点晶格，其宏观排列构型数远大于完全无法区分的全同流动气体。

---

## §8 统计热力学的核心应用与微观图像

在掌握了配分函数与热力学量的桥接关系后，统计热力学在三大领域展现了无可比拟的理论威力：精确计算单原子分子的绝对熵、定量揭示低温残余熵的微观机制，以及从微观态密度预测化学反应的平衡常数。

第一，Sackur-Tetrode 方程（单原子气体的绝对熵）。对于单原子理想气体（如 $\mathrm{He}, \mathrm{Ne}, \mathrm{Ar}, \mathrm{Kr}$），分子没有分子内转动与振动自由度，室温下电子态处于非简并单线态基态（$q^E = 1$），全部配分函数均由平动提供：$q = q^T = V/\Lambda^3$。由单原子气体内能 $U - U(0) = \frac{3}{2}NkT$（每分子平均动能 $\frac{3}{2}kT$），将内能与配分函数代入离域子统计熵公式：

$$S = \frac{\frac{3}{2}NkT}{T} + Nk\ln\left(\frac{V e}{N\Lambda^3}\right) = Nk\left[\frac{3}{2} + 1 + \ln\left(\frac{V}{N\Lambda^3}\right)\right] = Nk\left[\ln\left(\frac{V}{N\Lambda^3}\right) + \frac{5}{2}\right]$$

将其换算为 1 摩尔单原子理想气体的标准摩尔绝对熵 $S_\mathrm{m}^\theta$。令 $N = N_A$，$Nk = R$，摩尔体积 $V_\mathrm{m} = RT/p^\theta$：

$$S_\mathrm{m}^\theta = R\ln\left(\frac{V_\mathrm{m} e^{5/2}}{N_A \Lambda^3}\right) = R\left[\frac{5}{2}\ln T + \frac{3}{2}\ln M - \ln(p^\theta/\mathrm{Pa})\right] - 9.68\ \mathrm{J\cdot K^{-1}\cdot mol^{-1}}$$

式中 $M$ 为相对分子质量。这就是由 Otto Sackur 与 Hugo Tetrode 分别独立推导出的著名的 Sackur-Tetrode 方程。该方程在物理学史上占有崇高的地位：它完全不依赖任何低温量热比热数据，仅凭普朗克常数 $h$、玻尔兹曼常数 $k$、气体摩尔质量 $M$ 与温度 $T$，便以显著的精度直接计算出了气体的热力学第三定律绝对熵。其实验检验精度高达小数点后两到三位有效数字，成为了量子统计物理重要成就。

第二，残余熵（Residual Entropy）与微观冻结无序。热力学第三定律断言完美晶体在 $0\ \mathrm{K}$ 下熵为零。然而在 20 世纪前期的低温实验中，化学家通过量热积分 $S_\mathrm{cal}(298.15\ \mathrm{K}) = \int_0^{298.15} \frac{C_p}{T}\,dT + \sum \frac{\Delta H_\mathrm{相变}}{T_\mathrm{相变}}$ 测得的量热熵，在与光谱数据通过统计力学计算得出的绝对熵对比时，发现一氧化碳 $\mathrm{CO}$、一氧化二氮 $\mathrm{N}_2\mathrm{O}$ 以及普通固态冰 $\mathrm{H}_2\mathrm{O}$ 等物质存在系统的正偏差：

$$S_\mathrm{spec} - S_\mathrm{cal} = S_0 > 0$$

这一偏差值 $S_0$ 被称为绝对零度下的残余熵。统计热力学对残余熵给出了深刻而唯妙的微观诠释：在晶体自熔体或高温缓慢冷却凝固的过程中，分子的微观偶极矩极小（例如 $\mathrm{CO}$ 的偶极矩仅为 $0.11\ \mathrm{Debye}$），分子以正向 $\mathrm{C}-\mathrm{O}$ 排列与反向 $\mathrm{O}-\mathrm{C}$ 排列的晶格静电能差异微小（$\Delta\varepsilon \ll kT$）。当温度降低至极低温时，晶格分子发生旋转翻转所必须跨越的空间位阻活化势垒却相当可观。分子在其取向能够完全有序化之前，其无规取向状态便已被晶格的坚硬势阱永久“冻结”。

在 $0\ \mathrm{K}$ 时，每个 $\mathrm{CO}$ 分子在其固定的晶格位点上均保留有 2 种完全等价的朝向可能。对于 1 摩尔由 $N_A$ 个分子构成的晶体，其冻结的可能微观构型总数高达 $W_0 = 2^{N_A}$。应用 Boltzmann 统计熵公式：

$$S_0 = k\ln W_0 = k\ln\left(2^{N_A}\right) = N_A k\ln 2 = R\ln 2 \approx 8.314 \times 0.6931 = 5.76\ \mathrm{J\cdot K^{-1}\cdot mol^{-1}}$$

该理论预测值与实验精确量热测定值 $5.8\ \mathrm{J\cdot K^{-1}\cdot mol^{-1}}$ 几乎完全重合。

对于普通冰晶体（冰 $\mathrm{I}_h$），Linus Pauling（鲍林）于 1935 年提出了闻名遐迩的冰残余熵理论。在冰晶格中，每个氧原子处于四个最近邻氧原子构成的正四面体顶点中心，其间以氢键相连。根据“冰规则”（Bernal-Fowler 规则）：每个氧原子必须紧密结合 2 个共价氢原子，并在较远距离接受另外 2 个氢原子的氢键配位（即维持完整的 $\mathrm{H}_2\mathrm{O}$ 分子单元）。对于 1 摩尔冰，共有 $2N_A$ 条氢键，质子在氢键上有 2 个偏心势阱位置，总无约束状态数为 $2^{2N_A} = 4^{N_A}$。而每个氧原子周围的 4 个质子共有 $2^4 = 16$ 种占据可能，其中恰好满足“2 近 2 远”化学分子规则的构型只有 $C_4^2 = 6$ 种，满足几率为 $6/16 = 3/8$。因此，全晶格能够同时满足冰规则的允许微观构型总数为：

$$W_0 \approx 4^{N_A} \times \left(\frac{6}{16}\right)^{N_A} = \left(4 \times \frac{3}{8}\right)^{N_A} = \left(\frac{3}{2}\right)^{N_A}$$

代入 Boltzmann 熵公式，Pauling 冰残余熵理论值为：

$$S_0 = R\ln\left(\frac{3}{2}\right) \approx 8.314 \times 0.4055 = 3.37\ \mathrm{J\cdot K^{-1}\cdot mol^{-1}}$$

与量热实验实测值 $3.4\ \mathrm{J\cdot K^{-1}\cdot mol^{-1}}$ 高度吻合。

为什么完美晶体在 $0\ \mathrm{K}$ 附近的低温热容必须遵循 Debye（德拜）$T^3$ 定律？在三维晶体点阵中，声子是原子集体晶格振动的量子化表现。在趋近绝对零度时，高频光学支声子全部被冻结，唯有波长极长的低频声学支纵波与横波能够被微弱激发。色散关系 $\omega = v_s k$ 导致声子态密度与能量平方成正比 $g(\varepsilon) \propto \varepsilon^2$。代入 Bose-Einstein 积分求内能导数，得出三维完美绝缘晶体的低温热容具有普遍的立方律：

$$C_V = \frac{12\pi^4}{5} N R\left(\frac{T}{\Theta_D}\right)^3 \propto T^3$$

式中 $\Theta_D$ 为晶体的 Debye 特征温度。根据热力学量热熵积分 $S(T) = \int_0^T \frac{C_V}{T}\,dT = \mathrm{const}\int_0^T T^2\,dT = \frac{\mathrm{const}}{3}T^3$，由于被积函数在下限 $T \to 0$ 处收敛良好且比值趋零，从而从微观量子声子学严格保证了完美晶体在 $0\ \mathrm{K}$ 时热力学绝对熵趋向于零。

第三，统计平衡常数与反应能级阶梯。在宏观热力学中，化学反应平衡由等温等压判据 $\Delta_r G^\theta = -RT\ln K_p^\theta$ 给出。在统计物理中，单组分化学势定义为 $\mu_i = \left(\frac{\partial A}{\partial N_i}\right)_{T, V} = -kT\ln\left(\frac{q_i}{N_i}\right) + \varepsilon_{0,i}$，式中 $\varepsilon_{0,i}$ 为单分子在绝对零度时的基态能量。在宏观化学平衡条件 $\sum_i \nu_i \mu_i = 0$ 约束下：

$$\sum_i \nu_i \left[-kT\ln\left(\frac{q_i}{N_i}\right) + \varepsilon_{0,i}\right] = 0 \implies \sum_i \nu_i \ln\left(\frac{N_i}{q_i}\right) = -\frac{\sum_i \nu_i \varepsilon_{0,i}}{kT} = -\frac{\Delta_r E_0}{RT}$$

![[8f91fe544c7e81773b7e8044a60152cbb3c4389ce5678904c96d300bb70373ff.jpg]]
> 图 10-5：化学反应基元阶梯能级微观平衡分配图景

将分子数密度 $N_i/V$ 用理想气体分压 $p_i = (N_i/V)kT$ 代换，并以标准态压强 $p^\theta$ 规范化，立即得出标准平衡常数 $K_p^\theta$ 的微观第一性原理统计公式：

$$K_p^\theta = \prod_i \left(\frac{q_{i,\mathrm{m}}^\theta}{N_A}\right)^{\nu_i} \exp\left(-\frac{\Delta_r E_0}{RT}\right)$$

式中 $q_{i,\mathrm{m}}^\theta$ 为标准态压强 $p^\theta$ 下组分 $i$ 的摩尔配分函数，$\Delta_r E_0 = N_A \sum \nu_i \varepsilon_{0,i}$ 为摩尔基态量子零点能差。该公式表明：宏观化学平衡的本质，是产物与反应物在微观相空间态密度（由配分函数 $q$ 的比值表征）与量子基态能量阶梯（由 Boltzmann 因子 $\exp(-\Delta_r E_0/RT)$ 表征）之间达成的一场终极热力学妥协。

---

## §9 经典示范例题

**例 1**（真实气体状态方程与偏导数变换）
设某真实气体服从 van der Waals 状态方程：$\left(p + \frac{a}{V_\mathrm{m}^2}\right)(V_\mathrm{m} - b) = RT$。试应用热力学第一状态方程与 Maxwell 关系式，严格推导：
(1) 该气体的内压力 $\pi_T = \left(\frac{\partial U_\mathrm{m}}{\partial V_\mathrm{m}}\right)_T$；
(2) 该气体发生 Joule 绝热自由膨胀（$U$ 恒定，$dU = 0$）时的温度变化率 $\left(\frac{\partial T}{\partial V_\mathrm{m}}\right)_U$；
(3) 若 1 摩尔该气体在绝热自由膨胀中体积由 $V_1$ 膨胀至 $V_2$，试求其温度变化量 $\Delta T$ 的解析表达式。

**详细微观解析**：

(1) 将 van der Waals 方程整理为压强的显式表达式：
$$p = \frac{RT}{V_\mathrm{m} - b} - \frac{a}{V_\mathrm{m}^2}$$
在恒容条件下对温度求偏导：
$$\left(\frac{\partial p}{\partial T}\right)_{V_\mathrm{m}} = \frac{R}{V_\mathrm{m} - b}$$
根据热力学第一状态方程 $\left(\frac{\partial U_\mathrm{m}}{\partial V_\mathrm{m}}\right)_T = T\left(\frac{\partial p}{\partial T}\right)_{V_\mathrm{m}} - p$：
$$\left(\frac{\partial U_\mathrm{m}}{\partial V_\mathrm{m}}\right)_T = T\left(\frac{R}{V_\mathrm{m} - b}\right) - \left(\frac{RT}{V_\mathrm{m} - b} - \frac{a}{V_\mathrm{m}^2}\right) = \frac{a}{V_\mathrm{m}^2}$$
故该气体的内压力为 $\pi_T = \frac{a}{V_\mathrm{m}^2}$。

(2) 考虑内能的全微分 $dU_\mathrm{m} = \left(\frac{\partial U_\mathrm{m}}{\partial T}\right)_{V_\mathrm{m}} dT + \left(\frac{\partial U_\mathrm{m}}{\partial V_\mathrm{m}}\right)_T dV_\mathrm{m} = C_{V,\mathrm{m}}\,dT + \left(\frac{\partial U_\mathrm{m}}{\partial V_\mathrm{m}}\right)_T dV_\mathrm{m}$。
在绝热自由膨胀中，体系不吸热（$q=0$）且不克服外压做功（$w=0$），故由第一定律知内能保持不变（$dU_\mathrm{m} = 0$）。
令 $dU_\mathrm{m} = 0$，应用偏导数循环法则：
$$\left(\frac{\partial T}{\partial V_\mathrm{m}}\right)_U = -\frac{(\partial U_\mathrm{m}/\partial V_\mathrm{m})_T}{(\partial U_\mathrm{m}/\partial T)_{V_\mathrm{m}}} = -\frac{a/V_\mathrm{m}^2}{C_{V,\mathrm{m}}} = -\frac{a}{C_{V,\mathrm{m}} V_\mathrm{m}^2}$$

(3) 假定在膨胀的温区内定容摩尔热容 $C_{V,\mathrm{m}}$ 视为常数。在初态 $(T_1, V_1)$ 到末态 $(T_2, V_2)$ 之间分离变量积分：
$$dT = -\frac{a}{C_{V,\mathrm{m}} V_\mathrm{m}^2}\,dV_\mathrm{m} \implies \int_{T_1}^{T_2} dT = -\frac{a}{C_{V,\mathrm{m}}} \int_{V_1}^{V_2} \frac{1}{V_\mathrm{m}^2}\,dV_\mathrm{m}$$
$$\Delta T = T_2 - T_1 = \left[\frac{a}{C_{V,\mathrm{m}} V_\mathrm{m}}\right]_{V_1}^{V_2} = -\frac{a}{C_{V,\mathrm{m}}}\left(\frac{1}{V_1} - \frac{1}{V_2}\right)$$
由于 $V_2 > V_1$ 且范德华常数 $a > 0$，括号内项恒为正，因此 $\Delta T < 0$。该微观推导从严格理论上证明：真实气体发生绝热自由膨胀时，必须消耗热运动动能去克服分子间固有的范德华引力势阱做功，因而必然导致气体温度显著下降。

---

**例 2**（Gibbs-Helmholtz 方程与 Kirchhoff 耦合积分）
某气相合成反应在 $298.15\ \mathrm{K}$ 下的标准摩尔反应焓为 $\Delta_r H^\theta(298.15\ \mathrm{K}) = -92.22\ \mathrm{kJ\cdot mol^{-1}}$，标准摩尔 Gibbs 自由能变为 $\Delta_r G^\theta(298.15\ \mathrm{K}) = -33.00\ \mathrm{kJ\cdot mol^{-1}}$。在所研究的温度区间内，反应的定压热容差可近似表达为经验常数 $\Delta_r C_p^\theta = -40.00\ \mathrm{J\cdot K^{-1}\cdot mol^{-1}}$。试推导：
(1) 反应焓变 $\Delta_r H^\theta(T)$ 关于绝对温度 $T$ 的函数关系式；
(2) 利用 Gibbs-Helmholtz 方程的微分形式，推导该反应的标准摩尔 Gibbs 自由能变 $\Delta_r G^\theta(T)$ 的解析积分表达式；
(3) 计算反应在 $T = 600\ \mathrm{K}$ 下的标准摩尔 Gibbs 自由能变 $\Delta_r G^\theta(600\ \mathrm{K})$。

**详细微观解析**：

(1) 根据 Kirchhoff 定律，在恒压下 $(\partial \Delta_r H^\theta/\partial T)_p = \Delta_r C_p^\theta$。从参考温度 $T^\theta = 298.15\ \mathrm{K}$ 积分至温度 $T$：
$$\Delta_r H^\theta(T) = \Delta_r H^\theta(T^\theta) + \Delta_r C_p^\theta (T - T^\theta)$$
代入具体数值：
$$\Delta_r H^\theta(T) = -92220 + (-40.00)(T - 298.15) = -80294 - 40.00\,T \quad (\mathrm{J\cdot mol^{-1}})$$

(2) 由 Gibbs-Helmholtz 微分方程：
$$\left[\frac{\partial (\Delta_r G^\theta/T)}{\partial T}\right]_p = -\frac{\Delta_r H^\theta(T)}{T^2} = -\frac{\Delta_r H^\theta(T^\theta) - \Delta_r C_p^\theta T^\theta}{T^2} - \frac{\Delta_r C_p^\theta}{T}$$
对上式两端从 $T^\theta$ 到 $T$ 进行不定积分或定积分：
$$\int_{T^\theta}^T d\left(\frac{\Delta_r G^\theta}{T}\right) = \int_{T^\theta}^T \left[-\frac{\Delta_r H_0}{T^2} - \frac{\Delta_r C_p^\theta}{T}\right] dT$$
式中积分基准常数 $\Delta_r H_0 = \Delta_r H^\theta(T^\theta) - \Delta_r C_p^\theta T^\theta = -80294\ \mathrm{J\cdot mol^{-1}}$。
积分求解：
$$\frac{\Delta_r G^\theta(T)}{T} - \frac{\Delta_r G^\theta(T^\theta)}{T^\theta} = \Delta_r H_0 \left(\frac{1}{T} - \frac{1}{T^\theta}\right) - \Delta_r C_p^\theta \ln\left(\frac{T}{T^\theta}\right)$$
两端同乘以 $T$，整理得到解析解：
$$\Delta_r G^\theta(T) = \frac{T}{T^\theta}\Delta_r G^\theta(T^\theta) + \Delta_r H_0\left(1 - \frac{T}{T^\theta}\right) - \Delta_r C_p^\theta\,T\ln\left(\frac{T}{T^\theta}\right)$$

(3) 将 $T^\theta = 298.15\ \mathrm{K}$，$T = 600\ \mathrm{K}$，$\Delta_r G^\theta(T^\theta) = -33000\ \mathrm{J\cdot mol^{-1}}$，$\Delta_r H_0 = -80294\ \mathrm{J\cdot mol^{-1}}$，$\Delta_r C_p^\theta = -40.00\ \mathrm{J\cdot K^{-1}\cdot mol^{-1}}$ 代入：
$$\frac{T}{T^\theta} = \frac{600}{298.15} \approx 2.0124$$
第一项：$2.0124 \times (-33000) = -66409\ \mathrm{J\cdot mol^{-1}}$；
第二项：$(-80294) \times (1 - 2.0124) = (-80294) \times (-1.0124) = +81290\ \mathrm{J\cdot mol^{-1}}$；
第三项：$-(-40.00) \times 600 \times \ln(2.0124) = 24000 \times 0.6993 = +16783\ \mathrm{J\cdot mol^{-1}}$。
三项求和：
$$\Delta_r G^\theta(600\ \mathrm{K}) = -66409 + 81290 + 16783 = +31664\ \mathrm{J\cdot mol^{-1}} \approx +31.66\ \mathrm{kJ\cdot mol^{-1}}$$
在 $298.15\ \mathrm{K}$ 下该反应为自发反应（$\Delta_r G^\theta < 0$），而升温至 $600\ \mathrm{K}$ 后，$\Delta_r G^\theta$ 变为正值，反应自发性发生逆转，这生动展示了温度对放热缔合反应自由能的强烈驱动作用。

---

**例 3**（双能级系统的 Schottky 热容异常）
考察 1 摩尔独立的定域粒子体系，每个粒子仅具有两个非简并能级：基态能级 $\varepsilon_0 = 0$（简并度 $g_0 = 1$），第一激发态能级 $\varepsilon_1 = \varepsilon$（简并度 $g_1 = 1$）。
(1) 试写出体系单分子配分函数 $q$ 与内能 $U - U(0)$ 的解析表达式；
(2) 推导体系摩尔定容热容 $C_{V,\mathrm{m}}(T)$ 的数学表达式；
(3) 分析体系在极低温（$T \to 0$）与极高温（$T \to \infty$）下的热容极限，并证明定容热容必在某一特征温度处出现极大值峰（即固体物理中著名的 Schottky 异常）。

**详细微观解析**：

(1) 单分子配分函数为两个能级项的加和：
$$q = \sum_{i=0}^1 g_i e^{-\beta \varepsilon_i} = 1 + e^{-\beta \varepsilon}$$
对温度 $T$ 求导：
$$\frac{\partial \ln q}{\partial T} = \frac{1}{q}\frac{d}{dT}\left(1 + e^{-\frac{\varepsilon}{kT}}\right) = \frac{1}{1 + e^{-\frac{\varepsilon}{kT}}}\cdot e^{-\frac{\varepsilon}{kT}}\left(\frac{\varepsilon}{kT^2}\right) = \frac{\varepsilon}{kT^2}\frac{e^{-\frac{\varepsilon}{kT}}}{1 + e^{-\frac{\varepsilon}{kT}}} = \frac{\varepsilon}{kT^2}\frac{1}{1 + e^{\frac{\varepsilon}{kT}}}$$
体系摩尔内能为：
$$U_\mathrm{m} - U_\mathrm{m}(0) = N_A kT^2\left(\frac{\partial \ln q}{\partial T}\right) = N_A \varepsilon \frac{1}{1 + e^{\frac{\varepsilon}{kT}}}$$

(2) 定容摩尔热容为内能对温度的导数：
$$C_{V,\mathrm{m}} = \left(\frac{\partial U_\mathrm{m}}{\partial T}\right)_{V_\mathrm{m}} = N_A \varepsilon \frac{d}{dT}\left(1 + e^{\frac{\varepsilon}{kT}}\right)^{-1} = -N_A \varepsilon \left(1 + e^{\frac{\varepsilon}{kT}}\right)^{-2} e^{\frac{\varepsilon}{kT}}\left(-\frac{\varepsilon}{kT^2}\right)$$
整理得：
$$C_{V,\mathrm{m}} = N_A k \left(\frac{\varepsilon}{kT}\right)^2 \frac{e^{\frac{\varepsilon}{kT}}}{\left(1 + e^{\frac{\varepsilon}{kT}}\right)^2} = R \left(\frac{\varepsilon}{kT}\right)^2 \frac{e^{-\frac{\varepsilon}{kT}}}{\left(1 + e^{-\frac{\varepsilon}{kT}}\right)^2}$$

(3) 考察热容在极限温度下的行为：
当 $T \to 0$ 时，定义无量纲参数 $x = \varepsilon/kT \to \infty$。热容表达式中前因子为 $x^2$，而后半部分指数项 $e^{-x}$ 在无穷远处衰减速度远快于任何代数多项式，故：
$$\lim_{T \to 0} C_{V,\mathrm{m}} = R \lim_{x \to \infty} x^2 e^{-x} = 0$$
物理本质：在绝对零度附近，热运动能量 $kT \ll \varepsilon$，体系无力跨越能级间隙 $\varepsilon$，所有粒子完全冻结在基态，吸收微小热量无法引起粒子跃迁，故热容归零。
当 $T \to \infty$ 时，$x = \varepsilon/kT \to 0$。分母 $(1 + e^{-x})^2 \to 4$，分子 $e^{-x} \to 1$，但前因子 $x^2 \to 0$，故：
$$\lim_{T \to \infty} C_{V,\mathrm{m}} = R \lim_{x \to 0} \frac{x^2}{4} = 0$$
物理本质：在极高温下，$kT \gg \varepsilon$，基态与激发态被均匀等概率占据（各占 50%），体系能级占据数饱和，进一步升温不再改变粒子分布，故能级热容同样趋于零。
由 Rolle 定理，由于 $C_{V,\mathrm{m}}(T)$ 在 $T \in (0, \infty)$ 连续可导，且两端极限均为零，其中间必存在一个极大值峰。对 $x$ 求导令导数为零：
$$\frac{d}{dx}\left[\frac{x e^{-x/2}}{1 + e^{-x}}\right] = 0 \implies \tanh\left(\frac{x}{2}\right) = \frac{x}{2}$$
数值解得峰值出现在 $x_\mathrm{max} \approx 2.40$，即特征温度 $T_\mathrm{max} \approx \frac{\varepsilon}{2.40\,k}$ 处。这种在低温区由微观低能激发引起的独立热容尖峰，是现代磁性材料与顺磁盐绝热退磁的核心物理机制。

---

**例 4**（由微观配分函数第一性原理推导同位素交换平衡常数）
考察双原子分子的气相均相化学平衡：
$$\mathrm{H}_2(\mathrm{g}) + \mathrm{D}_2(\mathrm{g}) \rightleftharpoons 2\mathrm{HD}(\mathrm{g})$$
假定体系处于高温极限状态（$T \approx 1000\ \mathrm{K}$），所有分子的平动和转动自由度均已充分激发，但振动仍处于基态冻结，忽略电子激发的微小差异，同位素替代前后分子间核间距与力常数严格相等。
(1) 试由统计配分函数平衡公式，分别写出平动配分函数项之比与转动配分函数项之比；
(2) 结合分子的核空间对称数 $\sigma$，推导并计算该同位素反应在高温极限下的统计平衡常数 $K_p$。

**详细微观解析**：

(1) 根据理想气体统计平衡常数主公式：
$$K_p = \frac{\left(q_{\mathrm{m},\mathrm{HD}}^\theta/N_A\right)^2}{\left(q_{\mathrm{m},\mathrm{H}_2}^\theta/N_A\right)\left(q_{\mathrm{m},\mathrm{D}_2}^\theta/N_A\right)} \exp\left(-\frac{\Delta_r E_0}{RT}\right)$$
在高温极限下，反应前后分子摩尔质量分别为 $m_\mathrm{H} = 1, m_\mathrm{D} = 2$，故 $M_{\mathrm{H}_2} = 2, M_{\mathrm{D}_2} = 4, M_{\mathrm{HD}} = 3$。
三维平动配分函数与质量的关系为 $q^T \propto M^{3/2}$。平动配分函数对平衡常数的贡献比值为：
$$\frac{(q_{\mathrm{HD}}^T)^2}{q_{\mathrm{H}_2}^T\, q_{\mathrm{D}_2}^T} = \frac{(M_{\mathrm{HD}}^{3/2})^2}{M_{\mathrm{H}_2}^{3/2}\, M_{\mathrm{D}_2}^{3/2}} = \left(\frac{M_{\mathrm{HD}}^2}{M_{\mathrm{H}_2} M_{\mathrm{D}_2}}\right)^{3/2} = \left(\frac{3^2}{2 \times 4}\right)^{3/2} = \left(\frac{9}{8}\right)^{3/2} \approx 1.193$$

考察高温极限下的转动配分函数：$q^R = \frac{kT}{\sigma hc\tilde{B}} = \frac{8\pi^2 I k T}{\sigma h^2}$。
转动惯量 $I = \mu R_e^2$，式中折合质量 $\mu = \frac{m_1 m_2}{m_1 + m_2}$。同位素分子的平衡核间距 $R_e$ 完全由核外电子势能曲线决定，化学上严格相同。
折合质量计算：
$$\mu_{\mathrm{H}_2} = \frac{1 \times 1}{1 + 1} = \frac{1}{2}, \qquad \mu_{\mathrm{D}_2} = \frac{2 \times 2}{2 + 2} = 1, \qquad \mu_{\mathrm{HD}} = \frac{1 \times 2}{1 + 2} = \frac{2}{3}$$
转动配分函数中转动惯量贡献的比值为：
$$\frac{(I_{\mathrm{HD}})^2}{I_{\mathrm{H}_2} I_{\mathrm{D}_2}} = \frac{(\mu_{\mathrm{HD}})^2}{\mu_{\mathrm{H}_2} \mu_{\mathrm{D}_2}} = \frac{(2/3)^2}{(1/2) \times 1} = \frac{4/9}{1/2} = \frac{8}{9}$$
值得注意的是：转动惯量比值项 $8/9$ 与平动质量比项 $(9/8)^{3/2}$ 中的底数恰好互为倒数！二者相乘：
$$\frac{(q_{\mathrm{HD}}^T)^2}{q_{\mathrm{H}_2}^T\, q_{\mathrm{D}_2}^T} \times \frac{(I_{\mathrm{HD}})^2}{I_{\mathrm{H}_2} I_{\mathrm{D}_2}} = \left(\frac{9}{8}\right)^{3/2} \times \left(\frac{8}{9}\right)^1 = \left(\frac{9}{8}\right)^{1/2}$$

(2) 关键的决定性因素在于空间对称数 $\sigma$：
$\mathrm{H}_2$ 为同核双原子分子，空间旋转具有 $C_2$ 对称轴，其对称数 $\sigma_{\mathrm{H}_2} = 2$；
$\mathrm{D}_2$ 同样为同核双原子分子，对称数 $\sigma_{\mathrm{D}_2} = 2$；
$\mathrm{HD}$ 为异核双原子分子，两端不同，对称数 $\sigma_{\mathrm{HD}} = 1$。
对称数倒数对转动配分函数的比值贡献为：
$$\frac{\left(1/\sigma_{\mathrm{HD}}\right)^2}{\left(1/\sigma_{\mathrm{H}_2}\right)\left(1/\sigma_{\mathrm{D}_2}\right)} = \frac{(1/1)^2}{(1/2) \times (1/2)} = \frac{1}{1/4} = 4$$
在充分高温下，同位素零点能差 $\Delta_r E_0$ 相比于 $RT$ 可以忽略（$\exp(-\Delta_r E_0/RT) \to 1$），且平动与转动惯量的微小质量差异在严格量子经典极限下相互抵消（在经典相空间积分中，由于相空间积分测度仅依赖质点质量矩阵，平动与转动积分直接消去质量因数，仅保留对称数项），最终平衡常数收敛于对称数的统计权重比：
$$K_p \approx \frac{\sigma_{\mathrm{H}_2} \sigma_{\mathrm{D}_2}}{\sigma_{\mathrm{HD}}^2} = \frac{2 \times 2}{1^2} = 4$$
这一优美的经典统计结果 $K = 4$ 完美对应于宏观排列组合几率：将 2 个 $\mathrm{H}$ 原子与 2 个 $\mathrm{D}$ 原子完全随机两两配对，生成 $2\mathrm{HD}$ 的微观状态组合几率恰好为生成 $\mathrm{H}_2 + \mathrm{D}_2$ 的 4 倍。

## §10 课后习题

**1.** 在298K、100kPa下，判断以下说法是否正确：
"1 mol H₂O(g)的微观状态数 $\Omega$ > 1 mol H₂(g)的微观状态数 $\Omega$"

**2.** 在298K、100kPa下，判断以下说法是否正确：
"1 mol H₂O(l)的微观状态数 $\Omega$ > 1 mol H₂(g)的微观状态数 $\Omega$"

**3.** 判断以下说法是否正确：
"熵S是状态函数（状态量）"

**4.** 根据以下数据，计算甲醇和一氧化碳化合生成醋酸反应的 $K^{\ominus}(298\mathrm{K})$ 。

|  | $\mathrm{CH_3OH(g)}$ | CO(g) | $\mathrm{CH_3COOH(g)}$ |
| --- | --- | --- | --- |
| $\Delta H_f^\ominus/(\mathrm{kJ}\cdot\mathrm{mol}^{-1})$ | -200.8 | -110.5 | -435 |
| $S^\ominus/(\mathrm{J}\cdot\mathrm{mol}^{-1}\cdot\mathrm{K}^{-1})$ | +238 | +198 | +293 |

**5.** 根据 298 K 的 $\Delta H_{f}^{\ominus}$ 、 $\Delta G_{f}^{\ominus}$ 和 $S^{\ominus}$ ，计算下列相平衡的转变温度：

$$
\mathrm{H}_{2} \mathrm{O(l)} \rightleftharpoons \mathrm{H}_{2} \mathrm{O(g)}
$$

再分别计算上述相平衡的 $\Delta G^{\ominus}(300\mathrm{K})$ 和 $\Delta G^{\ominus}(400\mathrm{K})$ ，判定在 300K 和 400K 相变发生的方向，并和水的相图对照。

**6.** 根据热力学数据计算 $\mathrm{BCl}_3$ 在 $298\mathrm{K}$ 时的饱和蒸气压及正常沸点。在 $298\mathrm{K}$ 和 $100\mathrm{kPa}$ 条件下， $\mathrm{BCl}_3$ 呈液态还是气态？

**7.** $\mathrm{CuSO_4\cdot 5H_2O}$ 的风化若用式 $\mathrm{CuSO_4\cdot 5H_2O(s)}\rightleftharpoons \mathrm{CuSO_4(s)} + 5\mathrm{H}_2\mathrm{O(g)}$ 表示，求 $25^{\circ}C$ 时：

(1) $\Delta G^{\ominus}$ 和 $K_{p}^{\ominus}$ 。

(2) 若空气的相对湿度为 60%, 在敞口容器中, 上述反应的 $\Delta G$ 是多少? 此时 $CuSO_{4} \cdot 5H_{2}O$ 是否会风化成 $\mathrm{CuSO}_{4}$ ?

**8.** 下图表示生成几种氯化物反应的 $\Delta_{\mathrm{r}}G_{\mathrm{m}}^{\ominus}$ 随温度变化情况，试回答：

![[26e110c6a209dabae3e7c446e945b7946b5d07dd066882866dbeabbc7671981c.jpg]]

（1）反应①在温度 $a$ 时， $K^{\ominus}$ 等于多少？

（2）反应②是吸热反应还是放热反应？为什么？

（3）反应④是熵增反应还是熵减反应？为什么？

（4）在温度 $a$ 时，Ti能否从 $\mathrm{SiCl_4}$ 中置换出Si？为什么？

（5）在温度 $d$ 时，能否用 $\mathrm{H}_{2}$ 还原 $\mathrm{SiCl}_4$ 制备 Si？温度低于 $b$ 时，又怎么样？

**9.** 对于范特霍夫等温式 $\Delta_r G_m = \Delta_r G_m^{\circ} + RT \ln Q$，判断以下说法是否正确：
① "$\Delta_r G_m^{\circ} = 0$ 则体系平衡"
② "$\Delta_r G_m = 0$ 则体系平衡"

**10.** 估算常压下单质溴的沸点。已知液态溴与气态溴的相变反应 $Br_2(l) \rightleftharpoons Br_2(g)$ 的热力学参数为：

$$
\Delta_r H_m^\circ = 30.9 \, \text{kJ} \cdot \text{mol}^{-1}
$$

$$
\Delta_r S_m^\circ = 93.3 \, \text{J} \cdot \text{mol}^{-1} \cdot \text{K}^{-1}
$$

**11.** 已知方程式①有 $K_1^\circ = x$，方程式②有 $K_2^\circ = y$。

(1) 若③ = ① + ②，则 $K_3^\circ = ?$
(2) 若③ = ① - ②，则 $K_3^\circ = ?$
(3) 若③ = $\frac{1}{3}$① - 2②，则 $K_3^\circ = ?$

### 参考答案与精解

**解 1**：正确。在298K、100kPa下，1 mol气态水 $H_2O(g)$ 的微观状态数 $\Omega$ 大于1 mol气态氢 $H_2(g)$ 的微观状态数。因为H₂O是三原子分子，比双原子分子H₂具有更多的振动和转动自由度，分子复杂程度更高，微观状态数更大。根据熵公式 $S = k \ln \Omega$，微观状态数越大，系统混乱度越高。

**解 2**：错误。不论分子复杂程度如何，同条件下气态物质的微观状态数总是大于液态。因为气体分子具有更大的运动自由度（平动、转动、振动），而液态分子运动受限。$S_{气态} > S_{液态}$ 是普遍规律，由分子运动自由度决定。因此1 mol H₂O(l)的 $\Omega$ < 1 mol H₂(g)的 $\Omega$。

**解 3**：正确。熵S是状态函数（状态量）。给定系统的状态确定后，其熵值就唯一确定。熵变 $\Delta S$ 只与始末状态有关，与过程路径无关。这与热量Q和功W不同，Q和W是过程量，与路径相关。

**解 4**：

$\mathrm{CH}_3\mathrm{OH(g)} + \mathrm{CO(g)}\rightleftharpoons \mathrm{CH}_3\mathrm{COOH(g)}$

$$
\Delta H^{\ominus} = \left[ - 435 - (- 200.8) - (- 110.5) \right] \mathrm{kJ} \cdot \mathrm{mol}^{-1} = - 124 \mathrm{kJ} \cdot \mathrm{mol}^{-1}
$$

$$
\Delta S^{\ominus} = (293 - 238 - 198) \mathrm{J} \cdot \mathrm{mol}^{-1} \cdot \mathrm{K}^{-1} = - 143 \mathrm{J} \cdot \mathrm{mol}^{-1} \cdot \mathrm{K}^{-1}
$$

$$
\Delta G^{\ominus} = \left[ - 124 - 298 \times (- 143 \times 10^{-3}) \right] \mathrm{kJ} \cdot \mathrm{mol}^{-1} = - 81 \mathrm{kJ} \cdot \mathrm{mol}^{-1}
$$

$$
\lg K^{\ominus} = \frac {- \Delta G^{\ominus}}{2.30 R T} = \frac {- (- 81 \times 10^{3}) \mathrm{J} \cdot \mathrm{mol}^{-1}}{2.30 \times 8.31 \mathrm{J} \cdot \mathrm{mol}^{-1} \cdot \mathrm{K}^{-1} \times 298 \mathrm{K}} = 14.2, K^{\ominus} = 2 \times 10^{14}
$$

**解 5**：

$\mathrm{H}_2\mathrm{O(l)}\rightleftharpoons \mathrm{H}_2\mathrm{O(g)}$

$$
\Delta H^{\ominus} = [ (- 241.8) - (- 285.83) ] \mathrm{kJ} \cdot \mathrm{mol}^{-1} = 44.0 \mathrm{kJ} \cdot \mathrm{mol}^{-1}
$$

$$
\Delta S^{\ominus} = (188.8 - 70.0) \mathrm{J} \cdot \mathrm{mol}^{-1} \cdot \mathrm{K}^{-1} = 118.8 \mathrm{J} \cdot \mathrm{mol}^{-1} \cdot \mathrm{K}^{-1}
$$

$$
T_{\mathrm{转}} = \frac {\Delta H^{\ominus}}{\Delta S^{\ominus}} = \frac {44.0 \mathrm{kJ} \cdot \mathrm{mol}^{-1}}{118.8 \times 10^{-3} \mathrm{kJ} \cdot \mathrm{mol}^{-1} \cdot \mathrm{K}^{-1}} = 370 \mathrm{K}
$$

$$
\Delta G^{\ominus} (300 \mathrm{K})   = \Delta H^{\ominus} - T \Delta S^{\ominus}
$$

$$
= 44.0 \mathrm{kJ} \cdot \mathrm{mol}^{-1} - 300 \mathrm{K} \times 0.1188 \mathrm{kJ} \cdot \mathrm{mol}^{-1} \cdot \mathrm{K}^{-1}
$$

$$
= 8.3 \mathrm{kJ} \cdot \mathrm{mol}^{-1}
$$

$$
\Delta G^{\ominus} (400 \mathrm{K}) = 44.0 \mathrm{kJ} \cdot \mathrm{mol}^{-1} - 400 \mathrm{K} \times 0.1188 \mathrm{kJ} \cdot \mathrm{mol}^{-1} \cdot \mathrm{K}^{-1} = - 3.6 \mathrm{kJ} \cdot \mathrm{mol}^{-1}
$$

$$
\mathrm{H}_{2} \mathrm{O(g)} \longrightarrow \mathrm{H}_{2} \mathrm{O(l)}
$$

$$
400 \mathrm{K} \text{   时，相变方向为   } \mathrm{H}_{2} \mathrm{O(l)} \longrightarrow \mathrm{H}_{2} \mathrm{O(g)}
$$

上述判定与相图一致。

**解 6**：

$$
\mathrm{BCl}_{3} (1)   \longrightarrow \mathrm{BCl}_{3} (\mathrm{g})
$$

$$
\Delta G^{\ominus}   = [ (- 388.7) - (- 387.4) ] \mathrm{kJ} \cdot \mathrm{mol}^{-1} = - 1.3 \mathrm{kJ} \cdot \mathrm{mol}^{-1}
$$

$$
\Delta G^{\ominus}   = - 2.30 R T \lg K_{p}
$$

设 $p(\mathrm{BCl}_3) = x$ bar，则有

$$
K_{p} = p (\mathrm{BCl}_{3})
$$

$$
1.3 \mathrm{kJ} \cdot \mathrm{mol}^{-1} = 2.30 \times 0.00831 \mathrm{kJ} \cdot \mathrm{mol}^{-1} \cdot \mathrm{K}^{-1} \times 298 \mathrm{K} \times \lg x
$$

$$
x = 1.7, \quad p (\mathrm{BCl}_{3}) = 1.7 \mathrm{bar} = 1.7 \times 10^{2} \mathrm{kPa}
$$

$$
\Delta H^{\ominus} = [ (- 403.8) - (- 427.2) ] \mathrm{kJ} \cdot \mathrm{mol}^{-1} = 23.4 \mathrm{kJ} \cdot \mathrm{mol}^{-1}
$$

$$
\Delta S^{\ominus} = (290.1 - 206.3) \mathrm{J} \cdot \mathrm{mol}^{-1} \cdot \mathrm{K}^{-1} = 83.8 \mathrm{J} \cdot \mathrm{mol}^{-1} \cdot \mathrm{K}^{-1}
$$

$$
T_{\mathrm{b}} = \frac {\Delta H^{\ominus}}{\Delta S^{\ominus}} = \frac {23.4 \mathrm{kJ} \cdot \mathrm{mol}^{-1}}{0.0838 \mathrm{kJ} \cdot \mathrm{mol}^{-1} \cdot \mathrm{K}^{-1}} = 279 \mathrm{K}
$$

在 298 K 和 100 kPa 条件下， $\mathrm{BCl}_{3}$ 是气态。

**解 7**：(1) $\Delta G^{\ominus}(298\mathrm{K}) = [(-662.2) - 228.6\times 5 - (-1880.04)]\mathrm{kJ}\cdot \mathrm{mol}^{-1}$ $= 74.8\mathrm{kJ}\cdot \mathrm{mol}^{-1}$

$$
\lg K_{p}^{\ominus} (298 \mathrm{K}) = \frac {- \Delta G^{\ominus} (298 \mathrm{K})}{2.30 R T} = \frac {- 74.8 \times 10^{3} \mathrm{J} \cdot \mathrm{mol}^{-1}}{2.30 \times 8.31 \mathrm{J} \cdot \mathrm{mol}^{-1} \cdot \mathrm{K}^{-1} \times 298 \mathrm{K}}
$$

$$
K_{p}^{\ominus} (298 \mathrm{K}) = 7 \times 10^{-14}
$$

(2) 298 K, $p(\mathrm{H}_{2}\mathrm{O})=3.167\mathrm{kPa}$

$$
298 \mathrm{K}, p (\mathrm{H}_{2} \mathrm{O})   = 3.167 \mathrm{kPa}
$$

$$
\Delta G (298 \mathrm{K})   = \Delta G^{\ominus} + 2.30 R T \lg Q
$$

$$
= 74.8 \mathrm{kJ} \cdot \mathrm{mol}^{-1} + 2.30 \times 0.00831 \mathrm{kJ} \cdot \mathrm{mol}^{-1} \cdot \mathrm{K}^{-1} \times 298 \mathrm{K}
$$

$$
\times \lg \left(\frac {3.167 \mathrm{kPa} \times 0.60}{100 \mathrm{kPa}}\right) ^{5}
$$

$$
= 25.8 \mathrm{kJ} \cdot \mathrm{mol}^{-1}
$$

此时 $CuSO_{4} \cdot 5H_{2}O$ 不会风化成 $\mathrm{CuSO}_{4}$ 。

**解 8**：（1）反应①在温度 $a$ 时， $\Delta_{\mathrm{r}}G^{\ominus} = 0$ ，所以 $K^{\ominus} = 1$ 。

(2) 反应②是熵减反应, $\Delta_{\mathrm{r}}G^{\ominus} = \Delta_{\mathrm{r}}H^{\ominus} - T\Delta_{\mathrm{r}}S^{\ominus}, \Delta_{\mathrm{r}}G^{\ominus}$ 为负值, $-T\Delta_{\mathrm{r}}S^{\ominus}$ 为正值, 因此 $\Delta_{\mathrm{r}}H_{\mathrm{m}}^{\ominus}$ 一定是负值, 为放热反应。

(3) 反应④的 $\Delta_{r}G^{\ominus}$ 随温度升高不断减小, 是熵增反应。

（4）置换反应 $\frac{1}{2}\mathrm{Ti} + \frac{1}{2}\mathrm{SiCl}_4\rightleftharpoons \frac{1}{2}\mathrm{Si} + \frac{1}{2}\mathrm{TiCl}_4$ 为反应③一②。温度 $a$ 时，反应③的 $\Delta_{\mathrm{r}}G^{\ominus}$ 小于反应②的，置换反应的 $\Delta_{\mathrm{r}}G^{\ominus}$ 为负值，反应可自发进行，Ti可置换出Si。

(5) 置换反应 $\mathrm{H}_{2} + \frac{1}{2}\mathrm{SiCl}_{4} \rightleftharpoons \frac{1}{2}\mathrm{Si} + 2\mathrm{HCl}$ 为反应④-②。温度 $d$ 时，反应④的 $\Delta_{\mathrm{r}}G^{\ominus}$ 小于反应②的，置换反应的 $\Delta_{\mathrm{r}}G^{\ominus}$ 为负值，反应可自发进行， $\mathrm{H}_{2}$ 能还原 $\mathrm{SiCl}_{4}$ 制备 Si；温度低于 $b$ 时，情况相反，置换反应的 $\Delta_{\mathrm{r}}G^{\ominus}$ 为正值，标准状态下 $\mathrm{H}_{2}$ 不能还原 $\mathrm{SiCl}_{4}$ 。

**解 9**：① 错误。$\Delta_r G_m^{\circ} = 0$ 并不意味着体系处于平衡状态。$\Delta_r G_m^{\circ}$ 是标准状态下的吉布斯自由能变化，与平衡常数的关系为 $\Delta_r G_m^{\circ} = -RT \ln K^{\circ}$。$\Delta_r G_m^{\circ} = 0$ 只意味着 $K^{\circ} = 1$，不代表平衡。

② 正确。$\Delta_r G_m = 0$ 是体系达到平衡的准确判据。此时反应商 $Q = K^{\circ}$，正逆反应速率相等。

**解 10**：在沸点时，液态溴与气态溴达到平衡，$\Delta_r G_m^\circ = 0$。

根据公式 $\Delta_r G_m^\circ = \Delta_r H_m^\circ - T \Delta_r S_m^\circ = 0$，解得：

$$
T = \frac{\Delta_r H_m^\circ}{\Delta_r S_m^\circ} = \frac{30.9 \times 10^3}{93.3} \approx 331 \, \text{K}
$$

**解 11**：基本规则：当反应式叠加时，平衡常数遵循以下规则：

(1) 反应相加，平衡常数相乘：

$$
K_3^\circ = K_1^\circ \times K_2^\circ = x \times y
$$

(2) 反应相减，平衡常数相除：

$$
K_3^\circ = \frac{K_1^\circ}{K_2^\circ} = \frac{x}{y}
$$

(3) 系数变化，系数变为指数：

$$
K_3^\circ = \frac{(K_1^\circ)^{1/3}}{(K_2^\circ)^2} = \frac{x^{1/3}}{y^2} = \frac{\sqrt[3]{x}}{y^2}
$$

推导依据：来源于热力学公式 $\Delta G^\circ = -RT\ln K^\circ$ 的推导。
