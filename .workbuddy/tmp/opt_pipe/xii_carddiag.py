# -*- coding: utf-8 -*-
"""逐判据诊断单卡为何掉池（卷 XII 题-GChO-03-02）。"""
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, r"C:\Obsidion\妙妙屋\.workbuddy\tmp\opt_pipe")
sys.path.insert(0, r"C:\Obsidion\妙妙屋\.workbuddy\tmp")
import build_org as BO  # noqa: E402
import build_multi as B  # noqa: E402

R = r"C:\Obsidion\妙妙屋"
REL = r"04-题库/2026机构初赛模拟题/质心GChO/题-GChO-03-02-天然气的主要成分为甲烷水合物.md"
p = os.path.join(R, REL)
t = open(p, encoding="utf-8").read()

def g(k):
    m = re.search(r"^" + k + r":\s*(.*)$", t, re.M)
    return m.group(1).strip() if m else ""

print("subject_module=%r exam_stage=%r difficulty=%r" % (g("subject_module"), g("exam_stage"), g("difficulty")))
print("source_norm=%r source_file=%r" % (g("source_norm"), g("source_file")))
print("EXCLUDE 命中:", p.replace(os.sep, "/") in BO.EXCLUDE)
print("BATCH_BAD:", bool(BO.BATCH_BAD.search(g("source_norm"))))
print("RISK:", [x for x in B.RISK if x in t])

h1m = re.search(r"^#\s+(.+)$", t, re.M)
h1 = h1m.group(1) if h1m else ""
tn = re.sub(r"<!--.*?-->", "", t, flags=re.S)
print("is_cn_prelim:", B.is_cn_prelim(tn), "| KEEP_POOL 命中:", os.path.basename(p) in BO.load_pool_keep())
print("ORG_CHAP(src):", bool(B.ORG_CHAP.search(g("source"))), "| ORG_CHAP(h1):", bool(B.ORG_CHAP.search(h1)))

c = BO.X.extract(p)
rawq, rawa = c["question"], c["answer"]
print("\nPLACEHOLDER(q):", bool(BO.PLACEHOLDER.search(rawq)))
if BO.PLACEHOLDER.search(rawa) and "![" not in rawa:
    _body = "\n".join(l for l in rawa.split("\n") if l.strip() and not BO.NOTE_LINE.search(l.strip()))
    print("PLACEHOLDER(a) 非注记净字数:", len(re.sub(r"\s+", "", _body)))
print("has_fake_struct(q/a):", BO.has_fake_struct(rawq), BO.has_fake_struct(rawa))
print("len(rawq)=%d len(rawa)=%d  $q=%d $a=%d" % (len(rawq), len(rawa), rawq.count("$"), rawa.count("$")))
q0 = BO.conv_imgs(BO.clean_q(rawq))
a0 = BO.clean_a(BO.conv_imgs(rawa), q0)
q, a = BO.html_table_to_md(q0), BO.html_table_to_md(a0)
print("LEAK(q):", bool(BO.LEAK.search(q)))
qn, an = re.sub(r"\s+", "", q), re.sub(r"\s+", "", a)
print("len(an)=%d len(qn)=%d" % (len(an), len(qn)))
print("ORGRE hits:", len(B.ORGRE.findall(q + " " + a)))
print("编号列表≥8:", len(re.findall(r"^\*\*\s*\d{1,2}\s*[.．]\s*\*\*", q + "\n" + a, re.M)))
print("HANDWRITTEN:", bool(BO.HANDWRITTEN.search(BO._HW_STRIP.sub(" ", q + " " + a))))
if "![[" not in a:
    _r = BO.contain_ratio(an, qn)
    print("回显 ratio=%.3f （≥0.80 或 ≥0.70且非回显<80 ⇒ 弃）" % _r)
    print("GARB2PAT:", bool(BO.GARB2PAT.search(a)))
_own = BO.own_qno(t, p)
print("own_qno=%r" % _own)
print("overflow_reason 命中:", BO.overflow_reason(q, a, _own))
