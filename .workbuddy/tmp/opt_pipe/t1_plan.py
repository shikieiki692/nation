# -*- coding: utf-8 -*-
r"""T1 拟改清单（只读）：逐处给出「原文 → 拟改」，标注 AUTO/REVIEW。"""
import os, re, io
os.chdir(r'C:\Obsidion\妙妙屋')

D1 = re.compile(r'\\mathrm\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*?\\mathring[^{}]*(?:\{[^{}]*\}[^{}]*)*?)\}')
D2 = re.compile(r'\\mathrm\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*?\\Delta[^{}]*(?:\{[^{}]*\}[^{}]*)*?)\}')
XARR = re.compile(r'\\x?rightarrow\s*\[[^\]]*\\Delta')

def d1_fix(seg):
    body = re.sub(r'\\mathrm\s*\{[^{}]*\\mathring\s*A\s*\}', '', seg)
    body = re.sub(r'\\mathring\s*A', '', body)
    if re.sub(r'[\s~]', '', body) == '':
        return r'\text{Å}'
    return None

def d2_fix(seg):
    if XARR.search(seg):
        return None
    if re.search(r'\\Delta\s*[_^]', seg):
        return None
    if re.search(r'\\Delta\s*(?:[HGSURAF](?![a-z]))', seg):
        return None
    if re.search(r'\\Delta\s*[A-Z][A-Za-z]', seg):
        out = re.sub(r'\\Delta\s*', '', seg)
        return out if out.strip() else None
    if re.fullmatch(r'[\s~]*\\Delta[\s~]*', seg):
        return ''
    return None

auto = rev = 0
print('%-3s %-6s %-42s %s' % ('#', '类', '原文', '→ 拟改'))
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
            i += 1
            kind = 'D1' if '\\mathring' in m.group(1) else 'D2'
            r = d1_fix(m.group(1)) if kind == 'D1' else d2_fix(m.group(1))
            tag = 'AUTO' if r is not None else 'REVIEW'
            if r is not None:
                auto += 1
                out = r if r != '' else '(整体删除)'
            else:
                rev += 1
                out = '—'
            print('%-3d %-4s %-6s %-42s %s' % (i, kind, tag, m.group(0)[:42].replace('\n', '⏎'), out[:44]))
print()
print('合计 %d 处：AUTO %d ｜ REVIEW %d' % (i, auto, rev))
