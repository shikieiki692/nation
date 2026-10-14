# -*- coding: utf-8 -*-
"""恢复被并行 stale-tree 回退的本会话文件（隔离索引，不碰主索引）"""
import os, subprocess, sys, time, re
os.chdir(r'C:\Obsidion\妙妙屋')
def run(a, env=None):
    return subprocess.run(a, capture_output=True, text=True, encoding='utf-8', errors='replace', env=env)

MINE = [x for x in run(['git', '-c', 'core.quotepath=false', 'show', '--name-only', '--format=', 'c591ad280']).stdout.split('\n') if x.strip()]
print('我的文件 =', len(MINE))
miss = [p for p in MINE if not os.path.exists(p)]
if miss:
    print('❌ 工作区缺文件:', miss); sys.exit(2)

IDX = os.path.join(os.getcwd(), '.git', 'idx_restore')
env = dict(os.environ, GIT_INDEX_FILE=IDX)
run(['git', 'read-tree', 'HEAD'], env=env)
for i in range(0, len(MINE), 120):
    run(['git', 'add', '-f', '--'] + MINE[i:i+120], env=env)
got = [x for x in run(['git', '-c', 'core.quotepath=false', 'diff', '--cached', '--name-only'], env=env).stdout.split('\n') if x.strip()]
if sorted(got) != sorted(MINE):
    print('❌ staged 不符', sorted(set(got) ^ set(MINE))[:8]); sys.exit(2)
print('staged == MINE (%d) ✓' % len(MINE))

MSG = ('fix(首页): 恢复被并行提交 stale-tree 回退的 type 收口（仅补回本会话文件）\n\n'
       '- 事故：并行会话 f36f2450d／576da4929 基于陈旧树提交，把 c591ad280 的 100 文件全数回退（含 00-首页 92 文件 type 收口、本报告）\n'
       '- 处置：隔离索引 read-tree HEAD + 仅 add 本会话 100 文件 → 单独 fixup commit；**未碰并行会话暂存项**\n'
       '- 内容一字未改，仅把已确认的 type 收口恢复回 HEAD')
for i in range(6):
    r = run(['git', 'commit', '-m', MSG], env=env)
    if r.returncode == 0:
        print(r.stdout[-140:]); break
    if 'cannot lock ref' in (r.stderr or ''):
        time.sleep(1.5); continue
    print('❌ commit FAIL'); print((r.stdout + r.stderr)[-900:]); sys.exit(1)
os.remove(IDX)
# 不动主索引
print('=== 复核：新 HEAD 相对 c591ad280 只应含「并行新增」，不含我的回退 ===')
d = run(['git', '-c', 'core.quotepath=false', 'diff', '--name-status', 'c591ad280', 'HEAD']).stdout
lines = [l for l in d.split('\n') if l.strip()]
print('   总差异文件 =', len(lines))
mine_back = [l for l in lines if l[2:].strip().strip('"') in MINE]
print('   其中「我的文件」仍被回退 =', len(mine_back), '(应为 0)')
for l in mine_back[:5]:
    print('     ', l[:90])
print('--- 非我差异（并行新增，保留）---')
for l in lines[:8]:
    print('   ', l[:90])
