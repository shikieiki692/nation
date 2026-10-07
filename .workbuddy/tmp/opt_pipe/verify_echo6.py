import csv, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, ".workbuddy/tmp/opt_pipe")
sys.argv = ["x", "--vol", "V9", "--all-years"]
import build_org as BO
R = r"C:\Obsidion\妙妙屋"
rows = list(csv.DictReader(open(os.path.join(R, "09-审计报告/2026-10-07-不可组卷题目清单.csv"), encoding="utf-8-sig")))
KEYS = ("题-HYS-40-02-地球", "题-HYS-40-03-低配", "题-GM-23-02", "题-HYS-03-02-配位", "题-HYS-02-07-万物", "题-HYS-02-01-科学")
for r in rows:
    bn = os.path.basename(r["path"])
    if not bn.startswith(KEYS):
        continue
    p = os.path.join(R, r["path"])
    c = BO.X.extract(p)
    q = BO.html_table_to_md(BO.conv_imgs(BO.clean_q(c["question"])))
    a = BO.html_table_to_md(BO.clean_a(BO.conv_imgs(c["answer"]), BO.conv_imgs(BO.clean_q(c["question"]))))
    print("%-56s %-6s %-10s | 清洗后 题面 %5d 字/%-2d 图  答案 %5d 字/%-2d 图  ECHO=%.2f"
          % (bn[:56], r["verdict"], r["reason"] or "—",
             len(re.sub(r"\s+", "", q)), q.count("!["),
             len(re.sub(r"\s+", "", a)), a.count("!["),
             BO.contain_ratio(re.sub(r"\s+", "", a), re.sub(r"\s+", "", q))))
