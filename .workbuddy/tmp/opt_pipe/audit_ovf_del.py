#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""audit_ovf_del.py —— 打印 round-1 被删段（供判断「删的是他题内容还是本卡答案」）。"""
import difflib, glob, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
BK = os.path.join(R, ".workbuddy/tmp/opt_pipe/ovf_backup")
sys.path.insert(0, os.path.join(R, ".workbuddy/tmp/opt_pipe"))
sys.argv = ["x", "--vol", "AD", "--all-years"]
import build_org as BO
ONLY = sys.argv[0] and os.environ.get("KEYS", "")
want = [k for k in ONLY.split(",") if k]
for f in sorted(glob.glob(os.path.join(BK, "*.orig"))):
    bn = os.path.basename(f)[:-5]
    if want and not any(w in bn for w in want):
        continue
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
    pat = re.compile(r'(?m)^[ \t]*(?:#{1,4}[ \t]*)?\*{0,2}[ \t]*(\d{1,2})\s*[-－]\s*\d{1,2}(?![0-9])')
    kept = set(x.strip() for x in a1.split("\n"))
    deleted = [l for l in a0.split("\n") if l.strip() and l.strip() not in kept]
    print("=" * 100)
    print("%s | own=%s | 原答案区 %d → 现 %d | 视为删除的行 %d" % (bn[:56], own, len(a0), len(a1), len(deleted)))
    # 被删段里出现的「行首小问组」编号
    nums = sorted(set(int(m.group(1)) for l in deleted for m in [pat.match(l)] if m))
    print("   被删行中出现的小问组编号: %s（本卡 own=%s）" % (nums[:20], own))
    print("   --- 被删段 头 420 ---")
    print(re.sub(r"\n{2,}", "\n", "\n".join(deleted))[:420])
    print("   --- 被删段 尾 200 ---")
    print(re.sub(r"\n{2,}", "\n", "\n".join(deleted))[-200:])
