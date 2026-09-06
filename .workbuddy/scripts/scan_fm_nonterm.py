# -*- coding: utf-8 -*-
"""临时扫描：frontmatter knowledge_points 红链值盘点 + 非术语值启发式标记"""
import os, re, sys, yaml, collections

ROOT = r"C:\Obsidion\妙妙屋"
SKIP = {'.git', '.venv', 'node_modules', '.workbuddy', '_归档', '_archive_v2', '99-归档', '09-审计报告', 'kb-vault-mcp', '.obsidian'}

# 1) 收集全库 md basename（用于解析红链目标是否真的不存在）
all_names = set()
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in SKIP]
    for f in filenames:
        if f.endswith('.md'):
            all_names.add(os.path.splitext(f)[0])

# 2) 扫描 frontmatter 中带链接语义的字段
FIELDS = ['knowledge_points', 'related_kp', 'related', 'prerequisites']
broken = collections.Counter()          # value -> count
samples = collections.defaultdict(list) # value -> [(file, field)]
fm_files = 0

for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in SKIP]
    for f in filenames:
        if not f.endswith('.md'):
            continue
        p = os.path.join(dirpath, f)
        try:
            text = open(p, encoding='utf-8').read()
        except Exception:
            continue
        m = re.match(r'^---\r?\n(.*?)\r?\n---', text, re.S)
        if not m:
            continue
        try:
            fm = yaml.safe_load(m.group(1))
        except Exception:
            continue
        if not isinstance(fm, dict):
            continue
        fm_files += 1
        for field in FIELDS:
            v = fm.get(field)
            if v is None:
                continue
            vals = v if isinstance(v, list) else [v]
            for item in vals:
                if not isinstance(item, str):
                    continue
                name = re.sub(r'^\[\[|\]\]$', '', item.strip()).split('|')[0].split('#')[0].strip()
                if not name:
                    continue
                if name not in all_names:
                    broken[name] += 1
                    if len(samples[name]) < 3:
                        samples[name].append((os.path.relpath(p, ROOT), field))

print(f"含 frontmatter 的 md: {fm_files}")
print(f"红链唯一值: {len(broken)}  总计: {sum(broken.values())}")

# 3) 非术语启发式
suspect_pat = re.compile(
    r'(题|填空|选择|判断|简答|计算|综合|分析题|待|人工|标定|暂|占位|TODO|TBD|待定|待补|待查|'
    r'\d{4}|\d+\s*(届|年|月)|[a-zA-Z]{6,}|[?？!！。；;，,、]{1}|^\s*$|说明|见|其他|未知)', re.I)
sus = {k: v for k, v in broken.items() if suspect_pat.search(k) and len(k) <= 12}
print(f"\n=== 疑似非术语值（启发式）: {len(sus)} ===")
for k in sorted(sus, key=sus.get, reverse=True):
    print(f"  [{sus[k]}] {k}  <- {samples[k][0][0]} ({samples[k][0][1]})")

# 4) 高频红链 top20（真知识点，供参考，不处理）
print("\n=== 高频红链 top20（真知识点，不处理）===")
for k, c in broken.most_common(20):
    print(f"  [{c}] {k}")
