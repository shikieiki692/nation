# -*- coding: utf-8 -*-
"""卷末选题清单 数学自洽 + 与题面来源行一致性核查（9 卷答案版）"""
import io, os, re

os.chdir(r'C:\Obsidion\妙妙屋')
MD = '04-题库'
VOLS = ['X', 'XI', 'XIp', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII']

def star_count(s):
    return s.count('⭐')

print('%-7s %-5s %-5s %-7s %-7s %-6s %-8s %s' % ('卷', '表行', '声明题', '分值合计', '声明分', '机构', '难度分布', '判定'))
for v in VOLS:
    p = os.path.join(MD, '初赛模拟卷%s（非有机·答案版）.md' % v)
    t = io.open(p, encoding='utf-8-sig').read()
    # 声明题数/满分：取卷首 "本卷共 N 题，满分 M 分" 或 "N 题，满分 M 分"
    m = re.search(r'共\s*(\d+)\s*题[，,]\s*满分\s*(\d+)\s*分', t)
    if not m:
        m = re.search(r'(\d+)\s*题[，,]\s*满分\s*(\d+)\s*分', t)
    n_decl, full_decl = (int(m.group(1)), int(m.group(2))) if m else (None, None)
    # 卷末清单
    i = t.find('附：选题清单')
    seg = t[i:] if i >= 0 else ''
    rows = []
    for ln in seg.split('\n'):
        mm = re.match(r'^\|\s*(\d+)\s*\|(.+)\|\s*$', ln)
        if mm:
            cols = [c.strip() for c in ln.strip('|').split('|')]
            if len(cols) >= 7:
                rows.append(cols)
    tot = 0
    insts = set()
    diffs = {}
    for c in rows:
        try:
            tot += int(re.sub(r'[^\d]', '', c[6]) or 0)
        except Exception:
            pass
        insts.add(c[3])
        diffs[star_count(c[5])] = diffs.get(star_count(c[5]), 0) + 1
    # 题面来源行的机构
    src_insts = set()
    for mm in re.finditer(r'^>\s*来源[:：]\s*(\S+)', t, re.M):
        src_insts.add(mm.group(1))
    n_qt = len(re.findall(r'^###\s+第\s*\d+\s*题', t, re.M))
    ok = (len(rows) == n_qt == n_decl) and (tot == full_decl)
    inst_match = (insts == src_insts)
    print('%-7s %-5d %-5s %-7d %-7s %-6d %-8s %s' % (
        v, len(rows), n_decl, tot, full_decl, len(insts),
        ' '.join('%d★×%d' % (k, n) for k, n in sorted(diffs.items())),
        ('OK' if ok else '⚠️') + ('' if inst_match else ' 来源列≠题面(%s)' % sorted(insts ^ src_insts)) +
        ('  题面题数=%d' % n_qt if n_qt != len(rows) else '')))
