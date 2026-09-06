# -*- coding: utf-8 -*-
"""修复：结构化学阶段测试卷 used_in 多标——150 个非卷内题删除该 used_in 标量行。

背景：提交 aa629df1 三篇阶段测试卷生成时，结构化学篇按 200 题版打了标，
卷子后来定稿 50 题，多出的 150 个标量标记（全库诊断均为单值标量形态、
无其他卷名共存、与 09-03 并行写库零交集）需要清除。

规则：
  · 只删「整行恰好是 used_in: "[[结构化学阶段测试卷]]"」的行（标量形态）
  · 列表/block 形态中出现该卷名的文件不动（诊断=0 个，防意外）
  · 每文件断言恰好删 1 行、其余行逐一相等；读写 newline=""；写前 zip 快照

用法：python -X utf8 fix_usedin_overmark.py [--write]
"""
import os, re, sys, zipfile, datetime

VAULT = r"C:\Obsidion\妙妙屋"
PAPER = "结构化学阶段测试卷"
TARGET_LINE = re.compile(r'^used_in:\s*"\[\[' + re.escape(PAPER) + r'\]\]"\s*\r?$')
ANY_REF = re.compile(r"^used_in:", re.M)


def bn(x):
    return x.replace("\\", "/").split("/")[-1].removesuffix(".md")


# ── 收集目标 ──
files = []
for root in ("04-题库", "05-真题库"):
    for dp, dn, fn in os.walk(os.path.join(VAULT, root)):
        for f in fn:
            if f.endswith(".md"):
                p = os.path.join(dp, f)
                t = open(p, encoding="utf-8", newline="").read(4000)
                if re.search(r"^used_in:.*" + PAPER, t, re.M):
                    files.append(p)

paper_t = open(os.path.join(VAULT, "04-题库", PAPER + ".md"),
               encoding="utf-8", newline="").read()
inlinks = {bn(l) for l in re.findall(r"\[\[([^\]\|#]+)", paper_t)
           if "测试卷" not in l and "工作台" not in l}
targets = [p for p in files if bn(p) not in inlinks]
assert len(targets) == 150, f"目标应 150，实得 {len(targets)}"

WRITE = "--write" in sys.argv
if WRITE:
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = os.path.join(VAULT, ".workbuddy", "backups", f"fix_usedin_{ts}.zip")
    zf = zipfile.ZipFile(bak, "w", zipfile.ZIP_DEFLATED)

ok = 0
for p in targets:
    t = open(p, encoding="utf-8", newline="").read()
    lines = t.split("\n")
    idxs = [i for i, ln in enumerate(lines) if TARGET_LINE.match(ln)]
    assert len(idxs) == 1, f"{p}: 期望恰好 1 行目标，实得 {len(idxs)}"
    # 安全阀：该文件不得存在列表/多值形态的 used_in 引用
    rest = "\n".join(lines[:idxs[0]] + lines[idxs[0] + 1:])
    refs = [l for l in rest.split("\n") if ANY_REF.match(l) and PAPER in l]
    assert not refs, f"{p}: 删除后仍残留 {PAPER} 引用 {refs!r}"
    assert not any("\n" in ln for ln in lines)
    if WRITE:
        zf.write(p, os.path.relpath(p, VAULT).replace("\\", "/"))
        new_t = "\n".join(lines[:idxs[0]] + lines[idxs[0] + 1:])
        open(p, "w", encoding="utf-8", newline="").write(new_t)
    ok += 1

if WRITE:
    zf.close()
    print(f"快照 → {bak}")
print(f"{'实写' if WRITE else 'dry-run'} 完成：{ok} 个文件，每个删 1 行 used_in 标量。")
