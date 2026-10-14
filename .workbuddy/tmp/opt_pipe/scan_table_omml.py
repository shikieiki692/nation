# -*- coding: utf-8 -*-
r"""扫描交付 docx：表格单元格内含 OMML 公式者（LibreOffice 列宽估算偏小 ⇒ 裁切风险）。

背景（2026-10-14 卷 XVII 实测）：
  表格单元格内的 OMML 公式会被 LibreOffice 按「估算宽度」裁切——`[H⁺]/mol·L⁻¹` 印成 `[H⁺]/mo`、
  `8.71×10⁻³` 印成 `8.71 × 10`；**qa_volX2 / qa_vol_deliver / table_wrap_audit 三闸门都看不见**。
  反证：同表**纯文本**单元格（`-`）显示正常。

本工具列出所有「表格 + 含 OMML 单元格」的组合，并给出该表列数与列宽，供**定向目检**。
用法：python scan_table_omml.py [--docs 目录] [--quiet]
"""
import os, re, sys, glob, zipfile

ROOT = r"C:\Obsidion\妙妙屋"
DOCX_DIR = os.path.join(ROOT, '00-首页', '题组Word', '初赛模拟卷', '真题版式')
QUIET = '--quiet' in sys.argv
for i, a in enumerate(sys.argv):
    if a == '--docs' and i + 1 < len(sys.argv):
        DOCX_DIR = sys.argv[i + 1]

TOT = []
for p in sorted(glob.glob(os.path.join(DOCX_DIR, '*.docx'))):
    try:
        x = zipfile.ZipFile(p).read('word/document.xml').decode('utf-8')
    except Exception:
        continue
    name = os.path.basename(p)
    tbls = re.findall(r'<w:tbl>.*?</w:tbl>', x, re.S)
    rows = []
    for ti, tb in enumerate(tbls, 1):
        grid = re.findall(r'<w:gridCol[^>]*w:w="(\d+)"', tb)
        cells = re.findall(r'<w:tc>.*?</w:tc>', tb, re.S)
        omml_cells = [c for c in cells if '<m:oMath' in c]
        if not omml_cells:
            continue
        # 取含 OMML 单元格的文本摘要（前 3 个）
        samples = []
        for c in omml_cells[:3]:
            t = ''.join(re.findall(r'<(?:w|m):t[^>]*>([^<]*)</(?:w|m):t>', c))
            samples.append(t.strip()[:26])
        rows.append((ti, len(grid), len(cells), len(omml_cells), samples))
    if rows:
        TOT.append((name, rows))

print('=' * 96)
print('交付 docx：表格内含 OMML 单元格清单（⇒ LibreOffice 裁切风险区，需定向目检）')
print('=' * 96)
tot_cells = 0
for name, rows in TOT:
    print('\n■ %s' % name)
    for ti, ncol, ncell, nomml, samples in rows:
        tot_cells += nomml
        print('   表%-2d 列%-2d 单元格%-3d ┆ 含OMML %-2d ┆ %s' % (ti, ncol, ncell, nomml, ' / '.join(samples)))
print('\n%s' % ('-' * 96))
print('合计：%d 份 docx 含此类表格 ｜ 含 OMML 单元格 %d 个' % (len(TOT), tot_cells))
print('处置：tabular 内公式**优先改纯文本 Unicode**（规避裁切）；确认可留者需逐页目检该表。')
