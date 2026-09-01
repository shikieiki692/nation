# -*- coding: utf-8 -*-
"""用 validate_kb 自身逻辑精确复算 frontmatter 红链全集"""
import sys, re, os
sys.path.insert(0, r"C:\Obsidion\妙妙屋\11-模板\scripts")
from pathlib import Path
import validate_kb as vk

ROOT = vk.VAULT_ROOT
rows = []
files = vk.collect_md_files(ROOT, vk.INCLUDE_DIRS)
for p in files:
    rel = p.relative_to(ROOT).as_posix()
    try:
        fm, _body = vk.parse_frontmatter_from_file(p)
    except Exception:
        continue
    if not isinstance(fm, dict):
        continue
    for field in vk.QB_LINK_FIELDS:
            vals = fm.get(field)
            if isinstance(vals, str):
                vals = [vals]
            if not isinstance(vals, list):
                continue
            for v in vals:
                if not isinstance(v, str):
                    continue
                for tgt in re.findall(r"(?<!\!)\[\[([^\]|#]+)", v):
                    tgt = tgt.strip()
                    if not tgt or vk.is_placeholder_target(tgt):
                        continue
                    if Path(tgt).suffix.lower() in {".png",".jpg",".jpeg",".gif",".webp",".svg"}:
                        continue
                    if vk.find_wikilink_target(tgt, ROOT) is None:
                        rows.append((rel, field, tgt))

print("TOTAL", len(rows))
# 我关心的键
keys = ["习题-结构化学基础","学生讲义模板","第24章","第25章","第2章-有机结构","第37章","第41章",
        "第7章-离域","批次Z-G","Ch13-选择题","Ch14-简答","Ch14-选择题","例18.3","20.1-20.10",
        "21.1-21.12","晶体-习18","晶体-习32","拆题清单","题-459"]
for k in keys:
    hits = [r for r in rows if k in r[0]]
    if hits:
        print("HIT", k, hits[:6])
# 我回填的16值是否出现在任何其他文件的红链里
names = ["共轭效应","分子轨道理论","键级","原子光谱与光谱项","杂化轨道理论","NiAs型结构"]
for n in names:
    hits = [r for r in rows if r[2] == n]
    print(f"红链里含 {n}: {len(hits)}", hits[:4])
