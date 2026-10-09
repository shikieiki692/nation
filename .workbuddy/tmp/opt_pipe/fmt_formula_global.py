# -*- coding: utf-8 -*-
"""全局「化学式排版」修复：只跑 `fspace` / `fbase` / `fempty` 三条**纯格式**规则。

- 目标：`04-题库/2026机构初赛模拟题/**/题-*.md`（源卡）
- 安全检查：
  1. 逐文件断言「去掉数学定界符/`\\mathrm`/空白后，可见字符完全一致」——证明只动了排版；
  2. 幂等：二次运行应报 0 处；
  3. 备份到 `.workbuddy/tmp/opt_pipe/card_bak_globalfmt/`。
用法：`python fmt_formula_global.py [--apply]`
"""
import os, re, sys, glob, shutil, datetime, collections

HERE = r"C:\Obsidion\妙妙屋\.workbuddy\tmp\opt_pipe"
sys.path.insert(0, HERE)
import volpost  # noqa

R = r"C:\Obsidion\妙妙屋"
Q = os.path.join(R, "04-题库/2026机构初赛模拟题")
BAK = os.path.join(HERE, "card_bak_globalfmt")
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
    """可见字符指纹：去数学定界符、组括号、`\\mathrm`、空白。"""
    return VIS.sub("", t)


def main():
    apply_ = "--apply" in sys.argv
    stamp = datetime.datetime.now().strftime("%m%d_%H%M")
    if apply_:
        os.makedirs(BAK, exist_ok=True)
    files = sorted(glob.glob(os.path.join(Q, "**", "题-*.md"), recursive=True))
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
        # ① 可见字符不变（只动排版）
        if visible(raw) != visible(new):
            bad.append((fp, "可见字符改变"))
            continue
        # ② 幂等
        again, _ = apply_rules(new)
        if again != new:
            bad.append((fp, "非幂等"))
            continue
        nfiles += 1
        tot += len(chg)
        cnt = collections.Counter(c[0] for c in chg)
        per.append((os.path.relpath(fp, R).replace("\\", "/"), len(chg), dict(cnt)))
        if apply_:
            shutil.copy2(fp, os.path.join(BAK, os.path.basename(fp) + ".bak-" + stamp))
            with open(fp, "w", encoding="utf-8", newline="\n") as f:
                f.write(new)

    print("%s 化学式排版：%d 卡 / %d 处（CRLF 归一 %d）"
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
    print("\n   前 12 张：")
    for rel, n, cnt in per[:12]:
        print("      %-44s %3d %s" % (os.path.basename(rel)[:42], n, cnt))


if __name__ == "__main__":
    main()
