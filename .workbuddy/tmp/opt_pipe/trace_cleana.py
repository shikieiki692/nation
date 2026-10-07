import os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, ".workbuddy/tmp/opt_pipe")
sys.argv = ["x", "--vol", "TR", "--all-years"]
import build_org as BO
R = r"C:\Obsidion\妙妙屋"
P = os.path.join(R, "04-题库/2026机构初赛模拟题/化英社/题-HYS-40-03-低配位超价磷物种是磷化学的研.md")
c = BO.X.extract(P)
print("extract: 题面 %d 字/%d 图 | 答案 %d 字/%d 图" %
      (len(c["question"]), c["question"].count("!["), len(c["answer"]), c["answer"].count("![")))
q = BO.conv_imgs(BO.clean_q(c["question"]))
print("clean_q 后 题面 %d 字/%d 图" % (len(q), q.count("![")))
a = BO.conv_imgs(c["answer"])
print("conv_imgs 后 答案 %d 字/%d 图" % (len(a), a.count("![")))
steps = [
    ("strip_src_heading", lambda x: BO.strip_src_heading(x)),
    ("flatten_layout_tables", lambda x: BO.flatten_layout_tables(x)),
    ("drop_empty_headings", lambda x: BO.drop_empty_headings(x)),
    ("flatten_subq_headings", lambda x: BO.flatten_subq_headings(x)),
    ("drop_wm_text", lambda x: BO.drop_wm_text(x)),
    ("strip_artifacts", lambda x: BO.strip_artifacts(x)),
    ("fix_orphan_tables", lambda x: BO.fix_orphan_tables(x)),
    ("fix_tex", lambda x: BO.fix_tex(x)),
]
y = a
for name, fn in steps:
    y = fn(y)
    print("  %-24s → %5d 字/%2d 图" % (name, len(y), y.count("![")))
q2 = q
for name, fn in steps:
    q2 = fn(q2)
print("--- 题面同样过一遍（不含 strip_q_echo）→ %d 字/%d 图" % (len(q2), q2.count("![")))
z = BO.strip_q_echo(q, y)
print("strip_q_echo 后 答案 → %4d 字/%2d 图" % (len(z), z.count("![")))
