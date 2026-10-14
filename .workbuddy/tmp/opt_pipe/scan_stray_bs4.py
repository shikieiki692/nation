# -*- coding: utf-8 -*-
r"""stray 判定 v3：\substack{} 用真正的花括号深度跟踪；\begin{} 用 \end{} 配对。"""
import os, io, re
os.chdir(r'C:\Obsidion\妙妙屋')
BLOCK = re.compile(r'\$\$(.+?)\$\$', re.S)
INLINE = re.compile(r'(?<!\$)\$([^$\n]+?)\$(?!\$)')

def stray_positions(seg):
    out = []; i = 0; n = len(seg)
    stack = []          # 元素: ('sub', depth) 或 ('env', name)
    m_env = re.compile(r'\\begin\{([a-zA-Z*]+)\}')
    m_end = re.compile(r'\\end\{([a-zA-Z*]+)\}')
    m_sub = re.compile(r'\\substack\s*\(')
    m_sub2 = re.compile(r'\\substack\s*\{')
    while i < n:
        if seg.startswith('\\\\', i):
            if not stack:
                out.append(i)
            i += 2; continue
        m = m_env.match(seg, i)
        if m:
            stack.append(['env', m.group(1)]); i = m.end(); continue
        m = m_end.match(seg, i)
        if m:
            # 弹到最近的同名 env
            for j in range(len(stack) - 1, -1, -1):
                if stack[j][0] == 'env' and stack[j][1] == m.group(1):
                    del stack[j:]; break
            i = m.end(); continue
        m = m_sub2.match(seg, i)
        if m:
            stack.append(['sub', 1]); i = m.end(); continue
        if seg[i] == '{':
            if stack and stack[-1][0] == 'sub':
                stack[-1][1] += 1
            i += 1; continue
        if seg[i] == '}':
            if stack and stack[-1][0] == 'sub':
                stack[-1][1] -= 1
                if stack[-1][1] == 0:
                    stack.pop()
            i += 1; continue
        i += 1
    return out

hits = []
for root in ['04-题库', '04-课件', '03-知识点', '05-真题库']:
    for dp, dn, fn in os.walk(root):
        for f in fn:
            if not f.endswith('.md'):
                continue
            p = os.path.join(dp, f)
            try:
                t = io.open(p, encoding='utf-8-sig').read()
            except Exception:
                continue
            det = []
            for m in BLOCK.finditer(t):
                for pos in stray_positions(m.group(1)):
                    det.append(('块', m.group(1)[max(0, pos - 60):pos + 35].replace('\n', '⏎')))
            for m in INLINE.finditer(t):
                for pos in stray_positions(m.group(1)):
                    det.append(('行内', m.group(1)[max(0, pos - 45):pos + 30]))
            if det:
                hits.append((p, det))
print('真命中 %d 文件' % len(hits))
for p, det in hits:
    print('◆ %s' % p[:72])
    for k, seg in det:
        print('   [%s] …%s…' % (k, seg))
print()
print('合计 %d 处' % sum(len(d) for _, d in hits))
