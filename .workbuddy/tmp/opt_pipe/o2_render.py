# -*- coding: utf-8 -*-
r"""o2_render.py —— O2 回源渲染（**按 FM source_file 权威定位**，绕开会错配的 locate_pdf）。

对每张卡：
  · 试题 PDF：文字层 ⇒ 8-gram 命中页渲染（前 2 页）；扫描件 ⇒ 全页缩略图
  · 答案 PDF：同上（另册）
输出：.workbuddy/tmp/opt_pipe/locate_out/o2v/<tag>/q_pNN.png | a_pNN.png | thumb_pNN.png
"""
import os
import re
import sys

import fitz

ROOT = r"C:/Obsidion/妙妙屋"
OUT = os.path.join(ROOT, ".workbuddy", "tmp", "opt_pipe", "locate_out", "o2v")
B = "06-外部资料导入/OCR/01-题目"
YJ = B + "/2026年壹尖培优夏令营（国初高端冲刺营）"
CH = "06-外部资料导入/OCR/chemy/第39届Chemy化学奥林匹克竞赛模拟试题参考答案合集/第39届Chemy化学奥林匹克竞赛模拟试题参考答案合集._200-329.pdf"

JOBS = [
    # (卡, 试题 PDF, 答案 PDF)
    ("04-题库/2026机构初赛模拟题/化英社/题-HYS-11-08-酶催化有机合成可以利用生物催.md",
     B + "/第40届化英社化学奥林匹克（初赛）夏季/第40届化英社化学奥林匹克（初赛）夏季模拟试题11.pdf",
     B + "/第40届化英社化学奥林匹克（初赛）夏季/第40届化英社化学奥林匹克(初赛)夏季初赛模拟11参考答案.pdf"),
    ("04-题库/2026机构初赛模拟题/清北营/题-QBY-17-08-近些年来有关金属催化的有机反.md",
     B + "/2026清北营夏令营/清北营高二试卷（前13套）/2026年清北营暑假高二班-试卷17.pdf",
     B + "/2026清北营夏令营/清北营高二试卷（前13套）/2026年清北营暑假高二班-试卷17-参考答案.pdf"),
    ("04-题库/2026机构初赛模拟题/chemy/题-CM-207-09-在药物分子中吡唑环是一个十分常见.md", CH, CH),
    ("04-题库/2026机构初赛模拟题/伽马/题-GM-10-08-8112021年Richmo.md",
     B + "/2026伽马暑假刷题班/伽马化学2026年暑期模拟10.pdf",
     B + "/2026伽马暑假刷题班/伽马化学2026年暑期模拟10答案.pdf"),
    ("04-题库/2026机构初赛模拟题/壹尖培优/题-YJ-09-06-费托合成FischerTro.md",
     YJ + "/第40届中国化学奥林匹克（初赛）模拟试题和答题卡/第 40 届中国化学奥林匹克（初赛）模拟试题9.pdf",
     YJ + "/第40届中国化学奥林匹克（初赛）模拟试题答案/第 40 届中国化学奥林匹克（初赛）模拟试题9参考答案.pdf"),
    ("04-题库/2026机构初赛模拟题/化英社/题-HYS-40-09-23Wittig重排是一类重.md",
     B + "/2026年化英社春季联考线上班/化英社春季联考6/第40届化英社化学奥林匹克（初赛）春季联考6-final.pdf",
     B + "/2026年化英社春季联考线上班/化英社春季联考6/第40届化英社化学奥林匹克（初赛）春季联考6 答案-final.pdf"),
    ("04-题库/2026机构初赛模拟题/清北营/题-QBY-01-06-某类有机发光小分子可以可逆形.md",
     B + "/2026年清北营寒假班/2026年清北营寒假高二班试卷（未修订版）(1)/2026年清北营寒假班-试卷1.pdf",
     B + "/2026年清北营寒假班/2026年清北营寒假高二班试卷（未修订版）(1)/2026年清北营寒假班-试卷1-参考答案.pdf"),
    ("04-题库/2026机构初赛模拟题/chemy/题-CM-17-08-烷烃构象中的取代基排斥不仅取.md",
     B + "/2026年chemy夏令营/第40届chemy夏季班/第40届chemy初赛模拟17/第40届chemy初赛模拟17试题.pdf",
     B + "/2026年chemy夏令营/第40届chemy夏季班/第40届chemy初赛模拟17/第40届chemy初赛模拟17答案.pdf"),
    ("04-题库/2026机构初赛模拟题/伽马/题-GM-09-10-C19二萜生物碱C19DTA.md",
     B + "/2026伽马暑假刷题班/伽马化学2026年暑期模拟9.pdf",
     B + "/2026伽马暑假刷题班/伽马化学2026年暑期模拟9答案.pdf"),
    ("04-题库/2026机构初赛模拟题/壹尖培优/题-YJ-04-08-本题要求立体化学中药甘遂为大.md",
     YJ + "/第40届中国化学奥林匹克（初赛）模拟试题和答题卡/第 40 届中国化学奥林匹克（初赛）模拟试题4.pdf",
     YJ + "/第40届中国化学奥林匹克（初赛）模拟试题答案/第 40 届中国化学奥林匹克（初赛）模拟试题4参考答案.pdf"),
]


