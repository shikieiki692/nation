# -*- coding: utf-8 -*-
"""交付物「表格折行」审计（只读）——机构模拟卷组卷线 SOP ⑤-b。

用途：出完 docx 后，扫描卷内每张表的每一列，用「字体度量模型」算出该列
      最长单元格**单行所需宽度**，与 tblGrid 实际列宽比对，标出会折行的列。
      配合 build_chusai_zhenti_layout 的 `set_table_widths` / `set_list_table_widths`
      （两者共用同一度量模型，单一真源）。

用法：
    python table_wrap_audit.py                # 只审 5 卷的「答案与解析版」
    python table_wrap_audit.py -all           # 审 真题版式 目录下全部 docx
    python table_wrap_audit.py -v             # 附带「会折行列」的逐行单元格内容
    python table_wrap_audit.py <docx 路径>     # 只审指定文件

判读：
    · 清单表的「卷内题号」表头设计上折两行（内容只有 1~2 位数字）⇒ 报折行属预期；
    · 「题名」「题卡」为长文本列，必然折行 ⇒ 属预期；
    · 其余列报折行即为**缺陷**（应回到 `build_chusai_zhenti_layout` 的度量模型查因）。

★ 2026-10-11：**边距按表自带 `tblCellMar` 计**（此前固定用布局工具的默认 CELL_PAD ⇒ 对
  「显式收紧边距」的表（如卷 XVI 的 21 列颜色表，边距 40tw=2pt×2）会误报折行，实测假阳性）。
"""
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(r"C:\Obsidion\妙妙屋")
sys.path.insert(0, str(ROOT / ".workbuddy" / "scripts"))
from build_chusai_zhenti_layout import CELL_PAD, TEXT_W_TW, _txt_pt   # noqa: E402

BASE = ROOT / "00-首页" / "题组Word" / "初赛模拟卷" / "真题版式"
CELL_RE = re.compile(r"<w:tc>[\s\S]*?</w:tc>")
ROW_RE = re.compile(r"<w:tr\b[\s\S]*?</w:tr>")
TBL_RE = re.compile(r"<w:tbl>[\s\S]*?</w:tbl>")
GRID_RE = re.compile(r"<w:tblGrid>[\s\S]*?</w:tblGrid>")
W_TXT = re.compile(r"<w:t(?:\s[^>]*)?>([\s\S]*?)</w:t>")
CELLMAR_RE = re.compile(r"<w:tblCellMar>[\s\S]*?</w:tblCellMar>")


def cell_pad_pt(tbl_xml):
    """表自带单元格左右边距（pt）；未显式声明 ⇒ None（回落到默认 CELL_PAD）。"""
    m = CELLMAR_RE.search(tbl_xml)
    if not m:
        return None
    tot = 0.0
    for tag in ("left", "right"):
        mm = re.search(r"<w:%s\b[^>]*?w:w=\"(-?\d+)\"" % tag, m.group(0))
        if mm:
            tot += int(mm.group(1)) / 20.0
    return tot if tot > 0 else None


def is_vert_head(tbl_xml, col_idx, max_len=4):
    """判「竖排表头列」：**仅第 0 列**，且表头格是汉字（≤max_len 字）、其余格是短标签
    （≤max_len 字的汉字或数字）。源卷的「颜色/波长」「卷内题号」就是这样竖着写，
    列窄⇒一字一行属**设计**，不是折行缺陷。

    ⚠️ 只对**首列**放行：数据列（col≥1）折行仍照报——「950 折成 95/0」那类才是真缺陷。
    """
    if col_idx != 0:
        return False
    rows = ROW_RE.findall(tbl_xml)
    if not rows:
        return False
    hdr = cells(rows[0])[0] if cells(rows[0]) else ""
    hdr_c = re.sub(r"[\s\u200b]", "", hdr)
    if re.fullmatch(r"[\u4e00-\u9fff]{1,%d}" % max_len, hdr_c) is None:
        return False
    for r in rows:
        cs = cells(r)
        if not cs:
            continue
        t = re.sub(r"[\s\u200b]", "", cs[0])
        if not t:
            continue
        if re.fullmatch(r"[\u4e00-\u9fff]{1,%d}|\d{1,%d}" % (max_len, max_len), t) is None:
            return False
    return True


