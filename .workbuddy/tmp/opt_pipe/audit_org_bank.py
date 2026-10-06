# -*- coding: utf-8 -*-
"""audit_org_bank.py —— 机构模拟题题库全量体检（04-题库/2026机构初赛模拟题/，4032 卡）。

维度：FM 合法性/必填/重复键 · 结构（题目/答案区）· 图片引用 vs 实际文件 · 占位语 ·
     假结构式 · 答案区越界 · 题目/答案过短 · 题面重复 · wikilink 断链 · 译名可疑。
输出：摘要 + `09-审计报告/2026-10-06-机构题库体检.csv`。
"""
import os
import re
import csv
import sys
import glob
import collections

ROOT = r"C:\Obsidion\妙妙屋"
BASE = os.path.join(ROOT, '04-题库', '2026机构初赛模拟题')
SRCS = ['化英社', '清北营', 'chemy', '伽马', '壹尖培优', '汇智', 'XeChem', '质心GChO',
        '质心UChO', '方圆', '一式', '北京夏令营', '2ChO']
OUTCSV = os.path.join(ROOT, '09-审计报告', '2026-10-06-机构题库体检.csv')
sys.stdout.reconfigure(encoding='utf-8')

PLACEHOLDER = re.compile(r'⛔|源池(无|仅|未见)|未录入|未定位|待人工核|文字化需人工转录|已随卡|源卷答案|答案出处[：:]|文字层自动提取|未逐字校对|答案（源 ?PDF')
ARR_FAKE = re.compile(r'\\begin\{array\}(?:\{[^}]*\})?(.*?)\\end\{array\}', re.S)
WM_TEXT = re.compile(r'^(清北营教育|清北教育|清北营|化英社|北斗学友|致学教育|教育|ZCHEM|ZChem)\s*$')
# ── 译名可疑：罕用字/同音形近误替 ──
NAME_SUSPECT = [
    (re.compile(r'轮牌|元素轮|轮同位素|铊的同位素|铊牌|元素铊'), 'Rg(錀) 疑误作 轮/铊'),
    (re.compile(r'氪氙|氙氙|分子氙'), 'N(氮) 疑误作 氙'),
]
TITLE_ERR = re.compile(r'^#{2,4}[ \t]*第[ \t]*\d+[ \t]*题')


def has_fake(a):
    for body in ARR_FAKE.findall(a):
        for l in [x.strip() for x in re.split(r'(?<!\\)\\\\', body) if x.strip()]:
            if re.fullmatch(r'[|/]+', l):
                return True
            if re.match(r'^[|/]', l) and len(l) < 60:
                return True
            if re.search(r'[|/]$', l) and len(l) < 60 and re.search(r'[\u4e00-\u9fffA-Za-z]', l):
                return True
    return False


def fm_fields(t):
    m = re.match(r'^---[ \t]*\n(.*?)\n---[ \t]*\n', t, re.S)
    return m.group(1) if m else None


