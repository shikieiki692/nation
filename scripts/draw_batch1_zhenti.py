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

def draw_fig1_radar():
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, polar=True)
    labels = ['调用速度', '决策质量', '止损意识', '容错机制', '时间感知']
    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]
    values = [4, 5, 3, 4, 5]
    values += values[:1]
    
    ax.plot(angles, values, 'o-', linewidth=2, color='darkorange')
    ax.fill(angles, values, color='orange', alpha=0.25)
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=12)
    ax.set_ylim(0, 5)
    ax.set_title("考试元能力五维度雷达图", pad=20, fontsize=14, fontweight='bold')
    return save_and_hash(fig, "fig1_radar")

def draw_fig2_strategy():
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('off')
    
    cols = ["题型 I\n(基础题)", "题型 II\n(中档题)", "题型 III\n(压轴题)", "题型 IV\n(创新题)"]
    rows = ["识别特征", "武器库", "分值占比", "建议用时"]
    data = [
        ["常规眼熟", "题干长信息多", "反常态/极端", "新概念/新模型"],
        ["秒杀技巧", "流程法", "极限法/分类", "类比/本质"],
        ["~30%", "~40%", "~20%", "~10%"],
        ["1 min/题", "3 min/题", "5 min/题", "视情况止损"]
    ]
    
    table = ax.table(cellText=data, rowLabels=rows, colLabels=cols, loc='center', cellLoc='center')
    table.scale(1, 3.5)
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    
    for (i, j), cell in table.get_celld().items():
        if i == 0 or j == -1:
            cell.set_text_props(weight='bold', color='white')
            cell.set_facecolor('#0066cc')
        else:
            cell.set_facecolor('#f0f8ff')
            
    ax.set_title("四类题型策略匹配板", fontsize=15, fontweight='bold', pad=20)
    return save_and_hash(fig, "fig2_strategy")

def draw_fig3_5step():
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.axis('off')
    
    steps = ["①信息提取", "②识别变化", "③跟踪电子", "④验证闭环", "⑤落笔"]
    times = ["~30s", "~1min", "~2min", "~1min", "~30s"]
    
    for i in range(5):
        x = 0.1 + i*0.18
        box = patches.FancyBboxPatch((x, 0.4), 0.14, 0.2, boxstyle="round,pad=0.05", 
                                     facecolor='#e6ffe6', edgecolor='#009900', lw=2)
        ax.add_patch(box)
        ax.text(x+0.07, 0.5, steps[i], ha='center', va='center', fontsize=12, fontweight='bold')
        ax.text(x+0.07, 0.3, times[i], ha='center', va='center', fontsize=10, color='gray')
        
        if i < 4:
            ax.annotate("", xy=(x+0.16, 0.5), xytext=(x+0.14, 0.5), arrowprops=dict(arrowstyle="->", lw=2, color='black'))
            
    return save_and_hash(fig, "fig3_5step")

def draw_fig4_gantt():
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.axis('off')
    
    phases = [
        ("通览全局", 0, 10, '#cccccc'),
        ("题型 I+II", 10, 80, '#99ff99'),
        ("题型 III", 80, 130, '#ffff99'),
        ("题型 IV", 130, 160, '#ff9999'),
        ("机动检查", 160, 180, '#ccccff')
    ]
    
    ax.plot([0, 180], [0.5, 0.5], color='black', lw=1)
    
    for label, start, end, color in phases:
        rect = patches.Rectangle((start, 0.4), end-start, 0.2, facecolor=color, edgecolor='black')
        ax.add_patch(rect)
        ax.text((start+end)/2, 0.5, f"{label}\n({end-start}min)", ha='center', va='center', fontsize=10)
        
    ax.set_xlim(-10, 190)
    ax.set_ylim(0, 1)
    ax.text(90, 0.8, "180 min 时间分配甘特图", ha='center', va='center', fontsize=14, fontweight='bold')
    
    # Timeline ticks
    for tick in [0, 60, 120, 180]:
        ax.text(tick, 0.3, f"{tick}m", ha='center', va='top', fontsize=10)
        ax.plot([tick, tick], [0.35, 0.4], color='black')
        
    return save_and_hash(fig, "fig4_gantt")

