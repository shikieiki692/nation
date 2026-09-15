# -*- coding: utf-8 -*-
"""裸下标批量修复器（组 1 高 + 组 2 中置信度）。

设计要点
- **遮蔽逻辑与 `scan_bare5.py` 逐字一致**（code span / `$$…$$` / `$…$` / `[[…]]` /
  行内 HTML 注释 / frontmatter / 代码围栏），二者必须同步修改。
- 只在**可见区**替换；`is_pathish` 排除媒体文件名。
- **安全跳闸**：token 后紧跟 `^`/`_`（属 `X_a^b` 组合，须人工定夺）→ 跳过，记入「跳过」。
- 逐文件断言：行数不变、`$` 奇偶不变、控制字符 0。
- 默认 dry-run；`--apply` 才落盘（写盘用 `newline=""` 保行尾）。

用法
    python -X utf8 11-模板/scripts/qa/fix_bare5.py --roots <目录> [<目录> ...]
        [--exclude <子串> ...] [--only <文件清单.txt>] [--apply]
"""
import os
import re
import sys
import collections

sys.stdout.reconfigure(encoding="utf-8")
REPO = r"c:\Obsidion\妙妙屋"
os.chdir(REPO)

# ────────────────────────── 遮蔽（与 scan_bare5.py 同源，逐字） ──────────────────────────
SUB_UNI = "₀-₉₊₋₌₍₎ₐₑₒₓₔₕₖₗₘₙₚₛₜⁿ"
SUP_UNI = "⁰-⁹⁺⁻⁼⁽⁾ⁿ"
BODY = r"A-Za-z0-9()+\-−·/_%"
FIRSTCH = r"0-9A-Za-z()+\-−·θφλμνσπσΣΔΩ°½¼¾′″" + SUB_UNI + SUP_UNI
GREEK = r"\u0370-\u03FF\u1F00-\u1FFF"
PAT = re.compile(r"(?<![\\$A-Za-z0-9" + GREEK + r"])"
                 r"([" + GREEK + r"A-Za-z][" + GREEK + r"A-Za-z0-9]{0,14})"
                 r"([_^])(["
                 + FIRSTCH + r"][" + BODY + SUB_UNI + SUP_UNI + r"]{0,10})")
MEDIA_EXT = re.compile(r'\.(?:jpe?g|png|gif|webp|svg|bmp|tiff?|pdf|md|docx?|xlsx?|zip)(?:$|[|\])\s])', re.I)
SUPSUB = set("₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎ₐₑₒₓₔₕₖₗₘₙₚₛₜⁿ"
             "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿ")


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


def is_pathish(raw, a, b):
    word_re = re.compile(r'[A-Za-z0-9_\-./\\]+')
    wa = a
    while wa > 0 and word_re.match(raw[wa - 1]):
        wa -= 1
    wb = b
    while wb < len(raw) and word_re.match(raw[wb]):
        wb += 1
    if MEDIA_EXT.search(raw[wa:wb]):
        return True

    def _ascii_word(ch):
        return ch.isascii() and (ch.isalnum() or ch == '_')
    return (a > 0 and _ascii_word(raw[a - 1])) or (b < len(raw) and _ascii_word(raw[b]))


