import os, re, json, hashlib, shutil

vault_root = r'C:\Obsidion\妙妙屋'
media_dir = os.path.join(vault_root, '媒体仓库')
report_path = os.path.join(vault_root, '09-审计报告', 'auto-validation', '2026-08-05-validation.md')
todo_list = os.path.join(vault_root, '00-首页', '活跃任务', '图片剩余待手绘清单.md')

def calculate_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

# 1. build global file map
ignore_dirs = {'.git', '.obsidian', '.trash', '.agents', '.kb', 'node_modules', '.claude'}
all_files_map = {}
for root, dirs, files in os.walk(vault_root):
    dirs[:] = [d for d in dirs if d not in ignore_dirs]
    for fn in files:
        if fn.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tif', '.tiff')):
            if fn not in all_files_map:
                all_files_map[fn] = []
            all_files_map[fn].append(os.path.join(root, fn))

# 2. Extract errors from validation report
errors = []
with open(report_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

in_missing = False
for line in lines:
    line_s = line.strip()
    if line_s.startswith('**图片缺失**'):
        in_missing = True
        continue
    if in_missing and line_s.startswith('**'):
        break
    if in_missing and line_s.startswith('- `'):
        m = re.search(r"- `([^`]+)` → (.*?) →", line_s)
        if m:
            md_rel = m.group(1).strip()
            link_text = m.group(2).strip()
            errors.append((md_rel, link_text))

print(f"Extracted {len(errors)} missing images from report.")

# 3. Process errors
resolved_count = 0
unresolved = []
new_media = []

for md_rel, link_text in errors:
    md_abs = os.path.join(vault_root, md_rel)
    if not os.path.exists(md_abs):
        print(f"File not found: {md_abs}")
        continue
    
    # parse link
    m_link = re.search(r'!\[\[(.*?)\]\]', link_text)
    if not m_link:
        m_link = re.search(r'!\[.*?\]\((.*?)\)', link_text)
    
    if not m_link:
        continue
    
    inner_link = m_link.group(1).split('|')[0].split('#')[0]
    basename = os.path.basename(inner_link)
    
    # find where this file actually is
    actual_path = None
    
    # First check if it's already in media_dir under the basename
    if os.path.exists(os.path.join(media_dir, basename)):
        actual_path = os.path.join(media_dir, basename)
    else:
        # Check if we can find it in the global map
        candidates = all_files_map.get(basename, [])
        if len(candidates) > 0:
            # prefer ones not in .trash
            valid_candidates = [c for c in candidates if '.trash' not in c]
            if valid_candidates:
                actual_path = valid_candidates[0]

    if not actual_path:
        # Check if inner_link is an absolute/relative path within vault that exists
        p = os.path.normpath(os.path.join(vault_root, inner_link))
        if os.path.exists(p) and os.path.isfile(p):
            actual_path = p
    
    with open(md_abs, 'r', encoding='utf-8') as f:
        content = f.read()

    if actual_path:
        # We found the physical file!
        hash_val = calculate_sha256(actual_path)
        ext = os.path.splitext(actual_path)[1]
        new_name = f"{hash_val}{ext}"
        new_dest = os.path.join(media_dir, new_name)
        
        if not os.path.exists(new_dest):
            shutil.copy2(actual_path, new_dest)
            new_media.append((basename, new_name))
        
        new_link_text = f"![[{new_name}]]"
        content = content.replace(link_text, new_link_text)
        resolved_count += 1
    else:
        # True missing file -> placeholder
        placeholder = f"📌 **图片待补：** {basename}"
        content = content.replace(link_text, placeholder)
        unresolved.append((md_rel, basename, link_text))
        resolved_count += 1

    with open(md_abs, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Processed {resolved_count}/{len(errors)} items.")

# 4. Record true missing files
if unresolved:
    with open(todo_list, 'r', encoding='utf-8') as f:
        todo_content = f.read()
    
    to_append = []
    for md_rel, basename, orig_link in unresolved:
        to_append.append(f"- **文件**: [[{os.path.basename(md_rel)}]]")
        to_append.append(f"  - **内容**: {basename} (缺图 86 修复扫尾)")
        to_append.append(f"  - **原文**: `{orig_link}`\n")
    
    with open(todo_list, 'a', encoding='utf-8') as f:
        f.write('\n' + '\n'.join(to_append))
    print(f"Appended {len(unresolved)} items to todo list.")

# 5. Output newly copied media for index script to pick up
if new_media:
    out_map = r'c:\Obsidion\妙妙屋\10-索引与统计\修复缺失图片_映射.json'
    mapping = {}
    for old, new in new_media:
        mapping[old] = {"hash": new, "status": "ok"}
    
    with open(out_map, 'w', encoding='utf-8') as f:
        json.dump({"mapping": mapping}, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(new_media)} new media mappings.")
