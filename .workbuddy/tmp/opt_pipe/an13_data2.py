# -*- coding: utf-8 -*-
"""卷 XIII 解析数据（第 6~10 题）。"""

A2 = {
 6: dict(
   考点=r"Clausius-Clapeyron 方程求蒸气压 · 拉乌尔定律与泡点/露点 · 理想溶液蒸馏"
        r"（知识点：〈Clapeyron方程〉、〈相图与相平衡〉、〈化学势〉）",
   思路=r"先用 C-C 方程由溴苯正常沸点求 407 K 的 $p_B^*$；再由 9:1 混合物在 407 K 恰好沸腾（$p=101.325\ \mathrm{kPa}$）反解 $p_A^*$；"
        r"之后「出现第一个气泡」按**泡点**（液相组成不变）处理，「剩最后一滴液体」按**露点附近**（气相总组成约等于原投料）处理。",
   步骤=[
     ("6-1", "6 分",
      r"① 由 C-C 方程：$\ln\frac{p_B^*(407\ \mathrm{K})}{101.325\ \mathrm{kPa}}"
      r"=\frac{44500}{8.314}\left(\frac{1}{429}-\frac{1}{407}\right)$，解得 $p_B^*(407\ \mathrm{K})=51.621\ \mathrm{kPa}$。"
      r"② 9 mol A + 1 mol B（$x_A=0.9$）在 407 K 恰好沸腾：$p=p_A^*x_A+p_B^*x_B=101.325\ \mathrm{kPa}$，"
      r"解得 $p_A^*(407\ \mathrm{K})=(101.325-0.1\times51.621)/0.9=106.820\ \mathrm{kPa}$。"
      r"③ $x_A=0.4$ 的液体在 407 K 出现**第一个气泡**时液相组成未变，总压 "
      r"$p_1=0.4\times106.820+0.6\times51.621=73.701\ \mathrm{kPa}$；"
      r"气相组成 $y_A=p_A^*x_A/p_1=42.728/73.701=0.58$，$y_B=0.42$。"),
     ("6-2", "4 分",
      r"继续降压至只剩**最后一滴液体**时，可近似认为气相总组成等于原液相组成（$y_A=0.4$、$y_B=0.6$）。"
      r"该液滴与气相成平衡：$p_A=p_A^*x_A=y_Ap_2$、$p_B=p_B^*x_B=y_Bp_2$，两式相除 "
      r"$\frac{x_A}{x_B}=\frac{y_A}{y_B}\cdot\frac{p_B^*}{p_A^*}=\frac{0.4}{0.6}\times\frac{51.621}{106.820}=0.322$，"
      r"结合 $x_A+x_B=1$ 解得 $x_A=0.244$、$x_B=0.756$；"
      r"$p_2=p_A^*x_A+p_B^*x_B=65.1\ \mathrm{kPa}$（源答案印 65.39 kPa，系将 $x_A$ 舍入为 0.24 后代 $p_B^*x_B$ 所致）。"),
    ],
   易错=r"① 「出现第一个气泡」是**泡点**（液相组成不变），「剩最后一滴液体」是**露点附近**（气相组成约等于原投料组成），两者已知量不同；"
        r"② C-C 方程中的 $\Delta_{\mathrm{vap}}H$ 只能用溴苯自己的 44.5 kJ·mol⁻¹（题给），氯苯的 $p^*$ 靠「恰好沸腾」反解；"
        r"③ 题给标准大气压为 101.325 kPa，勿与 101.3 kPa 混用。",
 ),
 7: dict(
   考点=r"$\Delta_rG^\ominus=\Delta_rH^\ominus-T\Delta_rS^\ominus$ 与 $K^\ominus$ 的换算 · 分压平衡计算（转化率）· 亨利定律与二元弱酸 pH"
        r"（知识点：〈化学平衡计算〉、〈Gibbs自由能〉、〈化学平衡〉、〈pH〉、〈酸碱平衡〉）",
   思路=r"按「热力学量 → $K^\ominus$ → 平衡组成（分压式）」三步走；7-4 是「亨利定律求溶解浓度 + 二元弱酸质子条件求 pH」。",
   步骤=[
     ("7-1", "4 分",
      r"$4\mathrm{NO}+3\mathrm{O_2}+2\mathrm{H_2O}\to4\mathrm{HNO_3}$；$2\mathrm{SO_2}+\mathrm{O_2}+2\mathrm{H_2O}\to2\mathrm{H_2SO_4}$。"),
     ("7-2", "7 分",
      r"$2\mathrm{NO}+\mathrm{O_2}\rightleftharpoons2\mathrm{NO_2}$。"
      r"$\Delta_rH_m^\ominus=2\times33.2-2\times91.3=-116.2\ \mathrm{kJ\cdot mol^{-1}}$；"
      r"$\Delta_rS_m^\ominus=2\times240.1-2\times210.8-205.2=-146.6\ \mathrm{J\cdot K^{-1}\cdot mol^{-1}}$；"
      r"$\Delta_rG_m^\ominus(600\ \mathrm{K})=-116.2-600\times(-0.1466)=-28.2\ \mathrm{kJ\cdot mol^{-1}}$；"
      r"$K^\ominus=\exp(-\Delta_rG_m^\ominus/RT)=\exp(28200/(8.314\times600))=285$。"
      r"设 NO 转化率为 $x$（初始 $n(\mathrm{NO}):n(\mathrm{O_2})=2:1$）：平衡时 $n(\mathrm{NO})=2-2x$、$n(\mathrm{O_2})=1-x$、"
      r"$n(\mathrm{NO_2})=2x$，总量 $3-x$；$\Delta\nu=2-3=-1$，而题给 $p=100\ \mathrm{kPa}=p^\ominus$，故 $K_x=K^\ominus=285$。"
      r"代入 $K_x=\frac{x^2(3-x)}{(1-x)^3}=285$，解得 $x\approx0.83$。"),
     ("7-3", "8 分",
      r"$2\mathrm{SO_2}+\mathrm{O_2}\rightleftharpoons2\mathrm{SO_3}$。"
      r"$\Delta_rH_m^\ominus=2\times(-395.7)-2\times(-296.8)=-197.8\ \mathrm{kJ\cdot mol^{-1}}$；"
      r"$\Delta_rS_m^\ominus=2\times256.8-2\times248.2-205.2=-188.0\ \mathrm{J\cdot K^{-1}\cdot mol^{-1}}$；"
      r"$\Delta_rG_m^\ominus(900\ \mathrm{K})=-197.8-900\times(-0.188)=-28.6\ \mathrm{kJ\cdot mol^{-1}}$；"
      r"$K^\ominus=\exp(28600/(8.314\times900))=45.7$。"
      r"设反应进度 $x\ \mathrm{mol}$（起始 1 mol $\mathrm{SO_2}$ + 1 mol $\mathrm{O_2}$）："
      r"$n(\mathrm{SO_2})=1-2x$、$n(\mathrm{O_2})=1-x$、$n(\mathrm{SO_3})=2x$，总量 $2-x$；"
      r"刚性容器（$V=80\ \mathrm{L}$）中用分压写 $K^\ominus$（$p_i/p^\ominus=n_iRT/(Vp^\ominus)$）："
      r"$K^\ominus=\frac{(2x)^2}{(1-2x)^2(1-x)}\cdot\frac{Vp^\ominus}{RT}=45.7$，解得 $x=0.42$。"
      r"平衡总压 $p=(2-x)RT/V=1.58\times8.314\times900/0.080=1.48\ \mathrm{bar}$。"),
     ("7-4", "7 分",
      r"空气中 $\mathrm{SO_2}$ 峰值浓度 $500\ \mu\mathrm{g/m^3}$ ⇒ 分压 "
      r"$p=\frac{cRT}{M}=\frac{500\times10^{-6}}{64}\times8.314\times298=0.0194\ \mathrm{Pa}=1.915\times10^{-7}\ \mathrm{atm}$。"
      r"由亨利定律（题给 $K=1.36\ \mathrm{mol/(L\cdot atm)}$）："
      r"$c(\mathrm{H_2SO_3})=Kp=1.36\times1.915\times10^{-7}=2.60\times10^{-7}\ \mathrm{mol/L}$。"
      r"质子条件：$[\mathrm{H^+}]=[\mathrm{HSO_3^-}]+2[\mathrm{SO_3^{2-}}]+[\mathrm{OH^-}]$。"
      r"因 $K_{a1}c=3.64\times10^{-9}\gg K_w$，$[\mathrm{OH^-}]$ 可忽略；又 $K_{a2}=6.3\times10^{-8}$ 使第二级电离的贡献远小于第一级，"
      r"故 $[\mathrm{H^+}]\approx\sqrt{K_{a1}c}=\sqrt{1.4\times10^{-2}\times2.60\times10^{-7}}=6.03\times10^{-5}\ \mathrm{mol/L}$，pH $=4.22$。"),
    ],
   易错=r"① $\Delta_rS$ 计算中 $\mathrm{O_2}$ 的 $S^\ominus$ 别漏乘/漏减（按方程系数）；"
        r"② $K^\ominus$ 与 $K_x$ 之间隔着 $(p/p^\ominus)^{\Delta\nu}$——7-2 因 $p=p^\ominus=100\ \mathrm{kPa}$ 恰好相等，"
        r"7-3 因容器体积固定须用分压 $p_i=n_iRT/V$；"
        r"③ 亨利常数单位为 $\mathrm{mol/(L\cdot atm)}$，压力须换算成 atm；"
        r"④ 7-4 的亚硫酸虽是二元弱酸，但 $K_{a2}$ 很小，用 $\sqrt{K_{a1}c}$ 即可。",
 ),
 8: dict(
   考点=r"缓冲溶液（Henderson-Hasselbalch 式）· 沉淀溶解-配位多重平衡 · 质量守恒"
        r"（知识点：〈缓冲溶液〉、〈亨德森-哈塞尔巴赫方程〉、〈多重平衡〉、〈稳定常数〉、〈溶解度〉）",
   思路=r"8-1 直接用缓冲公式（同离子效应使 HAc 几乎不解离）；8-2 先算「若完全溶解所需 $\mathrm{Pb}$ 浓度」与"
        r"「饱和溶液能达到的最大 $\mathrm{Pb}$ 浓度」作比较判断，再借醋酸根质量守恒求上清液 $[\mathrm{Ac^-}]$。",
   步骤=[
     ("8-1", "2 分",
      r"$n(\mathrm{NaAc})=0.125/82.03=1.52\times10^{-3}\ \mathrm{mol}$ ⇒ "
      r"$c(\mathrm{NaAc})=1.52\times10^{-3}/0.020=0.0762\ \mathrm{mol/L}$。"
      r"NaAc 是强电解质，大量 $\mathrm{Ac^-}$ 强烈抑制 HAc 解离，故 $[\mathrm{HAc}]\approx7.5\times10^{-4}\ \mathrm{mol/L}$、"
      r"$[\mathrm{Ac^-}]\approx0.0762\ \mathrm{mol/L}$。"
      r"pH $=\mathrm{p}K_a+\lg\frac{[\mathrm{Ac^-}]}{[\mathrm{HAc}]}=4.75+\lg\frac{0.0762}{7.5\times10^{-4}}=4.75+2.01=6.76$。"),
     ("8-2", "6 分",
      r"**不能。** 若 0.040 g $\mathrm{PbSO_4}$（$M=303.3$）全部溶于 20 mL，则 "
      r"$c(\mathrm{Pb})=[\mathrm{SO_4^{2-}}]=0.040/(303.3\times0.020)=6.60\times10^{-3}\ \mathrm{mol/L}$，"
      r"要求 $[\mathrm{Pb^{2+}}]=K_{sp}/[\mathrm{SO_4^{2-}}]=1.62\times10^{-8}/6.60\times10^{-3}=2.45\times10^{-6}\ \mathrm{mol/L}$，"
      r"即配合作用须把 $\mathrm{Pb}$ 的溶解度放大 $6.60\times10^{-3}/2.45\times10^{-6}\approx2690$ 倍。"
      r"但饱和溶液中 $c(\mathrm{Pb})=\sqrt{K_{sp}(1+\beta_1[\mathrm{Ac^-}]+\beta_2[\mathrm{Ac^-}]^2+\beta_3[\mathrm{Ac^-}]^3)}$，"
      r"在可用 $[\mathrm{Ac^-}]\approx0.076\ \mathrm{mol/L}$ 时括号内约 $1.2\times10^{3}<2690$，"
      r"对应最大 $c(\mathrm{Pb})\approx3.6\times10^{-3}\ \mathrm{mol/L}$（约 0.022 g）$<6.60\times10^{-3}\ \mathrm{mol/L}$ ⇒ 不能完全溶解。"
      r"由醋酸根质量守恒 "
      r"$c(\mathrm{HAc})+c(\mathrm{NaAc})=[\mathrm{HAc}]+[\mathrm{Ac^-}]+[\mathrm{Pb^{2+}}](\beta_1[\mathrm{Ac^-}]+2\beta_2[\mathrm{Ac^-}]^2+3\beta_3[\mathrm{Ac^-}]^3)$"
      r"（因 $c(\mathrm{HAc})/c(\mathrm{NaAc})\approx0.01$，可认为 $[\mathrm{HAc}]$ 不变），"
      r"联立 $[\mathrm{Pb^{2+}}][\mathrm{SO_4^{2-}}]=K_{sp}$ 与 $[\mathrm{SO_4^{2-}}]=c(\mathrm{Pb})$，"
      r"解得上清液 $[\mathrm{Ac^-}]\approx0.066\ \mathrm{mol/L}$。"),
    ],
   易错=r"① 8-1 中 HAc 的解离被大量 $\mathrm{Ac^-}$ 抑制，故 $c(\mathrm{HAc})$ 仍按加入量计；"
        r"② 8-2 的判据是「最大可溶解 $c(\mathrm{Pb})$ 与所需 $c(\mathrm{Pb})$ 的比较」，不是直接比 $K_{sp}$；"
        r"③ $\mathrm{Pb}$ 的形态要含 $\beta_1\sim\beta_3$ 三个配合物，醋酸根质量守恒须把配合物中的醋酸根按 1:2:3 计入。",
 ),
 9: dict(
   考点=r"van't Hoff 等压方程（$K$ 与 $T$）· $\Delta_rG^\ominus=-RT\ln K^\ominus$ · 平衡转化率（$K_x$ 与 $K_p^\ominus$ 的关系）· Le Châtelier 原理"
        r"（知识点：〈van't Hoff方程〉、〈Le Châtelier原理〉、〈化学平衡计算〉、〈Gibbs自由能〉）",
   思路=r"由两个温度的 $K$ 用 van't Hoff 积分式求 $\Delta_rH^\ominus$；外推到 1100 K 得 $K_p^\ominus$ 与 $\Delta_rG^\ominus$、$\Delta_rS^\ominus$；"
        r"转化率用「总量 $2+2x$、$\Delta\nu=+2$、$K_p^\ominus=K_x(p/p^\ominus)^2$」求解；9-4/9-5 分别用 $K_x$ 对 $p$ 的偏导与 van't Hoff 判据。",
   步骤=[
     ("9-1", "2 分",
      r"$\mathrm{CH_4(g)}+\mathrm{H_2O(g)}\rightleftharpoons\mathrm{CO(g)}+3\mathrm{H_2(g)}$。"),
     ("9-2", "7 分",
      r"由 van't Hoff 等压方程（$\Delta_rH^\ominus$ 视为常数）："
      r"$\ln\frac{K^\ominus(298)}{K^\ominus(1580)}=-\frac{\Delta_rH_m^\ominus}{R}\left(\frac{1}{298}-\frac{1}{1580}\right)$，"
      r"$\ln\frac{1.45\times10^{-25}}{2.66\times10^{4}}=-67.2$，解得 $\Delta_rH_m^\ominus\approx2.06\times10^{5}\ \mathrm{J\cdot mol^{-1}}=206\ \mathrm{kJ\cdot mol^{-1}}$（吸热）。"
      r"再由 1100 K：$\ln K^\ominus(1100)=\ln K^\ominus(1580)-\frac{\Delta_rH_m^\ominus}{R}\left(\frac{1}{1100}-\frac{1}{1580}\right)"
      r"=10.19-6.84=3.35$ ⇒ $K_p^\ominus=28.4$。"
      r"$\Delta_rG_m^\ominus=-RT\ln K_p^\ominus=-8.314\times1100\times3.35=-3.06\times10^{4}\ \mathrm{J\cdot mol^{-1}}$；"
      r"$\Delta_rS_m^\ominus=\frac{\Delta_rH_m^\ominus-\Delta_rG_m^\ominus}{T}=\frac{206000+30600}{1100}=215\ \mathrm{J\cdot K^{-1}\cdot mol^{-1}}$。"),
     ("9-3", "5 分",
      r"设 $\mathrm{CH_4}$ 转化率为 $x$：平衡时 $n(\mathrm{CH_4})=n(\mathrm{H_2O})=1-x$、$n(\mathrm{CO})=x$、$n(\mathrm{H_2})=3x$，"
      r"总量 $n_{总}=2+2x$；$\Delta\nu=(1+3)-(1+1)=2$，故 "
      r"$K_p^\ominus=K_x(p/p^\ominus)^2=K_x\times1.6^{2}$（$p=1.60\ \mathrm{bar}=1.6p^\ominus$）。"
      r"$K_x=\frac{x(3x)^3}{(1-x)^2(2+2x)^2}=\frac{27x^4}{4(1-x)^2(1+x)^2}$，代入 "
      r"$K_p^\ominus=28.4$ 得 $\frac{x^2}{(1-x)(1+x)}=\sqrt{\frac{28.4}{17.28}}=1.282$，"
      r"解得 $x^2=0.562$，$x=0.749$。"),
     ("9-4", "3 分",
      r"$\Delta\nu(\mathrm{g})=+2>0$。以摩尔分数表示的平衡常数满足 "
      r"$\left(\frac{\partial\ln K_x}{\partial p}\right)_T=-\frac{\sum\nu_B(\mathrm g)}{p}<0$，"
      r"即 $K_x$ 随压力增大而减小。物理意义：该反应气体分子数增大，加压使平衡向气体分子数减小的**逆向**移动，"
      r"故增加压力**不利**于提高 $\mathrm{CH_4}$ 的平衡转化率。（亦可由 Le Châtelier 原理直接判断。）"),
     ("9-5", "3 分",
      r"$\Delta_rH_m^\ominus=+206\ \mathrm{kJ\cdot mol^{-1}}>0$（吸热）。由 van't Hoff 等压方程 "
      r"$\left(\frac{\partial\ln K_p^\ominus}{\partial T}\right)_p=\frac{\Delta_rH_m^\ominus}{RT^2}>0$，"
      r"$K_p^\ominus$ 随温度升高而增大，故升高温度**有利**于提高转化率。"
      r"（亦可由 Le Châtelier 原理：吸热反应升温向正反应方向移动。）"),
    ],
   易错=r"① van't Hoff 积分式中 $\left(\frac{1}{T_1}-\frac{1}{T_2}\right)$ 的次序与 $K$ 的比值次序必须对应；"
        r"② $K_p^\ominus$ 与 $K_x$ 之间隔着 $(p/p^\ominus)^{\Delta\nu}$，$\Delta\nu$ 只计气态物质；"
        r"③ 9-4 与 9-5 的结论方向相反（加压不利、升温有利），别都写成「有利」。",
 ),
 10: dict(
   考点=r"弹式热量计（恒容）与 $\Delta_rU/\Delta_rH$ 换算 · 燃烧热与生成焓 · 凝固点降低（依数性）· Clapeyron 方程与熔点随压力的变化"
        r"（知识点：〈化学热力学〉、〈内能〉、〈稀溶液依数性〉、〈Clapeyron方程〉、〈相变热力学〉）",
   思路=r"弹式热量计测的是 $\Delta_rU$（恒容）；由两次实验的水温升高比得量热计热容；"
        r"$\Delta_rH=\Delta_rU+\Delta\nu RT$；10-2 用「放热/熔化焓」的比值区间判断，10-3 用「依数性 → 压强效应 → Clapeyron 方程」。",
   步骤=[
     ("10-1", "8 分",
      r"$\mathrm{H_2(g)}+\frac12\mathrm{O_2(g)}=\mathrm{H_2O(l)}$，$\Delta_rH_m^\ominus=-285.8\ \mathrm{kJ\cdot mol^{-1}}$，"
      r"气相 $\Delta\nu=0.5-1=-1.5$，"
      r"$\Delta_rU_m^\ominus=\Delta_rH_m^\ominus-\Delta\nu RT=-285.8-(-1.5\times8.314\times298\times10^{-3})=-285.8+3.72=-282.08\ \mathrm{kJ\cdot mol^{-1}}$。"
      r"0.30 mol $\mathrm{H_2}$ 恒容燃烧放热 $0.30\times282.08=84.62\ \mathrm{kJ}$，使水温升 5.212 K ⇒ 量热计热容 "
      r"$C=84.62/5.212=16.24\ \mathrm{kJ\cdot K^{-1}}$。"
      r"2.345 g 正癸烷（$\mathrm{C_{10}H_{22}}$，$M=142.29$）$=0.016481\ \mathrm{mol}$，燃烧使水温升 6.862 K ⇒ 放热 "
      r"$C\times6.862=111.41\ \mathrm{kJ}$，故 $\Delta_rU_m^\ominus=-111.41/0.016481=-6.759\times10^{3}\ \mathrm{kJ\cdot mol^{-1}}$。"
      r"燃烧方程 $\mathrm{C_{10}H_{22}(l)}+15.5\mathrm{O_2(g)}=10\mathrm{CO_2(g)}+11\mathrm{H_2O(l)}$，气相 $\Delta\nu=10-15.5=-5.5$，"
      r"$\Delta_rH_m^\ominus=\Delta_rU_m^\ominus+\Delta\nu RT=-6759-5.5\times8.314\times298\times10^{-3}=-6773\ \mathrm{kJ\cdot mol^{-1}}\approx-6.773\times10^{3}\ \mathrm{kJ\cdot mol^{-1}}$。"),
     ("10-2", "6 分",
      r"碳燃烧放热全部用于熔化冰（$\Delta_{\mathrm{fus}}H=6.007\ \mathrm{kJ\cdot mol^{-1}}$，$M(\mathrm{H_2O})=18.02$，$M(\mathrm C)=12.01$）："
      r"① 完全生成 $\mathrm{CO_2}$：1 mol C 放热 393.51 kJ ⇒ 熔化冰 $393.51/6.007=65.51\ \mathrm{mol}$，"
      r"$\frac{m(\text{冰})}{m(\mathrm C)}=\frac{65.51\times18.02}{12.01}=98.27$。"
      r"② 完全生成 CO：1 mol C 放热 110.52 kJ ⇒ 熔化冰 $110.52/6.007=18.40\ \mathrm{mol}$，"
      r"$\frac{m(\text{冰})}{m(\mathrm C)}=\frac{18.40\times18.02}{12.01}=27.60$。"
      r"实验值 96.5、69、40 **全部落在 27.60 与 98.27 之间** ⇒ 说明碳发生**不完全燃烧**、产物是 CO 与 $\mathrm{CO_2}$ 的混合物，"
      r"故碳的不完全燃烧**可以解释**数据的差异。"),
     ("10-3", "6 分",
      r"金星大气压下水中 $\mathrm{CO_2}$ 质量分数 7.50%：1 L 水（约 1000 g）溶解 "
      r"$\mathrm{CO_2}$ $1000\times0.075/44.01=1.704\ \mathrm{mol}$，折合约 $1.704/(1-0.075)=1.842\ \mathrm{mol/kg}$ 溶剂。"
      r"由依数性（凝固点降低）$\Delta T_f=K_fb=1.86\times1.842=3.43\ \mathrm{K}$ ⇒ 仅由浓度引起的熔点 $=273.16-3.43=269.73\ \mathrm{K}$。"
      r"实测熔点 269.29 K，差值 $0.44\ \mathrm{K}$ 即压强所致："
      r"$\Delta p=93\times101325-610.48=9.42\times10^{6}\ \mathrm{Pa}$，故 "
      r"$\frac{\mathrm{d}T}{\mathrm{d}p}\approx\frac{-0.44}{9.42\times10^{6}}=-4.7\times10^{-8}\ \mathrm{K\cdot Pa^{-1}}<0$。"
      r"该值小于零的原因：由 Clapeyron 方程 $\frac{\mathrm{d}T}{\mathrm{d}p}=\frac{\Delta_{\mathrm{fus}}V}{\Delta_{\mathrm{fus}}S}$，"
      r"冰熔化时体积**减小**（$\Delta_{\mathrm{fus}}V<0$）而熵增（$\Delta_{\mathrm{fus}}S>0$），故斜率为负；"
      r"从化学平衡看，加压有利于向体积减小的方向（熔化）移动，即加压使熔点降低——这正是滑冰时「复冰」现象的机理。"),
    ],
   易错=r"① 弹式热量计测 $\Delta U$（恒容），由 $\Delta U$ 求 $\Delta H$ 时必须加 $\Delta\nu RT$，且 $\Delta\nu$ 只计气态；"
        r"② 正癸烷燃烧方程中 $\mathrm{O_2}$ 系数为 15.5，$\Delta\nu=10-15.5=-5.5$，别漏算；"
        r"③ 10-2 要分别算两种完全燃烧产物的比值，结论是「实验值介于两者之间」；"
        r"④ 10-3 的凝固点降低要用**质量摩尔浓度**（mol/kg 溶剂），且冰熔化的体积变化为负。",
 ),
}
