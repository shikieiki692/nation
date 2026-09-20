#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""render_gate.py —— 公式渲染闸门（结构闸门查不出来的那一层）。

现有闸门（jsyaml / validate_kb / gate_exercise_books）查的是 **结构**：
frontmatter、断链、图片、题号……**没有一项查「公式到底能不能渲染」**。
2026-09-20 一次会话内修的 7 类缺陷（div 包裹 / `\\AA` / TAB 污染 /
`[\\[` / 断行宏 / `$$` 结构错位 / `\\text{\\text{}}` 嵌套）**全部落在它们的盲区**。

本闸门按**两套渲染器**分别断言（两套真相不可混用）：

  A) **docx 栏**（学生拿到的 Word）
     前置：剥 frontmatter → 跑 build-all-handout-docx.py 的 _preprocess_markdown
     方言：markdown+tex_math_dollars+tex_math_single_backslash+pipe_tables+raw_tex
     断言：① `Could not convert TeX math` == 0
           ② 产物正文字面 `$` == 0
           ③ oMath 计数（提供 --baseline 时才比较，不减少）

  B) **Obsidian 栏**（人读 md）
     语义：CommonMark 家族（行首块级标签 = raw HTML block，吞掉块内 markdown）
     断言：① 行首 `<div` == 0
           ② `\\AA` == 0
           ③ 真 TAB 残名（TAB + ext/imes/heta…）== 0

⚠️ **两栏不可互推**：实测跨行 `$$` 在 CommonMark 下失配、在管线方言下正常；
`<div>` 在 CommonMark 下吞公式、在管线方言下被降级无害。**选错栏 = 结论全错。**

用法
----
    python -X utf8 11-模板/scripts/render_gate.py --changed <路径> [<路径>…]
    python -X utf8 11-模板/scripts/render_gate.py --manifest <清单文件>
    python -X utf8 11-模板/scripts/render_gate.py --domain 04-课件/习题集
    python -X utf8 11-模板/scripts/render_gate.py --changed … --baseline   # 与 git HEAD 比 oMath

