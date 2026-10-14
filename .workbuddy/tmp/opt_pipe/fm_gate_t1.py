# -*- coding: utf-8 -*-
r"""用 yaml_compat（ruamel YAML1.2 strict）校验改动文件的 FM。"""
import os, io, json, subprocess, sys
os.chdir(r'C:\Obsidion\妙妙屋')
PY = r'C:\Users\蕾赛\AppData\Local\Programs\Python\Python312\python.exe'

files = subprocess.run(['git', '-c', 'core.quotepath=false', 'status', '--short', '04-题库'],
                       capture_output=True, text=True, encoding='utf-8').stdout
paths = [l[3:].strip().strip('"') for l in files.strip().split('\n') if l.strip()]
req = []
for i, p in enumerate(paths):
    try:
        src = io.open(p, encoding='utf-8-sig').read()
    except Exception as e:
        print('读取失败', p); continue
    m = src.split('---')
    fm = m[1] if len(m) > 2 else ''
    req.append({'id': p, 'source': fm, 'mode': 'strict'})

r = subprocess.run([PY, '-X', 'utf8', '.workbuddy/scripts/yaml_compat.py'],
                   input=json.dumps(req, ensure_ascii=False),
                   capture_output=True, text=True, encoding='utf-8')
try:
    out = json.loads(r.stdout)
except Exception:
    print('解析后端输出失败:', r.stdout[-400:], r.stderr[-400:]); sys.exit(1)
bad = [o for o in out if not o.get('ok')]
print('校验 %d 个文件的 FM（strict）｜ 失败 %d' % (len(out), len(bad)))
for b in bad:
    print('  ✗ %s : %s' % (b.get('id', '')[-40:], str(b.get('error'))[:120]))
print('VERDICT:', 'PASS' if not bad else 'FAIL')
