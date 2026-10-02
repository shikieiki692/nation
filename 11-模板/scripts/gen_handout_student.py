# -*- coding: utf-8 -*-
"""通用学生专用版派生（v3：纯标记驱动，零答案）。
用法: python gen_handout_student.py <讲义名> <模块目录>
例:   python gen_handout_student.py 化学动力学 3-物理化学

铁律：**学生专用版不得出现任何答案**。
切块原则（v3 变更点）：
  * 只认**显式答案标记**（`**解**：`/`**解析**：`/`**详细解析**：`…、`**练 N**`、`**例 N 详细解答**`、
    同行 `**解析**：内容`）——标记起、到下一个标题/分隔线止，**整块切净**（含公式之后的散文）。
  * **不再**使用「例题标题 → 首个显示公式」的启发式（v2 曾据此把题面自带的 `$$` 数据块误当答案起点，
    造成「空题」，也把公式之后的散文留在学生版）。
  * 若某「例题/示例」块既无显式标记、块内又有 `$$`，则**不切**并打印告警（须回母版补标记）——宁可告警，不可误切。
"""
import re
import sys
import pathlib

name, mod = sys.argv[1], sys.argv[2]
BASE = pathlib.Path("C:/Obsidion/妙妙屋/04-课件/学生讲义")
SRC = BASE / mod / f"{name}-超级充实版（自学完整）.md"
DST = BASE / "学生专用版" / mod / f"{name}-超级充实版（学生专用版）.md"

MOD = r"(?:详细|微观|完整|简要|逐步|逐题|逐问)*"
# ---- 答案起始标记（独占一行的加粗标记）----
# 覆盖实际语料：**解** / **解析** / **解答** / **详解** / **详细解析** / **详细微观解析** /
#                **参考答案** / **答案** / **解 N** / **解（7-1）** …
ANS = re.compile(r"^\*\*%s(?:解|解析|解答|详解|答案|参考答案|精解|解析与解答)"
                 r"(?:\s*\d{1,2}|（[^）]*）)*\*\*\s*[：:]?\s*$" % MOD)
ANS_LIAN = re.compile(r"^\*\*练\s*\d+\*\*(?!\s*·)\s*$")          # 答案侧「**练 N**」
HDR = re.compile(r"^#{1,4}\s")
SEP = re.compile(r"^---\s*$")
# 例题/示例标题（仅用于「无标记」告警，不再用于切块）
# 注意：不要含「解析」——理论小节（如「…的严格解析」）会被误伤。
HEAD_EX = re.compile(r"^#{3,4}\s*.*(?:示例|例题|例\s?[A-Z0-9]|练\s?\d|真题|全解)")
# 同行答案标记（**答案**：内容 / **解析**：内容 …）与「**例 N 详细解答**」型例题解答
ANS_INLINE = re.compile(r"^\*\*%s(?:解|解析|解答|详解|答案|参考答案|精解)"
                        r"(?:\s*\d{1,2})?\*\*[ \t]*[：:]?[ \t]*\S" % MOD)
EX_ANS = re.compile(r"^\*\*例\s*\d+[^\n*]{0,30}?(?:详细解答|解答|解析|详解)\*\*")
STEM_EX = re.compile(r"^\*\*例\s*\d+\*\*\s*$")

s = SRC.read_text(encoding="utf-8")
_m = re.search(r"(?m)^### 参考答案与精解[ \t]*$", s)
if not _m:
    raise SystemExit("未定位答案区标题")
lines = s[:_m.start()].split("\n")      # 练习区答案已整块剥离
n = len(lines)


def block_end(k):
    """从 k 起，返回所属块（标题/分隔线为界）的结束下标（不含）。"""
    j = k + 1
    while j < n and not HDR.match(lines[j]) and not SEP.match(lines[j]):
        j += 1
    return j


def trim_tail(e):
    while e > 0 and lines[e - 1].strip() == "":
        e -= 1
    return e


ranges = []
covered = set()

# ---------- Pass 1：独占一行的答案标记（含 详细解析 / 解析与解答） ----------
k = 0
while k < n:
    if ANS.match(lines[k]) or ANS_LIAN.match(lines[k]):
        e = trim_tail(block_end(k))
        if e > k:
            ranges.append((k, e))
            covered.update(range(k, e))
        k = block_end(k) if block_end(k) > k else k + 1
    else:
        k += 1

