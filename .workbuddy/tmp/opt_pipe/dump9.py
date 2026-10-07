import csv, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, ".workbuddy/tmp/opt_pipe")
sys.argv = ["x", "--vol", "D9", "--all-years"]
import build_org as BO
R = r"C:\Obsidion\妙妙屋"
rows = [r for r in csv.DictReader(open(os.path.join(R, "09-审计报告/2026-10-07-不可组卷题目清单.csv"), encoding="utf-8-sig"))
        if r["reason"] in ("题面/答案过短",)]
for r in rows:
    p = os.path.join(R, r["path"])
    t = open(p, encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")
    i = t.find("## 题目"); j = t.find("## 参考答案"); k = t.find("## 知识点映射")
    araw = t[j:k]
    c = BO.X.extract(p)
    a = BO.html_table_to_md(BO.clean_a(BO.conv_imgs(c["answer"]), BO.conv_imgs(BO.clean_q(c["question"]))))
    print("=" * 100)
    print("%s | 答案区原文 %d 字/%d 图 → 清洗后 %d 字/%d 图"
          % (os.path.basename(p)[:54], len(araw), len(re.findall(r"!\[", araw)), len(re.sub(r"\s+", "", a)), len(re.findall(r"!\[", a))))
    print("--- 答案区原文 前 700 ---")
    print(re.sub(r"\n{3,}", "\n\n", araw)[:700])
