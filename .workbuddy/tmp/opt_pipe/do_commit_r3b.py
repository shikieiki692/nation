# -*- coding: utf-8 -*-
"""第二轮提交：列感知裁图 + 整册卡精简 + 答案解析 + 闸门伪判据修正（隔离索引 + 分块 add）。"""
import glob, os, subprocess, sys, time
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


names = set()
for d in ("gcho_ans_backup", "analysis_backup", "booklet_backup"):
    for f in glob.glob(os.path.join(O, d, "*.orig")):
        names.add(os.path.basename(f)[:-5])
PATHS = []
for nm in sorted(names):
    hits = glob.glob(os.path.join(ROOT, "04-题库", "**", nm), recursive=True)
    if hits:
        PATHS.append(os.path.relpath(hits[0], ROOT))
    else:
        print("  ! 未找到卡:", nm)
st = run("status", "--porcelain", "-uall", "--", "04-题库/2026机构初赛模拟题/质心GChO").stdout.decode("utf-8", "replace")
for line in st.split("\n"):
    if line.strip():
        PATHS.append(line[3:].strip().strip('"'))
PATHS += [
    "04-题库/初赛模拟卷XI（非有机·答案版）.md",
    "04-题库/初赛模拟卷XI（非有机·学生版）.md",
    "00-首页/题组Word/初赛模拟卷/真题版式/初赛模拟卷XI（非有机·答案与解析版·真题版式）.docx",
    "00-首页/题组Word/初赛模拟卷/真题版式/初赛模拟卷XI（非有机·学生版·真题版式）.docx",
    "00-首页/题组Word/初赛模拟卷/真题版式/初赛模拟卷XIp（非有机·学生版·真题版式）.docx",
    "00-首页/题组Word/初赛模拟卷/真题版式/初赛模拟卷XIp（非有机·答案与解析版·真题版式）.docx",
    "09-审计报告/2026-10-07-GChO手写稿答案治理与质量提升方案.md",
    ".workbuddy/memory/MEMORY.md",
    ".workbuddy/memory/2026-10-07.md",
]
for t in ("gcho_crop.py", "fix_gap3.py", "trim_booklet.py", "add_analysis.py", "find_ans16.py",
          "build_org.py", "do_commit_gcho.py", "add_gcho_allow.py", "booklet_log.txt",
          "apply_log4.txt", "vol_plan_XI.json", "gcho_preflight.py", "gc_gcho_imgs.py",
          "verify_gcho_crop.py", "gcho_batch_apply.py", "do_commit_r3b.py", "msg_r2.txt",
          "patch_ph.py", "patch_ans_gate.py"):
    if os.path.exists(os.path.join(O, t)):
        PATHS.append(O + "/" + t)
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
    r = subprocess.run(["git", "commit", "-F", O + "/msg_r2.txt"], capture_output=True, env=ENV, timeout=1800)
    out = (r.stdout + r.stderr).decode("utf-8", "replace")
    if r.returncode == 0:
        print("提交成功（第 %d 轮）：" % k)
        for l in out.split("\n")[:8]:
            if l.strip():
                print("  " + l[:130])
        ok = True
        break
    if "cannot lock ref 'HEAD'" in out or "but expected" in out:
        print("第 %d 轮遇 HEAD 竞态，10s 后重试" % k); time.sleep(10); continue
    print("第 %d 轮失败：\n%s" % (k, out[:900])); sys.exit("中止")
if os.path.exists(IDX):
    os.remove(IDX)
if ok:
    for i in range(0, len(PATHS), 60):
        run("reset", "-q", "HEAD", "--", *PATHS[i:i + 60])
    print("主索引已同步")
print("HEAD = %s" % run("log", "-1", "--oneline").stdout.decode("utf-8").strip())