# ---------- Pass 1b：同行答案标记 与「**例 N 详细解答**」 ----------
k = 0
while k < n:
    if (ANS_INLINE.match(lines[k]) or EX_ANS.match(lines[k])) and k not in covered:
        e = k + 1
        while (e < n and not HDR.match(lines[e]) and not SEP.match(lines[e])
               and not STEM_EX.match(lines[e])):
            e += 1
        e = trim_tail(e)
        if e > k:
            ranges.append((k, e))
            covered.update(range(k, e))
        k = e if e > k else k + 1
    else:
        k += 1

# ---------- 告警：无显式标记的例题/示例块（含 $$）——须回母版补标记 ----------
warn = []
k = 0
while k < n:
    if HEAD_EX.match(lines[k]) and k not in covered:
        e = block_end(k)
        if not any(j in covered for j in range(k + 1, e)) \
                and any(lines[j].lstrip().startswith("$$") for j in range(k + 1, e)):
            warn.append("L%d %s" % (k + 1, lines[k].strip()[:56]))
        k = e
    else:
        k += 1

ranges.sort()
merged = []
for a, b in ranges:
    if merged and a <= merged[-1][1]:
        merged[-1] = (merged[-1][0], max(merged[-1][1], b))
    else:
        merged.append((a, b))
if len(merged) != len(ranges):
    print(":: 合并重叠区间 %d -> %d" % (len(ranges), len(merged)))
ranges = merged

# ---------- 应用切除，留白替代 ----------
out, k = [], 0
for a, b in ranges:
    out += lines[k:a]
    out += ["", "<br><br><br>", ""]
    k = b
out += lines[k:]
head = "\n".join(out)

# FM 改写：容忍 title/template_version 的版本号与措辞差异（v2.0/v3.0、学生讲义-/无前缀）
head = re.sub(r"(?m)^(title:.*)$", lambda m: m.group(1).replace("自学完整", "学生专用版"), head, count=1)
head = re.sub(r"(?m)^(title:(?!.*学生专用版).*)$", lambda m: m.group(1) + "（超级充实版·学生专用版）", head, count=1)
head = re.sub(r"(?m)^template_version:.*$", "template_version: 学生专用版 v3.0", head, count=1)

# ---------- 练习区每题后插留白 ----------
res, pend = [], False
for L in head.split("\n"):
    if re.match(r"^\*\*\d+\.\*\*([ \t]|$)", L):
        if pend:
            res += ["", "<br><br><br>", ""]
        pend = True
    res.append(L)
if pend:
    res += ["", "<br><br><br>"]
t = "\n".join(res).rstrip() + "\n"

n_blank = t.count("<br><br><br>")
n_img = t.count("![[")
n_prac = len(re.findall(r"(?m)^\*\*(\d+)\.\*\*([ \t]|$)", t))
assert n_prac >= 1, "未识别到练习题"
assert n_blank == n_prac + len(ranges), \
    "留白数 %d ≠ 练习 %d + 例题块 %d" % (n_blank, n_prac, len(ranges))
assert "### 参考答案与精解" not in t, "残留 §N 答案区"
assert re.search(r"(?m)^template_version:\s*学生专用版 v3\.0$", t), "template_version 未改写"
leak = [L for L in t.split("\n") if ANS.match(L) or ANS_LIAN.match(L)
        or ANS_INLINE.match(L) or EX_ANS.match(L)]
assert not leak, "残留答案标记: %r" % leak[:3]
t = re.sub(r"(?m)^image_count:\s*\d+\s*$", "image_count: %d" % n_img, t, count=1)
assert re.search(r"(?m)^image_count: %d$" % n_img, t), "image_count 未更新"

print("切除答案块 %d 处 | 留白总数 %d（练习 %d + 例题 %d） | 学生版图数 %d"
      % (len(ranges), n_blank, n_prac, len(ranges), n_img))
if warn:
    print(":: 告警 %d 处（无显式答案标记的例题块，须回母版补标记）：" % len(warn))
    for w in warn:
        print("     ", w)

DST.parent.mkdir(parents=True, exist_ok=True)
DST.write_text(t, encoding="utf-8", newline="\n")
print("已写盘:", DST.name, "(%d 行)" % (t.count("\n") + 1))
