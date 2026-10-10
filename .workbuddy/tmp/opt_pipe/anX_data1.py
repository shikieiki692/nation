# -*- coding: utf-8 -*-
"""卷 X 解析数据（第 1~5 题）。

解析**取材 03-知识点**：引真实页名，并把该页「核心原理/判据」与「易错点/迷思概念」搬进解析；
凡答案区为结构图者，**已逐张目检原图**（读图结果写入解析），不用 OCR 转述。
分步不标分值（沿用卷 XIV/XV/XIp 口径：源小问给分之和 ≠ 卷面分）。
"""

A1 = {
 1: dict(
   考点=r"高周期过渡金属的识别（Ta）· 同多酸根与 Lindqvist 结构 $[\mathrm{Ta_6O_{19}}]^{8-}$ · "
        r"过氧配合物与三角十二面体（bisdisphenoid）配位 · 由质量分数定化学式 · 18 电子规则与抗磁性"
        r"（知识点：〈多金属氧酸盐〉、〈钒的多酸〉、〈配位化学〉、〈18电子规则〉、〈元素化学〉）",
   思路=r"先用「耐王水腐蚀、溶于热浓 KOH」把 M 锁为 **Ta**；再由 `ω(O)` **反推**并**用配平复核** A／D 的化学式——"
        r"A 的阴离子是 **Lindqvist 同多酸根**（6 个 $\mathrm{TaO_6}$ 八面体共棱，$O_h$），D 是它的 Na 盐。"
        r"C 由「$\mathrm{H_2O_2}$ + 碱析出、Ta 为三角十二面体」判为**过氧配合物**（8 配位）；"
        r"E 由 `ω(O)=5.28%` 唯一确定 $\mathrm{TaOCl_3}$，再由「6 配位 + 共用 O/Cl + Ta–O–Ta 180°」画链；"
        r"F 的阳离子由题干「含 $\mathrm{Te_6}$ 六元环的无限链」直接给出；I 由「共面八面体 + 抗磁性」定。",
   步骤=[
     ("1-1", "—",
      r"M＝**Ta**。$\omega(\mathrm O)=28.67\%$ 与配平**双重校验**：$\mathrm{K_8[Ta_6O_{19}]\cdot17H_2O}$ 的 "
      r"$\omega(\mathrm O)=\frac{36\times16.00}{2008.7}=28.67\%$（⚠️ 源答案印作 $\mathrm{K_8Ta_5O_{19}\cdot17H_2O}$，但左端含 6 个 Ta、"
      r"且按 $\mathrm{Ta_5}$ 算 $\omega(\mathrm O)=31.5\%$ 不合 ⇒ 应为 **$\mathrm{K_8[Ta_6O_{19}]\cdot17H_2O}$**）。"
      r"方程式：$6\mathrm{Ta}+8\mathrm{KOH}+28\mathrm{H_2O}=\mathrm{K_8[Ta_6O_{19}]\cdot17H_2O}+15\mathrm{H_2}$；"
      r"$\mathrm{TaCl_5}+\mathrm{Cl_2O}=\mathrm{TaOCl_3}+2\mathrm{Cl_2}$。"),
     ("1-2", "—",
      r"A 的阴离子＝**Lindqvist 型** $[\mathrm{Ta_6O_{19}}]^{8-}$：6 个 $\mathrm{TaO_6}$ 八面体**共棱**连成 $O_h$ 簇，12 个端基 O 朝外；"
      r"C 的阴离子＝**过氧** $[\mathrm{Ta(O_2)_4}]^{3-}$：Ta 被 4 个 $\eta^2$-$\mathrm{O_2^{2-}}$ 包围、8 配位，"
      r"配位多面体为**三角十二面体（bisdisphenoid，$D_{2d}$）**。"),
     ("1-3", "—",
      r"E＝$\mathrm{TaOCl_3}$：$\omega(\mathrm O)=\frac{16.00}{180.95+16.00+3\times35.45}=5.28\%$ 与题给一致；"
      r"Ta 6 配位、相邻单元**共用 O 与 Cl** 连成**双一维链**，链中 $\mathrm{Ta{-}O{-}Ta}$ 约 $180^\circ$。"),
     ("1-4", "—",
      r"F 的阳离子＝含 $\mathrm{Te_6}$ 六元环的无限链 $[\mathrm{Te{-}Te{-}Te_6}]_n^{2n+}$（三配位 Te 取邻位或间位，$\mathrm{sp^3}$）；"
      r"方程式：$15\mathrm{Te}+\mathrm{TeCl_4}+4\mathrm{TaOCl_3}=(\mathrm{Te_8})_2(\mathrm{Ta_4O_4Cl_{16}})$"
      r"（Te：$15+1=16=2\times8$ ✓）。"),
     ("1-5", "—",
      r"$2(\mathrm{TaCl_4\cdot2THT})+2\mathrm{Na(Hg)}=\mathrm{Ta_2Cl_6(THT)_3}+2\mathrm{NaCl}+\mathrm{THT}+2\mathrm{Hg}$；"
      r"I 为**共面八面体**双核（有金属–金属键、含镜面而无 $C_3$ 轴），抗磁性 ⇒ **不符合 EAN 规则**"
      r"（须画出 M–M 键及其键级）。"),
     ("1-6", "—",
      r"等当量 I 与 $\mathrm{Ph_2PCH_2CH_2PPh_2}$ 取代，得「形式上二聚体」J：所有 P 均参与配位 ⇒ 以**双膦桥**把两个双核单元连成二聚结构。"),
     ("1-7", "—",
      r"L／N／O 均为 **16e** 结构：K（$\mathrm{Cp^*TaCl_3}$ 型）与 $\mathrm{PhSiH_3}$ 反应得 L；"
      r"L 与偶氮苯先释 $\mathrm{H_2}$ 得 N，再裂解得 O ⇒ 按 16e 与 N=N 断裂路径画出三者。"),
    ],
   易错=r"① 由「溶于热浓 KOH」定 Ta 后**必须用 $\omega(\mathrm O)$ 复核**化学式（源答案 Ta₅ 系印误，正解 Ta₆）；"
        r"② A 与 C 的阴离子**不是同一类**——前者是同多酸根（共棱八面体），后者是过氧 8 配位；"
        r"③ 「三角十二面体」＝**8 配位**多面体（bisdisphenoid），勿误当 12 配位；"
        r"④ E 的链靠**共用 O 与 Cl** 维系，$180^\circ$ 的 $\mathrm{Ta{-}O{-}Ta}$ 对应端基 O。",
 ),
 2: dict(
   考点=r"Zintl 相与「超原子」电子计数（Jellium 模型）· $E^{4-}$ 的电子结构 · 菱形十二面体簇 · "
        r"Mg–Mg 键与亚价铝化学 · 由质量分数定化学式"
        r"（知识点：〈原子簇化学〉、〈等电子体〉、〈8电子规则〉、〈主族元素化学〉、〈碳族元素〉）",
   思路=r"2-1 从「$E^{4-}$ 把电子交给 $\mathrm{Mg^{2+}}$」判闭壳层稳定与 n 型半导体；"
        r"2-2 系列全部**先由质量分数算 $M$**，再按对称性与配位数**拼出**结构（X 的四个 $\mathrm{AlCl_2(OEt_2)}$ 单元、"
        r"Y 的带心菱形十二面体、Z 的 $C_{3v}$）；2-2-3 用 **Jellium 能级序**做超原子电子计数；"
        r"2-3 依「先 1:1 得直线型 [A]，再被 1 分子底物还原」推 [A]、B，再按 E 的不同走 C/D·F/G。",
   步骤=[
     ("2-1", "—",
      r"$\mathrm{Mg_2E}$ 中 $E^{4-}\rightarrow \mathrm{Mg^{2+}}$ 的**电子转移**使碳族元素达 4− 的闭壳层、体系稳定；"
      r"多出的电子进入导带 ⇒ **n 型半导体**。"),
     ("2-2-1", "—",
      r"由 $\omega(\mathrm{Si})=3.923\%$（只含 1 个 Si）得 $M=\frac{28.09}{0.03923}=716.1$；扣 Si 余 688.0＝$4\times172.0$，"
      r"恰为 4 个 $\mathrm{AlCl_2(OEt_2)}$（Al 为 +3、4 配位：2 Cl ＋ 1 $\mathrm{OEt_2}$ ＋ 1 Si）⇒ "
      r"$\mathbf X=\mathrm{Si[AlCl_2(OEt_2)]_4}$：Si 居四面体心。"),
     ("2-2-2", "—",
      r"$\mathbf Y$ 的核心为**带心菱形十二面体**：中心 Si，外层 14 个 Al（8 个未被 $\mathrm{Cp^*}$ 配位、6 个被 $\mathrm{Cp^*}$ 配位）；"
      r"由 $m/z=1217$ 与只含 Si/Al/C/H 定其组成，画出菱形十二面体骨架（12 个菱形面）。"),
     ("2-2-3", "—",
      r"骨架电子数 $4+3\times8+2\times6=40$ ⇒ 按题给能级序填为 $1S^21P^61D^{10}2S^21F^{14}2P^6$（**全充满闭壳层**）⇒ "
      r"稳定性来源＝**超原子闭壳层**（Jellium 模型）。"),
     ("2-2-4", "—",
      r"$\mathbf Z=\mathrm{HSi(AlBrCp^*)_3\cdot AlBrCp^*}$（$\mathrm{AlBrCp^*}$ 为中性配体，Al 周围 10e），"
      r"$C_{3v}$：Si 居中，3 个 AlBrCp* 与 1 个游离 AlBrCp*。"),
     ("2-3-1", "—",
      r"[A]＝直线型 E 配位中间体（$\mathrm{ArN{-}Mg{-}E{-}Mg{-}NAr}$ 骨架）；B 再由底物还原得，副产含 Mg–Mg 键的 $(\mathrm{MgL})_2$。"),
     ("2-3-2", "—",
      r"$2\mathrm{Na_2(MgL)_2}+\mathrm{ECp^*_2}\rightarrow \mathrm{Na_2E(MgL)_2}+2\mathrm{NaCp^*}+(\mathrm{MgL})_2$。"),
     ("2-3-3-1", "—",
      r"E＝Sn／Pb：B 与体系中原位生成的零价 E 化合得含 **1 根 E–E 键**的 C（Mg 4 配位；Na 同时配位两个 E ⇒ 须标 Na 环境）。"),
     ("2-3-3-2", "—",
      r"E＝Si／Ge：$\mathrm E^{4-}$ 攫取 Ar 上的 H 得含 **Mg–C 键**与 1 个五元环的中间体 D，"
      r"再经分子内亲核加成得同样含五元环的 F（E 同时配位两个 Na，**须标立体化学**）。"),
     ("2-3-4", "—",
      r"E＝Sn：B 与过量 $\mathrm{N_2O}$ 反应得含 **4 个 $\mu^2$-O** 的 G（各金属取最稳定价态，不考虑 O 对 $\mathrm{Na^+}$ 的配位）。"),
    ],
   易错=r"① 2-2-1 的 $M=716$ 必须**先由质量分数算摩尔质量**再凑单元，不能臆造化学式；"
        r"② 「带心菱形十二面体」＝中心原子 ＋ 12 个菱形面（本题 Al 在**外**层）；"
        r"③ Jellium 计数中「未被 $\mathrm{Cp^*}$ 配位」与「被 $\mathrm{Cp^*}$ 配位」的 Al 各贡献 **3e⁻ 与 2e⁻**，勿一视同仁；"
        r"④ 2-3-2 用 L 表示配体，勿漏 $\mathrm{NaCp^*}$ 与 $(\mathrm{MgL})_2$。",
 ),
 3: dict(
   考点=r"硼–氟化学 · BF 与 CO 的等电子关系（配位化学上的「羰基类似物」）· 硼氟多聚物与质谱**同位素峰**"
        r"（$^{10}\mathrm B/^{11}\mathrm B$）· 由质量分数定聚合度 · 配体键角与配位方式"
        r"（知识点：〈硼化学〉、〈等电子体〉、〈质谱〉、〈过渡金属羰基化合物〉）",
   思路=r"整题围绕 **BF≡CO 的等电子关系**：先写 BF 的价电子组态，再由质谱（$m/z$）与质量分数定"
        r"各物种——D 由 $m/z=125\sim128$ 定 $\mathrm{B_3F_5}$、E 由 $\omega(\mathrm B)$ 定 $\mathrm{B_8F_{12}}$；"
        r"CO 加速分解所成的 G 由 $\nu_{\mathrm{CO}}=2162\ \mathrm{cm^{-1}}$（端基）＋ F 全同（高对称）定结构；"
        r"3-6/3-7 由 Ru–B–Ru 键角与「分子量差 28」判配位方式与键级。",
   步骤=[
     ("3-1", "—",
      r"BF 共 8 个价电子（B 3 ＋ F 7）：$(1\sigma)^2(2\sigma)^2(1\pi)^4(3\sigma)^2$，最高占据为 $\sigma$ 电子 ⇒ 抗磁性。"),
     ("3-2", "—",
      r"A＝$\mathrm{BF_3}$、C＝$\mathrm{B_2F_4}$、E＝$\mathrm{B_8F_{12}}$（$\omega(\mathrm B)=27.5\%$）；"
      r"D 由 $m/z=125\sim128$（$M\approx127$）定 $\mathrm{B_3F_5}$：画出 B–B–B 骨架 ＋ 5 个 F。"),
     ("3-3", "—",
      r"B 有 $^{10}\mathrm B$ 与 $^{11}\mathrm B$ 两种同位素，$\mathrm{B_3}$ 共 $2^3=4$ 种组合 ⇒ 出现 4 个分子离子峰；"
      r"自然界 F 只有 $^{19}\mathrm F$ ⇒ 若答「F 的同位素」不得分。"),
     ("3-4", "—",
      r"$4\mathrm{B_3F_5}=\mathrm{B_8F_{12}}+2\mathrm{B_2F_4}$。"),
     ("3-5-1", "—",
      r"G＝$\mathrm{B_4F_6CO}$：$\nu_{\mathrm{CO}}=2162\ \mathrm{cm^{-1}}$ ⇒ CO 为**端基**；$^{19}\mathrm F$-NMR 仅一种 F ⇒ 结构高对称；"
      r"H 由 $\omega(\mathrm B)=17.64\%$ 定，与 G 同构（$\mathrm{PF_3}$ 代 CO）。"),
     ("3-5-2", "—",
      r"$2\mathrm{B_3F_5}=\mathrm{B_2F_4}+\mathrm{B_4F_6CO}$。"),
     ("3-6", "—",
      r"P／$\mathrm{Q^+}$／R 为 **Ru–B–Ru** 桥联的双核：$\mathrm{Q^+}$ 的 Ru–B–Ru＝$175.5^\circ$（近直线）；"
      r"R 比 P 少 28（失 1 个 CO）、且 Ru···Ru 明显缩短 ⇒ 分别画出 BF 桥联方式与键级变化。"),
     ("3-7-1", "—",
      r"X、Y 为 $\mathrm{BO^-}$ 配位的 Pt 化合物；Y 为 $\mathrm{Pt(PCy_3)_2(BO)}$ 型，**须体现 Pt–B–O 键角**。"),
     ("3-7-2", "—",
      r"与 $\mathrm{AlBr_3}$ 配位的是 **O**（B 已被 Pt 配位）；配位后 Pt–B–O 键角**基本不变**。"),
     ("3-7-3", "—",
      r"银盐 $\mathrm{Ag[Al(OC(CH_3)_3)_4]}$ 处理 Y，得带 2 个正电的双核配离子 Z（Pt 为 3 配位）。"),
    ],
   易错=r"① 质谱多峰来源是 **B 的同位素**（$^{10}\mathrm B/^{11}\mathrm B$），不是 F；"
        r"② 3-8 的给分关键词是「BF 与 CO 为**等电子体/前线轨道相似**」；"
        r"③ $\mathrm{B_4F_6CO}$ 的 CO 为**端基**（2162 cm⁻¹），区别于桥基 CO（<1900 cm⁻¹）；"
        r"④ $\omega(\mathrm B)$ 用于定 E／H 的**聚合度**，务必先算 $M$ 再定下标。",
 ),
 4: dict(
   考点=r"碲的元素化学与链状结构（$\mathrm{Te_2Br}$ 共棱六元环、TeI 链）· "
        r"重铬酸钾–亚铁铵**返滴定**与计量关系（$1\ \mathrm{Cr_2O_7^{2-}}\sim6\ \mathrm{Fe^{2+}}$）· 质量分数计算"
        r"（知识点：〈元素化学〉、〈氧族元素〉、〈氧化还原滴定〉、〈碘量法〉）",
   思路=r"4-1 纯结构题，按题干「共棱六元 Te 环 + Br 桥联相间 Te」与「Te 链 + I 桥联相间 Te」照画；"
        r"4-2 先写**氧化 Te(IV)→Te(VI)** 与**滴定 $\mathrm{Fe^{2+}}$** 两支方程，"
        r"再用**返滴定差值**取 $n(\mathrm{Cr_2O_7^{2-}})_{\text{反应}}$，最后按 $3\mathrm{Te}\sim1\mathrm{Cr_2O_7^{2-}}$ 换算 $\omega(\mathrm{Te})$。",
   步骤=[
     ("4-1", "—",
      r"$\mathrm{Te_2Br}$：**共棱**连接的六元 Te 环沿链延伸，Br 桥联「相间的两个 Te」；"
      r"TeI：一条 Te 链，一半 Te 只连 1 个 I，另一半 Te 与相间 Te **共享同一个 I**（照画即可）。"),
     ("4-2-1", "—",
      r"$3\mathrm{H_2TeO_3}+\mathrm{Cr_2O_7^{2-}}+8\mathrm{H^+}+2\mathrm{H_2O}=3\mathrm{H_6TeO_6}+2\mathrm{Cr^{3+}}$；"
      r"$\mathrm{Cr_2O_7^{2-}}+6\mathrm{Fe^{2+}}+14\mathrm{H^+}=2\mathrm{Cr^{3+}}+6\mathrm{Fe^{3+}}+7\mathrm{H_2O}$。"),
     ("4-2-2", "—",
      r"返滴定：$n(\mathrm{Cr_2O_7^{2-}})_{\text{余}}=\frac{15.67\times0.2005}{6\times1000}$；"
      r"$n_{\text{反应}}=40.02\times0.02334\times10^{-3}-n_{\text{余}}=4.104\times10^{-4}\ \mathrm{mol}$；"
      r"$\omega(\mathrm{Te})=\frac{3\times4.104\times10^{-4}\times127.6}{0.3631}=43.27\%$。"),
    ],
   易错=r"① 返滴定必须用**差值** $n_{\text{反应}}=n_{\text{总}}-n_{\text{余}}$，且 $1\ \mathrm{Cr_2O_7^{2-}}\sim6\ \mathrm{Fe^{2+}}$；"
        r"② 第一步是把 $\mathrm{Te^{IV}}$ 氧化到 $\mathrm{Te^{VI}}$（$\mathrm{H_2TeO_3}\rightarrow\mathrm{H_6TeO_6}$），"
        r"$1\ \mathrm{Cr_2O_7^{2-}}$ 对应 **3 个 Te**；"
        r"③ $\mathrm{Te_2Br}$ 是**共棱六元环**、TeI 是**链**，勿画成同一拓扑。",
 ),
 5: dict(
   考点=r"硒的含氧酸与含氟酸（$\mathrm{HOSeF_5}$）· 卤素互化物与拟卤素类比（$\mathrm{SeCN}$）· "
        r"歧化/水解方程式的配平 · 由质量分数推断元素与物种"
        r"（知识点：〈元素化学〉、〈卤素互化物〉、〈无机酸〉、〈软硬酸碱理论〉）",
   思路=r"推断钥匙有三：① 名称「满月女神塞勒涅」＋ $\omega(\mathrm X)=41.35\%$ ⇒ **Se**；"
        r"② 「溶于金的氧化性酸」B＝$\mathrm{H_2SeO_4}$ ⇒ C＝$\mathrm{H_2SeO_3}$、HA＝$\mathrm{HOSeF_5}$；"
        r"③ 反应 4~8 全部围绕 $\mathrm{Se_2(CN)_2}$ 的水解/歧化与 $\mathrm{SeCN}$ 的拟卤素行为，按**守恒**配平即可。",
   步骤=[
     ("5-1-1", "—",
      r"X＝**硒**；HA＝$\mathrm{HOSeF_5}$（$\omega(\mathrm{Se})=\frac{78.97}{190.9}=41.35\%$ 自洽）；"
      r"B＝$\mathrm{H_2SeO_4}$、C＝$\mathrm{H_2SeO_3}$。"
      r"反应 1：$6\mathrm{H_2SeO_4}+2\mathrm{Au}=\mathrm{Au_2(SeO_4)_3}+3\mathrm{H_2SeO_3}+3\mathrm{H_2O}$；"
      r"反应 2：$\mathrm{H_2SeO_4}+2\mathrm{HY}=\mathrm{H_2SeO_3}+\mathrm{Y_2}+\mathrm{H_2O}$。"),
     ("5-1-2", "—",
      r"$\mathrm{ClA}=\mathrm{ClSeOF_5}$ 在潮湿空气中水解、**无价态变化**（仅歧化 Cl 的环境）："
      r"$2\mathrm{ClSeOF_5}+\mathrm{H_2O}=\mathrm{Cl_2O}+2\mathrm{HOSeF_5}$。"),
     ("5-2", "—",
      r"反应 4：$2\mathrm{Se_2(CN)_2}+3\mathrm{H_2O}=\mathrm{HCN}+\mathrm{H_2SeO_3}+3\mathrm{HSeCN}$；"
      r"反应 5：$2\mathrm{Se_2(CN)_2}=\mathrm{Se(CN)_2}+\mathrm{Se(SeCN)_2}$（等物质的量歧化）；"
      r"反应 6：$5\mathrm{Se(CN)_2}+6\mathrm{H_2O}=2\mathrm{H_2SeO_3}+8\mathrm{HCN}+\mathrm{Se(SeCN)_2}$；"
      r"反应 7：$\mathrm{CsSeCN}+\mathrm{Se_2(CN)_2}=\mathrm{Cs[SeCN]_3}$；"
      r"反应 8：$3\mathrm{H_2SeO_3}+7\mathrm{HSCN}=3\mathrm{Se(SCN)_2}+5\mathrm{H_2O}+\mathrm{HCN}+\mathrm{H_2SO_4}$。"),
    ],
   易错=r"① 推断的两把钥匙是「满月女神 ＋ $\omega=41.35\%$」＝Se 与「溶金的氧化性酸」＝$\mathrm{H_2SeO_4}$；"
        r"② 反应 5/6 是 $\mathrm{Se(CN)_2}$ 体系的**歧化**，H 的 $\omega(\mathrm{Se})=81.99\%$ 可锁 $\mathrm{Se(SeCN)_2}$；"
        r"③ 反应 8 的两种产物酸**均不含 Se**（HCN 与 $\mathrm{H_2SO_4}$）。",
 ),
}
