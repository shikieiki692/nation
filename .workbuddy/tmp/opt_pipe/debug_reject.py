#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""debug_reject.py —— 对 A 类弃卡输出「判据命中证据」，核实是否误杀。"""
import csv, collections, re, sys, os
sys.stdout.reconfigure(encoding="utf-8")
_orig = list(sys.argv)                      # ★ import build_org 会重置 sys.argv，先留存
R = r"C:\Obsidion\妙妙屋"
sys.path.insert(0, R + r"\.workbuddy\tmp\opt_pipe")
sys.argv = ["debug_reject.py", "--vol", "DBG", "--all-years"]
import build_org as BO
X, B = BO.X, BO.B

rows = [r for r in csv.DictReader(open(R + "/09-审计报告/2026-10-07-不可组卷题目清单.csv", encoding="utf-8-sig"))
        if r["klass"] == "A"]
want = _orig[_orig.index("--reason") + 1] if "--reason" in _orig else None
lim = int(_orig[_orig.index("--limit") + 1]) if "--limit" in _orig else 6

shown = collections.Counter()
for r in rows:
    if want and r["reason"] != want:
        continue
    if shown[r["reason"]] >= lim:
        continue
    shown[r["reason"]] += 1
    p = R + "/" + r["path"]
    t = open(p, encoding="utf-8", errors="replace").read()
    try:
        c = X.extract(p)
    except Exception as e:
        print("【提取异常】%s %s" % (r["path"].split("/")[-1][:50], e)); continue
    rawq, rawa = c["question"], c["answer"]
    print("═" * 92)
    print("【%s】%s" % (r["reason"], r["path"].split("/")[-1][:56]))
    if r["reason"] == "无答案/占位":
        mq = BO.PLACEHOLDER.search(rawq); ma = BO.PLACEHOLDER.search(rawa)
        print("   PLACEHOLDER 命中题面:", mq.group(0) if mq else None,
              "| 命中答案:", ma.group(0) if ma else None)
        print("   答案含 '![' :", "![" in rawa, "| 答案长:", len(rawa))
        if ma:
            i = ma.start(); print("   答案上下文:", re.sub(r"\s+", " ", rawa[max(0, i - 60):i + 60]))
    elif r["reason"] == "题面泄露":
        for m in BO.LEAK.finditer(rawq):
            i = m.start(); print("   LEAK 命中 %r → %s" % (m.group(0), re.sub(r"\s+", " ", rawq[max(0, i - 70):i + 70])))
    elif r["reason"] == "答案公式未转录":
        print("   rawa长=%d rawa.$=%d rawq.$=%d 答案含图=%s" % (len(rawa), rawa.count("$"), rawq.count("$"), "![" in rawa))
    elif r["reason"] == "题面/答案过短":
        q0 = BO.conv_imgs(BO.clean_q(rawq)); a0 = BO.clean_a(BO.conv_imgs(rawa), q0)
        q, a = BO.html_table_to_md(q0), BO.html_table_to_md(a0)
        print("   raw: q=%d a=%d | 清洗后: q=%d a=%d" % (
            len(re.sub(r"\s+", "", rawq)), len(re.sub(r"\s+", "", rawa)),
            len(re.sub(r"\s+", "", q)), len(re.sub(r"\s+", "", a))))
        print("   答案尾 150:", re.sub(r"\s+", " ", a)[-150:])
    elif r["reason"] == "越界（含他题内容）":
        own = BO.own_qno(t, p)
        print("   本卡题号=%s | 原因=%s" % (own, BO.overflow_reason(
            BO.html_table_to_md(BO.conv_imgs(BO.clean_q(rawq))),
            BO.html_table_to_md(BO.clean_a(BO.conv_imgs(rawa), BO.conv_imgs(BO.clean_q(rawq)))), own)))
    elif r["reason"] == "假结构式":
        for nm, s in (("题面", rawq), ("答案", rawa)):
            for body in BO.ARR_FAKE.findall(s):
                for l in [x.strip() for x in re.split(r"(?<!\\)\\\\", body) if x.strip()]:
                    if re.fullmatch(r"[|/]+", l) or (re.match(r"^[|/]", l) and len(l) < 60) or \
                       (re.search(r"[|/]$", l) and len(l) < 60 and re.search(r"[\u4e00-\u9fffA-Za-z]", l)):
                        print("   %s 假结构行: %r" % (nm, l[:60])); break
    elif r["reason"] == "题名泄露":
        tm = re.search(r"^#{2,4}\s*第\s*[0-9一二三四五六七八九十]+\s*题\s*[.．、]?\s*"
                       r"(?:[（(][^）)\n]*[）)])?\s*([^\n（(]{2,26}?)\s*(?:[（(]|$)", rawq, re.M)
        print("   题名=%r | LEAK=%s" % (tm.group(1) if tm else None,
                                        BO.LEAK.search(tm.group(1)).group(0) if tm and BO.LEAK.search(tm.group(1)) else None))
    elif r["reason"] == "手写稿口语/涂鸦":
        s = BO._HW_STRIP.sub(" ", BO.html_table_to_md(BO.conv_imgs(BO.clean_q(rawq))) + " " +
                             BO.html_table_to_md(BO.clean_a(BO.conv_imgs(rawa), BO.conv_imgs(BO.clean_q(rawq)))))
        for m in BO.HANDWRITTEN.finditer(s):
            i = m.start(); print("   HANDWRITTEN %r → %s" % (m.group(0), s[max(0, i - 60):i + 60])); break
