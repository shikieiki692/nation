# -*- coding: utf-8 -*-
"""定位「第40届chemy初赛模拟10~18/无机19/有机20~22」的真身：
题面 CJK 8-gram 倒排索引 → 对全库（04-题库 全部卡 + chemy试题 原始合集）求最佳匹配。"""
import io, os, re, glob, collections

os.chdir(r'C:\Obsidion\妙妙屋')

CJK = re.compile(r'[\u4e00-\u9fff]')
LATEX = re.compile(r'\$[^$]*\$|\$\$.*?\$\$', re.S)
CMD = re.compile(r'\\[a-zA-Z]+')
IMG = re.compile(r'!\[[^\]]*\]\([^)]*\)|<img[^>]*>')
MDLINK = re.compile(r'\[\[[^\]]*\]\]')
REF = re.compile(r'^#{1,3}\s*参考答案.*$', re.M)


def norm(t):
    t = LATEX.sub(' ', t)
    t = IMG.sub(' ', t)
    t = CMD.sub(' ', t)
    t = MDLINK.sub(' ', t)
    t = re.sub(r'[^\u4e00-\u9fff0-9]', '', t)
    return t


def body_of(t):
    """题面区：FM 之后、参考答案之前。"""
    p = t.split('---')
    b = '---'.join(p[2:]) if len(p) > 2 else t
    m = REF.search(b)
    return b[:m.start()] if m else b


def grams(s, n=8):
    return {s[i:i + n] for i in range(0, len(s) - n + 1, 2)}


# ---------- 建索引 ----------
corpus = {}
for p in glob.glob('04-题库/**/*.md', recursive=True):
    try:
        t = io.open(p, encoding='utf-8-sig', errors='replace').read()
    except Exception:
        continue
    corpus[p] = norm(body_of(t))
for p in glob.glob('chemy试题/*.md'):
    try:
        t = io.open(p, encoding='utf-8-sig', errors='replace').read()
    except Exception:
        continue
    corpus['RAW:' + p] = norm(t)

print('语料文件数', len(corpus))
idx = collections.defaultdict(set)
for p, s in corpus.items():
    for g in grams(s):
        idx[g].add(p)
print('索引 gram 数', len(idx))

# ---------- 目标卡 ----------
TARGET = []
for p in glob.glob('04-题库/2026机构初赛模拟题/chemy/题-*.md'):
    t = io.open(p, encoding='utf-8-sig', errors='replace').read()
    m = re.search(r'^source_norm:\s*"?chemy-(.+?)"?\s*$', t, re.M)
    if m and re.match(r'第40届chemy初赛', m.group(1)):
        TARGET.append((m.group(1), p, t))

print('目标卡', len(TARGET))
print()

# 按套汇总
by_src = collections.defaultdict(list)
for s, p, t in TARGET:
    by_src[s].append((p, t))

for s in sorted(by_src, key=lambda x: (len(x), x)):
    files = by_src[s]
    agg = collections.Counter()
    for p, t in files:
        g = grams(norm(body_of(t)))
        if not g:
            continue
        cand = collections.Counter()
        for gg in g:
            for c in idx.get(gg, ()):
                cand[c] += 1
        for c, n in cand.items():
            if n >= max(6, len(g) * 0.15):
                agg[c] = max(agg[c], n / len(g))
    print('◆ %s（%d 卡）' % (s, len(files)))
    if agg:
        for c, r in agg.most_common(3):
            print('      相似 %.2f  %s' % (r, c[:96]))
    else:
        print('      ⇒ 全库无任何相似命中')
