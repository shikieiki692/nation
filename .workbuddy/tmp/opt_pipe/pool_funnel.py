# -*- coding: utf-8 -*-
"""pool_funnel.py —— 复现 build_org 的选卡过滤漏斗，回答「4032 张怎么会缺」。

输出：① 全库 4032 卡 按 模块/时序/难度 的分布（未过滤）② 逐条过滤器剩余量。
"""
import os
import re
import sys
import glob
import collections

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import build_org as O          # noqa: E402
import build_multi as B        # noqa: E402
import mv_extract as X         # noqa: E402

BASE = O.BASE
SRCS = O.SRCS


def g(t, k):
    m = re.search(r'^' + k + r':\s*(.*)$', t, re.M)
    return m.group(1).strip() if m else ''


def main():
    cards = []
    for rel in SRCS:
        cards += sorted(glob.glob(os.path.join(BASE, rel, '**', '题-*.md'), recursive=True))
    print('★ 全库机构题卡（13 机构）:', len(cards))

    def dist(keyf, title):
        c = collections.Counter(keyf(p) for p in cards)
        print('  ──', title)
        for k, v in c.most_common():
            print('     %-14s %5d' % (k, v))

    texts = {p: open(p, encoding='utf-8-sig').read() for p in cards}
    dist(lambda p: g(texts[p], 'subject_module') or '(空)', '按 subject_module')
    dist(lambda p: '省预赛' if g(texts[p], 'exam_stage') == '省预赛' else '非省预赛', '按 exam_stage')
    dist(lambda p: g(texts[p], 'difficulty') or '0', '按 difficulty')
    dist(lambda p: '2025~26' if O.in_2526(g(texts[p], 'source_norm'), g(texts[p], 'source_file')) else '更早',
         '按 2025~2026（in_2526）')

    # 逐过滤器
    steps = [('全部卡', lambda t, p: True),
             ('① in_2526（2025~26）', lambda t, p: O.in_2526(g(t, 'source_norm'), g(t, 'source_file'))),
             ('② 非「讲稿」批次', lambda t, p: not O.BATCH_BAD.search(g(t, 'source_norm'))),
             ('③ 模块∈{元素/结构/原理} 且 非省预赛',
              lambda t, p: g(t, 'subject_module') in ('元素与分析', '结构化学', '化学原理') and g(t, 'exam_stage') != '省预赛'),
             ('④ difficulty≥4 且 无 RISK 词', lambda t, p: int(g(t, 'difficulty') or 0) >= 4 and not [x for x in B.RISK if x in t]),
             ]
    keep = cards[:]
    print('\n★ 过滤漏斗（累计）')
    n0 = len(keep)
    for name, fn in steps[1:]:
        keep = [p for p in keep if fn(texts[p], p)]
        print('  %-34s 剩 %5d' % (name, len(keep)))
    # ⑤ 后续需要 extract，逐个走完（保持顺序）
    rest = [('⑤ 非国内初赛真题 is_cn_prelim', lambda t, p: not B.is_cn_prelim(re.sub(r'<!--.*?-->', '', t, flags=re.S))),
            ('⑥ 非有机章 ORG_CHAP', lambda t, p: not B.ORG_CHAP.search(g(t, 'source')) and
                                          not B.ORG_CHAP.search((re.search(r'^#\s+(.+)$', t, re.M) or [None, ''])[1] if re.search(r'^#\s+(.+)$', t, re.M) else '')),
            ]
    for name, fn in rest:
        keep = [p for p in keep if fn(texts[p], p)]
        print('  %-34s 剩 %5d' % (name, len(keep)))
    # ⑦ extract + 内容闸
    ph = 0; fake = 0; form = 0; leakq = 0; org = 0; num = 0; short = 0; ok = 0; exfail = 0
    mod_ok = collections.Counter()
    for p in keep:
        t = texts[p]
        try:
            c = X.extract(p)
        except Exception:
            exfail += 1; continue
        rawq, rawa = c['question'], c['answer']
        if O.PLACEHOLDER.search(rawa) or O.PLACEHOLDER.search(rawq):
            ph += 1; continue
        if O.has_fake_struct(rawa) or O.has_fake_struct(rawq):
            fake += 1; continue
        if len(rawa) >= 400 and rawa.count('$') == 0 and rawq.count('$') >= 10:
            form += 1; continue
        q0 = O.conv_imgs(O.clean_q(rawq)); a0 = O.clean_a(O.conv_imgs(rawa), q0)
        q, a = O.html_table_to_md(q0), O.html_table_to_md(a0)
        if O.LEAK.search(q):
            leakq += 1; continue
        qn = re.sub(r'\s+', '', q); an = re.sub(r'\s+', '', a)
        if len(qn) < 60 or len(an) < 25:
            short += 1; continue
        if len(B.ORGRE.findall(q + ' ' + a)) >= 3:
            org += 1; continue
        if len(re.findall(r'^\*\*\s*\d{1,2}\s*[.．]\s*\*\*', q + '\n' + a, re.M)) >= 8:
            num += 1; continue
        ok += 1; mod_ok[g(t, 'subject_module')] += 1
    print('  %-34s 剔除 %d' % ('⑦ extract 失败', exfail))
    print('  %-34s 剔除 %d' % ('⑧ 占位语闸', ph))
    print('  %-34s 剔除 %d' % ('⑨ 假结构式闸', fake))
    print('  %-34s 剔除 %d' % ('⑩ 公式未转录闸', form))
    print('  %-34s 剔除 %d' % ('⑪ 题面泄露闸', leakq))
    print('  %-34s 剔除 %d' % ('⑫ 过短闸', short))
    print('  %-34s 剔除 %d' % ('⑬ 有机词≥3', org))
    print('  %-34s 剔除 %d' % ('⑭ 编号式答案≥8', num))
    print('  ★ 最终可用池：', ok, dict(mod_ok))


if __name__ == '__main__':
    main()
