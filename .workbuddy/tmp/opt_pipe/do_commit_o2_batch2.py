# -*- coding: utf-8 -*-
"""卷 O2 解析加厚 批2（Q5–7 六维）提交 —— 隔离索引 ＋ 逐路径精确 add。"""
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Obsidion\妙妙屋"
IDX = os.path.join(ROOT, ".workbuddy", "tmp", "_idx_o2_batch2")

PURE = [
    "04-题库/初赛模拟卷O2（有机·答案版）.md",
    "00-首页/题组Word/初赛模拟卷/真题版式/初赛模拟卷O2（有机·答案与解析版·真题版式）.docx",
]
FORCE = [
    ".workbuddy/tmp/opt_pipe/anO2_new2.py",
]

MSG = """feat(组卷): O2 解析加厚**批2**（Q5–7 六维）

- Q5（三钴碳化物簇，原卷 26 分档）／Q6（复杂 Wittig 重排）／Q7（TPE-UPy 超分子凝胶）
  按六维口径重写：判据直引／答案图逐张落位／分步推导含数值／得分点拆解／举一反三／溯源。
- 判据直引亮点：多核簇 §3.2 电子计数＋§3.3 三角构型表＋§四 μ-配体作用（Q5）；
  σ迁移反应/Woodward-Hoffmann/离子对机理（Q6）；超分子聚合物 §五「UPy 四重氢键 K_dim≈10⁶」
  ＋§3.3 Fujita 发散原理＋浓度效应＋¹H NMR 易错点「–NH 宽峰」（Q7）。
- 源级缺口登记（非本会话引入）：Q6 6-4-1 的 G/H 结构图在源卡答案表内即**空单元格** ⇒
  解析按卷内给分口径（G 3 分＋C–H···N 2 分＋N–H···O 1 分；H 2 分）落位并标注，不臆造结构；
  Q2 2-1-2 的 X 结构图同为源卡 `[IMAGE]` 占位（批1 已登记）。
- 验收：qa_vol_all 8 闸门 ALL PASS（④ 结构终检 0）｜pipe_tbl_audit 异常 0｜vol_poolchk 掉池 0｜
  fm_strict FAIL 0｜validate_kb Error 0。
- 自检：考点/易错 各 10；举一反三/溯源 各 8（Q1–8 新稿）。
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
    print((r.stdout + r.stderr).decode("utf-8", "replace")[-1000:])
    if r.returncode != 0:
        sys.exit(1)
    main_env = {k: v for k, v in os.environ.items() if k != "GIT_INDEX_FILE"}
    run(["git", "reset", "-q", "HEAD", "--"] + PURE + FORCE, main_env)
    left = run(["git", "diff", "--cached", "--name-only"], main_env).stdout.decode("utf-8").strip()
    print("主索引残留（reset 后）行数 =", len([x for x in left.split("\n") if x]))
    print("HEAD:", run(["git", "log", "--oneline", "-1"], main_env).stdout.decode("utf-8").strip())


if __name__ == "__main__":
    main()
