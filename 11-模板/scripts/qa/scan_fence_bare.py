# -*- coding: utf-8 -*-
"""围栏内裸下标扫描（md 侧「换维度复检」的第二维）。

背景：`scan_bare5.py` 按设计**跳过代码围栏**（围栏内多为代码/ASCII 图）。
但习题书里有 **ASCII 表格**（相图数据表等）被 ``` 包着 —— 围栏内的 `x_B` / `w_Sn`
在 Word 里会**字面印出**，属真污染，而 scan_bare5 看不到。
本脚本只报「围栏内、且看起来像表格/数据行」的裸下标，供人工判定后去围栏或改写。

用法:
    python -X utf8 11-模板/scripts/qa/scan_fence_bare.py <目录> [<目录> ...]
"""
import os
import re
import sys
import collections

sys.stdout.reconfigure(encoding="utf-8")
os.chdir(r"c:\Obsidion\妙妙屋")

# 与 scan_bare5.py 同源（三处同改：scan_bare5 / gen_acd_list / fix_bare5 / scan_fence_bare）
SUB_UNI = "₀-₉₊₋₌₍₎ₐₑₒₓₔₕₖₗₘₙₚₛₜⁿ"
SUP_UNI = "⁰-⁹⁺⁻⁼⁽⁾ⁿ"
BODY = r"A-Za-z0-9()+\-−·/_%"
FIRSTCH = r"0-9A-Za-z()+\-−·θφλμνσπσΣΔΩ°½¼¾′″" + SUB_UNI + SUP_UNI
GREEK = r"\u0370-\u03FF\u1F00-\u1FFF"
BASE = (r"[" + GREEK + r"A-Za-z][" + GREEK + r"A-Za-z0-9]{0,14}"
        r"(?:\([A-Za-z0-9]{1,8}\))?")
PAT = re.compile(r"(?<![\\$A-Za-z0-9" + GREEK + r"])"
                 r"(" + BASE + r")"
                 r"([_^])(["
                 + FIRSTCH + r"][" + BODY + SUB_UNI + SUP_UNI + r"]{0,10})")
MEDIA_EXT = re.compile(r'\.(?:jpe?g|png|gif|webp|svg|bmp|tiff?|pdf|md|docx?|xlsx?|zip)(?:$|[|\])\s])', re.I)
# 「像表格/数据行」：含表格分隔符、或数字密度较高（ASCII 数据表特征）
TABLEISH = re.compile(r"[|｜]|^\s*[+\-─┼]+|(\d[\d.\s]{3,})")


def is_pathish(raw, a, b):
    word_re = re.compile(r'[A-Za-z0-9_\-./\\]+')
    wa, wb = a, b
    while wa > 0 and word_re.match(raw[wa - 1]):
        wa -= 1
    while wb < len(raw) and word_re.match(raw[wb]):
        wb += 1
    if MEDIA_EXT.search(raw[wa:wb]):
        return True
    ok = lambda ch: ch.isascii() and (ch.isalnum() or ch == '_')
    return (a > 0 and ok(raw[a - 1])) or (b < len(raw) and ok(raw[b]))


roots = [a for a in sys.argv[1:] if not a.startswith("--")]
hits = []
files = 0
for root in roots:
    for dp, dn, fn in os.walk(root):
        if os.path.basename(dp).startswith('_') or '_归档' in dp or '_archive' in dp:
            continue
        for f in sorted(fn):
            if not f.endswith('.md') or f.startswith('README'):
                continue
            p = os.path.join(dp, f)
            files += 1
            in_fence = False
            fence_body = []
            start = 0
            for idx, raw in enumerate(open(p, encoding="utf-8", errors="replace").read().split("\n"), 1):
                s = raw.strip()
                if s.startswith('```') or s.startswith('~~~'):
                    if in_fence and fence_body:
                        for (i2, l2) in fence_body:
                            if not TABLEISH.search(l2):
                                continue
                            for mo in PAT.finditer(l2):
                                if is_pathish(l2, mo.start(), mo.end()):
                                    continue
                                hits.append((mo.group(0), p, i2, l2))
                    in_fence = not in_fence
                    fence_body = []
                    continue
                if in_fence:
                    fence_body.append((idx, raw))

print("扫描 %d 文件（围栏内）" % files)
by = collections.defaultdict(list)
for tok, p, idx, l2 in hits:
    by[tok].append((p, idx, l2))
print("围栏内命中 %d 处 / %d token / %d 文件" % (
    len(hits), len(by), len(set(h[1] for h in hits))))
print()
for tok, items in sorted(by.items(), key=lambda kv: (-len(kv[1]), kv[0])):
    print("[%s] ×%d" % (tok, len(items)))
    for p, idx, l2 in items[:6]:
        print("   %s L%d" % (p, idx))
        print("      %s" % l2.strip()[:200])
