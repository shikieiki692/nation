# -*- coding: utf-8 -*-
"""收紧版：live 文档中的题库过期数字（十六进制边界排除 + 上下文关键词）"""
import os, io, re

R = r'C:\Obsidion\妙妙屋'
SKIP_DIRS = {'.git', '.obsidian', 'node_modules', '_归档', '归档', '09-审计报告', '工作日志',
             '.workbuddy', '媒体仓库', '06-外部资料导入', '11-模板', '.claude'}

TOKENS = ['2,657', '2,659', '4,130', '4,127', '4,058', '4,183', '4,076', '4,327', '4,657',
          '1,685', '1,930', '4,298', '4,004', '2,484', '1,262', '1,553', '544', '484',
          '311', '263', '219', '208', '103', '697', '2,381', '3,933']
CTX = ('题库', '题目', '教材', '习题', '题卡', '组卷', '成书', '文件', '收录', '共')
HEX = re.compile(r'[0-9a-fA-F]')

hits = {}
for dp, dn, fn in os.walk(R):
    dn[:] = [d for d in dn if d not in SKIP_DIRS]
    for f in fn:
        if not f.endswith('.md'):
            continue
        p = os.path.join(dp, f)
        try:
            t = io.open(p, encoding='utf-8').read()
        except Exception:
            continue
        for i, line in enumerate(t.split('\n'), 1):
            if not any(c in line for c in CTX):
                continue
            for tk in TOKENS:
                pos = line.find(tk)
                while pos != -1:
                    a = line[pos - 1] if pos > 0 else ''
                    b = line[pos + len(tk)] if pos + len(tk) < len(line) else ''
                    # 十六进制边界排除：紧邻是 0-9a-f 则跳过（SHA1/行号）
                    if not HEX.match(a) and not HEX.match(b):
                        hits.setdefault(p, []).append((i, tk, line.strip()[:150]))
                    pos = line.find(tk, pos + 1)

print('命中文件数 =', len(hits))
for p in sorted(hits):
    print('#### %s' % os.path.relpath(p, R))
    seen = set()
    for i, tk, line in hits[p]:
        if line in seen:
            continue
        seen.add(line)
        print('     L%-4d [%s] %s' % (i, tk, line))
