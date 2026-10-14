# -*- coding: utf-8 -*-
r"""把 `\xrightarrow{...\\...}` 的实参包进 `\substack{}`（括号配平）。只改这两个文件。"""
import io, os, re, shutil, datetime
os.chdir(r'C:\Obsidion\妙妙屋')

FILES = [
 '04-题库/元文件/有机化学阶段测试卷-答案.md',
 '04-题库/有机化学/有机合成与金属有机/题-有机-合成-Grignard试剂与不同羰基化合物反应路线设计.md',
]
BAK = '.workbuddy/tmp/opt_pipe/_bak/arrow_%s' % datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
os.makedirs(BAK, exist_ok=True)

def balanced(t, i):
    """t[i] 应为 '{'，返回配平到对应 '}' 的内容起止 (content_start, end_index_exclusive_of_brace)"""
    assert t[i] == '{'
    d = 0
    j = i
    while j < len(t):
        if t[j] == '{':
            d += 1
        elif t[j] == '}':
            d -= 1
            if d == 0:
                return i + 1, j
        j += 1
    return None, None

def wrap_arrows(t):
    out = []
    i = 0
    n = 0
    while i < len(t):
        m = re.compile(r'\\(x|)rightarrow').match(t, i)
        if not m:
            out.append(t[i]); i += 1; continue
        j = m.end()
        # 可选 [ ... ]（配平）
        if j < len(t) and t[j] == '[':
            cs, ce = balanced(t, j)
            if cs is None:
                out.append(t[i]); i += 1; continue
            j = ce + 1
        while j < len(t) and t[j] in ' \t':
            j += 1
        if j >= len(t) or t[j] != '{':
            out.append(t[i]); i += 1; continue
        cs, ce = balanced(t, j)
        if cs is None:
            out.append(t[i]); i += 1; continue
        arg = t[cs:ce]
        if '\\\\' in arg and not arg.strip().startswith('\\substack'):
            new = m.group(0) + t[m.end():j] + '{\\substack{' + arg + '}}'
            out.append(new)
            n += 1
            i = ce + 1
        else:
            out.append(t[i]); i += 1
    return ''.join(out), n

tot = 0
for p in FILES:
    t = io.open(p, encoding='utf-8-sig').read()
    shutil.copy2(p, os.path.join(BAK, os.path.basename(p)[:60]))
    t2, n = wrap_arrows(t)
    if n:
        io.open(p, 'w', encoding='utf-8', newline='').write(t2)
    tot += n
    print('%-70s 包裹 %d 处  %d→%d 字节' % (os.path.basename(p)[:68], n, len(t), len(t2)))
print('合计 %d 处；备份 %s' % (tot, BAK))
