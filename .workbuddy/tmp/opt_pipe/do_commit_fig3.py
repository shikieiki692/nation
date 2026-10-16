# -*- coding: utf-8 -*-
r"""提交：A3 ④-e 三处真缺陷修复（X Q6 / XI Q10 / XIp Q7）＋ 三卷 docx 重建。
隔离索引 + 逐路径 add(-f) + 断言 + 竞态重试 + 主索引清理 + 提交完整性校验。"""
import os
import subprocess
import sys
import time

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Obsidion\妙妙屋"
os.chdir(ROOT)

D = "00-首页/题组Word/初赛模拟卷/真题版式/"
P = [
    "04-题库/初赛模拟卷X（非有机·答案版）.md",
    "04-题库/初赛模拟卷XI（非有机·答案版）.md",
    "04-题库/初赛模拟卷XI（非有机·学生版）.md",
    "04-题库/初赛模拟卷XIp（非有机·答案版）.md",
    "09-审计报告/2026-10-16-机构模拟卷④-e残余核查与师-生一致闸门通用化.md",
    "09-审计报告/auto-validation/2026-10-16-validation.md",
    D + "初赛模拟卷X（非有机·学生版·真题版式）.docx",
    D + "初赛模拟卷X（非有机·答案与解析版·真题版式）.docx",
    D + "初赛模拟卷XI（非有机·学生版·真题版式）.docx",
    D + "初赛模拟卷XI（非有机·答案与解析版·真题版式）.docx",
    D + "初赛模拟卷XIp（非有机·答案与解析版·真题版式）.docx",
    ".workbuddy/tmp/opt_pipe/vol_meta_X.json",
    ".workbuddy/tmp/opt_pipe/vol_meta_XI.json",
    ".workbuddy/tmp/opt_pipe/vol_meta_XIp.json",
    ".workbuddy/tmp/opt_pipe/fix_fig3.py",
    ".workbuddy/tmp/opt_pipe/reg_fig3_meta.py",
]

MSG = (
    "fix(组卷): ④-e 三处真缺陷修复 —— X Q6／XI Q10／XIp Q7「引而无图」补回 ＋ 三卷 docx 重建\n\n"
    "- 根因：源卡答案区/题面区**表格内 HTML `<img>`** 未落卷（旧版建卷器盲区；现行管线已修——O1 Q2 表内 32 张全落卷）。\n"
    "- 走**卷 md 层最小修补**（`fix_fig3.py`），⛔ 不跑 `build_org` 重建（会抹掉卷 md 层人工补丁，SOP §五-i⑦）；再重建 docx。\n"
    "- **X 答案版 6-2-2**：补回 `![[b820c9b2…]]`（$L_{Ph}$ 两种结构；`git log -S` 证构建期即丢）。源件带「清北营」灰字水印\n"
    "  ⇒ 复用 XV 线 `xv_dewm.py`（低饱和＋高亮置白）**去水印后原地替换**，逐张目检结构/标注完好（备份 `.workbuddy/tmp/dewm/`）。\n"
    "- **XI 10-1「方向」表**：首列 2 空单元格补 `![[143ca87a…]]`(b/a)、`![[7e7ab009…]]`(c/b)；两图标**无水印**；**学生版＋答案版同改**（题面区两版须一致）。\n"
    "- **XIp 答案版 7-1**：`| 7-1 | |` 空单元格补 `![[490596bc…]]`（分子玫瑰花结）；源件带清北营水印 ⇒ 同法去水印原地替换。\n"
    "- 登记：`vol_meta_{X,XI,XIp}.json::md_patches` 各加一条（`fix_fig3.py`）。\n"
    "- 验收：④-e `verify_fig_coverage` **X 76/76、XI 72/72、XIp 81/81，缺图 0 ⇒ PASS**（修前缺 1/2/1）；\n"
    "  `qa_vol_all --vol X / XI / XIp` **三卷 × 8 闸门 ALL PASS ✅**（④／④-b／④-c／④-d／④-e／④-f／⑤／⑥）。\n"
    "- docx：X（学生＋答案）、XI（学生＋答案）、XIp（答案）重建并过 `vol_img_upscale` 卷级补丁；\n"
    "  XIp 学生版逐 zip 条目与 HEAD **全同**（无内容变化）⇒ 已还原、不提交。\n"
    "- 双闸门：ruamel FM **FAIL 0**（5 文件）；`validate_kb --changed` 见报告。\n"
    "- 撞车防护：隔离索引 read-tree → 逐路径 add(-f) → 断言「暂存 ≡ 本会话集合」→ commit →\n"
    "  断言「主索引暂存 ⊆ 本会话集合」→ 逐批 reset -q HEAD --；**只 add 本会话 16 路径**。\n"
)


