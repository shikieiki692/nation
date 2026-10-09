# -*- coding: utf-8 -*-
"""验证 fbase 双上下标扩展：单/双形态、守卫、幂等。"""
import sys, collections
sys.path.insert(0, r"C:\Obsidion\妙妙屋\.workbuddy\tmp\opt_pipe")
import volpost as V
sys.stdout.reconfigure(encoding="utf-8")

WANT = ("fspace", "fbase", "fbase2", "fempty")
RULES = [(n, r, p) for n, r, p in V.RULES if n in WANT]


def apply(t):
    for _, rx, rep in RULES:
        t = rx.sub(lambda m, _r=rep: _r(m) if callable(_r) else m.expand(_r), t)
    return t


CASES = [
    (r"SbCl $_{6}^{-}$ 与 X", r"$\mathrm{SbCl}_{6}^{-}$ 与 X"),
    (r"BF $_{4}^{-}$ 介导", r"$\mathrm{BF}_{4}^{-}$ 介导"),
    (r"TEMPO $^{+}$ BF$_{4}^{-}$", r"$\mathrm{TEMPO}^{+}$ $\mathrm{BF}_{4}^{-}$"),
    (r"CrF $_{6}$ 晶体", r"$\mathrm{CrF}_{6}$ 晶体"),
    (r"KO $^{t}$Bu 试剂", r"KO$^{t}$Bu 试剂"),
    (r"[8]CPP $^{2+}$ 具有", r"[8]$\mathrm{CPP}^{2+}$ 具有"),
    (r"$10^{-4}$ 与 10$^{-4}$", r"$10^{-4}$ 与 $10^{-4}$"),
    (r"Fe $^{3+}$ $_{2}$ 反常", r"$\mathrm{Fe}^{3+}$ $_{2}$ 反常"),
    (r"Xe $^{IV}$ 与 XeF $_{4}$", r"$\mathrm{Xe}^{IV}$ 与 $\mathrm{XeF}_{4}$"),
]
ok = 0
for src, exp in CASES:
    got = apply(src)
    flag = "✅" if got == exp else "❌"
    if got == exp:
        ok += 1
    print("%s  %-32s → %s" % (flag, src, got))
    if got != exp:
        print("     期望: %s" % exp)
print("通过 %d/%d" % (ok, len(CASES)))
print("幂等:", all(apply(apply(s)) == apply(s) for s, _ in CASES))
