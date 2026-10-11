# -*- coding: utf-8 -*-
"""make_visual_checklist.py —— P1-8：生成「含图题必检清单」并导出必检页 PNG。

为什么要它（SOP 铁律三）：含图题的**答案区**若为结构图/手写扫描件，必须逐张目检原图；
但整卷逐页目检代价高（卷 XVI 实测 91 页）。本工具把「必须看的页」圈出来：
  ① 逐题统计「题面图数 / 答案区图数」（答案区有图 ⇒ **必检**）；
  ② 从交付 PDF（render_gate_out 里的 LibreOffice 产物）定位这些题所在页并导出 PNG；
  ③ 打印清单（题号/题名/图数/页码），直接当目检底稿。

用法：
    python make_visual_checklist.py --vol XVI [--dpi 130]
产出（均在被 gitignore 的 tmp 下）：
    .workbuddy/tmp/opt_pipe/visual_check/卷XVI/清单.md
    .workbuddy/tmp/opt_pipe/visual_check/卷XVI/ans_pNN.png
"""
import argparse
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
OUTROOT = os.path.join(R, ".workbuddy/tmp/opt_pipe/visual_check")
RENDER = os.path.join(R, ".workbuddy/tmp/opt_pipe/render_gate_out")
DELIV = os.path.join(R, "00-首页/题组Word/初赛模拟卷/真题版式")

IMG = re.compile(r"!\[\[([^\]\|\\]+?)(?:\\?\|\d+)?\]\]")


def parse_vol(vol):
    """返回 [(题号, 题名, 来源, 题面图数, 答案图数, 题面文本首行)]。"""
    p = os.path.join(R, "04-题库", "初赛模拟卷%s（非有机·答案版）.md" % vol)
    t = open(p, encoding="utf-8-sig").read().replace("\r\n", "\n")
    parts = re.split(r"^### 第 (\d+) 题", t, flags=re.M)
    rows = []
    for k in range(1, len(parts), 2):
        no = int(parts[k])
        body = parts[k + 1]
        head, _, rest = body.partition("#### 答案")
        ans = rest.split("> —— 解析 ——")[0] if rest else ""
        m = re.search(r"^（\d+ 分）?([^\n]{0,26})", head.strip())
        title = (m.group(1).strip() if m else "") or ""
        ms = re.search(r"^> 来源：(.+)$", head, re.M)
        src = ms.group(1).strip() if ms else ""
        rows.append((no, title[:24], src[:40], len(IMG.findall(head)), len(IMG.findall(ans))))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vol", required=True)
    ap.add_argument("--dpi", type=int, default=130)
    A = ap.parse_args()
    vol = A.vol
    rows = parse_vol(vol)
    outdir = os.path.join(OUTROOT, "卷%s" % vol)
    os.makedirs(outdir, exist_ok=True)

    # 定位交付 PDF（render_gate_out 里按 docx 名建目录）
    cand = [d for d in os.listdir(RENDER) if ("卷%s（" % vol) in d and "答案" in d]
    pdf = None
    if cand:
        d = os.path.join(RENDER, cand[0])
        pdfs = [f for f in os.listdir(d) if f.endswith(".pdf")]
        if pdfs:
            pdf = os.path.join(d, pdfs[0])
    pages = {}
    ranges = {}
    if pdf:
        import pymupdf
        doc = pymupdf.open(pdf)
        page_text = [pg.get_text() for pg in doc]
        # ① 用**题名**定位每题起始页（「第N题」会出现在交叉引用里，不可靠）
        for no, title, _s, _q, _a in rows:
            key = re.sub(r"\s+", "", title) if title else ""
            start = None
            if len(key) >= 4:
                for i, t in enumerate(page_text):
                    if key in re.sub(r"\s+", "", t):
                        start = i + 1
                        break
            if start is None:                     # 回退：题头「第 N 题（d 分）」
                pat = re.compile(r"第\s*%d\s*题\s*[（(]\s*\d+\s*分" % no)
                for i, t in enumerate(page_text):
                    if pat.search(t):
                        start = i + 1
                        break
            pages[no] = start
        # ② 每题页区间 = 本题起始页 → 下一题起始页-1
        starts = sorted([(pages[n], n) for n, _t, _s, _q, _a in rows if pages.get(n)])
        for idx, (st, no) in enumerate(starts):
            end = (starts[idx + 1][0] - 1) if idx + 1 < len(starts) else doc.page_count
            ranges[no] = (st, end)
        exported = []
        need_pages = set()
        img_pages = {}                     # 题号 → 区间内含图的页
        for no, _t, _s, _q, a in rows:
            if a > 0 and no in ranges:
                r0, r1 = ranges[no]
                rng = set(range(r0, r1 + 1))
                withimg = {p for p in rng if doc[p - 1].get_image_info()}
                img_pages[no] = sorted(withimg)
                # 导出＝区间内含图的页 ∪ 该题起始页（起始页给语境）
                need_pages |= (withimg | {r0})
        for pno in sorted(need_pages):
            pix = doc[pno - 1].get_pixmap(dpi=A.dpi)
            f = os.path.join(outdir, "ans_p%02d.png" % pno)
            pix.save(f)
            exported.append((pno, os.path.basename(f)))
        doc.close()
    else:
        exported = []
        img_pages = {}

    lines = ["# 卷 %s 含图题·必检清单（P1-8 自动生成）\n" % vol,
             "| 题号 | 题名 | 题面图 | 答案区图 | 判定 | 该题页区间 | 区间含图页 |",
             "|---|---|---:|---:|---|---|---|"]
    must = 0
    for no, title, _src, q, a in rows:
        verdict = "**必回源目检**" if a > 0 else ("题面图（可抽检）" if q > 0 else "无图")
        if a > 0:
            must += 1
        rg = ranges.get(no)
        rgs = ("p%d–p%d" % rg) if rg else "—"
        ip = img_pages.get(no) or []
        ipc = ("、".join("p%d" % x for x in ip) if ip else "—")
        lines.append("| %d | %s | %d | %d | %s | %s | %s |"
                     % (no, title or "—", q, a, verdict, rgs, ipc))
    tot_q = sum(r[3] for r in rows)
    tot_a = sum(r[4] for r in rows)
    lines += ["", "题面图合计 %d ｜ 答案区图合计 %d ｜ **答案区含图题数（必检）%d / %d**" % (tot_q, tot_a, must, len(rows))]
    if exported:
        lines += ["", "已导出必检页 PNG %d 张（%s）：%s" % (
            len(exported), "卷%s" % vol, "、".join("p%d" % p for p, _f in exported))]
    else:
        lines += ["", "⚠️ 未找到交付 PDF（先跑 qa_vol_render 生成 render_gate_out，或手动指定）。"]
    out = os.path.join(outdir, "清单.md")
    open(out, "w", encoding="utf-8", newline="").write("\n".join(lines) + "\n")
    print("\n".join(lines))
    print("\n→ 清单：", out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
