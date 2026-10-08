#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""add_analysis.py —— 给卷 XI 的 16 张卡在答案区尾部追加一行「解析（据源答案整理）」。
仅动答案区尾部；FM 与题面区不变；幂等（已有「> **解析**」则跳过）。
"""
import json, os, shutil, sys
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
BK = os.path.join(R, ".workbuddy/tmp/opt_pipe/analysis_backup")
os.makedirs(BK, exist_ok=True)

A = {
 "题-QBY-06-07": "考查配位化学与 18 电子规则。7-1 需由四方锥配位与中性 BDI 配体推出 Re 的价态并核算价电子数；7-2 借 Re 的质量分数 20.46% 及“仅 BDI、Cp 参与配位”反推离子型产物组成；7-3 由三重旋转轴与 Re 的质量分数 24.98% 定出 D＝Gd(THF)[CpRe(BDI)]₃。",
 "题-CM-174-01": "考查中国古代化学史与砷的化学。解答以源册答案表形式随卡（含各小问答案与方程式），详见随卷解图。",
 "题-GM-01-01": "考查小杂环化合物的结构、键合与自由基机理。要点：P 为 PhCS₃Cl；反应 1 为 2PhCS₃Cl → Ph₂C₂S₃Cl₂ + 3S；1.4 经自由基 PhCS₃· 偶联成 (PhCS₃)₂ 后再脱硫，得 R＝(PhCS₂)₂。",
 "题-YJ-01-01": "考查碘量法原理与实验异常探究。要点：滴定基于 Cr₂O₇²⁻~3I₂~6S₂O₃²⁻ 的计量关系；淡黄色沉淀源于 S₂O₃²⁻ 在酸性条件下分解（S₂O₃²⁻ + 2H⁺ → S↓ + SO₂ + H₂O）；末问由硫原子守恒与溶度积估算 S₈ 浓度及沉淀分散度（≈3.6×10⁵）。",
 "题-HZ-12-06": "考查 Bohr 氢原子模型的完整推导。要点：以折合质量 μ＝m_e·m_n/(m_e+m_n) 替代电子质量，联立“库仑力＝向心力”与角动量量子化 μvr＝nħ，导出轨道半径 r_n 与 Rydberg 常数表达式（题面已给出关键中间步骤提示）。",
 "题-XeC-13-01": "考查元素推断与核反应。要点：M 即“失踪元素”Tc（1937 年人工合成）；A~E 依次为 Tc₂O₇、Tc₂S₇、TcO₃F、TcO₂F₃、TcOF₅；⁹⁹Mo 经 β⁻ 衰变得 ⁹⁹ᵐTc，其退激属 γ 衰变。",
 "题-GChO-17-04": "考查古氏试砷法与砷的定量分析（含原子吸收-紫外分光光度法）。解答为源卷手写解析手稿裁图（含反应式与计算过程），详见随卷解图。",
 "题-HYS-40-01": "考查原子簇的电子计数（Zintl/Wade 规则）与簇结构重构。要点：由簇骨架电子数定出 6 与 12、n＝3 及 D₄d 对称性；1.3.2 须保留 [Sn₂Bi₆]²⁻ 除 Bi–Bi 外的全部键连，并新建 Bi–Bi 与 Sn–Sn 键。",
 "题-QBY-04-03": "考查晶胞原子计数与分数坐标定址。要点：由晶胞内 Cu 20、Zn 32 得最简式 Cu₅Zn₈，ρ≈8.02 g·cm⁻³；3-2 以各原子到最近簇心的相对距离，判定其所属的嵌套多面体层（Zn₄ 四面体 → Cu₄ 四面体 → Cu₆ 八面体 → Zn₁₂ 多面体）与元素。",
 "题-CM-12-07": "考查高压碳酸晶体的结构解析。要点：由两向投影图判 X 为简单单斜、Y 为底心正交，碳原子分别为 sp²/sp³；X 中 C–O 键接近等长源于分子内共轭与分子间氢键；7-2 借 ¹H/¹³C 仅一种环境及化学位移推阳离子的立体结构。",
 "题-GM-09-03": "考查铜的元素化学。要点：由晶胞参数与原子计数得金属互化物 CuNi₃、ρ≈9.04 g·cm⁻³，属正交晶系底心点阵；Cu₂O 显色归因于晶体缺陷；CuI 与 Hg 反应生成 Cu₂HgI₄ 并析出 Cu。",
 "题-YJ-01-05": "考查含 Se 晶体的结构计算。要点：PdSe₂ 中 Pd 为 +2、Se 配位数为 4；由组成反推 X 并经摩尔比推出 Y＝Se₄N₄；LaCsSe₂ 属 R 心六方点阵，由几何关系得 a＝445.0 pm、c＝2501 pm，ρ≈4.99 g·cm⁻³。",
 "题-HYS-13-05": "考查过渡金属的提取与纯化（RKEF 法与 Mond 法）。解答为源卷答案册按题裁图（含结构图与公式），详见随卷解图。",
 "题-QBY-01-05": "考查理想液体混合物的蒸气压与热力学循环。要点：先用 Trouton 规则（Δ_vapS ≈ 10.5R）估算 HN₃ 的蒸发焓，再按 Raoult 定律求各组分分压与总压；5-2-1 分析实测与理论偏差的原因（非理想性、缔合/氢键等）；5-2-2 以 Hess 定律组合给定数据求 Δ_fH°。",
 "题-CM-14-09": "考查含氟高活性物种的结构与动力学。要点：由关键中间体 A 的三个共振极限式解释其高活泼性（F 与碳负离子间的孤对排斥／α 效应，以及 F 的诱导吸电子使碳正离子去稳定）；9-2 由两组动力学实验数据定出反应级数。",
 "题-GM-09-02": "考查硫代砷酸盐的组成反推与链状结构。要点：由 Ag 的质量分数 22.23% 与 [pipH]⁺ 得 A＝[pipH]₂[AgAsS₄]；2-1-3 指出改用可溶银盐会因 Ag₂Sₓ 浓度过高而阻碍 [AgAsS₄]ₙ 链的组装；2-2 须据 Ga 四配位、Asᴵᴵᴵ 位于链中、Asⱽ 位于链外且仅含八元环画出结构。",
}

d = json.load(open(os.path.join(R, ".workbuddy/tmp/opt_pipe/vol_plan_XI.json"), encoding="utf-8"))
flat = [c for _, l in d for c in l]
n = 0
for c in flat:
    p = c["path"]
    key = None
    for k in A:
        if os.path.basename(p).startswith(k):
            key = k; break
    if not key:
        print("  未匹配解析:", os.path.basename(p)[:50]); continue
    t = open(p, encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")
    if "**解析**" in t:
        print("  已有解析，跳过:", os.path.basename(p)[:40]); continue
    j = t.find("## 参考答案"); kk = t.find("## 知识点映射")
    if j < 0 or kk < 0:
        print("  节缺失:", os.path.basename(p)[:40]); continue
    bkf = os.path.join(BK, os.path.basename(p) + ".orig")
    if not os.path.exists(bkf):
        open(bkf, "w", encoding="utf-8", newline="\n").write(t)
    line = "\n> **解析**（据源答案整理）：%s\n\n" % A[key]
    open(p, "w", encoding="utf-8", newline="\n").write(t[:kk].rstrip() + "\n" + line + t[kk:])
    n += 1
print("已注入解析 %d 卡" % n)
