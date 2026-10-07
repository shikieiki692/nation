import csv, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, ".workbuddy/tmp/opt_pipe")
sys.argv = ["x", "--vol", "LK", "--all-years"]
import build_org as BO
R = r"C:\Obsidion\妙妙屋"
rows = [r for r in csv.DictReader(open(os.path.join(R, "09-审计报告/2026-10-07-不可组卷题目清单.csv"), encoding="utf-8-sig"))
        if r["reason"] == "题面泄露"]
keys = sys.argv[0] and os.environ.get("KEYS", "")
want = [k.strip() for k in (os.environ.get("KEYS") or "").split(",") if k.strip()]
for r in rows:
    bn = os.path.basename(r["path"])
    if want and not any(w in bn for w in want):
        continue
    p = os.path.join(R, r["path"])
    t = open(p, encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")
    i = t.find("## 题目"); j = t.find("## 参考答案")
    c = BO.X.extract(p)
    q = BO.html_table_to_md(BO.conv_imgs(BO.clean_q(c["question"])))
    print("=" * 100)
    print("%-12s %s | 题面 %d 字" % (r["inst"], bn[:56], len(t[i:j])))
    seen = set()
    for m in BO.LEAK.finditer(q):
        if m.group(0) in seen:
            continue
        seen.add(m.group(0))
        s = max(0, m.start() - 130)
        print("   [%s] …%s…" % (m.group(0), re.sub(r"\s+", " ", q[s:m.end() + 90])))
