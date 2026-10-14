# -*- coding: utf-8 -*-
"""提交：卷族 docx 交付件与图源核查（隔离索引，只提交真有差异的路径）。"""
import os, subprocess, sys, time, re

os.chdir(r'C:\Obsidion\妙妙屋')
T = '.workbuddy/tmp/opt_pipe/'
CAND = [T + s for s in ['docx_inventory.py', 'img_loc16.py', 'write_docxchk.py', 'commit_docxchk.py']] + [
    '09-审计报告/2026-10-14-卷族docx交付件与图源核查.md',
    '00-首页/活跃任务/任务卡-2026-10-10-组卷线收尾.md',
    '00-首页/工作日志/2026-10-14.md',
    '.workbuddy/memory/2026-10-14.md',
]


def run(a, e=None):
    return subprocess.run(a, capture_output=True, text=True, encoding='utf-8', errors='replace', env=e)


PATHS = []
for p in CAND:
    if not os.path.exists(p):
        print('  跳过(不存在):', p); continue
    tracked = run(['git', 'ls-files', '--error-unmatch', p]).returncode == 0
    diff = run(['git', 'diff', '--name-only', 'HEAD', '--', p]).stdout.strip()
    if tracked and not diff:
        print('  跳过(无差异):', p); continue
    PATHS.append(p)
print('待提交 %d 个' % len(PATHS))

IDX = os.path.join(os.path.abspath('.git'), 'idx_docxchk_%d' % os.getpid())
env = dict(os.environ, GIT_INDEX_FILE=IDX)
run(['git', 'read-tree', 'HEAD'], env)
for i in range(0, len(PATHS), 80):
    r = run(['git', 'add', '-f', '--'] + PATHS[i:i + 80], env)
    if r.returncode:
        print('add fail', r.stderr[-300:]); sys.exit(2)
got = [x for x in run(['git', '-c', 'core.quotepath=false', 'diff', '--cached', '--name-only'], env).stdout.split('\n') if x]
if sorted(got) != sorted(PATHS):
    print('staged 不符:', sorted(set(got) ^ set(PATHS))[:8]); sys.exit(2)
print('staged == PATHS (%d) ✓' % len(PATHS))

MSG = ('docs(审计): 卷族 docx 交付件与图源核查 —— 发现「按当前构建器重出＝整卷丢图」（已回滚）\n\n'
       '- 盘点：真题版式目录 27 docx（X~XVII ＋ XIp，9 卷×3 版）＋ 老卷目录 27，齐全；\n'
       '  6 卷答案版落后于 md（X/XI/XIp/XIV/XVI/XVII，本轮补来源渠道标所致）；XV 已由并行线重出；\n'
       '  学生版/答题卡不含来源行 ⇒ 无需重出\n'
       '- 🔴 重出实验：word/media XIp 80→11、XVI 80→0、XVII 56→5 ⇒ 整卷丢图 ⇒ 已从备份回滚（复原 80/80/56）\n'
       '- 根因：build_chusai_zhenti_layout.py::resolve_images() 只查 媒体仓库/，无 fallback；\n'
       '  新卷图全在 04-题库/2026机构初赛模拟题/<机构>/images/（媒体仓库命中 0~11/80）；\n'
       '  老卷（I~IX）图在媒体仓库（命中 100%）⇒ 只有老卷可重建\n'
       '- 处置：未擅自重出（跨线工具 ＋ 共享目录），已登记任务卡 ⑨ 并给出 A/B/C 三方案\n'
       '- 判据：重出 docx 前必验「媒体数守恒」；脚本报「完成 N/N」≠ 产物正确')

for i in range(5):
    r = run(['git', 'commit', '-m', MSG], env)
    if r.returncode == 0:
        print(r.stdout[-150:]); break
    if 'cannot lock ref' in (r.stderr or ''):
        time.sleep(1.5); continue
    print('FAIL'); print((r.stdout + r.stderr)[-700:]); sys.exit(1)

if os.path.exists(IDX):
    os.remove(IDX)
o = run(['git', '-c', 'core.quotepath=false', 'show', '--stat', 'HEAD']).stdout
print(re.findall(r'\d+ files? changed.*', o))
print(run(['git', 'log', '-1', '--format=%h %s']).stdout.strip())
print('主索引暂存数:', run(['git', 'diff', '--cached', '--name-only']).stdout.count('\n'))
