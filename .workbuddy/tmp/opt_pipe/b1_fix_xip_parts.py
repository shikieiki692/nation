# -*- coding: utf-8 -*-
r"""B1：卷 XIp 卷级分区标题编号错位修复 —— 第二/第三 → 第一/第二。
依据：试点命令 `--quota "结构化学=5,化学原理=5"`（2026-10-07 报告）；
      现行生成器按 quota 列表序编号 ⇒ 结构化学＝第一部分、化学原理＝第二部分（与 XII 同构一致）。
      现值为旧版生成器（模块→固定序号映射）的陈旧产物。
用法：python b1_fix_xip_parts.py [--apply]。含断言 + 备份 + 逐字节自证。"""
import os, sys, shutil, datetime
sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Obsidion\妙妙屋"
QD = os.path.join(ROOT, "04-题库")
BAK = os.path.join(ROOT, ".workbuddy", "tmp", "opt_pipe", "_bak_xip_parts")
APPLY = "--apply" in sys.argv

PAIRS = [
    ("## 第二部分\u3000结构化学（第 1–5 题，共 65 分）",
     "## 第一部分\u3000结构化学（第 1–5 题，共 65 分）"),
    ("## 第三部分\u3000化学原理（第 6–10 题，共 65 分）",
     "## 第二部分\u3000化学原理（第 6–10 题，共 65 分）"),
]
FILES = [os.path.join(QD, f"初赛模拟卷XIp（非有机·{k}）.md") for k in ("学生版", "答案版")]

stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M")
os.makedirs(BAK, exist_ok=True)
bad = 0
for p in FILES:
    raw = open(p, "rb").read()
    txt = raw.decode("utf-8-sig").replace("\r\n", "\n")
    lines = txt.split("\n")
    new_lines, hits = [], []
    for i, ln in enumerate(lines, 1):
        orig = ln
        for old, new in PAIRS:
            if ln == old:                       # 整行全等 ⇒ 只可能是卷级标题行
                ln = new
                hits.append((i, old, new))
        new_lines.append(ln)
    print("=", os.path.basename(p))
    for i, old, new in hits:
        print(f"  L{i}: {old!r}\n     → {new!r}")
    if len(hits) != 2:
        print(f"  !! 命中 {len(hits)} 处（应 2）⇒ 中止"); bad += 1; continue
    out = "\n".join(new_lines)
    # 逐字节自证：逆向还原后须与原文完全一致
    back = out.replace(PAIRS[0][1], PAIRS[0][0]).replace(PAIRS[1][1], PAIRS[1][0])
    assert back == txt, "逆向自证失败"
    # 题面区外零改动：除两行外逐行等同
    diff_lines = [i for i, (a, b) in enumerate(zip(lines, new_lines), 1) if a != b]
    print(f"  差异行: {diff_lines}（应恰为两处分区标题行）")
    if not APPLY:
        continue
    shutil.copy2(p, os.path.join(BAK, f"{os.path.basename(p)}.{stamp}"))
    open(p, "wb").write(out.encode("utf-8"))
    print("  已写盘 ✔")
print("----")
print("APPLY" if APPLY else "DRY-RUN", "｜ 异常文件:", bad)
