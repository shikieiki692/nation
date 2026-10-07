import csv, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
key = sys.argv[1:]
rows = list(csv.DictReader(open(os.path.join(R, "09-审计报告/2026-10-07-不可组卷题目清单.csv"), encoding="utf-8-sig")))
for r in rows:
    bn = os.path.basename(r["path"])
    if not any(k in bn for k in key):
        continue
    p = os.path.join(R, r["path"])
    t = open(p, encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")
    j = t.find("## 参考答案"); k = t.find("## 知识点映射")
    a = t[j + len("## 参考答案"):k]
    print("=" * 100)
    print("%s | %s | 答案 %d 字" % (r["reason"], bn[:62], len(a)))
    off = 0
    for ln in a.split("\n"):
        s = ln.rstrip()
        if s.strip():
            print("%6d| %s" % (off, s[:140]))
        off += len(ln) + 1
