# -*- coding: utf-8 -*-
"""阶段5 批次12：8 张重画图生成器。
产出到 .workbuddy/tmp/stage5_img/ ，经人眼核验后再按 sha256 入 媒体仓库。
依赖：系统 Python 3.12（RDKit 2026.03 + matplotlib + numpy + PIL）
"""
import os, io, json

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, ".workbuddy", "tmp", "stage5_img")
os.makedirs(OUT, exist_ok=True)

from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import rdMolDraw2D
from PIL import Image

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import FancyArrowPatch

CJK = "C:/Windows/Fonts/msyh.ttc"
fp = FontProperties(fname=CJK)
plt.rcParams["axes.unicode_minus"] = False

DPI = 200
DARK = "#1a1a1a"
ACC = "#c0392b"

log = []


def save(fig, name):
    p = os.path.join(OUT, name)
    fig.savefig(p, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    log.append((name, os.path.getsize(p)))
    print("  ok", name, os.path.getsize(p))


# ---------------- RDKit 渲染 ----------------
def render(smi, w=560, h=440, stereo=False, rot=0.0, hi=None, lw=2.0):
    m = Chem.MolFromSmiles(smi)
    assert m is not None, smi
    AllChem.Compute2DCoords(m)
    if rot:
        AllChem.RotateDepictionMolecule(m, rot * 3.14159265 / 180.0)
    d = rdMolDraw2D.MolDraw2DCairo(w, h)
    o = d.drawOptions()
    o.bondLineWidth = lw
    o.addStereoAnnotation = stereo
    o.padding = 0.16
    if hi:
        rdMolDraw2D.PrepareAndDrawMolecule(d, m, highlightAtoms=hi)
    else:
        rdMolDraw2D.PrepareAndDrawMolecule(d, m)
    d.FinishDrawing()
    return d.GetDrawingText(), m, d


def img_arr(png_bytes):
    import numpy as np
    im = Image.open(io.BytesIO(png_bytes)).convert("RGB")
    return np.asarray(im), im.size


def put(ax, png_bytes, x0, x1, y0, y1):
    """把 RDKit PNG 放到 axes 的 (x0..x1, y0..y1)。
    extent=(left,right,bottom,top)，配合默认 origin='upper' 才不会上下镜像。"""
    a, (w, h) = img_arr(png_bytes)
    ax.imshow(a, extent=[x0, x1, y0, y1], aspect="auto", zorder=1)
    return (x0, x1, y0, y1), (w, h)


def to_fig(px, py, box, size):
    """RDKit 像素坐标(左上原点,y向下) → axes 坐标"""
    x0, x1, y0, y1 = box
    w, h = size
    return x0 + px / w * (x1 - x0), y1 - py / h * (y1 - y0)


# ============ R1 环己烷键线式 ============
def r1():
    png, m, d = render("C1CCCCC1", 420, 380, lw=2.4)
    fig, ax = plt.subplots(figsize=(2.3, 2.1))
    put(ax, png, 0, 1, 0, 1)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    save(fig, "R1_cyclohexane_skeletal.png")


# ============ R2 环己烯 + NBS → 3-溴环己烯 ============
def r2():
    p1, _, _ = render("C1CCCC=C1", 460, 380, lw=2.2)
    p2, _, _ = render("BrC1CCCC=C1", 460, 380, lw=2.2)
    fig, ax = plt.subplots(figsize=(7.0, 3.0))
    put(ax, p1, 0.00, 0.34, 0.30, 0.95)
    put(ax, p2, 0.66, 1.00, 0.30, 0.95)
    ax.add_patch(FancyArrowPatch((0.37, 0.62), (0.62, 0.62),
                                 arrowstyle="-|>", mutation_scale=18,
                                 lw=1.8, color=DARK))
    ax.text(0.495, 0.79, "NBS / AIBN / CCl$_4$", ha="center", va="bottom",
            fontsize=11, fontproperties=fp, color=DARK)
    ax.text(0.495, 0.74, "Δ, hν", ha="center", va="top",
            fontsize=10, fontproperties=fp, color=DARK)
    ax.text(0.495, 0.44, "+ 琥珀酰亚胺", ha="center", va="top",
            fontsize=9, fontproperties=fp, color="#555")
    ax.text(0.17, 0.13, "环己烯", ha="center", va="center",
            fontsize=12, fontproperties=fp, color=DARK)
    ax.text(0.83, 0.13, "3-溴环己烯", ha="center", va="center",
            fontsize=12, fontproperties=fp, color=DARK)
    ax.text(0.83, 0.03, "（烯丙位溴代，双键保留）", ha="center", va="center",
            fontsize=9, fontproperties=fp, color="#555")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    save(fig, "R2_cyclohexene_nbs_allylic.png")


# ============ R4/R5 d 轨道排布（低自旋） ============
def dorb(name, nelec):
    """nelec = t2g 上的电子数（低自旋）；d6→6, d5→5"""
    fig, ax = plt.subplots(figsize=(3.4, 2.8))
    y_t2g, y_eg = 0.28, 0.74
    xs = {"eg": [0.16, 0.44], "t2g": [0.06, 0.34, 0.62]}
    for x in xs["eg"]:
        ax.plot([x, x + 0.18], [y_eg, y_eg], color=DARK, lw=2.2)
    for x in xs["t2g"]:
        ax.plot([x, x + 0.18], [y_t2g, y_t2g], color=DARK, lw=2.2)
    occ = []
    k = nelec
    for _ in range(3):
        occ.append(min(2, k)); k -= min(2, k)
    for i, x in enumerate(xs["t2g"]):
        n = occ[i]
        if n >= 1:
            ax.annotate("", xy=(x + 0.055, y_t2g + 0.105), xytext=(x + 0.055, y_t2g - 0.105),
                        arrowprops=dict(arrowstyle="-|>", lw=1.5, color=ACC, mutation_scale=9))
        if n >= 2:
            ax.annotate("", xy=(x + 0.135, y_t2g - 0.105), xytext=(x + 0.135, y_t2g + 0.105),
                        arrowprops=dict(arrowstyle="-|>", lw=1.5, color=ACC, mutation_scale=9))
    ax.text(0.86, y_eg, "eg", fontsize=10.5, va="center", ha="left", color=DARK)
    ax.text(0.86, y_eg - 0.135, "(d$_{x^2-y^2}$, d$_{z^2}$)", fontsize=8.5,
            va="center", ha="left", color=DARK)
    ax.text(0.86, y_t2g, "t$_{2g}$", fontsize=10.5, va="center", ha="left", color=DARK)
    ax.text(0.86, y_t2g - 0.135, "(d$_{xy}$, d$_{xz}$, d$_{yz}$)", fontsize=8.5,
            va="center", ha="left", color=DARK)
    ax.set_xlim(0, 1.62); ax.set_ylim(0.04, 0.96); ax.axis("off")
    save(fig, name)


def r4():
    dorb("R4_Ru2+_d6_t2g6_eg0.png", 6)


def r5():
    dorb("R5_Ru3+_d5_t2g5_eg0.png", 5)


# ============ R6 (R)-2-溴丁烷 → (S)-2-丁醇 ============
def pick(smis, want):
    for s in smis:
        m = Chem.MolFromSmiles(s)
        Chem.AssignStereochemistry(m, cleanIt=True, force=True)
        cc = Chem.FindMolChiralCenters(m, includeUnassigned=True,
                                       useLegacyImplementation=False)
        if cc and cc[0][1] == want:
            return s, m, cc
    raise SystemExit("no match %s %s" % (smis, want))


def r6():
    sR, mR, cR = pick(["CC[C@@H](C)Br", "CC[C@H](C)Br"], "R")
    sS, mS, cS = pick(["CC[C@H](C)O", "CC[C@@H](C)O"], "S")
    print("    R 源:", sR, cR, " S 源:", sS, cS)
    p1, _, _ = render(sR, 460, 400, stereo=True, lw=2.2)
    p2, _, _ = render(sS, 460, 400, stereo=True, lw=2.2)
    fig, ax = plt.subplots(figsize=(7.0, 3.1))
    put(ax, p1, 0.00, 0.34, 0.32, 0.98)
    put(ax, p2, 0.66, 1.00, 0.32, 0.98)
    ax.add_patch(FancyArrowPatch((0.37, 0.64), (0.62, 0.64),
                                 arrowstyle="-|>", mutation_scale=18, lw=1.8, color=DARK))
    ax.text(0.495, 0.77, "OH$^-$ 从 C—Br 背面进攻", ha="center", va="bottom",
            fontsize=9, fontproperties=fp, color=DARK)
    ax.text(0.17, 0.13, "(R)-2-溴丁烷", ha="center", va="center",
            fontsize=12, fontproperties=fp, color=DARK)
    ax.text(0.83, 0.13, "(S)-2-丁醇", ha="center", va="center",
            fontsize=12, fontproperties=fp, color=DARK)
    ax.text(0.5, 0.03, "构型翻转（Walden 转化）", ha="center", va="center",
            fontsize=9, fontproperties=fp, color="#555")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    save(fig, "R6_R_to_S_walden_inversion.png")


# ============ R7 Pinacol 不对称底物 ============
def r7():
    png, m, d = render("CC(O)(c1ccccc1)C(C)(C)O", 620, 470, lw=2.0)
    fig, ax = plt.subplots(figsize=(3.2, 2.4))
    put(ax, png, 0, 1, 0, 1)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    save(fig, "R7_pinacol_asym_substrate.png")


# ============ R8 两步势能剖面 ============
def r8():
    import numpy as np
    x = np.linspace(0, 10, 1200)

    def gauss(c, amp, w):
        return amp * np.exp(-((x - c) ** 2) / (2 * w ** 2))

    # 反应物 → ‡1 → 中间体(谷) → ‡2 → 产物；两个峰、中间一个真极小值
    y = 0.30 + 0.18 * (x / 10) + gauss(2.6, 2.20, 0.75) + gauss(6.9, 1.00, 0.75)
    fig, ax = plt.subplots(figsize=(5.4, 3.2))
    ax.plot(x, y, color=DARK, lw=2.0)

    def at(xx):
        return float(np.interp(xx, x, y))

    X_R, X_T1, X_I, X_T2, X_P = 0.20, 2.60, 4.75, 6.90, 9.80
    for xx in (X_R, X_T1, X_I, X_T2, X_P):
        ax.plot([xx], [at(xx)], "o", ms=4, color=ACC, zorder=3)
    ax.annotate("‡₁", (X_T1, at(X_T1)), textcoords="offset points", xytext=(0, 8),
                ha="center", fontsize=12, color=ACC)
    ax.annotate("‡₂", (X_T2, at(X_T2)), textcoords="offset points", xytext=(0, 8),
                ha="center", fontsize=12, color=ACC)
    ax.annotate("反应物", (X_R, at(X_R)), textcoords="offset points",
                xytext=(6, -14), fontsize=10, fontproperties=fp, color=DARK)
    ax.text(X_I, 0.20, "中间体", ha="center", va="center", fontsize=10,
            fontproperties=fp, color=DARK)
    ax.annotate("产物", (X_P, at(X_P)), textcoords="offset points",
                xytext=(0, 10), ha="center", fontsize=10, fontproperties=fp, color=DARK)
    ax.annotate("", xy=(10.55, 0.0), xytext=(-0.25, 0.0),
                arrowprops=dict(arrowstyle="-|>", lw=1.4, color=DARK, shrinkA=0, shrinkB=0))
    ax.annotate("", xy=(-0.25, 4.05), xytext=(-0.25, 0.0),
                arrowprops=dict(arrowstyle="-|>", lw=1.4, color=DARK, shrinkA=0, shrinkB=0))
    ax.text(5.3, -0.40, "反应坐标", fontsize=10, fontproperties=fp,
            ha="center", va="center", color=DARK)
    ax.text(-0.62, 2.0, "能量", fontsize=10, fontproperties=fp,
            rotation=90, ha="center", va="center", color=DARK)
    ax.set_xlim(-1.1, 11.1); ax.set_ylim(-0.80, 4.35); ax.axis("off")
    save(fig, "R8_two_step_potential_profile.png")


# ============ R9 1,2-甲基迁移机理（手绘示意 + 弯箭头） ============
def r9():
    fig, ax = plt.subplots(figsize=(7.6, 3.0))
    # ---- 左：新戊基正离子 ----
    cL, yC = 0.26, 0.52
    ax.plot([cL, cL], [yC, yC + 0.31], color=DARK, lw=1.8)
    ax.plot([cL, cL], [yC, yC - 0.31], color=DARK, lw=1.8)
    ax.plot([cL, cL + 0.19], [yC, yC], color=DARK, lw=1.8)
    ax.plot([cL, cL - 0.10], [yC, yC], color=DARK, lw=1.8)
    ax.text(cL, yC + 0.36, "CH$_3$", ha="center", va="center", fontsize=11,
            fontproperties=fp, color=DARK)
    ax.text(cL, yC - 0.36, "CH$_3$", ha="center", va="center", fontsize=11,
            fontproperties=fp, color=DARK)
    ax.text(cL + 0.21, yC, "CH$_3$", ha="left", va="center", fontsize=11,
            fontproperties=fp, color=DARK)
    ax.text(cL - 0.13, yC, "CH$_2^+$", ha="right", va="center", fontsize=11.5,
            fontproperties=fp, color=DARK)
    # 弯箭头：上方 CH₃ → ⁺CH₂
    ax.add_patch(FancyArrowPatch((cL - 0.04, yC + 0.30), (cL - 0.13, yC + 0.07),
                                 connectionstyle="arc3,rad=0.62",
                                 arrowstyle="-|>", mutation_scale=13,
                                 lw=1.8, color=ACC, zorder=5))
    ax.text(cL - 0.30, yC + 0.44, "1,2-CH$_3$ 迁移", ha="left", va="center",
            fontsize=9.5, fontproperties=fp, color=ACC)
    # ---- 中：箭头 ----
    ax.add_patch(FancyArrowPatch((0.60, yC), (0.70, yC),
                                 arrowstyle="-|>", mutation_scale=18, lw=1.8, color=DARK))
    # ---- 右：叔戊基正离子 ----
    cR = 0.88
    ax.plot([cR, cR], [yC, yC + 0.31], color=DARK, lw=1.8)
    ax.plot([cR, cR], [yC, yC - 0.31], color=DARK, lw=1.8)
    ax.plot([cR, cR + 0.14], [yC, yC], color=DARK, lw=1.8)
    ax.text(cR - 0.03, yC + 0.36, "CH$_3$", ha="center", va="center", fontsize=11.5,
            fontproperties=fp, color=DARK)
    ax.text(cR - 0.03, yC - 0.36, "CH$_3$", ha="center", va="center", fontsize=11.5,
            fontproperties=fp, color=DARK)
    ax.text(cR + 0.01, yC, "C$^+$", ha="center", va="center", fontsize=11.5,
            fontproperties=fp, color=DARK,
            bbox=dict(fc="white", ec="none", pad=1.0))
    ax.text(cR + 0.17, yC, "CH$_2$CH$_3$", ha="left", va="center", fontsize=11,
            fontproperties=fp, color=DARK)
    # ---- 注记 ----
    ax.text(cL - 0.10, 0.03, "新戊基正离子（1°）", ha="center", va="center",
            fontsize=11, fontproperties=fp, color=DARK)
    ax.text(cR + 0.10, 0.03, "叔戊基正离子（3°，更稳）", ha="center", va="center",
            fontsize=11, fontproperties=fp, color=DARK)
    ax.text(0.60, -0.09, "C—CH$_3$ 的 σ 电子对整体迁移到相邻缺电子碳",
            ha="center", va="center", fontsize=9, fontproperties=fp, color="#555")
    ax.set_xlim(-0.20, 1.32); ax.set_ylim(-0.17, 1.04); ax.axis("off")
    save(fig, "R9_neopentyl_12_Me_shift.png")


if __name__ == "__main__":
    for f in (r1, r2, r4, r5, r6, r7, r8, r9):
        print(">>>", f.__name__)
        f()
    print("\n输出:", OUT)
    io.open(os.path.join(OUT, "_sizes.txt"), "w", encoding="utf-8").write(
        "\n".join("%s\t%d" % t for t in log))
