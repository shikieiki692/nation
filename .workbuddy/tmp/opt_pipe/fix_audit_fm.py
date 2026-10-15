# -*- coding: utf-8 -*-
"""给 09-审计报告 的历史报告批量补 frontmatter（title + type + date）

护栏：
  - 只处理「已跟踪 + 非归档 + 非并行领地 + 非工作区脏 + 无 FM」的 md
  - 只在文件**最前面**插入 FM，**正文逐字不动**（断言）
  - 第一行非 `#`／非空的跳过并报告
  - 幂等（已插 FM 的不会再匹配）
"""
import io, os, re, subprocess, sys, shutil, datetime
os.chdir(r'C:\Obsidion\妙妙屋')
from ruamel.yaml import YAML

APPLY = '--apply' in sys.argv
D = '09-审计报告'
EXCLUDE_SUBSTR = ('chemy', '图升级线', '图线')

st = subprocess.run(['git', '-c', 'core.quotepath=false', 'status', '--short', '--untracked-files=all', D],
                    capture_output=True, text=True, encoding='utf-8').stdout
untracked = {ln[3:].strip().strip('"') for ln in st.split('\n') if ln.startswith('?? ')}
dirty = {ln[3:].strip().strip('"') for ln in st.split('\n') if ln.strip() and not ln.startswith('?? ')}

DATE_PRE = re.compile(r'^(\d{4}-\d{2}-\d{2})-')
DATE_ANY = re.compile(r'(\d{4}-\d{2}-\d{2})')
H1 = re.compile(r'^#[ \t]+(\S.*?)[ \t]*$', re.M)


def q(s):
    """YAML 单引号包裹（内部单引号翻倍）"""
    return "'" + s.replace("'", "''") + "'"


jobs = []      # (path, fm_text)
skipped = []
for dp, dn, fn in os.walk(D):
    dn[:] = [x for x in dn if not (x.startswith('_归档') or x.startswith('_archive') or x == '归档')]
    for f in sorted(fn):
        if not f.endswith('.md'):
            continue
        p = os.path.join(dp, f).replace('\\', '/')
        if p in untracked or p in dirty:
            continue
        if any(s in p for s in EXCLUDE_SUBSTR):
            continue
        t = io.open(p, encoding='utf-8-sig', errors='replace').read()
        if re.match(r'^---[ \t]*\r?\n', t):
            continue
        first = t.split('\n')[0].strip()
        if not first.startswith('#'):
            skipped.append((p, '首行非标题: ' + first[:40]))
            continue
        m = H1.search(t)
        if not m:
            skipped.append((p, '无 H1'))
            continue
        title = m.group(1).strip()
        # 日期提取：① 文件名前缀 ② 文件名内嵌 ③ 路径内嵌 ④ 正文前 15 行
        dm = DATE_PRE.match(os.path.basename(p)) or DATE_ANY.search(os.path.basename(p))
        date = dm.group(1) if dm else None
        if not date:
            dm2 = DATE_ANY.search(p)
            date = dm2.group(1) if dm2 else None
        if not date:
            for ln in t.split('\n')[:15]:
                dm3 = DATE_ANY.search(ln)
                if dm3:
                    date = dm3.group(1)
                    break
        fm = ['---', 'title: ' + q(title), 'type: 审计报告']
        if date:
            fm.append('date: ' + date)
        fm.append('---')
        jobs.append((p, '\n'.join(fm)))

print('=== 待补 FM %d 个 ===' % len(jobs))
for p, fm in jobs[:12]:
    print('  ◆ %s' % p.replace(D + '/', '')[:80])
    print('     %s' % fm.replace('\n', ' | ')[:110])
if len(jobs) > 12:
    print('  …（另 %d 个）' % (len(jobs) - 12))
print()
print('跳过 %d 个：' % len(skipped))
for p, why in skipped[:10]:
    print('  ⚠️ %s  ← %s' % (p.replace(D + '/', '')[:66], why))
no_date = [p for p, fm in jobs if 'date:' not in fm]
print()
print('其中无日期可提取 = %d' % len(no_date))
for p in no_date[:8]:
    print('   ', p.replace(D + '/', '')[:80])

if not APPLY:
    print()
    print('(dry-run；加 --apply 执行)')
    sys.exit(0)

bak = '.workbuddy/tmp/opt_pipe/_bak/auditfm_%s' % datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
os.makedirs(bak, exist_ok=True)
y = YAML(typ='safe', pure=True); y.version = (1, 2); y.allow_duplicate_keys = False
done = 0
for p, fm in jobs:
    t = io.open(p, encoding='utf-8-sig').read()
    new = fm + '\n\n' + t
    # 断言①：正文逐字未变
    assert new[len(fm) + 2:] == t, p
    # 断言②：FM 严格解析通过（fm 是含首尾 --- 的完整字符串）
    y.load('\n'.join(fm.split('\n')[1:-1]))
    # 断言③：行数增量 = FM 行数 + 1（空行）
    assert new.count('\n') == t.count('\n') + len(fm.split('\n')) + 1, p
    assert new.startswith(fm + '\n\n'), p
    shutil.copy2(p, os.path.join(bak, os.path.basename(p)))
    io.open(p, 'w', encoding='utf-8', newline='').write(new)
    done += 1
print('已写盘 %d 个（备份 %s）' % (done, bak))
