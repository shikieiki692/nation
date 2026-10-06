# -*- coding: utf-8 -*-
"""方圆 FY-01 修复（第二版）：
 A) 还原误填：答案含 fy1_ 裁图、且 source 既非「有机化学测试题1」也非「有机化学试卷讲解1」→ 取 HEAD~1 答案区还原
 B) 补目标：source 含「有机化学试卷讲解1」的 6 张 → 按题号补裁图
用法：python fix_fy2.py [--apply]
"""
import subprocess, re, sys, os, glob

sys.stdout.reconfigure(encoding='utf-8')
os.chdir(r'C:\Obsidion\妙妙屋')
APPLY = '--apply' in sys.argv
OLD = '49d4821ce^'
IMG = '04-题库/2026机构初赛模拟题/方圆/images'


def g(a):
    return subprocess.run(['git'] + a, capture_output=True, text=True, encoding='utf-8', errors='replace').stdout


def rng(t):
    i = t.find('## 参考答案'); k = t.find('## 知识点映射')
    return (i, k) if i > 0 and k > i else (None, None)


def put(path, new):
    raw = open(path, 'rb').read()
    bom = raw[:3] == b'\xef\xbb\xbf'
    if APPLY:
        open(path, 'wb').write((b'\xef\xbb\xbf' if bom else b'') + new.encode('utf-8'))


cards = glob.glob('04-题库/2026机构初赛模拟题/方圆/题-*.md')
restored, filled = [], []
for p in cards:
    t = open(p, encoding='utf-8-sig').read().replace('\r\n', '\n')
    i, k = rng(t)
    if i is None:
        continue
    m = re.search(r'^source_file:[ \t]*(.*?)[ \t]*$', t, re.M)
    sf = m.group(1) if m else ''
    a = t[i:k]
    if 'fy1_' in a and '有机化学测试题1' not in sf and '有机化学试卷讲解1' not in sf:
        old = g(['show', OLD + ':' + p])
        oi, ok = rng(old) if old else (None, None)
        if oi is None:
            print('!! 取不到旧版', os.path.basename(p)); continue
        put(p, old[:oi] + old[oi:ok].rstrip('\n') + '\n' + old[ok:])
        restored.append(os.path.basename(p))
    elif '有机化学试卷讲解1' in sf:
        q = int(re.search(r'题-FY-01-(\d+)-', os.path.basename(p)).group(1))
        fs = sorted(glob.glob(os.path.join(IMG, 'fy1_FY-01-%02d_*.png' % q)))
        if not fs:
            print('!! 无裁图 FY-01-%02d' % q); continue
        md = ('（源：方圆《有机化学测试题1》参考答案 · 第 %d 题；按原册裁区，保留结构图与答案）\n\n' % q
              + '\n'.join('![](images/%s)' % os.path.basename(f) for f in fs)
              + '\n\n> 📌 据源答案册逐题裁区回填。\n')
        put(p, t[:i] + '## 参考答案\n\n' + md + '\n' + t[k:])
        filled.append((q, os.path.basename(p)))
print('A) 还原误填 %d 张：%s' % (len(restored), [x[:30] for x in restored]))
print('B) 补目标 %d 张：%s' % (len(filled), ['第%d题' % q for q, _ in filled]))
print('[%s]' % ('APPLY' if APPLY else 'DRY-RUN'))
