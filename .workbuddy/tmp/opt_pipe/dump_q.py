# -*- coding: utf-8 -*-
"""导出卷 XVII 每题的「题干 + 答案要点」，供撰写解析"""
import io, os, re
os.chdir(r'C:\Obsidion\妙妙屋')
t = io.open('04-题库/初赛模拟卷XVII（非有机·答案版）.md', encoding='utf-8-sig').read()
blocks = re.split(r'(?=^### 第 \d+ 题)', t, flags=re.M)
for b in blocks:
    m = re.match(r'^### 第 (\d+) 题', b)
    if not m:
        continue
    n = m.group(1)
    i = b.find('#### 答案')
    stem = b[:i] if i > 0 else b
    ans = b[i:] if i > 0 else ''
    # 去图引用
    stem = re.sub(r'!\[\[[^\]]*\]\]', '[图]', stem)
    ans = re.sub(r'!\[\[[^\]]*\]\]', '[图]', ans)
    # 压缩公式块
    ans = re.sub(r'\$\$\s*\\begin\{array\}.*?\\end\{array\}\s*\$\$', '[公式块]', ans, flags=re.S)
    ans = re.sub(r'\n{3,}', '\n\n', ans)
    print('=' * 100)
    print('### 第 %s 题' % n)
    print('--- 题面（前 1200 字）---')
    print(stem[:1200].strip())
    print()
    print('--- 答案（前 1800 字）---')
    print(ans[:1800].strip())
    print()
