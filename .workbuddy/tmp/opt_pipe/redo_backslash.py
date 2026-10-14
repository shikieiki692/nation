# -*- coding: utf-8 -*-
r"""① 回退我的错误修复（从 dblback 备份恢复）② 精确只改「恰好 2 反斜杠」的 T1 工具产物。"""
import os, io, glob, re, shutil, datetime
os.chdir(r'C:\Obsidion\妙妙屋')
BAK = sorted(glob.glob('.workbuddy/tmp/opt_pipe/_bak/dblback_*'))[-1]
print('从备份恢复:', BAK)

# ① 恢复（备份平铺存放，需找回原路径）
# 建 basename -> 原路径 映射
bymap = {}
for dp, dn, fn in os.walk('04-题库'):
    for f in fn:
        if f.endswith('.md'):
            bymap.setdefault(f, []).append(os.path.join(dp, f))
restored = 0
for f in os.listdir(BAK):
    if not f.endswith('.md'):
        continue
    src = os.path.join(BAK, f)
    cands = bymap.get(f, [])
    if not cands:
        print('  ⚠️ 找不到原路径:', f[:40]); continue
    # 内容匹配以消歧
    data = io.open(src, encoding='utf-8-sig', errors='replace').read()
    for c in cands:
        cur = io.open(c, encoding='utf-8-sig', errors='replace').read()
        if len(cur) != len(data) or cur[:200] != data[:200]:
            shutil.copy2(src, c); restored += 1
            break
print('恢复文件数:', restored)

# ② 精确修：恰好 2 个反斜杠 + mathrm{...}
PAT2 = re.compile(r'(?<!\\)\\\\(?!\\)mathrm\{([^{}]*)\}')
fixed = 0
files = 0
for dp, dn, fn in os.walk('04-题库'):
    for f in fn:
        if not f.endswith('.md'):
            continue
        p = os.path.join(dp, f)
        t = io.open(p, encoding='utf-8-sig').read()
        ms = list(PAT2.finditer(t))
        if not ms:
            continue
        files += 1
        cnt = [0]

        def rep(m):
            cnt[0] += 1
            return r'\mathrm{%s}' % m.group(1).strip()
        t2 = PAT2.sub(rep, t)
        io.open(p, 'w', encoding='utf-8', newline='').write(t2)
        fixed += cnt[0]
print('精确修复：%d 文件 / %d 处（2 反斜杠 → 1）' % (files, fixed))

# ③ 复验：2 反斜杠应为 0；3 反斜杠应保持
n2 = n3 = 0
for dp, dn, fn in os.walk('04-题库'):
    for f in fn:
        if not f.endswith('.md'):
            continue
        t = io.open(os.path.join(dp, f), encoding='utf-8-sig').read()
        for m in re.finditer(r'(\\+)mathrm', t):
            k = len(m.group(1))
            if k == 2:
                n2 += 1
            elif k == 3:
                n3 += 1
            elif k >= 4:
                print('  ⚠️ %d 反斜杠: %s' % (k, f[:40]))
print('复验：2 反斜杠残留 %d ｜ 3 反斜杠（合法） %d' % (n2, n3))
