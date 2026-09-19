# -*- coding: utf-8 -*-
"""裸下标统一扫描（遮蔽加固版）：code span / $$…$$ / $…$ / [[…]] / 注释 / frontmatter。

输出：
 1) 全量命中（A/B/C/D 分类）
 2) 按唯一 token 聚合
 3) 只输出指定类别的明细（--cls）
"""
import os, re, sys, collections
sys.stdout.reconfigure(encoding="utf-8")
os.chdir(r"c:\Obsidion\妙妙屋")

ROOT = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else "04-课件/习题集/四·成书层（习题书）/习题书-教师版"
WANT = None
for a in sys.argv[1:]:
    if a.startswith('--cls='):
        WANT = set(a.split('=', 1)[1])

SUB_UNI = "₀-₉₊₋₌₍₎ₐₑₒₓₔₕₖₗₘₙₚₛₜⁿ"
SUP_UNI = "⁰-⁹⁺⁻⁼⁽⁾ⁿ"
BODY = r"A-Za-z0-9()+\-−·/_%"
FIRSTCH = r"0-9A-Za-z()+\-−·θφλμνσπσΣΔΩ°½¼¾′″" + SUB_UNI + SUP_UNI
# 2026-09-15：基底补希腊字母 —— 原先只认 [A-Za-z]，导致 ρ_A / Δ_fH / φ_x 等全漏检
# （实证：教案 L227 的 ρ_A/ρ_B 未被命中，同句 M_A/M_B 被命中）
GREEK = r"\u0370-\u03FF\u1F00-\u1FFF"
# 2026-09-15(b)：基底允许一个尾随括号组 —— 修 `c(C2H6)^(1/2)` 类漏检
# （原基底 `[...][...]{0,14}` 要求以字母/数字续，遇到 `)`/`]` 结尾就断）
BASE = (r"[" + GREEK + r"A-Za-z][" + GREEK + r"A-Za-z0-9]{0,14}"
        r"(?:\([A-Za-z0-9]{1,8}\))?")
PAT = re.compile(r"(?<![\\$A-Za-z0-9" + GREEK + r"])"
                 r"(" + BASE + r")"
                 r"([_^])(["
                 + FIRSTCH + r"][" + BODY + SUB_UNI + SUP_UNI + r"]{0,10})")


def mask(line):
    out = list(line); i, n = 0, len(line)

    def blank(a, b):
        for k in range(a, min(b, n)):
            out[k] = ' '

    while i < n:
        ch = line[i]
        if ch == '`':
            j = line.find('`', i + 1)
            if j == -1:
                break
            blank(i, j + 1); i = j + 1; continue
        # 行内/行首 $$…$$（须先于单 $ 处理）
        if line.startswith('$$', i) and not (i > 0 and line[i - 1] == '\\'):
            j = line.find('$$', i + 2)
            if j == -1:
                blank(i, n); break
            blank(i, j + 2); i = j + 2; continue
        if ch == '$' and not (i > 0 and line[i - 1] == '\\'):
            j = line.find('$', i + 1)
            if j == -1:
                i += 1; continue
            blank(i, j + 1); i = j + 1; continue
        # wikilink / 嵌入 ![[…]]
        if line.startswith('![[', i) or line.startswith('[[', i):
            j = line.find(']]', i)
            if j == -1:
                break
            blank(i, j + 2); i = j + 2; continue
        i += 1
    return ''.join(out)


def cls(base, mark, sub):
    if mark == '^':
        return 'D'
    if re.search(r"[" + SUB_UNI + SUP_UNI + r"]", sub):
        return 'A'
    if re.fullmatch(r'[A-Za-z]', sub):
        return 'B'
    return 'C'


MEDIA_EXT = re.compile(r'\.(?:jpe?g|png|gif|webp|svg|bmp|tiff?|pdf|md|docx?|xlsx?|zip)(?:$|[|\])\s])', re.I)


def is_pathish(raw, a, b):
    """token 属于文件路径/文件名（如 ABOC202505_..._images/xxx.jpg）→ 判为假阳性。"""
    # 向左右扩到词边界（允许路径字符）
    word_re = re.compile(r'[A-Za-z0-9_\-./\\]+')
    wa = a
    while wa > 0 and word_re.match(raw[wa - 1]):
        wa -= 1
    wb = b
    while wb < len(raw) and word_re.match(raw[wb]):
        wb += 1
    word = raw[wa:wb]
    if MEDIA_EXT.search(word):
        return True
    # token 前后紧邻 **ASCII** 字母/数字/下划线 → 是更长词的一部分
    # （注意不能用 isalnum()：Unicode 上下标如 ³ ⁶ ₓ 也算 alnum，会误杀真命中）
    def _ascii_word(ch):
        return ch.isascii() and (ch.isalnum() or ch == '_')
    if (a > 0 and _ascii_word(raw[a - 1])) or (b < len(raw) and _ascii_word(raw[b])):
        return True
    return False


hits = []
files = []
for dp, dn, fn in os.walk(ROOT):
    if '_归档' in dp or '_archive' in dp or os.path.basename(dp).startswith('_'):
        continue
    for f in fn:
        if f.endswith('.md') and not f.startswith('README'):
            files.append(os.path.join(dp, f))
files.sort()

for p in files:
    lines = open(p, encoding="utf-8", errors="replace").read().split("\n")
    in_fence = in_fm = in_disp = False; fm_done = False
    for idx, raw in enumerate(lines, 1):
        s = raw.strip()
        if not fm_done:
            if idx == 1 and s == '---':
                in_fm = True; continue
            if in_fm:
                if s == '---':
                    in_fm = False; fm_done = True
                continue
        if s.startswith('```') or s.startswith('~~~'):
            in_fence = not in_fence; continue
        if in_fence: continue
        # 多行 $$ 显示块：按本行 $$ 计数翻转（奇=边界行；偶=行内成对）
        cnt_dd = s.count('$$')
        if cnt_dd:
            if cnt_dd % 2 == 1:
                in_disp = not in_disp
                continue
            if in_disp:
                continue
        if in_disp: continue
        if s.startswith('<!--') or s.endswith('-->'): continue
        m = mask(raw)
        for mo in PAT.finditer(m):
            tok = mo.group(0)
            if is_pathish(raw, mo.start(), mo.end()):
                continue
            c = cls(mo.group(1), mo.group(2), mo.group(3))
            hits.append((c, p, idx, tok, raw))

cnt = collections.Counter(h[0] for h in hits)
print("命中 %d 处：%s  （扫描 %d 文件）" % (len(hits), dict(cnt), len(files)))
print()

by = collections.defaultdict(list)
for c, p, idx, tok, raw in hits:
    by[(c, tok)].append((p, idx, raw))

sel = {k: v for k, v in by.items() if WANT is None or k[0] in WANT}
print("唯一 token %d（筛选后 %d）：" % (len(by), len(sel)))
for (c, tok), v in sorted(sel.items(), key=lambda x: (x[0][0], -len(x[1]), x[0][1])):
    print("  [%s] %-24s x%-3d %s L%d" % (c, tok, len(v), v[0][0].split('/')[-1][:40], v[0][1]))
