# -*- coding: utf-8 -*-
"""检查文件行尾构成（唯一可信方法：读字节数 CRLF vs 纯 LF）。"""
import sys

for p in sys.argv[1:]:
    b = open(p, "rb").read()
    crlf = b.count(b"\r\n")
    lf = b.count(b"\n") - crlf
    lone_cr = b.count(b"\r") - crlf
    tag = "全CRLF" if lf == 0 and lone_cr == 0 else ("全LF" if crlf == 0 and lone_cr == 0 else "混合")
    print(f"{p}: CRLF={crlf} 纯LF={lf} 孤CR={lone_cr} -> {tag}")
