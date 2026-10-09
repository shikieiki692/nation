# -*- coding: utf-8 -*-
"""卷 md 重建差异分类：把 `git diff HEAD` 的改动逐行归类，判定是否「只含预期改动」。

类别：FMT＝三条化学式规则（可见字符指纹一致）；RENUM＝小问号重编号（`N-N-x`→`N-M-x`）；
      OTHER＝其它（需人工判）。
用法：python vol_md_diff_classify.py <卷号>
"""
import re, sys, subprocess, difflib

V = sys.argv[1]
P = f"04-题库/初赛模拟卷{V}（非有机·答案版）.md"
P2 = f"04-题库/初赛模拟卷{V}（非有机·学生版）.md"

VIS = re.compile(r"\$|\{|\}|\\mathrm|\s|\\,")
LAB = re.compile(r"(?<![\d-])(\d{1,2})-(\d{1,2})(-\d{1,2})?(?![-\d])")


def old_text(p):
    r = subprocess.run(["git", "show", f"HEAD:{p}"], capture_output=True)
    return r.stdout.decode("utf-8").split("\n")


def new_text(p):
    return open(p, encoding="utf-8-sig").read().split("\n")


def renorm(s):
    """把「小问号」统一成 `*`，用于判定“差异只在于编号”。"""
    def sub(m):
        return "*%s%s" % (m.group(3) or "", "")
    return LAB.sub(sub, s)


for path in (P, P2):
    try:
        A, B = old_text(path), new_text(path)
    except FileNotFoundError:
        print("（缺）", path); continue
    sm = difflib.SequenceMatcher(None, A, B, autojunk=False)
    fmt = ren = oth = 0
    oth_lines = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        old, new = "\n".join(A[i1:i2]), "\n".join(B[j1:j2])
        if old == new:
            continue
        if VIS.sub("", old) == VIS.sub("", new):
            fmt += 1
        elif renorm(old) == renorm(new):
            ren += 1
        else:
            oth += 1
            oth_lines.append((old.strip()[:110], new.strip()[:110]))
    print("==== %s ====  FMT %d 块 ／ RENUM %d 块 ／ OTHER %d 块" % (path.split("/")[-1], fmt, ren, oth))
    for a, b in oth_lines[:25]:
        print("   OTHER\n     - %s\n     + %s" % (a, b))