def cells(row):
    out = []
    for c in CELL_RE.findall(row):
        t = "".join(W_TXT.findall(c))
        out.append(t.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">"))
    return out


def audit(path, verbose=False):
    xml = zipfile.ZipFile(str(path)).read("word/document.xml").decode("utf-8")
    print(f"\n### {path.name}")
    for ti, t in enumerate(TBL_RE.findall(xml)):
        rows = ROW_RE.findall(t)
        if not rows:
            continue
        ncol = max(len(cells(r)) for r in rows)
        if any(len(cells(r)) not in (ncol,) for r in rows):
            print(f"  [表{ti}] 列数不齐（合并单元格）跳过 ncolmax={ncol}")
            continue
        g = GRID_RE.search(t)
        ws = [int(x) for x in re.findall(r'w:w="(-?\d+)"', g.group(0))] if g else []
        if len(ws) != ncol:
            print(f"  [表{ti}] ✗ gridCol {len(ws)} != ncol {ncol} ⇒ **网格错误**（pandoc 对含合并首列的表会写错列数；"
                  f"渲染器将等比压缩/错位，必查）")
            continue
        # ★ 2026-10-11：grid 总宽 vs tblW —— 卷 XVI 颜色表的真实病根正是这条
        #   （20 根 gridCol×600tw = 12000tw > 表宽 9752tw ⇒ LO 等比压缩 0.773 ⇒ 波长「950」折成「95/0」）。
        tw = re.search(r'<w:tblW\b[^>]*?w:w="(-?\d+)"', t)
        total_w = int(tw.group(1)) if tw else None
        if total_w and sum(ws) > total_w * 1.005:
            print(f"  [表{ti}] ✗ **grid 总宽 {sum(ws) / 20:.1f}pt > 表宽 {total_w / 20:.1f}pt**"
                  f"（超 {(sum(ws) - total_w) / 20:.1f}pt）⇒ 渲染器等比压缩 ⇒ 列宽失真/数字折行，必查")
            continue
        need = [0.0] * ncol
        for r in rows:
            for j, txt in enumerate(cells(r)):
                need[j] = max(need[j], _txt_pt(txt))
        pad = cell_pad_pt(t) or CELL_PAD          # ★ 优先用表自带边距
        flags = [j for j in range(ncol) if need[j] > ws[j] / 20.0 - pad]
        vhead = [j for j in flags if is_vert_head(t, j)]
        # 「长文本列」：单行需宽 >100pt（题名/题卡/源 HTML 表长单元格）——版心 487pt 内
        # 本就不可能单行容纳，折行即**设计**；而「950 折成 95/0」那类 need 很小 ⇒ 仍会报。
        longc = [j for j in flags if j not in vhead and need[j] > 100.0]
        flags = [j for j in flags if j not in vhead and j not in longc]
        hdr = "/".join(cells(rows[0]))[:48]
        tag = "OK  " if not flags else "折行"
        note = ""
        if vhead or longc:
            parts = []
            if vhead:
                parts.append("%d 处竖排表头" % len(vhead))
            if longc:
                parts.append("%d 处长文本列" % len(longc))
            note = "，".join(parts) + "（设计/预期）"
        print(f"  [表{ti}] {tag} 列宽={[round(x / 20, 2) for x in ws]}pt "
              f"需={[round(x, 1) for x in need]}pt 边距={pad:.1f}pt 表头={hdr!r}"
              + (f"，{note}" if note else ""))
        for j in flags:
            print(f"        ↳ col{j}: 列宽 {ws[j] / 20:.2f}pt < 需 {need[j] + pad:.2f}pt")
        if flags and verbose:
            for ri, r in enumerate(rows):
                print(f"        行{ri}: {[c[:36] for c in cells(r)]}")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    verbose = "-v" in sys.argv
    if args:
        audit(Path(args[0]), verbose)
        return
    pat = "*.docx" if "-all" in sys.argv else "*答案与解析版·真题版式）.docx"
    for p in sorted(BASE.glob(pat)):
        audit(p, verbose)


if __name__ == "__main__":
    main()
