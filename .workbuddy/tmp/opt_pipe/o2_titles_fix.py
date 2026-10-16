# -*- coding: utf-8 -*-
r"""o2_titles_fix.py —— O2 人工题名（②-b）。

· 答案版：修 2 处**被自动截断**的题名（最小改动，其余 8 名保留）——
    Q3「在药物分子中」→「吡唑环的区域选择性烷基化」；Q8「烷烃构象中的取代基排斥不仅取」→「烷烃构象与 A¹,³ 张力」
· 学生版：题名**整体缺失**（`### 第 N 题（13 分）`）⇒ 按答案版最终题名镜像补入。
护栏：精确锚点 ＋ 逐处 count 断言 ＋ 幂等（已含新名即跳过）＋ EOL 守恒 ＋ 备份。
"""
import os
import re
import shutil
import sys

ROOT = r"C:/Obsidion/妙妙屋"
BAK = os.path.join(ROOT, ".workbuddy", "tmp", "opt_pipe", "_bak_o2_titles")
os.makedirs(BAK, exist_ok=True)

ANS = "04-题库/初赛模拟卷O2（有机·答案版）.md"
STU = "04-题库/初赛模拟卷O2（有机·学生版）.md"

# 最终 10 题名（两版一致）
TITLES = {
    1: "酶催化有机合成",
    2: "Palladacycle",
    3: "吡唑环的区域选择性烷基化",
    4: "分子编辑",
    5: "三钴碳化物簇",
    6: "复杂的 Wittig 重排",
    7: "某类有机发光小分子",
    8: "烷烃构象与 A¹,³ 张力",
    9: "天然产物全合成",
    10: "The FiRST Eye",
}
ANS_EDITS = [
    ("### 第 3 题（13 分）在药物分子中", "### 第 3 题（13 分）吡唑环的区域选择性烷基化"),
    ("### 第 8 题（13 分）烷烃构象中的取代基排斥不仅取", "### 第 8 题（13 分）烷烃构象与 A¹,³ 张力"),
]


def main():
    ok = 0
    # ① 答案版：修 2 处截断题名
    p = os.path.join(ROOT, ANS)
    shutil.copy2(p, os.path.join(BAK, os.path.basename(ANS)))
    body = open(p, encoding="utf-8-sig", newline="").read()
    out = body
    for old, new in ANS_EDITS:
        if new in out:
            print("  [IDEMPOTENT] 答案版已含新名：%s" % new[:28])
            continue
        n = out.count(old)
        if n != 1:
            print("  [SKIP n=%d] %s" % (n, old[:30]))
            continue
        out = out.replace(old, new)
    if out != body:
        open(p, "w", encoding="utf-8", newline="").write(out)
        print("  [OK] 答案版题名 ×2（+%d 字符）" % (len(out) - len(body)))
        ok += 1

    # ② 学生版：镜像补题名
    p = os.path.join(ROOT, STU)
    shutil.copy2(p, os.path.join(BAK, os.path.basename(STU)))
    body = open(p, encoding="utf-8-sig", newline="").read()
    out, nadd = body, 0
    for i, t in TITLES.items():
        head = "### 第 %d 题（13 分）" % i
        if head + t in out:
            continue                                   # 幂等
        m = re.search(re.escape(head) + r"(?![^\n]*[\u4e00-\u9fffA-Za-z])", out)
        if not m:
            print("  [SKIP] 学生版未找到裸题头：%s" % head)
            continue
        out = out[:m.end()] + t + out[m.end():]
        nadd += 1
    if out != body:
        open(p, "w", encoding="utf-8", newline="").write(out)
        print("  [OK] 学生版补题名 %d/10（+%d 字符）" % (nadd, len(out) - len(body)))
        ok += 1
    print("\n已改 %d / 2 文件" % ok)
    return 0


if __name__ == "__main__":
    sys.exit(main())
