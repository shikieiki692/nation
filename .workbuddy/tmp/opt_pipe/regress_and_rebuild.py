# -*- coding: utf-8 -*-
"""① 老卷回归（I，图在媒体仓库，应不受影响）；② 用新构建器统一重出 6 卷并校验。"""
import io, os, re, glob, shutil, zipfile, subprocess, time

os.chdir(r'C:\Obsidion\妙妙屋')
PY = r'C:\Users\蕾赛\AppData\Local\Programs\Python\Python312\python.exe'
BUILDER = '.workbuddy/scripts/build_chusai_zhenti_layout.py'
D = '00-首页/题组Word/初赛模拟卷/真题版式'
MEDIA = '媒体仓库'


def run(a):
    return subprocess.run(a, capture_output=True, text=True, encoding='utf-8', errors='replace')


def refs(v):
    t = io.open('04-题库/初赛模拟卷%s（非有机·答案版）.md' % v, encoding='utf-8-sig').read()
    return [os.path.basename(x) for x in re.findall(r'!\[\[([^\]|]+?\.(?:jpg|jpeg|png))', t, re.I)]


# ---------- ① 老卷回归 ----------
before = set(os.listdir(D))
med_b = len(os.listdir(MEDIA))
r = run([PY, '-X', 'utf8', BUILDER, '--answer', 'I'])
out = (r.stdout or '') + (r.stderr or '')
dxI = os.path.join(D, '初赛模拟卷I（非有机·答案与解析版·真题版式）.docx')
mi = len([x for x in zipfile.ZipFile(dxI).namelist() if x.startswith('word/media/')]) if os.path.exists(dxI) else -1
print('【老卷回归】卷 I rc=%d ｜ [缺图]=%d ｜ media=%d ｜ 引用=%d ｜ 媒体仓库 %d→%d'
      % (r.returncode, len(re.findall(r'\[缺图\]', out)), mi, len(refs('I')), med_b, len(os.listdir(MEDIA))))
# 删除老卷在本目录的产物（恢复原状：本目录不该有 I~IX）
for f in os.listdir(D):
    if f not in before and re.match(r'初赛模拟卷(I|II|III|IV|V|VI|VII|VIII|IX)（', f):
        os.remove(os.path.join(D, f)); print('  已删除回归产物:', f[:40])
print('  回归后目录文件数:', len(os.listdir(D)), '(应 =', len(before), ')')

# ---------- ② 重出 6 卷 ----------
VOLS = ['X', 'XI', 'XIp', 'XIV', 'XVI', 'XVII']
t0 = time.time()
r = run([PY, '-X', 'utf8', BUILDER, '--answer'] + VOLS)
out = (r.stdout or '') + (r.stderr or '')
print('\n【6 卷重出】rc=%d 耗时 %.0fs ｜ [缺图]=%d' % (r.returncode, time.time() - t0, len(re.findall(r'\[缺图\]', out))))
print('  媒体仓库 %d → %d（应不变）' % (med_b, len(os.listdir(MEDIA))))
bad = []
for v in VOLS:
    dx = os.path.join(D, '初赛模拟卷%s（非有机·答案与解析版·真题版式）.docx' % v)
    m = len([x for x in zipfile.ZipFile(dx).namelist() if x.startswith('word/media/')])
    e = len(refs(v))
    if m != e:
        bad.append((v, m, e))
    print('  卷%-5s media=%-3d 引用=%-3d %s' % (v, m, e, '✅' if m == e else '🔴'))
print('  校验失败:', bad if bad else '无')
