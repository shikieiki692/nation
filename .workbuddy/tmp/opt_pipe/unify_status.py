# -*- coding: utf-8 -*-
"""活页任务卡 status 统一 —— dry/apply 双模
规则：① 正文显式状态声明 > ② FM completed 字段 > ③ 已是规范值则保留 > ④ 默认 active
附：completed 卡缺日期时，按正文/updated 补（仅在可证时）
"""
import io, os, re, sys, datetime

os.chdir(r'C:\Obsidion\妙妙屋')
D = '00-首页/活跃任务'
APPLY = '--apply' in sys.argv

def rd(p): return io.open(p, encoding='utf-8-sig').read()
def fmsplit(t):
    m = re.match(r'^---\r?\n(.*?)\r?\n---\r?\n', t, re.S)
    return (m.group(1), t[m.end():]) if m else ('', t)
def get(s, k):
    m = re.search(r'^%s:[ \t]*(.*)$' % re.escape(k), s, re.M)
    return m.group(1).strip().strip('"') if m else None

# 显式声明（前 45 非空行）
DECL = re.compile(r'(?:状态|结论)[^\n]{0,24}?(completed|blocked|active|已完成|已收官|已闭环|已办结|已恢复\s*active|保持\s*blocked)', re.I)
DMAP = {'completed': 'completed', '已完成': 'completed', '已收官': 'completed', '已闭环': 'completed', '已办结': 'completed',
        'blocked': 'blocked', '保持blocked': 'blocked', 'active': 'active', '已恢复active': 'active'}

# 已人工确认的补充证据（逐卡）：卡名 -> (新状态, completed日期或None)
MANUAL = {
    '任务卡-KP待完善项非文字任务清零.md': ('active', None),          # 正文「本卡已恢复 active」
    '任务卡-2026-09-16-组题收口与两批新批次纳入.md': ('active', None),  # 正文「本卡是下一步计划」
    '任务卡-2026-09-14-习题书裸下标收口与git健壮性复核.md': ('active', None),  # 交接卡（新会话入口）
    '交接-2026-09-15-备课线收尾核验.md': ('active', None),          # 交接核验卡
    '习题册制作-执行计划-2026-08-29.md': ('active', None),          # 无显式完成声明 ⇒ 保守 active（登记）
}
# completed 卡补日期（可证）
DATE_FIX = {
    '任务卡-2026-09-21-北斗40套导入评估与规划.md': '2026-09-21',   # 正文「2026-09-21 整批收官」
}

changed = []
for f in sorted(os.listdir(D)):
    if not f.endswith('.md'):
        continue
    p = os.path.join(D, f); t = rd(p); s, b = fmsplit(t)
    if get(s, 'type') != '活跃任务卡':
        continue
    fmst = get(s, 'status'); comp = get(s, 'completed')
    head = '\n'.join([l for l in b.split('\n') if l.strip()][:45])
    m = DECL.search(head)
    decl = DMAP.get(m.group(1).replace(' ', '').lower()) if m else None
    if f in MANUAL:
        new, _ = MANUAL[f]
    elif decl:
        new = decl
    elif comp:
        new = 'completed'
    elif fmst in ('active', 'blocked', 'completed'):
        new = fmst
    else:
        new = 'active'
    need_date = (new == 'completed' and not comp)
    date_new = DATE_FIX.get(f) if need_date else None
    if new != fmst or (need_date and date_new):
        changed.append((f, fmst, new, comp, date_new, bool(decl)))
        if APPLY:
            ns = re.sub(r'^status:[ \t]*.*$', 'status: ' + new, s, count=1, flags=re.M)
            if need_date and date_new and not re.search(r'^completed:', ns, re.M):
                # 插到 status 行之后
                ns = re.sub(r'^(status: %s)$' % re.escape(new), r'\1\ncompleted: %s' % date_new, ns, count=1, flags=re.M)
            io.open(p, 'w', encoding='utf-8', newline='').write('---\n' + ns + '\n---\n' + b)

print('%-52s %-8s %-10s %-11s %s' % ('卡片', '现值', '新值', 'completed', '依据'))
print('-' * 96)
for f, o, n, comp, dn, decl in changed:
    basis = '正文声明' if decl else ('completed字段' if comp else ('已规范' if o in ('active', 'blocked', 'completed') else ('人工确认' if f in MANUAL else '默认')))
    print('%-52s %-8s %-10s %-11s %s%s' % (f[:52], o, n, dn or (comp or '-'), basis, '' if APPLY else '   [dry]'))
print()
print('%s：%d 张改动' % ('已应用' if APPLY else 'DRY', len(changed)))
