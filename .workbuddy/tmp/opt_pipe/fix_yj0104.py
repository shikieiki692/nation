# -*- coding: utf-8 -*-
"""fix_yj0104.py —— 删除「题-YJ-01-04」答案区的 OCR 串行冗余行。
原状：4-2-1 行之后多出一行错标题号的重复行（「2-1 酸浸作用: 回收阳板泥中的 Cu 元素…」）。
处置：删除该重复行（内容与 4-2-1 行重复）＋ 保留校勘注说明。
"""
import io, os, sys
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
CARD = os.path.join(R, "04-题库/2026机构初赛模拟题/壹尖培优/题-YJ-01-04-硒元素被誉为生命之火在电子和.md")
BK = os.path.join(R, ".workbuddy/tmp/opt_pipe/yj_backup")
os.makedirs(BK, exist_ok=True)
apply = "--apply" in sys.argv
BAD = "2-1 酸浸作用: 回收阳板泥中的 Cu 元素（通常用浓硫酸）；（1 分）"

t = io.open(CARD, encoding="utf-8-sig").read().replace("\r\n", "\n")
assert BAD in t, "未找到待删行"
j = t.find("## 参考答案"); k = t.find("## 知识点映射")
lines = t[j:k].split("\n")
out = [l for l in lines if l.strip() != BAD]
assert len(out) == len(lines) - 1, "删除行数异常：%d → %d" % (len(lines), len(out))
# 加校勘注（在答案区尾部）
out = [x for x in out if x.strip()]
out += ["", "> ⛔ 校勘（2026-10-07）：原答案区有一行 OCR 串行冗余——"
        "「2-1 酸浸作用: 回收阳板泥中的 Cu 元素…」，题号错标且内容与 4-2-1 行重复，已删除。", ""]
newt = t[:j] + "\n".join(out) + t[k:]
print("原答案区 %d 行 → %d 行" % (len(lines), len(out)))
if apply:
    bfp = os.path.join(BK, os.path.basename(CARD) + ".orig")
    if not os.path.exists(bfp):
        io.open(bfp, "w", encoding="utf-8", newline="\n").write(t)
    io.open(CARD, "w", encoding="utf-8", newline="\n").write(newt)
    print("✔ 已写入")
else:
    print("(dry-run)")
