import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import hashlib
import os
import shutil
import re

media_dir = r"C:\Obsidion\妙妙屋\媒体仓库"

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
    return file_hash

def draw_fig1_maxwell():
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.axis('off')
    
    # Born square (Thermodynamic square)
    # Corners: H, G, U, A
    corners = {
        "H": (0.8, 0.8),
        "G": (0.8, 0.2),
        "A": (0.2, 0.2),
        "U": (0.2, 0.8)
    }
    
    # Variables: S, P, V, T
    vars = {
        "S": (0.5, 0.9, "S"),
        "P": (0.9, 0.5, "P"),
        "T": (0.5, 0.1, "T"),
        "V": (0.1, 0.5, "V")
    }
    
    for label, (x, y) in corners.items():
        ax.text(x, y, label, ha='center', va='center', fontsize=20, fontweight='bold', color='blue',
                bbox=dict(facecolor='white', edgecolor='blue', boxstyle='circle'))
                
    for _, (x, y, label) in vars.items():
        ax.text(x, y, label, ha='center', va='center', fontsize=16, color='red')
        
    ax.annotate("", xy=(0.75, 0.25), xytext=(0.25, 0.75), arrowprops=dict(arrowstyle="->", lw=2))
    ax.annotate("", xy=(0.75, 0.75), xytext=(0.25, 0.25), arrowprops=dict(arrowstyle="->", lw=2))
    
    ax.text(0.5, 0.5, "Good Physicists\nHave Studied\nUnder Very\nActive Teachers", 
            ha='center', va='center', fontsize=10, color='gray')
            
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    return save_and_hash(fig, "fig1_maxwell")

def draw_fig2_partition():
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.axis('off')
    
    ax.text(0.5, 0.8, "分子配分函数 q", ha='center', va='center', fontsize=14, fontweight='bold',
            bbox=dict(facecolor='#f0f8ff', edgecolor='blue', boxstyle='round,pad=0.5'))
            
    branches = [
        ("平动 q_t\n(依赖 m, T, V)", 0.2, 0.4),
        ("转动 q_r\n(依赖 I, T, σ)", 0.4, 0.4),
        ("振动 q_v\n(依赖 ν̃, T)", 0.6, 0.4),
        ("电子 q_e\n(依赖 激发态, T)", 0.8, 0.4)
    ]
    
    for label, x, y in branches:
        ax.text(x, y, label, ha='center', va='center', fontsize=11,
                bbox=dict(facecolor='#fff0f0', edgecolor='red', boxstyle='round,pad=0.5'))
        ax.annotate("", xy=(x, y+0.1), xytext=(0.5, 0.75), arrowprops=dict(arrowstyle="->", lw=1.5, color='gray'))
        
    ax.text(0.5, 0.1, "q = q_t × q_r × q_v × q_e", ha='center', va='center', fontsize=14, color='darkgreen',
            bbox=dict(facecolor='#e6ffe6', edgecolor='green', boxstyle='round,pad=0.5'))
            
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    return save_and_hash(fig, "fig2_partition")

def draw_fig3_sackur():
    fig, ax = plt.subplots(figsize=(8, 4))
    
    T = np.linspace(100, 1000, 100)
    V1 = 1
    V2 = 10
    
    # Sackur-Tetrode proportional to 3/2 lnT + lnV
    S1 = 1.5 * np.log(T) + np.log(V1)
    S2 = 1.5 * np.log(T) + np.log(V2)
    
    ax.plot(T, S1, 'b-', lw=2, label='V = V1')
    ax.plot(T, S2, 'r-', lw=2, label='V = V2 (V2 > V1)')
    
    ax.set_xlabel("温度 T (K)")
    ax.set_ylabel("平动熵 S_t")
    ax.set_title("Sackur-Tetrode 方程：平动熵随 T 和 V 的变化")
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    return save_and_hash(fig, "fig3_sackur")

if __name__ == "__main__":
    h1 = draw_fig1_maxwell()
    h2 = draw_fig2_partition()
    h3 = draw_fig3_sackur()
    
    hashes = [h1, h2, h3]
    captions = [
        "*图 1 热力学四边形 (Born Square) 与 Maxwell 关系转换*",
        "*图 2 分子配分函数 q 的分解与依赖变量关系图*",
        "*图 3 Sackur-Tetrode 方程：平动熵随 T 和 V 变化关系*"
    ]
    
    filepath = r"C:\Obsidion\妙妙屋\04-课件\学生讲义\统计热力学与Maxwell关系-超级充实版（自学完整）.md"
    
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    text = re.sub(r'has_images:\s*false', 'has_images: true', text)
    text = re.sub(r'image_count:\s*0', 'image_count: 3', text)

    for i in range(1, 4):
        placeholder_pattern = re.compile(r'📌\s*\*\*图片待补（图\s*' + str(i) + r'）\*\*')
        replacement = f'<span class="claudian-embedded-image-fallback">![[{hashes[i-1]}.png]]</span>\n{captions[i-1]}'
        if placeholder_pattern.search(text):
            text = placeholder_pattern.sub(replacement, text)
            print(f"Replaced Fig {i}")
        else:
            print(f"Fig {i} placeholder not found!")
            
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    print("Done 统计热力学与Maxwell关系")
