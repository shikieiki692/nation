#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""add_analysis_XIII.py —— 给卷 XIII 答案版逐题在答案区尾部追加「解析（据源答案整理）」。

v2（2026-10-08）：① 解析**全面 LaTeX 化**（原版为 Unicode 上下标与纯文本公式）；
                  ② 小问编号**对齐卷内题号**（原版沿用源卡题号，如第 1 题却写 6-1）。
幂等（已有「> **解析**」则跳过）；仅动答案版 md，不动 FM/题面。
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
MD = os.path.join(R, "04-题库", "初赛模拟卷XIII（非有机·答案版）.md")

A = {
 1: "考查热化学与电解效率。"
    r"1-1：反应 $\mathrm{CH_3OH(g)} = \mathrm{CO(g)} + 2\mathrm{H_2(g)}$，由生成焓数据 "
    r"$Q_{p,m} = \Delta_r H_m^\ominus = -110.5-(-200.7) = +90.2\ \mathrm{kJ\cdot mol^{-1}}$（吸热）；气相 $\Delta n = 2$，"
    r"$W = -\Delta nRT = -2\times 8.314\times 298.15\times 10^{-3} \approx -4.96\ \mathrm{kJ\cdot mol^{-1}}$，"
    r"恒压 $\Delta H = \Delta U + \Delta nRT$ ⇒ $Q_{V,m} = \Delta U = Q_{p,m} + W \approx 85.2\ \mathrm{kJ\cdot mol^{-1}}$。"
    r"1-2：$\Delta_r H_m^\ominus > 0$，由 van't Hoff 等压方程 $\mathrm{d}\ln K^\ominus/\mathrm{d}T = \Delta_r H_m^\ominus/(RT^2) > 0$，"
    r"$K^\ominus$ 随 $T$ 升高而增大，故升温对甲醇裂解有利。"
    r"1-3：水分解 $\mathrm{H_2O(l)} \to \mathrm{H_2(g)} + \frac{1}{2}\mathrm{O_2(g)}$（阳极析氧超电势 0.9 V、阴极析氢 1.5 V），"
    r"$\Delta_r G_m^\ominus = -\Delta_f G_m^\ominus(\mathrm{H_2O,l}) = 237.1\ \mathrm{kJ\cdot mol^{-1}}$，"
    r"理论分解电压 $E^\ominus = \Delta_r G_m^\ominus/(nF) = 237.1\times 10^3/(2\times 96485) \approx 1.229\ \mathrm{V}$；"
    r"实际电解电压 $U = E^\ominus + 0.9 + 1.5 = 3.63\ \mathrm{V}$；电解效率 "
    r"$= (E^\ominus/U)\times(1-35\%) = (1.229/3.63)\times 0.65 \approx 22\%$。"
    r"1-4：1 mol 甲醇裂解吸热 $90.2\ \mathrm{kJ}$；$\mathrm{H_2}$ 燃烧生成 $\mathrm{H_2O(g)}$ 的 "
    r"$\Delta_r H_m^\ominus = -285.8+44.0 = -241.8\ \mathrm{kJ\cdot mol^{-1}}$，其中 70% 用于供热 ⇒ 需 "
    r"$\mathrm{H_2}$ 为 $90.2/(241.8\times 0.70) \approx 0.53\ \mathrm{mol}$；每摩尔甲醇产 2 mol $\mathrm{H_2}$，"
    r"扣除自耗 0.53 mol 后净得 1.47 mol，生成氢效率 $1.47/2 \approx 73\%$。",
 2: "考查相平衡与熔化热力学。"
    r"2-1：由基尔霍夫定律 $\Delta_{\mathrm{mel}}H_m(T) = \Delta_{\mathrm{mel}}H_m(T_m) + \Delta C_{p,m}(T-T_m)$，"
    r"其中 $T_m = 1808\ \mathrm{K}$、$\Delta_{\mathrm{mel}}H_m(T_m) = 15355\ \mathrm{J\cdot mol^{-1}}$、"
    r"$\Delta C_{p,m} = 1.255\ \mathrm{J\cdot K^{-1}\cdot mol^{-1}}$ ⇒ "
    r"$\Delta_{\mathrm{mel}}H_m = (1.255\,T/\mathrm{K} + 13086)\ \mathrm{J\cdot mol^{-1}}$。"
    r"2-2：正常熔点 1808 K 处熔化处于平衡，$\Delta_{\mathrm{mel}}S_m(1808\ \mathrm{K}) = 15355/1808 \approx 8.49\ \mathrm{J\cdot K^{-1}\cdot mol^{-1}}$；"
    r"经 $\Delta C_p$ 项修正 $\Delta_{\mathrm{mel}}S_m(1673\ \mathrm{K}) = 8.49 + 1.255\ln(1673/1808) \approx 8.40\ \mathrm{J\cdot K^{-1}\cdot mol^{-1}}$；"
    r"$\Delta_{\mathrm{mel}}H_m(1673\ \mathrm{K}) = 1.255\times 1673 + 13086 \approx 15186\ \mathrm{J\cdot mol^{-1}}$；"
    r"$\Delta_{\mathrm{mel}}G_m^\ominus = \Delta_{\mathrm{mel}}H_m - T\Delta_{\mathrm{mel}}S_m \approx 1.13\ \mathrm{kJ\cdot mol^{-1}}$，"
    r"故 $K^\ominus = \exp(-\Delta_{\mathrm{mel}}G_m^\ominus/RT) \approx 0.92$。"
    r"（注：源答案将 $\Delta_{\mathrm{mel}}S_m(1808\ \mathrm{K})$ 印作 $8.59\ \mathrm{J\cdot K^{-1}\cdot mol^{-1}}$，与 $15355/1808$ 不符，系笔误；"
    r"修正后 $K^\ominus \approx 0.92$，与其印值 0.931 的差异不改变下文两位有效数字的结论。）"
    r"2-3：该温度下 $\delta\text{-}\mathrm{Fe(s)}$ 与含 Fe 的硫化铁熔体两相平衡，"
    r"$K^\ominus = a(\mathrm{Fe,l}) = \gamma x$（$x = 0.87$）⇒ $\gamma = K^\ominus/x \approx 0.92/0.87 \approx 1.06 \approx 1.1$。",
 3: "考查稀溶液气液平衡与恒沸。"
    r"3-1：以 40 ℃（313.15 K）的 $p_A^* = 0.42\ \mathrm{atm}$、$p_B^* = 0.98\ \mathrm{atm}$ 为基准，"
    r"用克拉佩龙-克劳修斯式 $\ln[p^*(T)/p^*(313.15)] = (\Delta_{\mathrm{vap}}H_m/R)(1/313.15 - 1/T)$ 外推。"
    r"3-1-1：正常沸点处 $p_{\text{总}} = 1\ \mathrm{atm}$，故 "
    r"$0.75\,p_A^*(T) + 0.25\,p_B^*(T) = 1$，解得 $T \approx 330.4\ \mathrm{K}$；"
    r"此时 $p_A = 0.565\ \mathrm{bar}$、$p_B = 0.435\ \mathrm{bar}$，气相丙酮摩尔分数 $y_A = p_A/(p_A+p_B) = 0.565$。"
    r"3-1-2：已知气相组成 $y_A = 0.75$，由 $p_A = x_A p_A^*(T) = y_A p$、$p_B = (1-x_A)p_B^*(T) = (1-y_A)p$ 联立求沸点与液相组成，"
    r"得 $T \approx 334.5\ \mathrm{K}$、$x_A \approx 0.874$。"
    r"3-2：由 Margules 式 $\gamma_A = \exp(A x_B^2)$、$\gamma_B = \exp(A x_A^2)$（$A = 0.90$，$x_A = 0.75$、$x_B = 0.25$）"
    r"得 $\gamma_A \approx 1.058$、$\gamma_B \approx 1.659$；以修正的拉乌尔定律 "
    r"$x_A\gamma_A p_A^*(T) + x_B\gamma_B p_B^*(T) = 1$ 求沸点，解得 $T \approx 321.9\ \mathrm{K}$。"
    r"3-3-1：恒沸时气液两相组成相同，$y_A = x_A$ ⇒ $\gamma_A p_A^* = \gamma_B p_B^*$ ⇒ $A(x_B^2 - x_A^2) = \ln(p_B^*/p_A^*)$；"
    r"以 $x_B = 1-x_A$ 化简得 $A(1-2x_A) = \ln(p_B^*/p_A^*)$，即 $x_A = \frac{1}{2} - \frac{1}{2A}\ln(p_B^*/p_A^*)$。"
    r"3-3-2：代入 $A = 0.90$ 与 $p_A^*$、$p_B^*$（二者之比 40 ℃ 时为 2.33）得 $x_A \approx 0.0293$；"
    r"恒沸压力 $p = \gamma_A x_A p_A^* + \gamma_B x_B p_B^* \approx 0.981\ \mathrm{atm}$。",
 4: "考查沉淀-配位多重平衡。"
    r"4-1：设 1 L 氨水溶解 AgCl 达饱和，溶解量为 $s\ \mathrm{mol/L}$。由 $[\mathrm{Ag^+}][\mathrm{Cl^-}] = K_{sp}$ 及 "
    r"$[\mathrm{Cl^-}] = [\mathrm{Ag^+}]\left(1 + \beta_1[\mathrm{NH_3}] + \beta_2[\mathrm{NH_3}]^2\right)$ 得 "
    r"$[\mathrm{Ag^+}] = \sqrt{K_{sp}/\left(1 + \beta_1[\mathrm{NH_3}] + \beta_2[\mathrm{NH_3}]^2\right)}$；"
    r"氨的物料守恒 $1.00 = [\mathrm{NH_3}] + [\mathrm{NH_4^+}] + [\mathrm{Ag(NH_3)^+}] + 2[\mathrm{Ag(NH_3)_2^+}]$；"
    r"联立解得 $[\mathrm{NH_3}] \approx 0.794\ \mathrm{mol/L}$、$s \approx 0.101\ \mathrm{mol/L}$，"
    r"故 $m = s\,M(\mathrm{AgCl}) \approx 0.101\times 143.4 \approx 14.5\ \mathrm{g}$。"
    r"4-2：完全溶解 1.50 g AgCl 于 2.0 L ⇒ $c(\mathrm{Cl^-}) = 1.50/(143.4\times 2.0) \approx 5.23\times 10^{-3}\ \mathrm{mol/L}$，"
    r"$[\mathrm{Ag^+}] = K_{sp}/[\mathrm{Cl^-}] \approx 3.40\times 10^{-8}\ \mathrm{mol/L}$；"
    r"由溶解守恒解得 $[\mathrm{NH_3}] \approx 0.0416\ \mathrm{mol/L}$；再由电荷守恒得 $[\mathrm{NH_4^+}] \approx 8.70\times 10^{-4}\ \mathrm{mol/L}$，"
    r"故氨水最低总浓度 $c = [\mathrm{NH_3}] + [\mathrm{NH_4^+}] + [\mathrm{Ag(NH_3)^+}] + 2[\mathrm{Ag(NH_3)_2^+}] \approx 0.0529\ \mathrm{mol/L}$。",
 5: "考查 Latimer 电势图与电化学计算。"
    r"5-1：歧化反应 $2\mathrm{VO^{2+}} \to \mathrm{VO_2^+} + \mathrm{V^{3+}}$，"
    r"$\Delta_r G_m^\ominus = -nF\Delta E^\ominus = -1\times F\times(0.337-1.0) \approx +63.9\ \mathrm{kJ\cdot mol^{-1}} > 0$，"
    r"即歧化不能正向自发，故 $\mathrm{VO^{2+}}$ 不易发生歧化。"
    r"5-2-1：由连续电势对电子的加权平均关系 $(1.0+0.337+E_X)/3 = 0.361$ ⇒ $E_X \approx -0.254\ \mathrm{V}$（即 $E^\ominus(\mathrm{V^{3+}/V^{2+}})$）。"
    r"5-2-2：$\mathrm{V^{2+}}$ 被 $\mathrm{H^+}$ 氧化：$\mathrm{V^{2+}} + \mathrm{H^+} \to \mathrm{V^{3+}} + \frac{1}{2}\mathrm{H_2}$，"
    r"$\Delta_r G_m^\ominus = -1\times F\times(-0.254-0) \approx +24.5\ \mathrm{kJ\cdot mol^{-1}} > 0$，反应不能自发，"
    r"故 $\mathrm{V^{2+}}$ 在无氧条件下可热力学稳定存在。"
    r"5-3-1：$2\mathrm{VO^{2+}} + \mathrm{H_2} + 2\mathrm{H^+} \to 2\mathrm{V^{3+}} + 2\mathrm{H_2O}$，"
    r"$\Delta_r G_m^\ominus = -2F\times(0.337-0) \approx -65.0\ \mathrm{kJ\cdot mol^{-1}}$，"
    r"$K^\ominus = \exp(-\Delta_r G_m^\ominus/RT) \approx 2.5\times 10^{11}$。"
    r"5-3-2：$K^\ominus = [\mathrm{V^{3+}}]^2/\left([\mathrm{VO^{2+}}]^2[\mathrm{H^+}]^2\,p(\mathrm{H_2})/p^\ominus\right) = \alpha^2/[(1-\alpha)^2 (10^{-\mathrm{pH}})^2]$；"
    r"取 pH = 4.15 解得 $\alpha \approx 1$（近乎完全还原）。"
    r"5-3-3：取 $\alpha = 0.995$ 反解最大允许 pH，得 pH ≈ 3.40。"
    r"5-3-4：由 $\Delta E^\ominus = -\Delta_r H_m^\ominus/(zF) + [\Delta_r S_m^\ominus/(zF)]T$，斜率 "
    r"$\mathrm{d}E^\ominus/\mathrm{d}T = \Delta_r S_m^\ominus/(zF) = -1.75\times 10^{-3}\ \mathrm{V\cdot K^{-1}}$ ⇒ "
    r"$\Delta_r S_m^\ominus = zF\times(-1.75\times 10^{-3}) \approx -337.7\ \mathrm{J\cdot K^{-1}\cdot mol^{-1}}$（$z = 2$）；"
    r"再由题给各物质标准熵求 $\Delta_r H_m^\ominus = \Delta_r G_m^\ominus + T\Delta_r S_m^\ominus \approx -165.7\ \mathrm{kJ\cdot mol^{-1}}$。",
 6: "考查二组分理想液态混合物的气液平衡。"
    r"6-1：先用克拉佩龙-克劳修斯方程由溴苯的正常沸点求 407 K 时的饱和蒸气压，"
    r"$\ln[p_B^*(407\ \mathrm{K})/101.325\ \mathrm{kPa}] = (\Delta_{\mathrm{vap}}H_m(B)/R)(1/429-1/407)$，得 $p_B^* \approx 51.6\ \mathrm{kPa}$；"
    r"由 $x_A = 0.9$、$x_B = 0.1$ 的混合物在 407 K 恰好沸腾（$p = 101.325\ \mathrm{kPa}$）反解："
    r"$101.325 = 0.9p_A^* + 0.1p_B^*$ ⇒ $p_A^* \approx 106.8\ \mathrm{kPa}$。"
    r"再对 $x_A = 0.4$、$x_B = 0.6$ 求出现第一个气泡（液相组成基本不变）时的总压 "
    r"$p_1 = 0.4p_A^* + 0.6p_B^* \approx 73.7\ \mathrm{kPa}$，气相组成 $y_A = 0.4p_A^*/p_1 \approx 0.58$（$y_B \approx 0.42$）。"
    r"6-2：蒸馏至剩最后一滴液体时，可近似认为气相组成等于原液相组成，即 $y_A = 0.4$、$y_B = 0.6$；"
    r"由 $p_A = p_A^* x_A = y_A p_2$、$p_B = p_B^* x_B = y_B p_2$ 及 $x_A + x_B = 1$ 联立，"
    r"解得 $x_A \approx 0.24$、$x_B \approx 0.76$，此时总压 $p_2 \approx 65.4\ \mathrm{kPa}$。",
 7: "考查化学平衡与弱酸溶解。"
    r"7-1：$4\mathrm{NO} + 3\mathrm{O_2} + 2\mathrm{H_2O} \to 4\mathrm{HNO_3}$；"
    r"$2\mathrm{SO_2} + \mathrm{O_2} + 2\mathrm{H_2O} \to 2\mathrm{H_2SO_4}$。"
    r"7-2：$2\mathrm{NO} + \mathrm{O_2} \rightleftharpoons 2\mathrm{NO_2}$，"
    r"$\Delta_r H_m^\ominus = 2\times 33.2 - 2\times 91.3 = -116.2\ \mathrm{kJ\cdot mol^{-1}}$，"
    r"$\Delta_r S_m^\ominus = 2\times 240.1 - 2\times 210.8 - 205.2 = -146.6\ \mathrm{J\cdot K^{-1}\cdot mol^{-1}}$，"
    r"$\Delta_r G_m^\ominus = -116.2 - 600\times(-0.1466) \approx -28.2\ \mathrm{kJ\cdot mol^{-1}}$，"
    r"$K^\ominus = \exp(-\Delta_r G_m^\ominus/RT) \approx 285$；设 NO 转化率为 $x$（初始 NO:O₂ = 2:1），"
    r"平衡 $n(\mathrm{NO}) = 2-2x$、$n(\mathrm{O_2}) = 1-x$、$n(\mathrm{NO_2}) = 2x$、$\sum n = 3-x$，代入分压式解得 $x \approx 0.83$。"
    r"7-3：$2\mathrm{SO_2} + \mathrm{O_2} \rightleftharpoons 2\mathrm{SO_3}$，"
    r"$\Delta_r H_m^\ominus = 2\times(-395.7) - 2\times(-296.8) = -197.8\ \mathrm{kJ\cdot mol^{-1}}$，"
    r"$\Delta_r S_m^\ominus = 2\times 256.8 - 2\times 248.2 - 205.2 = -188.0\ \mathrm{J\cdot K^{-1}\cdot mol^{-1}}$，"
    r"$\Delta_r G_m^\ominus = -197.8 - 900\times(-0.188) \approx -28.6\ \mathrm{kJ\cdot mol^{-1}}$，$K^\ominus \approx 45.7$；"
    r"设反应进度 $x\ \mathrm{mol}$（$\mathrm{SO_2}$、$\mathrm{O_2}$ 各 1 mol），代入分压式解得 $x \approx 0.42$，"
    r"平衡总量 $2-x\ \mathrm{mol}$，$p = (2-x)RT/V \approx 1.48\ \mathrm{bar}$。"
    r"7-4：由 $\mathrm{SO_2}$ 浓度峰值 $c = 500\times 10^{-6}\ \mathrm{g/m^3}$ 得分压 "
    r"$p = cRT/M = (500\times 10^{-6}/64)\times 8.314\times 298 \approx 0.0194\ \mathrm{Pa}$，"
    r"$c(\mathrm{H_2SO_3}) = K_H\,(p/101325) = 1.36\times 0.0194/101325 \approx 2.60\times 10^{-7}\ \mathrm{mol/L}$；"
    r"由质子条件 $[\mathrm{H^+}] = [\mathrm{HSO_3^-}] + 2[\mathrm{SO_3^{2-}}] + [\mathrm{OH^-}]$ 及各电离平衡代入，"
    r"解得 $[\mathrm{H^+}] \approx 6.0\times 10^{-5}$ ⇒ pH ≈ 4.22。",
 8: "考查缓冲溶液与沉淀-配位耦合。"
    r"8-1：$n(\mathrm{NaAc}) = 0.125/82.03 \approx 1.52\times 10^{-3}\ \mathrm{mol}$，"
    r"$c(\mathrm{NaAc}) = 1.52\times 10^{-3}/0.020 \approx 0.0762\ \mathrm{mol/L}$；"
    r"因 NaAc 远多于 HAc，HAc 解离受同离子抑制，$c(\mathrm{HAc}) \approx 7.5\times 10^{-4}\ \mathrm{mol/L}$，"
    r"由缓冲公式 pH $= \mathrm{p}K_a + \lg\frac{c(\mathrm{Ac^-})}{c(\mathrm{HAc})} = 4.75 + \lg\frac{0.0762}{7.5\times 10^{-4}} \approx 6.76$。"
    r"8-2：判据为 PbSO₄ 的溶解守恒与 Pb-醋酸配合物的多重平衡。若完全溶解，则 $c(\mathrm{Pb}) = [\mathrm{SO_4^{2-}}]$ 且 "
    r"$[\mathrm{Pb^{2+}}][\mathrm{SO_4^{2-}}] = K_{sp}$；而 $c(\mathrm{Pb}) = [\mathrm{Pb^{2+}}](1 + \beta_1[\mathrm{Ac^-}] + \beta_2[\mathrm{Ac^-}]^2 + \beta_3[\mathrm{Ac^-}]^3)$。"
    r"又由醋酸-醋酸钠总量守恒 $c(\mathrm{HAc}) + c(\mathrm{NaAc}) = [\mathrm{HAc}] + [\mathrm{Ac^-}] + [\mathrm{Pb^{2+}}](\beta_1[\mathrm{Ac^-}] + 2\beta_2[\mathrm{Ac^-}]^2 + 3\beta_3[\mathrm{Ac^-}]^3)$，"
    r"因 $c(\mathrm{HAc})/c(\mathrm{NaAc}) \approx 0.01$ 可视 HAc 基本不变；联立解得 $[\mathrm{Ac^-}] \approx 0.066\ \mathrm{mol/L}$。"
    r"据此，0.040 g PbSO₄ 在本缓冲液中**不能完全溶解**（与源答案结论一致）。",
 9: "考查化学平衡与 van't Hoff 方程。"
    r"9-1：$\mathrm{CH_4(g)} + \mathrm{H_2O(g)} \to \mathrm{CO(g)} + 3\mathrm{H_2(g)}$。"
    r"9-2：由 van't Hoff 等压方程 $\ln\frac{K^\ominus(298)}{K^\ominus(1580)} = -\frac{\Delta_r H_m^\ominus}{R}\left(\frac{1}{298}-\frac{1}{1580}\right)$ "
    r"解得 $\Delta_r H_m^\ominus \approx 2.06\times 10^{5}\ \mathrm{J\cdot mol^{-1}}$；再由 "
    r"$\ln K^\ominus(1100) = \ln K^\ominus(298) - \frac{\Delta_r H_m^\ominus}{R}\left(\frac{1}{1100}-\frac{1}{298}\right)$ 得 $K^\ominus \approx 28.4$，"
    r"$\Delta_r G_m^\ominus = -RT\ln K^\ominus \approx -3.06\times 10^{4}\ \mathrm{J\cdot mol^{-1}}$，"
    r"$\Delta_r S_m^\ominus = (\Delta_r H_m^\ominus - \Delta_r G_m^\ominus)/1100 \approx 215\ \mathrm{J\cdot K^{-1}\cdot mol^{-1}}$。"
    r"9-3：设 $\mathrm{CH_4}$ 转化率为 $x$，平衡 $n(\mathrm{CH_4}) = n(\mathrm{H_2O}) = 1-x$、$n(\mathrm{CO}) = x$、$n(\mathrm{H_2}) = 3x$，"
    r"$\sum n = 2+2x$，气相 $\Delta\nu = 2$；由 $K^\ominus = K_x (p/p^\ominus)^2$ 代入 $p = 1.60\ \mathrm{bar}$ 解得 $x \approx 0.749$。"
    r"9-4：$\Delta\nu(\mathrm{g}) = 2 > 0$，加压使平衡向气体分子数减小（逆向）的方向移动，"
    r"$(\partial\ln K_x/\partial p)_T = -\Delta\nu/p < 0$，故加压不利于提高转化率。"
    r"9-5：$\Delta_r H_m^\ominus > 0$（吸热），$(\partial\ln K^\ominus/\partial T)_p = \Delta_r H_m^\ominus/(RT^2) > 0$ ⇒ $K^\ominus$ 随温度升高而增大，"
    r"故升温对提高转化率有利。",
 10: "考查热化学与相平衡。"
     r"10-1：$\mathrm{H_2} + \frac{1}{2}\mathrm{O_2} \to \mathrm{H_2O(l)}$，$\Delta_r H_m^\ominus = -285.8\ \mathrm{kJ\cdot mol^{-1}}$，气相 $\Delta n = -1.5$ ⇒ "
     r"$\Delta_r U_m^\ominus = \Delta_r H_m^\ominus - \Delta nRT \approx -282.1\ \mathrm{kJ\cdot mol^{-1}}$；"
     r"0.30 mol $\mathrm{H_2}$ 放热 $0.30\times 282.1 \approx 84.6\ \mathrm{kJ}$ 使水温升 5.212 K，得量热计热容 $C \approx 16.24\ \mathrm{kJ\cdot K^{-1}}$；"
     r"2.345 g 正癸烷（$M = 142.29$）为 0.01648 mol，水温升 6.862 K ⇒ 放热 $C\times 6.862 \approx 111.4\ \mathrm{kJ}$，"
     r"$\Delta_r U_m^\ominus \approx -111.4/0.01648 \approx -6.76\times 10^{3}\ \mathrm{kJ\cdot mol^{-1}}$；"
     r"燃烧 $\mathrm{C_{10}H_{22}} + 15.5\mathrm{O_2} \to 10\mathrm{CO_2} + 11\mathrm{H_2O(l)}$，气相 $\Delta n = 10-15.5 = -5.5$，"
     r"$\Delta_r H_m^\ominus = \Delta_r U_m^\ominus + \Delta nRT \approx -6.77\times 10^{3}\ \mathrm{kJ\cdot mol^{-1}}$。"
     r"10-2：分别按生成 $\mathrm{CO_2}$（$\Delta_f H_m^\ominus = -393.51$）与 $\mathrm{CO}$（$\Delta_f H_m^\ominus = -110.52$）计算熔化冰与燃烧碳的质量比 "
     r"$m(\text{冰})/m(\mathrm{C}) = |\Delta H|\times 18.02/(6.007\times 12.01)$，得 98.27（$\mathrm{CO_2}$）与 27.60（$\mathrm{CO}$）；"
     r"实验值 96.5、69、40 均介于两者之间，说明碳发生了不完全燃烧、产物为 CO 与 $\mathrm{CO_2}$ 的混合物，故可解释数据差异。"
     r"10-3：金星大气压下水中 $\mathrm{CO_2}$ 质量分数 7.50% ⇒ 每 1 L 水溶 $\mathrm{CO_2}$ $1000\times 0.075/44.01 \approx 1.704\ \mathrm{mol}$，"
     r"即约 $1.842\ \mathrm{mol/kg}$（按 1 kg 溶剂计）；由依数性造成凝固点降低 $1.842\times 1.86 \approx 3.43\ \mathrm{K}$，"
     r"得仅由浓度引起的熔点约 $273.16-3.43 = 269.73\ \mathrm{K}$；与实测 269.29 K 之差 0.44 K 即压强引起的降低。"
     r"$\Delta p = 93\times 101325 - 610.48 \approx 9.42\times 10^{6}\ \mathrm{Pa}$，由固液平衡的克拉佩龙方程近似 "
     r"$\mathrm{d}T/\mathrm{d}p \approx -0.44/9.42\times 10^{6} \approx -4.7\times 10^{-8}\ \mathrm{K\cdot Pa^{-1}}$；"
     r"因冰熔化体积减小，由勒夏特列原理加压使熔化更有利，故熔点随压强下降、斜率小于零。",
}

txt = open(MD, encoding="utf-8-sig").read().replace("\r\n", "\n")
if "> **解析**（据源答案整理）" in txt:
    print("已存在解析，跳过（如需重写请先重出卷 md）")
    sys.exit(0)
lines = txt.split("\n")
heads = [(i, int(m.group(1))) for i, l in enumerate(lines)
         for m in [re.match(r"^### 第 (\d+) 题", l)] if m]
heads.append((len(lines), None))
out, done = list(lines[:heads[0][0]]), 0   # ★ 保留首题之前的前言（FM+卷首标题+组卷口径+模块标题）
for k in range(len(heads) - 1):
    s, qno = heads[k]
    e = heads[k + 1][0]
    block = lines[s:e]
    if qno in A:
        idx = [j for j, l in enumerate(block) if l.strip() == "---"]
        if idx:
            pos = idx[-1]
            block = block[:pos] + ["> **解析**（据源答案整理）：" + A[qno], ""] + block[pos:]
            done += 1
    out += block
txt2 = "\n".join(out)
open(MD, "w", encoding="utf-8", newline="\n").write(txt2)
print("已插入解析 %d 题；文件 %d 字" % (done, len(txt2)))
