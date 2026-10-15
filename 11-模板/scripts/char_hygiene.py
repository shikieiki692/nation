#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""全库字符卫生普查（只读）——「坏区穷尽 ＋ 类别穷尽」双维一次扫。

口径来源：`00-首页/活跃任务/【直接复制】新会话提示词-2026-10-15-全库字符卫生普查线.md`
与 `09-审计报告/2026-10-14-chemy-P3旧卡归属错位评估.md` §8.8。

🔴🔴 铁律（本线口径教训）：**「全库」结论必须写明扫描类目与目录范围**。
   本脚本把两者都显式打印，并区分「真内容域」与「源材料域」（源材料域＝原始 OCR/教材导入，
   乱码属其固有属性，不计入判定）。

用法
----
    python char_hygiene.py --all                     # 04-题库 全域（题库线默认扫描面）
    python char_hygiene.py --domain 04-课件 03-知识点   # 指定若干目录
    python char_hygiene.py --changed <f1> <f2>       # 增量（本次改动文件）
    python char_hygiene.py --vault                   # 全 vault，按 真内容/源材料 分层
    python char_hygiene.py --cat fffd,pua,kangxi     # 只看指定类目
    python char_hygiene.py --detail                  # 附每处上下文
    python char_hygiene.py --report <out.md>         # 落报告（自带 FM，可 --report 到 09-审计报告）
    python char_hygiene.py --all -q                  # 只打印判定类目非零的行

退出码：0 = 无「判定类目」命中；1 = 有；2 = 参数错误。

类目分两档：
  · JUDGE    —— 判定为缺陷（命中即退出码 1）
  · ADVISORY —— 参考档（已知含大量合法用法：℃，x̄，全角标点，emoji 变体选择符…）
