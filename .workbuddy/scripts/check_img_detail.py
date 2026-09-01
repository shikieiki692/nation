# -*- coding: utf-8 -*-
"""详查 高中化学基础 的图片引用：解析到哪个目录 / 是否在媒体仓库 / 是否带子路径。"""
import re, os
from collections import defaultdict

VAULT = r"C:\Obsidion\妙妙屋"
TARGET = os.path.join(VAULT, "03-知识点", "高中化学基础")
IMG_EXT = {'.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp', '.bmp'}

img_index = defaultdict(list)
for root, dirs, files in os.walk(VAULT):
    dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']
    for f in files:
        if os.path.splitext(f)[1].lower() in IMG_EXT:
            img_index[f].append(os.path.join(root, f))

EMBED = re.compile(r'!\[\[([^\]\|#]+)[^\]]*\]\]')

rows = []
for f in sorted(os.listdir(TARGET)):
    if not f.endswith('.md'):
        continue
    text = open(os.path.join(TARGET, f), encoding='utf-8').read()
    for m in EMBED.finditer(text):
        raw = m.group(1).strip()
        base = os.path.basename(raw)
        hits = img_index.get(base, [])
        if not hits:
            rows.append((f, raw, 'MISSING', ''))
            continue
        for p in hits:
            rel = os.path.relpath(p, VAULT).replace('\\', '/')
            top = rel.split('/')[0]
            rows.append((f, raw, 'OK' if top == '媒体仓库' else '外散', rel))

print(f"{'源文件':<26} {'引用':<40} {'状态':<8} 解析位置")
print('-' * 130)
for src, raw, st, rel in rows:
    print(f"{src:<26} {raw[:38]:<40} {st:<8} {rel}")

miss = [r for r in rows if r[2] == 'MISSING']
out = [r for r in rows if r[2] == '外散']
print(f"\n总计 {len(rows)} 处图片引用 | 缺失 {len(miss)} | 不在媒体仓库(外散) {len(out)}")
