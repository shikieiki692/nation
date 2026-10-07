import csv, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, ".workbuddy/tmp/opt_pipe")
sys.argv = ["x", "--vol", "LK5", "--all-years"]
import build_org as BO
R = r"C:\Obsidion\妙妙屋"
rows = [r for r in csv.DictReader(open(os.path.join(R, "09-审计报告/2026-10-07-不可组卷题目清单.csv"), encoding="utf-8-sig"))
        if r["reason"] == "题面泄露"]

# 题头：`第N<题/題/愿/腰/段/顾> … （N 分…`  （限 12 字以内接到分值括注）
HDR = re.compile(r'第\s*(\d{1,2})\s*[题題愿腰段顾][^\n]{0,14}[（(]\s*\d+\s*分')

def strip_title(q, own):
    return "\n".join(l for l in q.split("\n")
                     if not re.match(r'^#{0,4}\s*第\s*%d\s*[题題愿腰段顾]\s*[（(]' % own, l.strip()))

ok, bad = [], []
for r in rows:
    p = os.path.join(R, r["path"])
    t = open(p, encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")
    own = BO.own_qno(t, p)
    c = BO.X.extract(p)
    q = BO.html_table_to_md(BO.conv_imgs(BO.clean_q(c["question"])))
    q1 = strip_title(q, own)
    pos = None
    for m in HDR.finditer(q1):
        if own is None or int(m.group(1)) != own:
            pos = m.start(); break
    q2 = q1[:pos].rstrip() if pos is not None else q1
    if not BO.LEAK.search(q2):
        ok.append((r, own, pos, len(q2)))
    else:
        bad.append((r, own, q2, list(dict.fromkeys(x.group(0) for x in BO.LEAK.finditer(q2)))))

print("题面泄露 %d 张" % len(rows))
print("✅ 可救：%d" % len(ok))
for r, own, pos, l in ok:
    print("   own=%-3s pos=%-5s 留%-5d %s" % (own, pos, l, os.path.basename(r["path"])[:54]))
print("❌ 仍泄露：%d" % len(bad))
for r, own, q2, hits in bad:
    print("   own=%-3s %-50s 残留 %s" % (own, os.path.basename(r["path"])[:50], hits[:3]))
