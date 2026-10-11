# -*- coding: utf-8 -*-
"""卷XVI 收口 QA：回源抽查 v2（直接读源 PDF 文字层）。"""
import os
import re

import pymupdf

VAULT = r"C:\Obsidion\妙妙屋"
P = {
    "Q6 汇智模拟1": r"06-外部资料导入\OCR\01-题目\2026年8月汇智长沙夏令营刷题班\2026暑假长沙化学刷题试题\长沙化学刷初赛模拟1.pdf",
    "Q11 chemy17试题": r"06-外部资料导入\OCR\01-题目\2026年chemy夏令营\第40届chemy夏季班\第40届chemy初赛模拟17\第40届chemy初赛模拟17试题.pdf",
    "Q11 chemy17答案": r"06-外部资料导入\OCR\01-题目\2026年chemy夏令营\第40届chemy夏季班\第40届chemy初赛模拟17\第40届chemy初赛模拟17答案.pdf",
    "Q7 XeChem（十）": r"06-外部资料导入\OCR\01-题目\2026年XeChem6月线上班\Xe6月网课资料\模拟试题\第40届XeChem初赛模拟试题（十）.pdf",
    "Q3 chemy12试卷": r"06-外部资料导入\OCR\01-题目\2026年chemy夏令营\第40届chemy夏季班\第40届chemy初赛模拟12\第40届chemy初赛模拟12试卷.pdf",
}


def text_of(rel, need_pages=None):
    p = os.path.join(VAULT, rel)
    if not os.path.exists(p):
        return None
    d = pymupdf.open(p)
    parts = []
    for i, pg in enumerate(d):
        parts.append((i + 1, pg.get_text()))
    d.close()
    return parts


def probe(label, parts, keys, ctx=70):
    print(f"\n=== {label}  （{len(parts) if parts else 0} 页）")
    if not parts:
        print("    <文件缺失>")
        return
    for k in keys:
        kk = re.sub(r"\s+", "", k)
        found = None
        for no, t in parts:
            flat = re.sub(r"\s+", "", t)
            i = flat.find(kk)
            if i >= 0:
                found = (no, flat[max(0, i - ctx): i + len(kk) + ctx])
                break
        if found:
            print(f"    ✓ p{found[0]:<3} {k}\n         …{found[1]}…")
        else:
            print(f"    ✗ 未找到 {k}")


probe("Q6 · 汇智《长沙化学刷初赛模拟1》", text_of(P["Q6 汇智模拟1"]), [
    "KCu(CN)2中含铜阴离子的结构", "目前制备CuCN的最好方法", "DMSO", "Cu6(CN)8",
    "正八面体", "越少", "避免",
])
probe("Q11 · chemy 模拟17 试题", text_of(P["Q11 chemy17试题"]), [
    "206pm", "基序", "S12", "液态硫", "5-2-3",
])
probe("Q11 · chemy 模拟17 答案", text_of(P["Q11 chemy17答案"]), [
    "331", "448", "3.90", "手性",
])
probe("Q7 · XeChem（十）", text_of(P["Q7 XeChem（十）"]), [
    "2014年", "硅簇", "CsNa9Si17", "Si4", "编号",
])
probe("Q3 · chemy 模拟12 试卷", text_of(P["Q3 chemy12试卷"]), [
    "回文", "DLX", "三方晶系", "33342",
])
