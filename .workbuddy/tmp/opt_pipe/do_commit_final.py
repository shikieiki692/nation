# -*- coding: utf-8 -*-
"""提交：机构模拟题救援收尾（越界清零＋题面泄露分类救援）。隔离索引＋竞态重试。"""
import os, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Obsidion\妙妙屋"
os.chdir(ROOT)
IDX = os.path.join(ROOT, ".git", "wb_idx_tmp")
ENV = dict(os.environ, GIT_INDEX_FILE=IDX)
O = ".workbuddy/tmp/opt_pipe"


def run(*a, env=None):
    return subprocess.run(["git", "-c", "core.quotepath=false"] + list(a),
                          capture_output=True, env=env or os.environ)


def norm(x):
    return x.replace("\\", "/")


PATHS = []
EXCL = {"04-题库/2026机构初赛模拟题/汇智/题-HZ-03-06-麦克斯韦妖Maxwellsd.md"}
for line in run("status", "--porcelain", "-uall", "--",
                "04-题库/2026机构初赛模拟题").stdout.decode("utf-8", "replace").split("\n"):
    if not line.strip():
        continue
    p = line[3:].strip().strip('"')
    if norm(p) in EXCL:
        print("  跳过（并行会话）:", p); continue
    PATHS.append(p)
PATHS += [
    "09-审计报告/2026-10-07-不可组卷题目清单.md",
    "09-审计报告/2026-10-07-不可组卷题目清单.csv",
    "11-模板/scripts/render_gate_allowlist.txt",
    ".workbuddy/memory/MEMORY.md",
    ".workbuddy/memory/2026-10-07.md",
]
for t in ("build_org.py", "audit_pool_reject.py", "make_reject_report.py",
          "overflow_hits.csv", "vol_plan_XI.json",
          "rescue_ovf2.py", "rescue_leak2.py", "check_keep.py", "risk_ovf.py",
          "ctx_leak.py", "dump_exact.py", "test_leak_cut3.py", "test_leak_cut2.py",
          "diag_leak30.py", "diag_ovf_tok2.py", "fix_cm6904.py", "fix_hys0106.py",
          "fix_xec4002.py", "add_allow_final.py", "do_commit_final.py", "msg_final.txt"):
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
    r = subprocess.run(["git", "commit", "-F", O + "/msg_final.txt"], capture_output=True, env=ENV, timeout=1800)
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
    print("第 %d 轮失败：\n%s" % (k, out[:1500])); sys.exit("中止")
if os.path.exists(IDX):
    os.remove(IDX)
if ok:
    for i in range(0, len(PATHS), 60):
        run("reset", "-q", "HEAD", "--", *PATHS[i:i + 60])
    print("主索引已同步")
print("HEAD = %s" % run("log", "-1", "--oneline").stdout.decode("utf-8").strip())
