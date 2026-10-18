# -*- coding: utf-8 -*-
"""F 判据 v4（终版 + 多分隔符）。只读。

判据 95（第三个缺陷，与 90/91/93/94 同族）：
  题面区不能只按 `## 参考答案` 切分。实测 12,296 卡中 1,038 张（8.4%）用别的写法
  （`## 解答` 115／`## 答案` 44／`## 解析` 16／`## 答案与解析` 2／无分隔 861）。
  只认 `## 参考答案` ⇒ 这些卡的答案区被算进题面区，答案区的图被当成题面图 ⇒ 漏报。
  ⇒ 取所有分隔符变体中**最早出现**的位置切分。
"""
import io, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")

ROOT = r"C:\Obsidion\妙妙屋"
REF = re.compile(r"(下图|右图|左图|上图|如[上左下右]图|如下[上左下右]*图|见[上左下右]图|见图|如图)")
NUM = re.compile(r"(?<![画绘])图\s*\d")
EMB = re.compile(r"!\[\[([^\]\|\\]+)")
MDIMG = re.compile(r"!\[\]\(images/([^)\s]+)\)")
SEPS = ["\n## 参考答案", "\n## 答案与解析", "\n## 答案", "\n## 解答", "\n## 解析",
        "\n## 试题解析", "\n## 解题思路"]
SKIP = {"images", ".git", "_归档", "_archive"}


def split_fm(t):
    if t.startswith("---"):
        i = t.find("\n---", 3)
        if i > 0:
            return t[i + 4:]
    return t


def front_of(body):
    pos = [body.find(s) for s in SEPS if body.find(s) > 0]
    return body[:min(pos)] if pos else body


out = []
n = 0
for dp, dn, fn in os.walk(os.path.join(ROOT, "04-题库")):
    dn[:] = [d for d in dn if d not in SKIP]
    for f in fn:
        if not f.endswith(".md") or f.startswith("初赛模拟卷"):
            continue
        p = os.path.join(dp, f)
        try:
            t = io.open(p, encoding="utf-8-sig").read().replace("\r\n", "\n")
        except Exception:
            continue
        n += 1
        front = front_of(split_fm(t))
        if EMB.search(front) or MDIMG.search(front):
            continue
        lines = [l for l in front.split("\n") if REF.search(l)]
        numl = [l for l in front.split("\n") if NUM.search(l)]
        if not lines and not numl:
            continue
        rel = os.path.relpath(p, ROOT).replace("\\", "/")
        if os.path.basename(rel) in ("README.md", "索引.md"):
            continue
        marked = ("题面缺图" in t) or ("组卷隔离" in t) or ("**④ 缺图**" in t)
        out.append((rel, "REF" if lines else "NUM", marked, (lines + numl)[0].strip()[:110]))

print("CARD=%d  HIT=%d  已自标=%d  未自标=%d"
      % (n, len(out), sum(1 for o in out if o[2]), sum(1 for o in out if not o[2])))
io.open(r".workbuddy/tmp/_fig_v4.txt", "w", encoding="utf-8").write(
    "\n".join("%s\t%s\t%s\t%s" % o for o in sorted(out)))
print("\n--- 未自标明细 ---")
for r, k, m, s in sorted(out):
    if not m:
        print("  [%s] %s" % (k, r))
        print("        › %s" % s[:100])
