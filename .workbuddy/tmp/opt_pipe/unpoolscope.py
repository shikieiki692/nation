# -*- coding: utf-8 -*-
"""unpoolscope.py —— 删除「已回到入池」的卡上的 `pool_scope` 行（RMW · 幂等）。

背景：`pool_keep.json` 放行 12 张后，它们从「弃卡」变「入池」；
`pool_scope:` 是**弃卡去向**标注，入池卡不应携带 ⇒ 精确删掉那一行。

纪律同 poolscope.py：RMW 只删一行、备份、逐字节复核、幂等。
用法：python unpoolscope.py --dry | --apply
"""
import csv, os, re, shutil, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Obsidion\妙妙屋"
CSV = os.path.join(ROOT, "09-审计报告", "2026-10-07-不可组卷题目清单.csv")
BAK = os.path.join(ROOT, ".workbuddy/tmp/opt_pipe/poolscope_rm_bak")
DRY = "--dry" in sys.argv
LINE = re.compile(r"\npool_scope[ \t]*:[^\n]*", re.M)


def main():
    rows = list(csv.DictReader(open(CSV, encoding="utf-8-sig")))
    inn = [r for r in rows if r["verdict"] == "入池"]
    print("入池 %d 张" % len(inn))
    os.makedirs(BAK, exist_ok=True)
    n, skips = 0, []
    for r in inn:
        p = r["path"]
        if not os.path.isfile(p):
            continue
        raw = open(p, encoding="utf-8-sig").read()
        if "\r\n" in raw:
            skips.append((p, "CRLF")); continue
        m = LINE.search(raw)
        if not m:
            continue
        seg = m.group(0)                       # 恰为 "\npool_scope: xxx"
        new = raw[:m.start()] + raw[m.end():]
        # 逐字节复核：长度差恰为 seg，且 pool_scope 键数恰少 1，其余不变
        if (len(raw) - len(new) != len(seg)
                or raw.count("pool_scope") - new.count("pool_scope") != 1):
            skips.append((p, "复核不通过")); continue
        n += 1
        if not DRY:
            rel = os.path.relpath(p, ROOT).replace(os.sep, "/")
            shutil.copy2(p, os.path.join(BAK, rel.replace("/", "__")))
            with open(p, "w", encoding="utf-8", newline="\n") as f:
                f.write(new)
    print("%s：删除 pool_scope 行 %d ｜ 跳过 %d" % ("(dry)" if DRY else "已写盘", n, len(skips)))
    for p, w in skips[:5]:
        print("   ✗", w, os.path.basename(p))


if __name__ == "__main__":
    main()
