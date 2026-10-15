# -*- coding: utf-8 -*-
"""枚举 02-数据库/06-学生侧材料/备课思路/10-索引与统计 的系统层页 + role 现状"""
import io, os, re, collections
os.chdir(r'C:\Obsidion\妙妙屋')
from ruamel.yaml import YAML
y = YAML(typ='safe')
SPEC = {'人工入口','人工导览','会话快照','执行聚合','方向指引','关系说明','执行协议','标准作业流程',
        '速查卡','任务调度参考','操作说明','工具说明','资源索引','日志索引','方法论','历史缺口 / 监控',
        '历史评估样例','维护备忘','规范词表','质量仪表','架构设计','模块级连接推进','模块级连接覆盖',
        '挂接度巡检','治理规划','会话交接','启动提示词'}
FOLDERS = ['02-数据库', '06-学生侧材料', '备课思路', '10-索引与统计']
SYSNAME = re.compile(r'(README|索引|总入口|导航)')
def rd(p): return io.open(p, encoding='utf-8-sig').read()
cand, role_drift = [], []
for T in FOLDERS:
    if not os.path.isdir(T):
        continue
    for dp, dn, fn in os.walk(T):
        if '.git' in dp or '归档' in dp or '_archive' in dp:
            continue
        for f in sorted(fn):
            if not f.endswith('.md'):
                continue
            p = os.path.join(dp, f).replace('\\', '/')
            t = rd(p); m = re.match(r'^---\r?\n(.*?)\r?\n---(\r?\n|$)', t, re.S)
            if not m:
                if SYSNAME.search(f):
                    cand.append((p, '(无FM)', None)); continue
                continue
            d = y.load(m.group(1)) or {}
            ty, r = d.get('type'), d.get('role')
            if SYSNAME.search(f):
                if ty != '系统' or r not in SPEC:
                    cand.append((p, ty, r))
            elif ty == '系统' and r not in SPEC:
                role_drift.append((p, ty, r))
print('=== A. 系统层候选页（文件名含 README/索引/总入口/导航，且 type≠系统 或 role 非规范）：%d ===' % len(cand))
for p, ty, r in cand:
    print('   %-52s type=%-8s role=%s' % (p[:52], ty, r))
print()
print('=== B. 其它「系统」页但 role 漂移：%d ===' % len(role_drift))
for p, ty, r in role_drift:
    print('   %-52s role=%s' % (p[:52], r))
