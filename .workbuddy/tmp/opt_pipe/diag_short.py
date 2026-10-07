import csv, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, ".workbuddy/tmp/opt_pipe")
sys.argv = ["x", "--vol", "SH", "--all-years"]
import build_org as BO
R = r"C:\Obsidion\妙妙屋"
rows = [r for r in csv.DictReader(open(os.path.join(R, "09-审计报告/2026-10-07-不可组卷题目清单.csv"), encoding="utf-8-sig"))
        if r["reason"] in ("题面/答案过短", "假结构式")]
for r in rows:
    p = os.path.join(R, r["path"])
    t = open(p, encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")
    i = t.find("## 题目"); j = t.find("## 参考答案"); k = t.find("## 知识点映射")
    qraw, araw = t[i:j], t[j:k]
    c = BO.X.extract(p)
    q = BO.html_table_to_md(BO.conv_imgs(BO.clean_q(c["question"])))
    a = BO.html_table_to_md(BO.clean_a(BO.conv_imgs(c["answer"]), BO.conv_imgs(BO.clean_q(c["question"]))))
    qi = len(re.findall(r"!\[", qraw)); ai = len(re.findall(r"!\[", araw))
    # 清洗后纯字数 + 图数
    print("=" * 100)
    print("[%s] %s | %s" % (r["reason"], os.path.basename(p)[:52], r["inst"]))
    print("  原文: 题面 %4d 字/%d 图 | 答案 %4d 字/%d 图" % (len(qraw), qi, len(araw), ai))
    print("  清洗: 题面 %4d 字/%d 图 | 答案 %4d 字/%d 图" %
          (len(re.sub(r"\s+", "", q)), len(re.findall(r"!\[", q)), len(re.sub(r"\s+", "", a)), len(re.findall(r"!\[", a))))
    print("  题面(清洗) 前 160: %s" % re.sub(r"\s+", " ", q)[:160])
    print("  答案(清洗) 前 160: %s" % re.sub(r"\s+", " ", a)[:160])
