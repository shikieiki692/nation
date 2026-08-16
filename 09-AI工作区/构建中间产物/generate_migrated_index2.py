import json, os

out_dir = r'c:\Obsidion\妙妙屋\10-索引与统计\讲义用图补录'
os.makedirs(out_dir, exist_ok=True)
out_file = os.path.join(out_dir, '_index.md')

with open(out_file, 'r', encoding='utf-8') as f:
    existing = f.read()

lines = []
def append_to_lines(map_path, desc_prefix):
    with open(map_path, 'r', encoding='utf-8') as f:
        mapping_data = json.load(f)
    
    mapping = mapping_data.get('mapping', {})
    for old_name, info in mapping.items():
        new_hash = info.get('hash')
        if not new_hash: continue
        
        alias = os.path.splitext(old_name)[0]
        desc = f"【{desc_prefix}】{alias}"
        
        if new_hash not in existing:
            lines.append(f"| {new_hash} | {desc} | {alias} | 缺失修复 | HIGH |")

try:
    append_to_lines(r'c:\Obsidion\妙妙屋\10-索引与统计\修复缺失图片_映射.json', '缺失引用修复')
except Exception as e:
    print(f"Error: {e}")

if lines:
    with open(out_file, 'a', encoding='utf-8') as f:
        f.write('\n' + '\n'.join(lines))
    print(f"Appended {len(lines)} new entries to _index.md")
else:
    print("No new entries to append.")
