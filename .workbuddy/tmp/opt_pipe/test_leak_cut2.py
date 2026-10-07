import csv, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, ".workbuddy/tmp/opt_pipe")
sys.argv = ["x", "--vol", "LK4", "--all-years"]
import build_org as BO
R = r"C:\Obsidion\妙妙屋"
rows = [r for r in csv.DictReader(open(os.path.join(R, "09-审计报告/2026-10-07-不可组卷题目清单.csv"), encoding="utf-8-sig"))
        if r["reason"] == "题面泄露"]

# 题头特征：括注里带「占 X% / 占比 X%」
HDRPCT = re.compile(r'[（(]\s*\d+\s*分[^）)]{0,40}占\s*比?\s*\d*\s*%')

def strip_title(q, own):
    out = []
    for l in q.split("\n"):
        if re.match(r'^#{0,4}\s*第\s*%d\s*[题題][（(]' % own, l.strip()):
            continue
        out.append(l)
    return "\n".join(out)

ok, bad = [], []
for r in rows:
    p = os.path.join(R, r["path"])
    t = open(p, encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")
    own = BO.own_qno(t, p)
    c = BO.X.extract(p)
    q = BO.html_table_to_md(BO.conv_imgs(BO.clean_q(c["question"])))
    q1 = strip_title(q, own)
    m = HDRPCT.search(q1)
    q2 = q1[:m.start()].rstrip() if m else q1
    if not BO.LEAK.search(q2):
        ok.append((r, own, (m.start() if m else None), len(q2)))
    else:
        bad.append((r, own, q2, list(dict.fromkeys(x.group(0) for x in BO.LEAK.finditer(q2)))))

print("题面泄露 %d 张" % len(rows))
print("✅ 剥自身标题 + 截断到题头 ⇒ 可救：%d" % len(ok))
for r, own, pos, l in ok:
    print("   own=%-3s pos=%-5s 留%-5d %s" % (own, pos, l, os.path.basename(r["path"])[:54]))
print("❌ 仍泄露：%d" % len(bad))
for r, own, q2, hits in bad:
    print("   own=%-3s %-50s 残留 %s" % (own, os.path.basename(r["path"])[:50], hits[:3]))
