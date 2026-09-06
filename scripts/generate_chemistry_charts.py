#!/usr/bin/env python3
"""Generate 5 high-quality chemistry knowledge point charts."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 200

MEDIA_DIR = r'C:\Obsidion\妙妙屋\媒体仓库'


# ============================================================
# Chart 1: UV-Vis conjugation vs lambda max
# ============================================================
def chart1_uv_vis():
    n_bonds = [1, 2, 3, 4, 5, 11]
    lambdas = [171, 217, 258, 290, 334, 450]
    labels = ['乙烯', '1,3-丁二烯', '1,3,5-己三烯', '辛四烯', '癸五烯', r'$\beta$-胡萝卜素']

    fig, ax = plt.subplots(figsize=(9, 5.5))

    # Polyfit for trend line
    xfit = np.linspace(0.8, 11.2, 200)
    coeffs = np.polyfit(n_bonds, lambdas, 3)
    yfit = np.polyval(coeffs, xfit)

    ax.plot(n_bonds, lambdas, 'o', color='#2563EB', markersize=10, zorder=5,
            label='实验数据点', markeredgecolor='white', markeredgewidth=1.5)
    ax.plot(xfit, yfit, '--', color='#F59E0B', linewidth=2, alpha=0.85,
            label='多项式拟合趋势线')

    # Annotate each point
    offsets = [(-8, -22), (-12, 14), (-8, 14), (-12, -22), (8, 10), (12, -18)]
    for i, (x, y, lbl) in enumerate(zip(n_bonds, lambdas, labels)):
        ax.annotate(lbl, (x, y), textcoords='offset points', xytext=offsets[i],
                    fontsize=8.5, ha='center',
                    arrowprops=dict(arrowstyle='->', color='gray', lw=0.8))

    ax.set_xlabel('共轭双键数 (n)', fontsize=12, fontweight='bold')
    ax.set_ylabel(r'$\lambda_{max}$ (nm)', fontsize=12, fontweight='bold')
    ax.set_title('共轭双键数与最大吸收波长 (λmax)', fontsize=14, fontweight='bold', pad=12)
    ax.set_xticks(range(1, 12))
    ax.legend(loc='upper left', fontsize=10, framealpha=0.9)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 12)

    fig.tight_layout()
    fig.savefig(f'{MEDIA_DIR}/UV-Vis_conjugation_lambda.png', dpi=200, bbox_inches='tight')
    plt.close(fig)
    print("Chart 1 saved: UV-Vis_conjugation_lambda.png")


# ============================================================
# Chart 2: Phosphine cone angle vs electronic parameter
# ============================================================
def chart2_phosphine():
    ligands  = ['PPh$_3$', 'PCy$_3$', 'P($t$-Bu)$_3$', 'P($p$-Tol)$_3$',
                'P(OPh)$_3$', 'P(OMe)$_3$', 'BINAP', 'SPhos', 'XPhos']
    chi      = [2066, 2056, 2056, 2061, 2085, 2082, 2063, 2054, 2053]  # cm^-1
    cone     = [145, 170, 182, 145, 128, 107, 155, 194, 212]  # degrees
    # Color by application: catalytic (blue shades) vs stoichiometric (orange shades)
    apps     = ['cat', 'cat', 'cat', 'cat', 'stc', 'stc', 'cat', 'cat', 'cat']
    colors   = ['#2563EB' if a == 'cat' else '#EA580C' for a in apps]

    fig, ax = plt.subplots(figsize=(9, 5.5))

    for i, (x, y, c, lbl) in enumerate(zip(chi, cone, colors, ligands)):
        ax.scatter(x, y, c=c, s=140, zorder=5, edgecolors='white', linewidths=1.2)
        # smart label placement
        offset_x, offset_y = 6, 6
        if lbl == 'PPh$_3$':       offset_y = -14
        if lbl == 'P($p$-Tol)$_3$': offset_x = -30; offset_y = -14
        if lbl == 'BINAP':          offset_x = 6;   offset_y = 12
        if lbl == 'P(OPh)$_3$':     offset_x = 6;   offset_y = -10
        if lbl == 'P(OMe)$_3$':     offset_y = 12
        ax.annotate(lbl, (x, y), textcoords='offset points', xytext=(offset_x, offset_y),
                    fontsize=8, ha='left' if offset_x >= 0 else 'right')

    # "Large steric, electron-rich" region annotation
    ax.annotate('大位阻富电子\n(有利于氧化加成)',
                xy=(2055, 190), fontsize=9, ha='center',
                bbox=dict(boxstyle='round,pad=0.4', fc='#FEF3C7', ec='#F59E0B', alpha=0.9))
    ax.annotate('', xy=(2055, 175), xytext=(2055, 205),
                arrowprops=dict(arrowstyle='->', color='#F59E0B', lw=1.5))

    # Legend patches
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#2563EB', edgecolor='white', label='催化常用配体'),
        Patch(facecolor='#EA580C', edgecolor='white', label='化学计量常用配体'),
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=10, framealpha=0.9)

    ax.set_xlabel(r'Tolman 电子参数 $\chi$ (cm$^{-1}$)', fontsize=12, fontweight='bold')
    ax.set_ylabel(r'Tolman 锥角 $\theta$ ($^\circ$)', fontsize=12, fontweight='bold')
    ax.set_title('膦配体空间效应与电子效应 (Tolman参数)', fontsize=14, fontweight='bold', pad=12)
    ax.set_xlim(2045, 2092)
    ax.set_ylim(95, 225)
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(f'{MEDIA_DIR}/phosphine_cone_angle_electronic.png', dpi=200, bbox_inches='tight')
    plt.close(fig)
    print("Chart 2 saved: phosphine_cone_angle_electronic.png")


# ============================================================
# Chart 3: Ionization energy period 2
# ============================================================
def chart3_ionization_energy():
    elements = ['Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne']
    ie = [520, 899, 801, 1086, 1402, 1314, 1681, 2081]

    fig, ax = plt.subplots(figsize=(9, 5.5))

    ax.plot(range(8), ie, 'o-', color='#2563EB', markersize=9, linewidth=2.2,
            markeredgecolor='white', markeredgewidth=1.5, zorder=5)

    # Shaded regions for stability
    # Be dip: s^2 full stability
    ax.axvspan(-0.2, 1.2, alpha=0.12, color='#60A5FA', zorder=0)
    ax.text(0.5, 2150, 's2 全满稳定', fontsize=9, ha='center', color='#1D4ED8',
            bbox=dict(fc='white', ec='#60A5FA', alpha=0.8, boxstyle='round,pad=0.3'))

    # N dip: p^3 half-full stability
    ax.axvspan(3.8, 5.2, alpha=0.12, color='#34D399', zorder=0)
    ax.text(4.5, 2150, 'p3 半满稳定', fontsize=9, ha='center', color='#047857',
            bbox=dict(fc='white', ec='#34D399', alpha=0.8, boxstyle='round,pad=0.3'))

    # Red arrows for dips
    ax.annotate('Be-B 下降\n2s2全满->2p1\n移走一个较稳定电子',
                xy=(1, 801), xytext=(2.5, 650),
                fontsize=8, ha='center', color='#DC2626',
                arrowprops=dict(arrowstyle='->', color='#DC2626', lw=1.8),
                bbox=dict(fc='#FEF2F2', ec='#DC2626', alpha=0.9, boxstyle='round,pad=0.3'))

    ax.annotate('N-O 下降\n2p3半满->2p4\n电子-电子排斥增加',
                xy=(5, 1314), xytext=(6.3, 1550),
                fontsize=8, ha='center', color='#DC2626',
                arrowprops=dict(arrowstyle='->', color='#DC2626', lw=1.8),
                bbox=dict(fc='#FEF2F2', ec='#DC2626', alpha=0.9, boxstyle='round,pad=0.3'))

    ax.set_xticks(range(8))
    ax.set_xticklabels(elements, fontsize=11, fontweight='bold')
    ax.set_xlabel('元素', fontsize=12, fontweight='bold')
    ax.set_ylabel('第一电离能 (kJ/mol)', fontsize=12, fontweight='bold')
    ax.set_title('第二周期元素第一电离能 (折点标注)', fontsize=14, fontweight='bold', pad=12)
    ax.set_ylim(300, 2300)
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(f'{MEDIA_DIR}/ionization_energy_period2.png', dpi=200, bbox_inches='tight')
    plt.close(fig)
    print("Chart 3 saved: ionization_energy_period2.png")


# ============================================================
# Chart 4: Electronegativity trend
# ============================================================
def chart4_electronegativity():
    Z_all   = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    elem    = ['Li','Be','B','C','N','O','F','Ne','Na','Mg','Al','Si','P','S','Cl','Ar','K','Ca']
    chi     = [0.98, 1.57, 2.04, 2.55, 3.04, 3.44, 3.98, 0, 0.93, 1.31, 1.61, 1.90, 2.19, 2.58, 3.16, 0, 0.82, 1.00]
    noble   = [7, 15]  # indices of Ne, Ar

    # Separate noble gases for distinct plotting
    main_z  = [z for i, z in enumerate(Z_all) if i not in noble]
    main_c  = [chi[i] for i in range(len(Z_all)) if i not in noble]
    noble_z = [Z_all[i] for i in noble]
    noble_c = [chi[i] for i in noble]
    noble_e = [elem[i] for i in noble]

    fig, ax = plt.subplots(figsize=(10, 5.5))

    # Period 2 (Z=3-10, Li-F)
    p2_z = main_z[:7]
    p2_c = main_c[:7]
    ax.plot(p2_z, p2_c, 'o-', color='#2563EB', markersize=8, linewidth=2,
            label='第二周期', markeredgecolor='white', markeredgewidth=1.2)

    # Period 3 (Z=11-18, Na-Cl)
    p3_z = main_z[7:14]
    p3_c = main_c[7:14]
    ax.plot(p3_z, p3_c, 's-', color='#DC2626', markersize=8, linewidth=2,
            label='第三周期', markeredgecolor='white', markeredgewidth=1.2)

    # Period 4 (Z=19-20, K-Ca)
    p4_z = main_z[14:]
    p4_c = main_c[14:]
    ax.plot(p4_z, p4_c, '^-', color='#059669', markersize=8, linewidth=2,
            label='第四周期', markeredgecolor='white', markeredgewidth=1.2)

    # Noble gases as open markers
    ax.plot(noble_z, noble_c, 'D', color='#9CA3AF', markersize=8, markeredgecolor='#6B7280',
            markeredgewidth=1.2, label='稀有气体 (近似值)', zorder=5)

    # Horizontal line at chi=2.0
    ax.axhline(y=2.0, color='#F59E0B', linestyle='--', linewidth=1.5, alpha=0.8)
    ax.text(5, 2.06, '金属/非金属分界 (χ=2.0)', fontsize=9, color='#D97706',
            fontweight='bold', ha='left',
            bbox=dict(fc='#FFFBEB', ec='#F59E0B', alpha=0.9, boxstyle='round,pad=0.3'))

    # Element labels
    for z, e, c in zip(main_z, [elem[i] for i in range(len(Z_all)) if i not in noble], main_c):
        ax.annotate(e, (z, c), textcoords='offset points', xytext=(0, 10),
                    fontsize=7.5, ha='center', fontweight='bold')

    # Periodic shading
    ax.axvspan(2.5, 9.5, alpha=0.05, color='#2563EB', zorder=0)
    ax.axvspan(10.5, 17.5, alpha=0.05, color='#DC2626', zorder=0)

    ax.set_xlabel('原子序数 Z', fontsize=12, fontweight='bold')
    ax.set_ylabel('Pauling 电负性 χ', fontsize=12, fontweight='bold')
    ax.set_title('Pauling电负性随原子序数的周期性变化', fontsize=14, fontweight='bold', pad=12)
    ax.set_xticks(Z_all)
    ax.set_xlim(2, 21)
    ax.set_ylim(0, 4.5)
    ax.legend(loc='lower right', fontsize=10, framealpha=0.9)
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(f'{MEDIA_DIR}/electronegativity_trend.png', dpi=200, bbox_inches='tight')
    plt.close(fig)
    print("Chart 4 saved: electronegativity_trend.png")


# ============================================================
# Chart 5: Lanthanide contraction
# ============================================================
def chart5_lanthanide():
    elements = ['La','Ce','Pr','Nd','Pm','Sm','Eu','Gd','Tb','Dy','Ho','Er','Tm','Yb','Lu']
    Z = list(range(57, 72))
    r = [103.2, 101.0, 99.0, 98.3, 97.0, 95.8, 94.7, 93.8, 92.3, 91.2, 90.1, 89.0, 88.0, 86.8, 86.1]

    fig, ax = plt.subplots(figsize=(9, 5.5))

    ax.plot(Z, r, 'o-', color='#7C3AED', markersize=8, linewidth=2.2,
            markeredgecolor='white', markeredgewidth=1.2, label=r'Ln$^{3+}$ 离子半径')

    # Annotate La and Lu
    ax.annotate(f'La3+: {r[0]} pm', xy=(Z[0], r[0]), xytext=(Z[0]+1.5, r[0]+3),
                fontsize=9, ha='left', color='#4C1D95', fontweight='bold',
                arrowprops=dict(arrowstyle='->', color='#7C3AED', lw=1.2))
    ax.annotate(f'Lu3+: {r[-1]} pm', xy=(Z[-1], r[-1]), xytext=(Z[-1]-2, r[-1]-4),
                fontsize=9, ha='right', color='#4C1D95', fontweight='bold',
                arrowprops=dict(arrowstyle='->', color='#7C3AED', lw=1.2))

    # Total contraction annotation
    total = r[0] - r[-1]
    ax.annotate('', xy=(71.3, r[-1]+0.5), xytext=(71.3, r[0]-0.5),
                arrowprops=dict(arrowstyle='<->', color='#DC2626', lw=2))
    ax.text(72.1, (r[0]+r[-1])/2, f'Δ ≈ {total:.1f} pm\n(镧系收缩)',
            fontsize=10, color='#DC2626', fontweight='bold', va='center',
            bbox=dict(fc='#FEF2F2', ec='#DC2626', alpha=0.9, boxstyle='round,pad=0.3'))

    # Cause annotation
    ax.text(63.5, 96.5, '原因：4f 电子屏蔽效应差\n核电荷增加 > 有效核电荷\n → 半径递减',
            fontsize=8.5, ha='center', va='center', color='#1E40AF',
            bbox=dict(fc='#EFF6FF', ec='#3B82F6', alpha=0.9, boxstyle='round,pad=0.5'))

    # Trend arrow
    ax.annotate('', xy=(70, 87), xytext=(58, 102),
                arrowprops=dict(arrowstyle='->', color='#9CA3AF', lw=1.5, linestyle='dashed'))

    ax.set_xlabel('原子序数 Z', fontsize=12, fontweight='bold')
    ax.set_ylabel('Ln3+ 离子半径 (pm)', fontsize=12, fontweight='bold')
    ax.set_title('镧系收缩：Ln3+离子半径随原子序数递减', fontsize=14, fontweight='bold', pad=12)
    ax.set_xticks(Z)
    ax.set_xticklabels(elements, fontsize=9, rotation=45, ha='right')
    ax.set_xlim(56, 73)
    ax.set_ylim(84, 107)
    ax.legend(loc='upper right', fontsize=10, framealpha=0.9)
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(f'{MEDIA_DIR}/lanthanide_contraction.png', dpi=200, bbox_inches='tight')
    plt.close(fig)
    print("Chart 5 saved: lanthanide_contraction.png")


# ============================================================
# Main
# ============================================================
if __name__ == '__main__':
    chart1_uv_vis()
    chart2_phosphine()
    chart3_ionization_energy()
    chart4_electronegativity()
    chart5_lanthanide()
    print("\nAll 5 charts generated successfully!")
