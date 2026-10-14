# -*- coding: utf-8 -*-
r"""P2-⑥ 可行性盘点（只读）：有机池规模 / 机构分布 / 难度分布 / 可成卷数估算。"""
import io, os, csv, re, collections
os.chdir(r'C:\Obsidion\妙妙屋')

# 入池集合（来自不可组卷清单 CSV）
rows = list(csv.reader(io.open('09-审计报告/2026-10-07-不可组卷题目清单.csv', encoding='utf-8-sig')))
h = rows[0]; i_p = h.index('path'); i_v = h.index('verdict')
inpool = set(r[i_p] for r in rows[1:] if len(r) > i_v and r[i_v] == '入池')
print('入池集合 %d 张' % len(inpool))

pat_mod = re.compile(r'^subject_module:\s*(.+)$', re.M)
pat_diff = re.compile(r'^difficulty:\s*(\d+)', re.M)
stat = collections.Counter()
inst = collections.Counter()
diff = collections.Counter()
n = 0
for p in inpool:
    fp = p.replace('/', os.sep)
    if not os.path.isfile(fp):
        continue
    t = io.open(fp, encoding='utf-8-sig').read()
    m = pat_mod.search(t)
    mod = (m.group(1).strip() if m else '(无)')
    stat[mod] += 1
    if mod == '有机化学':
        n += 1
        parts = p.split('/')
        inst[parts[3] if len(parts) > 3 else parts[2]] += 1
        d = pat_diff.search(t)
        diff[d.group(1) if d else '?'] += 1
print()
print('=== 入池卡的 subject_module 分布 ===')
for k, v in stat.most_common(10):
    print('  %-10s %d' % (k, v))
print()
print('=== 有机池：%d 张 ===' % n)
print('  按机构/目录：')
for k, v in inst.most_common(20):
    print('    %-22s %d' % (k, v))
print('  按难度：', dict(sorted(diff.items())))
print()
print('  ⇒ 按「每卷 ≤15 题」估：可成卷约 %d 卷（若单机构成卷则看各机构 ≥15 的个数）'
      % (n // 15))
