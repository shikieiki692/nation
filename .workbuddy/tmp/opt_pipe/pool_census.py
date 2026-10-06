# -*- coding: utf-8 -*-
"""pool_census.py —— 机构模拟题「可用池」详查（两种年份口径 × 逐步漏斗 × 分模块）。

口径与 build_org.build_pool() 完全一致，仅额外做分模块统计与「扣除既往各卷已用卡」。
用法: python -X utf8 pool_census.py
"""
import os
import re
import sys
import glob
import json
import collections

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import build_org as O          # noqa: E402
import build_multi as B        # noqa: E402
import mv_extract as X         # noqa: E402

BASE = O.BASE


def g(t, k):
    m = re.search(r'^' + k + r':\s*(.*)$', t, re.M)
    return m.group(1).strip() if m else ''


def funnel(use_all_years):
    """返回 (步计数列表, 最终 per-module Counter)。"""
    cards = []
    for rel in O.SRCS:
        cards += sorted(glob.glob(os.path.join(BASE, rel, '**', '题-*.md'), recursive=True))
    steps = [('⓪ 全部卡', len(cards))]
    modc = collections.Counter()
    texts = {p: open(p, encoding='utf-8-sig').read() for p in cards}

    # ① 年份
    keep = [p for p in cards if use_all_years
            or O.in_2526(g(texts[p], 'source_norm'), g(texts[p], 'source_file'))]
    steps.append(('① 年份闸', len(keep)))
    # ② 讲稿
    keep = [p for p in keep if not O.BATCH_BAD.search(g(texts[p], 'source_norm'))]
    steps.append(('② 非「讲稿」', len(keep)))
    # ③ 三模块 且 非省预赛
    keep = [p for p in keep if g(texts[p], 'subject_module') in ('元素与分析', '结构化学', '化学原理')
            and g(texts[p], 'exam_stage') != '省预赛']
    steps.append(('③ 三模块·非省预赛', len(keep)))
    # ④ diff≥4 且 无 RISK
    keep = [p for p in keep if int(g(texts[p], 'difficulty') or 0) >= 4
            and not [x for x in B.RISK if x in texts[p]]]
    steps.append(('④ difficulty≥4·无RISK词', len(keep)))
    # ⑤ 非国内初赛真题
    keep = [p for p in keep if not B.is_cn_prelim(re.sub(r'<!--.*?-->', '', texts[p], flags=re.S))]
    steps.append(('⑤ 非国内初赛真题', len(keep)))
    # ⑥ 非有机章
    def h1of(t):
        m = re.search(r'^#\s+(.+)$', t, re.M)
        return m.group(1) if m else ''
    keep = [p for p in keep if not B.ORG_CHAP.search(g(texts[p], 'source')) and not B.ORG_CHAP.search(h1of(texts[p]))]
    steps.append(('⑥ 非有机章', len(keep)))
    # ⑦ 内容闸（extract 起）
    ex = ph = fake = form = leakq = short = org = num = 0
    for p in keep:
        t = texts[p]
        try:
            c = X.extract(p)
        except Exception:
            ex += 1; continue
        rawq, rawa = c['question'], c['answer']
        if O.PLACEHOLDER.search(rawa) or O.PLACEHOLDER.search(rawq): ph += 1; continue
        if O.has_fake_struct(rawa) or O.has_fake_struct(rawq): fake += 1; continue
        if len(rawa) >= 400 and rawa.count('$') == 0 and rawq.count('$') >= 10: form += 1; continue
        q0 = O.conv_imgs(O.clean_q(rawq)); a0 = O.clean_a(O.conv_imgs(rawa), q0)
        q, a = O.html_table_to_md(q0), O.html_table_to_md(a0)
        if O.LEAK.search(q): leakq += 1; continue
        qn = re.sub(r'\s+', '', q); an = re.sub(r'\s+', '', a)
        if len(qn) < 60 or len(an) < 25: short += 1; continue
        if len(B.ORGRE.findall(q + ' ' + a)) >= 3: org += 1; continue
        if len(re.findall(r'^\*\*\s*\d{1,2}\s*[.．]\s*\*\*', q + '\n' + a, re.M)) >= 8: num += 1; continue
        modc[g(t, 'subject_module')] += 1
    steps.append(('⑦ 内容闸(extract/占位/假式/公式/泄露/过短/有机/编号)', sum(modc.values())))
    detail = {'extract失败': ex, '占位语': ph, '假结构式': fake, '公式未转录': form, '题面泄露': leakq,
              '过短': short, '有机词>=3': org, '编号式答案>=8': num}
    return steps, modc, detail


def main():
    print('=' * 92)
    print('机构模拟题 可用池普查（%，2026-10-06）')
    for label, flag in (('A. 默认（年份＝硬闸，产出卷X 的口径）', False),
                        ('B. --all-years（年份＝排序偏好）', True)):
        steps, modc, detail = funnel(flag)
        print('\n【%s】' % label)
        for name, v in steps:
            print('   %-42s %5d' % (name, v))
        print('   内容闸细分:', detail)
        print('   ★ 可用池：元素与分析 %d / 结构化学 %d / 化学原理 %d ＝ 合计 %d'
              % (modc['元素与分析'], modc['结构化学'], modc['化学原理'], sum(modc.values())))

    # 既往各卷已用卡
    used = set()
    for pf in sorted(glob.glob(os.path.join(HERE, 'vol_plan_*.json'))):
        for _m, lst in json.load(open(pf, encoding='utf-8')):
            for c in lst:
                used.add(c['path'].replace('\\', '/'))
    print('\n既往各卷已用卡：%d 张' % len(used))

    # 逐卷消耗估算（QUOTA 7/5/4）
    steps, modc, _ = funnel(True)
    n_el, n_st, n_pr = modc['元素与分析'], modc['结构化学'], modc['化学原理']
    print('\n【按 --all-years 池估算可出卷数（QUOTA 元素7/结构5/原理4）】')
    print('   不扣既往：元素可支撑 %d 卷、结构 %d 卷、原理 %d 卷 ⇒ 受元素限制 ≈ %d 卷'
          % (n_el // 7, n_st // 5, n_pr // 4, min(n_el // 7, n_st // 5, n_pr // 4)))
    print('   扣卷X(7/5/4) 后：元素 %d、结构 %d、原理 %d ⇒ 受元素限制 ≈ %d 卷'
          % ((n_el - 7) // 7, (n_st - 5) // 5, (n_pr - 4) // 4,
             min((n_el - 7) // 7, (n_st - 5) // 5, (n_pr - 4) // 4)))


if __name__ == '__main__':
    main()
