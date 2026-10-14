# -*- coding: utf-8 -*-
"""① role 补全 ＋ ② 无 FM 补建：按族映射 + dry/apply"""
import io, os, re, sys, shutil, datetime, subprocess
os.chdir(r'C:\Obsidion\妙妙屋')
APPLY = '--apply' in sys.argv
from ruamel.yaml import YAML
y = YAML(typ='safe')

def rd(p): return io.open(p, encoding='utf-8-sig').read()
def getfm(t):
    m = re.match(r'^---\r?\n(.*?)\r?\n---(\r?\n|$)', t, re.S)
    return (m.group(1), t[m.end():], m) if m else (None, t, None)
def h1of(body):
    for l in body.split('\n'):
        if l.startswith('# '):
            return l[2:].strip()
    return ''

def role_for(rel):
    b = os.path.basename(rel)
    if '/会话交接/' in rel: return '会话交接'
    if b.startswith(('交接提示词-', '【直接复制】新会话提示词', '核验提示词-', '新会话启动提示词')): return '启动提示词'
    if b.startswith(('计划-', '习题书V2')): return '治理规划'
    if b.startswith(('任务总览-', '待办清单-')): return '执行聚合'
    if b == 'README.md' or b.startswith(('图片剩余待手绘清单', 'KP复习清单')) or '现状总览' in b: return '资源索引'
    if b.startswith('图片核验任务包'): return '任务调度参考'
    if b.startswith('经验沉淀'): return '维护备忘'
    if 'Word友好' in b: return '速查卡'
    return None

# 并行脏（不碰）
st = subprocess.run(['git', '-c', 'core.quotepath=false', 'status', '--short'],
                    capture_output=True, text=True, encoding='utf-8').stdout
PARALLEL = set(l[3:].strip().strip('"') for l in st.split('\n') if l.strip() and '00-首页' in l)

ADDROLE, ADDFM, UNCLASS = [], [], []
for dp, dn, fn in os.walk('00-首页'):
    if '.git' in dp or '归档' in dp or '_archive' in dp:
        continue
    for f in sorted(fn):
        if not f.endswith('.md'):
            continue
        p = os.path.join(dp, f).replace('\\', '/')
        if p in PARALLEL:
            continue
        t = rd(p)
        s, body, m = getfm(t)
        r = role_for(p)
        if s is None:
            tgt = '工作日志' if '/工作日志/' in p else '系统'
            ADDFM.append((p, h1of(body) or f[:-3], tgt, r if tgt == '系统' else None))
        else:
            d = y.load(s) or {}
            if d.get('type') == '系统' and not d.get('role'):
                if r: ADDROLE.append((p, r))
                else: UNCLASS.append(p)

print('=== ① 补 role：%d 个 ===' % len(ADDROLE))
for p, r in ADDROLE: print('   %-56s → %s' % (p.replace('00-首页/', '')[:56], r))
print()
print('=== ② 补 FM：%d 个 ===' % len(ADDFM))
for p, ti, ty, r in ADDFM: print('   %-56s type=%s role=%s' % (p.replace('00-首页/', '')[:56], ty, r))
print()
print('=== 无法归类（需另判，%d）===' % len(UNCLASS))
for p in UNCLASS: print('   ', p)
if not APPLY:
    print('\n（dry-run，未写盘）'); sys.exit(0)

bak = '.workbuddy/tmp/opt_pipe/_bak/rolefm_%s' % datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
os.makedirs(bak, exist_ok=True); n = 0
for p, r in ADDROLE:
    shutil.copy2(p, os.path.join(bak, os.path.basename(p)))
    t = rd(p); s, body, m = getfm(t)
    nl = '\r\n' if '\r\n' in t[:m.end()] else '\n'
    ns = s + nl + 'role: ' + r
    io.open(p, 'w', encoding='utf-8', newline='').write('---' + nl + ns + nl + '---' + nl + body); n += 1
for p, ti, ty, r in ADDFM:
    shutil.copy2(p, os.path.join(bak, os.path.basename(p)))
    t = rd(p); s, body, m = getfm(t)
    nl = '\r\n' if '\r\n' in t[:200] else '\n'
    lines = ['title: ' + ti, 'type: ' + ty]
    if r: lines.append('role: ' + r)
    fm = nl.join(lines)
    io.open(p, 'w', encoding='utf-8', newline='').write('---' + nl + fm + nl + '---' + nl + nl + body); n += 1
print('已写盘 %d（备份 %s）' % (n, bak))
