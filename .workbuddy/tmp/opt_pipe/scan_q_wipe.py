# -*- coding: utf-8 -*-
"""扫描「题面被清洗链路吞掉内容」的卡。

比对：原始题面区（## 题目 .. ## 参考答案）
  vs 清洗后题面 q = html_table_to_md(conv_imgs(clean_q(extract)))

关注两类：
  A. 图片被吞：原文题面区有 ![[..]] 或 ![..](..)，清洗后 q 里图数明显减少；
  B. 文字大幅缩水：清洗后非空白字数 < 原文非空白字数 * 0.55（且原文 >= 120 字）。
"""
import glob, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.workbuddy/tmp/opt_pipe')
sys.argv = ['x', '--vol', 'SQ', '--all-years']
import build_org as BO

ROOT = r'C:\Obsidion\妙妙屋'


def nws(s):
    return re.sub(r'\s+', '', s)


def count_imgs(s):
    return len(re.findall(r'!\[\[[^\]]*\]\]|!\[[^\]]*\]\([^)]*\)', s))


def main():
    cards = glob.glob('04-题库/2026机构初赛模拟题/**/题-*.md', recursive=True)
    img_lost, txt_lost = [], []
    for p in cards:
        try:
            t = open(p, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n')
        except Exception:
            continue
        i = t.find('## 题目'); j = t.find('## 参考答案')
        if i < 0 or j < 0 or j <= i:
            continue
        qraw = t[i + len('## 题目'):j]
        try:
            c = BO.X.extract(p)
            q = BO.html_table_to_md(BO.conv_imgs(BO.clean_q(c['question'])))
        except Exception as e:
            txt_lost.append((p, 'EXTRACT_ERR:' + str(e)[:40], 0, 0, 0, 0))
            continue
        n_raw, n_cl = count_imgs(qraw), count_imgs(q)
        w_raw, w_cl = len(nws(qraw)), len(nws(q))
        # A. 图被吞（原文有图，清洗后少了一半以上）
        if n_raw > 0 and n_cl < n_raw:
            img_lost.append((p, n_raw, n_cl, w_raw, w_cl))
        # B. 文字大幅缩水
        if w_raw >= 120 and w_cl < w_raw * 0.55:
            txt_lost.append((p, 'TXT', n_raw, n_cl, w_raw, w_cl))

    print('扫描 %d 卡' % len(cards))
    print()
    print('=== A. 题面图片被吞（原 %d 处，去重后 %d 张卡）===' % (0, len(img_lost)))
    for r in sorted(img_lost, key=lambda x: -(x[1] - x[2]))[:40]:
        print('  图 %2d→%2d | 字 %5d→%5d | %s' % (r[1], r[2], r[3], r[4], os.path.basename(r[0])[:56]))
    print()
    print('=== B. 题面文字缩水 >45%%（%d 张）===' % len(txt_lost))
    for r in sorted(txt_lost, key=lambda x: x[4] - x[5])[:40]:
        print('  字 %5d→%5d (%.0f%%) | 图 %d→%d | %s' % (
            r[4], r[5], 100.0 * r[5] / max(1, r[4]), r[2], r[3], os.path.basename(r[0])[:52]))


main()
