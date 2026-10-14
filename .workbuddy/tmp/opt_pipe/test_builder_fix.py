# -*- coding: utf-8 -*-
"""测试改动后的构建器：无需手工部署即可取到新卷图。"""
import io, os, re, sys, glob, shutil, zipfile, subprocess, time

os.chdir(r'C:\Obsidion\妙妙屋')
PY = r'C:\Users\蕾赛\AppData\Local\Programs\Python\Python312\python.exe'
BUILDER = '.workbuddy/scripts/build_chusai_zhenti_layout.py'
STAGE = '.workbuddy/tmp/chusai_zhenti/imgstage'
MEDIA = '媒体仓库'
D = '00-首页/题组Word/初赛模拟卷/真题版式'

# 1) 语法
r = subprocess.run([PY, '-m', 'py_compile', BUILDER], capture_output=True, text=True, encoding='utf-8', errors='replace')
print('py_compile rc=%d %s' % (r.returncode, r.stderr[-300:] if r.returncode else 'OK'))
if r.returncode:
    sys.exit(1)

# 2) 清 staging
if os.path.isdir(STAGE):
    shutil.rmtree(STAGE)
print('已清 staging')

# 3) 前置：媒体仓库里确认没有 XVI 的图（证明"无需部署"）
med = set(os.listdir(MEDIA))
t = io.open('04-题库/初赛模拟卷XVI（非有机·答案版）.md', encoding='utf-8-sig').read()
refs = [os.path.basename(x) for x in re.findall(r'!\[\[([^\]|]+?\.(?:jpg|jpeg|png))', t, re.I)]
print('卷 XVI 图引用 %d ｜ 媒体仓库已含 %d（应为 0）' % (len(refs), sum(1 for x in refs if x in med)))
med_before = len(os.listdir(MEDIA))

# 4) 构建
t0 = time.time()
r = subprocess.run([PY, '-X', 'utf8', BUILDER, '--answer', 'XVI'], capture_output=True, text=True, encoding='utf-8', errors='replace')
el = time.time() - t0
out = (r.stdout or '') + (r.stderr or '')
miss = len(re.findall(r'\[缺图\]', out))
print('构建 rc=%d 耗时 %.0fs ｜ [缺图] 行数=%d' % (r.returncode, el, miss))
for l in [x for x in out.split('\n') if 'OK' in x or 'FAIL' in x][:3]:
    print('   ', l.strip()[:160])

# 5) 校验
dx = os.path.join(D, '初赛模拟卷XVI（非有机·答案与解析版·真题版式）.docx')
m = len([x for x in zipfile.ZipFile(dx).namelist() if x.startswith('word/media/')])
print('docx media=%d ｜ 引用=%d ｜ %s' % (m, len(refs), '✅ 守恒' if m == len(refs) else '🔴 不守恒'))
print('媒体仓库文件数：前 %d → 后 %d（应相等，证明未写入）' % (med_before, len(os.listdir(MEDIA))))
print('staging 目录图数：%d' % len(os.listdir(STAGE)) if os.path.isdir(STAGE) else 'staging 缺')
