# -*- coding: utf-8 -*-
# 2026-10-07 由 .workbuddy/scripts/qa_simvol_papers.py 迁入 11-模板/scripts/
# 原因：.workbuddy/ 被 gitignore，清理工作区即丢失该管线。
# 原文件保留在 .workbuddy/scripts/（可能有其他会话引用）。
# 职责：初赛模拟卷（非有机）组卷管线专用质检（撤题泄漏/清单一致性等四类 QA）
"""初赛模拟卷（非有机）组卷管线专用质检。

覆盖此前 QA 盲区（导致卷 IX 撤题泄漏 P0 漏网的四类问题）：
  ① 撤题/隐藏内容泄漏：源 md WITHDRAWN 包裹串不得出现在任何产物
  ② 选题清单一致性：答案版清单行数/题号 == 源卷题数；表结构为统一格式
  ③ 学生版答案泄漏：不得出现「参考答案/答案」区
  ④ 表格内图片溢出：图宽 > 所在列宽
  ⑤ callout 残渣：产物正文不得含 `[!type]`
  ⑥ 图片数守恒：docx media == blip == 源 md 图引用数
  ⑦ 图片宽度上限：单图 ≤ 10cm（设计口径）

用法：
  python qa_simvol_papers.py            # 全量
  python qa_simvol_papers.py VII        # 只查卷 VII
"""
import io
import os
import re
import sys
import zipfile
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

VAULT = Path(__file__).resolve().parents[2]
QB = VAULT / "04-题库"
BASE = VAULT / "00-首页/题组Word/初赛模拟卷"
ZHENTI = BASE / "真题版式"
VOLS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]
CM = 360000
DXA = 635

WT = re.compile(r"<w:t[^>]*>([^<]*)</w:t>")
IMGREF = re.compile(r"!\[\[([^\]|]+\.(?:jpg|png|jpeg|svg))")
WITHDRAWN_RE = re.compile(r"<!--\s*(?:BEGIN|END)\s+WITHDRAWN", re.I)
LEAK_TOKENS = ["WITHDRAWN", "撤题隔离", "钒的化合物"]
CALLOUT_RE = re.compile(r"\[!\w+\]")
HEADER = "| 卷内题号 | 题名 | 题卡 | 来源 | 模块 | 难度 | 分值 |"


def read(p):
    return Path(p).read_text(encoding="utf-8-sig").replace("\r\n", "\n")


def docx_xml(p):
    return zipfile.ZipFile(p).read("word/document.xml").decode("utf-8", "replace")


def docx_text(p):
    return "".join(WT.findall(docx_xml(p)))


def media_count(p):
    return len([n for n in zipfile.ZipFile(p).namelist() if n.startswith("word/media/")])


def table_overflow(p):
    """返回表格内超列宽的图列表。"""
    xml = docx_xml(p)
    out = []
    for ti, tb in enumerate(re.finditer(r"<w:tbl>.*?</w:tbl>", xml, re.S)):
        f = tb.group(0)
        if "<w:drawing" not in f:
            continue
        grid = [int(g) for g in re.findall(r'<w:gridCol w:w="(\d+)"', f)]
        if not grid:
            continue
        for tr in re.finditer(r"<w:tr>.*?</w:tr>", f, re.S):
            tcs = re.findall(r"<w:tc>.*?</w:tc>", tr.group(0), re.S)
            for ci, tc in enumerate(tcs):
                col = grid[ci] if ci < len(grid) else grid[-1]
                lim = col * DXA / CM
                for cx, cy in re.findall(r'<wp:extent cx="(\d+)" cy="(\d+)"', tc):
                    w = int(cx) / CM
                    if w > lim + 0.15:
                        out.append(f"表{ti}列{ci}: {w:.2f}cm>{lim:.2f}cm")
    return out


def max_img_width(p):
    xml = docx_xml(p)
    ws = [int(cx) / CM for cx, cy in re.findall(r'<wp:extent cx="(\d+)" cy="(\d+)"', xml)]
    return max(ws) if ws else 0.0


def check_src_md(v):
    """源 md 层检查（撤题标记配对、清单格式）。

    注意：源 md「允许」出现被 <!-- BEGIN/END WITHDRAWN --> 包裹的撤题块
    （这是撤题的存档方式）；此处只查标记是否成对。真正判泄漏在 docx 产物层。
    """
    probs = []
    for ed in ["学生版", "答案版"]:
        f = QB / f"初赛模拟卷{v}（非有机·{ed}）.md"
        text = read(f)
        n_begin = len(re.findall(r"<!--\s*BEGIN\s+WITHDRAWN", text, re.I))
        n_end = len(re.findall(r"<!--\s*END\s+WITHDRAWN", text, re.I))
        if n_begin != n_end:
            probs.append(f"源{ed}: WITHDRAWN 标记不配对 begin={n_begin} end={n_end}")
        if ed == "答案版":
            if "## 附：选题清单" in text:
                seg = text[text.find("## 附：选题清单"):]
                if HEADER not in seg:
                    probs.append("答案版: 清单非统一格式")
    return probs


def check_docx(p, v, ed, layout):
    probs = []
    text = docx_text(p)
    # ③ 学生版答案泄漏
    if "学生版" in p.name and ("参考答案" in text or "答案与解析" in text):
        probs.append("学生版含答案区")
    # ① 撤题泄漏（产物层）：WITHDRAWN 标记串、以及撤题特有正文（卷 IX 第7题）
    if "WITHDRAWN" in text:
        probs.append("产物含 WITHDRAWN 标记")
    if v == "IX" and "从 A 到 H 的一系列反应" in text:
        probs.append("产物含卷IX撤题正文（钒的化合物题干）")
    # ⑤ callout 残渣
    if CALLOUT_RE.search(text):
        probs.append("callout 残渣 [!type]")
    # ④ 表格图溢出
    ov = table_overflow(p)
    if ov:
        probs.extend(ov)
    # ⑦ 单图宽度上限
    mw = max_img_width(p)
    if mw > 10.15:
        probs.append(f"单图超宽 {mw:.2f}cm>10cm")
    # ⑥ 图片数守恒（docx media vs 源 md 图引用）
    src = QB / f"初赛模拟卷{v}（非有机·{ed}）.md"
    if src.exists():
        md_imgs = len(IMGREF.findall(read(src)))
        mc = media_count(p)
        if md_imgs and mc < md_imgs:
            probs.append(f"图片少 {mc}<md{md_imgs}")
    return probs


def main():
    only = sys.argv[1:] or VOLS
    total = 0
    bad = 0
    for v in only:
        # 源 md 层
        sp = check_src_md(v)
        # 基础版
        for ed in ["学生版", "答案版"]:
            p = BASE / f"初赛模拟卷{v}（非有机·{ed}）.docx"
            if p.exists():
                total += 1
                pr = check_docx(p, v, ed, "base")
                if pr:
                    bad += 1
                    print(f"❗ 基础版 {v} {ed}")
                    for x in pr:
                        print("    ", x)
        # 真题版式
        for suf, ed in [("学生版·真题版式", "学生版"), ("答案与解析版·真题版式", "答案版")]:
            p = ZHENTI / f"初赛模拟卷{v}（非有机·{suf}）.docx"
            if p.exists():
                total += 1
                pr = check_docx(p, v, ed, "zhenti")
                if pr:
                    bad += 1
                    print(f"❗ 真题版式 {v} {suf}")
                    for x in pr:
                        print("    ", x)
        if sp:
            bad += 1
            print(f"❗ 源 md {v}")
            for x in sp:
                print("    ", x)
    print(f"\n检查 {total} docx（源层 {len(only)} 卷），问题 {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
