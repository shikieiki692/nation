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

def draw_fig1_amphiphilic():
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.axis('off')
    
    # Liquid surface
    ax.axhline(0.3, color='blue', lw=2)
    ax.fill_between([0, 1], 0, 0.3, color='blue', alpha=0.1)
    ax.text(0.1, 0.15, "液相 (水)", color='blue', fontsize=12)
    ax.text(0.1, 0.4, "气相", color='gray', fontsize=12)
    
    # Molecules
    for x in np.linspace(0.3, 0.8, 6):
        # Head
        ax.add_patch(patches.Circle((x, 0.3), 0.03, facecolor='red', zorder=3))
        # Tail
        ax.plot([x, x+0.02, x-0.02, x+0.02, x-0.02, x], np.linspace(0.3, 0.7, 6), color='black', lw=1.5)
        
    ax.text(0.5, 0.8, "疏水尾 (朝向气相)", ha='center', fontsize=12)
    ax.text(0.5, 0.2, "亲水头 (埋入水相)", ha='center', fontsize=12, color='red')
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    return save_and_hash(fig, "fig1_amphiphilic")

def draw_fig2_cmc():
    fig, ax = plt.subplots(figsize=(6, 4))
    
    # x axis: log C
    x1 = np.linspace(1e-4, 1e-2, 50)
    y1 = 70 - 15 * (np.log10(x1) - np.log10(1e-4))
    
    x2 = np.linspace(1e-2, 1e-1, 50)
    y2 = 40 * np.ones_like(x2)
    
    ax.plot(np.log10(x1), y1, 'b-', lw=2)
    ax.plot(np.log10(x2), y2, 'b-', lw=2)
    
    cmc_x = np.log10(1e-2)
    ax.axvline(cmc_x, color='red', linestyle='--')
    ax.text(cmc_x, 35, "CMC", color='red', fontsize=12, ha='center')
    
    ax.set_xlabel("log(浓度)")
    ax.set_ylabel("表面张力 γ")
    ax.set_title("表面张力随浓度变化曲线 (CMC)")
    
    return save_and_hash(fig, "fig2_cmc")

def draw_fig3_colloid():
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.axis('off')
    
    # Core
    ax.add_patch(patches.Circle((0.5, 0.5), 0.1, facecolor='#cccccc', edgecolor='black'))
    ax.text(0.5, 0.5, "胶核\n[Fe(OH)₃]m", ha='center', va='center', fontsize=10)
    
    # Adsorption layer
    ax.add_patch(patches.Circle((0.5, 0.5), 0.15, fill=False, edgecolor='blue', linestyle='--'))
    ax.text(0.5, 0.67, "电位离子层 (FeO⁺)\n吸附层", ha='center', va='center', color='blue')
    
    # Slip plane
    ax.add_patch(patches.Circle((0.5, 0.5), 0.22, fill=False, edgecolor='red', lw=2))
    ax.text(0.75, 0.75, "滑动面 (ζ电位)", color='red')
    ax.annotate("", xy=(0.65, 0.65), xytext=(0.73, 0.73), arrowprops=dict(arrowstyle="->", color='red'))
    
    # Diffusion layer
    ax.add_patch(patches.Circle((0.5, 0.5), 0.35, fill=False, edgecolor='green', linestyle=':'))
    ax.text(0.5, 0.1, "扩散层 (Cl⁻)", ha='center', va='center', color='green')
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    return save_and_hash(fig, "fig3_colloid")

def draw_fig4_dlvo():
    fig, ax = plt.subplots(figsize=(6, 4))
    
    x = np.linspace(0.1, 3, 100)
    v_a = -1 / (x**2)
    v_r = 5 * np.exp(-3*x)
    v_total = v_a + v_r
    
    ax.plot(x, v_a, 'r--', label='范德华引力 (Va)')
    ax.plot(x, v_r, 'b--', label='双电层斥力 (Vr)')
    ax.plot(x, v_total, 'k-', lw=2, label='总势能 (V)')
    
    ax.axhline(0, color='gray', lw=1)
    
    # Barrier
    max_idx = np.argmax(v_total)
    ax.annotate('势垒', xy=(x[max_idx], v_total[max_idx]), xytext=(x[max_idx]+0.5, v_total[max_idx]+1),
                arrowprops=dict(arrowstyle='->'))
                
    ax.set_xlabel("粒子间距 H")
    ax.set_ylabel("势能 V")
    ax.set_title("DLVO 理论势能曲线")
    ax.set_ylim(-3, 3)
    ax.set_xlim(0, 3)
    ax.legend()
    
    return save_and_hash(fig, "fig4_dlvo")

