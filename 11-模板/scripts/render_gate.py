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


def prose_caret_hazard(text: str):
    """B 栏附加：prose 裸 `^` 与数学域内 `^` 同行 ⇒ pandoc superscript 配对吞公式。

    机制：pandoc 的 `markdown` 方言默认开 superscript 扩展，`^…^` 成对。
    prose 里一个落单的 `^`（如 `c_O₂^½·$c_M$/$K^{1/2}$`）会与后面公式里的 `^`
    配成一对，把中间的 `$…$` 整段吞掉 → 该公式不渲染。
    实测：`04-课件/习题集/…/3-化学动力学.md` L3880 即此症。

    判据：逐行「不在任何数学域内」的 `^` 为**奇数**，且同行数学域内也有 `^`。
    （单个 `~`（约等于）无害：pandoc 的 `~…~` 要求无空格。）
    """
    D = "$"
    bad = []
    in_fence = in_display = False
    for i, ln in enumerate(text.splitlines(), 1):
        st = ln.strip()
        if st.startswith("```") or st.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if st == D + D:
            in_display = not in_display
            continue
        if in_display:
            continue
        s = re.sub(r"`[^`]*`", lambda m: " " * len(m.group(0)), ln)
        np_ = nm = 0
        in_m = False
        for c in s:
            if c == D:
                in_m = not in_m
            elif c == "^":
                if in_m:
                    nm += 1
                else:
                    np_ += 1
        if np_ % 2 == 1 and nm > 0:
            bad.append((i, np_, nm))
    return bad


TMPDIR = VAULT / ".workbuddy" / "tmp" / "_render_gate"


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
    plain = re.sub(r"<[^>]+>", "", z)
    n_om = len(re.findall(r"<m:oMath", z))
    snip = ""
    m = re.search(r"Could not convert TeX math(.{0,90})", err, re.S)
    if m:
        snip = " ".join(m.group(1).split())[:90]
    return nfail, plain.count("$"), n_om, snip


def gate_obsidian(text: str):
    """B 栏：返回 (问题列表)。"""
    probs = []
    if RE_DIV_LINE.search(text):
        probs.append("行首 <div>（CommonMark 下吞块内 markdown）")
    n = len(RE_AA.findall(text))
    if n:
        probs.append("%s\\AA ×%d" % (BS, n))
    n = len(RE_TAB_RESID.findall(text))
    if n:
        probs.append("TAB 残名 ×%d" % n)
    n = len(RE_TEXT_TEXT.findall(text))
    if n:
        probs.append("%stext{%stext{} 嵌套 ×%d" % (BS, BS, n))
    pc = prose_caret_hazard(text)
    if pc:
        probs.append("prose 裸 `^` 与公式 `^` 同行 ×%d 行（superscript 会吞掉中间公式）"
                     % len(pc))
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


def main() -> int:
    ap = argparse.ArgumentParser(description="公式渲染闸门（双栏断言）")
    ap.add_argument("--changed", nargs="*", default=None)
    ap.add_argument("--manifest", default=None)
    ap.add_argument("--domain", default=None)
    ap.add_argument("--baseline", action="store_true",
                    help="与 git HEAD 版比较 oMath，断言不减少")
    ap.add_argument("-q", "--quiet", action="store_true", help="只打印失败项")
    args = ap.parse_args()

    rels = collect(args)
    if not rels:
        print("受检 0 文件（清单为空 —— 注意这**不是**通过）")
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
        nfail, n_lit, n_om, snip = gate_docx(bh, text)
        probs = gate_obsidian(text)
        if nfail:
            probs.append("docx 转换失败 ×%d  %s" % (nfail, snip))
        if n_lit > 0:
            probs.append("产物字面 $ ×%d" % n_lit)
        if args.baseline:
            old = git_head_text(rel)
            if old is not None:
                _, olit, oom, _ = gate_docx(bh, old)
                if oom >= 0 and n_om < oom:
                    probs.append("oMath 倒退 %d→%d" % (oom, n_om))
                if olit >= 0 and n_lit > olit:
                    probs.append("字面 $ 增加 %d→%d" % (olit, n_lit))
        rows.append((rel, n_om, probs))
        if probs:
            fails.append(rel)

    if not args.quiet:
        print("%-58s %6s  %s" % ("文件", "oMath", "结果"))
        print("-" * 84)
    for rel, n_om, probs in rows:
        if probs and args.quiet:
            pass
        elif probs:
            print("%-58s %6s  ❌" % (rel[-58:], n_om if n_om is not None else "—"))
            for x in probs:
                print("        · %s" % x)
        elif not args.quiet:
            print("%-58s %6s  ✅" % (rel[-58:], n_om))

    print("\nRENDER_GATE=%s  受检 %d / 失败 %d"
          % ("FAIL" if fails else "PASS", len(rels), len(fails)))
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
