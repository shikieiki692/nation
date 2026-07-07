"""Generate d-orbital splitting diagrams and other chemistry figures for the topic class handout."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

MEDIA = r'C:\Obsidion\妙妙屋\media'
os.makedirs(MEDIA, exist_ok=True)

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False


def draw_orbital_box(ax, x, y, w=0.35, label='', color='black'):
    """Draw a single orbital energy level box."""
    rect = patches.FancyBboxPatch((x - w/2, y - 0.06), w, 0.12,
                                   boxstyle="round,pad=0.01",
                                   linewidth=1.2, edgecolor=color, facecolor='white')
    ax.add_patch(rect)
    if label:
        ax.text(x, y, label, ha='center', va='center', fontsize=8, color=color)


def draw_arrow(ax, x, y_start, y_end, color='black', head_width=0.03):
    """Draw an up/down arrow for electron."""
    ax.annotate('', xy=(x, y_end), xytext=(x, y_start),
                arrowprops=dict(arrowstyle='->', color=color, lw=1.5),
                annotation_clip=False)


def draw_up_down_arrows(ax, x, y_center, color='black'):
    """Draw paired electrons (up + down arrows) in one orbital."""
    draw_arrow(ax, x - 0.04, y_center - 0.04, y_center + 0.04, color)
    draw_arrow(ax, x + 0.04, y_center + 0.04, y_center - 0.04, color)


def draw_single_arrow(ax, x, y_center, direction='up', color='black'):
    """Draw single electron (one arrow) in one orbital."""
    if direction == 'up':
        draw_arrow(ax, x, y_center - 0.04, y_center + 0.04, color)
    else:
        draw_arrow(ax, x, y_center + 0.04, y_center - 0.04, color)


def generic_octahedral_splitting(save_path=None):
    """Generic octahedral d-orbital splitting diagram (empty, no electrons)."""
    fig, ax = plt.subplots(1, 1, figsize=(4.5, 3.2))
    ax.set_xlim(-0.5, 3.0)
    ax.set_ylim(-0.3, 2.5)
    ax.set_aspect('equal')
    ax.axis('off')

    # Energy axis
    ax.annotate('', xy=(-0.3, 2.2), xytext=(-0.3, 0.2),
                arrowprops=dict(arrowstyle='->', color='gray', lw=1.0))
    ax.text(-0.4, 1.2, '能量', ha='center', va='center', fontsize=9, color='gray',
            rotation=90)

    # t2g level (3 orbitals)
    t2g_y = 0.7
    t2g_x = [0.8, 1.3, 1.8]
    for x in t2g_x:
        draw_orbital_box(ax, x, t2g_y)

    # eg level (2 orbitals)
    eg_y = 1.7
    eg_x = [1.05, 1.55]
    for x in eg_x:
        draw_orbital_box(ax, x, eg_y)

    # Delta_o arrow
    ax.annotate('', xy=(2.5, eg_y), xytext=(2.5, t2g_y),
                arrowprops=dict(arrowstyle='<->', color='#C0392B', lw=1.5))
    ax.text(2.75, (eg_y + t2g_y) / 2, '$\\Delta_o$', ha='center', va='center',
            fontsize=11, color='#C0392B', fontweight='bold')

    # Labels
    ax.text(1.3, t2g_y - 0.25, '$t_{2g}$', ha='center', va='center', fontsize=11, fontweight='bold')
    ax.text(1.3, t2g_y - 0.45, '($d_{xy}, d_{xz}, d_{yz}$)', ha='center', va='center', fontsize=8, color='gray')
    ax.text(1.3, eg_y + 0.25, '$e_g$', ha='center', va='center', fontsize=11, fontweight='bold')
    ax.text(1.3, eg_y + 0.45, '($d_{x^2\\!-\\!y^2},\\, d_{z^2}$)', ha='center', va='center', fontsize=8, color='gray')

    # Octahedral label
    ax.text(1.3, -0.15, '八面体场', ha='center', va='center', fontsize=10, color='#2C3E50')

    plt.tight_layout()
    path = save_path or os.path.join(MEDIA, 'cft-octahedral-generic.png')
    fig.savefig(path, dpi=250, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    return path


def octahedral_d6_lowspin(save_path=None):
    """Octahedral d-orbital splitting: d6 low-spin (Ru2+), t2g6 eg0."""
    fig, ax = plt.subplots(1, 1, figsize=(4.5, 3.5))
    ax.set_xlim(-0.5, 3.0)
    ax.set_ylim(-0.5, 2.8)
    ax.set_aspect('equal')
    ax.axis('off')

    # Energy axis
    ax.annotate('', xy=(-0.3, 2.5), xytext=(-0.3, 0.0),
                arrowprops=dict(arrowstyle='->', color='gray', lw=1.0))
    ax.text(-0.45, 1.25, '能量', ha='center', va='center', fontsize=9, color='gray',
            rotation=90)

    # t2g level — 6 electrons (3 paired)
    t2g_y = 0.6
    t2g_x = [0.8, 1.3, 1.8]
    for x in t2g_x:
        draw_orbital_box(ax, x, t2g_y)
        draw_up_down_arrows(ax, x, t2g_y)

    # eg level — 0 electrons (empty)
    eg_y = 1.7
    eg_x = [1.05, 1.55]
    for x in eg_x:
        draw_orbital_box(ax, x, eg_y, color='#95A5A6')

    # Delta_o
    ax.annotate('', xy=(2.5, eg_y), xytext=(2.5, t2g_y),
                arrowprops=dict(arrowstyle='<->', color='#C0392B', lw=1.5))
    ax.text(2.75, (eg_y + t2g_y) / 2, '$\\Delta_o$', ha='center', va='center',
            fontsize=11, color='#C0392B', fontweight='bold')

    # Labels
    ax.text(1.3, t2g_y - 0.25, '$t_{2g}$', ha='center', fontsize=11, fontweight='bold')
    ax.text(1.3, t2g_y - 0.45, '6e  (全充满)', ha='center', fontsize=8, color='#27AE60')
    ax.text(1.3, eg_y + 0.25, '$e_g$', ha='center', fontsize=11, fontweight='bold', color='#95A5A6')
    ax.text(1.3, eg_y + 0.45, '0e  (空)', ha='center', fontsize=8, color='#95A5A6')

    # Info box
    ax.text(1.3, -0.25, '$\\Delta_o > P$（强场）→ 低自旋 → 抗磁性',
            ha='center', fontsize=9, color='#2C3E50',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#EBF5FB', edgecolor='#3498DB', alpha=0.8))

    plt.tight_layout()
    path = save_path or os.path.join(MEDIA, 'cft-octahedral-d6-lowspin.png')
    fig.savefig(path, dpi=250, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    return path


def octahedral_d5_lowspin(save_path=None):
    """Octahedral d-orbital splitting: d5 low-spin (Ru3+), t2g5 eg0."""
    fig, ax = plt.subplots(1, 1, figsize=(4.5, 3.5))
    ax.set_xlim(-0.5, 3.0)
    ax.set_ylim(-0.5, 2.8)
    ax.set_aspect('equal')
    ax.axis('off')

    # Energy axis
    ax.annotate('', xy=(-0.3, 2.5), xytext=(-0.3, 0.0),
                arrowprops=dict(arrowstyle='->', color='gray', lw=1.0))
    ax.text(-0.45, 1.25, '能量', ha='center', va='center', fontsize=9, color='gray',
            rotation=90)

    # t2g level — 5 electrons (2 paired + 1 single)
    t2g_y = 0.6
    t2g_x = [0.8, 1.3, 1.8]
    for x in t2g_x[:2]:
        draw_orbital_box(ax, x, t2g_y)
        draw_up_down_arrows(ax, x, t2g_y)
    # Third orbital: single electron
    draw_orbital_box(ax, t2g_x[2], t2g_y)
    draw_single_arrow(ax, t2g_x[2], t2g_y, 'up')

    # eg level — 0 electrons
    eg_y = 1.7
    eg_x = [1.05, 1.55]
    for x in eg_x:
        draw_orbital_box(ax, x, eg_y, color='#95A5A6')

    # Delta_o
    ax.annotate('', xy=(2.5, eg_y), xytext=(2.5, t2g_y),
                arrowprops=dict(arrowstyle='<->', color='#C0392B', lw=1.5))
    ax.text(2.75, (eg_y + t2g_y) / 2, '$\\Delta_o$', ha='center', va='center',
            fontsize=11, color='#C0392B', fontweight='bold')

    # Labels
    ax.text(1.3, t2g_y - 0.25, '$t_{2g}$', ha='center', fontsize=11, fontweight='bold')
    ax.text(1.3, t2g_y - 0.45, '5e  (2对+1单)', ha='center', fontsize=8, color='#E67E22')
    ax.text(1.3, eg_y + 0.25, '$e_g$', ha='center', fontsize=11, fontweight='bold', color='#95A5A6')
    ax.text(1.3, eg_y + 0.45, '0e  (空)', ha='center', fontsize=8, color='#95A5A6')

    # Info box
    ax.text(1.3, -0.25, '$\\Delta_o > P$（强场）→ 低自旋 → 1个单电子 → 顺磁性',
            ha='center', fontsize=9, color='#2C3E50',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#FEF9E7', edgecolor='#F39C12', alpha=0.8))

    plt.tight_layout()
    path = save_path or os.path.join(MEDIA, 'cft-octahedral-d5-lowspin.png')
    fig.savefig(path, dpi=250, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    return path


def octahedral_d7_highspin(save_path=None):
    """Octahedral d-orbital splitting: d7 high-spin (Co2+), t2g5 eg2."""
    fig, ax = plt.subplots(1, 1, figsize=(4.5, 3.5))
    ax.set_xlim(-0.5, 3.0)
    ax.set_ylim(-0.5, 2.8)
    ax.set_aspect('equal')
    ax.axis('off')

    # Energy axis
    ax.annotate('', xy=(-0.3, 2.5), xytext=(-0.3, 0.0),
                arrowprops=dict(arrowstyle='->', color='gray', lw=1.0))
    ax.text(-0.45, 1.25, '能量', ha='center', va='center', fontsize=9, color='gray',
            rotation=90)

    # t2g level — 5 electrons
    t2g_y = 0.6
    t2g_x = [0.8, 1.3, 1.8]
    for x in t2g_x[:2]:
        draw_orbital_box(ax, x, t2g_y)
        draw_up_down_arrows(ax, x, t2g_y)
    draw_orbital_box(ax, t2g_x[2], t2g_y)
    draw_single_arrow(ax, t2g_x[2], t2g_y, 'up')

    # eg level — 2 electrons (2 single)
    eg_y = 1.7
    eg_x = [1.05, 1.55]
    for x in eg_x:
        draw_orbital_box(ax, x, eg_y)
        draw_single_arrow(ax, x, eg_y, 'up')

    # Delta_o (smaller for weak field)
    ax.annotate('', xy=(2.5, eg_y), xytext=(2.5, t2g_y),
                arrowprops=dict(arrowstyle='<->', color='#C0392B', lw=1.5))
    ax.text(2.75, (eg_y + t2g_y) / 2, '$\\Delta_o$', ha='center', va='center',
            fontsize=11, color='#C0392B', fontweight='bold')

    # Labels
    ax.text(1.3, t2g_y - 0.25, '$t_{2g}$', ha='center', fontsize=11, fontweight='bold')
    ax.text(1.3, t2g_y - 0.45, '5e  (2对+1单)', ha='center', fontsize=8, color='#E67E22')
    ax.text(1.3, eg_y + 0.25, '$e_g$', ha='center', fontsize=11, fontweight='bold')
    ax.text(1.3, eg_y + 0.45, '2e  (2单)', ha='center', fontsize=8, color='#E74C3C')

    # Info box
    ax.text(1.3, -0.25, '3个单电子 → 顺磁性  $\\mu = \\sqrt{3(3+2)} \\approx 3.87\\,\\mu_B$',
            ha='center', fontsize=9, color='#2C3E50',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#FEF9E7', edgecolor='#F39C12', alpha=0.8))

    plt.tight_layout()
    path = save_path or os.path.join(MEDIA, 'cft-octahedral-d7-highspin.png')
    fig.savefig(path, dpi=250, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    return path


def high_low_spin_decision(save_path=None):
    """High/low spin decision flowchart."""
    fig, ax = plt.subplots(1, 1, figsize=(6, 4.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')

    def box(x, y, w, h, text, color='#EBF5FB', edge='#2980B9', fontsize=9):
        rect = patches.FancyBboxPatch((x - w/2, y - h/2), w, h,
                                       boxstyle="round,pad=0.1",
                                       linewidth=1.2, edgecolor=edge, facecolor=color)
        ax.add_patch(rect)
        ax.text(x, y, text, ha='center', va='center', fontsize=fontsize, wrap=True)

    def diamond(x, y, w, h, text, color='#FEF9E7', edge='#F39C12', fontsize=8):
        diamond_pts = np.array([[x, y + h/2], [x + w/2, y], [x, y - h/2], [x - w/2, y]])
        poly = plt.Polygon(diamond_pts, closed=True, facecolor=color, edgecolor=edge, linewidth=1.2)
        ax.add_patch(poly)
        ax.text(x, y, text, ha='center', va='center', fontsize=fontsize)

    def arrow(x1, y1, x2, y2, text='', color='gray'):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color=color, lw=1.2))
        if text:
            mx, my = (x1+x2)/2, (y1+y2)/2
            ax.text(mx, my + 0.15, text, ha='center', va='center', fontsize=8, color=color)

    # Start
    box(5, 7.3, 3.0, 0.6, 'd电子数？', '#D5F5E3', '#27AE60', 10)

    # d1-d3, d8-d10
    arrow(5, 7.0, 2, 6.3)
    ax.text(3.0, 6.75, 'd1-d3\n或 d8-d10', ha='center', fontsize=7.5, color='gray')
    box(2, 5.9, 2.8, 0.6, '只有一种填充方式', '#D5F5E3', '#27AE60', 9)

    # d4-d7
    arrow(5, 7.0, 5, 6.3)
    ax.text(5.7, 6.75, 'd4-d7', ha='center', fontsize=7.5, color='gray')
    diamond(5, 5.6, 2.8, 1.0, '配体场强度？')

    # Weak field
    arrow(5, 5.1, 2.5, 4.2)
    ax.text(3.3, 4.7, '弱场配体', ha='center', fontsize=8, color='#E67E22')
    ax.text(3.3, 4.5, 'F⁻, H₂O, OH⁻', ha='center', fontsize=7, color='gray')
    box(2.5, 3.7, 2.6, 0.6, '高自旋（Hund规则）', '#FDEDEC', '#E74C3C', 9)
    box(2.5, 2.8, 2.6, 0.6, '先各填1个↑\n再配对', '#FDEDEC', '#E74C3C', 8)

    # Strong field
    arrow(5, 5.1, 7.5, 4.2)
    ax.text(6.7, 4.7, '强场配体', ha='center', fontsize=8, color='#2980B9')
    ax.text(6.7, 4.5, 'CN⁻, CO, NO₂⁻', ha='center', fontsize=7, color='gray')
    box(7.5, 3.7, 2.6, 0.6, '低自旋（先填满t₂g）', '#EBF5FB', '#2980B9', 9)
    box(7.5, 2.8, 2.6, 0.6, 'Δₒ > P → t₂g填满\n再填eₘ', '#EBF5FB', '#2980B9', 8)

    # Bottom note
    ax.text(5, 1.5, '关键：d1-d3和d8-d10不存在高低自旋问题，\n只有d4-d7需要判断配体场强度',
            ha='center', fontsize=8, color='#7F8C8D', style='italic')

    plt.tight_layout()
    path = save_path or os.path.join(MEDIA, 'flowchart-high-low-spin.png')
    fig.savefig(path, dpi=250, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    return path


def lattice_type_decision(save_path=None):
    """Lattice type judgment flowchart."""
    fig, ax = plt.subplots(1, 1, figsize=(6, 4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis('off')

    def box(x, y, w, h, text, color='#EBF5FB', edge='#2980B9', fontsize=9):
        rect = patches.FancyBboxPatch((x - w/2, y - h/2), w, h,
                                       boxstyle="round,pad=0.1",
                                       linewidth=1.2, edgecolor=edge, facecolor=color)
        ax.add_patch(rect)
        ax.text(x, y, text, ha='center', va='center', fontsize=fontsize)

    def diamond(x, y, w, h, text, color='#FEF9E7', edge='#F39C12', fontsize=8):
        diamond_pts = np.array([[x, y + h/2], [x + w/2, y], [x, y - h/2], [x - w/2, y]])
        poly = plt.Polygon(diamond_pts, closed=True, facecolor=color, edgecolor=edge, linewidth=1.2)
        ax.add_patch(poly)
        ax.text(x, y, text, ha='center', va='center', fontsize=fontsize)

    def arrow(x1, y1, x2, y2, text='', color='gray'):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color=color, lw=1.2))
        if text:
            mx, my = (x1+x2)/2, (y1+y2)/2
            ax.text(mx + 0.1, my, text, ha='left', va='center', fontsize=7.5, color=color)

    # Start
    box(5, 6.3, 4.0, 0.6, '体心/面心原子是否与顶点相同？', '#D5F5E3', '#27AE60', 9)

    # Yes branch
    arrow(5, 6.0, 3, 5.2)
    ax.text(3.5, 5.7, '是', ha='center', fontsize=8, color='#27AE60', fontweight='bold')

    diamond(3, 4.7, 2.5, 0.9, '体心 or 面心？')

    # Body center → same → BCC
    arrow(3, 4.25, 1.5, 3.4)
    ax.text(1.8, 3.9, '体心', ha='center', fontsize=7.5, color='gray')
    box(1.5, 2.9, 2.2, 0.6, 'BCC\n(体心立方)', '#D5F5E3', '#27AE60', 9)

    # Face center → same → FCC
    arrow(3, 4.25, 5, 3.4)
    ax.text(3.8, 3.9, '面心', ha='center', fontsize=7.5, color='gray')
    box(5, 2.9, 2.2, 0.6, 'FCC\n(面心立方)', '#D5F5E3', '#27AE60', 9)

    # No branch
    arrow(5, 6.0, 7.5, 5.2)
    ax.text(6.2, 5.7, '否', ha='center', fontsize=8, color='#E74C3C', fontweight='bold')

    box(7.5, 4.7, 2.5, 0.8, '基元含多种原子\n→ SC型（简单立方基底）', '#EBF5FB', '#2980B9', 8)
    box(7.5, 3.4, 2.5, 0.6, '按实际位置判断\n体心/面心/顶点', '#FDEDEC', '#E74C3C', 8)

    plt.tight_layout()
    path = save_path or os.path.join(MEDIA, 'flowchart-lattice-type.png')
    fig.savefig(path, dpi=250, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    return path


def distance_formula_decision(save_path=None):
    """Distance formula selection flowchart."""
    fig, ax = plt.subplots(1, 1, figsize=(6, 3.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')

    def box(x, y, w, h, text, color='#EBF5FB', edge='#2980B9', fontsize=8.5):
        rect = patches.FancyBboxPatch((x - w/2, y - h/2), w, h,
                                       boxstyle="round,pad=0.1",
                                       linewidth=1.2, edgecolor=edge, facecolor=color)
        ax.add_patch(rect)
        ax.text(x, y, text, ha='center', va='center', fontsize=fontsize)

    def diamond(x, y, w, h, text, color='#FEF9E7', edge='#F39C12', fontsize=7.5):
        diamond_pts = np.array([[x, y + h/2], [x + w/2, y], [x, y - h/2], [x - w/2, y]])
        poly = plt.Polygon(diamond_pts, closed=True, facecolor=color, edgecolor=edge, linewidth=1.2)
        ax.add_patch(poly)
        ax.text(x, y, text, ha='center', va='center', fontsize=fontsize)

    def arrow(x1, y1, x2, y2, text='', color='gray'):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color=color, lw=1.2))
        if text:
            mx, my = (x1+x2)/2, (y1+y2)/2
            ax.text(mx, my + 0.12, text, ha='center', fontsize=7, color=color)

    # Start
    box(5, 5.3, 3.0, 0.5, '晶胞参数 a, b, c, α, β, γ?', '#D5F5E3', '#27AE60', 9)

    # Cubic
    arrow(5, 5.05, 2, 4.3)
    ax.text(3.0, 4.8, 'a=b=c\nα=β=γ=90°', ha='center', fontsize=7, color='gray')
    box(2, 3.8, 2.4, 0.6, '立方\n$d=\\sqrt{(Δx)^2 a^2}$', '#EBF5FB', '#2980B9', 8)

    # Tetragonal
    arrow(5, 5.05, 5, 4.3)
    ax.text(5.5, 4.8, 'a=b≠c\nα=β=γ=90°', ha='center', fontsize=7, color='gray')
    box(5, 3.8, 2.4, 0.6, '四方\n$d=\\sqrt{(Δx)^2 a^2+(Δz)^2 c^2}$', '#EBF5FB', '#2980B9', 7.5)

    # Hexagonal
    arrow(5, 5.05, 8.2, 4.3)
    ax.text(7.0, 4.8, 'γ=120°\na=b≠c', ha='center', fontsize=7, color='gray')
    box(8.2, 3.8, 2.4, 0.8, '六方\n$d=\\sqrt{(Δx)^2 a^2+(Δy)^2 a^2+2ΔxΔy a^2\\cosγ}$', '#FEF9E7', '#F39C12', 7)

    # Bottom
    ax.text(5, 2.3, '核心：看γ是否=120° → 有无交叉项 2ΔxΔya²cosγ',
            ha='center', fontsize=8, color='#7F8C8D', style='italic')

    plt.tight_layout()
    path = save_path or os.path.join(MEDIA, 'flowchart-distance-formula.png')
    fig.savefig(path, dpi=250, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    return path


def gauche_effect_decision(save_path=None):
    """Gauche effect decision flowchart."""
    fig, ax = plt.subplots(1, 1, figsize=(5.5, 4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis('off')

    def box(x, y, w, h, text, color='#EBF5FB', edge='#2980B9', fontsize=8.5):
        rect = patches.FancyBboxPatch((x - w/2, y - h/2), w, h,
                                       boxstyle="round,pad=0.1",
                                       linewidth=1.2, edgecolor=edge, facecolor=color)
        ax.add_patch(rect)
        ax.text(x, y, text, ha='center', va='center', fontsize=fontsize)

    def diamond(x, y, w, h, text, color='#FEF9E7', edge='#F39C12', fontsize=7.5):
        diamond_pts = np.array([[x, y + h/2], [x + w/2, y], [x, y - h/2], [x - w/2, y]])
        poly = plt.Polygon(diamond_pts, closed=True, facecolor=color, edgecolor=edge, linewidth=1.2)
        ax.add_patch(poly)
        ax.text(x, y, text, ha='center', va='center', fontsize=fontsize)

    def arrow(x1, y1, x2, y2, text='', color='gray'):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color=color, lw=1.2))
        if text:
            mx, my = (x1+x2)/2, (y1+y2)/2
            ax.text(mx + 0.1, my, text, ha='left', fontsize=7.5, color=color, fontweight='bold')

    # Step 1
    box(5, 6.3, 3.5, 0.6, '分子中是否有 C—F 键？', '#D5F5E3', '#27AE60', 9)
    arrow(5, 6.0, 5, 5.2, '是')

    # Step 2
    diamond(5, 4.7, 3.2, 0.9, '相邻碳上是否有 C—H 键？')
    arrow(5, 4.25, 5, 3.3, '是')

    # Step 3
    diamond(5, 2.8, 3.8, 0.9, 'gauche构象能否σ→σ*重叠？')

    # Yes
    arrow(5, 2.35, 2.5, 1.5, '能')
    box(2.5, 1.0, 2.5, 0.7, 'gauche更稳定\n(σC-H → σ*C-F 超共轭)', '#D5F5E3', '#27AE60', 8)

    # No
    arrow(5, 2.35, 7.5, 1.5, '不能')
    box(7.5, 1.0, 2.5, 0.7, 'anti更稳定\n(位阻主导)', '#FDEDEC', '#E74C3C', 8)

    # No branches
    arrow(5, 6.0, 7.5, 5.2)
    ax.text(6.2, 5.7, '否', fontsize=7.5, color='#E74C3C', fontweight='bold')
    box(7.5, 4.9, 1.8, 0.5, '无gauche效应\n（普通构象）', '#FDEDEC', '#E74C3C', 7.5)

    arrow(5, 4.25, 7.5, 3.3)
    ax.text(6.5, 3.9, '否', fontsize=7.5, color='#E74C3C', fontweight='bold')
    box(7.5, 3.0, 1.8, 0.5, '无额外\n超共轭', '#FDEDEC', '#E74C3C', 7.5)

    plt.tight_layout()
    path = save_path or os.path.join(MEDIA, 'flowchart-gauche-effect.png')
    fig.savefig(path, dpi=250, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    return path


if __name__ == '__main__':
    print("Generating images...")
    p1 = generic_octahedral_splitting()
    print(f"  1. {os.path.basename(p1)}")
    p2 = octahedral_d6_lowspin()
    print(f"  2. {os.path.basename(p2)}")
    p3 = octahedral_d5_lowspin()
    print(f"  3. {os.path.basename(p3)}")
    p4 = octahedral_d7_highspin()
    print(f"  4. {os.path.basename(p4)}")
    p5 = high_low_spin_decision()
    print(f"  5. {os.path.basename(p5)}")
    p6 = lattice_type_decision()
    print(f"  6. {os.path.basename(p6)}")
    p7 = distance_formula_decision()
    print(f"  7. {os.path.basename(p7)}")
    p8 = gauche_effect_decision()
    print(f"  8. {os.path.basename(p8)}")
    print("Done!")
