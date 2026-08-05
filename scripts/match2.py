import sys; import io; sys.stdout = io.TextIOWrapper(open('matches_out.txt', 'wb'), encoding='utf-8')
import re
import difflib
import json
import os

def clean(s):
    return re.sub(r'[^\w\u4e00-\u9fa5A-Za-z0-9]', '', s).lower()

with open('batch3_placeholders.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

placeholders = {}
current = ""
for line in lines:
    if line.startswith('===') and line.endswith('===\n'):
        current = line.replace('===', '').strip().split(' (')[0]
        placeholders[current] = []
    elif line.startswith('📌 **图片待补'):
        match = re.match(r'📌 \*\*图片待补（([^）]+)）\*\*：(.*)', line.strip())
        if match:
            placeholders[current].append({'id': match.group(1), 'desc': match.group(2), 'raw': line.strip()})

images = []
with open(r'c:\Obsidion\妙妙屋\10-索引与统计\全库核心图谱总索引.md', 'r', encoding='utf-8') as f:
    for line in f:
        if line.strip().startswith('|') and len(line.split('|')) >= 5:
            parts = [p.strip() for p in line.split('|')]
            if len(parts[1]) >= 64:
                images.append({
                    'hash': parts[1], 
                    'text': parts[3],
                    'subject': parts[4],
                    'source': parts[5] if len(parts)>5 else ''
                })

for fname, items in placeholders.items():
    print(f"\n--- {fname} ---")
    for p in items:
        p_clean = clean(p['desc'])
        best = None
        max_ratio = 0
        
        for img in images:
            i_clean = clean(img['text'])
            # We want to know if the placeholder text is a subset of the image text or vice-versa
            # Use difflib.SequenceMatcher ratio on a sliding window or simply sequence matcher
            s = difflib.SequenceMatcher(None, p_clean, i_clean)
            # find longest common substring
            match = s.find_longest_match(0, len(p_clean), 0, len(i_clean))
            ratio = match.size / min(len(p_clean), len(i_clean)) if min(len(p_clean), len(i_clean)) > 0 else 0
            
            # Boost if English terms like "Weller", "Keggin", "Frost", "Latimer", "O2" match
            eng_p = set(re.findall(r'[A-Za-z0-9]+', p['desc']))
            eng_i = set(re.findall(r'[A-Za-z0-9]+', img['text'] + ' ' + img['source']))
            if eng_p and eng_p.intersection(eng_i):
                ratio += 0.5 * len(eng_p.intersection(eng_i)) / len(eng_p)
                
            if ratio > max_ratio:
                max_ratio = ratio
                best = img
                
        if max_ratio > 0.4:
            print(f"P: {p['desc'][:50]}...")
            print(f"M: {best['text'][:60]}... (Ratio: {max_ratio:.2f})")
        else:
            print(f"P: {p['desc'][:50]}...")
            print(f"M: [NO GOOD MATCH] (Best was {best['text'][:30]}... Ratio {max_ratio:.2f})")
