# -*- coding: utf-8 -*-
"""比对 docx 的 HEAD 版 vs 工作区版：逐 zip 条目 CRC32 是否全同（全同⇒仅时间戳变化）。"""
import io
import subprocess
import sys
import zipfile

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Obsidion\妙妙屋"
FILES = sys.argv[1:]

for rel in FILES:
    head = subprocess.run(["git", "show", "HEAD:" + rel], cwd=ROOT,
                          capture_output=True).stdout
    hz = zipfile.ZipFile(io.BytesIO(head))
    wz = zipfile.ZipFile(rel)
    hn = {i.filename: i.CRC for i in hz.infolist()}
    wn = {i.filename: i.CRC for i in wz.infolist()}
    same = (hn == wn)
    diff = [k for k in set(hn) | set(wn) if hn.get(k) != wn.get(k)]
    print("%-46s 条目 %d/%d  全同=%s  差异=%s" % (
        rel.split("/")[-1][:44], len(hn), len(wn), same, diff[:4] if not same else "无"))