"""
import argparse
import collections
import datetime as _dt
import io
import os
import re
import sys
import unicodedata

sys.stdout.reconfigure(encoding="utf-8")

VAULT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ---- 目录分层（口径同 11-模板/scripts/metadata_audit.py）----
SKIP_DIRS = {'.git', '.workbuddy', '.claude', 'node_modules', 'images', 'media', '__pycache__',
             '_归档', '_archive', '归档'}
# 源材料域：原始 OCR / 教材导入，乱码属固有属性，不计入判定
RAW_TOP = {'06-外部资料导入', '2026机构初赛模拟题', '2026其他资料', 'chemy试题', 'mineru',
           'mineru02', 'bdwp资源', 'clayden 有机化学', '中级无机化学', '人教版初中化学教材',
           '北斗40套', '各省预赛题目', '媒体仓库', '无机化学 习题集', '物理化学上下册',
           '结构化学习题与解析', '高中化学竞赛笔记', '高考化学', 'MATHEMATICS', '37决', '40届初赛',
           '重新ocr', 'scratch', '北斗40'}

# ---- 类目定义 ----
CATS = collections.OrderedDict([
    # —— JUDGE ——
    ('fffd',     (re.compile(r'[\uFFFD]'), 'U+FFFD 替换字符')),
    ('pua',      (re.compile(r'[\uE000-\uF8FF]'), 'PUA 私用区 U+E000–F8FF')),
    ('pua_supp', (re.compile(r'[\U000F0000-\U000FFFFD\U00100000-\U0010FFFD]'), '补充 PUA')),
    ('kangxi',   (re.compile(r'[\u2E80-\u2EFF\u2F00-\u2FDF]'), '康熙部首 / CJK 部首补充')),
    ('mathalnum', (re.compile(r'[\U0001D400-\U0001D7FF\U0001DEE0-\U0001DFFF]'), 'Unicode 数学字母')),
    ('indic',    (re.compile(r'[\u0900-\u097F\u0980-\u09FF\u0A00-\u0A7F\u0A80-\u0AFF\u0B00-\u0B7F'
                             r'\u0B80-\u0BFF\u0C00-\u0C7F\u0C80-\u0CFF\u0D00-\u0D7F\u0D80-\u0DFF]'),
                  '印度语系（ToUnicode 缺失假字符）')),
    ('cyrillic', (re.compile(r'[\u0400-\u04FF\u0500-\u052F]'), '西里尔字母（常为形近字母）')),
    ('otherscript', (re.compile(r'[\u0530-\u058F\u0590-\u05FF\u0600-\u06FF\u0700-\u074F\u0E00-\u0E7F'
                                r'\u0E80-\u0EFF\u0F00-\u0FFF\u1000-\u109F\u10A0-\u10FF\u1200-\u137F'
                                r'\u13A0-\u13FF\u1780-\u17FF\u1800-\u18AF\u1A00-\u1AAF\u1B00-\u1B7F]'),
                    '其他语系（阿拉伯/希伯来/泰/藏/缅/高棉…）')),
    ('u212b',    (re.compile(r'[\u212B]'), '非规范埃符号 U+212B（应 U+00C5）')),
    ('ctrl',     (re.compile(r'[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]'), 'C0/C1 控制字符')),
    ('nonchar',  (re.compile(r'[\uFDD0-\uFDEF\uFFFE\uFFFF]'), 'Unicode 非字符')),
    ('cjk_stroke', (re.compile(r'[\u31C0-\u31EF]'), 'CJK 笔画 U+31C0–31EF')),
    ('kana',     (re.compile(r'[\u3040-\u309F\u30A0-\u30FF]'), '日文假名（引用合法 / OCR 噪声需甄别）')),
    ('mojibake', (re.compile(r'(?!x)x'), 'GBK/UTF-8 编码层 mojibake（行级判据：标记字 ≥3）')),
    # —— ADVISORY ——
    ('cjk_comp', (re.compile(r'[\uF900-\uFAFF]'), 'CJK 兼容表意（已实证 0 处）')),
    ('greek',    (re.compile(r'[\u0370-\u03FF\u1F00-\u1FFF]'), '希腊字母（化学用量，合法）')),
    ('vs',       (re.compile(r'[\uFE00-\uFE0F]'), '变体选择符（emoji 呈现，合法）')),
    ('shy',      (re.compile(r'[\u00AD]'), '软连字符 U+00AD')),
    ('nbsp',     (re.compile(r'[\u00A0]'), 'NBSP U+00A0')),
    ('linesep',  (re.compile(r'[\u2028\u2029]'), '行/段分隔 U+2028/29')),
    ('zw',       (re.compile(r'[\u200B-\u200F\u202A-\u202E\u2060-\u2064\uFEFF]'), '零宽/方向控制/BOM')),
    ('letterlike', (re.compile(r'[\u2100-\u214F]'), 'Letterlike（℃/ℓ/ℎ 合法）')),
    ('combining', (re.compile(r'[\u0300-\u036F]'), '组合附加符（x̄/X̄ₙ/ν̃ 合法）')),
    ('fullwidth', (re.compile(r'[\uFF00-\uFFEF]'), '全角形式（中文标点合法）')),
    ('present_form', (re.compile(r'[\uFB00-\uFB4F\uFE30-\uFE4F\uFE50-\uFE6F\uFE70-\uFEFF]'),
                      '呈现形式/连字')),
    ('u00c5cmp', (re.compile(r'[\u00C5]'), 'Å U+00C5（规范写法，参考）')),
])
def _build_moji_set():
    """从固定常用字集构造「GBK mojibake 标记字」集。
    原理：把常用汉字逐字做 c.encode('utf-8').decode('gb18030')，得到 UTF-8 串被按
    GB18030 解码后出现的字形；剔除本身即常用字者，余下即高信号标记字。
    判据（行级）：一行内标记字 >= 3 即判 mojibake（实测：已知真阳性 9 字，全库假阳性 0）。
    """
    base = ('的一是了我不人在他有这上们来到时大地为子中你说生国年就那和要出也得里后自以会家可下过天去能对小多然于心学么之都看好起发当没成只如事把还用第样道想作种开美总从无情己面最女但现前些所同日手又行意动方期它头经长儿回位分爱老因很给名法间知世什两次使身者被高已亲其进此话常与活正感'
            '化反温压溶液电分原键能结元构析计算量值图表明含量质数式应平衡速催剂储物质能量')
    m = set()
    for c in set(base):
        for ch in c.encode('utf-8').decode('gb18030', 'ignore'):
            if ch not in base:
                m.add(ch)
    return m


MOJI_SET = _build_moji_set()
JUDGE = ['fffd', 'pua', 'pua_supp', 'kangxi', 'mathalnum', 'indic', 'cyrillic', 'otherscript',
         'u212b', 'ctrl', 'nonchar', 'cjk_stroke', 'kana', 'mojibake']


def iter_md(root):
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d not in SKIP_DIRS]
        for fn in fns:
            if fn.endswith('.md'):
                yield os.path.join(dp, fn)


def is_raw(rel):
    return rel.split('/')[0] in RAW_TOP


def top_of(rel):
    return rel.split('/')[0]


def main():
    ap = argparse.ArgumentParser(description='全库字符卫生普查（只读）')
    ap.add_argument('--all', action='store_true', help='扫 04-题库 全域')
    ap.add_argument('--vault', action='store_true', help='扫全 vault（按 真内容/源材料 分层）')
    ap.add_argument('--domain', nargs='*', default=None, help='指定目录（相对 vault）')
    ap.add_argument('--changed', nargs='*', default=None, help='只扫指定文件')
    ap.add_argument('--cat', default=None, help='逗号分隔类目名')
    ap.add_argument('--detail', action='store_true')
    ap.add_argument('--report', default=None)
    ap.add_argument('-q', '--quiet', action='store_true')
    args = ap.parse_args()

    cats = list(CATS.keys())
    if args.cat:
        cats = [c.strip() for c in args.cat.split(',') if c.strip() in CATS]
    if args.changed:
        files = [f if os.path.isabs(f) else os.path.join(VAULT, f) for f in args.changed]
        scope_desc = '--changed %d 个文件' % len(files)
    elif args.domain:
        files = []
        for d in args.domain:
            files += list(iter_md(os.path.join(VAULT, d)))
        scope_desc = '目录 %s' % ','.join(args.domain)
    elif args.vault:
        files = list(iter_md(VAULT))
        scope_desc = '全 vault'
    else:
        files = list(iter_md(os.path.join(VAULT, '04-题库')))
        scope_desc = '04-题库'

    cat_files = collections.Counter(); cat_occ = collections.Counter()
    grp_occ = collections.defaultdict(collections.Counter)
    grp_files = collections.defaultdict(collections.Counter)
    rows = []
    for p in files:
        try:
            t = io.open(p, encoding='utf-8-sig').read()
        except Exception as e:
            print('  ! 读取失败 %s: %s' % (p, e)); continue
        rel = os.path.relpath(p, VAULT).replace('\\', '/')
        grp = '源材料' if is_raw(rel) else '真内容'
        hits = {}
        for c in cats:
            if c == 'mojibake':
                for line in t.split('\n'):
                    n = sum(1 for ch in line if ch in MOJI_SET)
                    if n >= 3:
                        hits['mojibake'] = [(n, line.strip()[:70])]
                        break
                continue
            f = [(m.start(), m.group(0)) for m in CATS[c][0].finditer(t)]
            if f:
                hits[c] = f
        if not hits:
            continue
        for c, lst in hits.items():
            cat_files[c] += 1; cat_occ[c] += len(lst)
            grp_occ[grp][c] += len(lst); grp_files[grp][c] += 1
        rows.append((rel, grp, hits))

    out = []
    def P(s=''):
        out.append(s); print(s)

    P('=' * 78)
    P('字符卫生普查（只读）  扫描面 = %s  文件 %d  命中 %d' % (scope_desc, len(files), len(rows)))
    P('类目数 = %d（JUDGE %d / ADVISORY %d）' % (len(cats), len([c for c in cats if c in JUDGE]),
                                              len([c for c in cats if c not in JUDGE])))
    P('-' * 78)
    P('%-13s %7s %8s  %s' % ('类目', '文件', '处数', '说明'))
    judge_hit = False
    for c in cats:
        if not cat_occ[c]:
            continue
        tagc = 'J' if c in JUDGE else '-'
        if not (args.quiet and c not in JUDGE):
            P('[%s] %-10s %7d %8d  %s' % (tagc, c, cat_files[c], cat_occ[c], CATS[c][1]))
        if c in JUDGE:
            judge_hit = True
    if not judge_hit:
        P('✅ JUDGE 类目全 0')
    else:
        P('⚠️  JUDGE 类目命中：%s' % ', '.join('%s=%d' % (k, cat_occ[k]) for k in JUDGE if cat_occ[k]))
    if len(grp_occ) > 1 or '源材料' in grp_occ:
        P('-' * 78)
        for g in ('真内容', '源材料'):
            if grp_occ[g]:
                P('  【%s】%s' % (g, ', '.join('%s=%d' % (k, v) for k, v in grp_occ[g].most_common())))

    if args.detail and rows:
        P('=' * 78)
        for rel, grp, hits in rows:
            P('[%s|%s] %s' % (grp, top_of(rel), rel))
            t = io.open(os.path.join(VAULT, rel), encoding='utf-8-sig').read()
            for c, lst in hits.items():
                for pos, ch in lst[:40]:
                    if c == 'mojibake':
                        P('   %-11s 标记字 %d 处，所在行：%s' % (c, pos, ch))
                        continue
                    ctx = t[max(0, pos - 25):pos + 25].replace('\n', '⏎')
                    P('   %-11s U+%04X %r  …%s…' % (c, ord(ch), ch, ctx))

    if args.report:
        fm = ('---\ntitle: "%s"\ntype: 审计报告\ndate: %s\ntags: [化竞, 字符卫生, Unicode, 普查]\n---\n\n'
              % ('字符卫生普查-' + _dt.date.today().isoformat(), _dt.date.today().isoformat()))
        io.open(args.report, 'w', encoding='utf-8', newline='').write(fm + '\n'.join(out) + '\n')
        print('\n报告已落: %s' % args.report)

    return 1 if judge_hit else 0


if __name__ == '__main__':
    sys.exit(main())
