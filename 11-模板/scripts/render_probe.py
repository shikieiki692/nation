#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""render_probe.py —— 渲染缺陷**定位**探针（render_gate 只判「坏没坏」，本工具告诉你「坏在哪」）。

`render_gate` 的结论是二值的（FAIL/PASS + 计数）。但修的时候需要更细的信息：
  · 产物里那些**字面 `$`** 到底出自哪个段落？
  · pandoc 的 `Could not convert TeX math` 说的是哪一段公式？

本工具按**段落 / run** 粒度输出（且跳过代码段与代码 run —— 那里的 `$` 是合法的，
见 render_gate 里同一坑的三次踩坑记录）。

用法
----
    python -X utf8 11-模板/scripts/render_probe.py <相对路径> [<相对路径>…]
    python -X utf8 11-模板/scripts/render_probe.py --domain 04-课件/专题课

只读，不改任何文件。
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
TMP = VAULT / ".workbuddy" / "tmp" / ("_render_probe_%d" % os.getpid())
PANDOC = r"C:\Users\蕾赛\AppData\Local\Pandoc\pandoc.exe"
D = chr(36)
CODE_STYLES = ("VerbatimChar", "SourceCode", "CodeChar", "Verbatim")


def load_pipeline():
    spec = importlib.util.spec_from_file_location(
        "bh", VAULT / "11-模板" / "scripts" / "build-all-handout-docx.py")
    bh = importlib.util.module_from_spec(spec)
    sys.modules["bh"] = bh
    try:
        spec.loader.exec_module(bh)
    except SystemExit:
        pass
    return bh


def probe(bh, rel: str) -> None:
    p = VAULT / rel
    if not p.is_file():
        print("!! 不存在:", rel)
        return
    TMP.mkdir(parents=True, exist_ok=True)
    _, body, _ = bh._prepare_handout_markdown(p, verbose=False)
    pre = bh._preprocess_markdown(body)
    (TMP / "t.md").write_text(pre, encoding="utf-8")
    r = subprocess.run([PANDOC, "-f", bh.PANDOC_EXTENSIONS, "-t", "docx",
                        "-o", str(TMP / "t.docx"), str(TMP / "t.md")],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    err = (r.stdout or "") + (r.stderr or "")

    print("### %s" % rel)
    for m in re.finditer(r"Could not convert TeX math(.{0,200})", err, re.S):
        print("   [convert-fail] %s" % " ".join(m.group(1).split())[:200])
    if not (TMP / "t.docx").exists():
        print("   !! pandoc 未产出 docx")
        return
    z = zipfile.ZipFile(TMP / "t.docx").read("word/document.xml").decode("utf-8")
    n = 0
    for pa in re.findall(r"<w:p[ >].*?</w:p>", z, re.S):
        if "SourceCode" in "".join(re.findall(r'<w:pStyle w:val="([^"]+)"', pa)):
            continue
        txt = ""
        for run in re.findall(r"<w:r[ >].*?</w:r>", pa, re.S):
            rs = "".join(re.findall(r'<w:rStyle w:val="([^"]+)"', run))
            if any(c in rs for c in CODE_STYLES):
                continue
            txt += "".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", run))
        if D in txt:
            n += 1
            print("   [literal-$ ×%d] %r" % (txt.count(D), txt[:170]))
    if not n:
        print("   （无字面 `$` 段落）")
    print()


def main() -> int:
    ap = argparse.ArgumentParser(description="渲染缺陷定位探针（只读）")
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--domain", default=None)
    args = ap.parse_args()

    rels = list(args.paths)
    if args.domain:
        root = VAULT / args.domain
        rels += [p.relative_to(VAULT).as_posix() for p in sorted(root.rglob("*.md"))]
    if not rels:
        ap.error("需给路径或 --domain")

    bh = load_pipeline()
    for rel in rels:
        probe(bh, rel)

    for f in TMP.glob("*") if TMP.exists() else []:
        try:
            f.unlink()
        except OSError:
            pass
    try:
        TMP.rmdir()
    except OSError:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
