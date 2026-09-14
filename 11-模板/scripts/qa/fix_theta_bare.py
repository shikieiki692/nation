# -*- coding: utf-8 -*-
"""题源正文「裸标准态上标 ^θ」批量包装为行内数学。

- 只处理 04-题库/教材习题/化学能力测试/*.md
- 显式映射（30 种写法），最长优先
- 遮蔽 frontmatter / 围栏 / code span / 行内与块级 $…$ / [[…]] / HTML 注释
- 断言：行数不变、净 $ 数偶、控制字符 0
- 默认 dry-run；--apply 才落盘
"""
import os, re, sys, collections
sys.stdout.reconfigure(encoding="utf-8")
os.chdir(r"c:\Obsidion\妙妙屋")

ROOT = "04-题库/教材习题/化学能力测试"
APPLY = "--apply" in sys.argv

# (旧写法, 新写法)，最长优先
MAP = [
    (r"TΔrS^θ", r"$T\Delta_{\mathrm{r}}S^{\theta}$"),
    (r"TΔS^θₘ", r"$T\Delta S^{\theta}_{\mathrm{m}}$"),
    (r"TΔS^θ", r"$T\Delta S^{\theta}$"),
    (r"ΔvapH^θₘ", r"$\Delta_{\mathrm{vap}}H^{\theta}_{\mathrm{m}}$"),
    (r"ΔvapH^θ", r"$\Delta_{\mathrm{vap}}H^{\theta}$"),
    (r"ΔadH^θₘ", r"$\Delta_{\mathrm{ad}}H^{\theta}_{\mathrm{m}}$"),
    (r"Δ_adH^θₘ", r"$\Delta_{\mathrm{ad}}H^{\theta}_{\mathrm{m}}$"),
    (r"ΔcH^θ", r"$\Delta_{\mathrm{c}}H^{\theta}$"),
    (r"ΔrH^θₘ", r"$\Delta_{\mathrm{r}}H^{\theta}_{\mathrm{m}}$"),
    (r"ΔrS^θₘ", r"$\Delta_{\mathrm{r}}S^{\theta}_{\mathrm{m}}$"),
    (r"ΔrG^θₘ", r"$\Delta_{\mathrm{r}}G^{\theta}_{\mathrm{m}}$"),
    (r"ΔfH^θₘ", r"$\Delta_{\mathrm{f}}H^{\theta}_{\mathrm{m}}$"),
    (r"ΔfG^θₘ", r"$\Delta_{\mathrm{f}}G^{\theta}_{\mathrm{m}}$"),
    (r"ΔrH^θ", r"$\Delta_{\mathrm{r}}H^{\theta}$"),
    (r"ΔrS^θ", r"$\Delta_{\mathrm{r}}S^{\theta}$"),
    (r"ΔrG^θ", r"$\Delta_{\mathrm{r}}G^{\theta}$"),
    (r"ΔfH^θ", r"$\Delta_{\mathrm{f}}H^{\theta}$"),
    (r"ΔfG^θ", r"$\Delta_{\mathrm{f}}G^{\theta}$"),
    (r"ΔG^θₘ", r"$\Delta G^{\theta}_{\mathrm{m}}$"),
    (r"ΔH^θₘ", r"$\Delta H^{\theta}_{\mathrm{m}}$"),
    (r"ΔS^θₘ", r"$\Delta S^{\theta}_{\mathrm{m}}$"),
    (r"ΔG^θ", r"$\Delta G^{\theta}$"),
    (r"ΔH^θ", r"$\Delta H^{\theta}$"),
    (r"ΔS^θ", r"$\Delta S^{\theta}$"),
    (r"ΔU^θ", r"$\Delta U^{\theta}$"),
    (r"ΔA^θ", r"$\Delta A^{\theta}$"),
    (r"S^θₘ", r"$S^{\theta}_{\mathrm{m}}$"),
    (r"G^θₘ", r"$G^{\theta}_{\mathrm{m}}$"),
    (r"H^θₘ", r"$H^{\theta}_{\mathrm{m}}$"),
    (r"nFE^θ", r"$nFE^{\theta}$"),
    (r"FE^θ", r"$FE^{\theta}$"),
    (r"Kp^θ", r"$K_{\mathrm{p}}^{\theta}$"),
    (r"Cp^θ", r"$C_{\mathrm{p}}^{\theta}$"),
    (r"G^θ", r"$G^{\theta}$"),
    (r"E^θ", r"$E^{\theta}$"),
    (r"S^θ", r"$S^{\theta}$"),
    (r"H^θ", r"$H^{\theta}$"),
    (r"K^θ", r"$K^{\theta}$"),
    (r"p^θ", r"$p^{\theta}$"),
]
ALTS = sorted(MAP, key=lambda kv: -len(kv[0]))
PAT = re.compile("(?:" + "|".join(re.escape(k) for k, _ in ALTS) + ")")
REPL = dict((k, v) for k, v in MAP)


