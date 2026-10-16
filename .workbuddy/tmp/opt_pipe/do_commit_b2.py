# -*- coding: utf-8 -*-
r"""提交：B2 KP 链接卫生 —— D 8→1 ／ E 5→0（alias 承接 ＋ 去链）。
隔离索引 + 逐路径 add(-f) + 断言 + 竞态重试 + 主索引清理 + 提交完整性校验。"""
import os
import subprocess
import sys
import time

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Obsidion\妙妙屋"
os.chdir(ROOT)

P = [
    "03-知识点/化学原理/配合物几何构型.md",
    "03-知识点/无机和结构化学/氮族元素.md",
    "03-知识点/无机和结构化学/小分子活化.md",
    "03-知识点/化学原理/基尔霍夫定律.md",
    "03-知识点/无机和结构化学/配位化学.md",
    "03-知识点/无机和结构化学/硅烷.md",
    "09-审计报告/历史任务卡/任务卡-publishedKP断链修复.md",
    "09-审计报告/历史任务卡/任务卡-validate_kb与published断链目录治理.md",
    "09-审计报告/历史任务卡/任务卡-备课体系深度优化与审计.md",
    "09-审计报告/历史任务卡/计划-全库断链与图片缺失治理.md",
    "00-首页/活跃任务/断链内容建设backlog.md",
    "09-审计报告/auto-validation/2026-10-16-validation.md",
]

MSG = (
    "fix(组卷): B2 KP 链接卫生 —— D 真孤儿 8→1／E 悬空链 5→0（alias 承接＋去链）\n\n"
    "- 策略依据＝库既定三策略「**alias 承接 ＋ 改链 ＋ 去链**，0 新建」\n"
    "  （`00-首页/活跃任务/断链内容建设backlog.md` §使用建议）；⛔ 不新建 KP 页硬凑。\n"
    "- **D 真孤儿 8（去重 7）→ 1**：6 项 alias 承接（均命中「有承载」判例）——\n"
    "  `三方柱→配合物几何构型`（页含三帽三方柱／三棱柱）／`肼→氮族元素`（页内 5 处，与 backlog 判例一致）／\n"
    "  `氮气活化→小分子活化`（N₂ 活化专节）／`绝热燃烧→基尔霍夫定律`（绝热火焰温度解题范式）／\n"
    "  `配位方式→配位化学`（端基／桥联／螯合）／`硅烯→硅烷`（该页回链同卡 `题-34决理-2-1-3`）。\n"
    "- **D 余 1＝真内容缺口（登记待建）**：`[[电子顺磁共振]]`（题-177）全库无 KP 覆盖（03-知识点 0 命中）\n"
    "  ⇒ 非「命名不一致」，⛔ 不 alias 硬接（会造误导链）；登记 backlog §二（建议新页或并入「异构与结构表征」§2.2）。\n"
    "- **E 悬空链 5（去重 4）→ 0**：`09-审计报告/历史任务卡/` 4 卡 5 处 `source_notes` 去链——\n"
    "  `auto-validation/{2026-08-04,2026-06-29}-validation` **实测未录入库**（该目录自 2026-07-21／10-02 起）3 处；\n"
    "  `11-模板/scripts/{validate_kb.py,build-all-handout-docx.py}` **实存但非 .md**（wikilink 不解析）2 处；\n"
    "  FM 键集合不变、其余字节不动。\n"
    "- 双闸门：ruamel FM 严格解析 **FAIL 0**（10 文件）；`validate_kb --changed` **0 error / 0 warning / 6 info**。\n"
    "- 🔴 护栏：6 个 alias 页中 2 个为 **CRLF** ⇒ 首版正则漏 `\\r` 误插**重复 `aliases:` 键**（js-yaml4 会 THROW）\n"
    "  ⇒ 即时 `git checkout` 回滚重做；脚本改为 **CRLF 感知** ＋ 前置「aliases 键恰 0/1 个」＋ 后置「恰 1 个」断言 ＋ 落盘后严格解析。\n"
    "- 撞车防护：隔离索引 read-tree → 逐路径 add(-f) → 断言「暂存 ≡ 本会话集合」→ commit →\n"
    "  断言「主索引暂存 ⊆ 本会话集合」→ 逐批 reset -q HEAD --；**只 add 本会话 12 路径**。\n"
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


idx = os.path.join(ROOT, ".git", "session_idx_b2")
env = {"GIT_INDEX_FILE": idx}
for f in (idx, idx + ".lock"):
    if os.path.exists(f):
        os.remove(f)

h0 = ""
for attempt in range(6):
    h0 = head()
    run(["git", "read-tree", h0], env)
    B = 80
    for k in range(0, len(P), B):
        run(["git", "add", "-f", "--"] + P[k:k + B], env)
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
    print("  多:", sorted(set(st) - set(P))[:5])
    print("  少:", sorted(set(P) - set(st))[:5])
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
    print("!! 主索引含外来项，中止 reset：", foreign[:5])
    raise SystemExit(1)
for k in range(0, len(P), 80):
    run(["git", "reset", "-q", "HEAD", "--"] + P[k:k + 80])
after = [x for x in run(["git", "diff", "--cached", "--name-only"]).stdout.split("\n") if x.strip()]
print("reset 后主索引暂存:", len(after), "项（应为 0）")
print("NEW_HEAD", head()[:9])
