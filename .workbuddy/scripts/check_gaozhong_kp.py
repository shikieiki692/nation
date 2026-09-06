# -*- coding: utf-8 -*-
"""扫描 03-知识点/高中化学基础：统计双链断链 + 图片引用损坏。"""
import re
import os
import json
import sys
from collections import defaultdict

VAULT = r"C:\Obsidion\妙妙屋"
TARGET = os.path.join(VAULT, "03-知识点", "高中化学基础")

# 1) 建立全库 md 文件名索引（basename -> 绝对路径列表）
md_index = defaultdict(list)
for root, dirs, files in os.walk(VAULT):
    dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']
    for f in files:
        if f.lower().endswith('.md'):
            md_index[f].append(os.path.join(root, f))

# 2) 建立全库图片文件名索引（basename -> 绝对路径列表）
IMG_EXT = {'.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp', '.bmp', '.tif', '.tiff'}
img_index = defaultdict(list)
for root, dirs, files in os.walk(VAULT):
    dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']
    for f in files:
        if os.path.splitext(f)[1].lower() in IMG_EXT:
            img_index[f].append(os.path.join(root, f))

local_names = {f for f in os.listdir(TARGET) if f.lower().endswith('.md')}

LINK_RE = re.compile(r'(!?)\[\[([^\]\|#\^]+)(?:[#\^\|][^\]]*)?\]\]')
MD_LINK_IMG_RE = re.compile(r'!\[[^\]]*\]\(([^)]+)\)')

results = {}
total_wiki, total_img, broken_wiki, broken_img = 0, 0, 0, 0
broken_wiki_map = defaultdict(list)   # 目标 -> [源文件...]
broken_img_map = defaultdict(list)
img_used = defaultdict(list)          # 引用的图片 basename -> 源文件

for f in sorted(local_names):
    path = os.path.join(TARGET, f)
    with open(path, encoding='utf-8') as fh:
        text = fh.read()
    wl, il, bw, bi = [], [], [], []
    for m in LINK_RE.finditer(text):
        bang, target = m.group(1), m.group(2).strip()
        if bang:  # ![[...]] 图片
            total_img += 1
            base = os.path.basename(target)
            name = base if os.path.splitext(base)[1] else base + '.png'
            il.append(target)
            img_used[name].append(f)
            if name not in img_index:
                bi.append(target)
                broken_img += 1
                broken_img_map[target].append(f)
        else:
            total_wiki += 1
            wl.append(target)
            cand = target if target.lower().endswith('.md') else target + '.md'
            cand = os.path.basename(cand)
            if cand not in md_index:
                bw.append(target)
                broken_wiki += 1
                broken_wiki_map[target].append(f)
    for m in MD_LINK_IMG_RE.finditer(text):
        total_img += 1
        raw = m.group(1).strip().split()[0] if m.group(1).strip() else ''
        base = os.path.basename(raw)
        il.append(raw)
        img_used[base].append(f)
        if base not in img_index:
            bi.append(raw)
            broken_img += 1
            broken_img_map[raw].append(f)
    results[f] = dict(wiki=wl, broken_wiki=bw, img=il, broken_img=bi)

out = dict(
    target=TARGET,
    files=len(local_names),
    total_wiki=total_wiki, broken_wiki=broken_wiki,
    total_img=total_img, broken_img=broken_img,
    broken_wiki_map={k: v for k, v in broken_wiki_map.items()},
    broken_img_map={k: v for k, v in broken_img_map.items()},
    per_file={k: v for k, v in results.items() if v['broken_wiki'] or v['broken_img']},
)
with open(os.path.join(VAULT, '.workbuddy', 'scripts', 'check_gaozhong_kp.json'), 'w', encoding='utf-8') as fh:
    json.dump(out, fh, ensure_ascii=False, indent=1)

print(f"文件数 {len(local_names)}")
print(f"双链 {total_wiki} 条，断链 {broken_wiki} 条（唯一目标 {len(broken_wiki_map)}）")
print(f"图片引用 {total_img} 处，损坏 {broken_img} 处（唯一 {len(broken_img_map)}）")
print("\n=== 断链目标（未建文件） ===")
for k, v in sorted(broken_wiki_map.items(), key=lambda x: -len(x[1])):
    print(f"  [[{k}]]  被 {len(v)} 个文件引用: {', '.join(sorted(set(v))[:4])}{'...' if len(set(v))>4 else ''}")
print("\n=== 损坏图片 ===")
for k, v in sorted(broken_img_map.items(), key=lambda x: -len(x[1])):
    print(f"  ![[{k}]]  被 {len(v)} 个文件引用: {', '.join(sorted(set(v))[:3])}{'...' if len(set(v))>3 else ''}")
