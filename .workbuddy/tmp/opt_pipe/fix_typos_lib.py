# -*- coding: utf-8 -*-
"""全库（机构域 ＋ 卷 md）清理 OCR 形近错字：品体→晶体、品系→晶系、品胞→晶胞。

⚠️ 必须带负向后视，否则「**样品体**系 / **样品体**积 / **产品系**列」会被误改。
⚠️ 排除 `_待人工复核-空壳与重复卡/`（已弃用内容，不投入生产）。

用法：python fix_typos_lib.py            # dry
      python fix_typos_lib.py --apply
"""
import io, os, re, sys, collections

R = r"C:\Obsidion\妙妙屋"
sys.stdout.reconfigure(encoding="utf-8")

RULES = [
    ("品体→晶体", re.compile(r"(?<!样)品体"), "\u7ed3\u6676"),   # 晶体
    ("品系→晶系", re.compile(r"(?<!产|作|样|出|系|成|新)品系"), "\u6676\u7cfb"),
    ("品胞→晶胞", re.compile(r"品胞"), "\u6676\u80de"),
]
SKIP = ("_待人工复核", "images")

targets = []
# ⛔ 只改本线域：机构域源卡 ＋ 卷 md（教材习题/真题 等属别的线，跨线须先对齐）
for dp, dn, fn in os.walk(os.path.join(R, "04-题库", "2026机构初赛模拟题")):
    if any(s in dp for s in SKIP):
        continue
    for f in fn:
        if f.endswith(".md"):
            targets.append(os.path.join(dp, f))
for f in os.listdir(os.path.join(R, "04-题库")):
    if f.startswith("初赛模拟卷") and f.endswith(".md"):
        targets.append(os.path.join(R, "04-题库", f))

apply_ = "--apply" in sys.argv
agg = collections.Counter()
nfile = 0
for p in sorted(targets):
    raw = io.open(p, encoding="utf-8-sig").read()
    new = raw
    hit = {}
    for name, rx, rep in RULES:
        n = len(rx.findall(new))
        if n:
            hit[name] = n
            new = rx.sub(rep, new)
    if not hit:
        continue
    nfile += 1
    for k, v in hit.items():
        agg[k] += v
    rel = os.path.relpath(p, R).replace("\\", "/")
    print("  %-62s %s" % (rel[-60:], hit))
    if apply_:
        eol = "\r\n" if "\r\n" in raw else "\n"
        io.open(p, "w", encoding="utf-8", newline="\n").write(new.replace("\r\n", "\n"))

print("=" * 78)
print("%s 文件 %d ｜ 合计 %s" % ("已写盘" if apply_ else "(dry)", nfile, dict(agg)))
