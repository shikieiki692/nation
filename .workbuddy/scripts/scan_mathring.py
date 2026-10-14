# -*- coding: utf-8 -*-
r"""交付前扫描器：Å 误包（mathring）/「mathtyping」字面 / Δ 噪声。

背景（2026-10-13 卷 XVII 实测）：
  `\mathring{A}`（Å）被误包进 `\mathrm{}`（如 `\mathrm { ~ \mathrm{mathring A} ~ }`）
  ⇒ 交付 docx **渲染为字面「mathtyping A」**。
  机器闸门（qa_volX2 / qa_vol_deliver / table_wrap）**均看不见** ⇒ 需本专用扫描器。

用法：
  python scan_mathring.py                    # 扫全部卷 md（04-题库/初赛模拟卷*.md）＋ 交付 docx
  python scan_mathring.py --vol XVII         # 只扫指定卷
  python scan_mathring.py --md-only          # 只扫卷 md
  python scan_mathring.py --docs-only        # 只扫交付 docx
  python scan_mathring.py --quiet            # 只输出汇总（供闸门串联）

退出码：0 = 干净；1 = 有命中（可作交付前闸门）。
判据：
  H1 🔴 md   `\mathrm{…\mathring…}`（Å 被误包 ⇒ 必印 mathtyping）
  H2 🟠 md   `\mathrm{…\Delta…}`（Δ 噪声候选；`\xrightarrow[…\Delta…]` 与 `\Delta_`/`\Delta^` 为正当用法，本工具自动排除）
  H3 🔴 md   字面 `mathtyping`
  H4 🔴 docx 可见文本含 `mathtyping` / `mathring`
"""
import os, re, sys, glob, zipfile, io

ROOT = r"C:\Obsidion\妙妙屋"
MD_GLOB = os.path.join(ROOT, '04-题库', '初赛模拟卷*.md')
DOCX_DIR = os.path.join(ROOT, '00-首页', '题组Word', '初赛模拟卷', '真题版式')

VOL = None
for i, a in enumerate(sys.argv):
    if a == '--vol' and i + 1 < len(sys.argv):
        VOL = sys.argv[i + 1]
MD_ONLY = '--md-only' in sys.argv
DOCS_ONLY = '--docs-only' in sys.argv
QUIET = '--quiet' in sys.argv

# 需修判据（允许一层嵌套花括号，如 `C_ {2}`）
NEST = r'(?:[^{}]*(?:\{[^{}]*\}[^{}]*)*?)'
D1 = re.compile(r'\\mathrm\s*\{' + NEST + r'\\mathring' + NEST + r'\}')
D2 = re.compile(r'\\mathrm\s*\{' + NEST + r'\\Delta' + NEST + r'\}')
XARR = re.compile(r'\\x?rightarrow\s*\[[^\]]*\\Delta')
DELTA_SUB = re.compile(r'\\Delta\s*[_^]')          # \Delta_r G / \Delta H_ —— 正当符号
LIT = re.compile(r'mathtyping')

hits = []          # (级别, 文件, 类型, 片段)


def scan_md():
    paths = sorted(glob.glob(MD_GLOB))
    if VOL:
        paths = [p for p in paths if ('卷%s' % VOL) in os.path.basename(p)]
    for p in paths:
        try:
            t = io.open(p, encoding='utf-8-sig').read()
        except Exception:
            continue
        rel = p.replace(os.sep, '/')
        for m in LIT.finditer(t):
            hits.append(('🔴', rel, 'H3 字面 mathtyping', t[max(0, m.start() - 40):m.start() + 30]))
        for m in D1.finditer(t):
            hits.append(('🔴', rel, 'H1 Å 被误包', m.group(0)[:80]))
        for m in D2.finditer(t):
            seg = m.group(0)
            if XARR.search(seg) or DELTA_SUB.search(seg):
                hits.append(('🟠', rel, 'H2 Δ 候选(可能正当·需人判)', seg[:80]))
            else:
                hits.append(('🟠', rel, 'H2 Δ 噪声', seg[:80]))
    return paths


def scan_docs():
    out = []
    for p in sorted(glob.glob(os.path.join(DOCX_DIR, '*.docx'))):
        if VOL and ('卷%s' % VOL) not in os.path.basename(p):
            continue
        try:
            x = zipfile.ZipFile(p).read('word/document.xml').decode('utf-8')
        except Exception:
            continue
        txt = ''.join(re.findall(r'<(?:w|m):t[^>]*>([^<]*)</(?:w|m):t>', x))
        rel = p.replace(os.sep, '/')
        for kw in ('mathtyping', 'mathring'):
            if kw in txt:
                i = txt.index(kw)
                hits.append(('🔴', rel, 'H4 docx 含 %s' % kw, txt[max(0, i - 40):i + 30]))
        out.append(p)
    return out


nm = nd = 0
if not DOCS_ONLY:
    nm = len(scan_md())
if not MD_ONLY:
    nd = len(scan_docs())

red = [h for h in hits if h[0] == '🔴']
org = [h for h in hits if h[0] == '🟠']

if not QUIET:
    print('=' * 92)
    print('mathring / mathtyping / Δ 噪声 交付前扫描')
    print('  扫卷 md %d 份 ｜ 交付 docx %d 份%s' % (nm, nd, ('｜限定卷 %s' % VOL) if VOL else ''))
    print('-' * 92)
    for lv, f, kind, seg in hits[:40]:
        print('%s %-24s %-30s %s' % (lv, os.path.basename(f)[:24], kind, seg.replace('\n', '⏎')[:70]))
    if len(hits) > 40:
        print('  …（共 %d 条，仅列前 40）' % len(hits))
    print('-' * 92)

print('结果：🔴 必修 %d ｜ 🟠 待判 %d ｜ 合计 %d' % (len(red), len(org), len(hits)))
print('VERDICT:', 'FAIL' if red else ('WARN' if org else 'PASS'))
sys.exit(1 if red else 0)
