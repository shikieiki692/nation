import os
import re
import shutil

vault_root = r'C:\Obsidion\妙妙屋'
ignore_dirs = {'.git', '.obsidian', '.trash', '.agents', '.kb', 'node_modules', '.claude'}
IMAGE_EXT = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tif', '.tiff')
media_dir = os.path.join(vault_root, '媒体仓库')

def is_image_name(name: str) -> bool:
    return name.lower().endswith(IMAGE_EXT)

def clean_phys(raw: str) -> str:
    name = raw.replace('![[', '').replace(']]', '').strip()
    m = re.search(r'([^/\\()]+\.(?:jpg|jpeg|png|gif|webp|bmp|tif|tiff))', name, re.IGNORECASE)
    return m.group(1) if m else name

def build_vault_image_index():
    all_names = set()
    name_to_source = {}
    for root, dirs, files in os.walk(vault_root):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for fn in files:
            if not is_image_name(fn):
                continue
            all_names.add(fn)
            if fn not in name_to_source:
                name_to_source[fn] = os.path.join(root, fn)
    return all_names, name_to_source

print("Building image index...")
all_names, name_to_source = build_vault_image_index()
all_names_lower = {n.lower() for n in all_names}
print(f"Vault images found: {len(all_names)}")

files_changed = 0
rows_fixed = 0
rows_failed = 0

for root, dirs, files in os.walk(vault_root):
    dirs[:] = [d for d in dirs if d not in ignore_dirs]
    if '_index.md' not in files:
        continue
        
    filepath = os.path.join(root, '_index.md')
    rel_src = os.path.relpath(filepath, vault_root).replace('\\', '/')
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"  [WARN] read {rel_src}: {e}")
        continue
        
    new_lines = []
    changed = False
    in_table = False
    headers = []
    
    for line in lines:
        stripped = line.strip()
        if not (stripped.startswith('|') and stripped.endswith('|')):
            new_lines.append(line)
            continue
            
        cols = [c.strip() for c in stripped.split('|')[1:-1]]
        if not in_table:
            if any(('文件名' in c or 'Quality' in c or '质量' in c) for c in cols):
                in_table = True
                headers = cols
                new_lines.append(line)
            else:
                new_lines.append(line)
            continue
            
        # Divider line
        if set(stripped.replace('|', '').replace('-', '').replace(' ', '')) == set():
            new_lines.append(line)
            continue
            
        if len(cols) < 2:
            new_lines.append(line)
            continue
            
        qual_idx = next((i for i, h in enumerate(headers) if '质量' in h or 'Quality' in h), -1)
        if qual_idx == -1 or qual_idx >= len(cols):
            new_lines.append(line)
            continue
            
        if 'HIGH' not in cols[qual_idx].upper():
            new_lines.append(line)
            continue
            
        raw = cols[0]
        phys = clean_phys(raw)
        
        if '...' in phys:
            m = re.match(r'^([0-9a-fA-F]+)\.\.\.([0-9a-fA-F]*)(?:\.)?([a-zA-Z0-9]+)$', phys)
            if m:
                prefix, suffix, ext = m.group(1).lower(), m.group(2).lower(), m.group(3).lower()
                matches = [n for n in all_names_lower if n.startswith(prefix) and n.endswith(suffix + '.' + ext)]
                if len(matches) == 1:
                    full_name = matches[0]
                    # Carefully replace just the phys string in the raw column text
                    new_col0 = raw.replace(phys, full_name)
                    line = line.replace(raw, new_col0)
                    
                    # Ensure it's in media repo too (optional but good)
                    src_path = name_to_source.get(full_name)
                    dest_path = os.path.join(media_dir, full_name)
                    if src_path and not os.path.exists(dest_path):
                        shutil.copy2(src_path, dest_path)
                        
                    changed = True
                    rows_fixed += 1
                    print(f"Fixed: {phys} -> {full_name} in {rel_src}")
                else:
                    rows_failed += 1
                    print(f"Failed to resolve uniquely (matches: {len(matches)}): {phys} in {rel_src}")
            else:
                rows_failed += 1
                print(f"Regex no match: {phys} in {rel_src}")
                
        new_lines.append(line)
        
    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        files_changed += 1

print(f"\nDone! Files changed: {files_changed}, Rows fixed: {rows_fixed}, Rows failed: {rows_failed}")
