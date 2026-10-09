# -*- coding: utf-8 -*-
"""统计「卷 md 相对 HEAD 的化学式排版改动处数」（规则应用次数，非行数）。"""
import os, subprocess, sys, collections
HERE = r"C:\Obsidion\妙妙屋\.workbuddy\tmp\opt_pipe"
sys.path.insert(0, HERE)
import volpost  # noqa

R = r"C:\Obsidion\妙妙屋"
WANT = ("fspace", "fbase", "fbase2", "fempty")
RULES = [(n, r, p) for n, r, p in volpost.RULES if n in WANT]


def apply_rules(t):
    n = 0
    cnt = collections.Counter()
    for name, rx, rep in RULES:
        def _sub(m, _rep=rep, _name=name):
            nonlocal n
            n += 1; cnt[_name] += 1
            return _rep(m) if callable(_rep) else m.expand(_rep)
        t = rx.sub(_sub, t)
    return t, n, cnt


out = subprocess.run(["git", "-c", "core.quotepath=false", "status", "--porcelain"], cwd=R,
                     capture_output=True, text=True, encoding="utf-8").stdout
files = [l[3:].strip().strip('"') for l in out.splitlines()
         if "初赛模拟卷" in l and l[3:].strip().strip('"').endswith(".md")]
tot = 0
agg = collections.Counter()
for p in files:
    raw = open(os.path.join(R, p), encoding="utf-8-sig").read()
    head = subprocess.run(["git", "show", f"HEAD:{p}"], cwd=R, capture_output=True).stdout.decode("utf-8-sig")
    _, n, cnt = apply_rules(head)
    tot += n
    agg.update(cnt)
    print("  %-44s %3d %s" % (os.path.basename(p)[:42], n, dict(cnt)))
print("卷 md 合计：%d 文件 / %d 处 %s" % (len(files), tot, dict(agg)))
