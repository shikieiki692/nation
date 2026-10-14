# -*- coding: utf-8 -*-
"""活跃任务卡 status 统一（终版）
规则：① 人工确认表 > ② 正文显式状态声明 > ③ FM completed 字段 > ④ 保持规范值 > ⑤ 默认 active
"""
import io, os, re, sys

os.chdir(r'C:\Obsidion\妙妙屋')
D = '00-首页/活跃任务'
APPLY = '--apply' in sys.argv
def rd(p): return io.open(p, encoding='utf-8-sig').read()

DECL = re.compile(r'(?:状态|结论)[^\n]{0,24}?(completed|blocked|active|已完成|已收官|已闭环|已办结|已恢复\s*active|保持\s*blocked)', re.I)
DMAP = {'completed': 'completed', '已完成': 'completed', '已收官': 'completed', '已闭环': 'completed', '已办结': 'completed',
        'blocked': 'blocked', '保持blocked': 'blocked', 'active': 'active', '已恢复active': 'active'}

# 人工确认（逐卡读正文后定）
MANUAL = {
    '习题册制作-执行计划-2026-08-29.md': 'active',
    '交接-2026-09-15-备课线收尾核验.md': 'active',
    '任务卡-2026-09-14-习题书裸下标收口与git健壮性复核.md': 'active',
    '任务卡-2026-09-16-组题收口与两批新批次纳入.md': 'active',
    '任务卡-KP待完善项非文字任务清零.md': 'active',
    '任务卡-validate_kb每周运行.md': 'active',
    '任务卡-KP薄壳队列与治理后续.md': 'blocked',
    '任务卡-学生反馈闭环建立.md': 'blocked',
    '任务卡-学生材料清理.md': 'blocked',
    '任务卡-实验模块决策.md': 'blocked',
    '任务卡-纸质版排版测试.md': 'blocked',
    '任务卡-PPT制作方法探究与试点.md': 'blocked',
}
DATE_FIX = {
    '任务卡-2026-09-21-北斗40套导入评估与规划.md': '2026-09-21',
    '任务卡-2026-10-07-机构域答案缺口处理.md': '2026-10-08',
}

changed = []; unchanged = []
for f in sorted(os.listdir(D)):
    if not f.endswith('.md'):
        continue
    p = os.path.join(D, f); t = rd(p)
    m = re.match(r'^---\r?\n(.*?)\r?\n---\r?\n', t, re.S)
    if not m:
        continue
    s, b = m.group(1), t[m.end():]
    def g(k):
        mm = re.search(r'^%s:[ \t]*(.*)$' % k, s, re.M)
        return mm.group(1).strip().strip('"') if mm else None
    if g('type') != '活跃任务卡':
        continue
    fmst, comp = g('status'), g('completed')
    head = '\n'.join([l for l in b.split('\n') if l.strip()][:45])
    mm = DECL.search(head)
    decl = DMAP.get(mm.group(1).replace(' ', '').lower()) if mm else None
    if f in MANUAL:
        new, basis = MANUAL[f], '人工确认'
    elif decl:
        new, basis = decl, '正文声明'
    elif comp:
        new, basis = 'completed', 'completed字段'
    elif fmst in ('active', 'blocked', 'completed'):
        new, basis = fmst, '已规范'
    else:
        new, basis = 'active', '默认'
    need_date = (new == 'completed' and not comp)
    dn = DATE_FIX.get(f) if need_date else None
    if new != fmst or dn:
        changed.append((f, fmst, new, comp, dn, basis))
        if APPLY:
            ns = re.sub(r'^status:[ \t]*.*$', 'status: ' + new, s, count=1, flags=re.M)
            if dn and not re.search(r'^completed:', ns, re.M):
                ns = re.sub(r'^(status: %s)$' % re.escape(new), r'\1\ncompleted: ' + dn, ns, count=1, flags=re.M)
            io.open(p, 'w', encoding='utf-8', newline='').write('---\n' + ns + '\n---\n' + b)
    else:
        unchanged.append((f, fmst, new))

print('%-52s %-8s %-10s %-11s %s' % ('卡片', '现值', '新值', 'completed', '依据'))
print('-' * 96)
for f, o, n, comp, dn, basis in changed:
    print('%-52s %-8s %-10s %-11s %s' % (f[:52], o, n, dn or (comp or '-'), basis))
print()
import collections
c = collections.Counter(x[2] for x in changed)
print('%s：%d 张改动 %s' % ('已应用' if APPLY else 'DRY', len(changed), dict(c)))
print('未改动：%d 张 %s' % (len(unchanged), [x[0][:22] for x in unchanged]))
