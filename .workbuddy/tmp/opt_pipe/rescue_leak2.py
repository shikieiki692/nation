#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rescue_leak2.py —— 救「题面泄露」中「下一题题头串入题面」型：按题界截断题面。"""
import csv, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
sys.path.insert(0, os.path.join(R, ".workbuddy/tmp/opt_pipe"))
_orig = list(sys.argv)
sys.argv = ["x", "--vol", "RL2", "--all-years"]
import build_org as BO

apply = "--apply" in _orig
LIM = int(_orig[_orig.index("--limit") + 1]) if "--limit" in _orig else 999
BK = os.path.join(R, ".workbuddy/tmp/opt_pipe/leak2_backup")
os.makedirs(BK, exist_ok=True)

HDR = re.compile(r'第\s*(\d{1,2})\s*[题題愿腰段顾][^\n]{0,24}[（(]\s*\d+\s*分')
TITLE_OWN = None


def _ns_map(s):
    chs, idx = [], []
    for i, c in enumerate(s):
        if not c.isspace():
            chs.append(c); idx.append(i)
    return "".join(chs), idx


def map_back(raw, cleaned, cutpos):
    cn, _ = _ns_map(cleaned)
    rn, ridx = _ns_map(raw)
    n = len(re.sub(r"\s+", "", cleaned[:cutpos]))
    anchor = cn[max(0, n - 60):n]
    if len(anchor) < 8:
        return None
    p = rn.find(anchor)
    if p < 0:
        return None
    e = p + len(anchor)
    if e <= 0 or e > len(ridx):
        return None
    return ridx[e - 1] + 1


rows = [r for r in csv.DictReader(open(os.path.join(R, "09-审计报告/2026-10-07-不可组卷题目清单.csv"), encoding="utf-8-sig"))
        if r["reason"] == "题面泄露"]
print("题面泄露 %d 张\n" % len(rows))
n = 0
for r in rows:
    if n >= LIM:
        break
    p = os.path.join(R, r["path"])
    t = open(p, encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")
    i = t.find("## 题目"); j = t.find("## 参考答案"); k = t.find("## 知识点映射")
    if not (0 <= i < j < k):
        continue
    own = BO.own_qno(t, p)
    rawq = t[i:j]
    c = BO.X.extract(p)
    q = BO.html_table_to_md(BO.conv_imgs(BO.clean_q(c["question"])))
    # 剔自身标题行后再找题头
    q1 = re.sub(r'^#{0,4}[^\S\n]*第[^\S\n]*%s[^\S\n]*[题題][^\n]*$' % (own if own else r'\d+'), '', q, flags=re.M)
    pos = None
    for m in HDR.finditer(q1):
        if own is None or int(m.group(1)) != own:
            pos = m.start(); break
    if pos is None:
        print("  ⚠ 未找到下一题题头（实质泄露）：", os.path.basename(p)[:50]); continue
    cut = map_back(rawq, q, pos)
    if cut is None:
        print("  ⚠ 回映射失败：", os.path.basename(p)[:50]); continue
    keep = rawq[:cut].rstrip()
    drop = rawq[cut:].strip()
    a_len = len(t[j:k])
    print("═" * 94)
    print("%s | own=%s | 题面 %d → 留 %d（删 %d） | 答案区 %d 字" %
          (os.path.basename(p)[:50], own, len(rawq), len(keep), len(drop), a_len))
    print("   删段首 100: …%s…" % re.sub(r"\s+", " ", drop[:100]))
    print("   接缝: …%s…" % re.sub(r"\s+", " ", keep[-90:]))
    if apply:
        note = ("\n\n> 📄 校勘（2026-10-07）：题面区尾部串入了**后一题**的题头及其内容（%d 字），"
                "已按题界截断；如需该题请查源卷。\n" % len(drop))
        newt = t[:i] + keep + note + t[j:]
        bfp = os.path.join(BK, os.path.basename(p) + ".orig")
        if not os.path.exists(bfp):
            open(bfp, "w", encoding="utf-8", newline="\n").write(t)
        open(p, "w", encoding="utf-8", newline="\n").write(newt)
        print("   ✔ 已写入")
    n += 1
print("\n%s" % ("已写入" if apply else "（dry-run）"))
