# -*- coding: utf-8 -*-
"""全链「内容保真筛」v2：滑动 14-gram 集合比对（对插入/删除稳健）。"""
import os, re, sys, glob
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.workbuddy/tmp/opt_pipe')
sys.argv = ['x', '--vol', 'AUD2', '--all-years']
import build_org as BO

N = 14


def strip_md(s):
    s = re.sub(r'!\[\[[^\]]*\]\]', '', s)
    s = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', s)
    s = re.sub(r'</?[a-zA-Z][^>]*>', '', s)
    s = re.sub(r'[#*`>_~\[\](){}|\s]', '', s)
    s = re.sub(r'-', '', s)
    return s


def ng(s):
    if len(s) < N:
        return set()
    return {s[i:i + N] for i in range(len(s) - N + 1)}


def main():
    cards = glob.glob('04-题库/2026机构初赛模拟题/**/题-*.md', recursive=True)
    sus_q, sus_a = [], []
    n_pool = 0
    for p in cards:
        t = open(p, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n')
        i = t.find('## 题目'); j = t.find('## 参考答案'); k = t.find('## 知识点映射')
        if i < 0 or j < 0 or k < 0:
            continue
        rawq, rawa = t[i + len('## 题目'):j], t[j + len('## 参考答案'):k]
        m = re.search(r'(?m)^#{2,4}\s*第\s*[0-9一二三四五六七八九十]+\s*题[^\n]*$', rawq)
        head = m.group(0) if m else ''
        try:
            c = BO.X.extract(p)
            q0 = BO.conv_imgs(BO.clean_q(c['question']))
            a0 = BO.clean_a(BO.conv_imgs(c['answer']), q0)
            q, a = BO.html_table_to_md(q0), BO.html_table_to_md(a0)
        except Exception:
            continue
        if len(re.sub(r'\s+', '', q)) < 60 or len(re.sub(r'\s+', '', a)) < 25:
            continue
        n_pool += 1
        # 题面：原文(含标题) vs 清洗后
        q_raw, q_new = strip_md(BO.conv_imgs(rawq)), strip_md(q)
        hn = strip_md(head)
        bad_q = (ng(q_raw) - ng(q_new)) - ng(hn)
        if len(bad_q) >= 8:
            sus_q.append((p, len(bad_q)))
        # 答案：原文 vs 清洗后；把「能在题面里找到」的算合法回显
        a_raw, a_new = strip_md(BO.conv_imgs(rawa)), strip_md(a)
        pool_q = ng(q_new) | ng(q_raw)
        bad_a = (ng(a_raw) - ng(a_new)) - pool_q
        if len(bad_a) >= 8:
            sus_a.append((p, len(bad_a)))
    print('入池粗判 %d 张' % n_pool)
    print('=== 题面可疑丢块（≥8 gram）: %d 张 ===' % len(sus_q))
    for p, n in sorted(sus_q, key=lambda x: -x[1])[:30]:
        print('  %5d | %s' % (n, os.path.basename(p)[:58]))
    print('=== 答案可疑丢块（≥8 gram）: %d 张 ===' % len(sus_a))
    for p, n in sorted(sus_a, key=lambda x: -x[1])[:30]:
        print('  %5d | %s' % (n, os.path.basename(p)[:58]))


main()
