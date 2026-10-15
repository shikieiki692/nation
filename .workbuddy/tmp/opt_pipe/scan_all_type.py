# -*- coding: utf-8 -*-
"""全库 type / role 盘点（只读）：找 00-首页 与既有 4 目录之外的漂移"""
import io, os, re, collections
os.chdir(r'C:\Obsidion\妙妙屋')
from ruamel.yaml import YAML
y = YAML(typ='safe')

SPEC_TYPE = {'系统', '活跃任务卡', '工作日志'}
TOPDIRS = []
for d in sorted(os.listdir('.')):
    if os.path.isdir(d) and not d.startswith('.') and d not in ('媒体仓库',):
        TOPDIRS.append(d)

# 各顶层目录的 type 分布
print('=== 各顶层目录 type 分布（仅列有 FM 的 md）===')
for T in TOPDIRS:
    cnt = collections.Counter()
    for dp, dn, fn in os.walk(T):
        if '.git' in dp or '_归档' in dp or '_archive' in dp or '归档' in dp:
            continue
        for f in fn:
            if not f.endswith('.md'):
                continue
            p = os.path.join(dp, f)
            try:
                t = io.open(p, encoding='utf-8-sig', errors='replace').read()
            except Exception:
                continue
            m = re.match(r'^---\r?\n(.*?)\r?\n---(\r?\n|$)', t, re.S)
            if not m:
                continue
            try:
                d = y.load(m.group(1)) or {}
            except Exception:
                cnt['(FM解析失败)'] += 1
                continue
            cnt[d.get('type')] += 1
    if not cnt:
        continue
    tot = sum(cnt.values())
    bad = {k: v for k, v in cnt.items() if k not in SPEC_TYPE}
    nbad = sum(bad.values())
    print('  ◆ %-22s 有FM %-5d ｜ 非规范 %-5d' % (T, tot, nbad))
    for k, v in cnt.most_common(6):
        mark = ' ' if k in SPEC_TYPE else '⚠️'
        print('        %s %-18s %d' % (mark, repr(k), v))
