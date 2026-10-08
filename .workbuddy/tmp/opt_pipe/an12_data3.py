# -*- coding: utf-8 -*-
"""卷 XII 解析数据（第 8~10 题）。"""

A3 = {
 8: dict(
   考点=r"Langmuir 吸附等温式与线性化、吸附焓的 van't Hoff 关系、多组分吸附中的物料守恒"
        r"（知识点：〈Langmuir吸附等温式〉、〈吸附〉、〈化学平衡计算〉、〈van't Hoff方程〉）",
   思路=r"8-1 由两次实验的初、末态气体量差算吸附量 $q_A,q_B$，再用 Langmuir 的线性式 $\frac Pq=\frac1{q_mb}+\frac P{q_m}$ 两点定 $q_m$、$b$；"
        r"8-2 由 328 K 的单点数据反求 $b_{328}$，再用 van't Hoff 关系求吸附焓；"
        r"8-3 对 CO₂、N₂ 分别列「气相＋吸附相＝总量」的**物料守恒方程**求解分压；"
        r"8-4 吸附剂转入新容器、升温后重新建立平衡，仍用物料守恒，效率＝(吸附量−脱附后残留)/吸附量。",
   步骤=[
     ("8-1", "—",
      r"初始通入的 CO₂：$n_0=\dfrac{pV}{RT}=\dfrac{1.000\times10^{5}\times5.00\times10^{-4}}{8.314\times298.15}"
      r"=2.017\times10^{-2}\ \mathrm{mol}$；"
      r"平衡时气相残留 $n_g=\dfrac{0.208\times10^{5}\times2.00\times10^{-3}}{8.314\times298.15}=1.678\times10^{-2}\ \mathrm{mol}$，"
      r"故 $q_A=(2.017-1.678)\times10^{-3}/1.000=3.39\ \mathrm{mmol\cdot g^{-1}}$。"
      r"同理第二次 $q_B=4.11\ \mathrm{mmol\cdot g^{-1}}$。"
      r"由线性式两点求解：$q_m=\dfrac{P_B-P_A}{P_B/q_B-P_A/q_A}"
      r"=\dfrac{0.449-0.208}{0.449/4.11-0.208/3.39}\approx5.06\ \mathrm{mmol\cdot g^{-1}}$；"
      r"再代回得 $b_{298}=\dfrac{q}{P(q_m-q)}$ 形式反解约 $9.76\ \mathrm{bar^{-1}}$。"),
     ("8-2", "—",
      r"328 K、$P=0.200\ \mathrm{bar}$、$q=1.67\ \mathrm{mmol\cdot g^{-1}}$（设 $q_m$ 不随温度变）："
      r"$b_{328}=\dfrac{q}{P(q_m-q)}=\dfrac{1.67}{0.200\times(5.06-1.67)}\approx2.46\ \mathrm{bar^{-1}}$。"
      r"由 $\ln\dfrac{b_{328}}{b_{298}}=-\dfrac{\Delta H}{R}\left(\dfrac1{328}-\dfrac1{298}\right)$ 得"
      r"$\Delta H\approx-37.3\ \mathrm{kJ\cdot mol^{-1}}$（负值 ⇒ 吸附放热，升温不利于吸附）。"),
     ("8-3", "—",
      r"通入烟气：$n(\mathrm{CO_2})_0=0.15\times\dfrac{1.000\times10^{5}\times10.0\times10^{-3}}{8.314\times298.15}"
      r"=6.05\times10^{-2}\ \mathrm{mol}$，$n(\mathrm{N_2})_0=0.85\times0.4034=3.429\times10^{-1}\ \mathrm{mol}$。"
      r"**CO₂ 物料守恒**：$n_g+n_{ads}=n_0$，即"
      r"$\dfrac{P_{\mathrm{CO_2}}\times1000}{8.314\times298.15}+5.00\times\dfrac{q_mb_{298}P}{1+b_{298}P}\times10^{-3}"
      r"=6.05\times10^{-2}$ ⇒ 解得 $P_{\mathrm{CO_2}}=0.117\ \mathrm{bar}$，"
      r"$q_{ads}=2.70\ \mathrm{mmol\cdot g^{-1}}$（合 $13.5\ \mathrm{mmol}$）。"
      r"**N₂ 物料守恒**（Henry 式 $q=kP$）：$0.4034P_{N_2}+5.00\times0.0500P_{N_2}\times10^{-3}=0.3429$ "
      r"⇒ $P_{\mathrm{N_2}}=0.849\ \mathrm{bar}$，$n_{ads}=0.212\ \mathrm{mmol}$。"),
     ("8-4", "—",
      r"取出吸附剂（仅含 CO₂ $13.5\ \mathrm{mmol}$）转入 $2.00\ \mathrm L$ 真空容器、升温至 $328\ \mathrm K$，"
      r"重新列物料守恒：$\dfrac{P\times2000}{8.314\times328.15}+5.00\times\dfrac{q_mb_{328}P}{1+b_{328}P}\times10^{-3}"
      r"=1.35\times10^{-2}$ ⇒ 解得 $P_{\mathrm{CO_2}}=0.110\ \mathrm{bar}$，"
      r"此时残留吸附量 $q_{des}=1.08\ \mathrm{mmol\cdot g^{-1}}$。"
      r"工作效率 $\eta=\dfrac{q_{ads}-q_{des}}{q_{ads}}=\dfrac{2.70-1.08}{2.70}\approx59.9\%$。"),
    ],
   易错=r"① 8-1 的吸附量必须由「初态总量 − 平衡气相量」求出，直接用量纲算 $P/q$ 而不做物质的量换算会错；"
        r"② Langmuir 线性式有两个等价形式（$\frac Pq$ 对 $P$、或 $\frac1q$ 对 $\frac1P$），用错形式会算错 $b$；"
        r"③ 8-3／8-4 的气相体积分别是 $10.0\ \mathrm L$ 与 $2.00\ \mathrm L$（不是吸附剂体积），易混；"
        r"④ 328 K 时 $b$ 变小、$q$ 变小 ⇒ 脱附，效率分母用**吸附量**而非脱附量。"),
 9: dict(
   考点=r"Ostwald-Freundlich（Kelvin）方程的溶解度–粒度关系、奥斯特瓦尔德熟化、均相成核的临界晶核与成核势垒"
        r"（知识点：〈表面张力〉、〈溶解度〉、〈Gibbs自由能〉、〈溶度积〉、〈相变热力学〉）",
   思路=r"9-1 由两个不同半径的溶解度**相比**消去 $S_\infty$ 求界面张力 $\gamma$，再代回求大块溶解度；"
        r"9-2 熟化过程的本质是「小颗粒全溶、物质并入大颗粒」⇒ 颗粒数不变、**总体积不变**，据此定 $r_3$，再回代方程求 $S_3$；"
        r"9-3 临界晶核处于「自身溶解度＝过饱和浓度」的亚稳平衡，先求 $r_c$；成核势垒由体积项与表面项相加、对 $r$ 求极值得 $\Delta G_C$。",
   步骤=[
     ("9-1", "5 分",
      r"对 1:1 型电解质 $K_{sp}=S^2$，Ostwald-Freundlich 方程化为 $RT\ln\dfrac{S_r}{S_\infty}=\dfrac{\gamma M}{\rho r}$。"
      r"取两半径之比消去 $S_\infty$：$\ln\dfrac{S_2}{S_1}=\dfrac{\gamma M}{\rho RT}\left(\dfrac1{r_2}-\dfrac1{r_1}\right)$。"
      r"代入 $S_1=1.065\times10^{-5}$、$S_2=1.285\times10^{-5}$、$M=233.4\ \mathrm{g\cdot mol^{-1}}$、$\rho=4.50\ \mathrm{g\cdot cm^{-3}}$，"
      r"得 $\gamma\approx0.1197\ \mathrm{J\cdot m^{-2}}$。"
      r"再把 $\gamma$ 与 $r_1$ 代回：$\ln\dfrac{S_1}{S_\infty}=\dfrac{\gamma M}{\rho r_1RT}$ ⇒ $S_\infty=1.000\times10^{-5}\ \mathrm{mol\cdot L^{-1}}$。"),
     ("9-2", "6 分",
      r"小颗粒（$r_2=10.0\ \mathrm{nm}$）表面能高、溶解度大，会持续溶解并沉积到大颗粒（$r_1=40.0\ \mathrm{nm}$）上"
      r"（**奥斯特瓦尔德熟化**）。设大颗粒数 $N_1$ 不变，终态全部 $1.0\ \mathrm{mol}$ 由这 $N_1$ 个晶粒构成，"
      r"由**体积守恒**知终态单颗粒体积为初态的 2 倍：$r_3=\sqrt[3]{2}\,r_1=1.260\times40.0\ \mathrm{nm}=50.40\ \mathrm{nm}$。"
      r"再由 $RT\ln\dfrac{S_3}{S_\infty}=\dfrac{\gamma M}{\rho r_3}$ 得 $S_3=1.051\times10^{-5}\ \mathrm{mol\cdot L^{-1}}$。"),
     ("9-3", "—",
      r"临界晶核处于亚稳平衡：其溶解度恰等于过饱和浓度 $S_c=C$，即 $RT\ln\dfrac{C}{S_\infty}=\dfrac{\gamma M}{\rho r_c}$，"
      r"$\ln2\times2478.8$ 代入得 $r_c=3.613\times10^{-9}\ \mathrm m=3.613\ \mathrm{nm}$。"
      r"成核自由能 $\Delta G=\dfrac43\pi r^3\Delta g_v+4\pi r^2\gamma$（$\Delta g_v<0$），"
      r"对 $r$ 求导为零 ⇒ $r_c=-\dfrac{2\gamma}{\Delta g_v}$ ⇒ $\Delta g_v=-\dfrac{2\gamma}{r_c}$。"
      r"代回：$\Delta G_C=\dfrac43\pi r_c^3\times\left(-\dfrac{2\gamma}{r_c}\right)+4\pi r_c^2\gamma"
      r"=\dfrac43\pi\gamma r_c^2\approx6.55\times10^{-18}\ \mathrm J$。"),
    ],
   易错=r"① 9-1 必须先「两式相除」消 $S_\infty$（$S_\infty$ 未知），直接代入会陷入死循环；"
        r"② 单位：$M$ 用 $\mathrm{kg\cdot mol^{-1}}$、$\rho$ 用 $\mathrm{kg\cdot m^{-3}}$、$r$ 用 $\mathrm m$ 才能与 $RT$ 匹配；"
        r"③ 9-2 的 $r_3$ 由**体积守恒**（颗粒数 $N_1$ 不变）求得，不是「半径取平均」；"
        r"④ 9-3 的 $\Delta G_C$ 是 $\frac43\pi\gamma r_c^2$（推导后交叉项相消），漏掉体积项会得 2 倍值。"),
 10: dict(
   考点=r"热力学函数（$\Delta_rH$、$\Delta_rS$、$\Delta_rG$）与平衡常数的相互换算、气相–液相–溶解多相平衡的物料守恒与亨利定律"
        r"（知识点：〈化学热力学〉、〈Gibbs自由能〉、〈化学平衡〉、〈反应商〉、〈标准生成焓〉、〈标准熵〉）",
   思路=r"10-1／10-2 直接由 $\Delta_fH^\ominus$、$S_m^\ominus$ 算出 $\Delta_rH^\ominus$、$\Delta_rS^\ominus$，再按 $T$ 算 $\Delta_rG^\ominus$、"
        r"由 $\Delta_rG^\ominus=-RT\ln K^\ominus$ 求 $K^\ominus$；10-3 以「气–液两相物料守恒」列方程，"
        r"气相用 $pV=nRT$、液相用浓度的 4 次方与气体分压的 3 次方之比写出 $K$，解出反应进度 $x$；"
        r"末问引入亨利定律把溶解量并入守恒式。",
   步骤=[
     ("10-1", "3 分",
      r"$4\mathrm{NH_3(g)}+7\mathrm{O_2(g)}\to4\mathrm{NO_2(g)}+6\mathrm{H_2O(l)}$。"
      r"$\Delta_rH_m^\ominus=4\times33.2+6\times(-285.8)-4\times(-45.9)"
      r"=132.8-1714.8+183.6=-1398.4\ \mathrm{kJ\cdot mol^{-1}}$；"
      r"$\Delta_rS_m^\ominus=4\times240.1+6\times70.0-4\times192.8-7\times205.2"
      r"=960.4+420.0-771.2-1436.4=-827.2\ \mathrm{J\cdot mol^{-1}\cdot K^{-1}}$；"
      r"$\Delta_rG_m^\ominus=-1398.4-298.15\times(-827.2)\times10^{-3}=-1151.8\ \mathrm{kJ\cdot mol^{-1}}$。"),
     ("10-2", "—",
      r"$3\mathrm{NO_2(g)}+\mathrm{H_2O(l)}\to2\mathrm{HNO_3(aq)}$（$\mathrm{HNO_3}$ 完全电离，写成 $2\mathrm{H^+}+2\mathrm{NO_3^-}$）："
      r"$\Delta_rH_m^\ominus=2\times(-206.9)+91.3-3\times33.2-(-285.8)=-136.3\ \mathrm{kJ\cdot mol^{-1}}$；"
      r"$\Delta_rS_m^\ominus=2\times146.7+210.8-3\times240.1-70.0=-286.1\ \mathrm{J\cdot mol^{-1}\cdot K^{-1}}$。"
      r"$T=348.15\ \mathrm K$ 时 $\Delta_rG_m^\ominus=-136.3-348.15\times(-286.1)\times10^{-3}=-36.7\ \mathrm{kJ\cdot mol^{-1}}$；"
      r"$K^\ominus=\exp\!\left(\dfrac{36.7\times10^{3}}{8.314\times348.15}\right)\approx3.2\times10^{5}$。"),
     ("10-3-1", "—",
      r"$n_0(\mathrm{NO})=\dfrac{p_0V}{RT}=\dfrac{300\times40.0}{0.08314\times348.15}\approx415\ \mathrm{mol}$；"
      r"$n_0(\mathrm{NO_2})=\dfrac{100\times21000}{8.314\times348.15}\approx726\ \mathrm{mol}$。"
      r"气相体积 $=40.0-30.0=10.0\ \mathrm L$。设反应 $3\mathrm{NO_2}+\mathrm{H_2O}\to2\mathrm{H^+}+2\mathrm{NO_3^-}+\mathrm{NO}$ 进度为 $x$，"
      r"由 $K^\ominus=\dfrac{(2x/30)^4\cdot p(\mathrm{NO})}{p(\mathrm{NO_2})^3}=3.20\times10^{5}$ 解得 $x\approx241$。"
      r"于是 $c(\mathrm{HNO_3})=\dfrac{2x}{30.0}=16.1\ \mathrm{mol\cdot L^{-1}}$；"
      r"$p(\mathrm{NO})=1.90\times10^{3}\ \mathrm{bar}$、$p(\mathrm{NO_2})\approx7\ \mathrm{bar}$。"),
     ("10-3-2", "—",
      r"$\mathrm{NO_2(g)\rightleftharpoons NO_2(aq)}$：$K'=k\dfrac{p^\ominus}{c^\ominus}=1.20\times10^{-4}\times\dfrac{10^{5}}{10^{3}}=1.20\times10^{-2}$。"
      r"把溶解项并入物料守恒（气相分压由 $(726-3x)/(3K'RT+1)$ 形式给出），仍用同一 $K^\ominus=3.20\times10^{5}$ 解得"
      r"$p(\mathrm{NO_2})=7.30\ \mathrm{bar}$、$c(\mathrm{NO_2})=8.76\times10^{-2}\ \mathrm{mol\cdot L^{-1}}$。"),
    ],
   易错=r"① 10-1／10-2 的 $\Delta_rG^\ominus$ 必须在**指定温度**下算（$298.15$ vs $348.15\ \mathrm K$），不能混用；"
        r"② 10-3 的气相体积是「总容积 $40.0\ \mathrm L$ − 溶液 $30.0\ \mathrm L$ ＝ $10.0\ \mathrm L$」，漏减是常见错误；"
        r"③ 平衡常数表达式中浓度的幂次是 4（$2x/30$ 的 4 次方，来自 $2\mathrm{H^+}$ 与 $2\mathrm{NO_3^-}$），"
        r"气体项幂次为 3（$3\mathrm{NO_2}$）／1（$\mathrm{NO}$），配错会无解；"
        r"④ 亨利常数的量纲换算 $K'=k\,p^\ominus/c^\ominus$ 不可漏。"),
}
