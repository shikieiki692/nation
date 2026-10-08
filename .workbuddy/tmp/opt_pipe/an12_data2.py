# -*- coding: utf-8 -*-
"""卷 XII 解析数据（第 5~7 题）。"""

A2 = {
 5: dict(
   考点=r"萤石型结构与点缺陷、生成吉布斯自由能与混合熵、对峙反应平衡、Born-Haber 型热力学循环"
        r"（知识点：〈Gibbs自由能〉、〈化学平衡〉、〈晶胞〉、〈熵变计算〉、〈电极过程热力学〉）",
   思路=r"5-1 从萤石型的空隙分布定位掺杂氧的位置并数出填隙率；5-2 先用两个辅助反应（$8UO_2+O_2\to2U_4O_9$、"
        r"$2Am_2O_3+O_2\to4AmO_2$）分别反求 $\Delta_fG^\ominus(UO_2)$ 与 $\Delta_fG^\ominus(AmO_2)$，"
        r"再按 $0.85:0.15$ 加权，**并叠加混合熵项**；5-3 把氧势换算成氧分压后线性回归，令 $x=0$ 求平衡氧压；"
        r"5-4／5-5 从离子半径与价态稳定性定性解释、并配平氧化反应。",
   步骤=[
     ("5-1", "—",
      r"萤石型结构中阴离子构成简单立方、阳离子填半数立方体中心，**八面体空隙空置**（每晶胞 4 个，"
      r"恰与 4 个 $UO_2$ 式量对应）。额外掺入的氧即进入这些八面体空隙，每式量多出的氧为 $x$，"
      r"故**填隙率＝$x$**（占八面体空隙的 $x\times100\%$；$x<0.5$ 与题设一致）。"
      r"⚠️ 源答案此问答在 OCR 中缺失，以上据萤石型结构规律补出。"),
     ("5-2", "—",
      r"① $8UO_2+O_2\to2U_4O_9$：$\Delta_rS^\ominus=2\times334.1-8\times77.03-205.1=-153.14\ \mathrm{J\cdot mol^{-1}\cdot K^{-1}}$，"
      r"$\Delta_rH^\ominus=2\times(-4512)-8\times(-1085)=-344\ \mathrm{kJ\cdot mol^{-1}}$，"
      r"$\Delta_rG^\ominus=-344-298.15\times(-153.14)\times10^{-3}=-298.3\ \mathrm{kJ\cdot mol^{-1}}$；"
      r"由 $2\Delta_fG^\ominus(U_4O_9)-8\Delta_fG^\ominus(UO_2)=-298.3$ 得 $\Delta_fG^\ominus(UO_2)=-1096\ \mathrm{kJ\cdot mol^{-1}}$。"
      r"② $2Am_2O_3+O_2\to4AmO_2$：$\Delta_rH^\ominus=-348.8$、$\Delta_rS^\ominus=-171.5\ \mathrm{J\cdot mol^{-1}\cdot K^{-1}}$，"
      r"$\Delta_rG^\ominus=-297.7\ \mathrm{kJ\cdot mol^{-1}}$ ⇒ $\Delta_fG^\ominus(AmO_2)=-876.9\ \mathrm{kJ\cdot mol^{-1}}$。"
      r"③ 混合熵项 $T\Delta S_{\mathrm{mix}}=RT(0.85\ln0.85+0.15\ln0.15)=-1.05\ \mathrm{kJ\cdot mol^{-1}}$；"
      r"$\Delta_fG^\ominus=0.85\times(-1096)+0.15\times(-876.9)-1.05\approx-1064\ \mathrm{kJ\cdot mol^{-1}}$。"
      r"**末项即混合熵贡献**（$T\Delta S_{\mathrm{mix}}<0$ 使生成自由能略降低）。"),
     ("5-3", "3 分",
      r"由 $\Delta G(O_2)=RT\ln(p_{O_2}/p^\ominus)$（$T=2023\ \mathrm K$，$RT=16.82\ \mathrm{kJ\cdot mol^{-1}}$）把 6 组数据换算成"
      r"$p_{O_2}/p^\ominus$，对 $x\!\sim\!p_{O_2}/p^\ominus$ 线性回归得"
      r"$x=5.923\times10^{6}\cdot\dfrac{p_{O_2}}{p^\ominus}-3.224\times10^{-3}$。"
      r"令 $x=0$ 解得 $\dfrac{p_{O_2}}{p^\ominus}=5.443\times10^{-10}$"
      r"（即该对峙反应达平衡时的氧分压，与「额外掺杂氧浓度与氧分压成正比」的提示一致）。"),
     ("5-4", "—",
      r"$Am$ 的 5f 电子收缩使 $Am^{4+}$ 氧化性强，难以与还原性较强的 $U^{4+}$ 大量共存 ⇒ 实际存在的形式为"
      r"混合价 $(U^{4+}_{1-2x-2y})(U^{5+}_{2x-2y})(Am^{3+})(O^{2-}_{2-2x})$。"
      r"$Am^{3+}$ 的离子半径明显大于 $U^{4+}/Am^{4+}$，把晶格「撑开」，故晶胞参数 $a$ 总比两种原料的平均值大约 $10\ \mathrm{pm}$。"),
     ("5-5", "—",
      r"灼烧的目的是把 $Am$ 由 $+3$ 氧化到 $+4$（生成 $AmO_2$），同时把 $U$ 氧化到高价态。"
      r"若 $U$ 氧化为 $UO_3$，令 $U_{1-y}Am_yO_{2+x}$ 系数为 1，按 **U、Am、O 三元素守恒**配平："
      r"$U_{1-y}Am_yO_{2+x}+\dfrac{1-y-x}{2}O_2\to y\,AmO_2+(1-y)UO_3$。"
      r"⚠️ 源答案此问缺失；上式为「$U\to+6$、$Am\to+4$」假设下的配平结果，"
      r"若按 $U$ 只氧化到 $+5$（或生成 $U_4O_9$）则系数不同。"),
    ],
   易错=r"① 5-2 **必须含混合熵项**（题目明示「注意混合过程」），漏掉会使结果偏差约 $1\ \mathrm{kJ\cdot mol^{-1}}$；"
        r"② $\Delta_fG^\ominus(UO_2)$、$\Delta_fG^\ominus(AmO_2)$ **没有直接给**，须用辅助反应间接求解（这是本题的题眼）；"
        r"③ 5-3 的氧势要先经 $\Delta G=RT\ln(p/p^\ominus)$ 换成氧分压，不能直接拿 $\Delta G$ 与 $x$ 回归；"
        r"④ 5-5 配平要按元素守恒逐项核对（氧的收支最易错）。"),
 6: dict(
   考点=r"弱酸质子条件（PBE）与二元酸的处理、金属硫化物沉淀的溶度积判据"
        r"（知识点：〈酸碱平衡〉、〈缓冲溶液〉、〈溶度积〉、〈沉淀溶解平衡〉）",
   思路=r"6-1 因 $K_1\gg K_2$ 可只考虑一级电离，列出**质子条件式** $[\mathrm H^+]=[\mathrm{OH^-}]+[\mathrm{HS^-}]$，"
        r"再以 $[\mathrm H^+]$ 为未知量解方程；6-2 先由沉淀反应定量算出完全沉淀时溶液的 $[\mathrm H^+]$，"
        r"再由 $K_{a1}K_{a2}$ 求 $[\mathrm S^{2-}]$，最后按 $K_{sp}=[\mathrm M^{2+}][\mathrm S^{2-}]$ 求 $pK_{sp}$ 下限。",
   步骤=[
     ("6-1", "2 分",
      r"$K_1\gg K_2$ ⇒ 忽略二级电离。质子条件：$[\mathrm H^+]=[\mathrm{OH^-}]+[\mathrm{HS^-}]$，"
      r"用 $[\mathrm H^+]$ 表示为 $[\mathrm H^+]=\dfrac{K_w}{[\mathrm H^+]}+\dfrac{cK_1}{K_1+[\mathrm H^+]}$"
      r"（$c=1.0\times10^{-6}\ \mathrm{mol\cdot L^{-1}}$）。"
      r"解得 $[\mathrm H^+]=3.2\times10^{-7}\ \mathrm{mol\cdot L^{-1}}$ ⇒ $\mathrm{pH}=-\lg(3.2\times10^{-7})=6.49$。"
      r"（此时电离度已相当可观，说明极稀弱酸中 $K_1$ 与水的电离**必须同时计入**。）"),
     ("6-2", "3 分",
      r"沉淀反应 $\mathrm M^{2+}+\mathrm H_2S\to\mathrm{MS}+2\mathrm H^+$。"
      r"当 $[\mathrm M^{2+}]\le1.0\times10^{-6}$ 时，$0.10\ \mathrm{mol\cdot L^{-1}}$ 的 $\mathrm M^{2+}$ 已基本沉淀完，"
      r"故 $[\mathrm H^+]\approx0.20\ \mathrm{mol\cdot L^{-1}}$。"
      r"$[\mathrm S^{2-}]=\dfrac{K_1K_2[\mathrm H_2S]}{[\mathrm H^+]^2}"
      r"=\dfrac{1.3\times10^{-7}\times7.1\times10^{-15}\times0.10}{0.20^2}\approx2.1\times10^{-21}\ \mathrm{mol\cdot L^{-1}}$。"
      r"于是 $K_{sp}=[\mathrm M^{2+}][\mathrm S^{2-}]\le1.0\times10^{-6}\times2.1\times10^{-21}=2.1\times10^{-27}$，"
      r"即 $\mathrm{p}K_{sp}\ge26.68$。"),
    ],
   易错=r"① 6-1 若只列 $[\mathrm H^+]=[\mathrm{HS^-}]$ 而漏掉 $[\mathrm{OH^-}]$，在 $10^{-6}$ 级稀酸中会显著偏差；"
        r"② 6-2 的 $[\mathrm H^+]$ 由**沉淀反应完全进行**定量得到（$0.10\to0.20$），不是由 $K_a$ 算；"
        r"③ $[\mathrm S^{2-}]$ 必须用 $K_1K_2$ 两级常数相乘得到，只用 $K_2$ 会错。"),
 7: dict(
   考点=r"克劳修斯-克拉珀龙方程、原子光谱项与电离能、盖斯定律与 Born-Haber 循环"
        r"（知识点：〈Clapeyron方程〉、〈盖斯定律〉、〈Born-Haber循环〉、〈晶格能〉、〈焓变计算〉）",
   思路=r"7-1 由两个温度的蒸气压用 Clausius-Clapeyron 方程解蒸发焓；7-2 波数经 $E=N_Ahc\tilde\nu$ 换算成摩尔能量，"
        r"再加 $2.5RT$ 的平动/转动贡献得焓变；7-3 把表中 4 个反应按系数线性组合出 $\mathrm{Na+\frac12Cl_2\to NaCl(s)}$；"
        r"7-4 走 Born-Haber 循环：由生成焓倒推升华、电离、键焓、电子亲和能各步后得晶格焓。",
   步骤=[
     ("7-1", "2 分",
      r"$\ln\dfrac{p_2}{p_1}=\dfrac{\Delta H_{vap}}{R}\left(\dfrac1{T_1}-\dfrac1{T_2}\right)$，代入 $p_1=13.7$、$p_2=219.9\ \mathrm{kPa}$，"
      r"$T_1=968$、$T_2=1247\ \mathrm K$："
      r"$\ln\dfrac{219.9}{13.7}=2.776$，$\dfrac1{968}-\dfrac1{1247}=2.311\times10^{-4}\ \mathrm{K^{-1}}$，"
      r"$\Delta H_{vap}=\dfrac{2.776\times8.314}{2.311\times10^{-4}}\approx99.8\ \mathrm{kJ\cdot mol^{-1}}$。"),
     ("7-2", "2 分",
      r"$I=N_Ahc\tilde\nu=6.022\times10^{23}\times6.626\times10^{-34}\times2.998\times10^{8}\times4.1449\times10^{6}"
      r"\approx495.8\ \mathrm{kJ\cdot mol^{-1}}$"
      r"（$\tilde\nu=41449\ \mathrm{cm^{-1}}=4.1449\times10^6\ \mathrm{m^{-1}}$）。"
      r"$\Delta H_I=I+2.5RT=495.8+2.5\times8.314\times298.15\times10^{-3}=495.8+6.2=502.0\ \mathrm{kJ\cdot mol^{-1}}$。"),
     ("7-3", "2 分",
      r"按 $\mathrm{Na+\frac12Cl_2\to NaCl(s)}$ 组合表中四式（系数 $+\frac12,+\frac12,+1,-1$）："
      r"$\Delta_fH_m^\ominus(\mathrm{NaCl})=0.5\Delta H_1+0.5\Delta H_2+\Delta H_3-\Delta H_4"
      r"=0.5\times(-369.24)+0.5\times(-334.48)+(-55.72)-3.87=-411.45\ \mathrm{kJ\cdot mol^{-1}}$。"
      r"**组合思路**：$\frac12$①＋$\frac12$②得 $\mathrm{Na+\frac12Cl_2\to NaOH(aq)+HCl(aq)}$，"
      r"再加③（酸碱中和）减④（NaCl 溶解）即得目标式。"),
     ("7-4", "3 分",
      r"Born-Haber 循环：$\Delta_fH^\ominus(\mathrm{NaCl})=\Delta H_{fus}+\Delta H_{vap}+\Delta H_I+0.5\Delta H_D+\Delta H_E+\Delta H_L$，"
      r"故 $\Delta H_L=\Delta_fH^\ominus-\Delta H_{fus}-\Delta H_{vap}-0.5\Delta H_D-\Delta H_I-\Delta H_E"
      r"=-411.45-2.6-99.8-0.5\times242.6-502.04-(-349.0)\approx-788.2\ \mathrm{kJ\cdot mol^{-1}}$。"
      r"（负号表示由气态离子结合成晶体放热，量级与 NaCl 晶格能公认值一致。）"),
    ],
   易错=r"① 7-1 温度必须用**热力学温标**、蒸气压取比值；"
        r"② 7-2 波数 $\mathrm{cm^{-1}}$ 换 $\mathrm{m^{-1}}$ 要 ×100，漏乘会差 100 倍；"
        r"③ 7-3 组合系数为 $+\frac12,+\frac12,+1,-1$，符号（尤其 $-1$）易错；"
        r"④ 7-4 中 $\Delta H_E$ 本身为负值，公式里是「减去 $\Delta H_E$」⇒ 实际是加 $349.0$。"),
}
