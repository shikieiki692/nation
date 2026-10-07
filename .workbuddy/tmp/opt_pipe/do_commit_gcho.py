# -*- coding: utf-8 -*-
"""GChO 手写稿答案治理 —— 提交（隔离索引 + 竞态重试 + 分块 add + 主索引同步）。"""
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


# 1) 收集本会话路径
PATHS = []
st = run("status", "--porcelain", "--", "04-题库/2026机构初赛模拟题/质心GChO").stdout.decode("utf-8", "replace")
for line in st.split("\n"):
    if not line.strip():
        continue
    p = line[3:].strip().strip('"')
    if p:
        PATHS.append(p)
PATHS += [
    "09-审计报告/2026-10-07-GChO手写稿答案治理与质量提升方案.md",
    "11-模板/scripts/render_gate_allowlist.txt",
    ".workbuddy/memory/MEMORY.md",
    ".workbuddy/memory/2026-10-07.md",
]
TOOLS = ["gcho_crop.py", "gcho_batch_apply.py", "gcho_preflight.py", "ocr_batch_gcho.py",
         "verify_gcho_crop.py", "gc_gcho_imgs.py", "patch_ans_gate.py", "patch_ph.py",
         "sample_garb2.py", "build_org.py", "trim_overflow.py", "do_commit_gcho.py",
         "add_gcho_allow.py", "fix_gap3.py", "msg_gcho.txt", "overflow_hits.csv",
         "gcho_audit.tsv", "apply_log.txt", "apply_log2.txt", "apply_log3.txt",
         "apply_log4.txt", "ocr_log2.txt"]
PATHS += [O + "/" + t for t in TOOLS if os.path.exists(os.path.join(O, t))]

PATHS = list(dict.fromkeys(PATHS))
miss = [p for p in PATHS if not os.path.exists(p)]
if miss:
    sys.exit("磁盘缺失 %d：%s" % (len(miss), miss[:5]))
want = {norm(p) for p in PATHS}
print("本会话路径 %d 条" % len(PATHS))

ok = False
for k in range(1, 9):
    if os.path.exists(IDX):
        os.remove(IDX)
    if run("read-tree", "HEAD", env=ENV).returncode != 0:
        sys.exit("read-tree 失败")
    for i in range(0, len(PATHS), 80):                    # 分块，防 WinError 206
        chunk = PATHS[i:i + 80]
        r = run("add", "-f", "--", *chunk, env=ENV)
        if r.returncode != 0:
            sys.exit("add 失败：" + r.stderr.decode("utf-8", "replace")[:300])
    out = run("diff", "--cached", "--name-only", "-z", env=ENV).stdout.decode("utf-8")
    cur = {norm(x) for x in out.split("\0") if x}
    extra = cur - want
    if extra:
        sys.exit("中止：隔离索引多出 %s" % sorted(extra)[:5])
    bad = [m for m in (want - cur) if run("diff", "--quiet", "HEAD", "--", m).returncode != 0]
    if bad:
        sys.exit("中止：%s 有改动却未入暂存" % bad[:5])
    print("第 %d 轮：暂存 %d（期望 %d，未变 %d）" % (k, len(cur), len(want), len(want - cur)))
    r = subprocess.run(["git", "commit", "-F", O + "/msg_gcho.txt"], capture_output=True, env=ENV, timeout=1200)
    out = r.stdout.decode("utf-8", "replace") + r.stderr.decode("utf-8", "replace")
    if r.returncode == 0:
        print("提交成功（第 %d 轮）：" % k)
        for l in out.split("\n")[:8]:
            if l.strip():
                print("  " + l[:130])
        ok = True
        break
    if "cannot lock ref 'HEAD'" in out or "but expected" in out:
        print("第 %d 轮遇 HEAD 竞态，10s 后重试" % k); time.sleep(10); continue
    print("第 %d 轮失败（非竞态）：\n%s" % (k, out[:900]))
    sys.exit("中止")

if os.path.exists(IDX):
    os.remove(IDX)
if ok:
    for i in range(0, len(PATHS), 80):
        run("reset", "-q", "HEAD", "--", *PATHS[i:i + 80])
    print("主索引已同步本会话路径")
print("HEAD = %s" % run("log", "-1", "--oneline").stdout.decode("utf-8").strip())
