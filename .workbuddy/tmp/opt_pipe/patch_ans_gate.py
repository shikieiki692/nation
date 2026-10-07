#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""patch_ans_gate.py —— 给 build_org 加「答案可用闸」。
判据（保守）：答案区**无图** 且（① 仅题干回显 ≥0.75 或 ② 手写 OCR 乱码评分符 ≥3）⇒ 弃卡。
"""
import re, sys
sys.stdout.reconfigure(encoding="utf-8")
P = r"C:\Obsidion\妙妙屋\.workbuddy\tmp\opt_pipe\build_org.py"
s = open(P, encoding="utf-8").read()
orig = s

# 1) 常量
anchor1 = "HANDWRITTEN = re.compile(r'awsl|yyds|栓Q|xswl|nsdd|凑不出|瞎写|乱写|随便写|懒得写|不会画')"
assert anchor1 in s, "anchor1 未命中"
if "SCOREMARK = " not in s:
    s = s.replace(anchor1, anchor1 + """
SCOREMARK = re.compile(r"(?<![\\d.])\\d{1,2}(?:\\.\\d)?\\s*['\\u2032\\u2019]")   # 手写评分符 1' 0.5'
ECHO_HITS = []            # 答案可用闸：仅题干回显
GARB2_HITS = []           # 答案可用闸：手写 OCR 乱码


def contain_ratio(inner, outer):
    \"\"\"inner 中有多少 8-gram 出现在 outer 里（判「仅题干回显」）。\"\"\"
    if len(inner) < 8:
        return 1.0 if inner and inner in outer else 0.0
    gs = [inner[i:i + 8] for i in range(0, len(inner) - 7, 4)]
    if not gs:
        return 0.0
    return sum(1 for g in gs if g in outer) / len(gs)
""", 1)

# 2) 重置
s = s.replace("OVERFLOW_HITS.clear(); HANDWRITTEN_HITS.clear()",
              "OVERFLOW_HITS.clear(); HANDWRITTEN_HITS.clear(); ECHO_HITS.clear(); GARB2_HITS.clear()")

# 3) 闸门本体（插在手写稿闸之后）
anchor2 = """            if HANDWRITTEN.search(_HW_STRIP.sub(' ', q + ' ' + a)):
                HANDWRITTEN_HITS.append(p.replace(os.sep, '/'))
                continue"""
assert anchor2 in s, "anchor2 未命中"
if "# ★ 答案可用闸" not in s:
    s = s.replace(anchor2, anchor2 + """
            # ★ 答案可用闸：答案区无图 且（仅题干回显 / 手写 OCR 乱码）⇒ 弃卡
            if '![[' not in a:
                _an = re.sub(r'\\s+', '', a); _qn = re.sub(r'\\s+', '', q)
                if len(_an) >= 25 and contain_ratio(_an, _qn) >= 0.75:
                    ECHO_HITS.append(p.replace(os.sep, '/')); continue
                if len(SCOREMARK.findall(a)) >= 3:
                    GARB2_HITS.append(p.replace(os.sep, '/')); continue""", 1)

# 4) 打印
anchor3 = """    if OVERFLOW_HITS:"""
if "── ★ 答案可用闸" not in s:
    s = s.replace(anchor3, """    if ECHO_HITS:
        print('  ── ★ 答案可用闸：仅题干回显 %d 卡' % len(ECHO_HITS))
    if GARB2_HITS:
        print('  ── ★ 答案可用闸：手写 OCR 乱码 %d 卡' % len(GARB2_HITS))
    if OVERFLOW_HITS:""", 1)

open(P, "w", encoding="utf-8", newline="\n").write(s)
print("patched" if s != orig else "NO CHANGE")
print("checks:", "SCOREMARK" in s, "答案可用闸" in s, "contain_ratio" in s)
