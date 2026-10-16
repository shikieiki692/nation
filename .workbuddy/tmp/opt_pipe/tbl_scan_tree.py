# -*- coding: utf-8 -*-
"""目录树表格结构扫描：只报告有「行格数不符 / 两表合并」的 md（只读）。"""
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.join(".workbuddy", "tmp", "opt_pipe"))
import pipe_tbl_audit as A  # noqa: E402

ROOTS = sys.argv[1:] or ["04-课件/学生讲义", "04-题库"]
nfile = 0
nbad = 0
hits = []
for root in ROOTS:
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d not in (".git", "node_modules", ".obsidian")]
        for fn in fns:
            if not fn.endswith(".md"):
                continue
            p = os.path.join(dp, fn)
            nfile += 1
            try:
                rep = A.audit(p)
            except Exception as e:  # noqa: BLE001
                print("ERR", p, e)
                continue
            merged = [b for b in rep if b["nsep"] > 1]
            ragged = [b for b in rep if b["bad_rows"]]
            if merged or ragged:
                nbad += 1
                hits.append((p, merged, ragged))

print("扫描文件 %d，异常 %d" % (nfile, nbad))
for p, merged, ragged in hits:
    print("---", p)
    for b in merged:
        print("   [两表合并] L%d-%d 分隔=%d 列=%d 图=%d"
              % (b["start"], b["end"], b["nsep"], b["ncol"], len(b["imgs"])))
    for b in ragged:
        print("   [行格数不符] L%d-%d 列=%d 异常行=%s 图=%d"
              % (b["start"], b["end"], b["ncol"], b["bad_rows"][:6], len(b["imgs"])))