def draw_fig5_stoploss():
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.axis('off')
    
    ax.text(0.5, 0.8, "遇到难题", ha='center', va='center', fontsize=12, bbox=dict(boxstyle="circle", facecolor="#eeeeee"))
    ax.text(0.5, 0.5, "是否超止损线?\n(如 5 min)", ha='center', va='center', fontsize=12, bbox=dict(boxstyle="square", facecolor="#ffeeee"))
    
    ax.text(0.2, 0.2, "果断跳过\n并标记", ha='center', va='center', fontsize=12, bbox=dict(boxstyle="round", facecolor="#ffcccc"))
    ax.text(0.8, 0.2, "继续死磕", ha='center', va='center', fontsize=12, bbox=dict(boxstyle="round", facecolor="#ccffcc"))
    
    ax.text(0.2, 0.8, "回头做", ha='center', va='center', fontsize=12, bbox=dict(boxstyle="larrow", facecolor="#ccccff"))
    
    ax.annotate("", xy=(0.5, 0.6), xytext=(0.5, 0.73), arrowprops=dict(arrowstyle="->", lw=2))
    ax.annotate("Yes", xy=(0.2, 0.28), xytext=(0.4, 0.45), arrowprops=dict(arrowstyle="->", lw=2))
    ax.annotate("No", xy=(0.8, 0.28), xytext=(0.6, 0.45), arrowprops=dict(arrowstyle="->", lw=2))
    
    ax.annotate("", xy=(0.2, 0.75), xytext=(0.2, 0.28), arrowprops=dict(arrowstyle="->", lw=2, color='blue'))
    ax.annotate("", xy=(0.43, 0.8), xytext=(0.28, 0.8), arrowprops=dict(arrowstyle="->", lw=2, color='blue'))
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    return save_and_hash(fig, "fig5_stoploss")

def draw_fig6_bde_arnh2():
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.axis('off')
    
    nodes = {
        "ArNH₂(sol)": (0.2, 0.8),
        "ArNH•(sol) + H•(sol)": (0.8, 0.8),
        "ArNH₂⁺•(sol) + e⁻": (0.2, 0.2),
        "ArNH•(sol) + H⁺(sol)": (0.8, 0.2)
    }
    
    for label, (x, y) in nodes.items():
        box = patches.FancyBboxPatch((x-0.15, y-0.08), 0.3, 0.16, boxstyle="round,pad=0.02", 
                                     facecolor='#f0f8ff', edgecolor='#0000cc', lw=1.5)
        ax.add_patch(box)
        ax.text(x, y, label, ha='center', va='center', fontsize=11)
        
    ax.annotate("BDE", xy=(0.65, 0.8), xytext=(0.35, 0.8), arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.annotate("ET (-e⁻)", xy=(0.2, 0.65), xytext=(0.2, 0.35), arrowprops=dict(arrowstyle="<-", lw=1.5))
    ax.annotate("PT (-H⁺)", xy=(0.65, 0.2), xytext=(0.35, 0.2), arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.annotate("solv", xy=(0.8, 0.65), xytext=(0.8, 0.35), arrowprops=dict(arrowstyle="<-", lw=1.5))
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    return save_and_hash(fig, "fig6_bde_arnh2")

def draw_fig7_a4():
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.axis('off')
    
    ax.add_patch(patches.Rectangle((0.1, 0.1), 0.35, 0.8, fill=True, facecolor='#fffff0', edgecolor='black', lw=2))
    ax.text(0.275, 0.85, "A4 正面\n(硬核公式区)", ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(0.275, 0.5, "- 动力学三大方程\n- Nernst 展开\n- 热力学判据", ha='center', va='center', fontsize=10)
    
    ax.add_patch(patches.Rectangle((0.55, 0.1), 0.35, 0.8, fill=True, facecolor='#f0ffff', edgecolor='black', lw=2))
    ax.text(0.725, 0.85, "A4 背面\n(推断流程区)", ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(0.725, 0.5, "- 沉淀色卡\n- 焰色反应\n- 核心鉴别路径", ha='center', va='center', fontsize=10)
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    return save_and_hash(fig, "fig7_a4")

if __name__ == "__main__":
    h1 = draw_fig1_radar()
    h2 = draw_fig2_strategy()
    h3 = draw_fig3_5step()
    h4 = draw_fig4_gantt()
    h5 = draw_fig5_stoploss()
    h6 = draw_fig6_bde_arnh2()
    h7 = draw_fig7_a4()
    
    hashes = [h1, h2, h3, h4, h5, h6, h7]
    captions = [
        "*图 1 考试元能力五维度雷达图*",
        "*图 2 四类题型策略与特征匹配板*",
        "*图 3 考试解题五步法标准化流程图*",
        "*图 4 180 min 考试时间分配甘特图*",
        "*图 5 考试考场止损线决策图*",
        "*图 6 苯胺 BDE 热化学循环闭合图*",
        "*图 7 A4 速记卡版式布局示意*"
    ]
    
    filepath = r"C:\Obsidion\妙妙屋\04-课件\学生讲义\真题模拟拆解-超级充实版（自学完整）.md"
    
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    text = re.sub(r'has_images:\s*false', 'has_images: true', text)
    text = re.sub(r'image_count:\s*0', 'image_count: 7', text)

    for i in range(1, 8):
        placeholder_pattern = re.compile(r'📌\s*\*\*图片待补（图\s*' + str(i) + r'）\*\*')
        replacement = f'<span class="claudian-embedded-image-fallback">![[{hashes[i-1]}.png]]</span>\n{captions[i-1]}'
        if placeholder_pattern.search(text):
            text = placeholder_pattern.sub(replacement, text)
            print(f"Replaced Fig {i}")
        else:
            print(f"Fig {i} placeholder not found!")
            
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    print("Done 真题模拟拆解")
