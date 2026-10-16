# -*- coding: utf-8 -*-
r"""B1-b：卷 XIp 的「> **范围**」说明行编号同步（第二/第三 → 第一/第二）。
与 H2 标题同源（旧版生成器产物）。口径比照同构卷 XII。
用法：python b1_fix_xip_range.py [--apply]。含计数断言 + 备份。"""
import os, sys, shutil, datetime
sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Obsidion\妙妙屋"
QD = os.path.join(ROOT, "04-题库")
BAK = os.path.join(ROOT, ".workbuddy", "tmp", "opt_pipe", "_bak_xip_parts")
APPLY = "--apply" in sys.argv

OLD = "第二部分\u3000结构化学（第 1–5 题，65 分）、第三部分\u3000化学原理（第 6–10 题，65 分）"
NEW = "第一部分\u3000结构化学（第 1–5 题，65 分）、第二部分\u3000化学原理（第 6–10 题，65 分）"
FILES = [os.path.join(QD, f"初赛模拟卷XIp（非有机·{k}）.md") for k in ("学生版", "答案版")]

stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M")
os.makedirs(BAK, exist_ok=True)
bad = 0
for p in FILES:
    raw = open(p, "rb").read()
    txt = raw.decode("utf-8-sig").replace("\r\n", "\n")
    n = txt.count(OLD)
    print("=", os.path.basename(p), "｜命中", n, "处")
    if n != 1:
        print("  !! 应恰 1 处 ⇒ 中止"); bad += 1; continue
    out = txt.replace(OLD, NEW)
    assert out.count(NEW) == 1 and OLD not in out
    assert out.replace(NEW, OLD) == txt, "逆向自证失败"
    if not APPLY:
        continue
    shutil.copy2(p, os.path.join(BAK, f"{os.path.basename(p)}.range.{stamp}"))
    open(p, "wb").write(out.encode("utf-8"))
    print("  已写盘 ✔")
print("----")
print("APPLY" if APPLY else "DRY-RUN", "｜ 异常文件:", bad)
