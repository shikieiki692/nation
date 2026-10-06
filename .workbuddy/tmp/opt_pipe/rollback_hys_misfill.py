# -*- coding: utf-8 -*-
"""紧急回滚：撤销对「非 有机专题1」卡的误写（我的 glob 因 ID 撞车命中多卡）。
保留：source_file 含「有机专题1」的卡；其余 `git checkout HEAD -- <path>` 还原。
"""
import subprocess, sys, os, re

sys.stdout.reconfigure(encoding='utf-8')
os.chdir(r'C:\Obsidion\妙妙屋')


def git(args):
    return subprocess.run(['git'] + args, capture_output=True, text=True,
                          encoding='utf-8', errors='replace')


changed = [x for x in git(['diff', '--name-only', '-z']).stdout.split('\0') if x]
targets = [p for p in changed if '04-题库/2026机构初赛模拟题/化英社/' in p.replace('\\', '/')]
print('化英社已改 %d' % len(targets))
keep, revert = [], []
for p in targets:
    t = open(p, encoding='utf-8-sig').read()
    m = re.search(r'^source_file:[ \t]*(.*?)[ \t]*$', t, re.M)
    sf = m.group(1) if m else ''
    (keep if '有机专题1' in sf else revert).append(p)
print('保留 %d ；回滚 %d' % (len(keep), len(revert)))
for p in keep:
    print('  KEEP  ', os.path.basename(p))
if revert:
    r = git(['checkout', 'HEAD', '--'] + revert)
    print('checkout rc=%d %s' % (r.returncode, r.stderr[-200:]))
left = [x for x in git(['diff', '--name-only', '-z']).stdout.split('\0')
        if x and '04-题库/2026机构初赛模拟题/化英社/' in x.replace('\\', '/')]
print('回滚后化英社仍改 %d（应=保留数）' % len(left))
