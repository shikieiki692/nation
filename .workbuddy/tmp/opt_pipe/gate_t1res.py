# -*- coding: utf-8 -*-
r"""T1 RESIDUAL 闸门：FM strict + validate_kb + 卷层影响。"""
import os, io, json, subprocess, glob
os.chdir(r'C:\Obsidion\妙妙屋')
PY = r'C:\Users\蕾赛\AppData\Local\Programs\Python\Python312\python.exe'

st = subprocess.run(['git', '-c', 'core.quotepath=false', 'status', '--short', '04-题库'],
                    capture_output=True, text=True, encoding='utf-8').stdout
paths = [l[3:].strip().strip('"') for l in st.split('\n') if l.strip()]
print('改动文件 %d' % len(paths))

# FM strict
req = []
for p in paths:
    src = io.open(p, encoding='utf-8-sig').read()
    fm = src.split('---')[1] if src.startswith('---') else ''
    req.append({'id': p, 'source': fm, 'mode': 'strict'})
r = subprocess.run([PY, '-X', 'utf8', '.workbuddy/scripts/yaml_compat.py'],
                   input=json.dumps(req, ensure_ascii=False), capture_output=True, text=True, encoding='utf-8')
out = json.loads(r.stdout)
bad = [o for o in out if not o.get('ok')]
print('FM strict: %d/%d 通过 %s' % (len(out) - len(bad), len(out), '✅' if not bad else '❌'))
for b in bad:
    print('   ✗', b.get('id', '')[-40:], str(b.get('error'))[:90])

# validate_kb
r2 = subprocess.run([PY, '-X', 'utf8', '11-模板/scripts/validate_kb.py', '--changed'] + paths,
                    capture_output=True, text=True, encoding='utf-8')
for ln in r2.stdout.split('\n'):
    if '受检' in ln or 'Error' in ln or 'Warning' in ln:
        print('  ' + ln.strip())

# 卷层影响
used = set()
for pm in glob.glob('.workbuddy/tmp/opt_pipe/vol_plan_*.json'):
    try:
        d = json.load(io.open(pm, encoding='utf-8'))
    except Exception:
        continue
    for g in d:
        it = g[1] if isinstance(g, (list, tuple)) and len(g) > 1 else g
        if isinstance(it, list):
            for x in it:
                if isinstance(x, dict) and x.get('path'):
                    used.add(os.path.basename(x['path']))
inter = {os.path.basename(p) for p in paths} & used
print('卷层影响: %s' % ('无（%d 卡∩卷计划=0）✅' % len(paths) if not inter else '⚠️ ' + str(sorted(inter)[:5])))