# ────────────────────────── 组 1 / 组 2 映射 ──────────────────────────
# 规则：值一律「行内裸 $…$」；下标用 \mathrm；不改上下标语义。
MAP = {
    # ── A 类
    "c_O₂": r"$c_{\mathrm{O_2}}$",
    "c_O₂·": r"$c_{\mathrm{O_2}}$·",
    "p_NH₃": r"$p_{\mathrm{NH_3}}$",
    "p_O₂": r"$p_{\mathrm{O_2}}$",
    "p_SO₂": r"$p_{\mathrm{SO_2}}$",
    "p_H₂O": r"$p_{\mathrm{H_2O}}$",
    "p_H₂": r"$p_{\mathrm{H_2}}$",
    "p_N₂": r"$p_{\mathrm{N_2}}$",
    "p_CO₂": r"$p_{\mathrm{CO_2}}$",
    "e_g⁰": r"$e_g^0$",
    "Y_ySₓ₋₂": r"$Y_yS_{x-2y}$",
    # ── B 类
    "Dq_t": r"$Dq_t$",
    "RT_b": r"$RT_b$",
    "UCl_b": r"$\mathrm{UCl}_b$",
    "N_A": r"$N_{\mathrm{A}}$",
    "δ_H": r"$\delta_{\mathrm{H}}$",
    "δ_C": r"$\delta_{\mathrm{C}}$",
    "μ_B": r"$\mu_{\mathrm{B}}$",
    "θ_A": r"$\theta_{\mathrm{A}}$",
    "σ_m": r"$\sigma_{\mathrm{m}}$",
    "σ_p": r"$\sigma_{\mathrm{p}}$",
    "σ_d": r"$\sigma_{\mathrm{d}}$",
    "α_A": r"$\alpha_{\mathrm{A}}$",
    # ── C 类
    "S_N2": r"$S_{\mathrm{N}}2$",
    "S_N1": r"$S_{\mathrm{N}}1$",
    "J_PH": r"$J_{\mathrm{PH}}$",
    "J_CF": r"$J_{\mathrm{CF}}$",
    "J_HH": r"$J_{\mathrm{HH}}$",
    "J_HF": r"$J_{\mathrm{HF}}$",
    "J_cis": r"$J_{\mathrm{cis}}$",
    "J_trans": r"$J_{\mathrm{trans}}$",
    "J_axial/axial": r"$J_{\mathrm{axial/axial}}$",
    "J_PH)": r"$J_{\mathrm{PH}}$)",
    "k_obs": r"$k_{\mathrm{obs}}$",
    "p_total/2": r"$p_{\mathrm{total}}/2$",
    "p_total": r"$p_{\mathrm{total}}$",
    "p_max": r"$p_{\mathrm{max}}$",
    "t_break": r"$t_{\mathrm{break}}$",
    "r_CO": r"$r_{\mathrm{CO}}$",
    "d_xy": r"$d_{xy}$",
    "A_xN_y": r"$A_xN_y$",
    "ν_max": r"$\nu_{\mathrm{max}}$",
    "ε_max": r"$\varepsilon_{\mathrm{max}}$",
    "λ_max": r"$\lambda_{\mathrm{max}}$",
    "P_total/atm": r"$P_{\mathrm{total}}/\mathrm{atm}$",
    "p_HCl/Torr": r"$p_{\mathrm{HCl}}/\mathrm{Torr}$",
    "UCl_a)": r"$\mathrm{UCl}_a$)",
    "M_av": r"$M_{\mathrm{av}}$",
    # ── D 类
    "H^A": r"$H^{\mathrm{A}}$",
    "H^B": r"$H^{\mathrm{B}}$",
    "H^C": r"$H^{\mathrm{C}}$",
    "H^D": r"$H^{\mathrm{D}}$",
    "e^(−E/kT)": r"$e^{-E/kT}$",
    "sp^2": r"$sp^2$",
    "ns^n": r"$ns^n$",
    "np^(n−1)": r"$np^{n-1}$",
    "S^+": r"$S^{+}$",
    "SO4^2-": r"$\mathrm{SO_4^{2-}}$",
    "VO4^3-": r"$\mathrm{VO_4^{3-}}$",
    # ── 讲义专用
    "k_H₂O/k_D₂O": r"$k_{\mathrm{H_2O}}/k_{\mathrm{D_2O}}$",
    "k_H/k_D": r"$k_{\mathrm{H}}/k_{\mathrm{D}}$",
    "k_A": r"$k_{\mathrm{A}}$",
    "k_B)": r"$k_{\mathrm{B}})$",
    "k_B": r"$k_{\mathrm{B}}$",
    "k_D": r"$k_{\mathrm{D}}$",
    "k_H": r"$k_{\mathrm{H}}$",
    "k_rxn": r"$k_{\mathrm{rxn}}$",
    "μ_eff": r"$\mu_{\mathrm{eff}}$",
    "ΔH_vap/R": r"$\Delta H_{\mathrm{vap}}/R$",
    "ΔH_vap": r"$\Delta H_{\mathrm{vap}}$",
    "α_t": r"$\alpha_t$",
    "α_0": r"$\alpha_0$",
    "V_m": r"$V_{\mathrm{m}}$",
    "O_y": r"$O_y$",
    "d_z": r"$d_z$",
    "CHR_2": r"$\mathrm{CHR}_2$",
    "CH_2R": r"$\mathrm{CH}_2\mathrm{R}$",
    "CH_3": r"$\mathrm{CH}_3$",
    "CR_3": r"$\mathrm{CR}_3$",
    "E^θ": r"$E^{\theta}$",
    # ── 教案专用
    "M_A/M_B": r"$M_{\mathrm{A}}/M_{\mathrm{B}}$",
    "M_A": r"$M_{\mathrm{A}}$",
    "M_B": r"$M_{\mathrm{B}}$",
    "ρ_H₂": r"$\rho_{\mathrm{H_2}}$",
    "ρ_A/": r"$\rho_{\mathrm{A}}$/",   # 斜杠留在 math 外，避免与后一个 $…$ 拼出 $$（会被 pandoc 当 display math）
    "ρ_B": r"$\rho_{\mathrm{B}}$",
}


