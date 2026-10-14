# -*- coding: utf-8 -*-
r"""补卷 XV（4 张）/ XVI（1 张）真缺图 —— 源卡已有文件，卷内漏引。

每项：(卷, 版本列表, 锚点正则, 图文件名, 图注)
锚点＝该问号/说明句所在行；图插在**该整段结束处**（下一个问号/标题/分隔线前）。
安全：图块已存在则跳过；锚点须唯一；插入后断言图数 +1。
"""
import io, os, re, shutil, datetime

ROOT = r"C:\Obsidion\妙妙屋"
BAK = os.path.join(ROOT, '.workbuddy/tmp/opt_pipe/_bak/addfig_%s'
                   % datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
os.makedirs(BAK, exist_ok=True)

JOBS = [
    # 卷 XV 题面区（两版都有题面）
    ('XV', ['学生版', '答案版'], r'^5-3-1\s',
     'f4df0a6065155cd2b7ab69c189eb2834986d59696063cb709e36fdbbac77fea3.jpg', '图 1'),
    ('XV', ['学生版', '答案版'], r'^5-3-3\s',
     '00c6ede6e9c62616419a5a87e306e1a10876f3cabca638b3c9f04dd427bc7ec5.jpg', '图 2'),
    # 卷 XV 答案区（仅答案版）—— 锚点是答案文字行
    ('XV', ['答案版'], r'立方钙钛矿',
     '451a4e6e83d0945399bb9c1175fc34eea5d09f76e6674195ca224be932cf8796.jpg', '图 3'),
    ('XV', ['答案版'], r'^\*?\*?4-2',
     '023f35336b6db2d52e185a1347bf2d79c9134b8f19ff67540c9c049b6b8c0977.jpg', '图 4'),
    # 卷 XVI 第 10 题
    ('XVI', ['学生版', '答案版'], r'^10-\d',
     '96ea08d2500c9bdb2bfcf5149af01013e005963ef3f593d2ea81ade26fcacaf4.jpg', '图 1'),
]

for vol, tags, rx, img, cap in JOBS:
    for tag in tags:
        p = os.path.join(ROOT, '04-题库', '初赛模拟卷%s（非有机·%s）.md' % (vol, tag))
        if not os.path.isfile(p):
            print('  -- %s %s 文件不存在' % (vol, tag)); continue
        d = io.open(p, encoding='utf-8', newline='').read()
        if img[:20] in d:
            print('  -- %s %s 已含，跳过' % (vol, tag)); continue
        lines = d.split('\n')
        hits = [i for i, l in enumerate(lines) if re.match(rx, l.strip())]
        if len(hits) != 1:
            print('  !! %s %s 锚点 %s 命中 %d ⇒ 跳过' % (vol, tag, rx, len(hits))); continue
        i = hits[0]
        # 段尾：向下找下一个问号/标题/分隔线
        j = i + 1
        while j < len(lines):
            s = lines[j].strip()
            if re.match(r'^\d+(?:-\d+)*\s', s) or s.startswith('#') or s == '---':
                break
            j += 1
        k = j
        while k > i and lines[k - 1].strip() == '':
            k -= 1
        newlines = lines[:k] + ['', '![[%s]]' % img, cap] + lines[k:]
        new = '\n'.join(newlines)
        b, a = len(re.findall(r'!\[\[', d)), len(re.findall(r'!\[\[', new))
        if a != b + 1:
            print('  !! %s %s 图数异常 %d→%d ⇒ 跳过' % (vol, tag, b, a)); continue
        shutil.copy2(p, os.path.join(BAK, os.path.basename(p)))
        io.open(p, 'w', encoding='utf-8', newline='').write(new)
        print('  ✓ %s %s：L%d 段尾插入（图数 %d→%d）' % (vol, tag, k, b, a))
print('备份：', BAK)
