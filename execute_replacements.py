import os, sys, json, shutil

sys.stdout.reconfigure(encoding='utf-8')
vault = r'c:\Obsidion\妙妙屋'
media_dir = os.path.join(vault, '媒体仓库')
if not os.path.exists(media_dir): os.makedirs(media_dir)

with open('match_results.json', 'r', encoding='utf-8') as f:
    results = json.load(f)

print(f'Starting execution for {len(results)} items.')

# Build a map of all physical images to speed up finding the source file
print('Scanning vault for physical image files...')
img_paths = {}
for root, dirs, files in os.walk(vault):
    if '.git' in root or '.gemini' in root: continue
    for file in files:
        if file.lower().endswith(('.jpg', '.png', '.jpeg')):
            # Key by hash name
            img_paths[file] = os.path.join(root, file)
print(f'Found {len(img_paths)} physical images.')

added_to_index = []

for k, v in results.items():
    target = v['target']
    match = v['match']
    good_hash = match['hash'] + '.' + match['ext']
    
    # 1. Ensure image is in 媒体仓库
    if good_hash not in img_paths:
        print(f'Warning: Could not find physical file for {good_hash}')
        continue
    
    source_img_path = img_paths[good_hash]
    target_img_path = os.path.join(media_dir, good_hash)
    
    if source_img_path != target_img_path:
        shutil.copy2(source_img_path, target_img_path)
    
    # 2. Update markdown file
    md_path = target['path']
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except: continue
    
    if target['type'] == 'revert':
        bad_hash = target['bad_hash']
        # Replace bad_hash.png or bad_hash.jpg with good_hash
        new_match = target['full_match'].replace(bad_hash + '.png', good_hash).replace(bad_hash + '.jpg', good_hash)
        content = content.replace(target['full_match'], new_match)
        
    elif target['type'] == 'missing':
        orig = target['full_match']
        new_text = orig.replace('📌 **图片待补', '*图').replace('）**：', ' ') + '*'
        if orig.startswith('> '):
            final_replacement = f'> ![[{good_hash}]]\n{new_text}'
        else:
            final_replacement = f'![[{good_hash}]]\n{new_text}'
        content = content.replace(orig, final_replacement)
        
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    # 3. Prepare index entry
    desc = target['desc'].replace('\n', ' ').replace('|', ' ')
    src_relative = os.path.relpath(match['source'], vault).replace('\\\\', '/')
    kws = ' '.join(v['kws'])
    
    detailed_desc = f'【OCR恢复】{desc} (来源文件: {src_relative})'
    row = f'| {good_hash} | {kws} | {detailed_desc} | 待补 | {src_relative} | ✅在媒体仓库 |\n'
    added_to_index.append(row)

# 4. Append to 全库核心图谱总索引.md
index_path = os.path.join(vault, r'10-索引与统计\全库核心图谱总索引.md')
with open(index_path, 'a', encoding='utf-8') as f:
    for row in added_to_index:
        f.write(row)

print(f'Successfully processed and added {len(added_to_index)} images to index.')
