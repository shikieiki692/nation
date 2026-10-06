# -*- coding: utf-8 -*-
"""修复方圆 FY-01 误操作：
 A) 误填卡（有 fy1_ 裁图但 source ≠ 有机化学试卷讲解1）→ 答案区还原为 49d4821ce^ 版
 B) 目标卡（source = 有机化学试卷讲解1 的 6 张）→ 按题号补正确裁图
用法：python fix_fy.py [--apply]
"""
import subprocess, re, sys, os, glob

sys.stdout.reconfigure(encoding='utf-8')
os.chdir(r'C:\Obsidion\妙妙屋')
APPLY = '--apply' in sys.argv
BASE = '49d4821ce^'
IMG = '04-题库/2026机构初赛模拟题/方圆/images'


def g(a):
    return subprocess.run(['git'] + a, capture_output=True, text=True, encoding='utf-8', errors='replace').stdout


def ans_range(t):
    i = t.find('## 参考答案'); k = t.find('## 知识点映射')
    return (i, k) if i > 0 and k > i else (None, None)


def write(card, md):
    raw = open(card, 'rb').read()
    bom = raw[:3] == b'\xef\xbb\xbf'
    t = raw.decode('utf-8-sig').replace('\r\n', '\n')
    i, k = ans_range(t)
    new = t[:i] + '## 参考答案\n\n' + md + '\n' + t[k:]
    if APPLY:
        open(card, 'wb').write((b'\xef\xbb\xbf' if bom else b'') + new.encode('utf-8'))


cards = glob.glob('04/../04-题库/2026机构初赛模拟题/方圆/题-*.md')
cards = glob.glob('04-题库/2026机构初赛模拟题/方圆/题-*.md')
restored, filled = [], []
for p in cards:
    t = open(p, encoding='utf-8-sig').read().replace('\r\n', '\n')
    i, k = ans_range(t)
    if i is None:
        continue
    a = t[i:k]
    m = re.search(r'^source_file:[ \t]*(.*?)[ \t]*$', t, re.M)
    sf = m.group(1) if m else ''
    if 'fy1_' in a and '有机化学试卷讲解1' not in sf:
        old = g(['show', BASE + ':' + p])
        if old:
            oi, ok = ans_range(old)
            if oi is not None:
                new = old[:oi] + old[oi:ok].rstrip('\n') + '\n' + old[ok:]
                if APPLY:
                    raw = open(p, 'rb').read()
                    bom = raw[:3] == b'\xef\xbb\xbf'
                    open(p, 'wb').write((b'\xef\xbb\xbf' if bom else b'') + new.encode('utf-8'))
                restored.append(os.path.basename(p))
print('A) 还原误填 %d 张' % len(restored))
for x in restored:
    print('   ', x[:50])

# B) 目标卡
for p in cards:
    t = open(p, encoding='utf-8-sig').read().replace('\r\n', '\n')
    m = re.search(r'^source_file:[ \t]*(.*?)[ \t]*$', t, re.M)
    if not m or '有机化学试卷讲解1' not in m.group(1):
        continue
    mid = re.search(r'题-FY-01-(\d+)-', os.path.basename(p))
    q = int(mid.group(1)) if mid else 0
    fs = sorted(glob.glob(os.path.join(IMG, 'fy1_FY-01-%02d_*.png' % q)))
    if not fs:
        print('!! 无裁图 FY-01-%02d' % q); continue
    md = ('（源：方圆《有机化学测试题1》参考答案 · 第 %d 题；按原册裁区，保留结构图与答案）\n\n' % q
          + '\n'.join('![](images/%s)' % os.path.basename(f) for f in fs)
          + '\n\n> 📌 据源答案册逐题裁区回填。\n')
    write(p, md)
    filled.append((q, os.path.basename(p)))
print('B) 回填目标卡 %d 张' % len(filled))
for q, x in filled:
    print('   第%d题 %s' % (q, x[:46]))
print('[%s]' % ('APPLY' if APPLY else 'DRY-RUN'))
