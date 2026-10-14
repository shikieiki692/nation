# -*- coding: utf-8 -*-
"""fmt_ext2.py —— 收紧版「化学式排版」扩域（仅 真题/化学原理/有机化学，**不含教材习题=跨线**）。

与 fmt_formula_global 同源，但只保留**已验证安全**的两条规则，并对 fspace 加守卫：

· fspace' = `(?<!\\d[-.])([A-Za-z0-9])[ \\t]+(\\$[_^]\\{)` → `\\1\\2`
  守卫排除「题号尾部」语境（`8-4 $^{235}U$` 的空格是合法分隔，删了会渲染成 `8-4235U`）。
· fbase  = 原样（已在 目标域 抽样验证：`M $^{n+}$` → `$\\mathrm{M}^{n+}$` **视觉等价**）。
· **不用** fempty（上标改挂关系符，未证安全）／fbase2（半改，产物与 fbase 不一致）。

用法：python fmt_ext2.py [--apply]
"""
import os, re, sys, glob, shutil, datetime, collections
HERE = r"C:\Obsidion\妙妙屋\.workbuddy\tmp\opt_pipe"
sys.path.insert(0, HERE)
import volpost

R = r"C:\Obsidion\妙妙屋"
ROOTS = ["04-题库/真题", "04-题库/化学原理", "04-题库/有机化学"]   # ⚠️ 刻意排除 04-题库/教材习题（另一条线）
BAK = os.path.join(HERE, "card_bak_extfmt2")

FSPACE = re.compile(r'(?<!\d[-.])([A-Za-z0-9])[ \t]+(\$[_^]\{)')
FBASE = next((rx, rep) for nm, rx, rep in volpost.RULES if nm == 'fbase')
RULES = [('fspace_g', FSPACE, r'\1\2'), ('fbase', FBASE[0], FBASE[1])]

VIS = re.compile(r"\$|\{|\}|\\mathrm|\s|\\,")


def apply_rules(t):
    chg = []
    for name, rx, rep in RULES:
        def _sub(m, _rep=rep, _name=name):
            new = _rep(m) if callable(_rep) else m.expand(_rep)
            chg.append((_name, m.group(0), new))
            return new
        t = rx.sub(_sub, t)
    return t, chg


def main():
    apply_ = "--apply" in sys.argv
    stamp = datetime.datetime.now().strftime("%m%d_%H%M")
    if apply_:
        os.makedirs(BAK, exist_ok=True)
    files = []
    for root in ROOTS:
        files += glob.glob(os.path.join(R, root, "**", "题-*.md"), recursive=True)
    files = sorted(set(files))
    print("候选 %d（根：%s）" % (len(files), "／".join(ROOTS)))
    tot, nfiles, bad, eol = 0, 0, [], 0
    per = []
    for fp in files:
        raw = open(fp, encoding="utf-8-sig").read()
        if "\r\n" in raw:
            eol += 1
            raw = raw.replace("\r\n", "\n")
        new, chg = apply_rules(raw)
        if new == raw:
            continue
        if VIS.sub("", raw) != VIS.sub("", new):
            bad.append((fp, "可见字符改变")); continue
        again, _ = apply_rules(new)
        if again != new:
            bad.append((fp, "非幂等")); continue
        nfiles += 1; tot += len(chg)
        per.append((os.path.relpath(fp, R).replace("\\", "/"), len(chg),
                    dict(collections.Counter(c[0] for c in chg))))
        if apply_:
            shutil.copy2(fp, os.path.join(BAK, os.path.basename(fp) + ".bak-" + stamp))
            with open(fp, "w", encoding="utf-8", newline="\n") as f:
                f.write(new)
    agg = collections.Counter()
    for _r, _n, c in per:
        for k, v in c.items():
            agg[k] += v
    print("%s 收紧扩域：%d 卡 / %d 处（CRLF %d）" % ("已写盘" if apply_ else "(dry)", nfiles, tot, eol))
    print("   规则：", dict(agg))
    if bad:
        print("\n!! 安全检查未过 %d：" % len(bad))
        for fp, why in bad[:20]:
            print("   ", why, os.path.basename(fp))
        sys.exit(1)
    print("\n   前 12 张：")
    for rel, n, c in sorted(per, key=lambda x: -x[1])[:12]:
        print("      %-48s %3d %s" % (rel[-46:], n, c))


if __name__ == "__main__":
    main()