def hanzi(s):
    return re.sub(r"[^\u4e00-\u9fff]", "", s)


def section(txt, *names):
    for nm in names:
        # ★ 结束前瞻必须是「恰好两个 #」（`##(?!\#)`）——原写法 `^##[ \t]*\S` 会匹配 `### 第 N 题`，
        #   导致「## 题目」段被瞬间截断为空 ⇒ 题面 8-gram 恒 0（假「覆盖 0.00」）。
        m = re.search(r"^##[ \t]*" + nm + r"[ \t]*\n(.*?)(?=^##(?!\#)[ \t]*\S|^##[ \t]*$|\Z)", txt, re.S | re.M)
        if m:
            return m.group(1)
    return txt


def clean(t):
    t = re.sub(r"!\[\[?[^\]]*\]?\]", " ", t)
    t = re.sub(r"\$\$.*?\$\$", " ", t, flags=re.S)
    return re.sub(r"\$[^$]*\$", " ", t)


def grams(s, k=8):
    return [s[i:i + k] for i in range(0, max(1, len(s) - k + 1), k)]


def rank(pages_h, text, topn=2):
    gs = grams(hanzi(clean(text)))
    sc = [(sum(1 for g in gs if g in ph), i) for i, ph in enumerate(pages_h)]
    sc.sort(reverse=True)
    return [i for s, i in sc[:topn] if s > 0], sc[:3]


def main():
    only = sys.argv[1:] or None
    for card, qpdf, apdf in JOBS:
        if only and not any(o in card for o in only):
            continue
        txt = open(os.path.join(ROOT, card), encoding="utf-8-sig").read()
        tag = os.path.basename(card)[2:24]
        d = os.path.join(OUT, tag)
        os.makedirs(d, exist_ok=True)
        print("=" * 96)
        print("### %s" % os.path.basename(card)[:58])
        for kind, pdf, secs, topn in (("q", qpdf, ("题目",), 3), ("a", apdf, ("参考答案", "答案"), 3)):
            p_ = os.path.join(ROOT, pdf)
            if not os.path.isfile(p_):
                print("   [%s] !! PDF 不存在: %s" % (kind, pdf))
                continue
            with fitz.open(p_) as doc:
                n = doc.page_count
                ph = [hanzi(doc[i].get_text()) for i in range(n)]
                has = len("".join(ph).strip()) > 80
                print("   [%s] %s | 页数=%d 文字层=%s" % (kind, os.path.basename(pdf)[:52], n, "有" if has else "无(扫描)"))
                if has:
                    pgs, sc = rank(ph, section(txt, *secs), topn=topn)
                    print("        命中页:", [p + 1 for p in pgs], "| top3 得分:", [(i + 1, s) for s, i in sc])
                    if pgs:
                        for p in pgs:
                            doc[p].get_pixmap(dpi=130).save(os.path.join(d, "%s_p%02d.png" % (kind, p + 1)))
                    else:
                        # ★ 文字层存在但 8-gram 零命中（多为「扫描图＋薄页眉文字层」）⇒ 退回全页缩略图
                        for p in range(n):
                            doc[p].get_pixmap(dpi=60).save(os.path.join(d, "thumb_%s_p%02d.png" % (kind, p + 1)))
                        print("        ⚠ 文字层命中 0 ⇒ 退回全页缩略图 %d 张" % n)
                else:
                    for p in range(n):
                        doc[p].get_pixmap(dpi=60).save(os.path.join(d, "thumb_%s_p%02d.png" % (kind, p + 1)))
                    print("        扫描件：出 %d 张缩略图" % n)


if __name__ == "__main__":
    main()
