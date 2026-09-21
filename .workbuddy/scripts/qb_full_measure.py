# -*- coding: utf-8 -*-
"""题库全量实测（2026-09-21 下午）：为 题库总索引 / 题库架构总览 回填数字。
口径严格区分：md 数（含索引/系统/答案等非题文件） vs type:题目 非 deprecated（题数）。"""
import os, re
from collections import Counter, defaultdict

ROOT = r'C:\Obsidion\妙妙屋'
QB = os.path.join(ROOT, '04-题库')
TK = os.path.join(ROOT, '05-真题库')


def fm(txt):
    """取 frontmatter 文本（--- 之间的部分）"""
    if txt.startswith('---'):
        i = txt.find('\n---', 3)
        if i > 0:
            return txt[3:i]
    return txt[:3000]


def scan(base):
    """返回 [(relpath, fmtext)]"""
    out = []
    for dp, ds, fs in os.walk(base):
        if '_归档' in dp:
            continue
        for fn in fs:
            if fn.endswith('.md'):
                p = os.path.join(dp, fn)
                try:
                    t = open(p, encoding='utf-8', errors='replace').read()
                except Exception:
                    continue
                out.append((os.path.relpath(p, base).replace('\\', '/'), fm(t)))
    return out


def field(fmtext, key):
    m = re.search(r'(?m)^%s:\s*(.*)$' % re.escape(key), fmtext)
    return m.group(1).strip() if m else None


def is_dep(fmtext):
    return bool(re.search(r'(?m)^status:\s*deprecated', fmtext))


qb = scan(QB)
tk = scan(TK)

# ---------- 1. 顶层目录 md 数 / 题目数 ----------
print('=' * 78)
print('【1】04-题库 顶层分区 md 数 与 type:题目 非 deprecated')
print('=' * 78)
top_md = Counter()
top_q = Counter()
top_dep = Counter()
for rel, f in qb:
    seg = rel.split('/')[0] if '/' in rel else '(顶层文件)'
    top_md[seg] += 1
    if field(f, 'type') == '题目':
        if is_dep(f):
            top_dep[seg] += 1
        else:
            top_q[seg] += 1
for k in sorted(top_md):
    print('  %-14s md %5d   type题目(非dep) %5d   dep %d' % (k, top_md[k], top_q[k], top_dep[k]))
print('  %-14s md %5d   type题目(非dep) %5d   dep %d' % ('【合计】', sum(top_md.values()), sum(top_q.values()), sum(top_dep.values())))

# ---------- 2. type 分布 ----------
print()
print('=' * 78)
print('【2】type 分布')
print('=' * 78)
ct = Counter(); ctd = Counter()
for rel, f in qb:
    t = field(f, 'type') or '(无type)'
    ct[t] += 1
    if is_dep(f):
        ctd[t] += 1
for k, n in sorted(ct.items(), key=lambda x: -x[1]):
    print('  04 %-10s %5d  dep %d' % (k, n, ctd.get(k, 0)))
ct2 = Counter()
for rel, f in tk:
    ct2[field(f, 'type') or '(无type)'] += 1
for k, n in sorted(ct2.items(), key=lambda x: -x[1]):
    print('  05 %-10s %5d' % (k, n))

# ---------- 3. 教材习题 逐源 ----------
print()
print('=' * 78)
print('【3】教材习题 逐源：md 数 / type题目非dep / dep')
print('=' * 78)
EX = os.path.join(QB, '教材习题')
src_md = Counter(); src_q = Counter(); src_dep = Counter(); src_other = defaultdict(list)
for rel, f in qb:
    if not rel.startswith('教材习题/'):
        continue
    parts = rel.split('/')
    key = parts[1] if len(parts) > 2 else '(教材习题根)'
    src_md[key] += 1
    if field(f, 'type') == '题目':
        if is_dep(f):
            src_dep[key] += 1
        else:
            src_q[key] += 1
tot = 0
for k in sorted(src_q, key=lambda x: -src_q[x]):
    print('  %-26s md %5d  题目(非dep) %5d  dep %d' % (k, src_md[k], src_q[k], src_dep[k]))
    tot += src_q[k]
print('  %-26s md %5d  题目(非dep) %5d  dep %d' % ('【小计】', sum(src_md.values()), tot, sum(src_dep.values())))

# ---------- 4. 真题 逐届/区 ----------
print()
print('=' * 78)
print('【4】真题/ 分区：md 数 / type题目非dep')
print('=' * 78)
z_md = Counter(); z_q = Counter()
for rel, f in qb:
    if not rel.startswith('真题/'):
        continue
    seg = rel.split('/')[1] if len(rel.split('/')) > 2 else '(根)'
    z_md[seg] += 1
    if field(f, 'type') == '题目' and not is_dep(f):
        z_q[seg] += 1
for k in sorted(z_md):
    print('  %-18s md %5d  题目(非dep) %5d' % (k, z_md[k], z_q[k]))
print('  %-18s md %5d  题目(非dep) %5d' % ('【真题/小计】', sum(z_md.values()), sum(z_q.values())))

# ---------- 5. pack 分布 ----------
print()
print('=' * 78)
print('【5】pack 分布（04-题库 全部 md 口径）')
print('=' * 78)
pk = Counter()
for rel, f in qb:
    pk[field(f, 'pack') or '(空)'] += 1
for k, n in sorted(pk.items(), key=lambda x: -x[1]):
    print('  %-14s %5d' % (k, n))

# ---------- 6. teaching_level / difficulty ----------
print()
print('=' * 78)
print('【6】teaching_level 与 difficulty 分布（type:题目 非dep）')
print('=' * 78)
tl = Counter(); df = Counter(); ss = Counter()
for rel, f in qb:
    if field(f, 'type') == '题目' and not is_dep(f):
        tl[field(f, 'teaching_level') or '(空)'] += 1
        df[field(f, 'difficulty') or '(空)'] += 1
        ss[field(f, 'source_subject') or '(空)'] += 1
print('  teaching_level:', dict(sorted(tl.items(), key=lambda x: -x[1])))
print('  difficulty    :', dict(sorted(df.items(), key=lambda x: -x[1])))
print('  source_subject:', dict(sorted(ss.items(), key=lambda x: -x[1])))

# ---------- 7. 汇总 ----------
print()
print('=' * 78)
print('【7】口径汇总')
print('=' * 78)
q04 = sum(1 for rel, f in qb if field(f, 'type') == '题目' and not is_dep(f))
q05_t = sum(1 for rel, f in tk if field(f, 'type') == '真题')
q05_q = sum(1 for rel, f in tk if field(f, 'type') == '题目')
print('  04-题库 type:题目 非dep            =', q04)
print('  05-真题库 type:真题                =', q05_t)
print('  05-真题库 type:题目                =', q05_q)
print('  组卷池 = 题目(04) + 真题(05)       =', q04 + q05_t)
print('  04-题库 md 总数                    =', sum(top_md.values()))
print('  05-真题库 md 总数                  =', len(tk))
print('  04+05 md 总数                      =', sum(top_md.values()) + len(tk))
