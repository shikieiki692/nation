# -*- coding: utf-8 -*-
"""隔离索引提交（不碰主索引，无竞态）。"""
import os, subprocess, sys, time, re

os.chdir(r'C:\Obsidion\妙妙屋')
T = '.workbuddy/tmp/opt_pipe/'
PATHS = [T + s for s in ['src_root_survey.py', 'src_health.py', 'trace_miss.py', 'vol_crosscheck.py',
                         'vol_claim_qa.py', 'edition_vs_src.py', 'vol_img_v2.py', 'vol_img_v3.py',
                         'deep_img10.py', 'img_audit_v4.py', 'write_check2.py', 'commit_check2.py']] + [
    '09-审计报告/2026-10-14-来源标注与图引用全库体检.md',
    '00-首页/工作日志/2026-10-14.md']
PATHS = [p for p in PATHS if os.path.exists(p)]

IDX = os.path.join(os.path.abspath('.git'), 'idx_check2_%d' % os.getpid())
env = dict(os.environ, GIT_INDEX_FILE=IDX)


def run(a, e=None):
    return subprocess.run(a, capture_output=True, text=True, encoding='utf-8', errors='replace', env=e)


r = run(['git', 'read-tree', 'HEAD'], env)
print('read-tree', r.returncode)
for i in range(0, len(PATHS), 80):
    r = run(['git', 'add', '-f', '--'] + PATHS[i:i + 80], env)
    if r.returncode:
        print('add fail', r.stderr[-300:]); sys.exit(2)
got = [x for x in run(['git', '-c', 'core.quotepath=false', 'diff', '--cached', '--name-only'], env).stdout.split('\n') if x]
if sorted(got) != sorted(PATHS):
    print('staged 不符:', sorted(set(got) ^ set(PATHS))[:8]); sys.exit(2)
print('staged == PATHS (%d) ✓' % len(PATHS))

MSG = ('docs(审计): 来源标注与图引用·全库体检 —— 六项全过，无内容缺陷\n\n'
       '- ① 各机构 source_file：仅 chemy 240 张缺失，系站点源合集(1~24)本地未存，已登记备查 ⇒ 非缺陷\n'
       '- ② 卷内来源机构 vs 卡目录：78 处 = 目录名 北斗40 ≠ 机构名「北斗学友」⇒ 非张冠李戴\n'
       '- ③ 跨卷重复用卡 0/252；④ 卷口径承诺（题数/机构数/难度<4=0/有机=0/满分）全兑现\n'
       '- ⑤ 「第N届」vs 源件：命中 2390 / 未见 0 ⇒ 届次标注全忠于源件\n'
       '- ⑥ 图引用体检：04-题库 12,334 md / 43,250 引用 ⇒ 真断链 0 / 畸形 0 / 扩展名错配 0\n'
       '- 三次自我更正（判据/正则假阳性）：未试 vault 根 / 未查登记表 / 正则把扩展名挤出捕获组')

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
print('主索引状态:', run(['git', 'status', '-sb']).stdout.split('\n')[0])
