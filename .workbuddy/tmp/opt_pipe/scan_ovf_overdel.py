#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""scan_ovf_overdel.py —— 排查 round-1 rescue_ovf 是否误删本卡答案。
判据：备份的「原答案区」里含本卡小问组 `own-M`（说明本卡答案在被删段内）。"""
import glob, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
BK = os.path.join(R, ".workbuddy/tmp/opt_pipe/ovf2_backup")
sys.path.insert(0, os.path.join(R, ".workbuddy/tmp/opt_pipe"))
sys.argv = ["x", "--vol", "SC", "--all-years"]
import build_org as BO

notes = 0
risky = []
for f in sorted(glob.glob(os.path.join(BK, "*.orig"))):
    bn = os.path.basename(f)[:-5]
    cur = os.path.join(R, "04-题库/2026机构初赛模拟题", **{}) if False else None
    # 找现文件
    hits = glob.glob(os.path.join(R, "04-题库/2026机构初赛模拟题/**/") + bn, recursive=True)
    if not hits:
        print("！现文件缺失:", bn[:60]); continue
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
    # 原答案区里本卡小问组（行首 own-M）出现次数
    ownpat = re.compile(r'(?m)^[ \t]*(?:#{1,4}[ \t]*)?\*{0,2}[ \t]*%d\s*[-－]\s*\d{1,2}(?![0-9])' % own)
    n_own_old = len(ownpat.findall(a0))
    if n_own_old and len(re.sub(r"\s+", "", a1)) < 260:
        risky.append((bn, own, len(a0), len(a1), n_own_old, p))
print("检查 %d 份备份；疑似「误删本卡答案」 %d 张\n" % (len(glob.glob(os.path.join(BK, '*.orig'))), len(risky)))
for bn, own, l0, l1, n, p in sorted(risky, key=lambda x: -x[3]):
    print("%-56s own=%-3s 原答案区 %5d 字（含本卡小问 %d 处）→ 现 %4d 字" % (bn[:56], own, l0, n, l1))
