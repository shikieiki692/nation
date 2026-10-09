# -*- coding: utf-8 -*-
"""把「化学式排版」规则（fspace/fbase/fbase2/fempty）**直接**打到卷 md 上。

为什么不用重出：XII/XIII 的**人工题名**（`volpost --titles`）与**结构化解析**
（`add_analysis`）是**卷 md 层**的产物，`build_org` 重建会抹掉（2026-10-09 实测）。
⇒ 「重出一遍」= 源卡做全局 fmt（库级一致）＋ 卷 md 做**最小改动** fmt（只动排版）。

安全检查：① 可见字符指纹一致（只动定界符/空白）；② 幂等；③ 备份。
用法：`python fmt_formula_volmd.py [--apply]`
"""
import os, re, sys, glob, shutil, datetime, collections

HERE = r"C:\Obsidion\妙妙屋\.workbuddy\tmp\opt_pipe"
sys.path.insert(0, HERE)
import volpost  # noqa

R = r"C:\Obsidion\妙妙屋"
BAK = os.path.join(HERE, "volmd_bak_formula")
WANT = ("fspace", "fbase", "fbase2", "fempty")
RULES = [(n, r, p) for n, r, p in volpost.RULES if n in WANT]

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
    files = sorted(glob.glob(os.path.join(R, "04-题库/初赛模拟卷*（非有机·*版）.md")))
    tot, nf, bad = 0, 0, []
    for fp in files:
        raw = open(fp, encoding="utf-8-sig").read()
        eol = "\r\n" in raw
        if eol:
            raw = raw.replace("\r\n", "\n")
        new, chg = apply_rules(raw)
        if new == raw:
            continue
        if VIS.sub("", raw) != VIS.sub("", new):
            bad.append((fp, "可见字符改变"))
            continue
        again, _ = apply_rules(new)
        if again != new:
            bad.append((fp, "非幂等"))
            continue
        nf += 1
        tot += len(chg)
        cnt = collections.Counter(c[0] for c in chg)
        print("   %-46s %3d %s" % (os.path.basename(fp)[:44], len(chg), dict(cnt)))
        if apply_:
            shutil.copy2(fp, os.path.join(BAK, os.path.basename(fp) + ".bak-" + stamp))
            with open(fp, "w", encoding="utf-8", newline="\n") as f:
                f.write(new)
    print("%s 卷 md 化学式排版：%d 文件 / %d 处" % ("已写盘" if apply_ else "(dry)", nf, tot))
    if bad:
        print("!! 未通过 %d" % len(bad))
        for f, w in bad:
            print("   ", w, os.path.basename(f))
        sys.exit(1)


if __name__ == "__main__":
    main()
