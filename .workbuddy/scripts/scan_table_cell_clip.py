# -*- coding: utf-8 -*-
r"""交付前扫描器：表格单元格内 OMML 被裁切（LibreOffice 列宽估算偏小）。

背景（2026-10-14 实测）：
  表格单元格内的 OMML 公式会被 LibreOffice 按「估算宽度」裁切 ——
  卷 XVII 第 10 题：`[H⁺]/mol·L⁻¹` 印成 `[H⁺]/mo`、`8.71×10⁻³` 印成 `8.71 × 10`；
  卷 XVI 第 2 题：`V_ads/(cm³·g⁻¹)` 印成 `V_ads/(c`。
  **qa_volX2 / qa_vol_deliver / table_wrap_audit 三闸门都看不见**（裁切发生在渲染层）。
  反证：同表**纯文本**单元格显示正常。

判据（三步）：
  ① 清单化：docx 中「表格 + 含 OMML 单元格」全部列出；
  ② 筛疑：该单元格文本与**同卷已渲染 PDF 全文**比最长前缀匹配率 —— <90% 疑、<70% 高疑；
  ③ 定性：`--pages` 输出疑点页号 ⇒ **必须逐页目检**（实测真阳性率约 1/5，PDF 字符差异会误报）。

用法（**须用带 pymupdf 的解释器**，如受管 venv）：
  python scan_table_cell_clip.py                  # 全部交付 docx
  python scan_table_cell_clip.py --vol XVI        # 指定卷
  python scan_table_cell_clip.py --pages          # 附疑点页号
  python scan_table_cell_clip.py --quiet          # 只输出汇总
退出码：0 = 无疑点；1 = 有高疑（<70%，须目检）。
"""
import os, re, sys, glob, zipfile

ROOT = r"C:\Obsidion\妙妙屋"
DOCX_DIR = os.path.join(ROOT, '00-首页', '题组Word', '初赛模拟卷', '真题版式')
PDF_ROOT = os.path.join(ROOT, '.workbuddy', 'tmp', 'opt_pipe', 'render_gate_out')

VOL = None
for i, a in enumerate(sys.argv):
    if a == '--vol' and i + 1 < len(sys.argv):
        VOL = sys.argv[i + 1]
PAGES = '--pages' in sys.argv
QUIET = '--quiet' in sys.argv

try:
    import pymupdf
except ImportError:
    pymupdf = None


# ★ 字符归一化表：消解 PDF 文本提取与 docx 的**符号变体**差异（这是本判据的主要误报源）
TRANS = str.maketrans({
    '∘': '°', '\u2212': '-', '\u2013': '-', '\u2014': '-',   # 度符号 / 各种减号
    '⋅': '·', '\u00b7': '·',                                  # 点乘
    '（': '(', '）': ')', '，': ',', '：': ':',               # 全角→半角
    '\u00a0': '', '\u2009': '', '\u200b': '',                 # 各类窄空格/零宽
})


def norm(s):
    return re.sub(r'\s+', '', s.translate(TRANS))


def omml_cells(docx_path):
    """[(表序, 列数, 单元格文本)]，仅含 OMML 者。"""
    x = zipfile.ZipFile(docx_path).read('word/document.xml').decode('utf-8')
    out = []
    for ti, tb in enumerate(re.findall(r'<w:tbl>.*?</w:tbl>', x, re.S), 1):
        ncol = len(re.findall(r'<w:gridCol', tb))
        for c in re.findall(r'<w:tc>.*?</w:tc>', tb, re.S):
            if '<m:oMath' not in c:
                continue
            t = ''.join(re.findall(r'<(?:w|m):t[^>]*>([^<]*)</(?:w|m):t>', c)).strip()
            if t:
                out.append((ti, ncol, t))
    return out


def longest_prefix(a, b):
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if a[:mid] in b:
            lo = mid
        else:
            hi = mid - 1
    return lo


rows_inventory, suspects, high = [], [], []
for docx in sorted(glob.glob(os.path.join(DOCX_DIR, '*.docx'))):
    name = os.path.basename(docx)[:-5]
    # ⚠️ 必须带分隔符匹配：`卷XVI` 是 `卷XVII` 的子串（曾致 --vol XVI 误含 XVII）
    if VOL and ('卷%s（' % VOL) not in name:
        continue
    cells = omml_cells(docx)
    if not cells:
        continue
    rows_inventory.append((name, len(cells)))
    pdfs = glob.glob(os.path.join(PDF_ROOT, name, '*.pdf'))
    if not pdfs or pymupdf is None:
        continue
    d = pymupdf.open(pdfs[0])
    pages = [norm(pg.get_text()) for pg in d]
    full = '\n'.join(pages)
    d.close()
    for ti, ncol, t in cells:
        n = norm(t)
        if len(n) < 5 or n in full:
            continue
        r = longest_prefix(n, full) / len(n)
        if r >= 0.90:
            continue
        pg = None
        if PAGES:
            pg = next((i + 1 for i, p in enumerate(pages) if n[:max(3, len(n) // 3)] in p), None)
        rec = (name, ti, ncol, t, r, pg)
        suspects.append(rec)
        if r < 0.70:
            high.append(rec)

if not QUIET:
    print('=' * 96)
    print('表格单元格 OMML 裁切扫描（交付前）')
    print('  交付 docx 含 OMML 表格单元格：%d 份 / %d 个' % (len(rows_inventory), sum(n for _, n in rows_inventory)))
    print('-' * 96)
    if suspects:
        print('疑点（匹配率 <90%）：')
        for name, ti, ncol, t, r, pg in suspects:
            print('  %-42s 表%-2d 列%-2d %3.0f%%%s  %s'
                  % (name[:42], ti, ncol, r * 100, (' 页%-3s' % pg) if pg else '', t[:40]))
    print('-' * 96)
print('结果：疑点 %d ｜ 其中高疑(<70%%) %d' % (len(suspects), len(high)))
print('VERDICT:', 'FAIL(须逐页目检定性)' if high else ('WARN' if suspects else 'PASS'))
sys.exit(1 if high else 0)
