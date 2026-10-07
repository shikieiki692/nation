import csv, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
rows = [r for r in csv.DictReader(open(os.path.join(R, "09-审计报告/2026-10-07-不可组卷题目清单.csv"), encoding="utf-8-sig"))
        if r["reason"] == "无答案/占位"]
KEYS = ("题-GChO-26-09", "题-GChO-54-09", "题-CM-58-05", "题-CM-60-03", "题-CM-62-04", "题-CM-65-05", "题-CM-68-03")
for r in rows:
    bn = os.path.basename(r["path"])
    if not bn.startswith(KEYS):
        continue
    p = os.path.join(R, r["path"])
    t = open(p, encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")
    j = t.find("## 参考答案"); k = t.find("## 知识点映射")
    a = t[j:k]
    print("=" * 96)
    print("%s | 答案区 %d 字 | 含图 %d" % (bn[:58], len(a), a.count("![")))
    print(re.sub(r"\n{2,}", "\n", a)[:520])
