import os
import re
import shutil

vault_root = r'C:\Obsidion\妙妙屋'
media_dir = os.path.join(vault_root, '媒体仓库')
ignore_dirs = {'.git', '.obsidian', '.trash', '.agents', '.kb', 'node_modules', '.claude'}

# 1. Build a map of ALL images in the vault
all_images = {}
for root, dirs, files in os.walk(vault_root):
    dirs[:] = [d for d in dirs if d not in ignore_dirs]
    for fn in files:
        if fn.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tif', '.tiff')):
            all_images[fn] = os.path.join(root, fn)

# 2. Check all markdown files for missing links
missing_links = []
md_files = []
for root, dirs, files in os.walk(vault_root):
    dirs[:] = [d for d in dirs if d not in ignore_dirs]
    for fn in files:
        if fn.endswith('.md'):
            md_files.append(os.path.join(root, fn))

link_pattern = re.compile(r'!\[.*?\]\((.*?)\)|!\[\[(.*?)\]\]')

for md_path in md_files:
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        continue
        
    for m in link_pattern.finditer(content):
        # markdown links or wikilinks
        link = m.group(1) if m.group(1) else m.group(2)
        if not link: continue
        
        # clean link (remove # headers or | sizes)
        link = link.split('#')[0].split('|')[0]
        link = os.path.basename(link) # just the filename
        
        if not link.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tif', '.tiff')):
            continue
            
        # Check if it exists in media_dir
        expected_path = os.path.join(media_dir, link)
        if not os.path.exists(expected_path):
            missing_links.append({
                'md_path': md_path,
                'link': link,
                'full_match': m.group(0)
            })

print(f"Found {len(missing_links)} missing image references.")
for m in missing_links[:10]:
    print(f"{os.path.relpath(m['md_path'], vault_root)}: {m['link']}")
