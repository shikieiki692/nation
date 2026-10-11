# -*- coding: utf-8 -*-
"""卷XVI 收口 QA（v2）：按真实标记（## 第N部分／#### 答案／> —— 解析 ——）核自洽。"""
import os
import re

VAULT = r"C:\Obsidion\妙妙屋"
ANS = os.path.join(VAULT, "04-题库/初赛模拟卷XVI（非有机·答案版）.md")
STU = os.path.join(VAULT, "04-题库/初赛模拟卷XVI（非有机·学生版）.md")
load = lambda p: open(p, encoding="utf-8-sig").read().replace("\r\n", "\n")
a, s = load(ANS), load(STU)

print("[2] 模块声明:")
for m in re.findall(r"^## 第[一二]部分.*$", a, re.M):
    print("   ", m)
for m in re.findall(r"^## 第[一二]部分.*$", s, re.M):
    print("   (学生版)", m)
print("   → 答案版/学生版 模块段数:", len(re.findall(r"^## 第[一二]部分", a, re.M)),
      "/", len(re.findall(r"^## 第[一二]部分", s, re.M)))

# 答案区
blocks = re.split(r"^#### 答案$", a, flags=re.M)
print(f"\n[3] #### 答案 段数: {len(blocks)-1}")
short = [i for i, b in enumerate(blocks[1:], 1) if len(re.sub(r"\s+", "", b)) < 40]
print("    过短(<40 非空白字)的段:", short if short else "无 ✓")

# 逐题结构（题头 → 答案 → 解析 → 考点/思路/易错）
qsec = re.split(r"^### 第 (\d+) 题", a, flags=re.M)
rows = []
for k in range(1, len(qsec), 2):
    no = int(qsec[k]); body = qsec[k + 1]
    has_ans = "#### 答案" in body
    has_par = "> —— 解析 ——" in body
    has_kd = "> **考点**" in body
    has_sl = "> **思路**" in body
    has_yc = "> **易错**" in body
    n_xiang = len(re.findall(r"^> \*\*\d+-\d", body, re.M))
    rows.append((no, has_ans, has_par, has_kd, has_sl, has_yc, n_xiang))
print("\n[4] 逐题结构（题号 答案 解析 考点 思路 易错 详解条数）:")
bad = 0
for r in rows:
    flag = "" if all(r[1:6]) and r[6] > 0 else "  ← 缺"
    if flag:
        bad += 1
    print(f"    第{r[0]:>2}题  {'✓' if r[1] else '✗'}    {'✓' if r[2] else '✗'}    "
          f"{'✓' if r[3] else '✗'}    {'✓' if r[4] else '✗'}    {'✓' if r[5] else '✗'}    {r[6]:>3}{flag}")
print(f"    结构不完整题数: {bad}")

# 学生版污染
print("\n[5] 学生版污染检查:")
for pat, name in ((r"^#### 答案$", "#### 答案"), (r"> —— 解析 ——", "解析块"),
                  (r"^> \*\*考点\*\*", "考点行"), (r"^> 来源：", "来源行"),
                  (r"^### 第 \d+ 题（\d+ 分）[^\n]+$", "题名尾（应为空）")):
    n = len(re.findall(pat, s, re.M))
    print(f"    {name}: {n} {'✓' if n == 0 else '← 需查'}")

# 题面区一致性：剔掉 答案/解析/来源/分值题头差异后比对
def qbody(text):
    out, skip = [], False
    for ln in text.split("\n"):
        if ln.startswith("#### 答案") or ln.startswith("> —— 解析 ——"):
            skip = True
        if ln.startswith("### 第 ") or ln.startswith("## ") or ln.startswith("# "):
            skip = False
        if skip:
            continue
        if ln.startswith("> 来源：") or ln.startswith("> 题卡溯源") or ln.startswith("> 请将答案"):
            continue
        if re.match(r"^### 第 \d+ 题", ln):
            ln = re.sub(r"^### 第 (\d+) 题.*$", r"### 第 \1 题", ln)
        out.append(ln.rstrip())
    return out

qa, qs = qbody(a), qbody(s)
# 去掉 FM 与标题区（应差）后对齐
def cut_fm(x):
    i = x.index("# 初赛模拟卷 XVI") if "# 初赛模拟卷 XVI" in x else 0
    for j, ln in enumerate(x):
        if ln.startswith("## 第"):
            return x[j:]
    return x

qa, qs = cut_fm(qa), cut_fm(qs)
n = min(len(qa), len(qs))
diff = [(i, qa[i], qs[i]) for i in range(n) if qa[i] != qs[i]]
print(f"\n[6] 题面区（第 1 部分起）行数 答案版 {len(qa)} / 学生版 {len(qs)} ｜ 差异 {len(diff)}")
for i, x, y in diff[:8]:
    print(f"    #{i}: A={x[:70]!r}\n          S={y[:70]!r}")
