"""
Generate CaC2 crystal structure diagram.
CaC2 has a tetragonal structure derived from NaCl.
Ca2+ at corners and face centers (like Na in NaCl).
C2^2- dumbbells at edge centers and body center (like Cl in NaCl),
but elongated along c-axis (tetragonal distortion).
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

DPI = 200
OUT = r'C:\Obsidion\妙妙屋\media'


def fig_cac2_structure():
    fig = plt.figure(figsize=(6, 5.5))
    ax = fig.add_subplot(111, projection='3d')

    # Tetragonal unit cell: a = b != c (c is elongated)
    a = 1.0
    c = 1.3  # elongated c-axis

    # Draw unit cell edges
    # Bottom face
    ax.plot([0,a,a,0,0], [0,0,a,a,0], [0,0,0,0,0], 'k-', lw=1.5)
    # Top face
    ax.plot([0,a,a,0,0], [0,0,a,a,0], [c,c,c,c,c], 'k-', lw=1.5)
    # Vertical edges
    for x, y in [(0,0), (a,0), (a,a), (0,a)]:
        ax.plot([x,x], [y,y], [0,c], 'k-', lw=1.5, alpha=0.4)

    # Ca2+ positions (like Na in NaCl): corners + face centers
    ca_positions = []
    # Corners
    for x in [0, a]:
        for y in [0, a]:
            for z in [0, c]:
                ca_positions.append([x, y, z])
    # Face centers (top/bottom)
    for x, y in [(a/2, a/2)]:
        ca_positions.append([x, y, 0])
        ca_positions.append([x, y, c])
    # Face centers (sides)
    for y in [0, a]:
        ca_positions.append([a/2, y, c/2])
    for x in [0, a]:
        ca_positions.append([x, a/2, c/2])

    ca_positions = np.array(ca_positions)

    # Draw Ca2+ ions (large gray spheres)
    for pos in ca_positions:
        ax.scatter(pos[0], pos[1], pos[2], c='#999999', s=150,
                   edgecolors='black', linewidth=1, zorder=5)

    # C2^2- positions (like Cl in NaCl): edge centers + body center
    # But C2^2- is a dumbbell along c-axis
    c2_positions = []
    # Edge centers (horizontal edges)
    for z in [0, c]:
        c2_positions.append([a/2, 0, z])
        c2_positions.append([a/2, a, z])
        c2_positions.append([0, a/2, z])
        c2_positions.append([a, a/2, z])
    # Body center
    c2_positions.append([a/2, a/2, c/2])

    c2_positions = np.array(c2_positions)

    # Draw C2^2- dumbbells (two small black dots connected by a line along c-axis)
    dumbbell_length = 0.15  # C-C bond length in fractional coords
    for pos in c2_positions:
        # Two C atoms forming the dumbbell
        c1 = [pos[0], pos[1], pos[2] - dumbbell_length * c]
        c2 = [pos[0], pos[1], pos[2] + dumbbell_length * c]
        ax.scatter(c1[0], c1[1], c1[2], c='black', s=60, edgecolors='black',
                   linewidth=0.8, zorder=6)
        ax.scatter(c2[0], c2[1], c2[2], c='black', s=60, edgecolors='black',
                   linewidth=0.8, zorder=6)
        # Bond line
        ax.plot([c1[0], c2[0]], [c1[1], c2[1]], [c1[2], c2[2]],
                'k-', linewidth=2, zorder=6)

    # Labels
    ax.text(a/2, -0.15, -0.1, 'Ca2+', fontsize=10, ha='center', fontfamily='SimHei',
            color='#666666')
    ax.text(a+0.15, a/2, c/2, 'C2^2-', fontsize=10, ha='center', fontfamily='SimHei',
            color='black')

    # Axis labels
    ax.text(a+0.1, 0, 0, 'a', fontsize=12, ha='center', fontfamily='SimHei')
    ax.text(0, a+0.1, 0, 'a', fontsize=12, ha='center', fontfamily='SimHei')
    ax.text(-0.05, -0.05, c+0.1, 'c', fontsize=12, ha='center', fontfamily='SimHei')

    ax.set_xlim([-0.2, a+0.3])
    ax.set_ylim([-0.2, a+0.3])
    ax.set_zlim([-0.2, c+0.2])
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('w')
    ax.yaxis.pane.set_edgecolor('w')
    ax.zaxis.pane.set_edgecolor('w')
    ax.set_box_aspect([1, 1, c/a])
    ax.view_init(elev=20, azim=-50)

    ax.set_title('CaC2 晶胞（体心四方）', fontsize=13, fontweight='bold',
                 fontfamily='SimHei', pad=5)

    # Info box
    info = ("Ca2+: 角顶+面心 (like Na in NaCl)\n"
            "C2^2-: 棱心+体心 (哑铃型, //c轴)\n"
            "点阵类型: 体心四方 (I)")
    ax.text2D(0.02, 0.02, info, fontsize=8, fontfamily='SimHei',
              transform=ax.transAxes, verticalalignment='bottom',
              bbox=dict(boxstyle='round,pad=0.3', facecolor='#f5f5f5',
                        edgecolor='gray', alpha=0.9))

    plt.tight_layout()
    plt.savefig(os.path.join(OUT, 'cac2-unit-cell.png'),
                dpi=DPI, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print("OK: CaC2 unit cell")


if __name__ == '__main__':
    fig_cac2_structure()
