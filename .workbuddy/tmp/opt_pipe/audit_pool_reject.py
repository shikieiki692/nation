# -*- coding: utf-8 -*-
"""audit_pool_reject.py —— 复刻 build_org.build_pool() 的判据链，
对 04-题库/2026机构初赛模拟题 全量卡逐张判定「能否进组卷池」并记录原因。

产出：
  09-审计报告/2026-10-07-不可组卷题目清单.csv   （逐卡：路径/机构/题号/模块/难度/结论/原因）
  （汇总 md 由 audit_pool_report.py 生成）
注意：判据与 build_org.py 保持一致；若 build_org 后续变更，本脚本需同步。
"""
import collections, csv, glob, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
BASE_DIR = r"C:\Obsidion\妙妙屋\.workbuddy\tmp\opt_pipe"
sys.argv = ["audit_pool_reject.py", "--vol", "AUDIT", "--all-years"]
sys.path.insert(0, BASE_DIR)
import build_org as BO          # 复用其全部判据常量与函数
X = BO.X
B = BO.B

OUT = os.path.join(BO.ROOT, "09-审计报告", "2026-10-07-不可组卷题目清单.csv")

# A 类＝内容不可用（需修）；B 类＝口径外（正常过滤）
CLASS = {
    "回源核验换卡": "A", "无答案/占位": "A", "假结构式": "A", "答案乱码（无中文）": "A",
    "题名泄露": "A", "题面泄露": "A", "手写稿口语/涂鸦": "A", "仅题干回显": "A",
    "OCR 乱码宏": "A", "越界（含他题内容）": "A", "题面/答案过短": "A",
    "有机章节": "B", "非目标模块": "B", "省预赛": "B", "年份口径外": "B",
    "讲稿批次": "B", "难度<4": "B", "RISK 命中": "B", "提取异常": "B",
    "题面含竞赛真题特征": "B", "编号列表≥8": "B",
}


