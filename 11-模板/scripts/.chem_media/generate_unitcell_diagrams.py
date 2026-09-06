"""
Generate two diagrams:
1. 3D atom counting showing corner/edge/face/body contributions
2. Simple cubic unit cell (8 corner atoms only)
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

DPI = 200
OUT = r'C:\Obsidion\妙妙屋\media'


def fig_atom_counting_3d():
    """3D unit cell showing atoms at 4 different positions with contribution labels."""
    fig = plt.figure(figsize=(7, 6))
    ax = fig.add_subplot(111, projection='3d')

    a = 1.0

    # Draw unit cell edges
    for z in [0, a]:
        ax.plot([0,a,a,0,0], [0,0,a,a,0], [z,z,z,z,z], 'k-', lw=1.5)
    for x, y in [(0,0), (a,0), (a,a), (0,a)]:
        ax.plot([x,x], [y,y], [0,a], 'k-', lw=1.5, alpha=0.5)

    # Corner atoms (8 corners) - dark gray
    corners = [(x,y,z) for x in [0,a] for y in [0,a] for z in [0,a]]
    for pos in corners:
        ax.scatter(*pos, c='#555555', s=120, edgecolors='black', linewidth=0.8, zorder=5)

    # Edge atoms (12 edges) - medium gray
    edges = []
    for i in [0, a]:
        for j in [0, a]:
            edges.append((i, j, a/2))  # vertical edges
            edges.append((i, a/2, j))  # y-direction edges
            edges.append((a/2, i, j))  # x-direction edges
    # Remove duplicates
    edges = list(set(edges))
    for pos in edges:
        ax.scatter(*pos, c='#999999', s=100, edgecolors='black', linewidth=0.8, zorder=5)

    # Face atoms (6 faces) - light gray
    faces = [(a/2, a/2, 0), (a/2, a/2, a),
             (a/2, 0, a/2), (a/2, a, a/2),
             (0, a/2, a/2), (a, a/2, a/2)]
    for pos in faces:
        ax.scatter(*pos, c='#cccccc', s=100, edgecolors='black', linewidth=0.8, zorder=5)

    # Body atom (1) - white
    ax.scatter(a/2, a/2, a/2, c='white', s=150, edgecolors='black', linewidth=1.5, zorder=6)

    # Legend annotations
    ax.text(a+0.15, a+0.15, a+0.05, 'Corner: 1/8', fontsize=8, fontfamily='SimHei', color='#555555')
    ax.text(a+0.15, a+0.15, a/2, 'Edge: 1/4', fontsize=8, fontfamily='SimHei', color='#999999')
    ax.text(a+0.15, a+0.15, 0, 'Face: 1/2', fontsize=8, fontfamily='SimHei', color='#888888')
    ax.text(a+0.15, a/2, a/2, 'Body: 1', fontsize=8, fontfamily='SimHei', color='black')

    ax.set_xlim([-0.1, a+0.4])
    ax.set_ylim([-0.1, a+0.4])
    ax.set_zlim([-0.1, a+0.15])
    ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
    ax.xaxis.pane.fill = False; ax.yaxis.pane.fill = False; ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('w'); ax.yaxis.pane.set_edgecolor('w'); ax.zaxis.pane.set_edgecolor('w')
    ax.set_box_aspect([1,1,1])
    ax.view_init(elev=20, azim=-55)

    ax.set_title('晶胞原子计数', fontsize=14, fontweight='bold', fontfamily='SimHei', pad=5)

    # Formula box
    formula = ("8 corners x 1/8 = 1\n12 edges x 1/4 = 3\n6 faces x 1/2 = 3\n1 body x 1 = 1\nTotal = 8 atoms")
    ax.text2D(0.02, 0.02, formula, fontsize=9, fontfamily='SimHei',
              transform=ax.transAxes, verticalalignment='bottom',
              bbox=dict(boxstyle='round,pad=0.4', facecolor='#f5f5f5', edgecolor='gray'))

    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '图-晶胞原子计数3D.png'),
                dpi=DPI, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print("OK: 3D atom counting")


def fig_simple_cubic_unitcell():
    """Simple cubic unit cell - 8 corner atoms with unit cell wireframe."""
    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_subplot(111, projection='3d')

    a = 1.0

    # Unit cell edges (solid lines)
    for z in [0, a]:
        ax.plot([0,a,a,0,0], [0,0,a,a,0], [z,z,z,z,z], 'k-', lw=2)
    for x, y in [(0,0), (a,0), (a,a), (0,a)]:
        ax.plot([x,x], [y,y], [0,a], 'k-', lw=2, alpha=0.6)

    # 8 corner atoms
    corners = [(x,y,z) for x in [0,a] for y in [0,a] for z in [0,a]]
    for pos in corners:
        ax.scatter(*pos, c='#999999', s=250, edgecolors='black', linewidth=1.5, zorder=5)

    ax.set_xlim([-0.15, a+0.15])
    ax.set_ylim([-0.15, a+0.15])
    ax.set_zlim([-0.15, a+0.15])
    ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
    ax.xaxis.pane.fill = False; ax.yaxis.pane.fill = False; ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('w'); ax.yaxis.pane.set_edgecolor('w'); ax.zaxis.pane.set_edgecolor('w')
    ax.set_box_aspect([1,1,1])
    ax.view_init(elev=20, azim=-55)

    ax.set_title('简单立方晶胞 (P)', fontsize=13, fontweight='bold', fontfamily='SimHei', pad=5)
    ax.text2D(0.5, 0.05, '8 x 1/8 = 1 atom', fontsize=10, ha='center',
              fontfamily='SimHei', transform=ax.transAxes,
              bbox=dict(boxstyle='round,pad=0.2', facecolor='#f5f5f5', edgecolor='gray'))

    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '图-简单立方晶胞3D.png'),
                dpi=DPI, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print("OK: Simple cubic unit cell")


def fig_bcc_unitcell():
    """Body-centered cubic unit cell - 8 corner + 1 body center."""
    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_subplot(111, projection='3d')
    a = 1.0

    # Unit cell edges
    for z in [0, a]:
        ax.plot([0,a,a,0,0], [0,0,a,a,0], [z,z,z,z,z], 'k-', lw=2)
    for x, y in [(0,0), (a,0), (a,a), (0,a)]:
        ax.plot([x,x], [y,y], [0,a], 'k-', lw=2, alpha=0.6)

    # 8 corner atoms
    for x in [0,a]:
        for y in [0,a]:
            for z in [0,a]:
                ax.scatter(x, y, z, c='#999999', s=250, edgecolors='black', linewidth=1.5, zorder=5)

    # 1 body center atom
    ax.scatter(a/2, a/2, a/2, c='#666666', s=300, edgecolors='black', linewidth=1.5, zorder=6)

    ax.set_xlim([-0.15, a+0.15]); ax.set_ylim([-0.15, a+0.15]); ax.set_zlim([-0.15, a+0.15])
    ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
    ax.xaxis.pane.fill = False; ax.yaxis.pane.fill = False; ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('w'); ax.yaxis.pane.set_edgecolor('w'); ax.zaxis.pane.set_edgecolor('w')
    ax.set_box_aspect([1,1,1]); ax.view_init(elev=20, azim=-55)
    ax.set_title('体心立方晶胞 (I)', fontsize=13, fontweight='bold', fontfamily='SimHei', pad=5)
    ax.text2D(0.5, 0.05, '8 x 1/8 + 1 = 2 atoms', fontsize=10, ha='center',
              fontfamily='SimHei', transform=ax.transAxes,
              bbox=dict(boxstyle='round,pad=0.2', facecolor='#f5f5f5', edgecolor='gray'))
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '图-体心立方晶胞3D.png'), dpi=DPI, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("OK: BCC unit cell")


def fig_fcc_unitcell():
    """Face-centered cubic unit cell - 8 corner + 6 face center."""
    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_subplot(111, projection='3d')
    a = 1.0

    # Unit cell edges
    for z in [0, a]:
        ax.plot([0,a,a,0,0], [0,0,a,a,0], [z,z,z,z,z], 'k-', lw=2)
    for x, y in [(0,0), (a,0), (a,a), (0,a)]:
        ax.plot([x,x], [y,y], [0,a], 'k-', lw=2, alpha=0.6)

    # 8 corner atoms
    for x in [0,a]:
        for y in [0,a]:
            for z in [0,a]:
                ax.scatter(x, y, z, c='#999999', s=200, edgecolors='black', linewidth=1.2, zorder=5)

    # 6 face center atoms
    face_centers = [(a/2,a/2,0), (a/2,a/2,a), (a/2,0,a/2), (a/2,a,a/2), (0,a/2,a/2), (a,a/2,a/2)]
    for pos in face_centers:
        ax.scatter(*pos, c='#666666', s=250, edgecolors='black', linewidth=1.5, zorder=6)

    ax.set_xlim([-0.15, a+0.15]); ax.set_ylim([-0.15, a+0.15]); ax.set_zlim([-0.15, a+0.15])
    ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
    ax.xaxis.pane.fill = False; ax.yaxis.pane.fill = False; ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('w'); ax.yaxis.pane.set_edgecolor('w'); ax.zaxis.pane.set_edgecolor('w')
    ax.set_box_aspect([1,1,1]); ax.view_init(elev=20, azim=-55)
    ax.set_title('面心立方晶胞 (F)', fontsize=13, fontweight='bold', fontfamily='SimHei', pad=5)
    ax.text2D(0.5, 0.05, '8 x 1/8 + 6 x 1/2 = 4 atoms', fontsize=10, ha='center',
              fontfamily='SimHei', transform=ax.transAxes,
              bbox=dict(boxstyle='round,pad=0.2', facecolor='#f5f5f5', edgecolor='gray'))
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '图-面心立方晶胞3D.png'), dpi=DPI, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("OK: FCC unit cell")


if __name__ == '__main__':
    fig_atom_counting_3d()
    fig_simple_cubic_unitcell()
    fig_bcc_unitcell()
    fig_fcc_unitcell()
