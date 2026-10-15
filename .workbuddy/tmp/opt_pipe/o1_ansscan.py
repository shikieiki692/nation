# -*- coding: utf-8 -*-
"""O1 答案侧静态扫描（SOP §五-b 九类缺陷的机器可判部分；只读）。

逐卡扫「## 参考答案」区：
  D1 源题号残留（独立行「第N题」）
  D2 小问号粘连（行首 `N-M` 紧跟非空白）
  D4/D5 标准态错形（\theta/\Theta/裸 circ）与 OCR 残迹（\dot{…}）
  D6 评分标记形态（(N') / 半角括号 N 分）
  C1 $$ 行尾粘连（铁律二失败模式）
  C2 字面 $（解析注入缺陷 12 的前兆）
  C3 空基底（<m:e/> 前兆：\begin{array} 尾部 \\）
  D7 答案区出现「高于本卡题号」的小问组（越界闸已拦，这里复核）
"""
import os, re, sys

ROOT = r"C:\Obsidion\妙妙屋"
cards = [l.strip() for l in open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                              "o1_cards.txt"), encoding="utf-8") if l.strip()]

PAT = {
    "D1_源题号残留": re.compile(r"^#{0,4}\s*第\s*[0-9一二三四五六七八九十]+\s*题\s*[（(]", re.M),
    "D2_小问粘连": re.compile(r"^\d+-\d+(?![\d\s\-])", re.M),
    "D5_标准态错形": re.compile(r"\\theta|\\Theta|[^f]\{\\circ\}|\^\\circ(?![a-z])"),
    "D5b_OCR残迹": re.compile(r"\\dot\{|\\dot\\"),
    "D6_评分标记": re.compile(r"[（(]\s*\d+\s*['′]\s*[）)]|\(\d+\s*分\)|\d+'\s"),
    "C1_行尾$$": re.compile(r"^\s*[^$\n].*\$\$\s*$"),
    "C3_空基底": re.compile(r"\\\\\s*(?:\\hline\s*)?\\\\\s*\\end\{array\}"),
    "D7_越界问组": re.compile(r"^([5-9])-\d+-", re.M),
}

total = 0
for rel in cards:
    p = os.path.join(ROOT, rel.replace("/", os.sep))
    t = open(p, encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")
    i = t.find("## 参考答案")
    a = t[i:] if i >= 0 else ""
    if not a.strip():
        print("[无答案区] %s" % os.path.basename(rel)); continue
    own = re.search(r"题-([A-Za-z]+)-(\d+)-(\d+)-", os.path.basename(rel))
    hits = []
    for name, pat in PAT.items():
        ms = pat.findall(a)
        if ms:
            hits.append("%s×%d" % (name, len(ms)))
    # 字面 $ 统计（单个 $ 不成对出现次数粗查）
    n_dollar = len(re.findall(r"(?<!\$)\$(?!\$)", a))
    print("== %s | 答案区 %d 字 | $单=%d %s" % (
        os.path.basename(rel)[:40], len(a), n_dollar, ("| " + "；".join(hits)) if hits else "| 九类全净"))
    total += len(hits)
print("\n命中合计:", total)
