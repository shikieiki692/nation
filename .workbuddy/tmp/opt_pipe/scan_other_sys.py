# -*- coding: utf-8 -*-
"""扫描 00-首页 之外的「系统层」区域（02-数据库/06-学生侧材料/备课思路等）type 漂移"""
import io, os, re, collections
os.chdir(r'C:\Obsidion\妙妙屋')
from ruamel.yaml import YAML
y = YAML(typ='safe')
TARGETS = ['02-数据库', '06-学生侧材料', '备课思路', '01-备课', '10-索引与统计']
print('=== 顶层目录 ===')
tops = sorted(d for d in os.listdir('.') if os.path.isdir(d) and not d.startswith('.') and d != '.git')
print('  ', tops)
print()
for T in TARGETS:
    if not os.path.isdir(T):
        print('◆ %s —— 不存在' % T); continue
    cnt = collections.Counter(); files = []
    for dp, dn, fn in os.walk(T):
        if '.git' in dp or '归档' in dp or '_archive' in dp:
            continue
        for f in sorted(fn):
            if not f.endswith('.md'):
                continue
            p = os.path.join(dp, f).replace('\\', '/')
            t = io.open(p, encoding='utf-8-sig').read()
            m = re.match(r'^---\r?\n(.*?)\r?\n---(\r?\n|$)', t, re.S)
            if not m:
                cnt['(无FM)'] += 1; continue
            d = y.load(m.group(1)) or {}
            ty = d.get('type'); cnt[ty] += 1
            files.append((p, ty, d.get('role')))
    print('◆ %s（%d md）' % (T, sum(cnt.values())))
    for k, v in cnt.most_common(12):
        print('     %-16s %d' % (repr(k), v))
    # 疑似入口/索引页（含 索引/README/总览/说明/导航）
    suspects = [(p, ty, r) for p, ty, r in files if re.search(r'(索引|README|总览|说明|导航|入口|规范|指南)', p)]
    if suspects:
        print('     --- 疑似入口/索引页 ---')
        for p, ty, r in suspects[:25]:
            print('        %-52s type=%s role=%s' % (p[:52], ty, r))
    print()
