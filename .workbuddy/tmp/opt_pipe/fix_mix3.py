# -*- coding: utf-8 -*-
"""三合一：
  A. 09-审计报告 18 个非规范 type → 审计报告
  B. 09-审计报告 11 个未跟踪·无 FM → 补 FM（首行插入）
  C. 11-模板/规范 4 个无 FM → 补 FM（type: 规范）
"""
import io, os, re, subprocess, sys, shutil, datetime
os.chdir(r'C:\Obsidion\妙妙屋')
from ruamel.yaml import YAML

APPLY = '--apply' in sys.argv
y = YAML(typ='safe', pure=True); y.version = (1, 2)

def git(a):
    return subprocess.run(a, capture_output=True, text=True, encoding='utf-8', errors='replace').stdout

def is_arch(p):
    return ('_归档' in p) or ('_archive' in p) or ('/归档' in p)

def q(s):
    return "'" + s.replace("'", "''") + "'"

DATE_PRE = re.compile(r'^(\d{4}-\d{2}-\d{2})-')
DATE_ANY = re.compile(r'(\d{4}-\d{2}-\d{2})')
H1 = re.compile(r'^#[ \t]+(\S.*?)[ \t]*$', re.M)

# 未跟踪集合
st = git(['git', '-c', 'core.quotepath=false', 'status', '--short', '--untracked-files=all', '09-审计报告', '11-模板/规范'])
untracked = {ln[3:].strip().strip('"') for ln in st.split('\n') if ln.startswith('?? ')}
dirty = {ln[3:].strip().strip('"') for ln in st.split('\n') if ln.strip() and not ln.startswith('?? ')}

OK_TYPE = {'审计报告', '活跃任务卡', '系统'}
EX_OWN = ('chemy', '图升级线', '图线')
A_jobs = []   # (path, old_line, new_line)
B_jobs = []   # (path, fm_text, kind)
C_jobs = []

# ---------- A: 09-审计报告 非规范 type ----------
for dp, dn, fn in os.walk('09-审计报告'):
    dn[:] = [x for x in dn if not (x.startswith('_归档') or x.startswith('_archive') or x == '归档')]
    for f in sorted(fn):
        if not f.endswith('.md'):
            continue
        p = os.path.join(dp, f).replace('\\', '/')
        if p in untracked or p in dirty or any(s in p for s in EX_OWN):
            continue
        t = io.open(p, encoding='utf-8-sig', errors='replace').read()
        m = re.match(r'^---[ \t]*\r?\n(.*?)\r?\n---(\r?\n|$)', t, re.S)
        if not m:
            continue
        try:
            d = y.load(m.group(1)) or {}
        except Exception:
            continue
        ty = d.get('type')
        if ty in OK_TYPE or ty is None:
            continue
        old = [l for l in m.group(1).split('\n') if re.match(r'^type:[ \t]*', l)]
        if len(old) != 1:
            print('  ⚠️ A 跳过（type 行数≠1）', p)
            continue
        A_jobs.append((p, old[0], 'type: 审计报告'))

# ---------- B: 09-审计报告 未跟踪·无 FM ----------
for p in sorted(untracked):
    if not p.endswith('.md'):
        continue
    t = io.open(p, encoding='utf-8-sig', errors='replace').read()
    if re.match(r'^---[ \t]*\r?\n', t):
        continue
    m = H1.search(t)
    if not m:
        print('  ⚠️ B 跳过（无 H1）', p)
        continue
    title = m.group(1).strip()
    dm = DATE_PRE.match(os.path.basename(p)) or DATE_ANY.search(os.path.basename(p)) or DATE_ANY.search(p)
    date = dm.group(1) if dm else None
    fm = ['---', 'title: ' + q(title), 'type: 审计报告']
    if date:
        fm.append('date: ' + date)
    fm.append('---')
    B_jobs.append((p, '\n'.join(fm), '补FM+入库'))

# ---------- C: 11-模板/规范 无 FM ----------
for f in sorted(os.listdir('11-模板/规范')):
    if not f.endswith('.md'):
        continue
    p = '11-模板/规范/' + f
    if p in dirty:
        continue
    t = io.open(p, encoding='utf-8-sig', errors='replace').read()
    if re.match(r'^---[ \t]*\r?\n', t):
        continue
    m = H1.search(t)
    if not m:
        print('  ⚠️ C 跳过（无 H1）', p)
        continue
    C_jobs.append((p, '\n'.join(['---', 'title: ' + q(m.group(1).strip()), 'type: 规范', '---']), '补FM'))

print('=== A 非规范 type 归一 %d ===' % len(A_jobs))
for p, o, n in A_jobs:
    print('   %-58s %s → %s' % (p.replace('09-审计报告/', '')[:58], o.strip(), n.strip()))
print()
print('=== B 未跟踪补 FM 并入库 %d ===' % len(B_jobs))
for p, fm, _ in B_jobs:
    print('   %-64s %s' % (p.replace('09-审计报告/', '')[:64], fm.replace('\n', ' | ')[:70]))
print()
print('=== C 规范目录补 FM %d ===' % len(C_jobs))
for p, fm, _ in C_jobs:
    print('   %-50s %s' % (p[:50], fm.replace('\n', ' | ')))

if not APPLY:
    print()
    print('(dry-run；加 --apply 执行)')
    sys.exit(0)

bak = '.workbuddy/tmp/opt_pipe/_bak/mix_%s' % datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
done = 0
for p, old, new in A_jobs:
    t = io.open(p, encoding='utf-8-sig').read()
    m = re.match(r'^---[ \t]*\r?\n(.*?)\r?\n---', t, re.S)
    fm = m.group(1)
    assert fm.count(old) == 1, ('A', p)
    nfm = fm.replace(old, new)
    body = t[m.end():]
    assert body == t[m.end():]
    rel = p.replace('/', '__')
    os.makedirs(bak, exist_ok=True)
    shutil.copy2(p, os.path.join(bak, rel))
    io.open(p, 'w', encoding='utf-8', newline='').write('---\n' + nfm + '\n---' + body)
    done += 1
for p, fm, _ in B_jobs + C_jobs:
    t = io.open(p, encoding='utf-8-sig').read()
    new = fm + '\n\n' + t
    assert new[len(fm) + 2:] == t, ('B/C body', p)
    y.load('\n'.join(fm.split('\n')[1:-1]))
    assert new.count('\n') == t.count('\n') + len(fm.split('\n')) + 1, ('B/C lines', p)
    os.makedirs(bak, exist_ok=True)
    shutil.copy2(p, os.path.join(bak, p.replace('/', '__')))
    io.open(p, 'w', encoding='utf-8', newline='').write(new)
    done += 1
print('已写盘 %d 个（备份 %s，保留相对路径）' % (done, bak))
