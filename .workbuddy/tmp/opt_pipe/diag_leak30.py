import csv, os, re, sys, collections
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, ".workbuddy/tmp/opt_pipe")
sys.argv = ["x", "--vol", "LG", "--all-years"]
import build_org as BO
R = r"C:\Obsidion\妙妙屋"

rows = [r for r in csv.DictReader(open(os.path.join(R, "09-审计报告/2026-10-07-不可组卷题目清单.csv"), encoding="utf-8-sig"))
        if r["reason"] == "题面泄露"]
print("题面泄露 %d 张" % len(rows))
rep = collections.Counter()
title_only = []
scr_only = []
real = []
for r in rows:
    p = os.path.join(R, r["path"])
    t = open(p, encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")
    i = t.find("## 题目"); j = t.find("## 参考答案")
    c = BO.X.extract(p)
    q = BO.html_table_to_md(BO.conv_imgs(BO.clean_q(c["question"])))
    hits = [m.group(0) for m in BO.LEAK.finditer(q)]
    # ① 去标题行
    q1 = re.sub(r'^#{2,4}[ \t]*第[ \t]*\d+[ \t]*题[^\n]*$', '', q, flags=re.M)
    if not BO.LEAK.search(q1):
        title_only.append(r); continue
    # ② 再去「评分括注」 (N 分, ...) / （N分，…）
    q2 = re.sub(r'[（(]\s*\d+\s*分[^）)]{0,80}[）)]', '（评分）', q1)
    q2 = re.sub(r'共\s*\d+\s*分[^）)。\n]{0,40}', '（评分）', q2)
    if not BO.LEAK.search(q2):
        scr_only.append(r); continue
    real.append((r, hits, q))
    print("-" * 90)
    print("%-14s %s" % (r["inst"], os.path.basename(r["path"])[:58]))
    print("   题面区 %d 字 | LEAK命中 %d 种: %s" % (len(t[i:j]), len(set(hits)), list(dict.fromkeys(hits))[:4]))
    for m in BO.LEAK.finditer(q2):
        s = max(0, m.start() - 60)
        print("     [%s] …%s…" % (m.group(0), re.sub(r"\s+", " ", q2[s:m.end() + 50])))
        break
print()
print("=== 分类小结 ===")
print("  仅标题行分值（可救）   %d" % len(title_only))
print("  仅评分括注（可救）     %d" % len(scr_only))
print("  实质泄露（难救）       %d" % len(real))
print()
for tag, lst in [("标题行", title_only), ("评分括注", scr_only)]:
    print("[%s]:" % tag)
    for r in lst:
        print("   ", os.path.basename(r["path"])[:64])
