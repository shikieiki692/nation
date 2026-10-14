# -*- coding: utf-8 -*-
r"""提交：P0 THIN 关闭 + 图升级线独立复核。"""
import os, subprocess, sys, time
ROOT = r'C:\Obsidion\妙妙屋'
PATHS = [
    '.workbuddy/tmp/opt_pipe/verify_upgrade_vs_vols.py',
    '.workbuddy/tmp/opt_pipe/write_p1b3.py',
    '00-首页/活跃任务/任务卡-2026-10-10-组卷线收尾.md',
    '09-审计报告/2026-10-14-卷X-XV图片排版核验.md',
    '00-首页/工作日志/2026-10-14.md',
    '.workbuddy/memory/2026-10-14.md',
]
MSG = ('docs(组卷线): 关闭 P0「细长条 THIN 6 处」＋ 独立复核并行会话图升级线无卷影响\n\n'
       '- P0 THIN 关闭：qa_vol_render 复测 XI 0 / XIp 0（XIp THIN −3）⇒ 原定「回源重裁」无需再做；\n'
       '  余 XVI 2 处为 informational（源切片属性，可追责 0）\n'
       '- 唯一余项：XIp 答案版 SMALL×1＝19.3×11.0mm（解包目检＝手写批注「状态量」，源仅 114×65px）\n'
       '  ＋ 1 张轨道图（170×176px）⇒ 属源图分辨率低，须走图升级/源 PDF 重裁\n'
       '- 独立复核：并行会话 93149975a 替换 314 图/186 卡，声称未被卷引用 ⇒\n'
       '  取清单 lib_img 与 X~XVII 九卷全部图引用求交，命中 0 ✓（两边不冲突）\n'
       '- 任务卡 P0① 细长条行更新为「已清零」')

def run(a):
    return subprocess.run(a, cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace')

r = run(['git', 'add', '-f', '--'] + PATHS)
if r.returncode != 0:
    print('add 失败'); print(r.stderr[-500:]); sys.exit(1)
st = [x for x in run(['git', '-c', 'core.quotepath=false', 'diff', '--cached', '--name-only']).stdout.strip().split('\n') if x]
if sorted(st) != sorted(PATHS):
    print('⚠️ staged 不符'); print(' 额外:', sorted(set(st) - set(PATHS))[:6]); print(' 缺失:', sorted(set(PATHS) - set(st))[:6]); sys.exit(2)
print('staged == PATHS (%d) ✓' % len(PATHS))
for i in range(5):
    r = run(['git', 'commit', '--only', '-m', MSG, '--'] + PATHS)
    if r.returncode == 0:
        print(r.stdout[-150:]); break
    if 'cannot lock ref' in (r.stderr or ''):
        time.sleep(1.5); continue
    print('commit 失败'); print(r.stdout[-400:]); print(r.stderr[-400:]); sys.exit(3)
else:
    sys.exit(3)
run(['git', 'reset', '-q', 'HEAD', '--'] + PATHS)
out = run(['git', '-c', 'core.quotepath=false', 'show', '--stat', 'HEAD']).stdout
bad = [l for l in out.split('\n') if 'delete mode' in l or '=>' in l]
print('\n'.join(out.strip().split('\n')[-4:]))
print('delete/rename 行:', bad if bad else '无 ✓')
