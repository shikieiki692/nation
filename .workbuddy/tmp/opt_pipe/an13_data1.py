# -*- coding: utf-8 -*-
"""卷 XIII 解析数据（第 1~5 题）。"""

A1 = {
 1: dict(
   考点=r"热化学（反应焓与 $Q_p/Q_V$）· van't Hoff 等压方程与平衡移动 · 电解的分解电压与超电势"
        r"（知识点：〈化学热力学〉、〈Gibbs自由能〉、〈化学平衡〉、〈电极过程热力学〉）",
   思路=r"先由生成焓算 $\Delta_rH_m^\ominus$，再借 $Q_p-Q_V=\Delta\nu RT$ 换算；判断温度影响看 $\Delta_rH$ 的符号"
        r"（或 $\Delta_rG=\Delta_rH-T\Delta_rS$ 的变号温度）；电解效率是「理论分解电压／实际电压」与电能利用率的乘积；"
        r"末问做能量衡算，注意 $\mathrm{H_2}$ 燃烧产物按**气态水**计。",
   步骤=[
     ("1-1", "6 分",
      r"$\mathrm{CH_3OH(g)}=\mathrm{CO(g)}+2\mathrm{H_2(g)}$。"
      r"$\Delta_rH_m^\ominus=\Delta_{\mathrm f}H_m^\ominus(\mathrm{CO})-\Delta_{\mathrm f}H_m^\ominus(\mathrm{CH_3OH})"
      r"=(-110.5)-(-200.7)=+90.2\ \mathrm{kJ\cdot mol^{-1}}$，即恒压热效应 $Q_{p,m}=+90.2\ \mathrm{kJ\cdot mol^{-1}}$（吸热）。"
      r"气相 $\Delta\nu=(1+2)-1=2$，体积功 $W=-p\Delta V=-\Delta\nu RT=-2\times8.314\times298.15\times10^{-3}"
      r"=-4.96\ \mathrm{kJ\cdot mol^{-1}}$。故恒容热效应 "
      r"$Q_{V,m}=\Delta_rU_m^\ominus=\Delta_rH_m^\ominus+W=90.2-4.96=85.2\ \mathrm{kJ\cdot mol^{-1}}$。"),
     ("1-2", "3 分",
      r"$\Delta_rH_m^\ominus=+90.2\ \mathrm{kJ\cdot mol^{-1}}>0$（吸热）。由 van't Hoff 等压方程 "
      r"$\mathrm{d}\ln K^\ominus/\mathrm{d}T=\Delta_rH_m^\ominus/(RT^2)>0$，$K^\ominus$ 随温度升高而增大，"
      r"故**升温有利于甲醇裂解**。亦可由 $\Delta_rG_m^\ominus=\Delta_{\mathrm f}G_m^\ominus(\mathrm{CO})"
      r"-\Delta_{\mathrm f}G_m^\ominus(\mathrm{CH_3OH})=(-137.2)-(-162.0)=+24.8\ \mathrm{kJ\cdot mol^{-1}}$"
      r"（298 K 不自发）与 $\Delta_rS_m^\ominus=(\Delta_rH_m^\ominus-\Delta_rG_m^\ominus)/T\approx+219\ \mathrm{J\cdot K^{-1}\cdot mol^{-1}}$"
      r"（气体分子数增多、熵增）看出：升温使 $-T\Delta_rS$ 项增大，$T>\Delta_rH_m^\ominus/\Delta_rS_m^\ominus\approx411\ \mathrm{K}$ 时 $\Delta_rG_m^\ominus<0$。"),
     ("1-3", "6 分",
      r"$\mathrm{H_2O(l)}=\mathrm{H_2(g)}+\frac12\mathrm{O_2(g)}$，"
      r"$\Delta_rG_m^\ominus=-\Delta_{\mathrm f}G_m^\ominus(\mathrm{H_2O,l})=+237.1\ \mathrm{kJ\cdot mol^{-1}}$。"
      r"理论分解电压 $E^\ominus=\Delta_rG_m^\ominus/(nF)=237.1\times10^{3}/(2\times96485)=1.229\ \mathrm{V}$。"
      r"实际电解电压 $U=E^\ominus+\eta(\mathrm{O_2})+\eta(\mathrm{H_2})=1.229+0.9+1.5=3.63\approx3.6\ \mathrm{V}$。"
      r"电解质与导线损失 35% 电能 ⇒ 电能利用率 65%。"
      r"故电解效率 $=(E^\ominus/U)\times65\%=(1.229/3.6)\times0.65\approx22\%$。"),
     ("1-4", "6 分",
      r"① 1 mol 甲醇裂解吸热 $90.2\ \mathrm{kJ}$。"
      r"② 供热用 $\mathrm{H_2}$ 燃烧，产物按气态水计：$\mathrm{H_2(g)}+\frac12\mathrm{O_2(g)}=\mathrm{H_2O(g)}$，"
      r"$\Delta_rH_m^\ominus=\Delta_{\mathrm f}H_m^\ominus(\mathrm{H_2O,l})+\Delta_{\mathrm{vap}}H_m^\ominus"
      r"=-285.8+44.0=-241.8\ \mathrm{kJ\cdot mol^{-1}}$。"
      r"③ 需 $\mathrm{H_2}$ 量 $n=90.2/(241.8\times0.70)=0.533\ \mathrm{mol}$。"
      r"④ 1 mol 甲醇裂解生成 2 mol $\mathrm{H_2}$，扣除供热自耗 0.533 mol 后净得 1.467 mol。"
      r"⑤ 产氢效率 $=1.467/2\approx73\%$。"),
    ],
   易错=r"① $Q_p$ 与 $Q_V$ 相差 $\Delta\nu RT$，$\Delta\nu$ **只计气态物质**；"
        r"② 判断温度影响须用 $\Delta_rH$ 的符号，不能一律说「升温有利」；"
        r"③ 电解效率里「电压效率」与「电能效率」要相乘，且超电势使实际电压**升高**；"
        r"④ 产氢效率要扣除燃烧自耗的 $\mathrm{H_2}$，且产物须按气态水计（用液态水会高估供热量、结论偏大）。",
 ),
 2: dict(
   考点=r"基尔霍夫定律（$\Delta H$ 随 $T$ 变化）· 相平衡与熔化热力学 · 活度与活度系数"
        r"（知识点：〈相变热力学〉、〈Gibbs自由能〉、〈化学势〉、〈Clapeyron方程〉）",
   思路=r"$\Delta C_p$ 为常数 ⇒ $\Delta_{\mathrm{mel}}H$ 是 $T$ 的一次函数；正常熔点处固液平衡 ⇒ $\Delta G=0$ ⇒ "
        r"$\Delta S=\Delta H/T$；再由 $\Delta G=\Delta H-T\Delta S$ 求 $K^\ominus$；最后用 $K^\ominus=a(\mathrm{Fe,l})=\gamma x$ 反求活度系数。",
   步骤=[
     ("2-1", "2 分",
      r"由基尔霍夫定律 $\mathrm{d}(\Delta_{\mathrm{mel}}H_m)/\mathrm{d}T=\Delta C_{p,m}$（常数）⇒ "
      r"$\Delta_{\mathrm{mel}}H_m(T)=\Delta C_{p,m}T+I$。代入 $T=1808\ \mathrm{K}$、$\Delta_{\mathrm{mel}}H_m=15355\ \mathrm{J\cdot mol^{-1}}$ "
      r"得 $I=15355-1.255\times1808=13086\ \mathrm{J\cdot mol^{-1}}$，"
      r"故 $\Delta_{\mathrm{mel}}H_m=(1.255\,T/\mathrm{K}+13086)\ \mathrm{J\cdot mol^{-1}}$。"),
     ("2-2", "6 分",
      r"① 正常熔点 1808 K 处固液两相平衡，$\Delta_{\mathrm{mel}}G_m=0$ ⇒ "
      r"$\Delta_{\mathrm{mel}}S_m(1808\ \mathrm{K})=\Delta_{\mathrm{mel}}H_m/1808=15355/1808=8.494\ \mathrm{J\cdot K^{-1}\cdot mol^{-1}}$。"
      r"② $\Delta C_{p,m}$ 为常数时熵变按 $\Delta C_p\ln(T_2/T_1)$ 修正："
      r"$\Delta_{\mathrm{mel}}S_m(1673\ \mathrm{K})=8.494+1.255\ln(1673/1808)=8.494-0.097=8.397\ \mathrm{J\cdot K^{-1}\cdot mol^{-1}}$。"
      r"③ $\Delta_{\mathrm{mel}}H_m(1673\ \mathrm{K})=1.255\times1673+13086=15186\ \mathrm{J\cdot mol^{-1}}$。"
      r"④ $\Delta_{\mathrm{mel}}G_m^\ominus=\Delta_{\mathrm{mel}}H_m-T\Delta_{\mathrm{mel}}S_m=15186-1673\times8.397=1138\ \mathrm{J\cdot mol^{-1}}$。"
      r"⑤ $K^\ominus=\exp(-\Delta_{\mathrm{mel}}G_m^\ominus/RT)=\exp(-1138/(8.314\times1673))=0.921$。"
      r"（亦可直接用 Gibbs-Helmholtz 不定积分式：$\Delta G/T=-\int(\Delta H/T^2)\mathrm{d}T+I'=-1.255\ln T+13086/T+I'$，"
      r"由 $T=1808\ \mathrm{K}$、$\Delta G=0$ 定出 $I'=2.175$，再代 1673 K 求 $\Delta G$，结果一致。）"
      r"（校勘：源答案把 $\Delta_{\mathrm{mel}}S_m(1808\ \mathrm{K})$ 印作 8.5924，与 $15355/1808=8.494$ 不符，系笔误；"
      r"本卷已按更正值计算，$K^\ominus$ 相应由 0.931 更正为 0.921。）"),
     ("2-3", "4 分",
      r"该温度下 $\delta\text{-}\mathrm{Fe(s)}$ 与硫化铁熔体（$x(\mathrm{Fe})=0.87$）两相平衡。"
      r"以纯液态 Fe 为标准态、纯固相 $\delta\text{-}\mathrm{Fe(s)}$ 活度为 1，故 $K^\ominus=a(\mathrm{Fe,l})=\gamma x$。"
      r"于是 $\gamma=K^\ominus/x=0.921/0.87=1.06\approx1.1$。"),
    ],
   易错=r"① $\Delta_{\mathrm{mel}}S$ 不能一律用 $\Delta H/T$ 求，须计入 $\Delta C_p$ 项；"
        r"② $K^\ominus$ 与活度的关系依赖「纯液态 Fe 为标准态」，别把摩尔分数当活度；"
        r"③ $\gamma>1$ 表示熔体中 Fe 的活度大于其摩尔分数（对拉乌尔定律正偏差）。",
 ),
 3: dict(
   考点=r"Clausius-Clapeyron 方程外推饱和蒸气压 · 拉乌尔定律与理想溶液沸点 · Margules 方程与活度系数 · 恒沸物判据"
        r"（知识点：〈Clapeyron方程〉、〈化学势〉、〈相图与相平衡〉）",
   思路=r"以 40 ℃ 的 $p^*$ 为基准，用 C-C 方程把 $p^*$ 外推到任意 $T$；理想溶液用 $\sum x_ip_i^*=p$ 求沸点；"
        r"非理想溶液把 $p_i^*$ 换成 $\gamma_i x_i p_i^*$；恒沸（$y_A=x_A$）配合 Margules 式可解析求 $x_A$。",
   步骤=[
     ("3-1-1", "5 分",
      r"温度 $T$ 下各纯组分的饱和蒸气压由 C-C 方程外推（$\Delta_{\mathrm{vap}}H_m$ 视为常数）："
      r"$\ln[p^*(T)/p^*(313.15\ \mathrm{K})]=(\Delta_{\mathrm{vap}}H_m/R)(1/313.15-1/T)$。"
      r"理想溶液正常沸点处 $p=1\ \mathrm{atm}$：$0.75p_A^*(T)+0.25p_B^*(T)=1$，解得 $T=330.4\ \mathrm{K}$。"
      r"此时 $p_A=0.565\ \mathrm{bar}$、$p_B=0.435\ \mathrm{bar}$，气相丙酮摩尔分数 $y_A=p_A/(p_A+p_B)=0.565$。"),
     ("3-1-2", "6 分",
      r"已知**气相**组成为 $y_A=0.75$，设沸点为 $T$、液相组成为 $x_A$。由 "
      r"$p_A=x_Ap_A^*(T)=y_Ap$、$p_B=(1-x_A)p_B^*(T)=(1-y_A)p$ 及 $p=p_A+p_B$，两式相除消去 $p$："
      r"$\frac{x_Ap_A^*(T)}{(1-x_A)p_B^*(T)}=\frac{0.75}{0.25}=3$，联立总压条件解得 $T=334.5\ \mathrm{K}$、$x_A=0.874$。"),
     ("3-2", "5 分",
      r"由 Margules 方程（$A=0.90$，$x_A=0.75$、$x_B=0.25$）："
      r"$\gamma_A=\exp(Ax_B^2)=\exp(0.90\times0.0625)=1.058$，$\gamma_B=\exp(Ax_A^2)=\exp(0.90\times0.5625)=1.659$。"
      r"非理想溶液的沸点条件为 $x_A\gamma_Ap_A^*(T)+x_B\gamma_Bp_B^*(T)=1$，解得 $T=321.9\ \mathrm{K}$。"
      r"（$\gamma_A,\gamma_B$ 均大于 1 ⇒ 对拉乌尔定律正偏差 ⇒ 沸点低于理想溶液的 330.4 K，与该体系能形成最低恒沸物一致。）"),
     ("3-3-1", "8 分",
      r"恒沸时气相与液相组成相同，即 $y_A=x_A$。由 "
      r"$y_A=\frac{\gamma_Ax_Ap_A^*}{\gamma_Ax_Ap_A^*+\gamma_Bx_Bp_B^*}=x_A$，约去 $x_A$ 整理得 $\gamma_Ap_A^*=\gamma_Bp_B^*$。"
      r"代入 Margules 式并取对数：$A(x_B^2-x_A^2)=\ln(p_B^*/p_A^*)$；再以 $x_B=1-x_A$ 代入得 "
      r"$A(1-2x_A)=\ln(p_B^*/p_A^*)$，故 $x_A=\frac12-\frac{1}{2A}\ln\frac{p_B^*}{p_A^*}$。"),
     ("3-3-2", "3 分",
      r"代入 $A=0.90$ 与 40 ℃ 的 $p_B^*/p_A^*=0.98/0.42=2.333$（$\ln=0.847$）："
      r"$x_A=0.5-0.847/(2\times0.90)=0.0293$。"
      r"恒沸压力 $p=\gamma_Ax_Ap_A^*+\gamma_Bx_Bp_B^*=0.981\ \mathrm{atm}$。"),
    ],
   易错=r"① C-C 外推必须用**同一物质**的 $\Delta_{\mathrm{vap}}H$（A、B 数值不同，勿混用）；"
        r"② 恒沸判据是 $\gamma_Ap_A^*=\gamma_Bp_B^*$（相等的是活度系数与纯蒸气压之积），**不是** $p_A^*=p_B^*$；"
        r"③ Margules 式中 $x_B^2$ 与 $x_A^2$ 极易写反。",
 ),
 4: dict(
   考点=r"沉淀溶解平衡与配位平衡的耦合（$K=K_{sp}\beta$）· 物料/电荷/溶解守恒联立 · 弱碱溶液的 $[\mathrm{OH^-}]$"
        r"（知识点：〈多重平衡〉、〈化学平衡计算〉、〈稳定常数〉、〈溶解度〉、〈pH〉）",
   思路=r"多重平衡题的通用套路是「先列守恒、再用平衡常数把各形态表为 $[\mathrm{NH_3}]$ 的函数」，最后解一元方程；"
        r"注意题问的「氨水浓度」指**总氨**（游离 + 铵 + 配位氨）。",
   步骤=[
     ("4-1", "8 分",
      r"设 1 L 1.00 mol/L 氨水溶解 AgCl 达饱和、溶解量 $s\ \mathrm{mol/L}$，则 $[\mathrm{Cl^-}]=s$。"
      r"① 溶解守恒：$[\mathrm{Cl^-}]=[\mathrm{Ag^+}]+[\mathrm{Ag(NH_3)^+}]+[\mathrm{Ag(NH_3)_2^+}]"
      r"=[\mathrm{Ag^+}](1+\beta_1[\mathrm{NH_3}]+\beta_2[\mathrm{NH_3}]^2)$。"
      r"② 溶度积：$[\mathrm{Ag^+}][\mathrm{Cl^-}]=K_{sp}$；联立①②得 "
      r"$[\mathrm{Ag^+}]=\sqrt{K_{sp}/(1+\beta_1[\mathrm{NH_3}]+\beta_2[\mathrm{NH_3}]^2)}$，$s=K_{sp}/[\mathrm{Ag^+}]$。"
      r"③ 氨的物料守恒：$1.00=[\mathrm{NH_3}]+[\mathrm{NH_4^+}]+[\mathrm{Ag(NH_3)^+}]+2[\mathrm{Ag(NH_3)_2^+}]$。"
      r"④ 电荷守恒结合氨水的弱碱水解得 $[\mathrm{H^+}]=\sqrt{K_w/(1+[\mathrm{NH_3}]/K_a)}$，$K_a=K_w/K_b$。"
      r"联立解得 $[\mathrm{NH_3}]=0.794\ \mathrm{mol/L}$、$s=0.101\ \mathrm{mol/L}$，"
      r"故 $m=sM(\mathrm{AgCl})=0.101\times143.4=14.5\ \mathrm{g}$。"),
     ("4-2", "6 分",
      r"完全溶解 1.50 g AgCl 于 2.0 L ⇒ $[\mathrm{Cl^-}]=1.50/(143.4\times2.0)=5.233\times10^{-3}\ \mathrm{mol/L}$。"
      r"由 $K_{sp}$ 得 $[\mathrm{Ag^+}]=K_{sp}/[\mathrm{Cl^-}]=3.398\times10^{-8}\ \mathrm{mol/L}$"
      r"（远小于 $[\mathrm{Cl^-}]$，说明银主要以氨配合物形态存在）。"
      r"代入溶解守恒解得 $[\mathrm{NH_3}]=0.0416\ \mathrm{mol/L}$；再由电荷守恒（$[\mathrm{H^+}]$ 可忽略）"
      r"$[\mathrm{NH_4^+}]+[\mathrm{H^+}]=[\mathrm{OH^-}]$ 得 $[\mathrm{NH_4^+}]=8.70\times10^{-4}\ \mathrm{mol/L}$。"
      r"故所需氨水**最低总浓度** $c=[\mathrm{NH_3}]+[\mathrm{NH_4^+}]+[\mathrm{Ag(NH_3)^+}]+2[\mathrm{Ag(NH_3)_2^+}]=0.0529\ \mathrm{mol/L}$。"),
    ],
   易错=r"① 问「氨水的浓度」要算**总氨**（游离 + 铵 + 配位氨），只报游离 $[\mathrm{NH_3}]$ 会偏小近一半；"
        r"② $[\mathrm{Ag^+}]$ 的表达式要含 $\beta_2[\mathrm{NH_3}]^2$ 项；"
        r"③ 4-2 的 0.0529 mol/L 是**最低**浓度（其按单位体积的 AgCl 量少于 4-1），勿与 4-1 的 1.00 mol/L 条件混淆。",
 ),
 5: dict(
   考点=r"Latimer 图的电子数加权平均 · 歧化/反歧化判据 · $\Delta_rG^\ominus=-nFE^\ominus$ 与 $K^\ominus$ 的换算 · Nernst 方程（pH 影响）"
        r"（知识点：〈Latimer图〉、〈Frost图〉、〈Nernst方程〉、〈Gibbs自由能〉）",
   思路=r"不相邻电对的电位必须按电子数加权（$E=\sum n_iE_i/\sum n_i$），不可取算术平均；"
        r"某物种是否歧化看「右侧电位 − 左侧电位」（$>0$ 则歧化）；"
        r"电势差与 $\Delta G$、$K$ 之间用 $\Delta_rG^\ominus=-nFE^\ominus$、$K^\ominus=\exp(-\Delta_rG^\ominus/RT)$ 贯通；"
        r"含 $\mathrm{H^+}$ 的电极其电位随 pH 由 Nernst 方程决定。",
   步骤=[
     ("5-1", "3 分",
      r"电势图：$\mathrm{VO_2^+}\to\mathrm{VO^{2+}}\to\mathrm{V^{3+}}$，对应电位 $1.0\ \mathrm{V}$、$0.337\ \mathrm{V}$。"
      r"对中间物种 $\mathrm{VO^{2+}}$，右侧还原电位 $E(\mathrm{VO^{2+}/V^{3+}})=0.337\ \mathrm{V}$ "
      r"**小于**左侧 $E(\mathrm{VO_2^+/VO^{2+}})=1.0\ \mathrm{V}$，不满足歧化判据（右大于左），故 $\mathrm{VO^{2+}}$ 不易歧化。"
      r"定量核对：歧化反应 $2\mathrm{VO^{2+}}\to\mathrm{VO_2^+}+\mathrm{V^{3+}}$，"
      r"$\Delta_rG_m^\ominus=-nF(E_{右}-E_{左})=-1\times96485\times(0.337-1.0)=+63.97\ \mathrm{kJ\cdot mol^{-1}}>0$，正向非自发，结论一致。"),
     ("5-2-1", "2 分",
      r"由「连续电势对电子的加权平均」关系：$\frac{1\times1.0+1\times0.337+1\times E_X}{3}=0.361$，"
      r"解得 $E_X=3\times0.361-1.337=-0.254\ \mathrm{V}$，即 $E^\ominus(\mathrm{V^{3+}/V^{2+}})=-0.254\ \mathrm{V}$。"),
     ("5-2-2", "3 分",
      r"**不能。** $\mathrm{V^{2+}}$ 在水溶液中会被 $\mathrm{H^+}$ 氧化："
      r"$\mathrm{V^{2+}}+\mathrm{H^+}\to\mathrm{V^{3+}}+\frac12\mathrm{H_2}$。"
      r"该电池 $E^\ominus=E^\ominus(\mathrm{H^+/H_2})-E^\ominus(\mathrm{V^{3+}/V^{2+}})=0-(-0.254)=+0.254\ \mathrm{V}>0$，"
      r"$\Delta_rG_m^\ominus=-nFE^\ominus=-1\times96485\times0.254=-24.51\ \mathrm{kJ\cdot mol^{-1}}<0$，反应自发。"
      r"故 pH = 0 时 $\mathrm{V^{2+}}$ 会不断被 $\mathrm{H^+}$ 氧化放出 $\mathrm{H_2}$，"
      r"**无法得到热力学稳定的 $\mathrm{V^{2+}}$ 水溶液**。"),
     ("5-3-1", "3 分",
      r"$2\mathrm{VO^{2+}}+\mathrm{H_2}+2\mathrm{H^+}\to2\mathrm{V^{3+}}+2\mathrm{H_2O}$（H₂ 系数取 1，故耦合 $2\mathrm{VO^{2+}}$，$n=2$）。"
      r"$E^\ominus=E^\ominus(\mathrm{VO^{2+}/V^{3+}})-E^\ominus(\mathrm{H^+/H_2})=0.337-0=0.337\ \mathrm{V}$，"
      r"$\Delta_rG_m^\ominus=-nFE^\ominus=-2\times96485\times0.337=-65.03\ \mathrm{kJ\cdot mol^{-1}}$，"
      r"$K^\ominus=\exp(-\Delta_rG_m^\ominus/RT)=\exp(65030/(8.314\times298))=2.51\times10^{11}$。"),
     ("5-3-2", "4 分",
      r"设 $\mathrm{VO^{2+}}$ 的转化率为 $\alpha$，初始浓度为 $c$，平衡时 "
      r"$[\mathrm{VO^{2+}}]=c(1-\alpha)$、$[\mathrm{V^{3+}}]=c\alpha$，$\mathrm{H_2}$ 分压为 $1.0\ \mathrm{bar}=p^\ominus$。"
      r"$K^\ominus=\frac{[\mathrm{V^{3+}}]^2}{[\mathrm{VO^{2+}}]^2[\mathrm{H^+}]^2\cdot(p_{\mathrm{H_2}}/p^\ominus)}"
      r"=\frac{\alpha^2}{(1-\alpha)^2(10^{-\mathrm{pH}})^2}=2.51\times10^{11}$。"
      r"代入 pH = 4.15：$\frac{\alpha}{1-\alpha}=\sqrt{2.51\times10^{11}\times10^{-8.30}}=35.5$，解得 $\alpha=0.973\approx0.97$（近完全还原）。"),
     ("5-3-3", "4 分",
      r"要求 $\alpha\ge99.5\%$，即 $\frac{\alpha}{1-\alpha}\ge199$。由 $K^\ominus=\left(\frac{\alpha}{1-\alpha}\right)^2\times10^{2\mathrm{pH}}$："
      r"$10^{2\mathrm{pH}}=\frac{2.51\times10^{11}}{199^2}=6.34\times10^{6}$，$2\mathrm{pH}=6.80$。"
      r"即需 $\mathrm{pH}\le3.40$，故溶液**最大允许 pH 为 3.40**"
      r"（pH 越低、消耗 $\mathrm{H^+}$ 越彻底，还原越完全，与 Le Châtelier 原理一致）。"),
     ("5-3-4", "5 分",
      r"由 $E^\ominus=-\frac{\Delta_rH_m^\ominus}{nF}+\frac{\Delta_rS_m^\ominus}{nF}T$ 知斜率 "
      r"$\mathrm{d}E^\ominus/\mathrm{d}T=\Delta_rS_m^\ominus/(nF)$，故 "
      r"$\Delta_rS_m^\ominus=nF(-1.75\times10^{-3})=2\times96485\times(-1.75\times10^{-3})=-337.7\ \mathrm{J\cdot K^{-1}\cdot mol^{-1}}$。"
      r"又 $\Delta_rS_m^\ominus=2S_m^\ominus(\mathrm{V^{3+}})+2S_m^\ominus(\mathrm{H_2O,l})-2S_m^\ominus(\mathrm{VO^{2+}})"
      r"-S_m^\ominus(\mathrm{H_2})-2S_m^\ominus(\mathrm{H^+})$，代入数据得 "
      r"$-337.7=2(-307.0)+2(70.0)-2S_m^\ominus(\mathrm{VO^{2+}})-130.7-0$，"
      r"解得 $S_m^\ominus(\mathrm{VO^{2+}})=-133.5\ \mathrm{J\cdot K^{-1}\cdot mol^{-1}}$。"
      r"再由 $\Delta_rH_m^\ominus=\Delta_rG_m^\ominus+T\Delta_rS_m^\ominus=-65.03\times10^{3}+298\times(-337.7)"
      r"=-1.657\times10^{5}\ \mathrm{J\cdot mol^{-1}}\approx-165.7\ \mathrm{kJ\cdot mol^{-1}}$。"),
    ],
   易错=r"① 歧化判据是「右侧电位大于左侧电位」时中间物种歧化，别把方向弄反；"
        r"② 计算电池电动势时 $E_{cell}=E_{阴极}-E_{阳极}$：$\mathrm{H^+/H_2}$ 作阴极时是 $0-E(\mathrm{V^{3+}/V^{2+}})=+0.254\ \mathrm{V}$，**不是** $-0.254\ \mathrm{V}$；"
        r"③ $K^\ominus$ 表达式中 $\mathrm{H_2}$ 是气体，须写成 $p(\mathrm{H_2})/p^\ominus$ 而非浓度；"
        r"④ $\mathrm{d}E^\ominus/\mathrm{d}T$ 与 $\Delta_rS$ 同号，注意 $n=2$。",
 ),
}
