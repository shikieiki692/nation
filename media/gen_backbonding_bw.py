"""
Generate a black-and-white schematic of CO's σ-donation and π-backbonding
to a metal center (synergic bonding diagram).

Output: media/sigma-pi-backbonding-synergy.png
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch, Ellipse, Circle
from matplotlib.path import Path
import matplotlib.patches as mpatches
import numpy as np


def teardrop_path(cx, cy, length=0.9, width=0.55):
    """Create a teardrop-shaped Path pointing to the right."""
    r = width / 2
    tip_x = cx + length / 2
    body_center_x = cx - length / 2 + r

    n = 30
    theta = np.linspace(np.pi / 2, -np.pi / 2, n)
    x_sc = body_center_x + r * np.cos(theta)
    y_sc = cy + r * np.sin(theta)

    n_curve = 10
    t = np.linspace(0, 1, n_curve)

    x_upper = tip_x + (x_sc[0] - tip_x) * t
    y_upper = cy + (y_sc[0] - cy) * np.sqrt(t)

    x_lower = x_sc[-1] + (tip_x - x_sc[-1]) * t
    y_lower = y_sc[-1] + (cy - y_sc[-1]) * np.sqrt(t)

    verts = list(zip(x_upper, y_upper))
    verts.extend(list(zip(x_sc[1:-1], y_sc[1:-1])))
    verts.extend(list(zip(x_lower, y_lower)))
    verts.append((tip_x, cy))

    codes = [Path.MOVETO] + [Path.LINETO] * (len(verts) - 2) + [Path.CLOSEPOLY]
    return Path(verts, codes)


def main():
    fig, ax = plt.subplots(1, 1, figsize=(10, 5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(-2.5, 2.5)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor('white')

    O_x, O_y = 1.0, 0.0
    C_x, C_y = 3.0, 0.0
    M_x, M_y = 7.5, 0.0

    # ── CO Triple Bond (3 parallel lines) ──
    for dy in [-0.1, 0, 0.1]:
        ax.plot([O_x + 0.35, C_x - 0.35], [dy, dy], 'k-', linewidth=2.5, solid_capstyle='round')

    ax.text(O_x, O_y - 0.5, 'O', fontsize=20, fontweight='bold', ha='center', va='top',
            fontfamily='serif', color='black')
    ax.text(C_x, C_y - 0.5, 'C', fontsize=20, fontweight='bold', ha='center', va='top',
            fontfamily='serif', color='black')

    # ── 3σ HOMO (filled teardrop on C pointing toward M) ──
    td_path = teardrop_path(C_x + 0.6, C_y, length=0.9, width=0.55)
    td_patch = mpatches.PathPatch(td_path, facecolor='black', edgecolor='black', linewidth=2.5)
    ax.add_patch(td_patch)
    ax.text(C_x + 1.5, C_y + 0.55, '3σ (HOMO, filled)', fontsize=9.5, ha='center', va='bottom',
            fontweight='bold', color='black')

    # ── π* LUMO (empty lobes above/below C-O axis, dashed outline) ──
    for sign in [1, -1]:
        lobe = Ellipse((C_x - 0.15, sign * 0.9), width=0.5, height=0.7,
                        facecolor='white', edgecolor='black', linewidth=2, linestyle='--')
        ax.add_patch(lobe)
    ax.text(C_x - 0.15, 1.55, 'π* (LUMO, empty)', fontsize=9.5, ha='center', va='bottom',
            fontstyle='italic', color='black')

    # ── Metal Center (gray circle labeled M) ──
    m_circle = Circle((M_x, M_y), 0.45, facecolor='#C0C0C0', edgecolor='black', linewidth=2.5)
    ax.add_patch(m_circle)
    ax.text(M_x, M_y, 'M', fontsize=22, fontweight='bold', ha='center', va='center',
            fontfamily='serif', color='black')

    # ── dσ* (empty, lobe along axis pointing toward CO) ──
    dsigma = Ellipse((M_x - 0.85, M_y), width=0.6, height=0.45,
                      facecolor='white', edgecolor='black', linewidth=2, linestyle='--')
    ax.add_patch(dsigma)
    ax.text(M_x - 1.55, M_y - 0.5, 'dσ* (empty)', fontsize=9.5, ha='center', va='top',
            fontstyle='italic', color='black')

    # ── dπ (filled, lobes above/below pointing toward CO π*) ──
    for sign in [1, -1]:
        dpi_lobe = Ellipse((M_x - 0.6, sign * 0.85), width=0.5, height=0.5,
                            facecolor='black', edgecolor='black', linewidth=2)
        ax.add_patch(dpi_lobe)
    ax.text(M_x - 0.6, 1.55, 'dπ (filled)', fontsize=9.5, ha='center', va='bottom',
            fontweight='bold', color='black')

    # ── Arrow 1: σ donation (straight, below axis) ──
    ax.annotate('', xy=(M_x - 1.2, -0.35), xytext=(C_x + 1.3, -0.35),
                arrowprops=dict(arrowstyle='->', color='black', lw=2.5, mutation_scale=18))
    ax.text((C_x + M_x) / 2, -0.8, 'σ donation', fontsize=11, ha='center', va='top',
            fontstyle='italic', fontweight='bold', color='black')

    # ── Arrow 2: π backdonation (curved, above axis) ──
    arrow2 = FancyArrowPatch(
        (M_x - 0.85, 0.9), (C_x + 0.1, 1.0),
        connectionstyle='arc3,rad=-0.3',
        arrowstyle='->', color='black', lw=2.5, mutation_scale=18
    )
    ax.add_patch(arrow2)
    ax.text((C_x + M_x) / 2, 1.85, 'π backdonation', fontsize=11, ha='center', va='bottom',
            fontstyle='italic', fontweight='bold', color='black')

    # ── Title Banner ──
    ax.text(4.25, 2.2, 'Synergic Bonding: M ← CO', fontsize=15, fontweight='bold',
            ha='center', va='center', fontfamily='serif', color='black',
            bbox=dict(boxstyle='round,pad=0.35', facecolor='white', edgecolor='black', linewidth=1.5))

    # ── Legend Box ──
    lx, ly = 8.0, -2.2
    lw, lh = 1.8, 1.4

    legend_box = patches.FancyBboxPatch((lx, ly), lw, lh,
                                         boxstyle='round,pad=0.15',
                                         facecolor='white', edgecolor='black', linewidth=1.5)
    ax.add_patch(legend_box)

    ax.text(lx + lw / 2, ly + lh - 0.12, 'Legend', fontsize=8, ha='center', va='top',
            fontweight='bold', color='black')

    ax.add_patch(Ellipse((lx + 0.25, ly + 0.95), 0.2, 0.15,
                          facecolor='black', edgecolor='black', linewidth=1))
    ax.text(lx + 0.45, ly + 0.95, 'filled orbital', fontsize=7.5, va='center', color='black')

    ax.add_patch(Ellipse((lx + 0.25, ly + 0.65), 0.2, 0.15,
                          facecolor='white', edgecolor='black', linewidth=1, linestyle='--'))
    ax.text(lx + 0.45, ly + 0.65, 'empty orbital', fontsize=7.5, va='center', color='black')

    ax.annotate('', xy=(lx + 0.4, ly + 0.3), xytext=(lx + 0.1, ly + 0.3),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.5))
    ax.text(lx + 0.5, ly + 0.3, 'electron flow', fontsize=7.5, va='center', color='black')

    plt.tight_layout()
    plt.savefig(r'C:\Obsidion\妙妙屋\media\sigma-pi-backbonding-synergy.png',
                dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print("Image saved: media/sigma-pi-backbonding-synergy.png")


if __name__ == '__main__':
    main()
