# -*- coding: utf-8 -*-
"""全链「内容保真筛」：

对每张入池卡，比对「源卡原文」与「最终清洗 q/a」，找**丢失的文本块**：
  - 题面：丢失块若落在**标题行**（题号+题名+分值，strip_src_heading 合法删）⇒ 合规；
          否则 ⇒ 可疑（清洗链吞了正文）。
  - 答案：丢失块若能在**题面**里找到（回显，strip_q_echo 合法删）⇒ 合规；
          否则 ⇒ 可疑。
同时统计图：题面图 / 答案图的丢失与去向。

用 10-gram（步长 5）做指纹，逐卡报告可疑丢失。
"""
import os, re, sys, glob, collections
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.workbuddy/tmp/opt_pipe')
sys.argv = ['x', '--vol', 'AUD', '--all-years']
import build_org as BO

ROOT = r'C:\Obsidion\妙妙屋'
N = 10
STEP = 5


def strip_md(s):
    s = re.sub(r'!\[\[[^\]]*\]\]', '', s)
    s = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', s)
    s = re.sub(r'<[^>]+>', '', s)
    s = re.sub(r'[#*`>_~\[\](){}|]', '', s)
    s = re.sub(r'\s+', '', s)
    return s


def ngrams(s, n=N, step=STEP):
    if len(s) < n:
        return set()
    return {s[i:i + n] for i in range(0, len(s) - n + 1, step)}


def images(s):
    return re.findall(r'!\[\[([^\]]+)\]\]|!\[[^\]]*\]\(([^)]+)\)', s)
    # returns tuples; flatten below


def imgset(s):
    out = []
    for a, b in re.findall(r'!\[\[([^\]]+)\]\]|!\[[^\]]*\]\(([^)]+)\)', s):
        out.append(os.path.basename(a or b))
    return set(out)


def main():
    cards = glob.glob('04-题库/2026机构初赛模拟题/**/题-*.md', recursive=True)
    sus_q, sus_a = [], []
    n_pool = 0
    for p in cards:
        try:
            t = open(p, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n')
        except Exception:
            continue
        i = t.find('## 题目'); j = t.find('## 参考答案'); k = t.find('## 知识点映射')
        if i < 0 or j < 0 or k < 0:
            continue
        rawq, rawa = t[i + len('## 题目'):j], t[j + len('## 参考答案'):k]
        # 标题行（合法删）
        m = re.search(r'(?m)^#{2,4}\s*第\s*[0-9一二三四五六七八九十]+\s*题[^\n]*$', rawq)
        head = m.group(0) if m else ''
        try:
            c = BO.X.extract(p)
            q0 = BO.conv_imgs(BO.clean_q(c['question']))
            a0 = BO.clean_a(BO.conv_imgs(c['answer']), q0)
            q, a = BO.html_table_to_md(q0), BO.html_table_to_md(a0)
        except Exception as e:
            sus_q.append((p, 'EXTRACT_ERR ' + str(e)[:40], 0)); continue
        # 是否入池（粗判：题面/答案够长）
        if len(re.sub(r'\s+', '', q)) < 60 or len(re.sub(r'\s+', '', a)) < 25:
            continue
        n_pool += 1
        qn_raw, qn_new = strip_md(BO.conv_imgs(rawq)), strip_md(q)
        an_raw, an_new = strip_md(BO.conv_imgs(rawa)), strip_md(a)
        hn = strip_md(head)
        qn_all = strip_md(rawq)          # 含标题
        # 题面丢失
        lost_q = ngrams(qn_raw) - ngrams(qn_new)
        bad_q = {g for g in lost_q if g not in hn}
        if bad_q:
            sus_q.append((p, '题面丢块 %d' % len(bad_q), len(bad_q)))
        # 答案丢失
        lost_a = ngrams(an_raw) - ngrams(an_new)
        qset = ngrams(qn_new) | ngrams(qn_raw)
        bad_a = {g for g in lost_a if g not in qset}
        if bad_a:
            sus_a.append((p, '答案丢块 %d' % len(bad_a), len(bad_a)))
    print('入池粗判 %d 张' % n_pool)
    print()
    print('=== 题面可疑丢块（%d 张）===' % len(sus_q))
    for p, r, n in sorted(sus_q, key=lambda x: -x[2])[:40]:
        print('  %-18s | %s' % (r, os.path.basename(p)[:56]))
    print()
    print('=== 答案可疑丢块（%d 张）===' % len(sus_a))
    for p, r, n in sorted(sus_a, key=lambda x: -x[2])[:40]:
        print('  %-18s | %s' % (r, os.path.basename(p)[:56]))


main()
