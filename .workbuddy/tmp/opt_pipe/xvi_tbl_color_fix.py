# -*- coding: utf-8 -*-
"""卷XVI 专供：修「颜色汉字波长表」（21列）的 pandoc 网格错误。

根因：源表 21 列（首列为 颜色/波长 竖排头），pandoc 只写了 20 根
gridCol×600tw、21 个 tcW×600tw（合计 12600tw > 版心 9752tw），
set_table_widths 因「行间列数不齐」护栏跳过 ⇒ LO 等比压缩 0.773 倍后
有效文字宽 14.9pt < 「950」所需 15.8pt ⇒ 波长数字折行（950→95/0）。

修法（只动该表，tblLayout 保持 fixed）：
  1) tblGrid 重写为 21 根：col0=440tw，20 根数据列均分余量（末列配平）；
  2) 全部 tcW 按列宽重写；
  3) tblPr 注入 tblCellMar 左右各 40tw（2pt），有效文字宽 19.25pt ≥ 15.8pt。
用法：python xvi_tbl_color_fix.py  （自动找 真题版式/ 下 XVI 学生版+答案版）
"""
import re
import shutil
import zipfile
from pathlib import Path

BASE = Path(r"C:\Obsidion\妙妙屋\00-首页\题组Word\初赛模拟卷\真题版式")
FILES = [
    BASE / "初赛模拟卷XVI（非有机·学生版·真题版式）.docx",
    BASE / "初赛模拟卷XVI（非有机·答案与解析版·真题版式）.docx",
]
MARK = "缁"                      # 表内容指纹（首行第2格「缁」）
TOTAL = 9752                     # 版心宽（twips），与 tblW 一致
COL0 = 440                       # 竖排头列宽
NDATA = 20
MAR = 40                         # 单元格左右边距（twips）


def patch_xml(xml: str) -> tuple[str, bool]:
    tables = re.findall(r"<w:tbl>[\s\S]*?</w:tbl>", xml)
    for t in tables:
        if MARK not in t:
            continue
        ncol = len(re.findall(r"<w:tc>", re.search(r"<w:tr(?:\s[^>]*)?>[\s\S]*?</w:tr>", t).group(0)))
        assert ncol == NDATA + 1, f"列数异常 {ncol}"
        wid = [COL0] + [0] * NDATA
        base = (TOTAL - COL0) // NDATA
        for i in range(NDATA):
            wid[1 + i] = base
        wid[-1] += TOTAL - sum(wid)  # 末列配平
        assert sum(wid) == TOTAL
        nt = t
        # 1) tblGrid
        grid = "<w:tblGrid>" + "".join(f'<w:gridCol w:w="{w}"/>' for w in wid) + "</w:tblGrid>"
        if "<w:tblGrid>" in nt:
            nt = re.sub(r"<w:tblGrid>[\s\S]*?</w:tblGrid>", grid, nt, count=1)
        else:
            nt = nt.replace("<w:tblPr>", "</w:tblPr><w:tblGrid>".join([""]) , 0)  # 不应发生
            raise AssertionError("tblGrid 缺失")
        # 2) tblCellMar 注入 tblPr（置于 tblLayout 之前，Word 容忍顺序差异）
        if "<w:tblCellMar>" not in nt:
            mar = (f'<w:tblCellMar>'
                   f'<w:left w:type="dxa" w:w="{MAR}"/>'
                   f'<w:right w:type="dxa" w:w="{MAR}"/>'
                   f'</w:tblCellMar>')
            nt = nt.replace('<w:tblLayout w:type="fixed"/>', mar + '<w:tblLayout w:type="fixed"/>', 1)
        # 3) tcW 按列重写（逐行第 j 个 <w:tc> 对应 wid[j]）
        def fix_row(row: str) -> str:
            out, last, j = [], 0, 0
            for cm in re.finditer(r"<w:tcPr>|<w:tc>", row):
                pass
            # 逐 tc 处理
            parts = re.split(r"(<w:tc>)", row)
            res = []
            j = 0
            for k, seg in enumerate(parts):
                if seg == "<w:tc>":
                    res.append(seg)
                    continue
                if "<w:tcW" in seg and j < len(wid):
                    seg = re.sub(r'<w:tcW w:type="dxa" w:w="\d+"/>',
                                 f'<w:tcW w:type="dxa" w:w="{wid[j]}"/>', seg, count=1)
                    j += 1
                res.append(seg)
            assert j == len(wid), f"tcW 重写数 {j} != {len(wid)}"
            return "".join(res)
        rows = re.split(r"(<w:tr(?:\s[^>]*)?>[\s\S]*?</w:tr>)", nt)
        nt = "".join(fix_row(r) if r.startswith("<w:tr") else r for r in rows)
        xml = xml.replace(t, nt)
        return xml, True
    return xml, False


def main():
    for f in FILES:
        assert f.exists(), f
        bak = f.with_suffix(".docx.bak_tbl")
        shutil.copy2(f, bak)
        zin = zipfile.ZipFile(bak)
        items = zin.infolist()
        xml = zin.read("word/document.xml").decode("utf-8")
        xml2, ok = patch_xml(xml)
        if not ok:
            print(f"[SKIP] {f.name}：未找到指纹表")
            continue
        with zipfile.ZipFile(f, "w", zipfile.ZIP_DEFLATED) as zout:
            for it in items:
                data = xml2.encode("utf-8") if it.filename == "word/document.xml" else zin.read(it.filename)
                zout.writestr(it, data)
        zin.close()
        print(f"[OK] {f.name}：网格 21 列已重写（col0={COL0}, 数据列均分, 边距 {MAR}tw）")


if __name__ == "__main__":
    main()