def mask(line):
    out = list(line); i, n = 0, len(line)
    def blank(a, b):
        for k in range(a, min(b, n)):
            out[k] = ' '
    while i < n:
        ch = line[i]
        if ch == '`':
            j = line.find('`', i + 1)
            if j == -1:
                break
            blank(i, j + 1); i = j + 1; continue
        if line.startswith('$$', i) and not (i > 0 and line[i - 1] == '\\'):
            j = line.find('$$', i + 2)
            if j == -1:
                blank(i, n); break
            blank(i, j + 2); i = j + 2; continue
        if ch == '$' and not (i > 0 and line[i - 1] == '\\'):
            j = line.find('$', i + 1)
            if j == -1:
                i += 1; continue
            blank(i, j + 1); i = j + 1; continue
        if line.startswith('![[', i) or line.startswith('[[', i):
            j = line.find(']]', i)
            if j == -1:
                break
            blank(i, j + 2); i = j + 2; continue
        i += 1
    return ''.join(out)


def fix_line(raw):
    """在遮蔽层定位、在原行替换；返回 (新行, [(旧,新)])"""
    m = mask(raw)
    changes = []
    out = []
    last = 0
    for mo in PAT.finditer(m):
        a, b = mo.start(), mo.end()
        # 左边界：前面不能是 ASCII 字母/数字/下划线（避免词中被截）
        if a > 0 and raw[a - 1].isascii() and (raw[a - 1].isalpha() or raw[a - 1] == '_'):
            continue
        old = raw[a:b]
        new = REPL[old]
        out.append(raw[last:a]); out.append(new)
        last = b
        changes.append((old, new))
    out.append(raw[last:])
    return ''.join(out), changes


files = []
for dp, dn, fn in os.walk(ROOT):
    if '_归档' in dp or os.path.basename(dp).startswith('_'):
        continue
    for f in fn:
        if f.endswith('.md'):
            files.append(os.path.join(dp, f))
files.sort()

LOG = []
TARGETS = []
for p in files:
    raw_text = open(p, encoding="utf-8", newline="").read()
    lines = raw_text.split("\n")
    in_fence = in_fm = in_disp = False; fm_done = False
    changed = bool(False)
    for idx, raw in enumerate(lines):
        s = raw.strip()
        if not fm_done:
            if idx == 0 and s == '---':
                in_fm = True; continue
            if in_fm:
                if s == '---':
                    in_fm = False; fm_done = True
                continue
        if s.startswith('```') or s.startswith('~~~'):
            in_fence = not in_fence; continue
        if in_fence: continue
        c_dd = s.count('$$')
        if c_dd:
            if c_dd % 2 == 1:
                in_disp = not in_disp; continue
            if in_disp:
                continue
        if in_disp: continue
        if s.startswith('<!--') or s.endswith('-->'): continue
        if '^θ' not in raw:
            continue
        new, ch = fix_line(raw)
        if ch:
            LOG.append((p.replace("\\", "/"), idx + 1, ch, raw, new))
            lines[idx] = new
            changed = True
    if changed:
        TARGETS.append((p, raw_text, "\n".join(lines)))

print("涉及文件 %d；变更 %d 处" % (len(TARGETS), len(LOG)))
print()
c = collections.Counter()
for p, i, ch, a, b in LOG:
    for o, n in ch:
        c[(o, n)] += 1
print("=== 变更类型统计 ===")
for (o, n), k in c.most_common():
    print("  %-12s → %-34s x%d" % (o, n, k))
print()
for p, i, ch, a, b in LOG:
    print("[%s L%d]" % (p.split('/')[-1][:52], i))
    print("  旧: %s" % a[:175])
    print("  新: %s" % b[:175])

if APPLY:
    for p, s0, s in TARGETS:
        assert s.count("\n") == s0.count("\n"), "行数变化: " + p
        net = s.replace(chr(92) + chr(36), "").count(chr(36))
        assert net % 2 == 0, "净 $ 奇数: " + p
        ctrl = [c2 for c2 in s if ord(c2) < 0x20 and c2 not in "\r\n\t"]
        assert not ctrl, "含控制字符: " + p
        open(p, "w", encoding="utf-8", newline="").write(s)
    print("\nAPPLIED %d 文件" % len(TARGETS))