def judge(p, rel):
    """→ (结论, 原因) 结论∈{入池, 弃卡}"""
    pn = p.replace(os.sep, "/")
    t = open(p, encoding="utf-8", errors="replace").read()

    def g(k):
        m = re.search(r"^" + k + r":\s*(.*)$", t, re.M)
        return m.group(1).strip() if m else ""

    mod, stage, diff = g("subject_module"), g("exam_stage"), int(g("difficulty") or 0)
    src, norm, sf = g("source"), g("source_norm"), g("source_file")
    meta = dict(inst=rel, mod=mod, stage=stage, diff=diff, src=src)

    if pn in BO.EXCLUDE:
        return "弃卡", "回源核验换卡", meta
    _recent = 1 if BO.in_2526(norm, sf) else 0
    if _recent == 0 and not BO.ALL_YEARS:
        return "弃卡", "年份口径外", meta
    if BO.BATCH_BAD.search(norm):
        return "弃卡", "讲稿批次", meta
    if mod not in ("元素与分析", "结构化学", "化学原理"):
        return "弃卡", "非目标模块", meta
    if stage == "省预赛":
        return "弃卡", "省预赛", meta
    if diff < 4:
        return "弃卡", "难度<4", meta
    if [x for x in B.RISK if x in t]:
        return "弃卡", "RISK 命中", meta
    h1m = re.search(r"^#\s+(.+)$", t, re.M)
    h1 = h1m.group(1) if h1m else ""
    tn = re.sub(r"<!--.*?-->", "", t, flags=re.S)
    if B.is_cn_prelim(tn):
        return "弃卡", "题面含竞赛真题特征", meta
    if B.ORG_CHAP.search(src) or B.ORG_CHAP.search(h1):
        return "弃卡", "有机章节", meta
    try:
        c = X.extract(p)
    except Exception:
        return "弃卡", "提取异常", meta
    rawq, rawa = c["question"], c["answer"]
    if BO.PLACEHOLDER.search(rawq):
        return "弃卡", "无答案/占位", meta
    if BO.PLACEHOLDER.search(rawa) and "![" not in rawa:
        _body = "\n".join(l for l in rawa.split("\n")
                          if l.strip() and not BO.NOTE_LINE.search(l.strip()))
        if len(re.sub(r"\s+", "", _body)) < 25:
            return "弃卡", "无答案/占位", meta
    if BO.has_fake_struct(rawa) or BO.has_fake_struct(rawq):
        return "弃卡", "假结构式", meta
    if (len(rawa) >= 400 and rawa.count("$") == 0 and rawq.count("$") >= 10
            and "![" not in rawa and not re.search(r"[\u4e00-\u9fff]", rawa)):
        return "弃卡", "答案乱码（无中文）", meta
    tm = re.search(
        r"^#{2,4}\s*第\s*[0-9一二三四五六七八九十]+\s*题\s*[.．、]?\s*"
        r"(?:[（(][^）)\n]*[）)])?\s*([^\n（(]{2,26}?)\s*(?:[（(]|$)", rawq, re.M)
    title = tm.group(1).strip() if tm else ""
    if title and BO.LEAK.search(title):
        return "弃卡", "题名泄露", meta
    if len(re.sub(r"\s+", "", rawq)) < 60 or len(re.sub(r"\s+", "", rawa)) < 25:
        return "弃卡", "题面/答案过短", meta
    q0 = BO.conv_imgs(BO.clean_q(rawq))
    a0 = BO.clean_a(BO.conv_imgs(rawa), q0)
    q, a = BO.html_table_to_md(q0), BO.html_table_to_md(a0)
    if BO.LEAK.search(q):
        # 剔除**本卡自身**题目标题行后再判（标题的「（12 分，占 8%）」是分值，不是泄露）；
        # ⚠️ 只剔本卡号，否则会放过「下一题题头串入」。
        _ow = BO.own_qno(t, p)
        _qchk = re.sub(r"^#{0,4}[^\S\n]*第[^\S\n]*%s[^\S\n]*[题題][^\n]*$" % (_ow if _ow else r"\d+"),
                       "", q, flags=re.M)
        if BO.LEAK.search(_qchk):
            return "弃卡", "题面泄露", meta
    qn = re.sub(r"\s+", "", q); an = re.sub(r"\s+", "", a)
    if len(an) < 25 or len(qn) < 60:
        return "弃卡", "题面/答案过短", meta
    if len(B.ORGRE.findall(q + " " + a)) >= 3:
        return "弃卡", "有机章节", meta
    if len(re.findall(r"^\*\*\s*\d{1,2}\s*[.．]\s*\*\*", q + "\n" + a, re.M)) >= 8:
        return "弃卡", "编号列表≥8", meta
    if BO.HANDWRITTEN.search(BO._HW_STRIP.sub(" ", q + " " + a)):
        return "弃卡", "手写稿口语/涂鸦", meta
    if "![[" not in a:
        _an = re.sub(r"\s+", "", a); _qn = re.sub(r"\s+", "", q)
        _r = BO.contain_ratio(_an, _qn)
        if len(_an) >= 40 and (_r >= 0.80 or (_r >= 0.70 and len(_an) * (1 - _r) < 80)):
            return "弃卡", "仅题干回显", meta
        if BO.GARB2PAT.search(a):
            return "弃卡", "OCR 乱码宏", meta
    _own = BO.own_qno(t, p)
    _of = BO.overflow_reason(q, a, _own)
    if _of:
        return "弃卡", "越界（含他题内容）", meta
    return "入池", "", meta


rows = []
for rel in BO.SRCS:
    for p in sorted(glob.glob(os.path.join(BO.BASE, rel, "**", "题-*.md"), recursive=True)):
        verdict, reason, meta = judge(p, rel)
        m = re.search(r"题-[A-Za-z]+-\d+-(\d+)-", os.path.basename(p))
        rows.append(dict(
            path=p.replace(os.sep, "/"), inst=rel, qno=(m.group(1) if m else ""),
            mod=meta["mod"], stage=meta["stage"], diff=meta["diff"],
            verdict=verdict, reason=reason, klass=(CLASS.get(reason, "") if reason else ""),
        ))

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["path", "inst", "qno", "mod", "stage", "diff", "verdict", "reason", "klass"])
    w.writeheader()
    w.writerows(rows)

tot = len(rows)
inn = sum(1 for r in rows if r["verdict"] == "入池")
print("全量卡 %d；入池 %d；弃卡 %d" % (tot, inn, tot - inn))
c = collections.Counter(r["reason"] for r in rows if r["verdict"] == "弃卡")
print("\n弃卡原因（按类别）：")
for reason, n in sorted(c.items(), key=lambda x: (CLASS.get(x[0], "z"), -x[1])):
    print("  [%s] %-22s %5d" % (CLASS.get(reason, "?"), reason, n))
print("\nA 类（内容不可用）合计 %d" % sum(n for r, n in c.items() if CLASS.get(r) == "A"))
print("CSV → %s" % OUT)
