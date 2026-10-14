# -*- coding: utf-8 -*-
r"""独立复核：图升级线替换的图是否被任何已交付卷引用（只读）。"""
import json, io, os, re
os.chdir(r'C:\Obsidion\妙妙屋')
p = '04-题库/2026机构初赛模拟题/chemy/_图片升级清单-2026-10-14.json'
d = json.load(io.open(p, encoding='utf-8'))
print('counts:', json.dumps(d.get('counts'), ensure_ascii=False))
rep = d.get('replaced') or []
print('replaced 条数:', len(rep))
print('首项样例:', json.dumps(rep[0], ensure_ascii=False)[:260] if rep else '(空)')

# 抽出被替换的图名（兼容多种键名）
names = set()
for it in rep:
    if isinstance(it, dict):
        for k in ('lib_img', 'new', 'file', 'name', 'img', 'path', 'dst', 'to', 'after'):
            v = it.get(k)
            if isinstance(v, str):
                names.add(os.path.basename(v)); break
    elif isinstance(it, str):
        names.add(os.path.basename(it))
print('提取到图名 %d 个；样例:' % len(names), list(names)[:3])

# 各卷引用
print()
print('=== 交叉：被替换图 ∩ 各卷引用 ===')
total_hit = 0
for V in ['X', 'XI', 'XIp', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII']:
    for tag in ['学生版', '答案版']:
        md = '04-题库/初赛模拟卷%s（非有机·%s）.md' % (V, tag)
        if not os.path.isfile(md):
            continue
        t = io.open(md, encoding='utf-8-sig').read()
        refs = {os.path.basename(m.group(1)) for m in re.finditer(r'!\[\[([^\]]+)\]\]', t)}
        hit = refs & names
        if hit:
            total_hit += len(hit)
            print('  🔴 %s %s：命中 %d 张' % (V, tag, len(hit)))
            for h in sorted(hit)[:5]:
                print('       ', h[:56])
print('合计命中 %d' % total_hit)
print('VERDICT:', 'FAIL（有卷受影响）' if total_hit else 'PASS（无卷引用被替换图，与并行会话结论一致）')
