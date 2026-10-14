# -*- coding: utf-8 -*-
"""卷「组卷口径」承诺兑现核查：题数 / 机构数与列表 / 难度门槛 / 满分 / 模块 / 无有机 / 无真题。
逐条把卷末清单与口径行对账；卡片侧读 difficulty・source_subject・source。"""
import io, os, re, glob, collections

os.chdir(r'C:\Obsidion\妙妙屋')
CARD = {}
for p in glob.glob('04-题库/**/*.md', recursive=True):
    CARD[os.path.basename(p)[:-3]] = p


def fm(t, k):
    m = re.search(r'^%s:[ \t]*"?(.+?)"?[ \t]*$' % k, t, re.M)
    return m.group(1) if m else ''


print('%-8s %-6s %-6s %-10s %-6s %-8s %s' % ('卷', '题数', '机构数', '难度<4', '满分', '有机题', '问题'))
tot_issue = 0
for v in sorted(glob.glob('04-题库/初赛模拟卷*（非有机·答案版）.md')):
    vol = os.path.basename(v).replace('初赛模拟卷', '').replace('（非有机·答案版）.md', '')
    t = io.open(v, encoding='utf-8-sig').read()
    claim = re.search(r'组卷口径\*\*：(\d+)\s*题跨\s*\*?\*?(\d+)\s*个来源机构', t)
    rows = []
    for l in t.split('\n'):
        m = re.match(r'\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*\[\[([^\]|]+)[^\]]*\]\]\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(⭐+)\s*\|\s*(\d+)', l)
        if m:
            rows.append(dict(no=int(m.group(1)), name=m.group(2), card=m.group(3).strip(),
                             inst=m.group(4).strip(), mod=m.group(5).strip(),
                             star=len(m.group(6)), pts=int(m.group(7))))
    issues = []
    if claim:
        cq, ci = int(claim.group(1)), int(claim.group(2))
        if cq != len(rows):
            issues.append('题数不符(口径%d/实际%d)' % (cq, len(rows)))
        insts = set(r['inst'] for r in rows)
        if ci != len(insts):
            issues.append('机构数不符(口径%d/实际%d:%s)' % (ci, len(insts), ','.join(sorted(insts))))
    low = []
    organic = []
    for r in rows:
        cp = CARD.get(r['card'])
        if not cp:
            issues.append('卡缺:' + r['card'][:20]); continue
        c = io.open(cp, encoding='utf-8-sig', errors='replace').read()
        d = fm(c, 'difficulty')
        if d and int(d) < 4:
            low.append('%d(%s)' % (r['no'], d))
        sub = fm(c, 'source_subject')
        if sub == '有机化学':
            organic.append(str(r['no']))
        if '真题' in fm(c, 'source') and '模拟' not in fm(c, 'source'):
            issues.append('疑真题第%d题' % r['no'])
    if low:
        issues.append('难度<4:' + ','.join(low))
    if organic:
        issues.append('有机题:' + ','.join(organic))
    total = sum(r['pts'] for r in rows)
    if total != 130:
        issues.append('满分离130(%d)' % total)
    tot_issue += len(issues)
    print('%-8s %-6s %-6s %-10s %-6s %-8s %s' % (
        vol, len(rows), len(set(r['inst'] for r in rows)), ','.join(low) or '-', total,
        ','.join(organic) or '-', '; '.join(issues) or '✅'))
print()
print('合计问题项', tot_issue)
