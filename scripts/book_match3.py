import os, glob, re, difflib, io, sys

placeholders = []
with open('batch3_placeholders.txt', 'r', encoding='utf-8') as f:
    for line in f:
        if line.startswith('📌 **图片待补'):
            match = re.match(r'📌 \*\*图片待补（([^）]+)）\*\*：(.*)', line.strip())
            if match:
                placeholders.append({'desc': match.group(2), 'raw': line.strip()})

book_images = []
for file in glob.glob(r'c:\Obsidion\妙妙屋\07-资料提炼\书籍提炼\*.md'):
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            # match hash inside double brackets, ignoring paths
            img_match = re.search(r'!\[\[.*?([a-f0-9]{64,}\.(?:jpg|png))\]\]', line, re.IGNORECASE)
            if img_match:
                hash_name = img_match.group(1)
                context = ' '.join([l.strip() for l in lines[max(0, i-4):min(len(lines), i+5)]])
                book_images.append({'hash': hash_name, 'context': context, 'file': os.path.basename(file)})

def clean(s):
    return re.sub(r'[^\w\u4e00-\u9fa5A-Za-z0-9]', '', s).lower()

matches = []
for p in placeholders:
    p_clean = clean(p['desc'])
    best_img = None
    max_ratio = 0
    for img in book_images:
        i_clean = clean(img['context'])
        if not i_clean: continue
        
        # Exact figure number matching strongly preferred
        ratio = 0
        fig_match = re.search(r'图\s?(\d+\.\d+)', p['desc'])
        if fig_match:
            fig_str = "图" + fig_match.group(1).replace('.','')
            if fig_str in i_clean:
                ratio += 0.8
                
        # Find Longest Common Substring length / p_clean length
        s = difflib.SequenceMatcher(None, p_clean, i_clean)
        m = s.find_longest_match(0, len(p_clean), 0, len(i_clean))
        if len(p_clean) > 0:
            ratio += m.size / len(p_clean)
            
        if ratio > max_ratio:
            max_ratio = ratio
            best_img = img
    if max_ratio > 0.4:
        matches.append((p, best_img, max_ratio))

with open('book_matches.txt', 'w', encoding='utf-8') as f:
    f.write(f'Found {len(matches)} matches out of {len(placeholders)}\n')
    for p, img, r in matches:
        f.write(f"P: {p['desc']}\n")
        f.write(f"M: {img['context'][:150]}... (Ratio {r:.2f} in {img['file']})\n")
        f.write(f"Hash: {img['hash']}\n\n")
