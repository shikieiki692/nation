# -*- coding: utf-8 -*-
r"""找出「图注行」后紧跟非空行（粘连）的位置。"""
import io, re
CAP = re.compile(r'^图\s*\d+')
for V in ['XV', 'X', 'XI', 'XIp', 'XIV']:
    for tag in ['学生版', '答案版']:
        p = '04-题库/初赛模拟卷%s（非有机·%s）.md' % (V, tag)
        try:
            lines = io.open(p, encoding='utf-8-sig').read().split('\n')
        except Exception:
            continue
        hits = []
        for i, ln in enumerate(lines):
            s = ln.strip()
            if re.fullmatch(r'图\s*\d+', s) and i + 1 < len(lines) and lines[i + 1].strip():
                hits.append((i + 1, s, lines[i + 1].strip()[:60]))
        if hits:
            print('=== %s %s ===' % (V, tag))
            for L, cap, nxt in hits:
                print('   L%-4d %r → %r' % (L, cap, nxt))
