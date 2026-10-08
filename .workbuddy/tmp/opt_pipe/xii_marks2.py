# -*- coding: utf-8 -*-
"""核对卷 XII 中 sc2/sc3 类评分标记的上下文（只读）。"""
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, r"C:\Obsidion\妙妙屋\.workbuddy\tmp\opt_pipe")
import volpost as V  # noqa: E402

PAT = re.compile(r"\d+\s*\^\s*\{\s*\\prime\s*\}|\(\s*[\d.]+\s*'\s*\)")
for rel in V.plan_cards("XII"):
    raw = V.read(os.path.join(V.R, rel)).replace("\r\n", "\n")
    for m in PAT.finditer(raw):
        a = max(0, m.start() - 56)
        print("%-30s …%s…" % (os.path.basename(rel)[:28], raw[a:m.end() + 18].replace("\n", "⏎")))
