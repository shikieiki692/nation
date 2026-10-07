import csv, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
BK = os.path.join(R, ".workbuddy/tmp/opt_pipe/ovf_backup")
rows = [r for r in csv.DictReader(open(os.path.join(R, "09-审计报告/2026-10-07-不可组卷题目清单.csv"), encoding="utf-8-sig"))
        if r["reason"] == "无答案/占位"]
KEYS = ("题-CM-58-05", "题-CM-60-03", "题-CM-62-04", "题-CM-65-05", "题-CM-68-03")
for r in rows:
    bn = os.path.basename(r["path"])
    if not bn.startswith(KEYS):
        continue
    old = os.path.join(BK, bn + ".orig")
    if not os.path.exists(old):
        print("！无备份", bn); continue
    t0 = open(old, encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")
    t1 = open(os.path.join(R, r["path"]), encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")
    def ans(t):
        j = t.find("## 参考答案"); k = t.find("## 知识点映射")
        return t[j + len("## 参考答案"):k]
    a0, a1 = ans(t0), ans(t1)
    print("=" * 98)
    print("%s | 原答案区 %d 字 → 现 %d 字" % (bn[:52], len(a0), len(a1)))
    print("  【原答案区全文】")
    print(re.sub(r"\n{2,}", "\n", a0)[:1100])
