# -*- coding: utf-8 -*-
"""09-审计报告 type 归一：审计/audit → 审计报告；无 type 的补 审计报告
排除：并行工作区占用的文件 / chemy 图升级线领地
"""
import io, os, re, sys, subprocess, shutil, datetime
os.chdir(r'C:\Obsidion\妙妙屋')
from ruamel.yaml import YAML
y = YAML(typ='safe', pure=True); y.version = (1, 2); y.allow_duplicate_keys = True

APPLY = '--apply' in sys.argv
D = '09-审计报告'

# 排除清单（并行领地/工作区脏）
EXCLUDE_SUBSTR = ('chemy', '图升级线', '图线')
st = subprocess.run(['git', '-c', 'core.quotepath=false', 'status', '--short', D],
                    capture_output=True, text=True, encoding='utf-8').stdout
dirty = set()
for ln in st.split('\n'):
    if not ln.strip():
        continue
    p = ln[3:].strip().strip('"')
    if p.endswith('.md'):
        dirty.add(p)

jobs = []   # (path, action, old_line, new_line)
def is_archived(path):
    return ('_归档' in path) or ('_archive' in path) or ('/归档' in path)

for dp, dn, fn in os.walk(D):
    dn[:] = [x for x in dn if not (x.startswith('_归档') or x.startswith('_archive') or x == '归档')]
    for f in sorted(fn):
        if not f.endswith('.md'):
            continue
        p = os.path.join(dp, f).replace('\\', '/')
        if is_archived(p):
            continue            # 归档目录：保真豁免
        if p in dirty:
            continue
        if any(s in p for s in EXCLUDE_SUBSTR):
            continue
        t = io.open(p, encoding='utf-8-sig', errors='replace').read()
        m = re.match(r'^---[ \t]*\r?\n(.*?)\r?\n---(\r?\n|$)', t, re.S)
        if not m:
            continue
        fm = m.group(1)
        try:
            d = y.load(fm) or {}
        except Exception:
            continue
        ty = d.get('type')
        if ty in ('审计', 'audit'):
            old = [l for l in fm.split('\n') if re.match(r'^type:[ \t]*(审计|audit)[ \t]*$', l)]
            assert len(old) == 1, (p, old)
            jobs.append((p, '归一同义', old[0], 'type: 审计报告'))
        elif 'type' not in d:
            # 插在 title 行后
            lines = fm.split('\n')
            idx = None
            for i, l in enumerate(lines):
                if re.match(r'^title:[ \t]', l):
                    idx = i
                    break
            if idx is None:
                idx = 0
            jobs.append((p, '补 type', lines[idx], lines[idx] + '\n' + 'type: 审计报告'))

print('=== 待改 %d 个 ===' % len(jobs))
for p, act, o, n in jobs:
    print('  [%s] %s' % (act, p[:86]))
print()
print('  归一同义 %d ｜ 补 type %d' % (sum(1 for j in jobs if j[1] == '归一同义'), sum(1 for j in jobs if j[1] == '补 type')))
print('  跳过工作区脏 %d' % len(dirty))
print('  跳过领地(chemy/图线) %d' % sum(1 for dp, dn, fn in os.walk(D) for f in fn if f.endswith('.md') and any(s in f for s in EXCLUDE_SUBSTR)))

if not APPLY:
    print()
    print('(dry-run；加 --apply 执行)')
    sys.exit(0)

bak = '.workbuddy/tmp/opt_pipe/_bak/audittype_%s' % datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
os.makedirs(bak, exist_ok=True)
done = 0
for p, act, o, n in jobs:
    t = io.open(p, encoding='utf-8-sig').read()
    m = re.match(r'^---[ \t]*\r?\n(.*?)\r?\n---', t, re.S)
    fm = m.group(1)
    if fm.count(o) != 1:
        print('  ⚠️ 跳过（命中≠1）%s' % p)
        continue
    shutil.copy2(p, os.path.join(bak, os.path.basename(p)))
    nfm = fm.replace(o, n)
    rest = t[m.end():]
    io.open(p, 'w', encoding='utf-8', newline='').write('---\n' + nfm + '\n---' + rest)
    done += 1
print('已写盘 %d' % done)
