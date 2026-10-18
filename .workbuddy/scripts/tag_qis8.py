# -*- coding: utf-8 -*-
"""P0-3：给 F 判据双缺 8 张卡补 question_image_status: 缺失（事实层，池计数零影响）。

只插入不替换（判据 70）；已有该字段则跳过（幂等）；断言锚点唯一。
用法：python tag_qis8.py [--apply]
"""
import io
import os
import re
import sys

ROOT = r"C:\Obsidion\妙妙屋"

PATHS = [
    r"04-题库/教材习题/化学竞赛初赛讲义/题-008-初赛讲义-配合物-习题4.5.md",
    r"04-题库/教材习题/化学竞赛初赛讲义/题-037-初赛讲义-配合物-习题4.56.md",
    r"04-题库/教材习题/化学竞赛初赛讲义/题-022-初赛讲义-金属有机化学-习题5.22.md",
    r"04-题库/教材习题/化学竞赛初赛讲义/题-032-初赛讲义-金属有机化学-习题5.32.md",
    r"04-题库/教材习题/汇智竞赛题目/题-汇智-晶体结构-31.md",
    r"04-题库/教材习题/汇智竞赛题目/题-汇智-晶体结构-5.md",
    r"04-题库/教材习题/汇智竞赛题目/题-汇智-晶体结构-51.md",
    r"04-题库/真题/第39届决赛/理论/题-39决理-4-电化学CO₂还原.md",
]

ANCHOR_ORDER = ["replacement_status", "consumption_status", "answer_status", "status"]
KEY = "question_image_status"
VAL = "缺失"


def fm_bounds(lines):
    """返回 (start,end)：start=首个 --- 行索引，end=闭合 --- 行索引。"""
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return 0, i
    return None


def plan(path):
    fp = os.path.join(ROOT, path)
    if not os.path.exists(fp):
        return None, "NOTFOUND"
    raw = open(fp, "rb").read()
    crlf = b"\r\n" in raw
    text = raw.decode("utf-8-sig")
    nl = "\r\n" if crlf else "\n"
    lines = text.split(nl)
    b = fm_bounds(lines)
    if b is None:
        return None, "NO_FM"
    s, e = b
    fm = lines[s + 1:e]
    # 幂等：已存在则跳过
    if any(re.match(r"^" + KEY + r"\s*:", ln) for ln in fm):
        return None, "ALREADY"
    # 找锚点（取最后一个出现的，因为 status 块通常在 FM 尾部）
    idx = None
    for a in ANCHOR_ORDER:
        pat = re.compile(r"^" + a + r"\s*:")
        hits = [i for i, ln in enumerate(fm) if pat.match(ln)]
        if hits:
            idx = hits[-1]
            break
    if idx is None:
        return None, "NO_ANCHOR"
    insert_at = s + 1 + idx + 1  # 插到锚点行之后
    return (fp, nl, lines, insert_at, crlf), "OK"


def main():
    apply = "--apply" in sys.argv
    n_ok = n_skip = n_bad = 0
    for p in PATHS:
        info, st = plan(p)
        name = os.path.basename(p)
        if st != "OK":
            print("[SKIP:%-9s] %s" % (st, name))
            if st in ("NOTFOUND", "NO_FM", "NO_ANCHOR"):
                n_bad += 1
            else:
                n_skip += 1
            continue
        fp, nl, lines, at, crlf = info
        anchor_line = lines[at - 1].strip()
        new_lines = lines[:at] + [KEY + ": " + VAL] + lines[at:]
        if apply:
            out = nl.join(new_lines)
            with io.open(fp, "w", encoding="utf-8", newline="") as f:
                f.write(out)
        print("[%s] %-46s 锚=%-34s CRLF=%s" % ("APPLY" if apply else "DRYRUN", name[:46], anchor_line[:34], crlf))
        n_ok += 1
    print("\n计划/已写 %d，跳过(已存在) %d，异常 %d" % (n_ok, n_skip, n_bad))


if __name__ == "__main__":
    main()