def process_file(path, apply):
    raw_text = open(path, encoding="utf-8", errors="replace", newline="").read()
    lines = raw_text.split("\n")
    n_ctrl = sum(1 for ch in raw_text if ord(ch) < 32 and ch not in "\n\r\t")
    par0 = raw_text.count("$") % 2
    out_lines = []
    changes = []
    skipped = collections.Counter()
    skip_lines = []
    applied = collections.Counter()
    in_fence = in_fm = in_disp = False
    fm_done = False
    for idx, raw in enumerate(lines, 1):
        s = raw.strip()
        if not fm_done:
            if idx == 1 and s == '---':
                in_fm = True; out_lines.append(raw); continue
            if in_fm:
                if s == '---':
                    in_fm = False; fm_done = True
                out_lines.append(raw); continue
        if s.startswith('```') or s.startswith('~~~'):
            in_fence = not in_fence; out_lines.append(raw); continue
        if in_fence:
            out_lines.append(raw); continue
        cnt_dd = s.count('$$')
        if cnt_dd:
            if cnt_dd % 2 == 1:
                in_disp = not in_disp; out_lines.append(raw); continue
            if in_disp:
                out_lines.append(raw); continue
        if in_disp:
            out_lines.append(raw); continue
        if s.startswith('<!--') or s.endswith('-->'):
            out_lines.append(raw); continue

        m = mask(raw)
        reps = []
        for mo in PAT.finditer(m):
            a, b = mo.start(), mo.end()
            tokn = raw[a:b]
            # 组3 跳闸：后紧跟 ^/_ → X_a^b 组合，须人工定夺
            if b < len(raw) and raw[b] in "^_":
                if not is_pathish(raw, a, b):
                    skipped[tokn] += 1
                    skip_lines.append((idx, tokn, raw))
                continue
            cur = b
            while cur < len(raw) and raw[cur] in SUPSUB:
                cur += 1
            cand = raw[a:cur]
            if cand in MAP:
                tok, end = cand, cur
            elif tokn in MAP:
                tok, end = tokn, b
            else:
                if not is_pathish(raw, a, b):
                    skipped[tokn] += 1
                    skip_lines.append((idx, tokn, raw))
                continue
            if is_pathish(raw, a, end):
                continue
            reps.append((a, end, tok))
            applied[tok] += 1
        if reps:
            new = raw
            for a, end, tok in sorted(reps, key=lambda x: -x[0]):
                new = new[:a] + MAP[tok] + new[end:]
            changes.append((idx, raw, new))
            out_lines.append(new)
        else:
            out_lines.append(raw)

    new_text = "\n".join(out_lines)
    par1 = new_text.count("$") % 2
    # $$ 邻接守卫：替换不得**引入**新的 $$（会被 pandoc 当 display math）
    dd_new = new_text.count("$$") - raw_text.count("$$")
    ok = (len(out_lines) == len(lines)) and (par0 == par1) and (n_ctrl == 0) and (dd_new == 0)
    return {
        "path": path, "lines": len(lines), "changes": changes,
        "par0": par0, "par1": par1, "ctrl": n_ctrl, "ok": ok, "dd_new": dd_new,
        "skipped": skipped, "applied": applied, "new_text": new_text,
        "skip_lines": skip_lines,
    }


