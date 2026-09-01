# -*- coding: utf-8 -*-
"""
阶段六：空间回收（用户已确认）

1. .kb/state/ 删 3 个归档 checkpoint + reverse_index.json —— 336 MB
   依据：manager.js 的 loadCheckpoint() 只读 checkpoint.jsonl；
        rotateCheckpoint() 只写不读 .1/.2/.3；grep 整个 dist 目录确认无读取点。
        reverse_index.json 由 kb_index 工具重建。
   保留：checkpoint.jsonl（当前快照，系统在用）

2. .workbuddy/ 删 tmp/ + _render/ —— 88 MB
   tmp/ 为本轮运行中间产物（已 gitignore，可重跑生成）
   _render/ 为 Word 管线对比渲染，全库无 md 引用；其中 4 个 PNG 已入库，需一并 git rm

3. dependency-map.json 加入 .gitignore + 从索引移除（文件保留在磁盘）
"""
import os
import shutil
import subprocess

VAULT = r"C:\Obsidion\妙妙屋"


def sz(p):
    return os.path.getsize(p) if os.path.isfile(p) else 0


def dsz(p):
    if not os.path.isdir(p):
        return 0
    t = 0
    for r, _, fs in os.walk(p):
        for f in fs:
            try:
                t += os.path.getsize(os.path.join(r, f))
            except OSError:
                pass
    return t


freed = []

# ---------- 1. .kb/state ----------
kb = os.path.join(VAULT, ".kb", "state")
targets = ["checkpoint.1.jsonl", "checkpoint.2.jsonl", "checkpoint.3.jsonl",
           "reverse_index.json"]
print("=== 1. .kb/state 归档清理 ===")
for fn in targets:
    p = os.path.join(kb, fn)
    if os.path.exists(p):
        s = sz(p)
        os.remove(p)
        freed.append((f".kb/state/{fn}", s))
        print(f"  已删 {s/1024/1024:8.1f} MB  {fn}")
# 复核：当前快照必须还在
cur = os.path.join(kb, "checkpoint.jsonl")
print(f"  保留 checkpoint.jsonl：{'存在' if os.path.exists(cur) else '缺失!!'} ({sz(cur)/1024/1024:.1f} MB)")

# ---------- 2. .workbuddy ----------
print("\n=== 2. .workbuddy 清理 ===")
for d in ["tmp", "_render"]:
    p = os.path.join(VAULT, ".workbuddy", d)
    if os.path.isdir(p):
        s = dsz(p)
        shutil.rmtree(p)
        freed.append((f".workbuddy/{d}/", s))
        print(f"  已删 {s/1024/1024:8.1f} MB  {d}/")

# 4 个已入库的 PNG 从索引移除
tracked = subprocess.run(
    ["git", "-c", "core.quotepath=false", "ls-files", ".workbuddy/_render"],
    capture_output=True, cwd=VAULT).stdout.decode("utf-8").splitlines()
tracked = [t.strip().strip('"') for t in tracked if t.strip()]
if tracked:
    subprocess.run(["git", "rm", "--cached", "--quiet", "--"] + tracked,
                   cwd=VAULT, check=False)
    print(f"  已从索引移除 {len(tracked)} 个已跟踪的 PNG")

# ---------- 3. dependency-map.json ----------
print("\n=== 3. dependency-map.json 忽略 ===")
DM_REL = "02-数据库/dependency-map.json"
dm = os.path.join(VAULT, DM_REL)
in_index = subprocess.run(["git", "ls-files", "--error-unmatch", DM_REL],
                          capture_output=True, cwd=VAULT).returncode == 0
if in_index:
    subprocess.run(["git", "rm", "--cached", "--quiet", "--", DM_REL],
                   cwd=VAULT, check=False)
    print(f"  已从索引移除（磁盘保留 {sz(dm)/1024/1024:.2f} MB）")
else:
    print("  本就不在索引中")

GI = os.path.join(VAULT, ".gitignore")
txt = open(GI, encoding="utf-8").read()
line = "02-数据库/dependency-map.json"
if "dependency-map.json" not in txt:
    if not txt.endswith("\n"):
        txt += "\n"
    txt += f"\n# 校验器每次全量重生成的依赖图（6.5 MB，每次提交 churn 约 20 万行）\n{line}\n"
    open(GI, "w", encoding="utf-8", newline="").write(txt)
    print("  已追加 .gitignore 规则")
else:
    print("  .gitignore 已含该规则")

total = sum(s for _, s in freed)
print(f"\n=== 释放磁盘 {total/1024/1024:.1f} MB ===")
for label, s in freed:
    print(f"  {s/1024/1024:8.1f} MB  {label}")
