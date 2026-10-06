# -*- coding: utf-8 -*-
"""精确列出机构题库中的「无答案/答案可疑」卡，按机构分组，并给出 source_file 回源线索。
口径（已排除历史自检坑）：
  - 读文件 utf-8-sig，CRLF 归一为 LF
  - 题面 = [## 题目, ## 参考答案)
  - 答案 = [## 参考答案, ## 知识点映射)
  - 答案「空」= 去图去标题去空白后 < 12 字（且无图）
  - 答案「占位」= 命中 ⛔/源池无|仅|未见 等明示无答案标记
输出：CSV 到 .workbuddy/tmp/opt_pipe/noans_list.csv + 控制台汇总
"""
import os, re, glob, sys, csv, collections

sys.stdout.reconfigure(encoding='utf-8')
BASE = '04-题库/2026机构初赛模拟题'
SRCS = ['化英社', '清北营', 'chemy', '伽马', '壹尖培优', '汇智', 'XeChem',
        '质心GChO', '质心UChO', '方圆', '一式', '北京夏令营', '2ChO']

# 明示「源池没有答案」的占位标记（只认真正的无答案声明）
PH = re.compile(r'⛔|源池(无|仅|未见)')


def get_fm(t, key):
    m = re.search(r'^' + key + r':[ \t]*(.*?)[ \t]*$', t, re.M)
    if not m:
        return ''
    v = m.group(1).strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in '"\'':
        v = v[1:-1]
    return v


def ans_sec(t):
    ia = t.find('## 参考答案')
    if ia < 0:
        ia = t.find('## 答案')
    if ia < 0:
        return ''
    e = t.find('\n## 知识点映射', ia)
    return t[ia:(e if e > 0 else len(t))]


def strip_marks(a):
    b = re.sub(r'!\[\[?[^\]]*\]?\]', '', a)
    b = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', b)
    b = re.sub(r'<img[^>]*>', '', b)
    b = re.sub(r'(?m)^#{1,6}.*$', '', b)
    return re.sub(r'\s+', '', b)


rows = []
cnt_all = collections.Counter()
cnt_noph = collections.Counter()
cnt_ph = collections.Counter()
for r in SRCS:
    for p in sorted(glob.glob(os.path.join(BASE, r, '**', '题-*.md'), recursive=True)):
        cnt_all[r] += 1
        t = open(p, encoding='utf-8-sig').read().replace('\r\n', '\n')
        a = ans_sec(t)
        has_img = bool(re.search(r'!\[|<img', a))
        an = strip_marks(a)
        cat = None
        if PH.search(a):
            cat = 'PH占位'
            cnt_ph[r] += 1
        elif len(an) < 12 and not has_img:
            cat = 'EMPTY真空'
            cnt_noph[r] += 1
        if cat:
            rows.append(dict(
                inst=r,
                card=os.path.basename(p)[:-3],
                path=p.replace(os.sep, '/'),
                cat=cat,
                source_file=get_fm(t, 'source_file'),
                source_norm=get_fm(t, 'source_norm'),
                subject=get_fm(t, 'subject_module'),
                difficulty=get_fm(t, 'difficulty'),
                ans_len=len(an),
            ))

out = '.workbuddy/tmp/opt_pipe/noans_list.csv'
with open(out, 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

print('=== 无答案卡按机构 ===')
print('%-10s %6s %6s %6s' % ('机构', '总卡', '占位', '真空'))
for r in SRCS:
    if cnt_ph[r] or cnt_noph[r]:
        print('%-10s %6d %6d %6d' % (r, cnt_all[r], cnt_ph[r], cnt_noph[r]))
print('%-10s %6d %6d %6d' % ('合计', sum(cnt_all.values()), sum(cnt_ph.values()), sum(cnt_noph.values())))
print()
print('总无答案 = %d（PH %d + EMPTY %d）' % (len(rows), sum(cnt_ph.values()), sum(cnt_noph.values())))
print('CSV →', out)
