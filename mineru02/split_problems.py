import re
import os
import shutil

with open('mineru02/第39届化学竞赛决赛第1场试题答案.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Split by '# 第 N 题' patterns, keeping the delimiter
pattern = r'(?=# 第\s*\d+\s*题)'
parts = re.split(pattern, content)
parts = [p.strip() for p in parts if p.strip()]

print(f'Total parts: {len(parts)}')
for i, p in enumerate(parts):
    first_line = p.split('\n')[0][:80]
    print(f'{i}: {first_line}')

# Extract problem info
problems = []
for p in parts:
    m = re.match(r'# 第\s*(\d+)\s*题\s+(.+?)\s*\((\d+)\s*分\)', p)
    if m:
        num = int(m.group(1))
        title = m.group(2).strip()
        score = int(m.group(3))
        problems.append({
            'num': num,
            'title': title,
            'score': score,
            'content': p
        })
        print(f"Found: 第{num}题 {title} ({score}分)")
    else:
        # Try alternate format
        m2 = re.match(r'# 第\s*(\d+)\s*题\s+(.+?)\s*\(共?(\d+)\s*分\)', p)
        if m2:
            num = int(m2.group(1))
            title = m2.group(2).strip()
            score = int(m2.group(3))
            problems.append({
                'num': num,
                'title': title,
                'score': score,
                'content': p
            })
            print(f"Found alt: 第{num}题 {title} ({score}分)")
        else:
            first_line = p.split('\n')[0][:80]
            print(f"No match: {first_line}")

print(f"\nTotal problems found: {len(problems)}")

# Save problem metadata
import json
with open('mineru02/problems_meta.json', 'w', encoding='utf-8') as f:
    json.dump([{'num': p['num'], 'title': p['title'], 'score': p['score']} for p in problems], f, ensure_ascii=False, indent=2)
