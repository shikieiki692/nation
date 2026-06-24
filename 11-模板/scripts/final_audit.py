import os, re, json

vault = r'C:\Obsidion\妙妙屋'
checks = []

P = "[OK]"
F = "[XX]"

# 1. Canvas file validation
print("=== 1. Canvas file ===")
with open(os.path.join(vault, '00-首页', '系统架构图.canvas'), 'r', encoding='utf-8') as f:
    canvas = json.load(f)
nodes = canvas.get('nodes', [])
edges = canvas.get('edges', [])
print("  nodes=" + str(len(nodes)) + " edges=" + str(len(edges)))
node_ids = set(n['id'] for n in nodes)
broken = 0
for e in edges:
    if e['fromNode'] not in node_ids:
        print("  " + F + " fromNode missing")
        broken += 1
    if e['toNode'] not in node_ids:
        print("  " + F + " toNode missing")
        broken += 1
s = P if broken == 0 else F
print("  " + s + " edges=" + str(len(edges)) + " broken=" + str(broken))
checks.append(('Canvas', s))

# 2. validate_kb.py functions
print("\n=== 2. validate_kb.py ===")
fp = os.path.join(vault, '11-模板', 'scripts', 'validate_kb.py')
with open(fp, 'r', encoding='utf-8') as f:
    content = f.read()
functions = re.findall(r'^def (\w+)', content, re.MULTILINE)
print("  functions: " + str(len(functions)))
for rf in ['find_wikilink_target', 'check_lifecycle', 'build_filename_index']:
    ok = rf in functions
    print("  " + (P if ok else F) + " " + rf)
    checks.append(('validate_kb.' + rf, P if ok else F))

# 3. quality-metrics.jsonl
print("\n=== 3. quality-metrics.jsonl ===")
fp = os.path.join(vault, '02-数据库', 'quality-metrics.jsonl')
with open(fp, 'r', encoding='utf-8') as f:
    lines = [l.strip() for l in f if l.strip()]
valid = sum(1 for l in lines if json.loads(l) or True)
# actually validate
valid = 0
for l in lines:
    try:
        json.loads(l)
        valid += 1
    except:
        pass
s = P if valid == len(lines) else F
print("  " + s + " " + str(valid) + "/" + str(len(lines)) + " valid")
checks.append(('metrics.jsonl', s))

# 4. dependency-map.json
print("\n=== 4. dependency-map.json ===")
fp = os.path.join(vault, '02-数据库', 'dependency-map.json')
with open(fp, 'r', encoding='utf-8') as f:
    depmap = json.load(f)
entries = len(depmap)
with_refs = sum(1 for v in depmap.values() if v.get('referenced_by'))
print("  " + P + " entries=" + str(entries) + " with_refs=" + str(with_refs))
checks.append(('dep-map', P + " " + str(entries) + " entries"))

# 5. Stage coverage
print("\n=== 5. Stage coverage ===")
total = 0
with_stage = 0
missing = []
for root, dirs, files in os.walk(os.path.join(vault, '03-知识点')):
    for f in files:
        if not f.endswith('.md'): continue
        if '.excalidraw' in f or f == '知识点.md': continue
        total += 1
        fp = os.path.join(root, f)
        with open(fp, 'r', encoding='utf-8') as fh:
            if re.search(r'^stage:', fh.read(), re.MULTILINE):
                with_stage += 1
            else:
                missing.append(os.path.relpath(fp, vault))
pct = with_stage / total * 100 if total > 0 else 0
s = P if len(missing) == 0 else F
print("  " + s + " " + str(with_stage) + "/" + str(total) + " (" + "{:.1f}%)".format(pct))
for m in missing:
    print("  " + F + " " + m)
checks.append(('stage coverage', s + " " + str(with_stage) + "/" + str(total)))

# 6. Templates
print("\n=== 6. Templates ===")
for tf in ['模板-知识点.md', '模板-学生讲义.md']:
    fp = os.path.join(vault, '11-模板', tf)
    with open(fp, 'r', encoding='utf-8') as fh:
        content = fh.read()
    ok = 'stage: draft' in content
    print("  " + (P if ok else F) + " " + tf)
    checks.append(('template.' + tf, P if ok else F))

# 7. Protocol
print("\n=== 7. Protocol ===")
fp = os.path.join(vault, '00-首页', 'Agent最小执行协议.md')
with open(fp, 'r', encoding='utf-8') as fh:
    content = fh.read()
for kw in ['STEP -1', '开工前健康检查', '质量看板', '收工清单', '自动化验证', 'validate_kb.py']:
    ok = kw in content
    print("  " + (P if ok else F) + " " + kw)
    checks.append(('protocol.' + kw, P if ok else F))

# 8. Cross-refs
print("\n=== 8. Cross-refs ===")
xrefs = [
    ('状态摘要.md', '质量看板'),
    ('活跃任务.md', '质量看板'),
    ('系统架构图.canvas', '入口层'),
    ('系统架构图.canvas', '自动化管道'),
]
for path, keyword in xrefs:
    fp = os.path.join(vault, '00-首页', path)
    with open(fp, 'r', encoding='utf-8') as fh:
        ok = keyword in fh.read()
    print("  " + (P if ok else F) + " " + path + " -> " + keyword)
    checks.append(('xref.' + keyword, P if ok else F))

# Summary
print("\n" + "=" * 50)
print("FINAL AUDIT SUMMARY")
print("=" * 50)
all_ok = True
for name, status in checks:
    ok = P in status
    if not ok: all_ok = False
    print("  " + status + " " + name)
print("\nRESULT: " + ("ALL PASS" if all_ok else "SOME FAILED"))
