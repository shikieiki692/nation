# -*- coding: utf-8 -*-
"""确凿非术语值清理：移除 frontmatter 中的题型标签/泛化占位值
原则：只删确凿非术语（阶段五口径），不碰真术语红链；改后 YAML 复验 + 空列表报警。"""
import os, re, sys, yaml

ROOT = r"C:\Obsidion\妙妙屋"
SKIP = {'.git', '.venv', 'node_modules', '.workbuddy', '99-归档', '09-审计报告',
        'kb-vault-mcp', '.obsidian', '_归档', '_archive_v2'}

# 确凿非术语值（阶段五口径：纯题型标签 / 泛化占位 / 自称占位）
BAD = {'选择题', '简答', '推断题', '命名题', '结构推断题', '化竞机理题', '化竞合成题',
       '综合', '综合分析', '跨章节综合', '有机化学综合', '磺化占位'}
FIELDS = ('knowledge_points', 'related', 'related_kp', 'related_notes')

changed = []   # (relpath, field, removed_values)
errors = []
empty_after = []  # (relpath, field)

def clean_flow_line(line):
    """flow 风格: key: ["[[a]]", "[[b]]"] — 删除 BAD 项"""
    m = re.match(r'^(\s*)([\w_]+):\s*(\[.*\])\s*$', line)
    if not m:
        return None
    indent, key, arr = m.groups()
    if key not in FIELDS:
        return None
    try:
        items = yaml.safe_load(arr)
    except Exception:
        return None
    if not isinstance(items, list):
        return None
    removed = []
    kept = []
    for it in items:
        s = str(it)
        name = re.sub(r'^\[\[|\]\]$', '', s.strip().strip('"\'')).split('|')[0].strip()
        if name in BAD:
            removed.append(name)
        else:
            kept.append(it)
    if not removed:
        return None
    if kept:
        newarr = '[' + ', '.join(f'"[[{str(k).strip(chr(34).strip())}]]"'
                                 if False else repr(k) for k in kept) + ']'
        # 保持双引号风格
        newarr = '[' + ', '.join('"[[' + re.sub(r'^\[\[|\]\]$', '', str(k).strip().strip('"\'')) + ']]"' for k in kept) + ']'
        return indent + key + ': ' + newarr, removed
    return indent + key + ': []', removed

for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in SKIP]
    for f in filenames:
        if not f.endswith('.md'):
            continue
        p = os.path.join(dirpath, f)
        try:
            lines = open(p, encoding='utf-8', newline='').read().splitlines(keepends=True)
        except Exception as e:
            errors.append((p, str(e))); continue
        # 定位 frontmatter 范围
        if not lines or lines[0].strip() != '---':
            continue
        try:
            end = next(i for i in range(1, len(lines)) if lines[i].strip() == '---')
        except StopIteration:
            continue
        fm_text = ''.join(lines[1:end])
        try:
            fm = yaml.safe_load(fm_text)
        except Exception as e:
            errors.append((p, f'YAML parse: {e}')); continue
        if not isinstance(fm, dict):
            continue
        # 预判：有哪些字段含 BAD 值
        targets = {}
        for field in FIELDS:
            v = fm.get(field)
            if v is None: continue
            vals = v if isinstance(v, list) else [v]
            hit = [str(x) for x in vals
                   if re.sub(r'^\[\[|\]\]$', '', str(x).strip().strip('"\'')).split('|')[0].strip() in BAD]
            if hit:
                targets[field] = hit
        if not targets:
            continue
        new_lines = []
        removed_here = {}
        for i, line in enumerate(lines):
            if 1 <= i < end:
                fl = clean_flow_line(line.rstrip('\r\n'))
                if fl is not None:
                    newline, removed = fl
                    eol = line[len(line.rstrip('\r\n')):]
                    new_lines.append(newline + eol)
                    removed_here.setdefault('flow', []).extend(removed)
                    continue
                bm = re.match(r'^(\s*-\s*)"?(\[\[)([^\]|\[#]+)(\]\])"?\s*$', line.rstrip('\r\n'))
                if bm and bm.group(3).strip() in BAD:
                    removed_here.setdefault('block', []).append(bm.group(3).strip())
                    continue  # 整行删除
            new_lines.append(line)
        if not removed_here:
            continue
        removed_all = removed_here.get('block', []) + removed_here.get('flow', [])
        # 与预判核对（统一剥 [[ ]] 与引号后比对）
        def norm(x):
            return re.sub(r'^\[\[|\]\]$', '', str(x).strip().strip('"\'')).split('|')[0].strip()
        expected = set().union(*[set(norm(v) for v in t) for t in targets.values()])
        if {norm(x) for x in removed_all} != expected:
            errors.append((p, f'移除集不符: 预判{expected} 实删{set(norm(x) for x in removed_all)}'))
            continue  # 不写入，人工复查
        # 校验改后 YAML
        try:
            end2 = next(i for i in range(1, len(new_lines)) if new_lines[i].strip() == '---')
            new_fm = yaml.safe_load(''.join(new_lines[1:end2]))
            if new_fm is None:
                raise ValueError('frontmatter 解析为空')
        except StopIteration:
            errors.append((p, '改后未找到 frontmatter 结束')); continue
        except Exception as e:
            errors.append((p, f'改后YAML异常: {e}')); continue
        for field in targets:
            v = new_fm.get(field)
            if v == [] or v is None:
                empty_after.append((p, field))
        with open(p, 'w', encoding='utf-8', newline='') as fh:
            fh.write(''.join(new_lines))
        changed.append((os.path.relpath(p, ROOT), targets, set(removed_all)))

print(f"改动文件: {len(changed)}")
for rel, t, r in changed:
    print(f"  {rel}: 移除 {sorted(r)} (字段 {list(t.keys())})")
print(f"\n空列表告警: {len(empty_after)}")
for rel, fld in empty_after:
    print(f"  {rel} -> {fld} 变空")
print(f"\n错误(未写入): {len(errors)}")
for rel, e in errors:
    print(f"  {rel}: {e}")
