# -*- coding: utf-8 -*-
"""补提交：替代建议表行拼接修复。"""
import os, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Obsidion\妙妙屋"
os.chdir(ROOT)
IDX = os.path.join(ROOT, ".git", "wb_idx_tmp5f")
ENV = dict(os.environ, GIT_INDEX_FILE=IDX)
O = ".workbuddy/tmp/opt_pipe"


def run(*a, env=None):
    return subprocess.run(["git", "-c", "core.quotepath=false"] + list(a), capture_output=True, env=env or os.environ)


PATHS = ["09-审计报告/2026-10-07-A类待换卡替代建议.md",
         O + "/make_replace_list.py", O + "/do_commit_fix9.py", O + "/msg_fix9.txt"]
want = {p.replace("\\", "/") for p in PATHS}
for k in range(1, 9):
    if os.path.exists(IDX):
        os.remove(IDX)
    if run("read-tree", "HEAD", env=ENV).returncode != 0:
        sys.exit("read-tree 失败")
    r = run("add", "-f", "--", *PATHS, env=ENV)
    if r.returncode != 0:
        sys.exit("add 失败")
    cur = {x.replace("\\", "/") for x in run("diff", "--cached", "--name-only", "-z", env=ENV).stdout.decode("utf-8").split("\0") if x}
    if cur - want:
        sys.exit("中止：多出 %s" % sorted(cur - want)[:5])
    print("第 %d 轮：暂存 %d" % (k, len(cur)))
    r = subprocess.run(["git", "commit", "-F", O + "/msg_fix9.txt"], capture_output=True, env=ENV, timeout=1800)
    out = (r.stdout + r.stderr).decode("utf-8", "replace")
    if r.returncode == 0:
        print("提交成功：")
        print("  " + out.split("\n")[0][:120])
        break
    if "cannot lock ref 'HEAD'" in out or "but expected" in out:
        time.sleep(10)
        continue
    sys.exit("失败：\n" + out[:1500])
if os.path.exists(IDX):
    os.remove(IDX)
for i in range(0, len(PATHS), 60):
    run("reset", "-q", "HEAD", "--", *PATHS[i:i + 60])
print("HEAD = %s" % run("log", "-1", "--oneline").stdout.decode("utf-8").strip())
