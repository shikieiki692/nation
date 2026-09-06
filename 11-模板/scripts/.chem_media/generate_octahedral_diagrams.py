"""
Generate two B&W octahedral coordination diagrams:
1. 图41: 2D cross-section of octahedral void (radius ratio critical condition)
2. 图43: 3D octahedral coordination geometry
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

DPI = 200
OUT = r'C:\Obsidion\妙妙屋\media'


def fig_octahedral_radius_ratio():
    """
    图41: 正方形截面——4个负离子(r⁻)在正方形顶点，正离子(r⁺)在中心。
    展示半径比临界条件的几何关系。
    """
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect('equal')
    ax.axis('off')

    # Parameters
    r_minus = 1.0  # radius of negative ion
    r_plus = np.sqrt(2) - 1  # critical radius ratio: r+/r- ≈ 0.414
    side = 2 * r_minus  # side length of square = 2*r_-

    # Center of the square
    cx, cy = 0, 0

    # 4 negative ions at corners of square
    corners = [(-r_minus, -r_minus), (r_minus, -r_minus),
               (r_minus, r_minus), (-r_minus, r_minus)]

    # Draw square (dashed, showing the geometric frame)
    square = plt.Polygon(corners, fill=False, edgecolor='gray', linewidth=1.0,
                          linestyle='--', zorder=1)
    ax.add_patch(square)

    # Draw diagonal (showing the critical contact line)
    ax.plot([-r_minus, r_minus], [-r_minus, r_minus], 'k-', linewidth=0.8, zorder=2)
    ax.plot([-r_minus, r_minus], [r_minus, -r_minus], 'k-', linewidth=0.8, zorder=2)

    # Draw negative ions (large, gray fill)
    for (x, y) in corners:
        circle = plt.Circle((x, y), r_minus, facecolor='#d0d0d0', edgecolor='black',
                             linewidth=1.5, zorder=3)
        ax.add_patch(circle)

    # Draw positive ion (small, black fill)
    circle_plus = plt.Circle((cx, cy), r_plus, facecolor='black', edgecolor='black',
                              linewidth=1.5, zorder=4)
    ax.add_patch(circle_plus)

    # Label r⁻ (on the top-right negative ion)
    ax.annotate('', xy=(r_minus + r_minus * np.cos(np.radians(135)),
                         r_minus + r_minus * np.sin(np.radians(135))),
                xytext=(r_minus, r_minus),
                arrowprops=dict(arrowstyle='<->', lw=1.2, color='black'))
    ax.text(r_minus + 0.55, r_minus + 0.55, r'$r_-$', fontsize=14, ha='center',
            va='center', fontfamily='SimHei')

    # Label r⁺ (from center to edge of positive ion)
    ax.annotate('', xy=(r_plus, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle='<->', lw=1.2, color='black'))
    ax.text(r_plus / 2, -0.15, r'$r_+$', fontsize=14, ha='center', va='center',
            fontfamily='SimHei', color='white',
            bbox=dict(boxstyle='round,pad=0.05', facecolor='black', edgecolor='none'))

    # Label the side length (top edge)
    ax.annotate('', xy=(r_minus, r_minus + 0.3), xytext=(-r_minus, r_minus + 0.3),
                arrowprops=dict(arrowstyle='<->', lw=1.0, color='black'))
    ax.text(0, r_minus + 0.5, r'$2r_-$', fontsize=12, ha='center', va='center',
            fontfamily='SimHei')

    # Label the diagonal distance (along the diagonal)
    diag_dist = np.sqrt(2) * r_minus  # = r+ + r- at critical condition
    mid_x = r_minus / 2
    mid_y = r_minus / 2
    ax.text(mid_x + 0.15, mid_y + 0.35, r'$\sqrt{2}\,r_- = r_+ + r_-$',
            fontsize=11, ha='center', va='center', fontfamily='SimHei',
            rotation=45, color='#333333')

    # Title
    ax.set_title('八面体空隙截面（正方形）', fontsize=13, fontweight='bold',
                 fontfamily='SimHei', pad=10)

    # Critical condition box
    ax.text(0, -1.8, r'临界条件: $\sqrt{2}\,r_- = r_+ + r_-$', fontsize=11,
            ha='center', va='center', fontfamily='SimHei',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#f5f5f5', edgecolor='gray'))
    ax.text(0, -2.3, r'$\frac{r_+}{r_-} = \sqrt{2} - 1 \approx 0.414$',
            fontsize=13, ha='center', va='center', fontfamily='SimHei',
            fontweight='bold')

    ax.set_xlim(-1.8, 1.8)
    ax.set_ylim(-2.7, 1.8)

    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '图-八面体空隙截面-半径比临界条件.png'),
                dpi=DPI, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print("OK: 八面体空隙截面（图41）")


def fig_octahedral_coordination_3d():
    """
    图43: 立体八面体配位——6个负离子在八面体顶点，正离子在中心。
    """
    fig = plt.figure(figsize=(6, 5.5))
    ax = fig.add_subplot(111, projection='3d')

    # Octahedron vertices (6 negative ions)
    # Top, Bottom, and 4 in the equatorial plane
    vertices = np.array([
        [0, 0, 1.2],    # top
        [0, 0, -1.2],   # bottom
        [1.2, 0, 0],    # front
        [-1.2, 0, 0],   # back
        [0, 1.2, 0],    # right
        [0, -1.2, 0],   # left
    ])

    # Center (positive ion)
    center = np.array([0, 0, 0])

    # Draw octahedron edges
    edges = [
        (0, 2), (0, 3), (0, 4), (0, 5),  # top to equatorial
        (1, 2), (1, 3), (1, 4), (1, 5),  # bottom to equatorial
        (2, 4), (4, 3), (3, 5), (5, 2),  # equatorial ring
    ]

    for i, j in edges:
        ax.plot([vertices[i, 0], vertices[j, 0]],
                [vertices[i, 1], vertices[j, 1]],
                [vertices[i, 2], vertices[j, 2]],
                'k-', linewidth=1.2, alpha=0.6)

    # Draw coordination bonds (center to vertices)
    for v in vertices:
        ax.plot([0, v[0]], [0, v[1]], [0, v[2]],
                'k--', linewidth=0.8, alpha=0.4)

    # Draw negative ions (gray spheres)
    for v in vertices:
        ax.scatter(v[0], v[1], v[2], c='#999999', s=200, edgecolors='black',
                   linewidth=1.2, zorder=5)

    # Draw positive ion (black sphere, larger)
    ax.scatter(0, 0, 0, c='black', s=300, edgecolors='black',
               linewidth=1.2, zorder=6)

    # Labels
    ax.text(0, 0, 1.45, '负离子', fontsize=9, ha='center', fontfamily='SimHei',
            color='#555555')
    ax.text(0, 0, -1.55, '负离子', fontsize=9, ha='center', fontfamily='SimHei',
            color='#555555')
    ax.text(1.5, 0, 0, '负离子', fontsize=9, ha='center', fontfamily='SimHei',
            color='#555555')
    ax.text(-1.5, 0, 0, '负离子', fontsize=9, ha='center', fontfamily='SimHei',
            color='#555555')
    ax.text(0, 1.5, 0, '负离子', fontsize=9, ha='center', fontfamily='SimHei',
            color='#555555')
    ax.text(0, -1.5, 0, '负离子', fontsize=9, ha='center', fontfamily='SimHei',
            color='#555555')
    ax.text(0.3, -0.3, 0.3, '正离子', fontsize=9, ha='center', fontfamily='SimHei',
            color='black', fontweight='bold')

    # Configure axes
    ax.set_xlim([-1.8, 1.8])
    ax.set_ylim([-1.8, 1.8])
    ax.set_zlim([-1.8, 1.8])
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('w')
    ax.yaxis.pane.set_edgecolor('w')
    ax.zaxis.pane.set_edgecolor('w')
    ax.set_box_aspect([1, 1, 1])
    ax.view_init(elev=15, azim=-60)

    ax.set_title('八面体配位（配位数 = 6）', fontsize=13, fontweight='bold',
                 fontfamily='SimHei', pad=5)

    # Info box
    info_text = ("配位数: 6\n"
                 "正离子位于八面体中心\n"
                 "6个负离子在八面体顶点\n"
                 "NaCl中Na⁺的配位环境")
    ax.text2D(0.02, 0.02, info_text, fontsize=8, fontfamily='SimHei',
              transform=ax.transAxes, verticalalignment='bottom',
              bbox=dict(boxstyle='round,pad=0.3', facecolor='#f5f5f5',
                        edgecolor='gray', alpha=0.9))

    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '图-八面体配位立体图.png'),
                dpi=DPI, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print("OK: 八面体配位立体图（图43）")


if __name__ == '__main__':
    fig_octahedral_radius_ratio()
    fig_octahedral_coordination_3d()
    print("\nBoth octahedral diagrams generated!")
