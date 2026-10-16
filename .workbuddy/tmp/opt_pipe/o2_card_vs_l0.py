# -*- coding: utf-8 -*-
r"""o2_card_vs_l0.py —— 逐卡：卡内「题目/参考答案」 ↔ L0 源 md（FM source_file）逐字比对。

判据（沿用 O1 J15 路线①）：卡应是 L0 源 md 的**忠实切片**。
  取卡内该段的汉字串，在 L0 源 md 的汉字流中做**最长公共子串**估算 + 覆盖率；
  ≥0.95 ⇒ 忠实切片；<0.80 ⇒ 需人工核（改字/漏句/换源）。
"""
import os
import re
import sys
from difflib import SequenceMatcher

import fitz  # noqa: F401  (确保走 venv)

ROOT = r"C:/Obsidion/妙妙屋"
sys.path.insert(0, os.path.join(ROOT, ".workbuddy", "tmp", "opt_pipe"))
import o2_render as R  # noqa: E402


def hz(s):
    return re.sub(r"[^\u4e00-\u9fff]", "", s)


ANS = {
    "HYS-11-08": "2026机构初赛模拟题/07-化英社/第40届化英社化学奥林匹克初赛夏季初赛模拟11参考答案.md",
    "QBY-17-08": "2026机构初赛模拟题/04-清北营/2026年清北营暑假高二班-试卷17-参考答案.md",
    "CM-207-09": "chemy试题/第39届Chemy化学奥林匹克竞赛模拟试题参考答案合集._200-329.md",
    "GM-10-08": "2026机构初赛模拟题/06-伽马/伽马化学2026年暑期模拟10答案.md",
    "YJ-09-06": "2026机构初赛模拟题/05-壹尖培优/第40届中国化学奥林匹克（初赛）模拟试题9参考答案.md",
    "HYS-40-09": "2026机构初赛模拟题/07-化英社/第40届化英社化学奥林匹克（初赛）春季联考6答案-final.md",
    "QBY-01-06": "2026机构初赛模拟题/04-清北营/2026年清北营寒假班-试卷1-参考答案.md",
    "CM-17-08": "2026机构初赛模拟题/10-chemy/第40届chemy初赛模拟17答案.md",
    "GM-09-10": "2026机构初赛模拟题/06-伽马/伽马化学2026年暑期模拟9答案.md",
    "YJ-04-08": "2026机构初赛模拟题/05-壹尖培优/第40届中国化学奥林匹克（初赛）模拟试题4参考答案.md",
}


def key_of(card):
    b = os.path.basename(card)
    for k in ("HYS-11-08", "QBY-17-08", "CM-207-09", "GM-10-08", "YJ-09-06",
              "HYS-40-09", "QBY-01-06", "CM-17-08", "GM-09-10", "YJ-04-08"):
        if k in b:
            return k
    return None


def cov(seg, body):
    g = R.grams(seg)
    return (sum(1 for x in g if x in body) / len(g)) if g else 0.0


def fm_source_file(path):
    t = open(path, encoding="utf-8-sig", newline="").read()
    m = re.search(r'^source_file:[ \t]*(.*)$', t, re.M)
    if not m:
        return None
    v = m.group(1).strip().strip('"').strip("'")
    return v or None


print("%-40s | %-8s %-8s | %-9s %-9s | L0 源 md" % ("卡", "题面字", "答案字", "题面cov", "答案cov"))
print("-" * 118)
flag = []
for card, _q, _a in R.JOBS:
    cp = os.path.join(ROOT, card)
    txt = open(cp, encoding="utf-8-sig").read()
    sf = fm_source_file(cp)
    l0 = None
    if sf:
        for cand in (sf, sf.replace("2026机构初赛模拟题/", "")):
            p = os.path.join(ROOT, cand)
            if os.path.isfile(p):
                l0 = p
                break
    row = []
    if not l0:
        print("%-40s | (未找到 L0 源 md: %s)" % (os.path.basename(card)[:38], sf))
        flag.append((os.path.basename(card), "no-L0", None))
        continue
    body = hz(open(l0, encoding="utf-8-sig", errors="replace").read())
    # ★ 答案另有独立的 L0 源 md（试题 md 不含答案）⇒ 答案段对该答案源核
    k = key_of(card)
    apath = os.path.join(ROOT, ANS.get(k, "")) if k else None
    abody = hz(open(apath, encoding="utf-8-sig", errors="replace").read()) if apath and os.path.isfile(apath) else body
    for secs, tgt in ((("题目",), body), (("参考答案", "答案"), abody)):
        seg = hz(R.clean(R.section(txt, *secs)))
        if not seg:
            row.append((0, None))
            continue
        # ★ 判据：卡内该段的 8-gram **包含率**（对整份 L0 源 md）——对重排/夹注鲁棒；
        #   前版用 SequenceMatcher 滑窗，探针未命中时退化失真（J2：先怀疑判据）。
        row.append((len(seg), cov(seg, tgt)))
    q, a = row
    print("%-40s | %-8s %-8s | %-9s %-9s | %s" % (
        os.path.basename(card)[:38], q[0], a[0],
        ("%.3f" % q[1]) if q[1] is not None else "-",
        ("%.3f" % a[1]) if a[1] is not None else "-",
        os.path.relpath(l0, ROOT)[:44]))
    if (q[1] is not None and q[1] < 0.95) or (a[1] is not None and a[1] < 0.95):
        flag.append((os.path.basename(card), "cov<0.95", (q[1], a[1])))

print("\n=== 需人工核（<0.95）===")
if not flag:
    print("  无 —— 10 卡均为 L0 源 md 的忠实切片 ✅")
for f in flag:
    print("  ", f)
