# -*- coding: utf-8 -*-
"""role 归一（35 漂移→规范）＋ 会话类小项；dry/apply"""
import io, os, re, sys, shutil, datetime
os.chdir(r'C:\Obsidion\妙妙屋')
APPLY = '--apply' in sys.argv
from ruamel.yaml import YAML
y = YAML(typ='safe')
SKIP = ('归档', '_archive')

MAP = {
 '执行计划': '治理规划', '活跃任务': '启动提示词', '自动库存汇总': '质量仪表',
 'SOP': '标准作业流程', 'Word讲义入口说明': '工具说明', '交接': '会话交接',
 '任务分类与依赖总图': '任务调度参考', '任务聚合': '执行聚合', '会话交接说明': '会话交接',
 '入库规范': '规范词表', '全库目录导航': '人工导览', '内容建设清单': '历史缺口 / 监控',
 '图片索引总入口': '资源索引', '工作流程': '方法论', '待办聚合': '执行聚合',
 '指标事实源': '质量仪表', '提示词': '启动提示词', '教学洞察批量生产': '启动提示词',
 '教材提炼状态追踪': '资源索引', '日志': '日志索引', '架构参考': '架构设计',
 '治理待办': '治理规划', '用户提示模板': '启动提示词', '系统连接总表': '模块级连接覆盖',
 '缺口登记 / 计划': '历史缺口 / 监控', '自动任务摘要': '质量仪表', '自动任务检查': '质量仪表',
 '自动审计摘要': '质量仪表', '自动异常巡检': '质量仪表', '自动汇总说明': '质量仪表',
 '自动版本汇总': '质量仪表', '角色索引': '规范词表', '讲义质量政策': '规范词表',
 '过程建模': '方法论', '配图政策': '规范词表',
}
# 会话类小项（未跟踪孤儿 → 补/改 FM 后入库）
OUTLIERS = {
 '00-首页/活跃任务/计划-2026-10-14-chemy全量对账与补录.md': ('系统', '治理规划'),
 '00-首页/活跃任务/交接提示词-2026-10-03-chemy-P1决赛两场与后续批次.md': ('系统', '启动提示词'),
}

def rd(p): return io.open(p, encoding='utf-8-sig').read()
def getfm(t):
    m = re.match(r'^---\r?\n(.*?)\r?\n---(\r?\n|$)', t, re.S)
    return (m.group(1), t[m.end():], m) if m else (None, t, None)

rolefix, outfix = [], []
for dp, dn, fn in os.walk('00-首页'):
    if '.git' in dp or any(s in dp for s in SKIP):
        continue
    for f in sorted(fn):
        if not f.endswith('.md'):
            continue
        p = os.path.join(dp, f).replace('\\', '/')
        t = rd(p); s, body, m = getfm(t)
        if s is None:
            continue
        d = y.load(s) or {}
        if d.get('type') == '系统' and d.get('role') in MAP:
            rolefix.append((p, d.get('role'), MAP[d['role']]))
for p, (ty, r) in OUTLIERS.items():
    if os.path.exists(p):
        t = rd(p); s, body, m = getfm(t)
        cur = (y.load(s) or {}).get('type') if s else None
        outfix.append((p, cur, ty, r, s is not None))

print('=== ① role 归一：%d 页 ===' % len(rolefix))
for p, a, b in rolefix:
    print('   %-58s %s → %s' % (p.replace('00-首页/', '')[:58], a, b))
print()
print('=== ② 会话类小项：%d ===' % len(outfix))
for p, cur, ty, r, hasfm in outfix:
    print('   %-58s (type=%s→%s, role=%s, 有FM=%s)' % (p.replace('00-首页/', '')[:58], cur, ty, r, hasfm))
if not APPLY:
    print('\n（dry-run，未写盘）'); sys.exit(0)

bak = '.workbuddy/tmp/opt_pipe/_bak/roleuni_%s' % datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
os.makedirs(bak, exist_ok=True); n = 0
for p, a, b in rolefix:
    shutil.copy2(p, os.path.join(bak, os.path.basename(p)))
    t = rd(p); s, body, m = getfm(t)
    nl = '\r\n' if '\r\n' in t[:m.end()] else '\n'
    ns = re.sub(r'^role:[ \t]*.*$', 'role: ' + b, s, count=1, flags=re.M)
    io.open(p, 'w', encoding='utf-8', newline='').write('---' + nl + ns + nl + '---' + nl + body); n += 1
for p, cur, ty, r, hasfm in outfix:
    shutil.copy2(p, os.path.join(bak, os.path.basename(p)))
    t = rd(p); s, body, m = getfm(t)
    if hasfm:
        nl = '\r\n' if '\r\n' in t[:m.end()] else '\n'
        if re.search(r'^type:', s, re.M):
            s = re.sub(r'^type:[ \t]*.*$', 'type: ' + ty, s, count=1, flags=re.M)
        else:
            s = 'type: ' + ty + nl + s
        if re.search(r'^role:', s, re.M):
            s = re.sub(r'^role:[ \t]*.*$', 'role: ' + r, s, count=1, flags=re.M)
        else:
            s = s + nl + 'role: ' + r
    else:
        nl = '\n'
        h1 = next((l[2:].strip() for l in body.split('\n') if l.startswith('# ')), os.path.basename(p)[:-3])
        s = nl.join(['title: ' + h1, 'type: ' + ty, 'role: ' + r])
        body = nl + body
    io.open(p, 'w', encoding='utf-8', newline='').write('---' + nl + s + nl + '---' + nl + body); n += 1
print('\n已写盘 %d（备份 %s）' % (n, bak))
