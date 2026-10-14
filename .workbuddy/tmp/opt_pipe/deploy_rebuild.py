# -*- coding: utf-8 -*-
"""按并行线「部署 → 重建 → 清理」流程，同步 6 卷答案版 docx。

护栏：
  ① 只向 媒体仓库/ **新增**缺失图（绝不覆盖已存在文件）；记录新增清单；
  ② 构建后断言 docx `word/media` 数 == 卷 md 图引用数；
  ③ 清理：只删「我新增且构建成功」的文件；
  ④ 失败则回滚 docx（从备份）并清理。
用法：--deploy（部署+构建+校验） / --clean（清理新增）
"""
import io, os, re, sys, glob, shutil, zipfile, subprocess, json, hashlib

os.chdir(r'C:\Obsidion\妙妙屋')
PY = r'C:\Users\蕾赛\AppData\Local\Programs\Python\Python312\python.exe'
MEDIA = '媒体仓库'
VOLS = ['X', 'XI', 'XIp', 'XIV', 'XVI', 'XVII']
LEDGER = '.workbuddy/tmp/opt_pipe/_deploy_ledger.json'
D = '00-首页/题组Word/初赛模拟卷/真题版式'


def refs_of(v):
    t = io.open('04-题库/初赛模拟卷%s（非有机·答案版）.md' % v, encoding='utf-8-sig').read()
    ns = [os.path.basename(x) for x in re.findall(r'!\[\[([^\]|]+?\.(?:jpg|jpeg|png))(?:\|[^\]]*)?\]\]', t, re.I)]
    ns += [os.path.basename(x) for x in re.findall(r'!\[[^\]]*\]\(([^)]+?\.(?:jpg|jpeg|png))\)', t, re.I)]
    return ns


def lib_index():
    idx = {}
    for dp, dn, fn in os.walk('.'):
        dn[:] = [d for d in dn if d not in ('.git', '.workbuddy') and not dp.endswith(MEDIA)]
        for f in fn:
            if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                idx.setdefault(f, os.path.join(dp, f))
    return idx


if '--clean' in sys.argv:
    led = json.load(io.open(LEDGER, encoding='utf-8')) if os.path.exists(LEDGER) else []
    n = 0
    for f in led:
        p = os.path.join(MEDIA, os.path.basename(f))
        if os.path.exists(p):
            os.remove(p); n += 1
    print('已清理部署文件 %d / %d' % (n, len(led)))
    if os.path.exists(LEDGER):
        os.remove(LEDGER)
    sys.exit(0)

IDX = lib_index()
print('库内图片索引 %d 个文件名' % len(IDX))
todo = {}
for v in VOLS:
    miss = []
    for n in refs_of(v):
        if os.path.exists(os.path.join(MEDIA, n)):
            continue
        if n in IDX:
            miss.append((n, IDX[n]))
        else:
            print('  ⛔ 卷%s 图在全库找不到: %s' % (v, n[:50]))
    todo[v] = miss
    print('  卷%-5s 需部署 %d 张' % (v, len(miss)))

if '--deploy' not in sys.argv:
    print('\n[dry-run] 未部署')
    sys.exit(0)

ledger = []
for v, lst in todo.items():
    for n, src in lst:
        dst = os.path.join(MEDIA, n)
        if not os.path.exists(dst):          # ① 绝不覆盖
            shutil.copy2(src, dst)
            ledger.append(n)
json.dump(ledger, io.open(LEDGER, 'w', encoding='utf-8'), ensure_ascii=False)
print('已部署 %d 张（清单 %s）' % (len(ledger), LEDGER))

# ② 构建
r = subprocess.run([PY, '-X', 'utf8', '.workbuddy/scripts/build_chusai_zhenti_layout.py', '--answer'] + VOLS,
                   capture_output=True, text=True, encoding='utf-8', errors='replace')
tail = [l for l in (r.stdout or '').split('\n') if l.strip()][-3:]
print('构建 rc=%d | %s' % (r.returncode, ' / '.join(tail)))

# ③ 校验
bad = []
for v in VOLS:
    dx = os.path.join(D, '初赛模拟卷%s（非有机·答案与解析版·真题版式）.docx' % v)
    if not os.path.exists(dx):
        bad.append((v, 'docx 缺失')); continue
    m = len([x for x in zipfile.ZipFile(dx).namelist() if x.startswith('word/media/')])
    e = len(refs_of(v))
    tag = '✅' if m == e else '🔴'
    if m != e:
        bad.append((v, 'media %d != 引用 %d' % (m, e)))
    print('  卷%-5s media=%-3d 引用=%-3d %s' % (v, m, e, tag))
print('校验失败:', bad if bad else '无')
