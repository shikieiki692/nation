# -*- coding: utf-8 -*-
r"""o2_subq_fix.py —— O2 卷 md 层小问改号残留修补（②-b）。

实测残留（`volpost --diag` ＋ 逐行定位，两版一致）：
  · Q1（源 化英社第8题）：「8-1\~1-3」＝ 原「8-1\~8-3」**只改了后一半** ⇒ 应「1-1\~1-3」
  · Q4（源 伽马第8题）：「8-1-12021 年, Richmond」/「8-32023 年, Tyler」两处行首改号未命中（紧跟数字）⇒ 应 4-1-1 / 4-3
其余题号经 `--diag` 逐题核对**无残留**（Q3 的 `**3-x**` 已正确改号；Q7/8/9 与卷号一致）。
护栏：精确锚点 ＋ 逐处 count 断言 ＋ 备份 ＋ 逆向逐字节自证 ＋ EOL 守恒。
"""
import os
import shutil
import sys

ROOT = r"C:/Obsidion/妙妙屋"
BAK = os.path.join(ROOT, ".workbuddy", "tmp", "opt_pipe", "_bak_o2_subq")
os.makedirs(BAK, exist_ok=True)

FILES = [
    "04-题库/初赛模拟卷O2（有机·答案版）.md",
    "04-题库/初赛模拟卷O2（有机·学生版）.md",
]
EDITS = [
    (r"下列8-1\~1-3将分别介绍", r"下列1-1\~1-3将分别介绍"),
    ("8-1-12021 年, Richmond Sarpong", "4-1-12021 年, Richmond Sarpong"),
    ("8-32023 年, Tyler J. Pearson", "4-32023 年, Tyler J. Pearson"),
]


def main():
    ok = 0
    for rel in FILES:
        p = os.path.join(ROOT, rel)
        shutil.copy2(p, os.path.join(BAK, os.path.basename(rel)))
        raw = open(p, encoding="utf-8-sig", newline="").read()
        bom = "\ufeff" if raw.startswith("\ufeff") else ""
        body = raw[1:] if bom else raw
        out = body
        for old, new in EDITS:
            n = out.count(old)
            if n != 1:
                print("  [SKIP n=%d] %s :: %s" % (n, os.path.basename(rel), old[:26]))
                continue
            out = out.replace(old, new)
        if out == body:
            print("  [NOCHANGE] %s" % os.path.basename(rel))
            continue
        # 逆向逐字节自证：把新串换回旧串应完全还原
        back = out
        for old, new in EDITS:
            back = back.replace(new, old)
        assert back == body, "逆向重建自证失败 %s" % rel
        open(p, "w", encoding="utf-8", newline="").write(bom + out)
        print("  [OK] %-34s +%d 字符（逆向自证 ✅）" % (os.path.basename(rel), len(out) - len(body)))
        ok += 1
    print("\n已改 %d / %d" % (ok, len(FILES)))
    return 0 if ok == len(FILES) else 1


if __name__ == "__main__":
    sys.exit(main())