def draw_fig5_wetting():
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.axis('off')
    
    # Solid
    ax.add_patch(patches.Rectangle((0.1, 0.2), 0.8, 0.1, facecolor='gray'))
    ax.text(0.5, 0.25, "固相 (Solid)", ha='center', va='center', color='white')
    
    # Drop
    theta = np.linspace(0, np.pi, 100)
    x = 0.5 + 0.2 * np.cos(theta)
    y = 0.3 + 0.15 * np.sin(theta)
    ax.fill(x, y, color='blue', alpha=0.3)
    ax.plot(x, y, color='blue', lw=2)
    
    ax.text(0.5, 0.4, "液相 (Liquid)", ha='center', color='blue')
    ax.text(0.2, 0.5, "气相 (Gas)", ha='center')
    
    # Angle
    ax.annotate("θ (接触角)", xy=(0.32, 0.32), xytext=(0.2, 0.35), arrowprops=dict(arrowstyle="->", lw=1))
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    return save_and_hash(fig, "fig5_wetting")

def draw_fig6_langmuir():
    fig, ax = plt.subplots(figsize=(6, 4))
    
    p = np.linspace(0, 10, 100)
    K = 1
    theta = K * p / (1 + K * p)
    
    ax.plot(p, theta, 'b-', lw=2)
    ax.axhline(1, color='red', linestyle='--')
    ax.text(8, 0.95, "θ = 1 (饱和吸附)", color='red')
    
    ax.set_xlabel("压力 p (或浓度 c)")
    ax.set_ylabel("覆盖度 θ")
    ax.set_title("Langmuir 吸附等温线")
    ax.set_ylim(0, 1.1)
    ax.grid(True, alpha=0.3)
    
    return save_and_hash(fig, "fig6_langmuir")

if __name__ == "__main__":
    h1 = draw_fig1_amphiphilic()
    h2 = draw_fig2_cmc()
    h3 = draw_fig3_colloid()
    h4 = draw_fig4_dlvo()
    h5 = draw_fig5_wetting()
    h6 = draw_fig6_langmuir()
    
    hashes = [h1, h2, h3, h4, h5, h6]
    captions = [
        "*图 1 两亲性分子在气-液界面的定向排列*",
        "*图 2 溶液表面张力随浓度变化及 CMC 拐点*",
        "*图 3 Fe(OH)₃ 胶团双电层结构及 ζ 电位分布*",
        "*图 4 DLVO 理论胶体粒子相互作用势能曲线*",
        "*图 5 润湿现象气-液-固三相交点及接触角 θ*",
        "*图 6 Langmuir 等温吸附曲线及 θ=1 极限*"
    ]
    
    filepath = r"C:\Obsidion\妙妙屋\04-课件\学生讲义\胶体与表面物理化学-超级充实版（自学完整）.md"
    
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    text = re.sub(r'has_images:\s*false', 'has_images: true', text)
    text = re.sub(r'image_count:\s*0', 'image_count: 6', text)

    for i in range(1, 7):
        placeholder_pattern = re.compile(r'📌\s*\*\*图片待补（图\s*' + str(i) + r'）\*\*')
        replacement = f'<span class="claudian-embedded-image-fallback">![[{hashes[i-1]}.png]]</span>\n{captions[i-1]}'
        if placeholder_pattern.search(text):
            text = placeholder_pattern.sub(replacement, text)
            print(f"Replaced Fig {i}")
        else:
            print(f"Fig {i} placeholder not found!")
            
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    print("Done 胶体与表面物理化学")
