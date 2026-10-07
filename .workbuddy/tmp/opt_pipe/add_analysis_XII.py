#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""add_analysis_XII.py —— 给卷 XII 答案版逐题在答案区尾部追加一行「解析（据源答案整理）」。
幂等（已有「> **解析**」则跳过）；仅动答案版 md，不动 FM/题面。
"""
import os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
MD = os.path.join(R, "04-题库", "初赛模拟卷XII（非有机·答案版）.md")

A = {
 1: "考查由螺旋链构型定晶系与分数坐标。要点：由 MF₄ 四边形共顶点连接的一维螺旋链，按 4 重/6 重螺旋的对称性判定 n=3、属六方晶系；再由螺旋轴操作生成 M 与 F 的全部分数坐标（旋转方向有误会致 z 坐标整体错位）；末问由两组 F–F 距离反解 a、c。",
 2: "考查 4₁ 螺旋轴操作与分数坐标生成。要点：由部分 A 原子坐标按 4₁ 螺旋（绕 c 转 90° 并平移 c/4）推出其余 A、B 原子坐标；再由 a＝b＝3.922 Å、c＝14.154 Å 与密度 8.976 g·cm⁻³ 反推化学式（A 为 U、B 为 Si）；并指出晶体中 4₁ 与 4₃ 螺旋轴所在位置。",
 3: "考查 AlB₂ 型结构与成键解释。要点：B 形成石墨烯状六元环、Ti 位于环间，共价/离子/金属键构成的三维强键网络解释其高硬度与高熔点；书写三条制备 TiB₂ 的反应方程式；由 a＝3.03 Å、c＝3.23 Å、Z＝1 计算理论密度与 B–B 最短距离；思考题按热膨胀系数计算 a、c 轴的相对伸长率。",
 4: "考查立方晶系与量热计算。要点：由分解所得液态水与甲烷气体的体积-密度数据求得一个立方正晶胞中水分子数为 46，从而给出晶胞组成（8 CH₄·46 H₂O）与立方晶胞参数；由两组燃烧焓之差求水的标准摩尔蒸发焓；再由恒容反应热换算标准反应焓。",
 5: "考查萤石型掺杂结构与混合热力学。要点：额外氧占据八面体空隙，由电价平衡求填隙率（用 x 表示）；由各组分的 ΔfH°、S°、ΔfG° 并按理想混合物模型计算 U₀.₈₅Am₀.₁₅O₂ 的标准摩尔生成吉布斯自由能；由氧势与平衡常数求 x 随氧分压的变化；解释晶胞参数偏大约 10 pm 的缺陷成因；写出灼烧再氧化为 AmO₂ 的方程式。",
 6: "考查弱酸分级电离与硫化物沉淀。要点：由 K₁≫K₂ 只计一级电离，用质子条件 [H⁺]＝[OH⁻]＋[HS⁻] 解出 pH；再由「完全沉淀」判据 [M²⁺]≤1.0×10⁻⁶ mol/L 与通 H₂S 至饱和（[H₂S]＝0.10 mol/L），求 MS 的 pKsp 下限。",
 7: "考查 Clausius–Clapeyron 方程与光谱解离能。要点：由两组温度下液态钠上方钠蒸气的平衡分压，用 ln(p₂/p₁)＝−(ΔH_vap/R)(1/T₂−1/T₁) 求蒸发热 ΔH_vap；再由 E＝hc₀N_A D 求解离能并计入 2.5RT 得 ΔH。",
 8: "考查 Langmuir 等温式与吸附热力学。要点：用两次进气-平衡压强数据联立 Langmuir 方程求出 298 K 下的饱和吸附量 q_m 与吸附常数 b₂₉₈；再由不同温度下的吸附量经 van't Hoff 式求吸附焓（或吸附热），并据此讨论吸附强弱。",
 9: "考查微晶溶解的界面热力学（Ostwald–Freundlich 公式）。要点：由两种晶粒半径的溶解度联立 RT·ln(S_r/S_∞)＝γM/(ρr) 求固-液界面张力 γ 与大块溶解度 S_∞；再由 Ostwald 熟化判断共存时的终态（大晶粒长大、小晶粒溶解）及终态溶解度；末问由过饱和浓度求均相成核临界半径与 Gibbs 自由能变（体积项＋表面项）。",
 10: "考查气相反应的热力学量与平衡计算。要点：先由标准生成焓、熵数据求氨氧化反应的 Δ_rH°、Δ_rS°、Δ_rG°，判断标准态自发性与最低反应温度；再由平衡常数求各组分平衡分压与转化率；末问在认为 HNO₃ 完全电离的前提下做物料与电荷守恒计算。",
}

txt = open(MD, encoding="utf-8-sig").read().replace("\r\n", "\n")
if "> **解析**（据源答案整理）" in txt:
    print("已存在解析，跳过"); sys.exit(0)
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
