# -*- coding: utf-8 -*-
"""A2 有机卷线 Step 0：有机池实测（只读）。

复现方案件口径：有机池 1,793（source_subject: 有机化学），
剔 `_待人工复核-空壳与重复卡` 97 ⇒ 可用 1,696。
并给出 机构 / difficulty / 分值 三维分布（SOP 要求建线先报分布再选题）。
"""
import os, re, glob, collections

BASE = r"C:\Obsidion\妙妙屋\04-题库\2026机构初赛模拟题"
SKIP_DIR = "_待人工复核-空壳与重复卡"


def fm_get(t, k):
    m = re.search(r'^' + k + r':[ \t]*(.*)$', t, re.M)
    return m.group(1).strip() if m else ''


rows = []
for p in glob.glob(os.path.join(BASE, '**', '题-*.md'), recursive=True):
    rel = os.path.relpath(p, BASE).replace(os.sep, '/')
    if rel.startswith(SKIP_DIR):
        continue
    try:
        t = open(p, encoding='utf-8-sig', errors='replace').read()
    except Exception:
        continue
    ss = fm_get(t, 'source_subject')
    sm = fm_get(t, 'subject_module')
    rows.append((rel, ss, sm, fm_get(t, 'difficulty'), fm_get(t, 'source_norm'),
                 fm_get(t, 'exam_stage'), fm_get(t, 'score')))

print("扫描卡总数（剔待复核目录后）=", len(rows))
c_ss = collections.Counter(r[1] for r in rows)
print("\n== source_subject 分布 ==")
for k, v in c_ss.most_common(12):
    print("   %-14s %d" % (k or '(空)', v))
c_sm = collections.Counter(r[2] for r in rows)
print("\n== subject_module 分布 ==")
for k, v in c_sm.most_common(12):
    print("   %-14s %d" % (k or '(空)', v))

org = [r for r in rows if r[1] == '有机化学']
print("\n== 有机池（source_subject=有机化学）== %d" % len(org))
inst = collections.Counter(r[4] for r in org)
print("\n-- 机构分布 --")
for k, v in inst.most_common(20):
    print("   %-16s %d" % (k or '(空)', v))
d = collections.Counter(r[3] for r in org)
print("\n-- difficulty 分布 --")
for k in sorted(d, key=lambda x: (len(x), x)):
    print("   %-6s %d" % (k or '(空)', d[k]))
sc = collections.Counter(r[6] for r in org)
print("\n-- score 分布（前 15）--")
for k, v in sc.most_common(15):
    print("   %-8s %d" % (k or '(空)', v))
st = collections.Counter(r[5] for r in org)
print("\n-- exam_stage 分布 --")
for k, v in st.most_common():
    print("   %-12s %d" % (k or '(空)', v))
