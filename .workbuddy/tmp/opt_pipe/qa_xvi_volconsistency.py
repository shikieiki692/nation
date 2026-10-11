# -*- coding: utf-8 -*-
"""卷XVI 收口 QA：卷 md 自洽 + 学生版/答案版一致性。"""
import os
import re

VAULT = r"C:\Obsidion\妙妙屋"
ANS = os.path.join(VAULT, "04-题库/初赛模拟卷XVI（非有机·答案版）.md")
STU = os.path.join(VAULT, "04-题库/初赛模拟卷XVI（非有机·学生版）.md")


def load(p):
    return open(p, encoding="utf-8-sig").read().replace("\r\n", "\n")


a = load(ANS)
s = load(STU)

# 1) 题头与分值
heads = re.findall(r"^### 第 (\d+) 题[（(](\d+)\s*分[）)]([^\n]*)$", a, re.M)
print(f"[1] 答案版题头 {len(heads)} 条")
nums = [int(h[0]) for h in heads]
scores = [int(h[1]) for h in heads]
print("    题号:", nums)
print("    连续 1..16:", nums == list(range(1, 17)))
print("    分值:", scores, "合计:", sum(scores))

# 2) 模块划分
m1 = re.search(r"第一部分 结构化学（第 (\d+)~(\d+) 题，共 (\d+) 分）", a)
m2 = re.search(r"第二部分 化学原理（第 (\d+)~(\d+) 题，共 (\d+) 分）", a)
print(f"[2] 模块声明: 结构 {m1.groups() if m1 else '缺失'} ｜ 原理 {m2.groups() if m2 else '缺失'}")

# 3) 答案区非空 + 解析块
ans_sec = re.findall(r"\*\*答案\*\*(.*?)(?=\n> —— 解析 ——|\n### 第 |\Z)", a, re.S)
print(f"[3] 答案区段 {len(ans_sec)} ｜ 空/过短 {sum(1 for x in ans_sec if len(re.sub(chr(92)+'s','',x))<20)}")
parsed = re.findall(r"> —— 解析 ——", a)
print(f"    解析块（> —— 解析 ——）: {len(parsed)}")
kaodian = re.findall(r"> \*\*考点\*\*", a)
print(f"    考点行: {len(kaodian)} ｜ 思路行: {len(re.findall(r'> \\*\\*思路\\*\\*', a))}"
      f" ｜ 易错行: {len(re.findall(r'> \\*\\*易错\\*\\*', a))}")

# 4) 学生版：无答案/无解析/无来源行
leak = []
for pat, name in ((r"\*\*答案\*\*", "答案标记"), (r"> —— 解析 ——", "解析块"),
                  (r"^> \*\*考点\*\*", "考点行"), (r"来源：", "来源行")):
    n = len(re.findall(pat, s, re.M))
    if n:
        leak.append(f"{name}×{n}")
print(f"[4] 学生版越界内容: {leak if leak else '无（零答案）✓'}")

# 5) 两版题面一致性（去掉答案/解析/来源行后逐行比对）
def qonly(text):
    out, skip = [], False
    for line in text.split("\n"):
        if line.startswith("**答案**") or line.startswith("> —— 解析 ——"):
            skip = True
        if line.startswith("### 第 ") or line.startswith("# "):
            skip = False
        if not skip and not line.startswith("> **") and not line.startswith("来源："):
            out.append(line.strip())
    return [x for x in out if x]


qa, qs = qonly(a), qonly(s)
diff = [i for i, (x, y) in enumerate(zip(qa, qs)) if x != y]
print(f"[5] 题面行数 答案版 {len(qa)} / 学生版 {len(qs)} ｜ 差异行 {len(diff)}")
for i in diff[:5]:
    print(f"    #{i}: A={qa[i][:60]!r}\n         S={qs[i][:60]!r}")

# 6) 题卡溯源清单
lst = re.findall(r"^\| (\d+) \|", a, re.M)
print(f"[6] 卷末清单行数: {len(lst)} ｜ 题号: {lst}")

# 7) 图片引用统计
imgs_a = re.findall(r"!\[\[([^\]\|]+)", a)
imgs_s = re.findall(r"!\[\[([^\]\|]+)", s)
print(f"[7] 图引用 答案版 {len(imgs_a)}（去重 {len(set(imgs_a))}）｜学生版 {len(imgs_s)}（去重 {len(set(imgs_s))}）")
