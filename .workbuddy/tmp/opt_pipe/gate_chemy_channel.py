# -*- coding: utf-8 -*-
"""改后闸门：FM(strict) + validate_kb(--dir) + render_gate(分批 --changed)。"""
import io, os, re, glob, json, subprocess, sys

os.chdir(r'C:\Obsidion\妙妙屋')
PY = r'C:\Users\蕾赛\AppData\Local\Programs\Python\Python312\python.exe'


def run(a, **kw):
    return subprocess.run(a, capture_output=True, text=True, encoding='utf-8', errors='replace', **kw)


# 改动清单（本次会话改的 183 卡）
st = run(['git', '-c', 'core.quotepath=false', 'status', '--short', '04-题库/2026机构初赛模拟题/chemy/'])
cards = [l[3:].strip().strip('"') for l in st.stdout.split('\n') if l.strip().endswith('.md')]
print('改动卡数', len(cards))

# 1) FM strict
req = [{'id': p, 'source': io.open(p, encoding='utf-8-sig').read().split('---')[1], 'mode': 'strict'} for p in cards]
r = run([PY, '-X', 'utf8', '.workbuddy/scripts/yaml_compat.py'], input=json.dumps(req, ensure_ascii=False))
bad = [o for o in json.loads(r.stdout) if not o.get('ok')]
print('FM strict: %d/%d ok' % (len(req) - len(bad), len(req)), 'FAIL' if bad else 'PASS')
for b in bad[:3]:
    print('   ', b)

# 2) validate_kb --dir
r = run([PY, '-X', 'utf8', '11-模板/scripts/validate_kb.py', '--dir', '04-题库/2026机构初赛模拟题/chemy'])
tail = [l for l in r.stdout.split('\n') if ('Error' in l or 'Warning' in l or '受检' in l)]
print('validate_kb:', ' | '.join(x.strip() for x in tail[-3:]))

# 3) render_gate 分批
B = 40
fail = []
for i in range(0, len(cards), B):
    chunk = cards[i:i + B]
    r = run([PY, '-X', 'utf8', '11-模板/scripts/render_gate.py', '--changed'] + chunk, timeout=1800)
    out = (r.stdout + r.stderr)
    tag = 'PASS' if 'PASS' in out else 'FAIL'
    if tag == 'FAIL':
        fail.append((i, out[-400:]))
    print('  render_gate 批 %d-%d : %s' % (i + 1, i + len(chunk), tag))
print('render_gate 失败批数', len(fail))
for f in fail[:2]:
    print(f[1])
