import os
import re
import json
import shutil

vault_root = r'C:\Obsidion\妙妙屋'
media_dir = os.path.join(vault_root, '媒体仓库')
excluded_json = os.path.join(vault_root, '10-索引与统计', 'excluded_dump.json')

IMAGE_EXT = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tif', '.tiff')

def build_vault_image_index():
    all_names = set()
    name_to_source = {}
    for root, dirs, files in os.walk(vault_root):
        dirs[:] = [d for d in dirs if d not in {'.git', '.obsidian', '.trash', '.agents', '.kb', 'node_modules', '.claude'}]
        for fn in files:
            if fn.lower().endswith(IMAGE_EXT):
                all_names.add(fn)
                if fn not in name_to_source:
                    name_to_source[fn] = os.path.join(root, fn)
    return all_names, name_to_source

print("Building image index...")
all_names, name_to_source = build_vault_image_index()
all_names_lower = {n.lower() for n in all_names}
print(f"Vault images found: {len(all_names)}")

with open(excluded_json, 'r', encoding='utf-8') as f:
    excluded = json.load(f)

by_file = {}
for e in excluded:
    by_file.setdefault(e['source_file'], []).append(e)

files_changed = 0
rows_removed = 0
rows_fixed = 0

for source_file, items in by_file.items():
    filepath = os.path.join(vault_root, source_file)
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    new_lines = []
    changed = False
    
    for line in lines:
        stripped = line.strip()
        if not (stripped.startswith('|') and stripped.endswith('|')):
            new_lines.append(line)
            continue
            
        cols = [c.strip() for c in stripped.split('|')[1:-1]]
        if not cols:
            new_lines.append(line)
            continue
            
        col0 = cols[0]
        phys = col0.replace('![[', '').replace(']]', '').strip()
        
        # Match item
        matched_item = None
        for item in items:
            if item['physical_filename'] == phys:
                matched_item = item
                break
                
        if matched_item:
            reason = matched_item['reason']
            if reason == '截断无法唯一恢复':
                m = re.match(r'^([0-9a-fA-F]+)\.\.\.([0-9a-fA-F]*)(?:\.)?([a-zA-Z0-9]+)$', phys)
                if m:
                    prefix = m.group(1).lower()
                    suffix = m.group(2).lower()
                    ext = m.group(3).lower()
                    
                    matches = []
                    for n in all_names_lower:
                        if n.startswith(prefix) and n.endswith(suffix + '.' + ext):
                            matches.append(n)
                            
                    if len(matches) == 1:
                        full_name = matches[0]
                        new_col0 = col0.replace(phys, full_name)
                        line = line.replace(col0, new_col0)
                        
                        src_path = name_to_source.get(full_name)
                        dest_path = os.path.join(media_dir, full_name)
                        if src_path and not os.path.exists(dest_path):
                            shutil.copy2(src_path, dest_path)
                            print(f"  Copied {full_name} to media_dir")
                            
                        changed = True
                        rows_fixed += 1
                        print(f"Fixed truncated: {phys} -> {full_name} in {source_file}")
                        new_lines.append(line)
                        continue
                    elif len(matches) == 0:
                        print(f"Cannot uniquely resolve {phys} in {source_file} (matches: 0). Removing row.")
                        changed = True
                        rows_removed += 1
                        continue
                    else:
                        print(f"Cannot uniquely resolve {phys} in {source_file} (matches: {len(matches)})")
                        new_lines.append(line)
                        continue
                else:
                    print(f"Regex didn't match truncated form: {phys}")
            elif reason in ('非图片名/垃圾值', '全库无此文件'):
                print(f"Removing garbage/missing row: {phys} in {source_file}")
                changed = True
                rows_removed += 1
                continue
                
        new_lines.append(line)
        
    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        files_changed += 1

print(f"\nDone! Files changed: {files_changed}, Rows fixed: {rows_fixed}, Rows removed: {rows_removed}")
