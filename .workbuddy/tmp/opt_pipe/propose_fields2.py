# -*- coding: utf-8 -*-
"""三字段取值提案（wikilink + 反引号路径，全部过存在性校验）"""
import io, os, re, glob

os.chdir(r'C:\Obsidion\妙妙屋')
D = '00-首页/活跃任务'
def rd(p): return io.open(p, encoding='utf-8-sig').read()
def fmsplit(t):
    m = re.match(r'^---\r?\n(.*?)\r?\n---\r?\n', t, re.S)
    return (m.group(1), t[m.end():]) if m else ('', t)
def get(s, k):
    m = re.search(r'^%s:[ \t]*(.*)$' % re.escape(k), s, re.M)
    return m.group(1).strip() if m else None
def has_block(s, k): return bool(re.search(r'^%s:' % re.escape(k), s, re.M))

# 全库 md 索引（相对路径，无扩展名）
ALL = set()
for dp, dn, fn in os.walk('.'):
    dn[:] = [d for d in dn if d not in ('.git', '.workbuddy')]
    for f in fn:
        if f.endswith('.md'):
            rel = os.path.relpath(os.path.join(dp, f), '.').replace('\\', '/')
            ALL.add(rel[:-3])
LOGS = sorted(os.path.basename(p)[:-3] for p in glob.glob('00-首页/工作日志/*.md'))
print('日志可用：%d 天（%s … %s）' % (len(LOGS), LOGS[0], LOGS[-1]))
print()

WL = re.compile(r'\[\[([^\]|#]+)')
BK = re.compile(r'`((?:09-审计报告|00-首页/工作日志|11-模板|04-题库|06-外部资料导入|02-数据库)/[^`\s]+?\.md)`')

def cls(l):
    if l.startswith('09-审计报告/') or l.startswith('00-首页/工作日志/'):
        return 'E'
    if l.startswith('11-模板/') or '规范' in l or 'SOP' in l or '总纲' in l:
        return 'S'
    if l.startswith('00-首页/活跃任务'):
        return 'R'
    if l.startswith('04-题库/') or l.startswith('06-外部资料导入'):
        return 'S'
    return None

for f in sorted(os.listdir(D)):
    if not f.endswith('.md'):
        continue
    t = rd(os.path.join(D, f)); s, b = fmsplit(t)
    if get(s, 'type') != '活跃任务卡':
        continue
    need = [k for k in ('source_notes', 'related_notes', 'evidence') if not has_block(s, k)]
    if not need:
        continue
    cands = []
    for l in WL.findall(b) + BK.findall(b):
        l = l.strip().lstrip('./')
        if l in ALL and l not in cands:
            cands.append(l)
    # 已有旧 related: 字段内容（从 FM 抓 wikilink）
    old_rel = WL.findall(s)
    for l in old_rel:
        if l in ALL and l not in cands:
            cands.append(l)
    S = [l for l in cands if cls(l) == 'S']
    R = [l for l in cands if cls(l) == 'R']
    E = [l for l in cands if cls(l) == 'E']
    # 兜底：本卡日期 → 当日日志
    md = re.search(r'(\d{4}-\d{2}-\d{2})', f)
    fb_log = None
    if md and ('00-首页/工作日志/' + md.group(1)) in ALL:
        fb_log = '00-首页/工作日志/' + md.group(1)
    print('◆ %s  | 缺 %s' % (f[:56], need))
    print('   S: %s' % (S[:3] or '—'))
    print('   R: %s' % (R[:3] or '—'))
    print('   E: %s%s' % (E[:3] or '—', ('  ｜兜底日志 %s' % fb_log) if fb_log and not E else ''))
    print('   已有旧 related 字段: %s' % ('是' if re.search(r'^related:', s, re.M) else '否'))
    print()
