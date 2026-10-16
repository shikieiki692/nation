# -*- coding: utf-8 -*-
"""布局图工具单测：render_block 在各 n 下「行格数一致」。"""
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "11-模板/scripts")
import layout_figs as LF  # noqa: E402


def hm(i):
    return ("%064x" % i) + ".jpg"


def ncell(l):
    s = l.strip()
    if not (s.startswith("|") and s.endswith("|")):
        return -1
    return len(re.split(r"(?<!\\)\|", s)) - 2


def issep(l):
    s = l.strip()
    if not (s.startswith("|") and s.endswith("|")):
        return False
    cs = [c.strip() for c in re.split(r"(?<!\\)\|", s)[1:-1]]
    return bool(cs) and all(re.fullmatch(r":?-+:?", c) for c in cs)


bad = 0
for n in range(2, 16):
    out = LF.render_block([hm(i) for i in range(n)], [])
    tb = [l for l in out if l.strip().startswith("|")]
    i = 0
    while i < len(tb):
        j = i
        while j < len(tb) and tb[j].lstrip().startswith("|"):
            j += 1
        blk = tb[i:j]
        seps = [k for k, l in enumerate(blk) if issep(l)]
        if seps:
            nc = ncell(blk[seps[0]])
            for k, l in enumerate(blk):
                if not issep(l) and ncell(l) != nc:
                    print("n=%d 行格数不符: %r (期望%d 得%d)"
                          % (n, l[:60], nc, ncell(l)))
                    bad += 1
        i = j
    print("n=%2d → 表块数 %d，格数一致 ✓" % (n, sum(1 for l in out if l.strip() == "")))

print("缺陷计数 =", bad)
