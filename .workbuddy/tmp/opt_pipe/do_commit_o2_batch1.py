# -*- coding: utf-8 -*-
"""卷 O2 解析加厚 批1（Q1–4 ＋ Q8 标杆落库）提交 —— 隔离索引 ＋ 逐路径精确 add。

铁律：① 只 add 本会话改动文件；② 隔离索引 commit；③ 提交后 git reset 清主索引残留。
"""
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Obsidion\妙妙屋"
IDX = os.path.join(ROOT, ".workbuddy", "tmp", "_idx_o2_batch1")

PURE = [
    "04-题库/初赛模拟卷O2（有机·答案版）.md",
    "00-首页/题组Word/初赛模拟卷/真题版式/初赛模拟卷O2（有机·答案与解析版·真题版式）.docx",
]
# .workbuddy/tmp/ 被 ignore ⇒ 需 -f
FORCE = [
    ".workbuddy/tmp/opt_pipe/anO2_new1.py",
    ".workbuddy/tmp/opt_pipe/del_old_analysis_O2.py",
]

MSG = """feat(组卷): O2 解析加厚**批1**（Q1–4 六维 ＋ Q8 标杆落库）

- Q1–4 按 owner 2026-10-16 六维口径重写解析（判据直引／答案图逐张落位／分步推导含数值／
  得分点拆解／举一反三／教材溯源）；Q8 标杆数据（anO2_probe_Q8.py）一并落库。
- 入库量：Q1–4 引 27 处 [[ ]] 真链接、直引 KP 定量/结论 30+ 条、答案图落位 24 张、
  举一反三 16 条、溯源 12 条；Q5–7/Q9–10 暂沿用旧稿（下批替换）。
- 新增：anO2_new1.py（Q1–4 数据）、del_old_analysis_O2.py（幂等删旧块，供后续批次复用）。
- 验收：qa_vol_all 8 闸门 ALL PASS（④ 结构终检 0）｜pipe_tbl_audit 异常 0｜
  vol_poolchk 掉池 0｜fm_strict FAIL 0｜validate_kb Error 0。
- 口径要点：题面已出现的图不清答（只落位解答新图＋答案行文字标注，但题面图仍逐张目检）；
  知识点一律 [[页名]] wikilink（docx 侧剥方括号、无副作用）。
"""


def run(args, env=None, check=True):
    r = subprocess.run(args, cwd=ROOT, env=env, capture_output=True)
    if check and r.returncode != 0:
        print("FAIL:", args)
        print(r.stdout.decode("utf-8", "replace")[-1500:])
        print(r.stderr.decode("utf-8", "replace")[-1500:])
        sys.exit(1)
    return r


def main():
    if os.path.exists(IDX):
        os.remove(IDX)
    env = {**os.environ, "GIT_INDEX_FILE": IDX}
    run(["git", "read-tree", "HEAD"], env)
    run(["git", "add", "-f", "--"] + PURE + FORCE, env)
    staged = [p for p in run(["git", "diff", "--cached", "--name-only", "-z"], env)
              .stdout.decode("utf-8").split("\0") if p]
    want = set(PURE) | set(FORCE)
    if set(staged) != want:
        print("!! 暂存集合 != 预期")
        print("  多:", sorted(set(staged) - want))
        print("  少:", sorted(want - set(staged)))
        sys.exit(1)
    print("暂存核对 OK：%d 个路径" % len(staged))
    r = run(["git", "commit", "-m", MSG], env, check=False)
    print((r.stdout + r.stderr).decode("utf-8", "replace")[-1200:])
    if r.returncode != 0:
        sys.exit(1)
    main_env = {k: v for k, v in os.environ.items() if k != "GIT_INDEX_FILE"}
    # ③ 清主索引残留（隔离索引 commit 会污染主索引）
    print("主索引残留（reset 前）:", run(["git", "diff", "--cached", "--name-only"], main_env)
          .stdout.decode("utf-8", "replace").strip()[:300] or "（空）")
    run(["git", "reset", "-q", "HEAD", "--"] + PURE + FORCE, main_env)
    left = run(["git", "diff", "--cached", "--name-only"], main_env).stdout.decode("utf-8").strip()
    print("主索引残留（reset 后）行数 =", len([x for x in left.split("\n") if x]))
    print("HEAD:", run(["git", "log", "--oneline", "-1"], main_env).stdout.decode("utf-8").strip())


if __name__ == "__main__":
    main()
