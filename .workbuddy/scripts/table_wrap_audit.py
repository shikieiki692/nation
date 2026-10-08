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
            print(f"  [表{ti}] gridCol {len(ws)} != ncol {ncol} 跳过")
            continue
        need = [0.0] * ncol
        for r in rows:
            for j, txt in enumerate(cells(r)):
                need[j] = max(need[j], _txt_pt(txt))
        flags = [j for j in range(ncol) if need[j] > ws[j] / 20.0 - CELL_PAD]
        hdr = "/".join(cells(rows[0]))[:48]
        print(f"  [表{ti}] {'OK  ' if not flags else '折行'} 列宽={[round(x / 20, 2) for x in ws]}pt "
              f"需={[round(x, 1) for x in need]}pt 表头={hdr!r}")
        for j in flags:
            print(f"        ↳ col{j}: 列宽 {ws[j] / 20:.2f}pt < 需 {need[j] + CELL_PAD:.2f}pt")
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
