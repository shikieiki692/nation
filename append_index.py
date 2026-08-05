import json, os

index_path = r'c:\Obsidion\妙妙屋\10-索引与统计\全库核心图谱总索引.md'
with open(index_path, 'r', encoding='utf-8') as f:
    index_lines = f.readlines()

existing_hashes = set()
for line in index_lines:
    if line.startswith('|') and len(line.split('|')) > 2:
        hash_col = line.split('|')[1].strip()
        existing_hashes.add(hash_col)

new_lines = []

def process_mapping(map_path, desc_prefix):
    with open(map_path, 'r', encoding='utf-8') as f:
        mapping_data = json.load(f)
        
    mapping = mapping_data.get('mapping', {})
    for old_name, info in mapping.items():
        new_hash = info.get('hash')
        if not new_hash: continue
        
        if new_hash not in existing_hashes:
            alias = os.path.splitext(old_name)[0]
            desc = f"【{desc_prefix}】{alias}"
            row = f"| {new_hash} | {alias} | {desc} | 讲义在用 | 媒体仓库/ | ✅在媒体仓库 |\n"
            new_lines.append(row)
            existing_hashes.add(new_hash)

# Process both JSON files
process_mapping(r'c:\Obsidion\妙妙屋\10-索引与统计\讲义media迁移映射.json', '讲义在用图迁移')
try:
    process_mapping(r'c:\Obsidion\妙妙屋\10-索引与统计\旧media迁移摘要.json', '旧media迁移')
except Exception as e:
    print(f"Skipped legacy media: {e}")

if new_lines:
    with open(index_path, 'a', encoding='utf-8') as f:
        f.writelines(new_lines)

print(f"Successfully appended {len(new_lines)} images to the index.")
