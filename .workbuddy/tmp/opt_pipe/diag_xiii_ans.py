# -*- coding: utf-8 -*-
"""卷 XIII 十卡答案区：待修点精确定位（只读）。"""
import io, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
plan = json.load(io.open(os.path.join(R, ".workbuddy/tmp/opt_pipe/vol_plan_XIII.json"), encoding="utf-8"))
cards = [c["path"] for _m, lst in plan for c in lst]

CHECK = {
    "8.5924": "第2题源答案笔误",
    "8.495": "第2题派生值",
    "\\Lambda": "第3题 A 被 OCR 成 Λ",
    "[NH_3]_2": "第4题 β₂ 分母应为平方",
    "\\left(（": "第4题 双括号",
    "第5题": "第4题 源题号",
    "第1题（10": "第6题 源题号",
    "第3题（8": "第8题 源题号",
    "2' 也可以": "第9题 标记残留",
    "<table><tr><td> $SO_{3}$ </td><td> $O_{2}$ </td><td> $SO_{3}$": "第7题 表格首列应为 SO₂",
}
for i, rel in enumerate(cards, 1):
    t = io.open(os.path.join(R, rel), encoding="utf-8-sig").read()
    a = re.search(r"^## 参考答案\s*\n(.*?)(?=^## 知识点映射|\Z)", t, re.S | re.M)
    seg = a.group(1) if a else ""
    print("=" * 96)
    print("卷内第 %2d 题 ← %s" % (i, os.path.basename(rel)[:52]))
    for pat, why in CHECK.items():
        n = t.count(pat)
        na = seg.count(pat)
        if n:
            print("   [全文 %2d / 答案区 %2d] %-42s ← %s" % (n, na, pat[:40], why))
            for m in list(re.finditer(re.escape(pat), t))[:2]:
                ctx = t[max(0, m.start() - 34):m.end() + 20].replace("\n", "⏎")
                print("         …%s…" % ctx)
