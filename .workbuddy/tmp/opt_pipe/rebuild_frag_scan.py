# -*- coding: utf-8 -*-
"""rebuild_frag_scan.py —— P0-3：扫「**OCR 碎片重建**」高风险点（答案区孤立短公式块等）。

病根（卷 XVI 实测）：`题-HZ-01-06` 6-1-2 的答案句在 OCR md 里**整句丢失**，只剩两块
孤立的 `$$NaHSO_3$$` / `$$(CN)_2$$` 漂移公式；修复时按残留公式**重建**成散文句，
用词与源答案册不符（「添加」写成「溶液」）——**没有任何闸门能发现**，靠人工「仔细检查」兜住。

判据（纯文本层，可复现；只**筛候选**，定性必须回源目检）：
  A. 答案区出现**孤立短公式块**：独占行、`$$` 包着 ≤24 字符、且不含中文的片段
     （典型的 OCR 把公式从句子中抠出来的残留；⚠️ 合法显示公式通常也不含中文，
      故 A 只是候选，须结合「上下文无对应文字」人工判）；
  B. 答案区出现「半截句」：以 `的`/`和`/`与`/`及` 结尾且总长 <40 字的残句行。

用法：
    python rebuild_frag_scan.py --vol XVI        # 只扫某卷计划锁内的卡
    python rebuild_frag_scan.py --all            # 扫全部机构卡（慢）
输出：候选清单（卡路径 / 行号 / 片段），并可与 vol_meta_<卷>.json 的 rebuild_flags 对照。
"""
import argparse
import glob
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
sys.path.insert(0, os.path.join(R, ".workbuddy", "tmp", "opt_pipe"))

DISP_RE = re.compile(r"\$\$([^$]{1,60})\$\$")          # 同行成对（判据 24 的合法形态也在其中，需人工判）
ISO_RE = re.compile(r"^\$\$\s*([^$\n]{1,24})\s*\$\$\s*$", re.M)   # 独占行的短公式块
HALF_TAIL = re.compile(r"[的和与及並且且]\s*$")
CJK = re.compile(r"[\u4e00-\u9fff]")


def scan_card(p):
    t = open(p, encoding="utf-8-sig").read().replace("\r\n", "\n")
    i, j = t.find("## 题目"), t.find("## 参考答案")
    if j <= i:
        return []
    a = t[j:]
    hits = []
    # A. 独占行短公式块（含中文的不算 —— 那是正常公式）
    for m in ISO_RE.finditer(a):
        body = m.group(1).strip()
        if CJK.search(body):
            continue
        if re.fullmatch(r"[A-Za-z0-9\s\\_{}^+\-().,·]+", body) is None:
            continue
        line_no = t[:j + m.start()].count("\n") + 1
        hits.append(("A-孤立短公式块", line_no, body[:40]))
    # B. 半截句结尾
    for m in HALF_TAIL.finditer(a):
        ln_start = a.rfind("\n", 0, m.start()) + 1
        ln = a[ln_start:m.end()].strip()
        if len(ln) < 40:
            line_no = t[:j + ln_start].count("\n") + 1
            hits.append(("B-半截句", line_no, ln[-38:]))
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vol")
    ap.add_argument("--all", action="store_true")
    A = ap.parse_args()
    if A.vol:
        plan_p = os.path.join(R, ".workbuddy/tmp/opt_pipe", "vol_plan_%s.json" % A.vol)
        cards = []
        for _m, lst in json.load(open(plan_p, encoding="utf-8")):
            cards += [c["path"].replace("/", os.sep) for c in lst]
        scope = "卷 %s 计划锁（%d 张）" % (A.vol, len(cards))
    else:
        cards = sorted(glob.glob(os.path.join(R, "04-题库/2026机构初赛模拟题", "*", "题-*.md")))
        scope = "全部机构卡（%d 张）" % len(cards)
    print("扫描范围：%s" % scope)
    total = 0
    for rel in cards:
        p = os.path.join(R, rel) if not os.path.isabs(rel) else rel
        if not os.path.exists(p):
            continue
        hits = scan_card(p)
        if hits:
            total += len(hits)
            print("\n▸ %s" % os.path.basename(p))
            for k, ln, frag in hits[:12]:
                print("    [%s] L%-5d %s" % (k, ln, frag))
    print("\n合计候选 %d 处 ｜ ⚠️ 本工具**只筛候选**：定性/修复前必须回源（PDF 原页）逐字目检。" % total)
    return 0


if __name__ == "__main__":
    sys.exit(main())
