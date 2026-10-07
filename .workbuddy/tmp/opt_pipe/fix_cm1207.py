# -*- coding: utf-8 -*-
"""fix_cm1207.py —— 删除「题-CM-12-07」中的页眉噪点图（二维码 / 卡通 logo）。
题面：1bb27ea3（二维码，表格外）＋ 3f71a1cd（卡通，表格内）
答案：adce5881 / e0d4e767（二维码）＋ fccb2d0d（卡通）
"""
import io, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
CARD = os.path.join(R, "04-题库/2026机构初赛模拟题/chemy/题-CM-12-07-71近年人们发现高压下可以制.md")
BK = os.path.join(R, ".workbuddy/tmp/opt_pipe/cm_backup")
os.makedirs(BK, exist_ok=True)
apply = "--apply" in sys.argv

DROP_Q = ["1bb27ea368a70b785cffe66c629104cffebc432ca4c94975967808863db0bac1",
          "3f71a1cd99b29f5b363272b5a7456426ef0fc84603cd63e15b1a81ce4692618b"]
DROP_A = ["adce5881eb2216caa4ff051e602dd0e7dd199201791df13af56568ce745d3372",
          "e0d4e767d37c4856934277f4d6f9098865efe7bb47d6349d2f0b6c120a8d5e26",
          "fccb2d0dca942c8686b9a330e7cb65350f56307e3b68826a3a1204d6e7b7620a"]

t = io.open(CARD, encoding="utf-8-sig").read().replace("\r\n", "\n")
orig = t
i = t.find("## 题目"); j = t.find("## 参考答案"); k = t.find("## 知识点映射")
q, a = t[i:j], t[j:k]

nq = 0
for h in DROP_Q:
    # ① 表格内 <td><img src="images/H"/></td> ⇒ 置空单元格（保持表结构）
    pat1 = re.compile(r'<td>\s*<img src="images/%s\.jpg"\s*/>\s*</td>' % h)
    q, c1 = pat1.subn("<td></td>", q); nq += c1
    # ② 行内/独立 ![](images/H.jpg)
    pat2 = re.compile(r'\s*!\[\]\(images/%s\.jpg\)\s*' % h)
    q, c2 = pat2.subn(" ", q); nq += c2
na = 0
for h in DROP_A:
    pat = re.compile(r'[ \t]*!\[\]\(images/%s\.jpg\)[ \t]*\n?' % h)
    a, c = pat.subn("", a); na += c
print("题面删 %d 处（期望 2）、答案删 %d 处（期望 3）" % (nq, na))
assert nq == 2 and na == 3, "删除数不符，中止"

a = re.sub(r"\n{3,}", "\n\n", a)
newt = t[:i] + q + a + t[k:]
# 校勘注（附在答案区尾）
newt = newt.replace("## 知识点映射",
                    "> ⛔ 校勘（2026-10-07）：原题面/答案区混入源 PDF **页眉装饰图**（二维码 ×3、卡通 logo ×2），"
                    "系建卡期切图噪声，已删除，不影响题目内容。\n\n## 知识点映射", 1)
if apply:
    bfp = os.path.join(BK, os.path.basename(CARD) + ".orig")
    if not os.path.exists(bfp):
        io.open(bfp, "w", encoding="utf-8", newline="\n").write(orig)
    io.open(CARD, "w", encoding="utf-8", newline="\n").write(newt)
    print("✔ 已写入")
else:
    print("(dry-run)")