def main():
    argv = sys.argv[1:]
    apply = "--apply" in argv
    dump = "--dump-skipped" in argv
    roots, excludes, only = [], [], None
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--roots":
            i += 1
            while i < len(argv) and not argv[i].startswith("--"):
                roots.append(argv[i]); i += 1
            continue
        if a == "--exclude":
            i += 1; excludes.append(argv[i]); i += 1; continue
        if a == "--only":
            i += 1; only = argv[i]; i += 1; continue
        i += 1

    if only:
        files = [l.strip() for l in open(only, encoding="utf-8").read().split("\n") if l.strip()]
    else:
        files = []
        for root in roots:
            for dp, dn, fn in os.walk(root):
                if any(x in dp for x in excludes):
                    continue
                if os.path.basename(dp).startswith('_') or '_归档' in dp or '_archive' in dp:
                    continue
                for f in fn:
                    if f.endswith('.md') and not f.startswith('README'):
                        files.append(os.path.join(dp, f))
    files = sorted(set(files))

    print("模式: %s   文件数: %d" % ("APPLY" if apply else "DRY-RUN", len(files)))
    tok_stat = collections.Counter()
    skip_stat = collections.Counter()
    bad = []
    all_skips = []
    total_chg = 0
    nfiles = 0
    for p in files:
        r = process_file(p, apply)
        if r["changes"]:
            nfiles += 1
            total_chg += len(r["changes"])
            tok_stat.update(r["applied"])
            print("\n=== %s  (%d 行变化, 行数 %d%s%s%s) ===" % (
                p, len(r["changes"]), r["lines"],
                "" if r["par0"] == r["par1"] else "  !!$奇偶变化",
                "" if r["ctrl"] == 0 else "  !!控制字符%d" % r["ctrl"],
                "" if r["dd_new"] == 0 else "  !!新增$$%d" % r["dd_new"]))
            for idx, old, new in r["changes"][:999]:
                print("  L%-5d - %s" % (idx, old[:200]))
                print("         + %s" % new[:200])
        skip_stat.update(r["skipped"])
        all_skips.extend((p, idx, tok, raw) for idx, tok, raw in r["skip_lines"])
        if not r["ok"]:
            bad.append(p)
        if apply and r["changes"]:
            with open(p, "w", encoding="utf-8", newline="") as f:
                f.write(r["new_text"])

    print("\n──── 汇总 ────")
    print("涉及文件: %d   变化行: %d   替换 token 数: %d" % (nfiles, total_chg, sum(tok_stat.values())))
    print("按 token（前 40）：")
    for k, v in tok_stat.most_common(40):
        print("   %-22s x%d" % (k, v))
    if skip_stat:
        print("跳过（组3/未映射，前 30）：")
        for k, v in skip_stat.most_common(30):
            print("   %-22s x%d" % (k, v))
    if dump and all_skips:
        bytok = collections.defaultdict(list)
        for p, idx, tok, raw in all_skips:
            bytok[tok].append((p, idx, raw))
        print("\n──── 组3 残量明细（需人工定夺，按 token 分组）────")
        for tok, items in sorted(bytok.items(), key=lambda kv: (-len(kv[1]), kv[0])):
            print("\n[%s] ×%d" % (tok, len(items)))
            for p, idx, raw in items[:20]:
                print("  %s L%d" % (p, idx))
                print("      %s" % raw.strip()[:230])
    if bad:
        print("!! 断言失败文件: %s" % bad)
    else:
        print("断言：全部通过（行数不变 / $ 奇偶不变 / 无新增 $$ / 控制字符 0）")


if __name__ == "__main__":
    main()
