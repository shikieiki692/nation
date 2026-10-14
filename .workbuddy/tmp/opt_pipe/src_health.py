# -*- coding: utf-8 -*-
"""全机构来源标注体检：
A. source_file 是否真实存在（相对库根）
B. source 与 source_file 是否自洽（套名关键词互证）
C. 卷内来源行的机构 vs 卡片所在目录机构（查张冠李戴）
"""
import io, os, re, glob, collections

os.chdir(r'C:\Obsidion\妙妙屋')
BASE = '04-题库/2026机构初赛模拟题/'
CARD_IDX = {}
for p in glob.glob('04-题库/**/*.md', recursive=True):
    CARD_IDX[os.path.basename(p)[:-3]] = p


def fm(t, k):
    m = re.search(r'^%s:[ \t]*"?(.+?)"?[ \t]*$' % k, t, re.M)
    return m.group(1) if m else ''


A_miss = collections.Counter()
A_tot = collections.Counter()
B_bad = []
rows = []
for d in sorted(os.listdir(BASE)):
    dp = os.path.join(BASE, d)
    if not os.path.isdir(dp):
        continue
    for p in glob.glob(dp + '/题-*.md'):
        t = io.open(p, encoding='utf-8-sig', errors='replace').read()
        sf, src = fm(t, 'source_file'), fm(t, 'source')
        A_tot[d] += 1
        if sf and not os.path.exists(sf.replace('\\', '/')):
            A_miss[d] += 1
            if A_miss[d] <= 2:
                B_bad.append(('MISS', p, sf))
        # B: source 里出现的关键词应能在 source_file 文件名中找到
        if sf and src:
            key = re.sub(r'[^0-9A-Za-z\u4e00-\u9fff]', '', src)
            base = re.sub(r'[^0-9A-Za-z\u4e00-\u9fff]', '', os.path.basename(sf).replace('.md', ''))
            n = 6
            hits = sum(1 for i in range(0, len(key) - n + 1) if key[i:i + n] in base)
            rows.append((d, p, src, os.path.basename(sf), hits / max(1, len(key) - n + 1)))

print('===== A. source_file 存在性 =====')
for d in sorted(A_tot):
    m = A_miss.get(d, 0)
    flag = '  ⚠️' if m else ''
    print('   %-12s %4d 卡 ｜ 缺失 %3d%s' % (d, A_tot[d], m, flag))
print('   合计卡 %d ｜ 缺失 %d' % (sum(A_tot.values()), sum(A_miss.values())))
print()
print('===== B. source ↔ source_file 自洽（低命中样例，<0.30）=====')
low = [r for r in rows if r[4] < 0.30]
print('   低命中 %d / %d' % (len(low), len(rows)))
agg = collections.Counter(x[0] for x in low)
print('   按机构:', dict(agg))
for r in low[:10]:
    print('     [%s] hits=%.2f  %s' % (r[0], r[4], r[2][:52]))
    print('        file= %s' % r[3][:64])
