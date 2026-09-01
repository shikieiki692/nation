# -*- coding: utf-8 -*-
"""为断链目标找库内候选文件；检查图片是否已在媒体仓库。"""
import os, re, difflib
from collections import defaultdict

VAULT = r"C:\Obsidion\妙妙屋"
TARGET = os.path.join(VAULT, "03-知识点", "高中化学基础")
MEDIA = os.path.join(VAULT, "媒体仓库")

md_files = []
for root, dirs, files in os.walk(VAULT):
    dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']
    for f in files:
        if f.lower().endswith('.md'):
            md_files.append((f[:-3], os.path.relpath(os.path.join(root, f), VAULT).replace('\\', '/')))
names = [n for n, _ in md_files]

broken = ["元素周期表", "离子反应", "热化学", "硫化学",
          "必修1 Ch1 - 物质及其变化 教师用书提炼", "必修1 Ch2 - 海水中的重要元素 教师用书提炼",
          "必修1 Ch3 - 铁 金属材料 教师用书提炼", "必修1 Ch4 - 物质结构 元素周期律 教师用书提炼",
          "必修2 Ch5 - 化工生产中的重要非金属元素 教师用书提炼", "必修2 Ch6 - 化学反应与能量 教师用书提炼",
          "必修2 Ch7 - 有机化合物 教师用书提炼", "必修2 Ch8 - 化学与可持续发展 教师用书提炼",
          "选修1 Ch1 - 化学反应的热效应 教师用书提炼", "选修1 Ch2 - 化学反应速率与化学平衡 教师用书提炼",
          "选修1 Ch3 - 水溶液中的离子反应与平衡 教师用书提炼", "选修1 Ch4 - 化学反应与电能 教师用书提炼",
          "选修2 Ch1 - 原子结构与性质 教师用书提炼", "选修2 Ch2 - 分子结构与性质 教师用书提炼",
          "选修2 Ch3 - 晶体结构与性质 教师用书提炼",
          "选修3 Ch1 - 有机化合物的结构特点与研究方法 教师用书提炼",
          "选修3 Ch2 - 烃 教师用书提炼", "选修3 Ch3 - 烃的衍生物 教师用书提炼",
          "选修3 Ch4 - 生物大分子 教师用书提炼", "选修3 Ch5 - 合成高分子 教师用书提炼"]

print("=== 断链目标 → 库内候选 ===")
for b in broken:
    key = re.sub(r'\s*-\s*', ' ', b).strip()
    cands = difflib.get_close_matches(b, names, n=3, cutoff=0.45)
    # 关键词命中
    kw = [w for w in re.split(r'[\s\-]+', b) if len(w) >= 2][:2]
    hits = [p for n, p in md_files if kw and all(k in n for k in kw)][:3]
    print(f"\n[[{b}]]")
    if cands:
        for c in cands:
            p = dict(md_files).get(c, '?')
            print(f"   近似: {c}   ({p})")
    if hits:
        for h in hits:
            print(f"   关键词: {h}")
    if not cands and not hits:
        print("   （库内无候选 → 确实未建）")

# 图片是否在媒体仓库
media_set = set(os.listdir(MEDIA))
MD_IMG = re.compile(r'!\[[^\]]*\]\(\s*<?([^)>]+?)>?\s*\)')
used = set()
for f in os.listdir(TARGET):
    if f.endswith('.md'):
        t = open(os.path.join(TARGET, f), encoding='utf-8').read()
        for m in MD_IMG.finditer(t):
            used.add(os.path.basename(m.group(1).strip()))
in_media = [u for u in used if u in media_set]
print(f"\n=== 图片 ===\n引用图片 {len(used)} 张，其中已在媒体仓库 {len(in_media)} 张，未入库 {len(used)-len(in_media)} 张")