def main():
    cards = []
    for rel in SRCS:
        cards += sorted(glob.glob(os.path.join(BASE, rel, '**', '题-*.md'), recursive=True))
    print('★ 卡总数：', len(cards))

    # 全库 md 索引（供 wikilink 断链检查）
    md_index = set()
    for dp, _, fs in os.walk(ROOT):
        if os.sep + '.git' in dp:
            continue
        for f in fs:
            if f.endswith('.md'):
                md_index.add(f[:-3])
    print('  全库 md 索引：', len(md_index))

    issues = []
    exp = collections.Counter()
    fps = collections.defaultdict(list)
    img_ref_total = 0
    img_missing = 0

    # 每个机构 images/ 的文件集合
    img_idx = collections.defaultdict(set)
    for rel in SRCS:
        for p in glob.glob(os.path.join(BASE, rel, 'images', '*')):
            img_idx[rel].add(os.path.basename(p))

    for p in cards:
        rel = os.path.relpath(p, BASE).split(os.sep)[0]
        name = os.path.basename(p)
        raw = open(p, 'rb').read()
        crlf = b'\r\n' in raw
        t = raw.decode('utf-8-sig').replace('\r\n', '\n')
        rows = []
        if crlf:
            rows.append(('行尾', 'CRLF（.gitattributes 定 eol=lf）')); exp['CRLF行尾'] += 1

        # 1 FM
        fm = fm_fields(t)
        if fm is None:
            rows.append(('FM', '缺 frontmatter')); exp['FM缺'] += 1
        else:
            # 重复键
            keys = re.findall(r'(?m)^([A-Za-z_][\w]*):', fm)
            dup = [k for k, v in collections.Counter(keys).items() if v > 1]
            if dup:
                rows.append(('FM', '重复键 %s' % dup)); exp['FM重复键'] += 1
            for req in ('title', 'type', 'source_norm', 'source_file', 'subject_module', 'difficulty'):
                if not re.search(r'(?m)^' + req + r':', fm):
                    rows.append(('FM', '缺字段 %s' % req)); exp['FM缺字段'] += 1
            # 块列表必须 '- '
            for line in fm.split('\n'):
                if re.match(r'^\s*\[\[', line):
                    rows.append(('FM', '块列表缺 "- "：%s' % line.strip()[:30])); exp['FM块列表'] += 1
                    break

        # 2 结构（题面＝[## 题目, ## 参考答案)；答案＝[## 参考答案, ## 知识点映射)）
        iq = t.find('## 题目')
        ia = t.find('## 参考答案')
        if iq < 0:
            rows.append(('结构', '缺 ## 题目')); exp['缺题目区'] += 1
        if ia < 0:
            ia2 = t.find('## 答案')
            if ia2 < 0:
                rows.append(('结构', '缺 ## 参考答案')); exp['缺答案区'] += 1
            else:
                ia = ia2
        q = (t[iq:ia] if (iq >= 0 and ia > iq) else (t[iq:] if iq >= 0 else ''))
        if ia >= 0:
            e = t.find('\n## 知识点映射', ia)
            a = t[ia:(e if e > 0 else len(t))]
        else:
            a = ''
        qn = re.sub(r'\s+', '', re.sub(r'!\[\[?[^\]]*\]?\]', '', q))
        an = re.sub(r'\s+', '', re.sub(r'!\[\[?[^\]]*\]?\]', '', a))
        if iq >= 0 and len(qn) < 60:
            rows.append(('结构', ('题目空壳 %d' % len(qn)) if len(qn) < 12 else ('题目过短 %d' % len(qn))))
            exp['题目空壳' if len(qn) < 12 else '题目过短'] += 1
        if ia >= 0 and len(an) < 25:
            rows.append(('结构', ('答案空壳 %d' % len(an)) if len(an) < 12 else ('答案过短 %d' % len(an))))
            exp['答案空壳' if len(an) < 12 else '答案过短'] += 1

        # 3 图片
        refs = re.findall(r'!\[\[([^\]\|]+?)(?:\\?\|\d+)?\]\]', t) + \
               re.findall(r'!\[[^\]]*\]\(\s*images/([^)\s]+)\s*\)', t) + \
               re.findall(r'<img[^>]*src="images/([^"]+)"', t)
        for r in refs:
            r = r.strip()
            img_ref_total += 1
            if r not in img_idx[rel]:
                img_missing += 1
                rows.append(('图片', '缺文件 images/%s' % r)); exp['图片缺文件'] += 1

        # 4 占位语
        if PLACEHOLDER.search(a) or PLACEHOLDER.search(q):
            rows.append(('内容', '占位语')); exp['占位语'] += 1

        # 5 假结构式
        if has_fake(a) or has_fake(q):
            rows.append(('内容', '假结构式')); exp['假结构式'] += 1

        # 6 答案区越界（出现别题的小题号前缀）
        if ia >= 0:
            m = re.search(r'第\s*(\d+)\s*题', name)
            # 卡题号取自 header
            hm = re.search(r'(?m)^#{2,4}[ \t]*第\s*[0-9一二三四五六七八九十]+\s*题', t)
            # 越界判据：答案区出现「第 M 题」且 M 与题面首个「第 N 题」不同
            qids = [int(x) for x in re.findall(r'(?m)^#{2,4}[ \t]*第[ \t]*(\d+)[ \t]*题', q)]
            aids = [int(x) for x in re.findall(r'(?m)^#{2,4}[ \t]*第[ \t]*(\d+)[ \t]*题', a)]
            if aids and qids and any(x not in qids for x in aids):
                rows.append(('答案', '答案区标题题号异于题面 %s vs %s' % (aids[:3], qids[:3])))
                exp['答案区题号异'] += 1

        # 7 译名可疑
        for rx, msg in NAME_SUSPECT:
            if rx.search(t):
                rows.append(('译名', msg)); exp['译名可疑'] += 1
                break

        # 8 题面(源卡标题行)异常：H2-H4 级别「第N题」混进题面
        # 9 题面指纹（重复）
        fp = re.sub(r'\s+', '', re.sub(r'(?m)^#{2,4}.*$', '', q))[:150]
        if len(fp) >= 80:
            fps[fp].append(name)

        for cat, msg in rows:
            issues.append((rel, name, cat, msg))

    # wikilink 断链（只看指向 md/无扩展名的链接；图片嵌入由图存在性单独校验）
    IMGEXT = ('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.bmp')
    dead = 0
    for p in cards:
        t = open(p, encoding='utf-8-sig').read().replace('\r\n', '\n')
        for m in re.finditer(r'(?<!!)\[\[([^\]\|#]+?)(?:\|[^\]]*)?\]\]', t):
            tgt = m.group(1).strip().split('/')[-1]
            if tgt.lower().endswith(IMGEXT):
                continue
            if tgt.endswith('.md'):
                tgt = tgt[:-3]
            if tgt and tgt not in md_index:
                dead += 1
                issues.append((os.path.relpath(p, BASE).split(os.sep)[0], os.path.basename(p), '断链', tgt))
    exp['断链'] = dead

    dupgrp = {k: v for k, v in fps.items() if len(v) > 1}
    print('\n★ 体检结果')
    for k, v in exp.most_common():
        print('   %-14s %5d' % (k, v))
    print('   图引用总数 %d，其中缺文件 %d' % (img_ref_total, img_missing))
    print('   题面指纹重复组 %d（涉及 %d 卡）' % (len(dupgrp), sum(len(v) for v in dupgrp.values())))
    for k, v in list(dupgrp.items())[:25]:
        print('      ×%d  %s' % (len(v), ' / '.join(v[:4])))

    with open(OUTCSV, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow(['机构', '文件', '类别', '问题'])
        w.writerows(issues)
    print('\n明细已写：', OUTCSV, '（%d 条）' % len(issues))


if __name__ == '__main__':
    main()
