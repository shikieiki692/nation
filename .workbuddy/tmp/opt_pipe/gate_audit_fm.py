# -*- coding: utf-8 -*-
"""批量补 FM 后的闸门校验"""
import io, os, re, subprocess
os.chdir(r'C:\Obsidion\妙妙屋')
from ruamel.yaml import YAML

out = subprocess.run(['git', '-c', 'core.quotepath=false', 'diff', '--name-only', '--', '09-审计报告'],
                     capture_output=True, text=True, encoding='utf-8').stdout
mine = [x for x in out.split('\n') if x.endswith('.md')]
print('改动 md =', len(mine))
bad = []
for p in mine:
    t = io.open(p, encoding='utf-8-sig').read()
    m = re.match(r'^---[ \t]*\r?\n(.*?)\r?\n---[ \t]*\r?\n', t, re.S)
    if not m:
        bad.append((p, 'FM 结构不符'))
        continue
    y = YAML(typ='safe', pure=True); y.version = (1, 2); y.allow_duplicate_keys = False
    try:
        y.load(m.group(1))
    except Exception as e:
        bad.append((p, str(e).splitlines()[0]))
print('FM strict: %d/%d' % (len(mine) - len(bad), len(mine)))
for p, e in bad[:10]:
    print('  FAIL', p, e)

# 逐文件核对：增量恰为 FM 行数 + 1
import collections
cnt = collections.Counter()
for p in mine:
    t = io.open(p, encoding='utf-8-sig').read()
    m = re.match(r'^---[ \t]*\r?\n(.*?)\r?\n---[ \t]*\r?\n\r?\n', t, re.S)
    if not m:
        cnt['结构异常'] += 1
        continue
    fm_lines = m.group(1).count('\n') + 1
    cnt['fm行数=%d' % fm_lines] += 1
print('FM 行数分布:', dict(cnt))
