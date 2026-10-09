# -*- coding: utf-8 -*-
"""扫描「化学式排版」在库内的残留形态，量化下一轮可优化项。"""
import re, os, sys, collections
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
ROOTS = [os.path.join(R, "04-题库")]

pats = {
    # 字母基底 + 上下标「同时」存在（本轮 fbase 未覆盖）
    "dual_script_unmerged": re.compile(r"[A-Za-z][0-9]*[ \t]*\$[_^]\{[^{}]*\}[_^]\{[^{}]*\}\$"),
    # 字母基底 + 单下标/上标（本轮 fbase 已覆盖，应≈0）
    "single_script_unmerged": re.compile(r"[A-Za-z][A-Za-z0-9]*[ \t]*\$[_^]\{[^{}]*\}\$"),
    # 字母/数字与 $ 间仍有空格（fspace 已覆盖，应≈0）
    "space_before_dollar": re.compile(r"[A-Za-z0-9][ \t]+\$[_^]\{"),
    # 块内空组（fempty 已覆盖，应≈0）
    "empty_group": re.compile(r"[}\w\)\]][ \t]*\{\}[ \t]*[\^_]"),
    # \text 外壳（另有规则？）
    "text_wrapper": re.compile(r"\\text\{[^{}]*\\mathrm"),
    # 裸单位（kj/mol 等非数学写法）
    "bare_unit": re.compile(r"(?<![\\{A-Za-z])(kJ/mol|kJ·mol-1|g/cm3|mol/L)\b"),
}
cnt = collections.Counter()
files = collections.Counter()
for root in ROOTS:
    for dp, dn, fn in os.walk(root):
        if "images" in dp:
            continue
        for f in fn:
            if not f.endswith(".md"):
                continue
            p = os.path.join(dp, f)
            try:
                t = open(p, encoding="utf-8-sig").read()
            except Exception:
                continue
            for k, rx in pats.items():
                n = len(rx.findall(t))
                if n:
                    cnt[k] += n
                    files[k + "__files"] += 1
for k in pats:
    print("%-24s 处=%-6d 文件=%d" % (k, cnt[k], files[k + "__files"]))