def run(a, env=None, chk=True):
    e = dict(os.environ)
    e.update(env or {})
    p = subprocess.run(a, cwd=ROOT, env=e, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if chk and p.returncode:
        print("FAIL", a[:3], p.stdout[-300:], p.stderr[-300:])
        raise SystemExit(1)
    return p


def head():
    return subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True,
                          text=True).stdout.strip()


idx = os.path.join(ROOT, ".git", "session_idx_fig3")
env = {"GIT_INDEX_FILE": idx}
for f in (idx, idx + ".lock"):
    if os.path.exists(f):
        os.remove(f)

h0 = ""
for attempt in range(6):
    h0 = head()
    run(["git", "read-tree", h0], env)
    for k in range(0, len(P), 80):
        run(["git", "add", "-f", "--"] + P[k:k + 80], env)
    if head() == h0:
        break
    print("  ⚠ HEAD 前进，重做（%d）" % attempt)
else:
    print("!! 不稳定")
    raise SystemExit(1)

st = [s for s in run(["git", "-c", "core.quotepath=false", "diff", "--cached",
                      "--name-only"], env).stdout.split("\n") if s.strip()]
print("staged %d 项 ｜ H0=%s" % (len(st), h0[:9]))
if sorted(st) != sorted(P):
    print("!! 暂存集合不符")
    print("  多:", sorted(set(st) - set(P))[:6])
    print("  少:", sorted(set(P) - set(st))[:6])
    raise SystemExit(1)

for i in range(6):
    p = subprocess.run(["git", "commit", "-m", MSG], cwd=ROOT, env=dict(os.environ, **env),
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if p.returncode == 0:
        print(p.stdout.strip()[:250])
        break
    if "cannot lock ref" in (p.stderr or "") or "index.lock" in (p.stderr or ""):
        time.sleep(3)
        continue
    print("CFAIL", p.stdout[-800:], p.stderr[-400:])
    raise SystemExit(1)
else:
    print("!! commit 未成功")
    raise SystemExit(1)

if os.path.exists(idx):
    os.remove(idx)

committed = [x for x in run(["git", "-c", "core.quotepath=false", "diff",
                             "--name-only", h0, "HEAD"]).stdout.split("\n") if x.strip()]
missing = sorted(set(P) - set(committed))
if missing:
    print("!! 提交可能被截断，缺 %d 项：" % len(missing), missing[:6])
    raise SystemExit(1)
extra = [x for x in committed if x not in set(P)]
print("提交含 %d 项 ｜ 额外路径: %s" % (len(committed), extra if extra else "无 ✅"))

main_staged = [x for x in run(["git", "-c", "core.quotepath=false", "diff", "--cached",
                              "--name-only"]).stdout.split("\n") if x.strip()]
print("主索引残留暂存 %d 项" % len(main_staged))
foreign = [x for x in main_staged if x not in set(P)]
if foreign:
    print("!! 主索引含外来项，中止 reset：", foreign[:6])
    raise SystemExit(1)
for k in range(0, len(P), 80):
    run(["git", "reset", "-q", "HEAD", "--"] + P[k:k + 80])
after = [x for x in run(["git", "diff", "--cached", "--name-only"]).stdout.split("\n") if x.strip()]
print("reset 后主索引暂存:", len(after), "项（应为 0）")
print("NEW_HEAD", head()[:9])
