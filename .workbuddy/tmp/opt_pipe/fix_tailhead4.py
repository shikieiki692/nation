# -*- coding: utf-8 -*-
"""修 4 张：题面区末尾的「答案册标题行」（含 HZ-01-09 的答案册前言）⇒ 截断 + 校勘注。"""
import os, re, sys, glob
sys.stdout.reconfigure(encoding='utf-8')

KEYS = ['题-HYS-01-10-具有吗啡骨架', '题-HYS-02-10-101以下是两个',
        '题-HZ-38-08-的晶胞参数', '题-HZ-01-09-某无色有机底物S']
HDR = re.compile(r'(?m)^#{1,4}[ \t]*([^\n]{0,70}?答案[^\n]{0,40})\s*$')

for k in KEYS:
    fs = [x for x in glob.glob('04-题库/2026机构初赛模拟题/**/题-*.md', recursive=True)
          if os.path.basename(x).startswith(k)]
    if not fs:
        print('未找到', k); continue
    p = fs[0]
    t = open(p, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n')
    i = t.find('## 题目'); j = t.find('## 参考答案')
    qz = t[i:j]
    cut = None
    for m in HDR.finditer(qz):
        if m.group(1).strip() in ('参考答案', '答案'):
            continue
        cut = m.start()
        hdr = m.group(1).strip()
        break
    if cut is None:
        print('未命中标题行:', os.path.basename(p)[:50]); continue
    dropped = qz[cut:].strip()
    keep = qz[:cut].rstrip()
    note = ('\n\n> 📄 校勘（2026-10-07）：源卡题面区末尾**混入了答案册标题/前言**（`%s` 起，共 %d 字）'
            '，非题目内容 ⇒ 已截断。' % (hdr[:44], len(dropped)))
    new_t = t[:i] + keep + note + '\n\n' + t[j:]
    open(p, 'w', encoding='utf-8', newline='\n').write(new_t)
    # 复核
    t2 = open(p, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n')
    i2 = t2.find('## 题目'); j2 = t2.find('## 参考答案')
    print('%-46s 题面 %d→%d 字 | 结构 %s' % (
        os.path.basename(p)[:44], len(qz), len(t2[i2:j2]),
        {h: t2.count(h) for h in ['## 题目', '## 参考答案', '## 知识点映射']}))
    print('    删: %r' % dropped[:90])
