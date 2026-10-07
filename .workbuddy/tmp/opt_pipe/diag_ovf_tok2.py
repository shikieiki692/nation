import csv, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, ".workbuddy/tmp/opt_pipe")
sys.argv = ["x", "--vol", "DG3", "--all-years"]
import build_org as BO
R = r"C:\Obsidion\妙妙屋"

rows = [r for r in csv.DictReader(open(os.path.join(R, "09-审计报告/2026-10-07-不可组卷题目清单.csv"), encoding="utf-8-sig"))
        if r["reason"] == "越界（含他题内容）"]

_NOTE = re.compile(r'^(?:[>]+\s*)*(?:📎|⛔|📄)|答案出处[：:]|[（(]源 ?PDF|未逐字校对'
                   r'|文字层自动提取|文字化需人工转录|源卷答案')

for r in rows:
    p = os.path.join(R, r["path"])
    t = open(p, encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")
    own = BO.own_qno(t, p)
    c = BO.X.extract(p)
    q = BO.html_table_to_md(BO.conv_imgs(BO.clean_q(c["question"])))
    a = BO.html_table_to_md(BO.clean_a(BO.conv_imgs(c["answer"]), BO.conv_imgs(BO.clean_q(c["question"]))))
    a_chk = "\n".join(l for l in a.split("\n") if l.strip() and not _NOTE.search(l.strip()))
    print("=" * 100)
    print("%s | own=%s" % (os.path.basename(p)[:56], own))
    for m in BO.SUBQ_HEAD_RE.finditer(a_chk):
        if int(m.group(1)) > own:
            line0 = a_chk.rfind("\n", 0, m.start()) + 1
            line1 = a_chk.find("\n", m.start())
            print("   [清理后·小问组] %-14s 行: %s" % (repr(m.group(0)), a_chk[line0:line1 if line1 > 0 else len(a_chk)][:96]))
    for m in BO.QW_RE.finditer(a_chk):
        n = BO._cn2int(m.group(1))
        if n and n > own:
            s = max(0, m.start() - 55)
            print("   [清理后·第N题] %s: …%s…" % (m.group(0), re.sub(r"\s+", " ", a_chk[s:m.end() + 35])))
