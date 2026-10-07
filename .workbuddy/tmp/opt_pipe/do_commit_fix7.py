# -*- coding: utf-8 -*-
"""提交：注记行剥离 + 4 张题面尾答案册标题。隔离索引＋竞态重试。"""
import os, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Obsidion\妙妙屋"
os.chdir(ROOT)
IDX = os.path.join(ROOT, ".git", "wb_idx_tmp5d")
ENV = dict(os.environ, GIT_INDEX_FILE=IDX)
O = ".workbuddy/tmp/opt_pipe"


def run(*a, env=None):
    return subprocess.run(["git", "-c", "core.quotepath=false"] + list(a),
                          capture_output=True, env=env or os.environ)


def norm(x):
    return x.replace("\\", "/")


PATHS = [
    "04-题库/2026机构初赛模拟题/化英社/题-HYS-01-10-具有吗啡骨架的化合物是一类常.md",
    "04-题库/2026机构初赛模拟题/化英社/题-HYS-02-10-101以下是两个十分经典的反.md",
    "04-题库/2026机构初赛模拟题/汇智/题-HZ-38-08-的晶胞参数为.md",
    "04-题库/2026机构初赛模拟题/汇智/题-HZ-01-09-某无色有机底物S在酸性水溶液.md",
    "09-审计报告/2026-10-07-不可组卷题目清单.md",
    "09-审计报告/2026-10-07-不可组卷题目清单.csv",
    "09-审计报告/2026-10-07-A类不可用题目处置清单.md",
    "11-模板/scripts/render_gate_allowlist.txt",
    ".workbuddy/memory/MEMORY.md",
    ".workbuddy/memory/2026-10-07.md",
]
for t in ("build_org.py", "make_reject_report.py", "scan_tail_sig.py", "scan_tail_sig2.py",
          "check37.py", "count_tailhead.py", "dump4tail.py", "fix_tailhead4.py", "count_notes.py",
          "do_commit_fix7.py", "msg_fix7.txt"):
    if os.path.exists(os.path.join(O, t)):
        PATHS.append(O + "/" + t)
PATHS = list(dict.fromkeys(PATHS))
miss = [p for p in PATHS if not os.path.exists(p)]
if miss:
    sys.exit("磁盘缺失：%s" % miss)
want = {norm(p) for p in PATHS}
print("本会话路径 %d 条" % len(PATHS))
ok = False
for k in range(1, 9):
    if os.path.exists(IDX):
        os.remove(IDX)
    if run("read-tree", "HEAD", env=ENV).returncode != 0:
        sys.exit("read-tree 失败")
    for i in range(0, len(PATHS), 60):
        r = run("add", "-f", "--", *PATHS[i:i + 60], env=ENV)
        if r.returncode != 0:
            sys.exit("add 失败：" + r.stderr.decode("utf-8", "replace")[:300])
    cur = {norm(x) for x in run("diff", "--cached", "--name-only", "-z", env=ENV).stdout.decode("utf-8").split("\0") if x}
    extra = cur - want
    if extra:
        sys.exit("中止：隔离索引多出 %s" % sorted(extra)[:5])
    bad = [m for m in (want - cur) if run("diff", "--quiet", "HEAD", "--", m).returncode != 0]
    if bad:
        sys.exit("中止：%s 有改动却未入暂存" % bad[:5])
    print("第 %d 轮：暂存 %d（期望 %d）" % (k, len(cur), len(want)))
    r = subprocess.run(["git", "commit", "-F", O + "/msg_fix7.txt"], capture_output=True, env=ENV, timeout=1800)
    out = (r.stdout + r.stderr).decode("utf-8", "replace")
    if r.returncode == 0:
        print("提交成功（第 %d 轮）：" % k)
        for l in out.split("\n")[:6]:
            if l.strip():
                print("  " + l[:130])
        ok = True
        break
    if "cannot lock ref 'HEAD'" in out or "but expected" in out:
        print("第 %d 轮遇 HEAD 竞态，10s 后重试" % k); time.sleep(10); continue
    print("第 %d 轮失败：\n%s" % (k, out[:2000])); sys.exit("中止")
if os.path.exists(IDX):
    os.remove(IDX)
if ok:
    for i in range(0, len(PATHS), 60):
        run("reset", "-q", "HEAD", "--", *PATHS[i:i + 60])
    print("主索引已同步")
print("HEAD = %s" % run("log", "-1", "--oneline").stdout.decode("utf-8").strip())
