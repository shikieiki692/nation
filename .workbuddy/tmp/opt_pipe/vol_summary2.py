# -*- coding: utf-8 -*-
"""模拟卷现状汇总 v2：题数/总分/模块/机构/难度分布。"""
import os, re, sys, json
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
O = os.path.join(R, ".workbuddy", "tmp", "opt_pipe")
VOLS = ["X", "XIp", "XI", "XII", "XIII", "XIV", "XV", "XVI"]


def fm_of(path):
    t = open(path, encoding="utf-8-sig").read()
    i = t.find("---", 3)
    fm = t[3:i]
    d = {}
    for k in ("difficulty", "source_norm", "source_subject"):
        m = re.search(r"^%s:\s*(.+)$" % k, fm, re.M)
        d[k] = m.group(1).strip().strip('"') if m else ""
    return d


print("%-5s %4s %6s %-24s %-4s %s" % ("卷", "题数", "总分", "模块配比", "机构", "难度分布"))
print("-" * 96)
tot_q = 0
for v in VOLS:
    p = os.path.join(O, "vol_plan_%s.json" % v)
    d = json.load(open(p, encoding="utf-8"))
    nq = ns = 0; mods = []; insts = set(); dd = {}
    for mod, lst in d:
        mods.append("%s%d" % (mod[:2], len(lst)))
        nq += len(lst)
        for c in lst:
            ns += c.get("score", 0) or 0
            f = fm_of(os.path.join(R, c["path"]))
            insts.add(c.get("src_dir", "?"))
            dd[f["difficulty"] or "?"] = dd.get(f["difficulty"] or "?", 0) + 1
    tot_q += nq
    dstr = " ".join("⭐%s×%d" % (k, dd[k]) for k in sorted(dd))
    print("%-5s %4d %6d %-24s %-4d %s" % (v, nq, ns, "＋".join(mods), len(insts), dstr))
print("-" * 96)
print("合计 8 卷：%d 题" % tot_q)
