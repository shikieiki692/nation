import csv, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, ".workbuddy/tmp/opt_pipe")
sys.argv = ["x", "--vol", "DG4", "--all-years"]
import build_org as BO
R = r"C:\Obsidion\妙妙屋"

rows = [r for r in csv.DictReader(open(os.path.join(R, "09-审计报告/2026-10-07-不可组卷题目清单.csv"), encoding="utf-8-sig"))
        if r["reason"] == "越界（含他题内容）"]

PAT = re.compile(r'(?m)^[ \t]*(?:#{1,4}[ \t]*)?\*{0,2}[ \t]*(\d{1,2})\s*[-－]\s*\d{1,2}(?![0-9])')

for r in rows:
    p = os.path.join(R, r["path"])
    t = open(p, encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")
    j = t.find("## 参考答案"); k = t.find("## 知识点映射")
    own = BO.own_qno(t, p)
    a = t[j:k]
    hits = [(m.start(), int(m.group(1)), m.group(0).strip()) for m in PAT.finditer(a)]
    ovf = [h for h in hits if own and h[1] > own]
    after_own = [h for h in hits if own and h[1] == own and ovf and h[0] > ovf[0][0]]
    print("=" * 96)
    print("%s | own=%s | 答案 %d 字" % (os.path.basename(p)[:52], own, len(a)))
    if ovf:
        c0 = ovf[0][0]
        print("  首个越界点 off=%d token=%r | 之后留 %d 字 | 其后仍有本卡 own-%s 组: %s"
              % (c0, ovf[0][2], len(a) - c0, own, [x[2] for x in after_own[:4]] or "无"))
        print("     越界点前 90: …%s…" % re.sub(r"\s+", " ", a[max(0, c0 - 90):c0]))
        print("     越界点后 110: …%s…" % re.sub(r"\s+", " ", a[c0:c0 + 110]))
