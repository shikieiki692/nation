# -*- coding: utf-8 -*-
"""验证 60 个修复文件：快照(写前) vs 磁盘(写后) 逐行 diff。
断言：① opcode 只含 equal / replace(1:1) / insert / delete；
      ② 所有新增行（含空行）行尾 \\r 状态与相邻保留行一致（禁裸 LF 混入 CRLF 区）。"""
import zipfile, os, difflib

VAULT = r"C:\Obsidion\妙妙屋"
bak = os.path.join(VAULT, ".workbuddy", "backups", "fix_kp_yaml_20260903_001146.zip")
z = zipfile.ZipFile(bak)
ok, bad = 0, 0
SHOW = {os.path.normpath(n) for n in [
    "03-知识点/决赛要求/物理化学深化/Boltzmann统计初步.md",
    "03-知识点/决赛要求/结构与配位深化/原子轨道与波函数.md",
    "03-知识点/有机化学/质子转移可行性.md",
]}
for name in z.namelist():
    rel = os.path.normpath(name)
    orig = z.read(name).decode("utf-8").split("\n")
    cur = open(os.path.join(VAULT, rel), encoding="utf-8", newline="").read().split("\n")
    sm = difflib.SequenceMatcher(None, orig, cur, autojunk=False)
    problems = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        # replace 允许非等长（D 类 1 行→3 行 sources 是有意替换），行尾检查兜底
        if tag in ("replace", "insert"):
            ref = cur[j1 - 1] if j1 > 0 else (cur[j2] if j2 < len(cur) else "")
            ref_tr = ref.endswith("\r")
            for k in range(j1, j2):
                if cur[k].endswith("\r") != ref_tr:
                    problems.append(f"L{k+1} 行尾与邻居不一致: {cur[k]!r}")
    if problems:
        bad += 1
        print(f"❌ {rel}")
        for p in problems:
            print(f"   {p}")
    else:
        ok += 1
        if rel in SHOW:
            print(f"✅ {rel} 变更区：")
            for tag, i1, i2, j1, j2 in sm.get_opcodes():
                if tag == "equal":
                    continue
                for k in range(max(0, j1 - 1), min(len(cur), j2 + 1)):
                    print(f"   {k+1:>4} {cur[k]!r}")
print(f"\n通过 {ok} / 异常 {bad} / 共 {ok + bad}")
