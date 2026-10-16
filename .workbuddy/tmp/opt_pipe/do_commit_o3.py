# -*- coding: utf-8 -*-
"""卷 O3 建卷提交 —— 隔离索引 ＋ 逐路径精确 add。"""
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Obsidion\妙妙屋"
IDX = os.path.join(ROOT, ".workbuddy", "tmp", "_idx_o3")

PURE = [
    "04-题库/初赛模拟卷O3（有机·答案版）.md",
    "04-题库/初赛模拟卷O3（有机·学生版）.md",
    "00-首页/题组Word/初赛模拟卷/真题版式/初赛模拟卷O3（有机·答案与解析版·真题版式）.docx",
    "00-首页/题组Word/初赛模拟卷/真题版式/初赛模拟卷O3（有机·学生版·真题版式）.docx",
    "00-首页/题组Word/初赛模拟卷/真题版式/初赛模拟卷O3（有机·答题卡）.docx",
    ".workbuddy/scripts/figcov_keep.json",
]
FORCE = [
    ".workbuddy/tmp/opt_pipe/vol_plan_O3.json",
    ".workbuddy/tmp/opt_pipe/vol_meta_O3.json",
    ".workbuddy/tmp/opt_pipe/o3_topic_map.json",
    ".workbuddy/tmp/opt_pipe/o3_titles.json",
    ".workbuddy/tmp/opt_pipe/o3_tblfix.py",
    ".workbuddy/tmp/opt_pipe/do_commit_o3.py",
]

MSG = """feat(组卷): O3 有机卷建卷并交付（10 题／130 分／5 机构）

- build_org.py --vol O3 --organic --all-years --topic-map o3_topic_map.json
  （干跑确认 → 落盘；池自动排除 O2 的 10 张，全卷与 O2 零重题）。
- 选卡（两段各 5 题）：段一 有机合成与反应机理 = HYS-15-07（羟基共轭效应与 Pd 催化异构化）／
  QBY-07-08（furanocembranolide）／CM-198-09（提高反应选择性的策略）／GM-01-08（天然产物 Guignard 的合成）／
  YJ-03-07（DNA 化学）；段二 结构鉴定与立体化学 = HYS-15-08（含氟体系的立体电子效应）／
  QBY-13-01（轴手性）／CM-200-08（氨基酸的结构与性质）／GM-06-09（分子内 Mannich 反应）／
  YJ-07-05（低价主族元素化学）。
- 主题核定：逐卡读题面后确认**与分类器默认一致**（零对调）；曾试把 GM-06-09／YJ-07-05 调入段一，
  实测连带拉进 GM-03-01（高分子）／YJ-06-07（多环芳烃）⇒ 反而新增错位，故撤回（记录在 o3_topic_map._note）。
- 后处理：volpost --ans（4 题变动／重述转标签 6 处）＋ --titles（10 处人工核定题名）；
  卷级补丁 o3_tblfix.py（登记进 vol_meta_O3.post_patches，build 自动重放）：判噪剔图后 2 处表格塌列
  ＋ 水印标题行「清北营教育」＋ 3 处被提升为标题的分值注 ⇒ 全部修复（标题跳跃 warning 2→0）。
- figcov_keep.json 登记 7 张判噪水印图（实测 hash 与判噪输出逐一对应）⇒ ④-e 由 FAIL 转 PASS。
- 验收：qa_vol_all 8 闸门 ALL PASS（④ 结构终检 0）｜pipe_tbl_audit 异常 0｜vol_poolchk 掉池 0｜
  fm_strict FAIL 0｜validate_kb Error 0／Warning 0。
- 三件套：答案与解析版／学生版／答题卡（含「卷级后处理补丁 1 个」自动重放）。
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
    print((r.stdout + r.stderr).decode("utf-8", "replace")[-900:])
    if r.returncode != 0:
        sys.exit(1)
    main_env = {k: v for k, v in os.environ.items() if k != "GIT_INDEX_FILE"}
    run(["git", "reset", "-q", "HEAD", "--"] + PURE + FORCE, main_env)
    left = run(["git", "diff", "--cached", "--name-only"], main_env).stdout.decode("utf-8").strip()
    print("主索引残留（reset 后）行数 =", len([x for x in left.split("\n") if x]))
    print("HEAD:", run(["git", "log", "--oneline", "-1"], main_env).stdout.decode("utf-8").strip())


if __name__ == "__main__":
    main()
