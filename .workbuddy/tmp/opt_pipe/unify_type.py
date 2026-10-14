# -*- coding: utf-8 -*-
"""00-首页 type 归一（→ 系统/活跃任务卡/工作日志）dry/apply"""
import io, os, re, shutil, datetime, sys, subprocess
os.chdir(r'C:\Obsidion\妙妙屋')
APPLY = '--apply' in sys.argv
ROOT = '00-首页'
OK = {'系统', '活跃任务卡', '工作日志'}
SKIP_PART = ('/归档/', '\\归档\\', '/_archive/', '\\_archive\\')

# 并行脏文件（不碰）
st = subprocess.run(['git', '-c', 'core.quotepath=false', 'status', '--short'],
                    capture_output=True, text=True, encoding='utf-8').stdout
PARALLEL = set()
for ln in st.split('\n'):
    if ln.strip() and ROOT in ln:
        PARALLEL.add(ln[3:].strip().strip('"'))

def target_for(rel, cur):
    if rel.startswith('00-首页/工作日志/'):
        return '工作日志'
    return '活跃任务卡' if cur == '活跃任务卡' else '系统'

todos, nofm, skipped = [], [], []
for dp, dn, fn in os.walk(ROOT):
    if '.git' in dp:
        continue
    for f in sorted(fn):
        if not f.endswith('.md'):
            continue
        p = os.path.join(dp, f)
        rel = p.replace('\\', '/')
        if any(part in p.replace('/', '\\') for part in ('\\归档\\', '\\_archive\\')):
            continue
        t = io.open(p, encoding='utf-8-sig').read()
        m = re.match(r'^---\r?\n(.*?)\r?\n---(\r?\n|$)', t, re.S)
        if not m:
            nofm.append(rel)
            continue
        fmtext = m.group(1)
        mm = re.search(r'^type:[ \t]*(.*)$', fmtext, re.M)
        cur = mm.group(1).strip().strip('"').strip("'") if mm else None
        if cur in OK and cur == target_for(rel, cur):
            continue
        tgt = target_for(rel, cur)
        if cur == tgt:
            continue
        if rel in PARALLEL:
            skipped.append((rel, cur, tgt)); continue
        todos.append((rel, cur, tgt))

print('=== 待改 %d 个文件 ===' % len(todos))
from collections import Counter
print('   按目标:', dict(Counter(t[2] for t in todos)))
print('   按原值:', dict(Counter(t[1] for t in todos)))
print()
for rel, cur, tgt in todos:
    print('   %-56s %s → %s' % (rel.replace('00-首页/', '')[:56], cur, tgt))
print()
print('=== 跳过（并行脏，%d）===' % len(skipped))
for rel, cur, tgt in skipped:
    print('   %s (%s→%s)' % (rel, cur, tgt))
print()
print('=== 无 frontmatter（%d，另案）===' % len(nofm))
for rel in nofm:
    print('   ', rel)

if not APPLY:
    print()
    print('（dry-run，未写盘；加 --apply 执行）')
    sys.exit(0)

# ---- apply ----
bak = '.workbuddy/tmp/opt_pipe/_bak/type_%s' % datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
os.makedirs(bak, exist_ok=True)
done = 0
for rel, cur, tgt in todos:
    dst = os.path.join(bak, os.path.basename(rel))
    shutil.copy2(rel, dst)
    t = io.open(rel, encoding='utf-8-sig').read()
    m = re.match(r'^---\r?\n(.*?)\r?\n---(\r?\n|$)', t, re.S)
    fmtext = m.group(1)
    nl = '\r\n' if '\r\n' in t[:m.end()] else '\n'
    body = t[m.end():]
    if re.search(r'^type:[ \t]*.*$', fmtext, re.M):
        nfm = re.sub(r'^type:[ \t]*.*$', 'type: ' + tgt, fmtext, count=1, flags=re.M)
    else:
        # 插到 title 之后，否则最前
        if re.search(r'^title:[ \t]*.*$', fmtext, re.M):
            nfm = re.sub(r'^(title:[ \t]*.*)$', r'\1' + nl + 'type: ' + tgt, fmtext, count=1, flags=re.M)
        else:
            nfm = 'type: ' + tgt + nl + fmtext
    out = '---' + nl + nfm + nl + '---' + nl + body
    io.open(rel, 'w', encoding='utf-8', newline='').write(out)
    done += 1
print()
print('已写盘 %d 个（备份于 %s）' % (done, bak))
