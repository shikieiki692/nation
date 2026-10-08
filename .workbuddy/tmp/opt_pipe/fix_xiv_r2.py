# -*- coding: utf-8 -*-
"""fix_xiv_r2.py —— 视觉核验后追加修复（3 处）。用法: python -X utf8 fix_xiv_r2.py [--apply]"""
import datetime
import os
import shutil
import sys

ROOT = r"C:\Obsidion\妙妙屋"
Q = os.path.join(ROOT, "04-题库", "2026机构初赛模拟题")

EDITS = [
    # 1) build_org 模板：合计行与脚注之间补空行 ⇒ 消除字面 ">"
    (os.path.join(ROOT, ".workbuddy", "tmp", "opt_pipe", "build_org.py"),
     "build_org: 合计与脚注间补空行",
     [("out += ['', '合计 %d 分；难度 ⭐⭐⭐⭐ ×%d、⭐⭐⭐⭐⭐ ×%d；有机化学 0 题、真题 0 题；跨 %d 个来源机构。'\n"
       "                    % (total, n4, n5, len(orgs)),\n"
       "                    '> 难度星级取自题卡 `difficulty` 字段。**本库 `exam_stage` 字段不可信**，故本卷不按考段标注。', '']",
       "out += ['', '合计 %d 分；难度 ⭐⭐⭐⭐ ×%d、⭐⭐⭐⭐⭐ ×%d；有机化学 0 题、真题 0 题；跨 %d 个来源机构。'\n"
       "                    % (total, n4, n5, len(orgs)), '',\n"
       "                    '> 难度星级取自题卡 `difficulty` 字段。**本库 `exam_stage` 字段不可信**，故本卷不按考段标注。', '']")]),
    # 2) HYS 卡：删内部溯源注（不该出现在交付件）
    (os.path.join(Q, "化英社", "题-HYS-01-02-研究钙钛矿衍生结构时常用Ra.md"),
     "第5题: 删内部溯源注",
     [("\n> ✅ 答案由源《第40届化英社化学奥林匹克（初赛）春季联考1 答案(1).md》第 2 题回收补录（回源核对 2026-09-27）。\n", "")]),
    # 3) HZ-11 卡：答案 8.08 Å 的 Å 被 OCR 成 A
    (os.path.join(Q, "汇智", "题-HZ-11-05-在晶体结构的研究中将晶胞拆分.md"),
     "第8题: 8.08 A → 8.08 Å",
     [("\\mathrm{a} = 8.08 \\mathrm{A}", "\\mathrm{a} = 8.08\\ \\text{Å}")]),
]


def main():
    apply = "--apply" in sys.argv
    stamp = datetime.datetime.now().strftime("%m%d_%H%M")
    ok = True
    for path, desc, pairs in EDITS:
        with open(path, encoding="utf-8-sig") as f:
            txt = f.read().replace("\r\n", "\n")
        orig = txt
        for old, new in pairs:
            n = txt.count(old)
            if n != 1:
                print(f"❌ [{os.path.basename(path)}] {desc}: old 命中 {n} 次 → {old[:50]!r}")
                ok = False
                continue
            txt = txt.replace(old, new, 1)
        if txt != orig and apply:
            shutil.copy2(path, path + f".bak-{stamp}")
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(txt)
            print(f"✅ [{os.path.basename(path)}] {desc}  已写  Δ={len(txt)-len(orig):+d}")
        else:
            print(f"·  [{os.path.basename(path)}] {desc}  {'无变化' if apply else '待写'}")
    print("APPLIED" if apply else "DRY-RUN", "OK" if ok else "HAS-ERRORS")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
