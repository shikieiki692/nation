"""
Generate 5 black-and-white matplotlib diagrams to replace Excalidraw hand-drawn images.
All figures are designed for clean B&W printing.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import os

DPI = 200
OUT = r'C:\Obsidion\妙妙屋\media'

# ============================================================
# Figure 1: 点阵·结构基元·晶胞 三要素关系图
# ============================================================
def fig_lattice_motif_unitcell():
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_aspect('equal')

    # Title
    ax.text(5, 6.5, '点阵·结构基元·晶胞 三要素关系', fontsize=16, fontweight='bold',
            ha='center', va='center', fontfamily='SimHei')

    # Core equation box
    eq_box = FancyBboxPatch((2.5, 5.5), 5, 0.7, boxstyle="round,pad=0.1",
                             facecolor='#f0f0f0', edgecolor='black', linewidth=1.5)
    ax.add_patch(eq_box)
    ax.text(5, 5.85, '晶体结构 = 点阵 + 结构基元', fontsize=13, fontweight='bold',
            ha='center', va='center', fontfamily='SimHei')

    # Lattice box (left)
    lat_box = FancyBboxPatch((0.3, 2.8), 3.8, 2.2, boxstyle="round,pad=0.15",
                              facecolor='white', edgecolor='black', linewidth=1.5)
    ax.add_patch(lat_box)
    ax.text(2.2, 4.7, '点阵 (Lattice)', fontsize=13, fontweight='bold',
            ha='center', va='center', fontfamily='SimHei')
    ax.text(2.2, 4.15, '抽象几何点的周期性排列', fontsize=9, ha='center', va='center', fontfamily='SimHei')
    ax.text(2.2, 3.7, '每个点的周围环境完全相同', fontsize=9, ha='center', va='center', fontfamily='SimHei')
    ax.text(2.2, 3.2, '框架——几何位置关系', fontsize=10, ha='center', va='center',
            fontfamily='SimHei', fontstyle='italic')

    # Motif box (right)
    mot_box = FancyBboxPatch((5.9, 2.8), 3.8, 2.2, boxstyle="round,pad=0.15",
                              facecolor='white', edgecolor='black', linewidth=1.5)
    ax.add_patch(mot_box)
    ax.text(7.8, 4.7, '结构基元 (Motif)', fontsize=13, fontweight='bold',
            ha='center', va='center', fontfamily='SimHei')
    ax.text(7.8, 4.15, '重复排列的具体内容', fontsize=9, ha='center', va='center', fontfamily='SimHei')
    ax.text(7.8, 3.7, '含什么 + 怎么排列', fontsize=9, ha='center', va='center', fontfamily='SimHei')
    ax.text(7.8, 3.2, '内容——原子/离子/分子组合', fontsize=10, ha='center', va='center',
            fontfamily='SimHei', fontstyle='italic')

    # Plus sign
    ax.text(5, 3.9, '+', fontsize=28, ha='center', va='center', color='gray')

    # Down arrow
    ax.annotate('', xy=(5, 2.5), xytext=(5, 2.8),
                arrowprops=dict(arrowstyle='->', lw=2, color='black'))

    # Unit cell box (bottom)
    uc_box = FancyBboxPatch((1.5, 0.5), 7, 1.8, boxstyle="round,pad=0.15",
                             facecolor='#f0f0f0', edgecolor='black', linewidth=1.5)
    ax.add_patch(uc_box)
    ax.text(5, 1.9, '晶胞 (Unit Cell)', fontsize=13, fontweight='bold',
            ha='center', va='center', fontfamily='SimHei')
    ax.text(5, 1.3, '点阵 × 结构基元 → 晶胞 → 平移复制 → 整个晶体', fontsize=10,
            ha='center', va='center', fontfamily='SimHei')

    # Example box (bottom)
    ex_box = FancyBboxPatch((0.3, -0.8), 9.4, 1.0, boxstyle="round,pad=0.1",
                             facecolor='white', edgecolor='gray', linewidth=1, linestyle='--')
    ax.add_patch(ex_box)
    ax.text(5, -0.3, '实例：NaCl点阵=fcc, 基元=1×NaCl | CsCl点阵=简单立方, 基元=1×CsCl | 金刚石点阵=fcc, 基元=2×C',
            fontsize=8, ha='center', va='center', fontfamily='SimHei', color='#444444')

    # Arrows from equation to boxes
    ax.annotate('', xy=(2.2, 5.0), xytext=(3.5, 5.5),
                arrowprops=dict(arrowstyle='->', lw=1.5, color='black'))
    ax.annotate('', xy=(7.8, 5.0), xytext=(6.5, 5.5),
                arrowprops=dict(arrowstyle='->', lw=1.5, color='black'))

    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '图-点阵结构基元晶胞关系.png'), dpi=DPI, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("OK: 点阵·结构基元·晶胞关系图")


# ============================================================
# Figure 2: 七大晶系判定决策树
# ============================================================
def fig_crystal_system_decision():
    fig, ax = plt.subplots(figsize=(10, 9))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 11)
    ax.axis('off')

    ax.text(6, 10.5, '七大晶系判定决策树', fontsize=16, fontweight='bold',
            ha='center', va='center', fontfamily='SimHei')

    def draw_box(x, y, text, w=3.0, h=0.65, fc='white', fs=9):
        box = FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.08",
                              facecolor=fc, edgecolor='black', linewidth=1.2)
        ax.add_patch(box)
        ax.text(x, y, text, fontsize=fs, ha='center', va='center', fontfamily='SimHei')

    def arrow(x1, y1, x2, y2, text='', side='right'):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', lw=1.2, color='black'))
        if text:
            mx, my = (x1+x2)/2, (y1+y2)/2
            offset = 0.12 if side == 'right' else -0.12
            ax.text(mx + offset, my, text, fontsize=8, ha='center', va='center',
                    fontfamily='SimHei', color='#333333',
                    bbox=dict(boxstyle='round,pad=0.08', facecolor='white', edgecolor='none', alpha=0.9))

    # Start
    draw_box(6, 9.7, '有4个C3轴？', fc='#e8e8e8', fs=10)
    arrow(6, 9.35, 6, 8.6, '是')

    # Branch
    draw_box(6, 8.2, '最高对称轴类型？', fc='#f5f5f5', fs=10)

    # Cubic (left)
    arrow(6, 7.9, 2.5, 7.0, '4个C3轴', 'left')
    draw_box(2.5, 6.6, '立方晶系\na=b=c, a=b=g=90', fc='#d8d8d8', h=0.85, fs=9)

    # Rhombohedral (right)
    arrow(6, 7.9, 9.5, 7.0, '1个C3或i3轴', 'right')
    draw_box(9.5, 6.6, '菱方(三方)\na=b=c, a=b=g<120', fc='#d8d8d8', h=0.85, fs=9)

    # Middle
    arrow(6, 7.9, 6, 7.0, '1个C4或i4轴')
    draw_box(6, 6.6, '有C6或i6轴？', fc='#f5f5f5', fs=9)

    # Tetragonal (left of center)
    arrow(6, 6.3, 3.5, 5.4, '无')
    draw_box(3.5, 5.0, '四方晶系\na=b!=c, a=b=g=90', fc='#d8d8d8', h=0.85, fs=9)

    # Hexagonal (center)
    arrow(6, 6.3, 6, 5.4, '是')
    draw_box(6, 5.0, '六方晶系\na=b!=c, g=120', fc='#d8d8d8', h=0.85, fs=9)

    # Orthorhombic
    arrow(6, 7.9, 6, 3.8, '3个C2轴或镜面')
    draw_box(6, 3.4, '正交晶系\na!=b!=c, a=b=g=90', fc='#d8d8d8', h=0.85, fs=9)

    # Monoclinic
    arrow(6, 7.9, 9.5, 3.8, '1个C2轴或镜面', 'right')
    draw_box(9.5, 3.4, '单斜晶系\nb!=90', fc='#d8d8d8', h=0.85, fs=9)

    # Triclinic
    arrow(6, 7.9, 9.5, 2.0, '无(仅C1或i)', 'right')
    draw_box(9.5, 1.6, '三斜晶系\na!=b!=g', fc='#d8d8d8', h=0.85, fs=9)

    # Note
    ax.text(1, 0.5, '注: 晶系由最高对称轴决定, 不仅看轴长轴角', fontsize=8,
            ha='left', va='center', fontfamily='SimHei', color='gray')

    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '图-七大晶系判定决策树.png'), dpi=DPI, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("OK: 七大晶系判定决策树")


# ============================================================
# Figure 3: 分数坐标三维可视化
# ============================================================
def fig_fractional_coordinates():
    fig = plt.figure(figsize=(7, 6))
    ax = fig.add_subplot(111, projection='3d')

    # Draw unit cell edges
    # Front face
    ax.plot([0,1,1,0,0], [0,0,0,0,0], [0,0,1,1,0], 'k-', lw=1.5)
    # Back face
    ax.plot([0,1,1,0,0], [1,1,1,1,1], [0,0,1,1,0], 'k-', lw=1.5, alpha=0.4)
    # Connecting edges
    ax.plot([0,0], [0,1], [0,0], 'k-', lw=1.5, alpha=0.4)
    ax.plot([1,1], [0,1], [0,0], 'k-', lw=1.5, alpha=0.4)
    ax.plot([1,1], [0,1], [1,1], 'k-', lw=1.5)
    ax.plot([0,0], [0,1], [1,1], 'k-', lw=1.5)

    # Axes
    ax.quiver(0, 0, 0, 0.4, 0, 0, color='black', arrow_length_ratio=0.2, lw=1.5)
    ax.quiver(0, 0, 0, 0, 0.4, 0, color='black', arrow_length_ratio=0.2, lw=1.5)
    ax.quiver(0, 0, 0, 0, 0, 0.4, color='black', arrow_length_ratio=0.2, lw=1.5)

    ax.text(0.5, -0.08, -0.08, 'a / x', fontsize=11, fontfamily='SimHei')
    ax.text(-0.08, 0.5, -0.08, 'b / y', fontsize=11, fontfamily='SimHei')
    ax.text(-0.08, -0.08, 0.5, 'c / z', fontsize=11, fontfamily='SimHei')

    # Key points
    points = {
        '(0,0,0)': (0, 0, 0),
        '(1,0,0)': (1, 0, 0),
        '(0,1,0)': (0, 1, 0),
        '(0,0,1)': (0, 0, 1),
        '(1,1,1)': (1, 1, 1),
        '(1/2,1/2,1/2)': (0.5, 0.5, 0.5),
        '(1/2,1/2,0)': (0.5, 0.5, 0),
        '(1/2,0,1/2)': (0.5, 0, 0.5),
        '(0,1/2,1/2)': (0, 0.5, 0.5),
    }

    # Draw points
    for label, (x, y, z) in points.items():
        if label == '(½,½,½)':
            ax.scatter([x], [y], [z], c='black', s=60, zorder=5, marker='D')
        elif '½' in label:
            ax.scatter([x], [y], [z], c='gray', s=40, zorder=5, marker='s')
        else:
            ax.scatter([x], [y], [z], c='black', s=50, zorder=5, marker='o')

    # Labels with offsets
    offsets = {
        '(0,0,0)': (-0.08, -0.12, -0.05),
        '(1,1,1)': (0.05, 0.05, 0.05),
        '(1/2,1/2,1/2)': (0.08, 0, 0),
        '(1/2,1/2,0)': (0.05, 0.05, -0.08),
        '(1/2,0,1/2)': (0.08, -0.05, 0),
        '(0,1/2,1/2)': (-0.12, 0, 0),
    }

    for label, (x, y, z) in points.items():
        if label in offsets:
            ox, oy, oz = offsets[label]
            ax.text(x+ox, y+oy, z+oz, label, fontsize=8, fontfamily='SimHei')

    # Table on the side (as text)
    table_text = (
        "Common positions:\n"
        "Corner: (0,0,0)\n"
        "Body: (1/2,1/2,1/2)\n"
        "Face: (1/2,1/2,0) etc\n"
        "Edge: (1/2,0,0) etc"
    )
    ax.text2D(0.72, 0.85, table_text, fontsize=8, fontfamily='SimHei',
              transform=ax.transAxes, verticalalignment='top',
              bbox=dict(boxstyle='round,pad=0.3', facecolor='#f5f5f5', edgecolor='gray'))

    ax.set_xlim(-0.1, 1.2)
    ax.set_ylim(-0.1, 1.2)
    ax.set_zlim(-0.1, 1.2)
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_zlabel('')
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('w')
    ax.yaxis.pane.set_edgecolor('w')
    ax.zaxis.pane.set_edgecolor('w')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.view_init(elev=20, azim=130)
    ax.set_box_aspect([1,1,1])

    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '图-分数坐标三维可视化.png'), dpi=DPI, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("OK: 分数坐标三维可视化")


# ============================================================
# Figure 4: 晶胞原子计数示意图
# ============================================================
def fig_atom_counting():
    fig, axes = plt.subplots(2, 2, figsize=(8, 7))

    configs = [
        ('顶角原子: 贡献 1/8', [(0,0), (1,0), (1,1), (0,1)], 0.125, '8 × 1/8 = 1'),
        ('棱心原子: 贡献 1/4', [(0.5,0), (1,0.5), (0.5,1), (0,0.5)], 0.25, '12 × 1/4 = 3'),
        ('面心原子: 贡献 1/2', [(0.5,0.5)], 0.5, '6 × 1/2 = 3'),
        ('体内原子: 贡献 1', [(0.5,0.5)], 1.0, '体内 × 1 = 1'),
    ]

    for ax, (title, positions, fraction, calc) in zip(axes.flat, configs):
        ax.set_xlim(-0.3, 1.6)
        ax.set_ylim(-0.3, 1.6)
        ax.set_aspect('equal')
        ax.axis('off')

        # Draw unit cell (square for simplicity)
        rect = plt.Rectangle((0, 0), 1, 1, fill=False, edgecolor='black', lw=1.5)
        ax.add_patch(rect)

        # Draw atoms
        for px, py in positions:
            circle = plt.Circle((px, py), 0.08, facecolor='black', edgecolor='black', zorder=5)
            ax.add_patch(circle)

        # Title
        ax.set_title(title, fontsize=10, fontfamily='SimHei', pad=8)

        # Fraction label
        frac_str = f'{fraction:.3g}'.rstrip('0').rstrip('.')
        ax.text(0.5, -0.2, f'每个原子贡献 = {frac_str}', fontsize=9,
                ha='center', va='center', fontfamily='SimHei')

        # Calculation
        ax.text(0.5, -0.35, calc, fontsize=9, ha='center', va='center',
                fontfamily='SimHei', fontweight='bold')

    fig.suptitle('晶胞中原子的计数规则', fontsize=14, fontweight='bold',
                 fontfamily='SimHei', y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(os.path.join(OUT, '图-晶胞原子计数示意图.png'), dpi=DPI, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("OK: 晶胞原子计数示意图")


# ============================================================
# Figure 5: 晶体对称性限制定律
# ============================================================
def fig_symmetry_limitation():
    fig, axes = plt.subplots(2, 4, figsize=(10, 5))

    # For each n, draw n-fold rotation around a point and show if it tiles
    n_values = [1, 2, 3, 4, 5, 6, 7, 8]
    allowed = {1, 2, 3, 4, 6}

    for ax, n in zip(axes.flat, n_values):
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_aspect('equal')
        ax.axis('off')

        # Draw rotation axes
        angle = 360 / n
        for i in range(n):
            theta = np.radians(i * angle)
            x, y = np.cos(theta), np.sin(theta)
            ax.plot([0, x*1.2], [0, y*1.2], 'k-', lw=1.5)

        # Draw the polygon that would be formed
        if n in allowed:
            polygon = plt.Polygon(
                [(np.cos(np.radians(i * angle)), np.sin(np.radians(i * angle))) for i in range(n)],
                fill=False, edgecolor='black', lw=2
            )
            ax.add_patch(polygon)
            status = 'ALLOWED'
            color = 'black'
        else:
            # Show incomplete coverage
            for i in range(n):
                theta1 = np.radians(i * angle)
                theta2 = np.radians((i + 1) * angle)
                arc_x = [0] + [np.cos(np.radians(t)) for t in np.linspace(i*angle, (i+1)*angle, 20)] + [0]
                arc_y = [0] + [np.sin(np.radians(t)) for t in np.linspace(i*angle, (i+1)*angle, 20)] + [0]
                ax.fill(arc_x, arc_y, alpha=0.15, color='gray')
            # Draw gap indicator
            ax.plot([0, 1.3], [0, 0], 'k--', lw=0.8, alpha=0.5)
            status = 'NOT ALLOWED'
            color = 'gray'

        ax.set_title(f'C{subscript_str(n)}  ({angle:.1f}°)', fontsize=10, fontfamily='SimHei',
                     fontweight='bold', color=color, pad=5)
        ax.text(0, -1.35, status, fontsize=8, ha='center', va='center',
                fontfamily='SimHei', color=color, fontweight='bold')

    fig.suptitle('晶体对称性限制定律：旋转轴轴次只能为 n = 1, 2, 3, 4, 6',
                 fontsize=12, fontweight='bold', fontfamily='SimHei', y=1.02)
    fig.text(0.5, -0.05, '原因：平移对称性要求旋转操作必须能无隙并置地铺满空间——n=5 和 n>6 无法满足此条件',
             fontsize=9, ha='center', fontfamily='SimHei', color='gray')
    plt.tight_layout(rect=[0, 0.05, 1, 0.95])
    plt.savefig(os.path.join(OUT, '图-对称性限制定律.png'), dpi=DPI, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("OK: 对称性限制定律")


def subscript_str(n):
    # Use regular text to avoid font issues
    return str(n)


# ============================================================
# Run all
# ============================================================
if __name__ == '__main__':
    fig_lattice_motif_unitcell()
    fig_crystal_system_decision()
    fig_fractional_coordinates()
    fig_atom_counting()
    fig_symmetry_limitation()
    print("\nAll 5 diagrams generated successfully!")
