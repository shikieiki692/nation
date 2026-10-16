# -*- coding: utf-8 -*-
"""B2｜E 悬空链去链（09-审计报告/历史任务卡/ 归档卡）。

政策依据：`09-审计报告/历史任务卡/计划-全库断链与图片缺失治理.md` evidence
  「0 新建 KP（**alias 承接 ＋ 改链 ＋ 去链** 三策略）」。
判据（实测 2026-10-16）：
  · `09-审计报告/auto-validation/{2026-08-04,2026-06-29}-validation` **不存在**（该目录自 2026-07-21／10-02 起）
  · `11-模板/scripts/{validate_kb.py,build-all-handout-docx.py}` **存在**，但非 .md ⇒ wikilink 不解析
做法：仅去 `[[ ]]`，保留文本并追加短注（FM 键集合不变、其余字节不动、EOL 守恒）。
"""
import os
import sys

VAULT = r"C:/Obsidion/妙妙屋"
D = os.path.join(VAULT, "09-审计报告", "历史任务卡")

EDITS = [
    ("任务卡-publishedKP断链修复.md",
     '  - "[[09-审计报告/auto-validation/2026-08-04-validation]]"',
     '  - "09-审计报告/auto-validation/2026-08-04-validation（该批 validation 报告未录入库）"'),
    ("任务卡-validate_kb与published断链目录治理.md",
     '  - "[[09-审计报告/auto-validation/2026-06-29-validation]]"',
     '  - "09-审计报告/auto-validation/2026-06-29-validation（该批 validation 报告未录入库）"'),
    ("任务卡-validate_kb与published断链目录治理.md",
     '  - "[[11-模板/scripts/validate_kb.py]]"',
     '  - "11-模板/scripts/validate_kb.py（脚本，非 md 笔记）"'),
    ("任务卡-备课体系深度优化与审计.md",
     '  - "[[11-模板/scripts/build-all-handout-docx.py]]"',
     '  - "11-模板/scripts/build-all-handout-docx.py（脚本，非 md 笔记）"'),
    ("计划-全库断链与图片缺失治理.md",
     '  - "[[09-审计报告/auto-validation/2026-08-04-validation]]"',
     '  - "09-审计报告/auto-validation/2026-08-04-validation（该批 validation 报告未录入库）"'),
]


def main():
    ok = 0
    for fn, old, new in EDITS:
        p = os.path.join(D, fn)
        raw = open(p, encoding="utf-8-sig", newline="").read()
        bom = "\ufeff" if raw.startswith("\ufeff") else ""
        body = raw[1:] if bom else raw
        n = body.count(old)
        if n != 1:
            print("  [SKIP n=%d] %s" % (n, fn))
            continue
        out = body.replace(old, new)
        open(p, "w", encoding="utf-8", newline="").write(bom + out)
        ok += 1
        print("  [OK] %s  <= %s" % (fn, old.strip()))
    print("\n已改 %d / %d" % (ok, len(EDITS)))
    return 0 if ok == len(EDITS) else 1


if __name__ == "__main__":
    sys.exit(main())
