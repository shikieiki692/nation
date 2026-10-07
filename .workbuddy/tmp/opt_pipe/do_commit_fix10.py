# -*- coding: utf-8 -*-
"""提交收口：GChO-63-07 回源裁图救回 + 报告 + 记忆。隔离索引＋竞态重试。"""
import os, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Obsidion\妙妙屋"
os.chdir(ROOT)
IDX = os.path.join(ROOT, ".git", "wb_idx_tmp5g")
ENV = dict(os.environ, GIT_INDEX_FILE=IDX)
O = ".workbuddy/tmp/opt_pipe"
IMG = ("04-题库/2026机构初赛模拟题/质心GChO/images/"
       "5d4d4010f41da5ef340eef815e918d524c2e306c9ee0d1b5a693248f9e98ed63.jpg")


def run(*a, env=None):
    return subprocess.run(["git", "-c", "core.quotepath=false"] + list(a),
                          capture_output=True, env=env or os.environ)


def norm(x):
    return x.replace("\\", "/")


PATHS = [
    "04-题库/2026机构初赛模拟题/质心GChO/题-GChO-63-07-如下的转化在Lewis酸的催.md",
    IMG,
    "09-审计报告/2026-10-07-不可组卷题目清单.md",
    "09-审计报告/2026-10-07-不可组卷题目清单.csv",
    "09-审计报告/2026-10-07-A类不可用题目处置清单.md",
    "09-审计报告/2026-10-07-A类待换卡替代建议.md",
    ".workbuddy/memory/MEMORY.md",
    ".workbuddy/memory/2026-10-07.md",
]
for t in ("make_reject_report.py", "make_replace_list.py", "look_hys2.py", "diff_hys2.py",
          "hys2_struct.py", "check_pair.py", "xec03.py", "gm25.py", "a_zone12.py",
          "test_rev_echo.py", "find_gcho63.py", "crop_gcho63.py", "rescue_gcho6307.py",
          "rescue_gcho6307b.py", "do_commit_fix10.py", "msg_fix10.txt"):
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
    r = subprocess.run(["git", "commit", "-F", O + "/msg_fix10.txt"], capture_output=True, env=ENV, timeout=1800)
    out = (r.stdout + r.stderr).decode("utf-8", "replace")
    if r.returncode == 0:
        print("提交成功（第 %d 轮）：" % k)
        for l in out.split("\n")[:5]:
            if l.strip():
                print("  " + l[:130])
        ok = True
        break
    if "cannot lock ref 'HEAD'" in out or "but expected" in out:
        print("第 %d 轮遇 HEAD 竞态，10s 后重试" % k)
        time.sleep(10)
        continue
    print("第 %d 轮失败：\n%s" % (k, out[:2500]))
    sys.exit("中止")
if os.path.exists(IDX):
    os.remove(IDX)
if ok:
    for i in range(0, len(PATHS), 60):
        run("reset", "-q", "HEAD", "--", *PATHS[i:i + 60])
    print("主索引已同步")
print("HEAD = %s" % run("log", "-1", "--oneline").stdout.decode("utf-8").strip())
