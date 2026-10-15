# -*- coding: utf-8 -*-
"""全库 type=系统 页的 role 盘点（只读）：找漂移 role"""
import io, os, re, collections
os.chdir(r'C:\Obsidion\妙妙屋')
from ruamel.yaml import YAML
y = YAML(typ='safe')

# 规范 §三 词表（26）+ 本会话新增 2
SPEC = {
 '人工入口','人工导览','会话快照','执行聚合','方向指引','关系说明','执行协议','标准作业流程',
 '速查卡','任务调度参考','操作说明','工具说明','资源索引','日志索引','方法论','历史缺口 / 监控',
 '历史评估样例','维护备忘','规范词表','质量仪表','架构设计','模块级连接推进','模块级连接覆盖',
 '挂接度巡检','治理规划','会话交接','启动提示词',
}

by_dir = collections.defaultdict(lambda: {'n':0,'no_role':0,'drift':collections.Counter()})
drift_files = collections.defaultdict(list)
for dp, dn, fn in os.walk('.'):
    if dp.startswith('./.git') or dp.startswith('./.workbuddy'):
        continue
    if '_归档' in dp or '_archive' in dp or '归档' in dp:
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
            continue
        if d.get('type') != '系统':
            continue
        top = p.replace('\\','/').split('/')[1] if p.startswith('./') else p.replace('\\','/').split('/')[0]
        top = p.replace('\\','/').replace('./','').split('/')[0]
        if top == '00-首页':
            continue   # 已收口
        by_dir[top]['n'] += 1
        r = d.get('role')
        if not r:
            by_dir[top]['no_role'] += 1
            drift_files[top].append((p.replace('\\','/'), '(缺 role)'))
        elif r not in SPEC:
            by_dir[top]['drift'][r] += 1
            drift_files[top].append((p.replace('\\','/'), r))

print('=== 00-首页 之外 的 type=系统 页 ===')
tot_n = tot_nr = tot_d = 0
for T in sorted(by_dir):
    v = by_dir[T]
    nd = sum(v['drift'].values())
    tot_n += v['n']; tot_nr += v['no_role']; tot_d += nd
    if v['n'] == 0:
        continue
    print('  ◆ %-20s 系统页 %-4d ｜ 缺role %-3d ｜ role漂移 %-3d' % (T, v['n'], v['no_role'], nd))
    for k, c in v['drift'].most_common():
        print('        ⚠️ %-22s %d' % (k, c))
print()
print('合计：系统页 %d ｜ 缺 role %d ｜ role 漂移 %d' % (tot_n, tot_nr, tot_d))
print()
print('=== 待改文件清单 ===')
for T in sorted(drift_files):
    if not drift_files[T]:
        continue
    print('◆', T)
    for p, r in drift_files[T]:
        print('   [%s] %s' % (r, p[:88]))