退出码：0 = 全过；1 = 有失败。
"""
import argparse
import importlib.util
import os
import re
import subprocess
import sys
import zipfile
from pathlib import Path

VAULT = Path(__file__).resolve().parents[2]
PANDOC = os.environ.get("PANDOC_BIN", "pandoc")
PIPELINE = VAULT / "11-模板" / "scripts" / "build-all-handout-docx.py"

# 管线真实方言（必须与 build-all-handout-docx.py::PANDOC_EXTENSIONS 一致）
PANDOC_EXT = "markdown+tex_math_dollars+tex_math_single_backslash+pipe_tables+raw_tex"

TAB = chr(9)
BS = chr(92)

# ── B 栏（Obsidian）签名 ────────────────────────────────────────────────
RE_DIV_LINE = re.compile(r"^[ \t]*<div\b", re.M)
RE_AA = re.compile(re.escape(BS) + r"AA\b")
RE_TAB_RESID = re.compile(TAB + r"(?:ext\{|ext\b|imes\b|heta\b|frac\b)")
RE_TEXT_TEXT = re.compile(re.escape(BS + "text{" + BS + "text{"))

# ── ⛔ 曾在此加过「prose 裸 `^`」签名检查，**已撤除，勿重加**（2026-09-20） ──
# 设想：pandoc 的 superscript 会把 prose 的 `^` 与后面最近的 `^` 配成一对，
# 跨过 `$…$` 就吞掉该公式。**机制属实**，但**判据无法可靠表达**：
#   同一形状，区间短则坏、区间长反而「好」—— pandoc 的 superscript 有长度/复杂度上限，
#   超限时解析失败、静默退化为字面文本因而无害。该上限不可预测。
# 实测代价：按该签名在本域报 6 份，逐一核对**全部是假阳性**（无一例「产物字面 $」）。
# → 这一类**必须按「结果」判**：本脚本 A 栏的「产物字面 `$` == 0」断言就是正解，
#   它能直接量出「公式到底渲没渲染出来」。**别再回到按形状猜。**
#
# 同理，`build-all-handout-docx.py` 里曾加的 `bare_script_fatal` 规则也已撤除。

# ⚠️ 临时目录**必须按进程隔离**：本闸门常被并发调用（如批处理扫描时又单查一份），
#    用固定路径会让两个进程互相覆盖 `_g.md`/`_g.docx`，读出**别人的产物**
#    —— 表现为 oMath 变成 0、假 PASS。2026-09-20 实测踩到（后台扫批时单查一份即复现）。
TMPDIR = VAULT / ".workbuddy" / "tmp" / ("_render_gate_%d" % os.getpid())

# ── 适用范围：文档类域默认跳过（2026-09-20 实测 3/4 假阳性后加的）────────────
# 闸门的 A 栏断言是「**产物字面 `$` == 0**」——它测的是「公式有没有渲染出来」。
# 但在**非数学文书**里，`$` 常被用作**非数学**用途，断言会误报：
#   · 价格：`| CrystalMaker | 付费(~$300) |`        （08-可视化资源 实测）
#   · 散文里描述这个字符：`②bash 内联 $ 转义变行锚…` （02-数据库 实测）
#   · DataviewJS 内联语法：`$=dv.pages('…').length` （12-教学洞察 实测）
#   · README/索引/审计报告：本身就是**在描述缺陷**，天然含坏例子
# 这三例都是「本来就该原样显示 `$`」，不是缺陷。
# → 默认只检查**数学内容域**；`--include-docs` 可强制纳入。
DOC_SKIP_DOMAINS = (
    "09-审计报告/", "02-数据库/", "12-教学洞察/", "08-可视化资源/",
    "10-索引与统计/", "01-考纲导航/", "11-模板/", "00-首页/", ".workbuddy/",
)


def should_check(rel: str, include_docs: bool) -> bool:
    if include_docs:
        return True
    if rel.rsplit("/", 1)[-1].lower() == "readme.md":
        return False                      # README 属文档
    return not any(rel.startswith(d) for d in DOC_SKIP_DOMAINS)


# ── 允许清单（与库里既有惯例对齐）────────────────────────────────────────
# 库里已有 `09-审计报告/2026-08-30-习题书V2-预检WARN允许清单.md` ——
# 把「确认属于启发式误报」的预检项登记为允许项。
# 本闸门沿用同一惯例：成片误报用**域划分**（上面）处理；
# 个别、按域划不开的登记到 `render_gate_allowlist.txt`。
DEFAULT_ALLOWLIST = VAULT / "11-模板" / "scripts" / "render_gate_allowlist.txt"


def load_allowlist(path):
    """读允许清单 → {相对路径: 原因}。文件不存在则返回空。"""
    allowed = {}
    if not path or not Path(path).is_file():
        return allowed
    for ln in Path(path).read_text(encoding="utf-8").splitlines():
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        parts = s.split("\t")
        allowed[parts[0].strip()] = parts[1].strip() if len(parts) > 1 else ""
    return allowed


def _load_pipeline():
    """加载 docx 管线的 _preprocess_markdown（闸门必须与真实管线同源）。"""
    spec = importlib.util.spec_from_file_location("_bh_for_gate", PIPELINE)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_bh_for_gate"] = mod
    try:
        spec.loader.exec_module(mod)
    except SystemExit:
        pass
    if not hasattr(mod, "_preprocess_markdown"):
        raise SystemExit("!! 无法从 %s 载入 _preprocess_markdown" % PIPELINE)
    return mod


def strip_frontmatter(raw: str) -> str:
    if raw.startswith("---"):
        parts = raw.split("---", 2)
        if len(parts) >= 3:
            return parts[2]
    return raw


def _literal_dollars(z: str) -> int:
    """数产物正文里的字面 `$`（= 未被解析成公式的 `$`）。

    ⚠️ **必须排除代码**，否则整片假阳性 —— 代码里的 `$` 是合法的：
      · 代码**块**：段落样式 `pStyle=SourceCode`（如 shell 的 `$PY`）
      · 行**内代码**：run 样式 `rStyle=VerbatimChar`（如文档里举例写 `` `$...$` ``）
    两次都是实测踩出来的：
      · `04-课件/学生讲义/README.md` 因代码块 `$PY` 被误报 ×7
      · `09-审计报告/…收官QA.md` 因行内 `` `奇数 `$` 行` `` / `` `$...$` `` 被误报 1→3
    所以这里**按 run 统计**：先跳过代码段落，再跳过代码 run。
    """
    CODE_RSTYLE = ("VerbatimChar", "SourceCode", "CodeChar", "Verbatim")
    n = 0
    for pa in re.findall(r"<w:p[ >].*?</w:p>", z, re.S):
        if "SourceCode" in "".join(re.findall(r'<w:pStyle w:val="([^"]+)"', pa)):
            continue                                  # 代码块整段跳过
        for run in re.findall(r"<w:r[ >].*?</w:r>", pa, re.S):
            rs = "".join(re.findall(r'<w:rStyle w:val="([^"]+)"', run))
            if any(c in rs for c in CODE_RSTYLE):
                continue                              # 行内代码 run 跳过
            n += "".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", run)).count("$")
    return n


def gate_docx(bh, text: str):
    """A 栏：返回 (失败数, 字面$数, oMath数, 报错摘要)。"""
    TMPDIR.mkdir(parents=True, exist_ok=True)
    src = TMPDIR / "_g.md"
    out = TMPDIR / "_g.docx"
    pre = bh._preprocess_markdown(strip_frontmatter(text))
    src.write_text(pre, encoding="utf-8")
    r = subprocess.run([PANDOC, "-f", PANDOC_EXT, "-t", "docx", "-o", str(out), str(src)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    err = (r.stdout or "") + (r.stderr or "")
    nfail = err.count("Could not convert TeX math")
    if not out.exists():
        return nfail, -1, -1, "pandoc 未产出 docx"
    z = zipfile.ZipFile(out).read("word/document.xml").decode("utf-8")
    n_om = len(re.findall(r"<m:oMath", z))
    snip = ""
    m = re.search(r"Could not convert TeX math(.{0,90})", err, re.S)
    if m:
        snip = " ".join(m.group(1).split())[:90]
    return nfail, _literal_dollars(z), n_om, snip


def gate_obsidian(text: str):
    """B 栏：返回 [(说明, 计数), …]（带计数是为了支持「只报新增」的回归比较）。"""
    probs = []
    n = len(RE_DIV_LINE.findall(text))
    if n:
        probs.append(("行首 <div>（CommonMark 下吞块内 markdown）", n))
    n = len(RE_AA.findall(text))
    if n:
        probs.append(("%sAA" % BS, n))
    n = len(RE_TAB_RESID.findall(text))
    if n:
        probs.append(("TAB 残名", n))
    n = len(RE_TEXT_TEXT.findall(text))
    if n:
        probs.append(("%stext{%stext{} 嵌套" % (BS, BS), n))
    return probs


def git_head_text(rel: str):
    r = subprocess.run(["git", "show", "HEAD:./" + rel], capture_output=True, cwd=VAULT)
    return r.stdout.decode("utf-8", "replace") if r.returncode == 0 else None


def collect(args):
    if args.changed:
        return list(args.changed)
    if args.manifest:
        p = Path(args.manifest)
        if not p.is_absolute():
            p = VAULT / p
        return [x.strip() for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
    if args.domain:
        root = VAULT / args.domain
        return [str(f.relative_to(VAULT).as_posix()) for f in sorted(root.rglob("*.md"))]
    raise SystemExit("!! 需指定 --changed / --manifest / --domain 之一")


def metrics(bh, text: str):
    """返回 (转换失败数, 产物字面$数, oMath数, 摘要, {B栏签名: 计数})。"""
    nfail, n_lit, n_om, snip = gate_docx(bh, text)
    return nfail, n_lit, n_om, snip, dict(gate_obsidian(text))


def main() -> int:
    ap = argparse.ArgumentParser(description="公式渲染闸门（双栏断言）")
    ap.add_argument("--changed", nargs="*", default=None)
    ap.add_argument("--manifest", default=None)
    ap.add_argument("--domain", default=None)
    ap.add_argument("--baseline", action="store_true",
                    help="与 git HEAD 版比较 oMath / 字面 $，断言不恶化")
    ap.add_argument("--regression", action="store_true",
                    help="**只报「比 HEAD 更差」的**：供 pre-commit 用，"
                         "避免把「文件里本来就有的历史缺陷」算到本次提交头上。"
                         "新文件（HEAD 无此文件）按全部新增上报。")
    ap.add_argument("-q", "--quiet", action="store_true", help="只打印失败项")
    ap.add_argument("--include-docs", action="store_true",
                    help="也检查文档类域（README / 审计报告 / 数据库表 / 索引等）。"
                         "默认跳过 —— 那里 `$` 常被用作价格、散文描述、DataviewJS 语法，会误报。")
    ap.add_argument("--allowlist", default=None,
                    help="允许清单路径（默认 11-模板/scripts/render_gate_allowlist.txt）；"
                         "登记的文件不计入失败。")
    ap.add_argument("--no-allowlist", action="store_true", help="忽略允许清单")
    args = ap.parse_args()

    allow = {} if args.no_allowlist else load_allowlist(
        args.allowlist or DEFAULT_ALLOWLIST)
    rels = [r for r in collect(args) if should_check(r, args.include_docs)]
    skipped = None
    if not rels:
        print("受检 0 文件（清单为空，或全部落在文档类域而被跳过"
              " —— 注意这**不是**通过）")
        return 0

    bh = _load_pipeline()
    fails, rows = [], []
    for rel in rels:
        p = VAULT / rel
        if not p.is_file():
            rows.append((rel, None, ["文件不存在"]))
            fails.append(rel)
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        nfail, n_lit, n_om, snip, obs = metrics(bh, text)

        if args.regression:
            # ── 只报「本次改动引入的」────────────────────────────────
            old = git_head_text(rel)
            probs = []
            if old is None:
                # 新文件：它带来的一切都是新增
                if nfail:
                    probs.append("docx 转换失败 ×%d  %s" % (nfail, snip))
                if n_lit > 0:
                    probs.append("产物字面 $ ×%d" % n_lit)
                for name, cnt in obs.items():
                    probs.append("%s ×%d" % (name, cnt))
                # ⚠️ 这句只是**说明**，不能当成问题项，否则干净的新文件也会被判失败
                #    （实测踩过：new_ok.md 只因为这句话被报 ❌）
                if probs:
                    probs.append("（新文件，以上按全部新增计）")
            else:
                o_fail, o_lit, o_om, _, o_obs = metrics(bh, old)
                if nfail > o_fail:
                    probs.append("docx 转换失败 %d→%d  %s" % (o_fail, nfail, snip))
                if n_lit > o_lit:
                    probs.append("产物字面 $ %d→%d" % (o_lit, n_lit))
                if o_om >= 0 and n_om < o_om:
                    probs.append("oMath 倒退 %d→%d" % (o_om, n_om))
                for name, cnt in obs.items():
                    if cnt > o_obs.get(name, 0):
                        probs.append("%s %d→%d" % (name, o_obs.get(name, 0), cnt))
        else:
            probs = ["%s ×%d" % (name, cnt) for name, cnt in obs.items()]
            if nfail:
                probs.append("docx 转换失败 ×%d  %s" % (nfail, snip))
            if n_lit > 0:
                probs.append("产物字面 $ ×%d" % n_lit)
            if args.baseline:
                old = git_head_text(rel)
                if old is not None:
                    _, olit, oom, _, _ = metrics(bh, old)
                    if oom >= 0 and n_om < oom:
                        probs.append("oMath 倒退 %d→%d" % (oom, n_om))
                    if olit >= 0 and n_lit > olit:
                        probs.append("字面 $ 增加 %d→%d" % (olit, n_lit))

        rows.append((rel, n_om, probs))
        if probs and rel not in allow:
            fails.append(rel)

    if not args.quiet:
        print("%-58s %6s  %s" % ("文件", "oMath", "结果"))
        print("-" * 84)
    for rel, n_om, probs in rows:
        if probs and args.quiet:
            pass
        elif probs:
            tag = ("ALLOW" if rel in allow else "❌")
            print("%-58s %6s  %s" % (rel[-58:], n_om if n_om is not None else "—", tag))
            for x in probs:
                print("        · %s" % x)
            if rel in allow:
                print("        （允许清单：%s）" % allow[rel])
        elif not args.quiet:
            print("%-58s %6s  ✅" % (rel[-58:], n_om))

    mode = "regression" if args.regression else "full"
    n_allow = sum(1 for rel, _, p in rows if p and rel in allow)
    tail = ("（另有允许 %d）" % n_allow) if n_allow else ""
    print("\nRENDER_GATE=%s [%s]  受检 %d / 失败 %d%s"
          % ("FAIL" if fails else "PASS", mode, len(rels), len(fails), tail))
    if fails:
        print("失败清单：")
        for f in fails:
            print("   ", f)

    for f in TMPDIR.glob("*") if TMPDIR.exists() else []:
        try:
            f.unlink()
        except OSError:
            pass
    try:
        TMPDIR.rmdir()
    except OSError:
        pass
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
