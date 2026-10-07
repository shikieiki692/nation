# -*- coding: utf-8 -*-
"""对 leak_backup / leak2_backup 的 .orig 模拟「题面泄露」闸（修复后）：
   - 原始版本在修复后的闸门下**仍是**题面泄露 ⇒ 原救援正确（保持现状）
   - 原始版本在修复后**通过** ⇒ 假阳性救援 ⇒ 应还原
输出每张卡的判定与依据。
"""
import os, re, sys, glob, shutil, tempfile
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.workbuddy/tmp/opt_pipe')
sys.argv = ['x', '--vol', 'LS', '--all-years']
import build_org as BO

ROOT = r'C:\Obsidion\妙妙屋'
OP = os.path.join(ROOT, '.workbuddy/tmp/opt_pipe')
TMP = os.path.join(OP, '_leaksim')
os.makedirs(TMP, exist_ok=True)


def nws(s):
    return len(re.sub(r'\s+', '', s))


def eval_orig(orig_text, basename):
    """在临时文件上跑闸门的 LEAK 部分 + 长度/无答案，返回 (leak_fail, reason, info)。"""
    tp = os.path.join(TMP, basename)
    open(tp, 'w', encoding='utf-8', newline='\n').write(orig_text)
    try:
        c = BO.X.extract(tp)
    except Exception as e:
        return True, 'EXTRACT_ERR:' + str(e)[:30], ''
    rawq, rawa = c['question'], c['answer']
    if BO.PLACEHOLDER.search(rawq):
        return True, '占位(题面)', ''
    if BO.PLACEHOLDER.search(rawa) and '![' not in rawa:
        _b = "\n".join(l for l in rawa.split("\n") if l.strip() and not BO.NOTE_LINE.search(l.strip()))
        if nws(_b) < 25:
            return True, '占位(答案)', ''
    q0 = BO.conv_imgs(BO.clean_q(rawq))
    a0 = BO.clean_a(BO.conv_imgs(rawa), q0)
    q, a = BO.html_table_to_md(q0), BO.html_table_to_md(a0)
    info = 'q=%d a=%d' % (nws(q), nws(a))
    if nws(rawq) < 60 or nws(rawa) < 25:
        return True, '过短(raw)', info
    if BO.LEAK.search(q):
        _own = BO.own_qno(orig_text, basename)
        _qchk = re.sub(r'^#{0,4}[^\S\n]*第[^\S\n]*%s[^\S\n]*[题題][^\n]*$' % BO.num_alt(_own),
                       '', q, flags=re.M)
        if BO.LEAK.search(_qchk):
            m = BO.LEAK.search(_qchk)
            return True, '题面泄露[%s]' % m.group(0)[:14], info
    return False, 'OK', info


results = []
for bk in ['leak_backup', 'leak2_backup']:
    d = os.path.join(OP, bk)
    for f in sorted(os.listdir(d)):
        if not f.endswith('.orig'):
            continue
        base = f[:-5]
        txt = open(os.path.join(d, f), encoding='utf-8-sig', errors='replace').read()
        fail, reason, info = eval_orig(txt, base)
        results.append((bk, base, fail, reason, info))

print('%-11s %-5s %-24s %s' % ('备份', '原版', '判定', '卡'))
for bk, base, fail, reason, info in results:
    print('%-11s %-5s %-24s %s' % (bk, '弃卡' if fail else '入池', reason, base[:52]))
print()
ok = [r for r in results if not r[2]]
print('原版通过（=假阳性救援，应还原）：%d 张' % len(ok))
for bk, base, _, _, _ in ok:
    print('   ', base[:60])
