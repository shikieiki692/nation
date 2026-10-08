#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""add_analysis.py —— 给某卷「答案版 md」逐题注入**结构化详细解析**（数据驱动 · 通用 · 幂等）。

【为什么有它】此前每卷都要重抄一份注入器（`add_analysis_XI.py` 单行版、`add_analysis_XII.py`、
`add_analysis_XIII.py`）—— 只有卷号与数据不同。本工具把**注入逻辑**一次固化。

用法：
  python add_analysis.py --vol XII --data an12_data1.py,an12_data2.py,an12_data3.py

数据文件格式（同 an12_data* / an13_data*）：
  A = { 题号: dict(考点=…, 思路=…, 步骤=[(小问号, 分值, 详解), …], 易错=…), … }

结构（每题的解析块，插在答案区之后、`---` 之前）：
  > —— 解析 ——          （以「—」开头 ⇒ 出卷器居中成横幅分隔）
  > **考点**：…          （引用 03-知识点 的〈页名〉）
  > **思路**：…
  > **N-x**（分值）…     （逐小问详解；分值写 "—" 则省略括号）
  > **易错**：…

幂等：答案版已含「> **考点**」则跳过（需重写请先重出卷 md）。
"""
import argparse
import importlib.util
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"


def load_data(files):
    A = {}
    for f in files:
        spec = importlib.util.spec_from_file_location(os.path.basename(f)[:-3], f)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        for k, v in vars(m).items():
            if k.startswith("A") and isinstance(v, dict):
                A.update(v)
    return A


def block_of(d):
    out = ["> —— 解析 ——", ">"]
    out += ["> **考点**：" + d["考点"], ">"]
    out += ["> **思路**：" + d["思路"], ">"]
    for tag, score, txt in d["步骤"]:
        head = "> **%s**" % tag
        if score and score not in ("—", "-", ""):
            head += "（%s）" % score
        else:
            head += "："          # 无分值的小问 ⇒ 用「：」分隔，避免「**8-2**328 K」粘连
        out += [head + txt, ">"]
    out += ["> **易错**：" + d["易错"], ""]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vol", required=True)
    ap.add_argument("--data", required=True, help="逗号分隔的数据文件")
    ap.add_argument("--md", help="覆盖默认卷 md 路径")
    a = ap.parse_args()
    A = load_data([p.strip() for p in a.data.split(",") if p.strip()])
    md = a.md or os.path.join(R, "04-题库", "初赛模拟卷%s（非有机·答案版）.md" % a.vol)
    txt = io.open(md, encoding="utf-8-sig").read().replace("\r\n", "\n")
    if "> **考点**：" in txt:
        print("已存在结构化解析，跳过（如需重写请先重出卷 md）")
        return
    lines = txt.split("\n")
    heads = [(i, int(m.group(1))) for i, l in enumerate(lines)
             for m in [re.match(r"^### 第 (\d+) 题", l)] if m]
    if not heads:
        print("未找到题块")
        return
    heads.append((len(lines), None))
    out, done = list(lines[:heads[0][0]]), 0
    for k in range(len(heads) - 1):
        s, qno = heads[k]
        e = heads[k + 1][0]
        blk = lines[s:e]
        if qno in A:
            idx = [j for j, l in enumerate(blk) if l.strip() == "---"]
            if idx:
                pos = idx[-1]
                blk = blk[:pos] + block_of(A[qno]) + blk[pos:]
                done += 1
        out += blk
    # ★ 断言：`$$` 必须独占一行 —— 行内出现 `$$` 即为「假块」（两段 `$…$` 拼接所致），
    #    会让 pandoc 把整段数学当字面文本（SOP 铁律二，2026-10-08 实测踩过）。
    bad = [i for i, l in enumerate(out, 1) if "$$" in l and l.strip() != "$$"]
    if bad:
        print("  ⚠ 检出 %d 行 `$$` 未独占一行（假块）：行号 %s" % (len(bad), bad[:6]))
    io.open(md, "w", encoding="utf-8", newline="\n").write("\n".join(out))
    print("卷 %s：已插入结构化解析 %d 题（数据 %d 题）" % (a.vol, done, len(A)))


if __name__ == "__main__":
    main()
