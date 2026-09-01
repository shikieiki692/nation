# -*- coding: utf-8 -*-
"""精确检查 高中化学基础 的 Markdown 图片相对路径是否可解析。"""
import re, os, urllib.parse
from collections import defaultdict, Counter

VAULT = r"C:\Obsidion\妙妙屋"
TARGET = os.path.join(VAULT, "03-知识点", "高中化学基础")
MD_IMG = re.compile(r'!\[[^\]]*\]\(\s*<?([^)>]+?)>?\s*(?:"[^"]*")?\s*\)')

stat = Counter()
rows = []
for f in sorted(os.listdir(TARGET)):
    if not f.endswith('.md'):
        continue
    src = os.path.join(TARGET, f)
    text = open(src, encoding='utf-8').read()
    for m in MD_IMG.finditer(text):
        raw = m.group(1).strip()
        if raw.startswith(('http://', 'https://', 'data:')):
            continue
        dec = urllib.parse.unquote(raw).replace('\\', '/')
        p_rel = os.path.normpath(os.path.join(TARGET, dec))    # 相对当前文件
        p_root = os.path.normpath(os.path.join(VAULT, dec.lstrip('/')))  # 相对 vault 根
        if os.path.isfile(p_rel):
            st, resolved = 'OK-相对文件', p_rel
        elif os.path.isfile(p_root):
            st, resolved = 'OK-仅根解析', p_root
        else:
            st, resolved = '损坏', None
        stat[st] += 1
        rows.append((f, raw, st, os.path.relpath(resolved, VAULT).replace('\\', '/') if resolved else ''))

print(f"{'源文件':<24} {'状态':<12} 引用路径")
print('-' * 140)
for f, raw, st, rel in rows:
    print(f"{f:<24} {st:<12} {raw}")

print("\n== 统计 ==")
for k, v in stat.items():
    print(f"  {k}: {v}")

print("\n== 损坏明细（按错误前缀归类）==")
bad_prefix = Counter()
for f, raw, st, rel in rows:
    if st == '损坏':
        bad_prefix[raw.split('/')[0] if '/' in raw else raw] += 1
for k, v in bad_prefix.most_common():
    print(f"  {k}  ->  {v} 处")
