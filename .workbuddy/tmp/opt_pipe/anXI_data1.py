# -*- coding: utf-8 -*-
"""卷 XI 解析数据（第 1~6 题）。答案区图片已逐张目检（读图结果写入解析）。"""

A1 = {
 1: dict(
   考点=r"配位化学与 **18 电子规则（EAN）** · 由质量分数定化学式 · 夹心（$\eta^5$-Cp）配位与三明治型组装 · "
        r"$\mathrm N_2$ 桥联的 IR 判据"
        r"（知识点：〈配位化学〉、〈18电子规则〉、〈金属有机化学基础〉、〈原子簇化学〉）",
   思路=r"先用四方锥配位 ＋ 中性 BDI 推 A 的价态与价电子数；再由 `ω(Re)` 反推 B／D／E 的组成，"
        r"并用「三重旋转轴 ⇒ Re 个数为 3」「N=N 红外 ⇒ $\mathrm N_2$ 桥联」两条硬信号定 C／D／E。",
   步骤=[
     ("1-1", "—",
      r"A 为四方锥、配体为中性 BDI（＋ Cp 与端基 O）⇒ **Re 为 +5 价**；价电子数 $5+2\times(2+1)+... =14\ \mathrm e$"
      r"（含 Cp 的 6 与 BDI 的 4 等）⇒ **不满足 18 电子规则**。"),
     ("1-2", "—",
      r"由 $\omega(\mathrm{Re})=20.46\%$ 且 B 含 Sn、Cl：$M=\frac{186.2}{0.2046}=910.0$ ⇒ "
      r"$\mathbf B=\mathrm{[CpRe(O)(BDI)][SnCl_3]}$（阳离子含 Re=O、阴离子为 $\mathrm{SnCl_3^-}$）；"
      r"过量 Na 把 $\mathrm{SnCl_3^-}$ 还原为 Sn、并把 Re=O 还原 ⇒ $\mathbf C=\mathrm{Na[CpRe(BDI)]}$"
      r"（阴离子 $[\mathrm{CpRe(BDI)}]^-$，Re 最外层 16e）。"),
     ("1-3", "—",
      r"由「同种配体视作等大球 + 三重旋转轴」⇒ Re 个数为 **3**；$\frac{3\times186.2}{24.98\%}=2236.2$，"
      r"减去 3 个 $[\mathrm{CpRe(BDI)}]$ 与 Gd 后余 71.7，恰为 1 个 THF ⇒ "
      r"$\mathbf D=\mathrm{Gd(THF)[CpRe(BDI)]_3}$。"),
     ("1-4", "—",
      r"氮气保护下多得的 E 破坏了三重旋转轴、且出现 **N=N 红外** ⇒ 只有 1 个 N=N ⇒ 它**桥联 Gd 与 Re**"
      r"（原本桥联的 Cp 环不再与 Gd 配位）；再由 $\omega(\mathrm{Re})=23.91\%$ 定其组成并画出结构。"),
    ],
   易错=r"① 1-2 的推算要**先由 ω 定 $M$**（$910.0$）再拆 $\mathrm{SnCl_3^-}$＋阳离子，不能臆造；"
        r"② B→C 有**两处还原**（$\mathrm{SnCl_3^-}\rightarrow\mathrm{Sn}$ 与 Re=O 被还原），漏一处即组成错；"
        r"③ 「三重旋转轴」是定 Re 个数为 3 的关键，勿忽略；"
        r"④ E 只含 **1 个 N=N**，故必为 Gd–N≡N–Re **桥联**（而非端基 $\mathrm N_2$）。",
 ),
 2: dict(
   考点=r"砷的元素化学与化学史 · 雄黄 $\mathrm{As_4S_4}$ 的**异构体**（As 环境数）· 雌黄在碳酸钠中的溶解 · "
        r"巴黎绿与 $\mathrm{AsO_2^-}$ 三聚体 · 马氏试砷法（$\mathrm{AsH_3}$）· 氧化还原配平"
        r"（知识点：〈元素化学〉、〈氮族元素〉、〈主族元素化学〉、〈含氧酸〉）",
   思路=r"2-1/2-2 由史料关键词（「赤乳」＝升华凝华；锡还原雌黄雄黄）作答；2-3 由「As 环境数」区分两种异构体；"
        r"2-4/2-5/2-6 全部按**守恒 ＋ 价态**配平。",
   步骤=[
     ("2-1", "—",
      r"「取雌黄雄黄烧下……此器皆生赤乳」＝**升华与凝华**（物理变化）。"),
     ("2-2", "—",
      r"锡还原雄黄、雌黄得单质砷：$\mathrm{As_4S_4}+2\mathrm{Sn}=2\mathrm{SnS_2}+4\mathrm{As}$。"),
     ("2-3", "—",
      r"**A**：所有 As 化学环境相同（$D_{2d}$ 型 $\mathrm{As_4S_4}$，As 与 S 交替成笼）；"
      r"**B**：有**三种**环境的 As（另一种 $\mathrm{As_4S_4}$ 异构体，As 的成键环境分三类）——分别画出两种笼形结构。"),
     ("2-4", "—",
      r"$\mathrm{As_2S_3}+3\mathrm{Na_2CO_3}=\mathrm{Na_3AsO_3}+\mathrm{Na_3AsS_3}+3\mathrm{CO_2}$。"),
     ("2-5", "—",
      r"巴黎绿中 $\mathrm{AsO_2^-}$ 以**三聚体**存在：由 3 个 As 与 6 个 O 组成六元环 $[\mathrm{As_3O_6}]^{3-}$"
      r"（每个 As 上、下各带一个端基 O）。"),
     ("2-6", "—",
      r"$\mathrm{As_2O_3}+6\mathrm{Zn}+12\mathrm{HCl}=2\mathrm{AsH_3}+6\mathrm{ZnCl_2}+3\mathrm{H_2O}$；"
      r"$2\mathrm{AsH_3}=2\mathrm{As}+3\mathrm{H_2}$；"
      r"$2\mathrm{As}+5\mathrm{ClO^-}+6\mathrm{OH^-}=2\mathrm{AsO_4^{3-}}+5\mathrm{Cl^-}+3\mathrm{H_2O}$。"),
    ],
   易错=r"① 2-1 是**物理**变化（升华/凝华），勿写成化学反应；"
        r"② $\mathrm{As_4S_4}$ 有两种异构体，判据是**As 的化学环境数**（1 种 vs 3 种）；"
        r"③ 2-6 中碱性 $\mathrm{NaClO}$ 只溶解 As、不溶 Sb —— 这是**马氏试砷法**区分二者的关键；"
        r"④ 2-4 产物是 $\mathrm{Na_3AsO_3}$（亚砷酸盐）与 $\mathrm{Na_3AsS_3}$（硫代亚砷酸盐），勿写成砷酸盐。",
 ),
 3: dict(
   考点=r"硫的小杂环化合物（$\mathrm{PhCS_3Cl}$）· **共振式与形式电荷** · 自由基偶联与脱硫机理 · "
        r"由摩尔质量定化学式"
        r"（知识点：〈元素化学〉、〈氧族元素〉、〈共振结构〉、〈离域π键〉）",
   思路=r"1.1 由 1:1 反应与化学式（Cl 为抗衡离子）定 P＝$\mathrm{PhCS_3Cl}$；1.4 由「摩尔质量 306」与"
        r"「三步自由基机理」定 R，再按「**形成自由基 → 偶联 → 分解脱硫**」写机理。",
   步骤=[
     ("1-1", "—",
      r"P 的化学式＝$\mathrm{PhCS_3Cl}$；阳离子 $\mathrm{PhCS_3^+}$ 的稳定共振式（**形式电荷尽量少**）："
      r"把正电荷落在 S 上，画出含 $\mathrm{S{-}S}$ 与 $\mathrm{C{=}S}$ 的若干等价共振式。"),
     ("1-2", "—",
      r"Q 的阳离子为 **$\mathrm{Ph_2C_2S_3^{2+}}$**（五元环：2 个带 Ph 的 C 与 3 个 S，每个 S 均与 C 相连），"
      r"抗衡离子为 $2\mathrm{Cl^-}$。"),
     ("1-3", "—",
      r"反应 1：$2\mathrm{PhCS_3Cl}\rightarrow\mathrm{Ph_2C_2S_3Cl_2}+3\mathrm S$；"
      r"反应 2：$\mathrm{Zn(PhCS_2)_2}+6\mathrm{AsF_5}\rightarrow\mathrm{PhC_2S_3(AsF_6)_2}+\mathrm S+\mathrm{Zn(AsF_6)_2}+2\mathrm{AsF_3}$。"),
     ("1-4", "—",
      r"R 的化学式＝$\mathrm{(PhCS_2)_2}$（$M\approx306$）；机理："
      r"$2\mathrm{PhCS_3Cl}+\mathrm{SO_2}\rightarrow2\mathrm{PhCS_3\!\cdot}+\mathrm{SO_2Cl_2}$；"
      r"$2\mathrm{PhCS_3\!\cdot}\rightarrow(\mathrm{PhCS_3})_2\rightarrow\mathrm{PhC(S){-}S{-}S(S)CPh}+2\mathrm S$ ⇒ 偶联物**脱硫**得 R。"),
    ],
   易错=r"① P 的 Cl 是**抗衡离子**，勿并入共价骨架；"
        r"② 共振式要给**形式电荷最小的稳定式**（电荷尽量落在 S 上）；"
        r"③ 1.4 的三步是「生成自由基 S → 偶联 → 分解（脱硫）」，缺一步即机理不完整；"
        r"④ 反应 2 的计量：$\mathrm{AsF_5}$ 既是氟化剂又是 Lewis 酸，产物含 $\mathrm{AsF_3}$ 与 $\mathrm{AsF_6^-}$。",
 ),
 4: dict(
   考点=r"碘量法（$\mathrm{Cr_2O_7^{2-}}\sim3\mathrm{I_2}\sim6\mathrm{S_2O_3^{2-}}$）· 硫代硫酸钠的酸分解 · "
        r"Winkler 法测溶解氧 · 由 Von Weimarn 经验式估**分散度**"
        r"（知识点：〈碘量法〉、〈氧化还原滴定〉、〈滴定分析基本原理〉、〈误差〉）",
   思路=r"4-1 由计量关系定标定式；4-2 是 $\mathrm S_2O_3^{2-}$ 在**酸性**下的歧化/分解；"
        r"4-3 用 Winkler 法的电子守恒（$1\ \mathrm{O_2}\sim4\ \mathrm{S_2O_3^{2-}}$）；4-4 由**硫原子守恒**算 $\mathrm S_8$ 浓度再算分散度。",
   步骤=[
     ("4-1", "—",
      r"$\mathrm{Cr_2O_7^{2-}}+14\mathrm{H^+}+6\mathrm{I^-}\rightarrow2\mathrm{Cr^{3+}}+3\mathrm{I_2}+7\mathrm{H_2O}$；"
      r"$\mathrm{I_2}+2\mathrm{S_2O_3^{2-}}\rightarrow2\mathrm{I^-}+\mathrm{S_4O_6^{2-}}$；"
      r"由 $\mathrm{K_2Cr_2O_7}\sim3\mathrm{I_2}\sim6\mathrm{Na_2S_2O_3}$ 得 $c=\frac{6\times0.12/294.18}{V/1000}=\frac{2.45}{V}\ \mathrm{mol/L}$。"),
     ("4-2", "—",
      r"$\mathrm{S_2O_3^{2-}}+2\mathrm{H^+}\rightarrow\mathrm S\downarrow+\mathrm{SO_2}\uparrow+\mathrm{H_2O}$（淡黄色沉淀即 S，酸性气体即 $\mathrm{SO_2}$）。"),
     ("4-3-1", "—",
      r"$2\mathrm{Mn^{2+}}+\mathrm{O_2}+4\mathrm{OH^-}\rightarrow2\mathrm{MnO(OH)_2}\downarrow$；"
      r"$\mathrm{MnO(OH)_2}+2\mathrm{I^-}+4\mathrm{H^+}\rightarrow\mathrm{Mn^{2+}}+\mathrm{I_2}+3\mathrm{H_2O}$。"),
     ("4-3-2", "—",
      r"电子守恒 $1\ \mathrm{O_2}\sim4\ \mathrm{S_2O_3^{2-}}$：$n(\mathrm{O_2})=\frac{0.01000\times8.50\times10^{-3}}{4}=2.125\times10^{-5}\ \mathrm{mol}$ ⇒ "
      r"$\mathrm{DO}=\frac{2.125\times10^{-5}\times32.00\times10^{3}}{0.10000}=6.80\ \mathrm{mg/L}$。"),
     ("4-4", "—",
      r"过量 $\mathrm S_2O_3^{2-}$ 全部转化后硫原子总浓度 $=\frac{2\times(25-2.45)}{100+25}=0.36\ \mathrm{mol/L}$；"
      r"$[\mathrm{S_8}]=0.36\times17\%\times90\%/8=6.9\times10^{-3}\ \mathrm{mol/L}$（密度≈纯水 ⇒ 同值 mol/kg）；"
      r"分散度 $=K\frac{C_Q-s}{s}=\frac{6.9\times10^{-3}-1.9\times10^{-8}}{1.9\times10^{-8}}=3.6\times10^{5}$。"),
    ],
   易错=r"① 4-3 的电子守恒是 $1\ \mathrm{O_2}\sim4\ \mathrm{Na_2S_2O_3}$，勿写成 $1:1$；"
        r"② 4-2 必须用**酸性**条件（若写中性不分解）；"
        r"③ 4-4 的硫原子总浓度要按**稀释后总体积**（$100+25$）算，且 $\mathrm S_2O_3^{2-}$ 含 **2** 个 S；"
        r"④ 分散度公式中 $s$ 是溶解度（$1.9\times10^{-8}$），分子分母单位一致。",
 ),
 5: dict(
   考点=r"Bohr 氢原子模型与 **Rydberg 常数**的推导（折合质量 ＋ 角动量量子化）· 氢原子光谱的极限行为 · "
        r"Hund 规则的能量来源（库仑排斥 ＋ **交换稳定化**）"
        r"（知识点：〈Bohr模型计算〉、〈原子结构〉、〈电子排布〉、〈洪特规则〉、〈量子数〉）",
   思路=r"5-1 严格按题给四步提示走：**折合质量 → 库仑力＝向心力 → 角动量量子化 → E=T+V → 归并系数得 R**；"
        r"5-2 用**自旋多重度 $2S+1$** 填表，再由「库仑排斥小、交换稳定化大者能量低」解释 Hund 规则。",
   步骤=[
     ("5-1-1", "—",
      r"折合质量 $\frac1\mu=\frac1{m_e}+\frac1{m_n}$；由 $\frac{\mu v^2}{r}=\frac{Ze^2}{4\pi\varepsilon_0r^2}$ 与 $\mu vr=n\hbar$ 消 $v$ 得 "
      r"$r_n=\frac{4\pi\varepsilon_0\hbar^2n^2}{\mu Ze^2}$；代入 $E_n=T+V=-\frac{\mu Z^2e^4}{2h^2(4\pi\varepsilon_0)^2n^2}$；"
      r"与 $\Delta E=R(\frac1{n_1^2}-\frac1{n_h^2})$ 对照 ⇒ **$R=\frac{\mu e^4}{8\varepsilon_0^2h^2}$**（$Z=1$）。"),
     ("5-1-2", "—",
      r"选 **abc**：电子能量与 $n^2$ 成反比 ⇒ $n$ 小时能级疏、$n$ 大时能级密；$n\to\infty$ 时 $E\to0$（电子**更高能**、"
      r"且已不再属于该原子）。"),
     ("5-2-1", "—",
      r"按 Hund 规则填 np 轨道（$1\to6$ 个电子）：未成对电子数 $1,2,3,2,1,0$，自旋多重度 $2,3,4,3,2,1$。"),
     ("5-2-2", "—",
      r"$\mathrm p^2$ 的三种排布：① 两电子同占一个轨道（自旋反平行）；② 两电子分占两轨道、**自旋平行**；"
      r"③ 两电子分占两轨道、**自旋反平行**。"),
     ("5-2-3", "—",
      r"能量高低 **(3)＜(2)＜(1)**：分占不同轨道可减小库仑排斥，且**自旋平行**带来**交换稳定化** ⇒ "
      r"体系倾向最大总自旋（Hund 规则）。"),
    ],
   易错=r"① 推导中必须用**折合质量** $\mu$（核非无穷重）；"
        r"② $E_n$ 的常数归并要保留 $\hbar=\frac h{2\pi}$ 的换算（即 $2(4\pi\varepsilon_0)^2\hbar^2=8\varepsilon_0^2h^2$）；"
        r"③ 5-1-2 的 $n\to\infty$ 意味着**电离**（$E\to0$ 而电子自由），勿答「能量最低」；"
        r"④ $\mathrm p^2$ 的三种排布要含**两种平行/反平行分占**，漏一排布即错。",
 ),
 6: dict(
   考点=r"元素推断（「失踪元素」Tc）· $\mathrm{Tc_2O_7}$ 与含氟酸的转化 · 阴阳离子均具 **$C_4$ 轴**的离子化合物 · "
        r"核素衰变（$\beta^-$、$\gamma$）与医用核素 $^{99\mathrm m}\mathrm{Tc}$ · 放射性药物配体"
        r"（知识点：〈元素化学〉、〈核反应〉、〈过渡金属通性〉、〈配位化学〉、〈稀有气体化合物〉）",
   思路=r"由「门捷列夫预言的失踪元素、1937 年人工合成」锁 **Tc**；再由「$\mathrm{Tc_2O_7}$＋HF/$\mathrm{XeF_6}$/$\mathrm{KrF_2}$ 逐步氟化」"
        r"定 A~E；G 由「$C_4$ 轴」＋ $\omega(\mathrm{Tc})=49.1\%$ 定阳离子组成；核素部分用**守恒**与衰变类型作答。",
   步骤=[
     ("6-1", "—",
      r"M＝**Tc**；A＝$\mathrm{Tc_2O_7}$、B＝$\mathrm{Tc_2S_7}$、C＝$\mathrm{TcO_3F}$、D＝$\mathrm{TcO_2F_3}$、E＝$\mathrm{TcOF_5}$"
      r"（F 的质量分数依次升高）。"),
     ("6-2", "—",
      r"反应 1：$\mathrm{Tc_2O_7}+2\mathrm{HF}=2\mathrm{TcO_3F}+\mathrm{H_2O}$；"
      r"反应 2：$2\mathrm{TcO_2F_3}+2\mathrm{KrF_2}=2\mathrm{TcOF_5}+\mathrm{O_2}+2\mathrm{Kr}$。"),
     ("6-3", "—",
      r"G 的阴阳离子均具 **$C_4$ 轴**：阳离子为 $\mathrm{[Tc_2O_2F_9]^+}$（$\mathrm{O{=}TcF_4{-}F{-}TcF_4{=}O}$ 型双核）、"
      r"阴离子为 $\mathrm{[Sb_2F_{11}]^-}$（$\mathrm{F{-}SbF_4{-}F{-}SbF_4{-}F}$）⇒ "
      r"$\mathbf G=\mathrm{[Tc_2O_2F_9][Sb_2F_{11}]}$（$\omega(\mathrm{Tc})=\frac{196}{399}=49.1\%$ ✓）。"),
     ("6-4-1", "—",
      r"N＝$^{99}_{42}\mathrm{Mo}$、X＝$^{99}_{43}\mathrm{Tc}$（$\beta^-$ 衰变：质量数不变、原子序数 +1）。"),
     ("6-4-2", "—",
      r"$^{99\mathrm m}\mathrm{Tc}\rightarrow^{99}\mathrm{Tc}$ 为 **$\gamma$ 衰变**（同质异能跃迁，仅释放光子）。"),
     ("6-5-1", "—",
      r"洗脱阶段 $\mathrm{{}^{99}MoO_4^{2-}}$ 衰变得 $\mathrm{{}^{99m}TcO_4^-}$。"),
     ("6-5-2", "—",
      r"按各药盒的配体与电荷/对称性要求画配合物：Cardiolyte（1+，$1:6$）、Myoview（1+，含 3 个镜面）、"
      r"Ceretec（中性，Tc 5 配位且价态与 Myoview 相同）。"),
     ("6-6", "—",
      r"K＝$\mathrm{K_2[BH_3CO_2]}$（B 不与 O 相连）；"
      r"反应 3：$2\mathrm{KOH}+\mathrm{THF\cdot BH_3}+\mathrm{CO}=\mathrm{K_2[BH_3CO_2]}+\mathrm{THF}+\mathrm{H_2O}$。"),
    ],
   易错=r"① 由「失踪元素 ＋ 1937 年合成」定 Tc，**不可**误判为 Re；"
        r"② G 的两离子都要求 $C_4$ 轴 ⇒ 必为**桥联双核**（$\mathrm{[Tc_2O_2F_9]^+}$ / $\mathrm{[Sb_2F_{11}]^-}$），勿写成单核 $\mathrm{[TcOF_4]^+}$；"
        r"③ $\beta^-$ 衰变**质量数不变**、$\gamma$ 衰变只放光子；"
        r"④ 6-6 的产物是 $\mathrm{K_2[BH_3CO_2]}$（2:1 型盐），B 不与 O 相连是定结构的关键。",
 ),
}
