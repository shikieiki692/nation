#!/usr/bin/env python3
"""Generate 4 B&W textbook-quality diagrams for coordination chemistry handout."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.font_manager import FontProperties
import numpy as np
import os

# Font setup
FONT_PATH = 'C:/Windows/Fonts/simhei.ttf'
fp_title = FontProperties(fname=FONT_PATH, size=16, weight='bold')
fp_label = FontProperties(fname=FONT_PATH, size=11)
fp_small = FontProperties(fname=FONT_PATH, size=9)
fp_tiny = FontProperties(fname=FONT_PATH, size=8)
fp_formula = FontProperties(fname=FONT_PATH, size=10)

OUT_DIR = r'C:\Obsidion\妙妙屋\media'
DPI = 200


def draw_horizontal_line(ax, x, y, length=0.3, lw=2, color='black'):
    """Draw a short horizontal line representing an energy level."""
    ax.plot([x - length/2, x + length/2], [y, y], color=color, linewidth=lw)


def draw_arrow(ax, x, y1, y2, text='', side='right', fontprop=None):
    """Draw a vertical arrow with optional label."""
    if fontprop is None:
        fontprop = fp_label
    ax.annotate('', xy=(x, y2), xytext=(x, y1),
                arrowprops=dict(arrowstyle='<->', color='black', lw=1.5))
    if text:
        offset = 0.05 if side == 'right' else -0.05
        ha = 'left' if side == 'right' else 'right'
        ax.text(x + offset, (y1 + y2) / 2, text, fontproperties=fontprop,
                ha=ha, va='center')


# ============================================================
# IMAGE 1: Octahedral Field Splitting
# ============================================================
def gen_octahedral_splitting():
    fig, ax = plt.subplots(1, 1, figsize=(7, 5))
    ax.set_xlim(-0.5, 4.5)
    ax.set_ylim(-1.5, 4.5)
    ax.axis('off')
    ax.set_aspect('equal')

    # Title
    ax.text(2, 4.2, '八面体场中 d 轨道分裂', fontproperties=fp_title,
            ha='center', va='top')

    # Y-axis
    ax.annotate('', xy=(0, 4), xytext=(0, -1),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.5))
    ax.text(-0.15, 1.5, '能量 E', fontproperties=fp_label,
            ha='right', va='center', rotation=90)

    # Column positions
    x_free = 1.0
    x_sphere = 2.2
    x_split = 3.5

    # Level: Free ion (5 degenerate d orbitals)
    for i in range(5):
        draw_horizontal_line(ax, x_free, 1.5, length=0.25, lw=1.8)
    ax.text(x_free, 1.1, '自由离子', fontproperties=fp_small, ha='center')

    # Dashed line from free to sphere
    ax.plot([x_free + 0.15, x_sphere - 0.15], [1.5, 1.5],
            color='gray', linewidth=1, linestyle='--')

    # Level: Spherical field
    for i in range(5):
        draw_horizontal_line(ax, x_sphere, 1.5, length=0.25, lw=1.5, color='gray')
    ax.text(x_sphere, 1.1, '球形场', fontproperties=fp_small, ha='center')

    # Dashed lines from sphere to split levels
    ax.plot([x_sphere + 0.15, x_split - 0.3], [1.5, 3.0],
            color='gray', linewidth=1, linestyle=':')
    ax.plot([x_sphere + 0.15, x_split - 0.3], [1.5, 0.2],
            color='gray', linewidth=1, linestyle=':')

    # Level: e_g (2 orbitals, higher)
    for i in range(2):
        draw_horizontal_line(ax, x_split, 3.0, length=0.25, lw=2)
    ax.text(x_split + 0.25, 3.0, '$e_g$', fontproperties=fp_label,
            ha='left', va='center', fontsize=12)
    ax.text(x_split + 0.25, 2.7, '+0.6$\\Delta_o$', fontproperties=fp_small,
            ha='left', va='center', color='gray')

    # Individual orbital labels for e_g
    ax.text(x_split - 0.2, 3.25, '$d_{x^2-y^2}$', fontproperties=fp_tiny,
            ha='center', va='bottom')
    ax.text(x_split + 0.2, 3.25, '$d_{z^2}$', fontproperties=fp_tiny,
            ha='center', va='bottom')

    # Level: t_2g (3 orbitals, lower)
    for i in range(3):
        draw_horizontal_line(ax, x_split, 0.2, length=0.25, lw=2)
    ax.text(x_split + 0.25, 0.2, '$t_{2g}$', fontproperties=fp_label,
            ha='left', va='center', fontsize=12)
    ax.text(x_split + 0.25, -0.1, '-0.4$\\Delta_o$', fontproperties=fp_small,
            ha='left', va='center', color='gray')

    # Individual orbital labels for t_2g
    ax.text(x_split - 0.3, -0.15, '$d_{xy}$', fontproperties=fp_tiny,
            ha='center', va='top')
    ax.text(x_split, -0.15, '$d_{xz}$', fontproperties=fp_tiny,
            ha='center', va='top')
    ax.text(x_split + 0.3, -0.15, '$d_{yz}$', fontproperties=fp_tiny,
            ha='center', va='top')

    # Delta arrow
    draw_arrow(ax, 4.2, 0.2, 3.0, text='$\\Delta_o$ = 10Dq', side='right')

    # Bottom annotation
    ax.text(2, -1.2, '重心守恒: 3*(-0.4$\\Delta_o$) + 2*(+0.6$\\Delta_o$) = 0',
            fontproperties=fp_small, ha='center', va='top',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='lightgray', alpha=0.5))

    fig.savefig(os.path.join(OUT_DIR, 'octahedral-field-splitting-bw.png'),
                dpi=DPI, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print("OK: octahedral-field-splitting-bw.png")


# ============================================================
# IMAGE 2: Three-Field Comparison
# ============================================================
def gen_three_field():
    fig, axes = plt.subplots(1, 3, figsize=(12, 5))
    fig.subplots_adjust(wspace=0.3)

    for i, (ax, title, config) in enumerate(zip(axes,
        ['Oh 八面体场', 'Td 四面体场', 'D₄h 正方形场'],
        ['oh', 'td', 'd4h'])):

        ax.set_xlim(-1, 4)
        ax.set_ylim(-2, 5)
        ax.axis('off')

        # Title
        ax.text(1.5, 4.5, title, fontproperties=fp_label, fontweight='bold',
                ha='center', va='top',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='lightgray'))

        # Y-axis
        ax.annotate('', xy=(-0.3, 4), xytext=(-0.3, -1.5),
                    arrowprops=dict(arrowstyle='->', color='black', lw=1.2))
        ax.text(-0.5, 1.5, 'E', fontproperties=fp_label,
                ha='right', va='center')

        x = 1.5  # center x for levels

        if config == 'oh':
            # e_g: 2 levels at top
            for j in range(2):
                draw_horizontal_line(ax, x - 0.15 + j * 0.3, 3.0, length=0.25, lw=2)
            ax.text(x + 0.6, 3.0, '$e_g$ (2)', fontproperties=fp_label, va='center')
            ax.text(x + 0.6, 2.7, '+0.6$\\Delta_o$', fontproperties=fp_tiny, va='center', color='gray')
            # t_2g: 3 levels at bottom
            for j in range(3):
                draw_horizontal_line(ax, x - 0.2 + j * 0.2, 0.0, length=0.2, lw=2)
            ax.text(x + 0.6, 0.0, '$t_{2g}$ (3)', fontproperties=fp_label, va='center')
            ax.text(x + 0.6, -0.3, '-0.4$\\Delta_o$', fontproperties=fp_tiny, va='center', color='gray')
            # Delta arrow
            draw_arrow(ax, 3.3, 0.0, 3.0, text='$\\Delta_o$', side='right', fontprop=fp_label)
            # Bottom info
            ax.text(1.5, -1.5, 'CN=6 | 正八面体\n$\\Delta_o$=10Dq',
                    fontproperties=fp_tiny, ha='center', va='top')

        elif config == 'td':
            # t_2: 3 levels at top (inverted!)
            for j in range(3):
                draw_horizontal_line(ax, x - 0.2 + j * 0.2, 3.0, length=0.2, lw=2)
            ax.text(x + 0.6, 3.0, '$t_2$ (3)', fontproperties=fp_label, va='center')
            ax.text(x + 0.6, 2.7, '+0.4$\\Delta_t$', fontproperties=fp_tiny, va='center', color='gray')
            # e: 2 levels at bottom
            for j in range(2):
                draw_horizontal_line(ax, x - 0.15 + j * 0.3, 0.0, length=0.25, lw=2)
            ax.text(x + 0.6, 0.0, 'e (2)', fontproperties=fp_label, va='center')
            ax.text(x + 0.6, -0.3, '-0.6$\\Delta_t$', fontproperties=fp_tiny, va='center', color='gray')
            # Delta arrow
            draw_arrow(ax, 3.3, 0.0, 3.0, text='$\\Delta_t$', side='right', fontprop=fp_label)
            # Note about inversion
            ax.text(1.5, -0.9, '! 分裂顺序反转', fontproperties=fp_tiny,
                    ha='center', va='top', color='gray')
            ax.text(1.5, -1.5, 'CN=4 | 正四面体\n$\\Delta_t$=(4/9)$\\Delta_o$',
                    fontproperties=fp_tiny, ha='center', va='top')

        elif config == 'd4h':
            # Square planar: 4 levels
            levels = [
                (3.5, '$d_{x^2-y^2}$'),
                (2.0, '$d_{z^2}$'),
                (0.8, '$d_{xy}$'),
                (-0.2, '$d_{xz}$, $d_{yz}$'),
            ]
            for j, (y, label) in enumerate(levels):
                n_lines = 2 if j == 3 else 1
                for k in range(n_lines):
                    offset = (k - 0.5) * 0.15 if n_lines > 1 else 0
                    draw_horizontal_line(ax, x + offset, y, length=0.2, lw=2)
                ax.text(x + 0.5, y, label, fontproperties=fp_small, va='center')
            # Delta arrow
            draw_arrow(ax, 3.3, -0.2, 3.5, text='$\\Delta_{sp}$', side='right', fontprop=fp_label)
            ax.text(1.5, -1.5, 'CN=4 | 正方形\n$\\Delta_{sp}$>$\\Delta_o$',
                    fontproperties=fp_tiny, ha='center', va='top')

    fig.savefig(os.path.join(OUT_DIR, 'three-field-splitting-comparison-bw.png'),
                dpi=DPI, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print("OK: three-field-splitting-comparison-bw.png")


# ============================================================
# IMAGE 3: High/Low Spin Decision Tree
# ============================================================
def gen_decision_tree():
    fig, ax = plt.subplots(1, 1, figsize=(8, 7))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Title
    ax.text(5, 9.7, '高/低自旋判断决策树', fontproperties=fp_title,
            ha='center', va='top')

    # Helper: draw rounded box
    def draw_box(ax, x, y, w, h, text, fc='white', ec='black', lw=1.5):
        rect = mpatches.FancyBboxPatch((x - w/2, y - h/2), w, h,
                boxstyle='round,pad=0.1', facecolor=fc, edgecolor=ec, linewidth=lw)
        ax.add_patch(rect)
        ax.text(x, y, text, fontproperties=fp_small, ha='center', va='center',
                multialignment='center')

    # Helper: draw diamond
    def draw_diamond(ax, x, y, w, h, text, fc='#f0f0f0', ec='black'):
        diamond = plt.Polygon([(x, y+h/2), (x+w/2, y), (x, y-h/2), (x-w/2, y)],
                              facecolor=fc, edgecolor=ec, linewidth=1.5)
        ax.add_patch(diamond)
        ax.text(x, y, text, fontproperties=fp_small, ha='center', va='center',
                multialignment='center')

    # Helper: draw arrow between points
    def draw_conn(ax, x1, y1, x2, y2, text=''):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color='black', lw=1.5))
        if text:
            mx, my = (x1+x2)/2, (y1+y2)/2
            ax.text(mx + 0.15, my, text, fontproperties=fp_tiny, ha='left', va='center')

    # Step 1: Start
    draw_box(ax, 5, 8.8, 3.0, 0.6, '确定 dⁿ 组态', fc='#d0d0d0')

    # Diamond 1: d4-d7?
    draw_diamond(ax, 5, 7.5, 3.0, 1.0, 'd 电子数在\nd⁴-d⁷ ?')

    draw_conn(ax, 5, 8.5, 5, 8.0)

    # No branch
    draw_conn(ax, 3.5, 7.5, 1.5, 7.5, '否')
    draw_box(ax, 1.5, 7.5, 2.5, 0.6, 'd¹-d³ / d⁸-d¹⁰\n只有一种排布', fc='#f5e0e0')

    # Yes branch
    draw_conn(ax, 5, 7.0, 5, 6.2, '是')

    # Diamond 2: Geometry?
    draw_diamond(ax, 5, 5.5, 3.0, 1.0, '几何构型?\nOh / Td / D₄h')

    # Td branch (left)
    draw_conn(ax, 3.5, 5.5, 1.5, 5.5, 'Td')
    draw_box(ax, 1.5, 5.5, 2.5, 0.6, '四面体 Td\nΔ小 → 全 HS', fc='#e0f0e0')

    # D4h branch (right)
    draw_conn(ax, 6.5, 5.5, 8.5, 5.5, 'D₄h')
    draw_box(ax, 8.5, 5.5, 2.5, 0.6, '正方形 D₄h\nΔ大 → 全 LS', fc='#e0e0f0')

    # Oh branch (down)
    draw_conn(ax, 5, 5.0, 5, 4.2, 'Oh')

    # Diamond 3: Δo > P?
    draw_diamond(ax, 5, 3.5, 3.0, 1.0, 'Δₒ > P ?\n(强场 vs 弱场)')

    # Yes → Low spin
    draw_conn(ax, 3.5, 3.5, 1.5, 3.5, '是')
    draw_box(ax, 1.5, 3.5, 2.5, 0.6, '低自旋 LS\n强场配体', fc='#d0e0f0')

    # No → High spin
    draw_conn(ax, 6.5, 3.5, 8.5, 3.5, '否')
    draw_box(ax, 8.5, 3.5, 2.5, 0.6, '高自旋 HS\n弱场配体', fc='#f5e0e0')

    # Note at bottom
    ax.text(5, 1.8, '注意: 高低自旋只对 Oh 场的 d4-d7 有选择\n-> Td 全 HS, D4h 全 LS',
            fontproperties=fp_small, ha='center', va='top',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='lightyellow', edgecolor='gray'))

    # Magnetic moment formula
    ax.text(5, 0.5, '磁矩: mu = sqrt[n(n+2)] B.M.  (n = 未成对电子数)',
            fontproperties=fp_tiny, ha='center', va='center', color='gray')

    fig.savefig(os.path.join(OUT_DIR, 'high-low-spin-decision-tree-bw.png'),
                dpi=DPI, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print("OK: high-low-spin-decision-tree-bw.png")


# ============================================================
# IMAGE 4: CFSE Calculation Flow
# ============================================================
def gen_cfse_flow():
    fig, ax = plt.subplots(1, 1, figsize=(9, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Title
    ax.text(5, 9.7, 'CFSE 计算四步流程', fontproperties=fp_title,
            ha='center', va='top')

    # Step boxes
    steps = [
        (8.5, 'Step 1: 确定 d^n 组态', '中心离子氧化态 -> 价电子数 -> 剩余 d 电子数', '#d0e8f0'),
        (7.0, 'Step 2: 确定几何构型', '配位数 -> Oh(6) / Td(4) / D4h(4)', '#d0e8d0'),
        (5.5, 'Step 3: 填充电子', '按分裂能级顺序 (Hund规则)\nt2g 先填再 eg', '#e8e0d0'),
        (4.0, 'Step 4: 代入公式', 'CFSE = (-0.4n_t2g + 0.6n_eg)*Delta_o\n+ 成对能修正', '#f0e8d0'),
    ]

    for y, title, desc, color in steps:
        # Main box
        rect = mpatches.FancyBboxPatch((1.5, y - 0.45), 5.0, 0.9,
                boxstyle='round,pad=0.1', facecolor=color, edgecolor='black', linewidth=1.5)
        ax.add_patch(rect)
        ax.text(4.0, y + 0.1, title, fontproperties=fp_label, fontweight='bold',
                ha='center', va='center')
        ax.text(4.0, y - 0.2, desc, fontproperties=fp_tiny, ha='center', va='center',
                multialignment='center')

    # Arrows between steps
    for i in range(3):
        y1 = steps[i][0] - 0.45
        y2 = steps[i+1][0] + 0.45
        ax.annotate('', xy=(4, y2), xytext=(4, y1),
                    arrowprops=dict(arrowstyle='->', color='black', lw=1.5))

    # Side note box
    note_lines = [
        '高/低自旋判断要点:',
        '* d1-d3 / d8-d10: 只有一种',
        '* d4-d7: Delta>P->LS, Delta<P->HS',
        '* Td场 Delta很小 -> 全HS',
        '* D4h场 Delta很大 -> 全LS',
        '* d5 HS: CFSE=0!',
    ]
    note_text = '\n'.join(note_lines)
    rect = mpatches.FancyBboxPatch((7.0, 5.5), 2.8, 2.5,
            boxstyle='round,pad=0.1', facecolor='white', edgecolor='gray',
            linewidth=1, linestyle='--')
    ax.add_patch(rect)
    ax.text(8.4, 6.75, note_text, fontproperties=fp_tiny, ha='center', va='center',
            multialignment='center')

    # Bottom formulas
    formulas = [
        '> Oh场: CFSE = -0.4*Delta_o*n(t2g) + 0.6*Delta_o*n(eg)',
        '> Td场: Delta_t = (4/9)*Delta_o, CFSE = -0.6*Delta_t*n(e) + 0.4*Delta_t*n(t2)',
        '> D4h场: 分裂为4层能级, 需逐层计算',
    ]
    for i, f in enumerate(formulas):
        ax.text(1.5, 2.8 - i * 0.4, f, fontproperties=fp_small, ha='left', va='center')

    # Example
    ax.text(5, 1.2,
            '示例: [Fe(CN)6]4- -> Fe2+(d6) -> Oh -> LS(Delta>P)\n'
            '-> t2g6 eg0 -> CFSE = 6*(-0.4*Delta_o) = -2.4*Delta_o + 3P',
            fontproperties=fp_tiny, ha='center', va='center', color='gray',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', alpha=0.7))

    fig.savefig(os.path.join(OUT_DIR, 'cfse-calculation-flow-bw.png'),
                dpi=DPI, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print("OK: cfse-calculation-flow-bw.png")


# Run all
if __name__ == '__main__':
    os.makedirs(OUT_DIR, exist_ok=True)
    gen_octahedral_splitting()
    gen_three_field()
    gen_decision_tree()
    gen_cfse_flow()
    print("\nAll 4 images generated successfully!")
