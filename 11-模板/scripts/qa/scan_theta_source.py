# -*- coding: utf-8 -*-
"""题源中「数学区之外」的 X^θ 形态普查（只读）。"""
import os, re, sys, collections
sys.stdout.reconfigure(encoding="utf-8")
os.chdir(r"c:\Obsidion\妙妙屋")

TOK = re.compile(r"(?<![\$A-Za-z0-9])([A-Za-z]\w{0,12})\^θ((?:ₘ)?)")


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
        if line.startswith('![[', i) or line.startswith('[[', i):
            j = line.find(']]', i)
            if j == -1:
                break
            blank(i, j + 2); i = j + 2; continue
        i += 1
    return ''.join(out)


total_in = total_out = 0
rows = []
ctxs = collections.Counter()
for dp, dn, fn in os.walk("04-题库"):
    if '_归档' in dp or '_archive' in dp or '元文件' in dp:
        continue
    for f in fn:
        if not f.endswith('.md'):
            continue
        fp = os.path.join(dp, f)
        try:
            lines = open(fp, encoding="utf-8", errors="replace").read().split("\n")
        except OSError:
            continue
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
            c_dd = s.count('$$')
            if c_dd:
                if c_dd % 2 == 1:
                    in_disp = not in_disp; continue
                if in_disp:
                    continue
            if in_disp: continue
            if s.startswith('<!--') or s.endswith('-->'): continue
            total_in += raw.count('^θ')
            m = mask(raw)
            for mo in TOK.finditer(m):
                total_out += 1
                rows.append((fp.replace("\\", "/"), idx, mo.group(1) + '^θ' + mo.group(2), raw.strip()))
                ctxs[mo.group(1) + '^θ' + mo.group(2)] += 1

print("题源 `^θ` 总数 %d（含数学区）；**数学区之外 %d 处**" % (total_in, total_out))
print("涉及文件 %d" % len(set(r[0] for r in rows)))
print()
print("=== 前 6 个 token 频次 ===")
for k, v in ctxs.most_common(6):
    print("  %-14s %d" % (k, v))
print()
print("=== 原始行样例（20 条）===")
seen = set()
for p, i, t, raw in rows:
    key = p.split('/')[-1]
    if key in seen:
        continue
    seen.add(key)
    print("  %s L%d" % (p.split('/')[-1][:58], i))
    print("     %s" % raw[:190])
    if len(seen) >= 20:
        break
