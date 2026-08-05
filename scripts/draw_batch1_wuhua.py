import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import hashlib
import os
import shutil

media_dir = r"C:\Obsidion\妙妙屋\媒体仓库"
os.makedirs(media_dir, exist_ok=True)

# Set font for Chinese
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

def save_and_hash(fig, name):
    tmp_path = f"tmp_{name}.png"
    fig.savefig(tmp_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    
    with open(tmp_path, "rb") as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()
        
    final_path = os.path.join(media_dir, f"{file_hash}.png")
    shutil.move(tmp_path, final_path)
    print(f"Generated {name}: {file_hash}.png")
    return file_hash

def draw_fig1_bridge():
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('off')
    
    # Draw central hub
    circle = patches.Circle((0.5, 0.5), 0.15, facecolor='#e6f2ff', edgecolor='#0066cc', lw=2)
    ax.add_patch(circle)
    ax.text(0.5, 0.5, "拿到题先找\n最短转接头\n(ΔG° / K / k-Ea)", ha='center', va='center', fontsize=12, fontweight='bold', color='#003366')
    
    # 5 weapons
    weapons = [
        ("热化学", 0.5, 0.85),
        ("平衡", 0.85, 0.5),
        ("电化学", 0.75, 0.15),
        ("动力学", 0.25, 0.15),
        ("路径设计", 0.15, 0.5)
    ]
    
    for label, x, y in weapons:
        box = patches.FancyBboxPatch((x-0.1, y-0.05), 0.2, 0.1, boxstyle="round,pad=0.02", 
                                     facecolor='#fff0f0', edgecolor='#cc0000', lw=1.5)
        ax.add_patch(box)
        ax.text(x, y, label, ha='center', va='center', fontsize=12, fontweight='bold')
        
        # Draw arrow to center
        ax.annotate("", xy=(0.5, 0.5), xytext=(x, y),
                    arrowprops=dict(arrowstyle="<->", color="gray", shrinkA=25, shrinkB=45, lw=1.5))
        
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    return save_and_hash(fig, "fig1_bridge")

def draw_fig2_born_haber():
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.axis('off')
    
    levels = [
        (0.1, 0.3, 0, "Li(s) + 1/2 F₂(g)"),
        (0.2, 0.4, 2, "Li(g) + 1/2 F₂(g)"),
        (0.3, 0.5, 4, "Li(g) + F(g)"),
        (0.4, 0.6, 6, "Li⁺(g) + e⁻ + F(g)"),
        (0.6, 0.8, 2, "Li⁺(g) + F⁻(g)"),
        (0.7, 0.9, -2, "LiF(s)")
    ]
    
    for i, (x1, x2, y, label) in enumerate(levels):
        ax.hlines(y, x1, x2, colors='black', lw=2)
        ax.text(x2 + 0.02, y, label, va='center', fontsize=12)
        
        if i > 0:
            prev_x1, prev_x2, prev_y, _ = levels[i-1]
            x_mid = (x1 + prev_x2) / 2
            
            # Draw arrow
            color = 'red' if y > prev_y else 'blue'
            ax.annotate("", xy=(x1+0.05, y), xytext=(prev_x2-0.05, prev_y),
                        arrowprops=dict(arrowstyle="->", color=color, lw=1.5))
            
    # Lattice energy
    ax.annotate("", xy=(levels[-1][0]+0.05, levels[-1][2]), xytext=(levels[-2][0]+0.05, levels[-2][2]),
                arrowprops=dict(arrowstyle="->", color="blue", lw=2))
    ax.text(0.6, 0, "晶格能 U", color="blue", fontsize=12)
    
    ax.set_xlim(0, 1)
    ax.set_ylim(-3, 7)
    return save_and_hash(fig, "fig2_born_haber")

def draw_fig3_bde():
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.axis('off')
    
    nodes = {
        "X-H(sol)": (0.2, 0.8),
        "X·(sol) + H·(sol)": (0.8, 0.8),
        "X⁺(sol) + H⁻(sol)": (0.8, 0.2),
        "X⁻(sol) + H⁺(sol)": (0.2, 0.2)
    }
    
    for label, (x, y) in nodes.items():
        box = patches.FancyBboxPatch((x-0.15, y-0.08), 0.3, 0.16, boxstyle="round,pad=0.02", 
                                     facecolor='#f0f8ff', edgecolor='#0000cc', lw=1.5)
        ax.add_patch(box)
        ax.text(x, y, label, ha='center', va='center', fontsize=11)
        
    ax.annotate("BDE (均裂)", xy=(0.65, 0.8), xytext=(0.35, 0.8), arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.annotate("① ET (电子转移)", xy=(0.8, 0.65), xytext=(0.8, 0.35), arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.annotate("② PT (质子转移)", xy=(0.35, 0.2), xytext=(0.65, 0.2), arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.annotate("③ 溶剂化", xy=(0.2, 0.35), xytext=(0.2, 0.65), arrowprops=dict(arrowstyle="->", lw=1.5))
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    return save_and_hash(fig, "fig3_bde")

def draw_fig4_pourbaix():
    fig, ax = plt.subplots(figsize=(8, 6))
    
    x = np.linspace(0, 14, 100)
    a_line = -0.059 * x
    b_line = 1.23 - 0.059 * x
    
    ax.plot(x, a_line, 'k--', label='a (H+/H2)')
    ax.plot(x, b_line, 'k--', label='b (O2/H2O)')
    
    ax.axvline(2, ymin=0, ymax=0.6, color='b')
    ax.plot([0, 2], [0.77, 0.77], 'b-')
    
    ax.text(1, 1.0, "Fe³⁺", fontsize=14, color='red')
    ax.text(1, 0.3, "Fe²⁺", fontsize=14, color='red')
    ax.text(1, -0.6, "Fe", fontsize=14, color='red')
    ax.text(8, 0.8, "Fe₂O₃", fontsize=14, color='red')
    ax.text(8, 0.0, "Fe₃O₄", fontsize=14, color='red')
    
    ax.set_xlabel("pH")
    ax.set_ylabel("E / V")
    ax.set_title("Fe-H₂O Pourbaix 图")
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    return save_and_hash(fig, "fig4_pourbaix")

def draw_fig5_steady_state():
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.axis('off')
    
    ax.text(0.5, 0.9, "稳态近似决策树\n(k₋₁ vs k₂)", ha='center', va='center', fontsize=14, fontweight='bold',
            bbox=dict(facecolor='#ffffcc', edgecolor='black', boxstyle='round,pad=0.5'))
            
    # Branches
    nodes = [
        ("k₋₁ >> k₂\n(平衡假设/前平衡)", 0.2, 0.5),
        ("k₋₁ << k₂\n(RDS在前)", 0.5, 0.5),
        ("k₋₁ ≈ k₂\n(一般稳态)", 0.8, 0.5)
    ]
    
    results = [
        ("k_obs = (k₁/k₋₁)k₂", 0.2, 0.2),
        ("k_obs = k₁", 0.5, 0.2),
        ("k_obs = k₁k₂/(k₋₁+k₂)", 0.8, 0.2)
    ]
    
    for i in range(3):
        label, x, y = nodes[i]
        res, rx, ry = results[i]
        
        ax.text(x, y, label, ha='center', va='center', fontsize=11,
                bbox=dict(facecolor='#e6f2ff', edgecolor='#0066cc', boxstyle='round,pad=0.3'))
        ax.text(rx, ry, res, ha='center', va='center', fontsize=11, color='#cc0000',
                bbox=dict(facecolor='#fff0f0', edgecolor='#cc0000', boxstyle='round,pad=0.3'))
                
        ax.annotate("", xy=(x, y+0.1), xytext=(0.5, 0.8), arrowprops=dict(arrowstyle="->", lw=1.5))
        ax.annotate("", xy=(rx, ry+0.1), xytext=(x, y-0.1), arrowprops=dict(arrowstyle="->", lw=1.5))
        
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    return save_and_hash(fig, "fig5_steady_state")

def draw_fig6_bridge1():
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.axis('off')
    
    steps = [
        ("E°(Cr₂O₇²⁻/Cr³⁺)\n+\nE°(Fe³⁺/Fe²⁺)", 0.1, 0.5),
        ("E°cell = 0.559V", 0.35, 0.5),
        ("ΔG° = -323.7 kJ", 0.6, 0.5),
        ("K = 1.1×10⁵⁶\n→ ICE", 0.85, 0.5)
    ]
    
    for i, (label, x, y) in enumerate(steps):
        ax.text(x, y, label, ha='center', va='center', fontsize=11,
                bbox=dict(facecolor='#f0fff0', edgecolor='#00cc00', boxstyle='round,pad=0.5'))
        if i > 0:
            prev_x = steps[i-1][1]
            ax.annotate("", xy=(x-0.12, y), xytext=(prev_x+0.12, y), arrowprops=dict(arrowstyle="->", lw=2, color='green'))
            
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    return save_and_hash(fig, "fig6_bridge1")

def draw_fig7_layer_path():
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.axis('off')
    
    ax.text(0.5, 0.8, "Ag⁺ 基础电对 (Nernst)", ha='center', va='center', fontsize=13, fontweight='bold',
            bbox=dict(facecolor='#ffe6e6', edgecolor='red', boxstyle='round,pad=0.5'))
            
    ax.text(0.2, 0.4, "左: AgCl (Ksp)", ha='center', va='center', fontsize=12,
            bbox=dict(facecolor='#e6ffe6', edgecolor='green', boxstyle='round,pad=0.5'))
            
    ax.text(0.8, 0.4, "右: Ag(NH₃)₂⁺ (Kf)", ha='center', va='center', fontsize=12,
            bbox=dict(facecolor='#e6e6ff', edgecolor='blue', boxstyle='round,pad=0.5'))
            
    ax.annotate("沉淀平衡联立", xy=(0.4, 0.7), xytext=(0.2, 0.5), arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.annotate("配位平衡联立", xy=(0.6, 0.7), xytext=(0.8, 0.5), arrowprops=dict(arrowstyle="->", lw=1.5))
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    return save_and_hash(fig, "fig7_layer_path")

if __name__ == "__main__":
    h1 = draw_fig1_bridge()
    h2 = draw_fig2_born_haber()
    h3 = draw_fig3_bde()
    h4 = draw_fig4_pourbaix()
    h5 = draw_fig5_steady_state()
    h6 = draw_fig6_bridge1()
    h7 = draw_fig7_layer_path()
    
    print("\nHashes:")
    print(f"Fig1: {h1}")
    print(f"Fig2: {h2}")
    print(f"Fig3: {h3}")
    print(f"Fig4: {h4}")
    print(f"Fig5: {h5}")
    print(f"Fig6: {h6}")
    print(f"Fig7: {h7}")
