import json, os

out_dir = r'c:\Obsidion\妙妙屋\10-索引与统计\讲义用图补录'
os.makedirs(out_dir, exist_ok=True)
out_file = os.path.join(out_dir, '_index.md')

lines = []
lines.append("# 讲义在用图 (迁移合并专用)\n")
lines.append("| 文件名 | 内容描述 | 建议重命名 | 关联KP | Quality |")
lines.append("| --- | --- | --- | --- | --- |")

def append_to_lines(map_path, desc_prefix):
    with open(map_path, 'r', encoding='utf-8') as f:
        mapping_data = json.load(f)
    
    mapping = mapping_data.get('mapping', {})
    for old_name, info in mapping.items():
        new_hash = info.get('hash')
        if not new_hash: continue
        
        alias = os.path.splitext(old_name)[0]
        desc = f"【{desc_prefix}】{alias}"
        
        # 文件名(含后缀) | 描述 | 建议重命名(Agent的语义搜索特征码) | KP | Quality
        lines.append(f"| {new_hash} | {desc} | {alias} | 讲义在用 | HIGH |")

append_to_lines(r'c:\Obsidion\妙妙屋\10-索引与统计\讲义media迁移映射.json', '讲义在用图迁移')
try:
    append_to_lines(r'c:\Obsidion\妙妙屋\10-索引与统计\旧media迁移摘要.json', '旧media迁移')
except: pass

with open(out_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print(f"Created {out_file} with {len(lines) - 3} entries.")
