#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""group_gate.py —— 组卷前置闸门（答案泄露 / 题面丢失 / 一卡多题）

🔴 为什么必须有这个闸门
   组卷器 build_multi/build_org 通过 `mv_extract.extract()` 切分题面与答案，而该函数
   **只认「独立成行的 ##参考答案/解答/答案/详解/解析」或 `<details>` 折叠块** 作为答案起点。
   若一张卡的答案写成 `**答案**：` 内联行 / `> **答案**：` 引用块 / 裸行 `答案：`，
   抽取器会把**整张卡当成题面** ⇒ 学生版直接印出答案。
   2026-10-07 全库实测：未治理前 161 张卡存在该风险（占在役卡 2.64%）。

   本闸门用**同一个抽取器**对候选卡实跑，把风险拦在组卷之前。
   ⚠️ 与 render_gate 相同：pre-commit 有时间预算会漏检，本闸门须**显式运行**。

用法
----
    python -X utf8 11-模板/scripts/group_gate.py --all
    python -X utf8 11-模板/scripts/group_gate.py --cards 选卡清单.txt
    python -X utf8 11-模板/scripts/group_gate.py --domain 04-题库/教材习题/赵鑫光

分级
----
    FATAL  答案泄露（学生版会印出答案）／题面为空  ⇒ 退出码 1，必须阻止组卷
    WARN   一卡多题／无答案可用／题面指图但无图     ⇒ 退出码 0，但需人工确认

退出码：0 = 无 FATAL；1 = 有 FATAL；2 = 参数/依赖错误
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, ".workbuddy", "tmp"))

EXCLUDE_TOP = ("2026机构初赛模拟题", "元文件", "_归档")

ANS_HINT = re.compile(
    r"(\*\*答案\*\*|【答案】|参考答案[::]|答案[::：]\s*\S|解答[::：|解\s*[::：]\s*\S|解析[::：])")
ANS_PTS = [
    re.compile(r"^\*\*答案\*\*[ \t]*[:：]", re.M),
    re.compile(r"^>[ \t]*\*\*答案\*\*[ \t]*[:：]", re.M),
    re.compile(r"^[ \t]*\*{0,2}答案\*{0,2}[ \t]*[::：]", re.M),
    re.compile(r"^[ \t]*\*{0,2}(?:解析|解答)\*{0,2}[ \t]*[::：][ \t]*\S", re.M),
    re.compile(r"^#{2,4}[ \t]*\d+[.．][^\n]*答案[ \t]*$", re.M),
]
QN_HEAD = re.compile(r"^#{2,4}[ \t]*\d+[.．]\d*[^\n]{0,60}$", re.M)
QN_INLINE = re.compile(r"^[ \t]{0,4}\*{0,2}\d+[.．]\d+[^\n]{0,70}", re.M)
FIG_HINT = re.compile(r"(如下图|上图|如图所示|见图|如左图|右图|（见图片）|\[见图片\])")
IMG_REF = re.compile(r"!\[\[[^\]]+\]\]")
FM = re.compile(r"^---[ \t]*\n.*?\n---[ \t]*\n", re.S)


def load_all(domain=None):
    base = os.path.join(ROOT, domain) if domain else os.path.join(ROOT, "04-题库")
    out = []
    for b, dirs, fs in os.walk(base):
        rel = os.path.relpath(b, ROOT)
        if any(("/%s" % x) in (rel + "/") or rel.endswith(x) for x in EXCLUDE_TOP):
            continue
        for f in fs:
            if f.endswith(".md") and not f.startswith("卷-"):
                out.append(os.path.join(b, f))
    return out


def check(path):
    """返回 (fatal_list, warn_list)"""
    fatal, warn = [], []
    raw = open(path, encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")
    m = FM.match(raw)
    body = raw[m.end():] if m else raw
    if m and "type: 题目" not in m.group(0):
        return [], []
    try:
        import mv_extract as X
        d = X.extract(path)
    except Exception as e:
        return [], ["抽取失败：%s" % str(e)[:60]]
    q, a = d["question"], d["answer"]
    qn = re.sub(r"\s+", "", q)
    an = re.sub(r"\s+", "", a)

    # FATAL ①：答案为空但卡内有答案文本 ⇒ 学生版泄露
    if an == "" and ANS_HINT.search(body):
        fatal.append("答案泄露：抽取器未识别答案起点，题面=%d 字（含答案）" % len(qn))
    # FATAL ②：题面为空
    if qn == "":
        fatal.append("题面丢失：抽取后题面为空")
    # FATAL ③：题面里出现答案标记
    if an != "" and ANS_HINT.search(q):
        fatal.append("题面含答案标记（切分点选错）")

    # WARN ①：一卡多题
    n_ans = sum(len(p.findall(body)) for p in ANS_PTS)
    n_qh = len(QN_HEAD.findall(body)) + len(QN_INLINE.findall(body))
    if n_ans >= 3 or n_qh >= 3:
        warn.append("一卡多题（答案点 %d / 题号 %d）：归一会丢题，禁止直接组卷" % (n_ans, n_qh))
    # WARN ②：无答案可用
    if an == "" and not ANS_HINT.search(body):
        warn.append("无答案可用")
    # WARN ③：题面指图但无图
    if FIG_HINT.search(q) and not IMG_REF.search(q):
        warn.append("题面指图但无图")
    return fatal, warn


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true", help="扫描全部在役题卡")
    ap.add_argument("--cards", help="候选卡清单（每行一个 vault 相对路径）")
    ap.add_argument("--domain", help="限定目录（vault 相对路径）")
    ap.add_argument("--out", help="报告输出 JSON 路径")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()

    try:
        import mv_extract  # noqa: F401
    except ImportError:
        print("!! 找不到 mv_extract.py（应在 %s）" % os.path.join(ROOT, ".workbuddy", "tmp"))
        return 2

    if a.cards:
        paths = []
        for line in open(a.cards, encoding="utf-8"):
            line = line.strip().strip('"')
            if line and not line.startswith("#"):
                p = line if os.path.isabs(line) else os.path.join(ROOT, line.replace("/", os.sep))
                if os.path.exists(p):
                    paths.append(p)
    elif a.domain or a.all:
        paths = load_all(a.domain)
    else:
        ap.print_help()
        return 2

    nf = nw = 0
    rep = []
    for p in paths:
        f, w = check(p)
        if f or w:
            rel = os.path.relpath(p, ROOT).replace("\\", "/")
            rep.append({"path": rel, "fatal": f, "warn": w})
            nf += len(f)
            nw += len(w)
            if not a.quiet:
                for x in f:
                    print("  ❌ FATAL %-72s %s" % (rel[:72], x))
                for x in w:
                    print("  ⚠️ WARN  %-72s %s" % (rel[:72], x))

    print("\nGROUP_GATE=%s  受检 %d ｜ FATAL %d ｜ WARN %d"
          % ("FAIL" if nf else "PASS", len(paths), nf, nw))
    if a.out:
        json.dump(rep, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("报告 → %s" % a.out)
    return 1 if nf else 0


if __name__ == "__main__":
    sys.exit(main())