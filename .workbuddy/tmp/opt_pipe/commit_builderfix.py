# -*- coding: utf-8 -*-
"""提交：构建器根治（多路径＋自动 staging）＋ 6 卷 docx 统一重出。"""
import os, subprocess, sys, time, re

os.chdir(r'C:\Obsidion\妙妙屋')
D = '00-首页/题组Word/初赛模拟卷/真题版式/'
T = '.workbuddy/tmp/opt_pipe/'
PATHS = ['.workbuddy/scripts/build_chusai_zhenti_layout.py'] + [
    D + '初赛模拟卷%s（非有机·答案与解析版·真题版式）.docx' % v for v in
    ['X', 'XI', 'XIp', 'XIV', 'XVI', 'XVII']] + [T + s for s in
    ['test_builder_fix.py', 'regress_and_rebuild.py', 'write_builderfix.py', 'commit_builderfix.py']] + [
    '09-审计报告/2026-10-14-卷族docx交付件与图源核查.md',
    '00-首页/工作日志/2026-10-14.md',
    '.workbuddy/memory/2026-10-14.md']


def run(a, e=None):
    return subprocess.run(a, capture_output=True, text=True, encoding='utf-8', errors='replace', env=e)


miss = [p for p in PATHS if not os.path.exists(p)]
if miss:
    print('缺文件:', miss); sys.exit(2)

IDX = os.path.join(os.path.abspath('.git'), 'idx_bfix_%d' % os.getpid())
env = dict(os.environ, GIT_INDEX_FILE=IDX)
run(['git', 'read-tree', 'HEAD'], env)
for i in range(0, len(PATHS), 80):
    r = run(['git', 'add', '-f', '--'] + PATHS[i:i + 80], env)
    if r.returncode:
        print('add fail', r.stderr[-400:]); sys.exit(2)
got = [x for x in run(['git', '-c', 'core.quotepath=false', 'diff', '--cached', '--name-only'], env).stdout.split('\n') if x]
if sorted(got) != sorted(PATHS):
    print('staged 不符:', sorted(set(got) ^ set(PATHS))[:8]); sys.exit(2)
print('staged == PATHS (%d) ✓' % len(PATHS))

MSG = ('fix(组卷): 构建器图片多路径解析＋自动 staging —— 根治「重出丢图」\n\n'
       '- 根因：resolve_images() 只查 媒体仓库/，而新卷图全在 04-题库/2026机构初赛模拟题/<机构>/images/\n'
       '  ⇒ 直接重建整卷丢图（实测 XIp 80→11 / XVI 80→0 / XVII 56→5）\n'
       '- 改法（44 insertions / 3 deletions，向后兼容）：\n'
       '  ① 新增 STAGE_IMG 暂存目录；② 新增 img_index() 全库图片名索引（一次性，排除 .git/.workbuddy）\n'
       '  ③ resolve_images 查找顺序 媒体仓库/ → 全库索引，命中即自动 staging 复制\n'
       '  ④ --resource-path 加第二根 {MEDIA}{os.pathsep}{STAGE_IMG}；⑤ main() 开头 rmtree 清 staging\n'
       '- 验证：py_compile OK；新卷单卷( XVI )[缺图]=0、media 80/80、媒体仓库零写入；\n'
       '  老卷回归( I )[缺图]=0、media 10/10、媒体仓库零写入 ⇒ 老卷行为不变；\n'
       '  6 卷统一重出 rc=0/24s/[缺图]=0/75-70-80-54-80-56 全守恒/媒体仓库零写入\n'
       '- ⇒ 新卷重建不再需要手工部署图片（原方案 B 退居备用）')

for i in range(5):
    r = run(['git', 'commit', '-m', MSG], env)
    if r.returncode == 0:
        print(r.stdout[-150:]); break
    if 'cannot lock ref' in (r.stderr or ''):
        time.sleep(1.5); continue
    print('FAIL'); print((r.stdout + r.stderr)[-800:]); sys.exit(1)

if os.path.exists(IDX):
    os.remove(IDX)
o = run(['git', '-c', 'core.quotepath=false', 'show', '--stat', 'HEAD']).stdout
print(re.findall(r'\d+ files? changed.*', o))
print(run(['git', 'log', '-1', '--format=%h %s']).stdout.strip())
print('暂存残留:', run(['git', 'diff', '--cached', '--name-only']).stdout.count('\n'))
