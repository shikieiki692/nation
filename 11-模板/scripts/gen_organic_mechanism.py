#!/usr/bin/env python3
"""Generate 3 organic mechanism diagrams — v2 with fixed subscripts."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import matplotlib.font_manager as fm
import os, sys

sys.stdout.reconfigure(encoding='utf-8')
OUTPUT_DIR = r"C:\Obsidion\妙妙屋\media"

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def arrow(ax, s, e, color='black', lw=1.5, rad=0):
    ax.add_patch(FancyArrowPatch(s, e, arrowstyle='->', color=color, lw=lw,
        connectionstyle=f"arc3,rad={rad}", mutation_scale=15, zorder=5))

def txt(ax, x, y, t, fs=12, ha='center', va='center', fw='normal', c='black'):
    ax.text(x, y, t, fontsize=fs, ha=ha, va=va, fontweight=fw, color=c, zorder=10)

def mathtxt(ax, x, y, t, fs=12, c='black'):
    ax.text(x, y, t, fontsize=fs, ha='center', va='center', color=c, zorder=10,
            math_fontfamily='DejaVu Sans')

# ============================================================
# Image 1: Grignard Reaction Mechanism (v2)
# ============================================================
def gen_grignard():
    fig, ax = plt.subplots(1, 1, figsize=(10, 4))
    ax.set_xlim(0, 10); ax.set_ylim(0, 4); ax.axis('off'); ax.set_aspect('equal')

    txt(ax, 5, 3.7, 'Grignard反应机理：溴苯→苯甲酸', fs=14, fw='bold')

    # PhBr
    txt(ax, 1.5, 2.5, 'PhBr', fs=14, fw='bold', c='#1a5276')
    txt(ax, 1.5, 2.0, '+ Mg', fs=11, c='#666666')
    txt(ax, 1.5, 1.5, '(乙醚, N$_2$)', fs=9, c='#888888')

    arrow(ax, (2.5, 2.5), (3.5, 2.5), color='#c0392b', lw=2)
    txt(ax, 3.0, 2.9, '(1)', fs=9, c='#c0392b')

    # PhMgBr
    txt(ax, 4.5, 2.5, 'PhMgBr', fs=14, fw='bold', c='#1a5276')
    txt(ax, 4.5, 2.0, '(格氏试剂)', fs=9, c='#888888')
    txt(ax, 4.5, 1.5, '强亲核试剂', fs=9, c='#c0392b')

    arrow(ax, (5.5, 2.5), (6.5, 2.5), color='#c0392b', lw=2)
    txt(ax, 6.0, 2.9, '(2)', fs=9, c='#c0392b')
    txt(ax, 6.0, 2.0, '+ CO$_2$', fs=10, c='#666666')

    # PhCOOMgBr
    txt(ax, 7.5, 2.5, 'PhCOOMgBr', fs=13, fw='bold', c='#1a5276')

    arrow(ax, (8.3, 2.5), (9.1, 2.5), color='#c0392b', lw=2)
    txt(ax, 8.7, 2.9, '(3)', fs=9, c='#c0392b')
    txt(ax, 8.7, 2.0, 'H$_3$O$^+$', fs=10, c='#666666')

    # PhCOOH
    txt(ax, 9.5, 2.5, 'PhCOOH', fs=14, fw='bold', c='#27ae60')

    txt(ax, 4.5, 0.8, 'Et$_2$O 配位稳定 Mg → 无水无氧条件', fs=9, c='#888888')
    txt(ax, 6.0, 1.1, 'C$^-$进攻CO$_2$的C=O', fs=9, c='#c0392b', fw='bold')

    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'grignard-mechanism-phbr-to-phcooh.png'), dpi=180, bbox_inches='tight')
    plt.close(fig)
    print("[OK] grignard-mechanism-phbr-to-phcooh.png")

# ============================================================
# Image 2: Cannizzaro Reaction Mechanism (v2)
# ============================================================
def gen_cannizzaro():
    fig, ax = plt.subplots(1, 1, figsize=(10, 5))
    ax.set_xlim(0, 10); ax.set_ylim(0, 5); ax.axis('off'); ax.set_aspect('equal')

    txt(ax, 5, 4.7, 'Cannizzaro反应机理：苯甲醛歧化', fs=14, fw='bold')

    # PhCHO + OH-
    txt(ax, 1.2, 3.5, 'PhCHO', fs=13, fw='bold', c='#1a5276')
    txt(ax, 1.2, 3.0, '+ OH$^-$', fs=11, c='#666666')
    txt(ax, 1.2, 2.5, '①亲核加成', fs=9, c='#888888')

    arrow(ax, (2.2, 3.5), (3.2, 3.5), color='#c0392b', lw=2)

    # Intermediate
    txt(ax, 4.2, 3.8, 'Ph—CH(O$^-$)$_2$', fs=12, fw='bold', c='#8e44ad')
    txt(ax, 4.2, 3.3, '(四面体双负离子)', fs=9, c='#888888')
    txt(ax, 4.2, 2.8, '关键中间体', fs=9, c='#c0392b', fw='bold')

    arrow(ax, (5.3, 3.5), (6.3, 3.5), color='#c0392b', lw=2)
    txt(ax, 5.8, 3.9, '②H$^-$转移', fs=9, c='#c0392b', fw='bold')

    # Products
    txt(ax, 7.5, 3.8, 'PhCOO$^-$', fs=12, fw='bold', c='#27ae60')
    txt(ax, 7.5, 3.3, '(氧化产物)', fs=9, c='#27ae60')

    txt(ax, 7.5, 2.2, 'PhCH$_2$OH', fs=12, fw='bold', c='#2980b9')
    txt(ax, 7.5, 1.7, '(还原产物)', fs=9, c='#2980b9')

    arrow(ax, (5.3, 3.7), (6.5, 3.7), color='#27ae60', lw=1.5)
    arrow(ax, (5.3, 3.3), (6.5, 2.3), color='#2980b9', lw=1.5)

    txt(ax, 4.2, 1.8, '浓NaOH(50%)', fs=10, c='#c0392b', fw='bold')
    txt(ax, 4.2, 1.3, '无α-H的醛才能发生', fs=9, c='#888888')
    txt(ax, 4.2, 0.8, '有α-H → Aldol缩合（竞争反应）', fs=9, c='#e74c3c')

    txt(ax, 5, 0.3, '总反应: 2 PhCHO + NaOH → PhCOONa + PhCH$_2$OH',
        fs=10, fw='bold', c='#1a5276')

    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'cannizzaro-mechanism-benzaldehyde.png'), dpi=180, bbox_inches='tight')
    plt.close(fig)
    print("[OK] cannizzaro-mechanism-benzaldehyde.png")

# ============================================================
# Image 3: Acetal/Ketal Protection Mechanism (v2)
# ============================================================
def gen_acetal():
    fig, ax = plt.subplots(1, 1, figsize=(10, 5.5))
    ax.set_xlim(0, 10); ax.set_ylim(0, 5.5); ax.axis('off'); ax.set_aspect('equal')

    txt(ax, 5, 5.2, '缩酮保护机理：环己酮 + 乙二醇', fs=14, fw='bold')

    # Step 1
    txt(ax, 1.0, 4.0, '环己酮', fs=12, fw='bold', c='#1a5276')
    txt(ax, 1.0, 3.5, '(C=O)', fs=10, c='#666666')
    txt(ax, 1.0, 3.0, '①H$^+$活化', fs=9, c='#c0392b')

    arrow(ax, (1.8, 3.8), (2.6, 3.8), color='#c0392b', lw=2)
    txt(ax, 2.2, 4.2, 'TsOH', fs=9, c='#888888')

    # Step 2
    txt(ax, 3.4, 4.0, '环己酮', fs=11, fw='bold', c='#1a5276')
    txt(ax, 3.4, 3.5, 'C=OH$^+$', fs=10, c='#c0392b')
    txt(ax, 3.4, 3.0, '②醇加成', fs=9, c='#888888')

    arrow(ax, (4.2, 3.8), (5.0, 3.8), color='#c0392b', lw=2)
    txt(ax, 4.6, 4.2, '+ HOCH$_2$CH$_2$OH', fs=9, c='#666666')

    # Intermediate
    txt(ax, 5.8, 4.0, '半缩酮', fs=11, fw='bold', c='#8e44ad')
    txt(ax, 5.8, 3.5, '(C(OH)(OCH$_2$CH$_2$OH))', fs=8, c='#888888')
    txt(ax, 5.8, 3.0, '③脱水', fs=9, c='#888888')

    arrow(ax, (6.6, 3.8), (7.4, 3.8), color='#c0392b', lw=2)
    txt(ax, 7.0, 4.2, '-H$_2$O', fs=9, c='#e74c3c')

    # Product
    txt(ax, 8.2, 4.0, '环状缩酮', fs=12, fw='bold', c='#27ae60')
    txt(ax, 8.2, 3.5, '1,3-二氧杂环戊烷', fs=8, c='#27ae60')
    txt(ax, 8.2, 3.0, '④保护完成', fs=9, c='#27ae60')

    # Reversibility
    txt(ax, 5, 2.5, '可逆反应  ⇌  除水驱动', fs=10, fw='bold', c='#c0392b')

    txt(ax, 5, 2.0, '保护基策略', fs=12, fw='bold', c='#1a5276')
    txt(ax, 5, 1.5, '缩酮对碱稳定 → 可在碱性条件下反应其他官能团', fs=9, c='#2980b9')
    txt(ax, 5, 1.0, '缩酮对酸不稳定 → 用稀酸即可脱保护恢复C=O', fs=9, c='#e74c3c')
    txt(ax, 5, 0.5, 'Dean-Stark分水器除水 → 推动平衡向右', fs=9, c='#888888')

    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'acetal-protection-cyclohexanone.png'), dpi=180, bbox_inches='tight')
    plt.close(fig)
    print("[OK] acetal-protection-cyclohexanone.png")

if __name__ == '__main__':
    gen_grignard()
    gen_cannizzaro()
    gen_acetal()
    print("\nAll 3 images generated (v2)!")
