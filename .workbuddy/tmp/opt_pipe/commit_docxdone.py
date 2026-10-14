# -*- coding: utf-8 -*-
"""提交：6 卷答案版 docx 同步（隔离索引，显式清单，不带并行会话的 XII/XIII）。"""
import os, subprocess, sys, time, re

os.chdir(r'C:\Obsidion\妙妙屋')
D = '00-首页/题组Word/初赛模拟卷/真题版式/'
T = '.workbuddy/tmp/opt_pipe/'
PATHS = [D + '初赛模拟卷%s（非有机·答案与解析版·真题版式）.docx' % v
         for v in ['X', 'XI', 'XIp', 'XIV', 'XVI', 'XVII']] + [T + s for s in
         ['deploy_rebuild.py', 'verify_img_source.py', 'write_docxdone.py', 'commit_docxdone.py']] + [
    '09-审计报告/2026-10-14-卷族docx交付件与图源核查.md',
    '00-首页/工作日志/2026-10-14.md',
    '.workbuddy/memory/2026-10-14.md']


def run(a, e=None):
    return subprocess.run(a, capture_output=True, text=True, encoding='utf-8', errors='replace', env=e)


miss = [p for p in PATHS if not os.path.exists(p)]
if miss:
    print('缺文件:', miss); sys.exit(2)

IDX = os.path.join(os.path.abspath('.git'), 'idx_docxdone_%d' % os.getpid())
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

MSG = ('fix(交付): 6 卷答案版 docx 同步 —— 按「部署→重建→清理」流程（含来源渠道标）\n\n'
       '- 起因：本轮给 7 卷补「来源渠道标」后，6 卷答案版 docx 落后（XV 已由并行线重出）\n'
       '- 首次直接重出＝整卷丢图（XIp 80→11 / XVI 80→0 / XVII 56→5）⇒ 已回滚；\n'
       '  查证后确认：构建器只查 媒体仓库/（自 10-08 未改），新卷图在 04-题库/<机构>/images/ ⇒\n'
       '  流程缺「部署」步（与并行线「部署→重建」一致）；卷 X/XVII 现有 docx 图与库内图内容 100% 一致即证\n'
       '- 执行：部署 393 张 → 重建 6/6 → word/media 75/70/80/54/80/56 == 各卷 md 图引用数（全 ✅）\n'
       '  → docx 含新渠道标（X 3/XI 2/XIp 2/XVI 2/XVII 9 处「2026夏令营」；XIV 1 处「2026寒假班」）\n'
       '  → 卷 XVI 的 80 张图 100% 命中 04-题库/2026机构初赛模拟题/ → 清理部署（媒体仓库 git 无变更）\n'
       '- 建议：根治＝给 resolve_images 加多路径（否则每轮重出都要手工部署）')

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
