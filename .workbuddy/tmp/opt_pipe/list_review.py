# -*- coding: utf-8 -*-
r"""列 T1 剩余 REVIEW 项（D1/D2 中非 auto 的），带上下文 + 文件。"""
import os, io, re
os.chdir(r'C:\Obsidion\妙妙屋')

D1 = re.compile(r'\\mathrm\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*?\\mathring[^{}]*(?:\{[^{}]*\}[^{}]*)*?)\}')
D2 = re.compile(r'\\mathrm\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*?\\Delta[^{}]*(\{[^{}]*\}[^{}]*)*?)\}')
XARR = re.compile(r'\\x?rightarrow\s*\[[^\]]*\\Delta')

def auto(seg, kind):
    if kind == 'D1':
        b = re.sub(r'\\mathrm\s*\{[^{}]*\\mathring\s*A\s*\}', '', seg)
        b = re.sub(r'\\mathring\s*A', '', b)
        return re.sub(r'[\s~]', '', b) == ''
    if XARR.search(seg):
        return False
    if re.search(r'\\Delta\s*[_^]', seg):
        return False
    if re.search(r'\\Delta\s*(?:[HGSURAF](?![a-z]))', seg):
        return False
    if re.search(r'\\Delta\s*[A-Z][A-Za-z]', seg):
        return True
    if re.fullmatch(r'[\s~]*\\Delta[\s~]*', seg):
        return True
    return False

i = 0
for dp, dn, fn in os.walk('04-题库'):
    for f in sorted(fn):
        if not f.endswith('.md'):
            continue
        p = os.path.join(dp, f).replace(os.sep, '/')
        try:
            t = io.open(p, encoding='utf-8-sig').read()
        except Exception:
            continue
        for m in list(D1.finditer(t)) + list(D2.finditer(t)):
            kind = 'D1' if '\\mathring' in m.group(1) else 'D2'
            if auto(m.group(1), kind):
                continue
            i += 1
            s = max(0, m.start() - 70)
            ctx = t[s:m.end() + 50].replace('\n', '⏎')
            print('[%2d] %s  %s' % (i, kind, os.path.basename(p)[:46]))
            print('     原文: %s' % m.group(0)[:74].replace('\n', '⏎'))
            print('     语境: …%s…' % ctx[:150])
print()
print('REVIEW 共 %d 处' % i)
