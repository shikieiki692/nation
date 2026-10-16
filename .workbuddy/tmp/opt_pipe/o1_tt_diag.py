# -*- coding: utf-8 -*-
"""复现 volpost --titles 的匹配逻辑，打印当前仍会命中的条目（查非幂等来源）。"""
import json, re, io

R = r"C:\Obsidion\妙妙屋"
md = R + r"\04-题库\初赛模拟卷O1（有机·答案版）.md"
cfg = json.load(io.open(R + r"\.workbuddy\tmp\opt_pipe\o1_titles.json", encoding="utf-8"))
txt = open(md, encoding="utf-8-sig").read()

for q, (a, b) in cfg.items():
    pat = re.compile(r"(?m)^(### 第 %s 题（[^）]*）)" % q)
    m = pat.search(txt)
    hit_head = bool(m and txt[m.end():].startswith(a))
    hit_cell = ("| %s | %s |" % (q, a)) in txt
    if hit_head or hit_cell:
        print("q%-3s head=%-5s cell=%-5s old=%r" % (q, hit_head, hit_cell, a))
