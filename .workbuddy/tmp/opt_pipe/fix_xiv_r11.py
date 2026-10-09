# -*- coding: utf-8 -*-
"""r11：跨段折断修复 + 评分细则排版规范化。"""
import os, shutil, datetime

Q = "04-题库/2026机构初赛模拟题"
BAK = ".workbuddy/tmp/opt_pipe/card_bak_r11"
os.makedirs(BAK, exist_ok=True)

EDITS = [
    # HZ-07-05：句中折断「试写出需要」
    (f"{Q}/汇智/题-HZ-07-05-有机金属卤化物钙钛矿材料近几.md",
     "试写出需\n\n要低温反应的原因。",
     "试写出需要低温反应的原因。",
     "HZ-07-05 折断合句"),
    # CM-01-05：评分细则折断 + 括号未闭合
    (f"{Q}/chemy/题-CM-01-05-很多具有钙钛矿结构的化合物是.md",
     "5-4-3（3分，示出低温相有SHG信号1分，示出高温相没有SHG信号1分，示出在相变温\n\n度（370 K）下 SHG 信号突跃消失 （1 分）",
     "5-4-3（共 3 分）：示出低温相有 SHG 信号（1 分），示出高温相没有 SHG 信号（1 分），示出在相变温度（370 K）下 SHG 信号突跃消失（1 分）。",
     "CM-01-05 5-4-3 细则"),
]

apply_ = "--apply" in os.sys.argv
cache, ok = {}, True
for path, old, new, tag in EDITS:
    t = open(path, encoding="utf-8-sig").read()
    n = t.count(old)
    if n != 1:
        print("!! [%s] 命中 %d 次（应为 1）" % (tag, n))
        ok = False
        continue
    print("OK [%s]" % tag)
    cache[path] = t.replace(old, new, 1)

if not ok:
    print("存在失败项，未写盘")
    os.sys.exit(1)

if apply_:
    stamp = datetime.datetime.now().strftime("%m%d_%H%M")
    for path, body in cache.items():
        shutil.copy2(path, os.path.join(BAK, os.path.basename(path) + ".bak-" + stamp))
        open(path, "w", encoding="utf-8", newline="\n").write(body)
    print("已写盘 %d 个文件" % len(cache))
else:
    print("(dry) 待写盘 %d 个文件" % len(cache))
