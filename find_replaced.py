import os, re, sys, json
sys.stdout.reconfigure(encoding='utf-8')

notes_dir = r'c:\Obsidion\妙妙屋\04-课件\学生讲义'
targets = [
    '物化综合计算', '真题模拟拆解', '胶体与表面', '统计热力学与Maxwell',
    '有效数字与误差分析',
    '氧族与氮族元素', '碱金属碱土金属与稀有气体', '碳族与硼族元素', '钛钒铬锰', '铁钴镍铜锌', '银金汞钼钨', '元素化学深度', '元素推断综合训练'
]

results = []

for root, dirs, files in os.walk(notes_dir):
    for file in files:
        if not file.endswith('.md'): continue
        if not any(t in file for t in targets): continue
        path = os.path.join(root, file)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
        except: continue
        
        matches = re.finditer(r'(> )?!\[\[([a-f0-9]{64})\.(png|jpg)\]\]\n(> )?\*图(.*?)\*：(.*)', content)
        for m in matches:
            results.append({
                'file': file,
                'path': path,
                'hash': m.group(2),
                'ext': m.group(3),
                'caption': m.group(5).strip(),
                'desc': m.group(6).strip(),
                'full': m.group(0)
            })

print(f'Total found replaced pictures: {len(results)}')
with open('replaced_pics.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
