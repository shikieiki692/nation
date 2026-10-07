#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""scan_ovf2.py —— 严判：原答案区 vs 现答案区的「本卡小问组」数量差 ⇒ 疑似误删。"""
import glob, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
sys.path.insert(0, os.path.join(R, ".workbuddy/tmp/opt_pipe"))
sys.argv = ["x", "--vol", "SC2", "--all-years"]
import build_org as BO
KEYS = ("题-CM-79-04", "题-CM-84-01", "题-CM-68-03", "题-CM-58-05", "题-CM-65-05", "题-CM-60-03", "题-CM-62-04")
for sub in ("ovf_backup", "ovf2_backup"):
    BK = os.path.join(R, ".workbuddy/tmp/opt_pipe", sub)
    fs = sorted(glob.glob(os.path.join(BK, "*.orig")))
    print("=" * 98)
    print("【%s】%d 份" % (sub, len(fs)))
    for f in fs:
        bn = os.path.basename(f)[:-5]
        hits = glob.glob(os.path.join(R, "04-题库/2026机构初赛模拟题/**/") + bn, recursive=True)
        if not hits:
            continue
        p = hits[0]
        t0 = open(f, encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")
        t1 = open(p, encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")

        def ans(t):
            j = t.find("## 参考答案"); k = t.find("## 知识点映射")
            return t[j + len("## 参考答案"):k] if 0 < j < k else ""
        a0, a1 = ans(t0), ans(t1)
        own = BO.own_qno(t1, p)
        if not own:
            continue
        pat = re.compile(r'(?m)^[ \t]*(?:#{1,4}[ \t]*)?\*{0,2}[ \t]*%d\s*[-－]\s*\d{1,2}(?![0-9])' % own)
        n0, n1 = len(pat.findall(a0)), len(pat.findall(a1))
        if n0 > n1:
            flag = "★误删" if bn.startswith(KEYS) else "  ?"
            print("%s %-54s own=%-3s 本卡小问 %d → %d | 答案区 %d → %d 字" % (flag, bn[:54], own, n0, n1, len(a0), len(a1)))
