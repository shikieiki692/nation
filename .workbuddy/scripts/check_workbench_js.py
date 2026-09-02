#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
校验《组卷工作台.md》里三块 dataviewjs：
  1) 抽出代码块落成临时 .js，交给 node --check 做纯语法检查（不执行，dv 未定义也无妨）
  2) 抽出 srcKey() 函数体，喂全库真实 source 值，与 Python 版的归一化结果逐条比对
     —— JS 版和 Python 版一旦不一致，「同来源限流 ≤3」就会算错
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

VAULT = Path(r"C:\Obsidion\妙妙屋")
WORKBENCH = VAULT / "04-题库" / "组卷工作台.md"
NODE = r"C:\Users\蕾赛\.workbuddy\binaries\node\versions\22.22.2-2\node.exe"
TMP = VAULT / ".workbuddy" / "tmp"
TMP.mkdir(parents=True, exist_ok=True)

BLOCK = re.compile(r"```dataviewjs\n(.*?)```", re.S)

# ── Python 版 srcKey（与 check_source_norm.py 完全一致，作为对照基准）──
PY_RULES = [
    (re.compile(r"[（(]忠实转录[)）]"), ""),
    (re.compile(r"[·•]\s*第\s*\d+\s*[讲章][\s\S]*$"), ""),
    (re.compile(r"第\s*[\d一二三四五六七八九十]+\s*[章节讲篇][\s\S]*$"), ""),
    (re.compile(r"[·•]\s*第\s*[\d一二三四五六七八九十]+\s*[分册卷][\s\S]*$"), ""),
    (re.compile(r"-\s*\d{1,2}\s*$"), ""),
    (re.compile(r"[\s·•、,，\-—]+$"), ""),
]


def py_srckey(s: str) -> str:
    k = str(s or "").trim() if hasattr(str, "trim") else str(s or "").strip()
    for pat, rep in PY_RULES:
        k = pat.sub(rep, k)
    return k.strip() or "(未知来源)"


def collect_sources() -> list[str]:
    """取全库题目的 source 去重值，只认 type ∈ {题目, 真题}。"""
    out = []
    for d in ("04-题库", "05-真题库"):
        for p in (VAULT / d).rglob("*.md"):
            try:
                b = p.read_bytes()
            except OSError:
                continue
            head = b[:3000].decode("utf-8", "ignore")
            if not re.search(r"^type:\s*(题目|真题)\s*$", head, re.M):
                continue
            m = re.search(r"^source:\s*(.+?)\s*$", head, re.M)
            if m:
                v = m.group(1).strip().strip('"').strip("'")
                if v:
                    out.append(v)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description="校验 md 里的 dataviewjs：语法 + srcKey 两版一致性")
    ap.add_argument("--file", default=str(WORKBENCH),
                    help="待校验的 md 文件（默认 04-题库/组卷工作台.md；staging 草稿用此参数）")
    args = ap.parse_args()
    target = Path(args.file)
    text = target.read_text(encoding="utf-8")
    blocks = BLOCK.findall(text)
    print(f"校验目标：{target}")
    print(f"抽出 {len(blocks)} 块 dataviewjs")

    # ① 语法检查
    ok = True
    for i, code in enumerate(blocks, 1):
        f = TMP / f"_wb_block{i}.js"
        f.write_text(code, encoding="utf-8", newline="")
        r = subprocess.run([NODE, "--check", str(f)], capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        if r.returncode == 0:
            print(f"  块{i}: ✅ 语法 OK（{len(code.splitlines())} 行）")
        else:
            ok = False
            print(f"  块{i}: ❌ 语法错误\n{r.stderr[:800]}")

    # ② srcKey 一致性：从文档里抽出函数原文，避免手抄走样
    m = re.search(r"function srcKey\(s\) \{.*?\n\}", text, re.S)
    if not m:
        print("❌ 文档里找不到 srcKey 函数，无法比对")
        sys.exit(1)
    js_fn = m.group(0)

    sources = collect_sources()
    uniq = sorted(set(sources))
    print(f"\n取到 {len(sources)} 条 source（去重 {len(uniq)}）")

    (TMP / "_srcs.json").write_text(json.dumps(uniq, ensure_ascii=False), encoding="utf-8")
    js = f"""
const fs = require('fs');
const srcs = JSON.parse(fs.readFileSync({str(TMP / '_srcs.json')!r}.replace(/\\\\/g,'/'), 'utf8'));
{js_fn}
const out = {{}};
for (const s of srcs) out[s] = srcKey(s);
process.stdout.write(JSON.stringify(out));
"""
    (TMP / "_srckey_test.js").write_text(js, encoding="utf-8", newline="")
    r = subprocess.run([NODE, str(TMP / "_srckey_test.js")], capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print(f"❌ node 执行失败：\n{r.stderr[:800]}")
        sys.exit(1)

    js_map = json.loads(r.stdout)
    diffs = []
    for s in uniq:
        a, b = py_srckey(s), js_map.get(s)
        if a != b:
            diffs.append((s, a, b))

    py_keys = Counter(py_srckey(s) for s in sources)
    js_keys = Counter(js_map[s] for s in sources)

    print(f"\n归一化结果：Python {len(py_keys)} 个来源 ｜ JS {len(js_keys)} 个来源")
    if diffs:
        print(f"❌ 两版结果不一致 {len(diffs)} 条（前 10）：")
        for s, a, b in diffs[:10]:
            print(f"   原文 {s!r}\n     PY={a!r}\n     JS={b!r}")
        ok = False
    else:
        print("✅ JS 版与 Python 版逐条一致")

    print("\nTOP 10 来源（JS 归一化后）：")
    for k, v in js_keys.most_common(10):
        print(f"   {v:5d}  {k[:44]}")

    # 清理临时 js
    for f in TMP.glob("_wb_block*.js"):
        f.unlink()
    (TMP / "_srckey_test.js").unlink(missing_ok=True)
    (TMP / "_srcs.json").unlink(missing_ok=True)

    print("\n" + ("✅ 全部通过" if ok else "❌ 存在问题"))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
