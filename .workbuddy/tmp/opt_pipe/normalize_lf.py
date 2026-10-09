# -*- coding: utf-8 -*-
"""把指定 md 文件的行尾统一为 LF（就地规范化，写盘前打印统计）。"""
import os
import sys

R = r"C:\Obsidion\妙妙屋"
for f in sys.argv[1:]:
    p = os.path.join(R, f)
    raw = open(p, "rb").read()
    crlf = raw.count(b"\r\n")
    lf = raw.count(b"\n") - crlf
    if crlf == 0:
        print("%-40s 已是 LF（%d 行）" % (os.path.basename(f), lf))
        continue
    new = raw.replace(b"\r\n", b"\n")
    open(p, "wb").write(new)
    print("%-40s CRLF %d → 0 ｜ 总行 %d" % (os.path.basename(f), crlf, new.count(b"\n")))
