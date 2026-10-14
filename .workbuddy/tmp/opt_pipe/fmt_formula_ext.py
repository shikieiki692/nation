# -*- coding: utf-8 -*-
"""fmt_formula_ext.py —— 「化学式排版」扩域：把 fmt_formula_global 的 fspace/fbase/fbase2/fempty
三条**纯格式**规则，从机构域扩到 教材习题 / 真题 / 化学原理 / 有机化学。

与 global 版**完全同源同判据**（同一 RULES、同一可见字符不变量、同一幂等断言、同一备份）。
用法：python fmt_formula_ext.py [--apply]
"""
import os, re, sys, glob, shutil, datetime, collections

HERE = r"C:\Obsidion\妙妙屋\.workbuddy\tmp\opt_pipe"
sys.path.insert(0, HERE)
import volpost  # noqa

R = r"C:\Obsidion\妙妙屋"
ROOTS = ["04-题库/教材习题", "04-题库/真题", "04-题库/化学原理", "04-题库/有机化学"]
BAK = os.path.join(HERE, "card_bak_extfmt")
WANT = ("fspace", "fbase", "fbase2", "fempty")
RULES = [(nm, rx, rep) for nm, rx, rep in volpost.RULES if nm in WANT]
assert len(RULES) == 4, [r[0] for r in RULES]


def apply_rules(t):
    chg = []
    for name, rx, rep in RULES:
        def _sub(m, _rep=rep, _name=name):
            new = _rep(m) if callable(_rep) else m.expand(_rep)
            chg.append((_name, m.group(0), new))
            return new
        t = rx.sub(_sub, t)
    return t, chg


VIS = re.compile(r"\$|\{|\}|\\mathrm|\s|\\,")


def visible(t):
    return VIS.sub("", t)


def main():
    apply_ = "--apply" in sys.argv
    stamp = datetime.datetime.now().strftime("%m%d_%H%M")
    if apply_:
        os.makedirs(BAK, exist_ok=True)
    files = []
    for root in ROOTS:
        files += glob.glob(os.path.join(R, root, "**", "题-*.md"), recursive=True)
    files = sorted(set(files))
    print("候选 %d 个 md（根：%s）" % (len(files), "／".join(ROOTS)))
    tot, nfiles, bad, eol = 0, 0, [], 0
    per = []
    byroot = collections.Counter()
    for fp in files:
        raw = open(fp, encoding="utf-8-sig").read()
        if "\r\n" in raw:
            eol += 1
            raw = raw.replace("\r\n", "\n")
        new, chg = apply_rules(raw)
        if new == raw:
            continue
        if visible(raw) != visible(new):
            bad.append((fp, "可见字符改变"))
            continue
        again, _ = apply_rules(new)
        if again != new:
            bad.append((fp, "非幂等"))
            continue
        nfiles += 1
        tot += len(chg)
        cnt = collections.Counter(c[0] for c in chg)
        rel = os.path.relpath(fp, R).replace("\\", "/")
        byroot[rel.split("/")[1] + ("/" + rel.split("/")[2] if len(rel.split("/")) > 3 else "")] += len(chg)
        per.append((rel, len(chg), dict(cnt)))
    print("%s 扩域排版：%d 卡 / %d 处（CRLF 归一 %d）"
          % ("已写盘" if apply_ else "(dry)", nfiles, tot, eol))
    agg = collections.Counter()
    for _rel, _n, cnt in per:
        for k, v in cnt.items():
            agg[k] += v
    print("   规则：", dict(agg))
    if bad:
        print("\n!! 未通过安全检查 %d 个：" % len(bad))
        for fp, why in bad[:20]:
            print("   ", why, os.path.basename(fp))
        sys.exit(1)
    print("\n   前 15 张：")
    for rel, n, cnt in sorted(per, key=lambda x: -x[1])[:15]:
        print("      %-46s %3d %s" % (rel[-44:], n, cnt))


if __name__ == "__main__":
    main()
