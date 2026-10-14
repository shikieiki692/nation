# -*- coding: utf-8 -*-
r"""D1/D2 批量修复脚本（P1 工具，供 chemy 域解锁后一键执行）。

用法：
  python fix_mathring_delta.py --dry            # 只列清单（默认）
  python fix_mathring_delta.py --apply          # 写盘（自动备份 + 断言）
  python fix_mathring_delta.py --apply --include-chemy   # 显式纳入 chemy 域

规则：
  D1  `\mathrm{...\mathring X...}`（被误包）→ `\text{Å}`（仅当整段只含 ~/空格/该 accent）
      其余形态 ⇒ 进 review 清单，不自动改
  D2  `\mathrm{...\Delta...}` → 去掉段内 `\Delta`（保留其余），如 `\mathrm { \Delta VCl_3 }` → `\mathrm { VCl_3 }`
      若段内 `\Delta` 出现在 `\xrightarrow[...]` 中 ⇒ 误报，跳过
"""
import os, re, sys, io, shutil, datetime

ROOT = '04-题库'
CHEMY = '2026机构初赛模拟题/chemy'
APPLY = '--apply' in sys.argv
INC_CHEMY = '--include-chemy' in sys.argv

D1 = re.compile(r'\\mathrm\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*?\\mathring[^{}]*(?:\{[^{}]*\}[^{}]*)*?)\}')
D2 = re.compile(r'\\mathrm\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*?\\Delta[^{}]*(?:\{[^{}]*\}[^{}]*)*?)\}')
XARR = re.compile(r'\\x?rightarrow\s*\[[^\]]*\\Delta')

BAK = '.workbuddy/tmp/opt_pipe/_bak/d1d2_%s' % datetime.datetime.now().strftime('%Y%m%d_%H%M%S')


def d1_fix(seg):
    """段内只含 ~/空格/\\mathrm{mathring A} ⇒ 视为纯 Å 标记，整体替换。"""
    body = re.sub(r'\\mathrm\s*\{[^{}]*\\mathring\s*A\s*\}', '', seg)
    body = re.sub(r'\\mathring\s*A', '', body)
    if re.sub(r'[\s~]', '', body) == '':
        return r'\text{Å}'
    return None


def d2_fix(seg):
    if XARR.search(seg):
        return None                       # 正当：反应条件「Δ」（\xrightarrow[\Delta]）
    if re.search(r'\\Delta\s*[_^]', seg):
        return None                       # 正当：\Delta_r G / \Delta H_n（带下标）⇒ 人工复核
    # 正当：热力学量符号（\Delta H / \Delta G / \Delta S / \Delta U / \Delta F / \Delta A …）
    if re.search(r'\\Delta\s*(?:[HGSURAF](?![a-z]))', seg):
        return None
    if re.search(r'\\Delta\s*[A-Z][A-Za-z]', seg):
        out = re.sub(r'\\Delta\s*', '', seg)   # 内容噪声：如 `\Delta VCl_3` 渲染成 ΔVCl₃ ⇒ 应删 Δ
        return out if out.strip() else None
    if re.fullmatch(r'[\s~]*\\Delta[\s~]*', seg):
        return ''                          # 孤立 Δ ⇒ 删除
    return None


plan, review = [], []
for dp, dn, fn in os.walk(ROOT):
    for f in fn:
        if not f.endswith('.md'):
            continue
        p = os.path.join(dp, f).replace(os.sep, '/')
        if (CHEMY in p) and not INC_CHEMY:
            continue
        try:
            t = io.open(p, encoding='utf-8-sig').read()
        except Exception:
            continue
        n1 = len(D1.findall(t)); n2 = len(D2.findall(t))
        if not (n1 or n2):
            continue
        t2 = t
        for m in reversed(list(D1.finditer(t))):
            r = d1_fix(m.group(1))
            if r is None:
                review.append((p, 'D1', m.group(0)[:70])); continue
            t2 = t2[:m.start()] + r + t2[m.end():]
        for m in reversed(list(D2.finditer(t2))):
            r = d2_fix(m.group(1))
            if r is None:
                review.append((p, 'D2', m.group(0)[:70])); continue
            if r == '':
                t2 = t2[:m.start()] + t2[m.end():]          # 孤立 Δ ⇒ 整体删除（不留空壳 \mathrm{}）
            else:
                t2 = t2[:m.start()] + r'\mathrm{%s}' % r.strip() + t2[m.end():]
        plan.append((p, n1, n2, len(t), len(t2), t2))

print('待修卡数 %d ｜ 需人工复核项 %d' % (len(plan), len(review)))
for p, n1, n2, b, a, _ in plan:
    print('  D1=%-2d D2=%-2d  %s' % (n1, n2, p[:74]))
if review:
    print('\n【需人工复核（脚本不动）】')
    for p, k, s in review[:12]:
        print('  [%s] %s | %s' % (k, p.split("/")[-1][:34], s))

if APPLY and plan:
    os.makedirs(BAK, exist_ok=True)
    for p, n1, n2, b, a, t2 in plan:
        shutil.copy2(p, os.path.join(BAK, os.path.basename(p)))
        left = len(D1.findall(t2)) + len(D2.findall(t2))
        if left:
            print('  ⚠️ %s 仍残留 %d ⇒ 跳过' % (p[-30:], left)); continue
        io.open(p, 'w', encoding='utf-8', newline='').write(t2)
        print('  ✓ %s  %d→%d 字节' % (p[-38:], b, a))
    print('备份：', BAK)
else:
    print('\n(dry-run；加 --apply 写盘)')
