# -*- coding: utf-8 -*-
"""列出 00-首页 所有 系统 页的 role+路径；并标非规范项"""
import io, os, re, collections
os.chdir(r'C:\Obsidion\妙妙屋')
from ruamel.yaml import YAML
y = YAML(typ='safe')
SKIP = ('归档', '_archive')
# 规范词表（含本轮新增 2）
SPEC = {'人工入口','人工导览','会话快照','执行聚合','方向指引','关系说明','执行协议',
        '标准作业流程','速查卡','任务调度参考','操作说明','工具说明','资源索引','日志索引',
        '方法论','历史缺口 / 监控','历史评估样例','维护备忘','规范词表','质量仪表','架构设计',
        '模块级连接推进','模块级连接覆盖','挂接度巡检','治理规划','会话交接','启动提示词'}
rows = []
for dp, dn, fn in os.walk('00-首页'):
    if '.git' in dp or any(s in dp for s in SKIP):
        continue
    for f in sorted(fn):
        if not f.endswith('.md'):
            continue
        p = os.path.join(dp, f).replace('\\', '/')
        t = io.open(p, encoding='utf-8-sig').read()
        m = re.match(r'^---\r?\n(.*?)\r?\n---(\r?\n|$)', t, re.S)
        if not m:
            continue
        d = y.load(m.group(1)) or {}
        if d.get('type') != '系统':
            continue
        rows.append((p.replace('00-首页/', ''), d.get('role')))

drift = collections.defaultdict(list)
for p, r in rows:
    if r not in SPEC:
        drift[r].append(p)
print('=== 非规范 role（%d 种 / %d 页）===' % (len(drift), sum(len(v) for v in drift.values())))
for r in sorted(drift, key=lambda x: (x is None, -len(drift[x]), str(x))):
    print('◆ role=%s (%d)' % (repr(r), len(drift[r])))
    for p in drift[r]:
        print('     ', p[:74])
print()
print('=== 非规范 type / 无 FM ===')
for dp, dn, fn in os.walk('00-首页'):
    if '.git' in dp or any(s in dp for s in SKIP):
        continue
    for f in sorted(fn):
        if not f.endswith('.md'):
            continue
        p = os.path.join(dp, f).replace('\\', '/')
        t = io.open(p, encoding='utf-8-sig').read()
        m = re.match(r'^---\r?\n(.*?)\r?\n---(\r?\n|$)', t, re.S)
        if not m:
            print('   无FM  ', p.replace('00-首页/', '')); continue
        d = y.load(m.group(1)) or {}
        if d.get('type') not in ('系统','活跃任务卡','工作日志'):
            print('   非规范type=%s  %s' % (d.get('type'), p.replace('00-首页/', '')))
