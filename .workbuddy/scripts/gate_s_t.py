# -*- coding: utf-8 -*-
r"""师-生题面一致闸门（通用，A 线全卷）——「学生版题面 ≡ 答案版题面」。

口径（仿 xvi_consistency.py，来自 `2026-10-14` 卷 XVI 实测）：
  · 按 `### 第 N 题` 切块；
  · 答案版**只取** `#### 答案` 之前的题面部分；
  · 允许答案版题面**独有** `> 来源` / `> 校勘` / `> [!info]` 行；
  · 比对前**剥块尾 `---` 与空行**（否则 300+ 假不一致）；模块标题 `## 第X部分` 不算题面内容；
  · 追加「学生版图引用必须全部出现在答案版」的集合检查。

用法：python gate_s_t.py --vol O1 ｜ --vol XVI
退出码：一致＝0；不一致＝1（可作闸门）。卷名中缀（有机/非有机）经 volname 运行时解析。
"""
import os, re, sys

VAULT = r"C:\Obsidion\妙妙屋"
sys.path.insert(0, os.path.join(VAULT, ".workbuddy", "scripts"))
import volname as VN

VOL = None
for i, a in enumerate(sys.argv):
    if a == "--vol" and i + 1 < len(sys.argv):
        VOL = sys.argv[i + 1]
if not VOL:
    print("用法：gate_s_t.py --vol <卷号>"); sys.exit(2)

ANS, STU = VN.md_path(VOL, "答案版"), VN.md_path(VOL, "学生版")


def load(p):
    return open(p, encoding="utf-8-sig").read().replace("\r\n", "\n")


def blocks_of(txt):
    out = {}
    for m in re.finditer(r"(?m)^### 第 (\d+) 题[^\n]*\n", txt):
        out[int(m.group(1))] = [m.start(), m.end()]
    keys = sorted(out)
    for i, k in enumerate(keys):
        e = out[keys[i + 1]][0] if i + 1 < len(keys) else len(txt)
        out[k] = txt[out[k][1]:e]
    return out


def qface(body, is_ans):
    if is_ans:
        am = re.search(r"(?m)^#### 答案\s*\n", body)
        body = body[:am.start()] if am else body
    lines = []
    for ln in body.split("\n"):
        t = ln.rstrip()
        if is_ans and t.lstrip().startswith(("> 来源", "> 校勘", "> [!info]")):
            continue
        if t.strip() in ("", "---"):
            continue
        if re.match(r"^##\s*第[一二三四]部分", t.strip()):  # 模块标题＝结构分隔，非题面内容
            continue
        lines.append(t.strip())
    return lines


if not (os.path.isfile(ANS) and os.path.isfile(STU)):
    print("缺文件：ANS=%s ｜ STU=%s" % (os.path.isfile(ANS), os.path.isfile(STU)))
    sys.exit(2)

a, s = load(ANS), load(STU)
ba, bs = blocks_of(a), blocks_of(s)
print("卷 %s 题块数：答案版 %d ｜ 学生版 %d" % (VOL, len(ba), len(bs)))
all_ok = True
for n in sorted(set(ba) | set(bs)):
    if n not in ba or n not in bs:
        print("第 %d 题：缺块！" % n); all_ok = False; continue
    qa, qs = qface(ba[n], True), qface(bs[n], False)
    if qa == qs:
        print("第 %2d 题：题面一致 ✓（%d 行）" % (n, len(qa)))
    else:
        all_ok = False
        print("第 %2d 题：✗ 不一致（答案版 %d 行 / 学生版 %d 行）" % (n, len(qa), len(qs)))
        for i in range(max(len(qa), len(qs))):
            x = qa[i] if i < len(qa) else "<缺>"
            y = qs[i] if i < len(qs) else "<缺>"
            if x != y:
                print("    #%d A=%r" % (i, x[:70]))
                print("        S=%r" % y[:70])

imgs_a = re.findall(r"!\[\[([^\]\|\\]+)", a)
imgs_s = re.findall(r"!\[\[([^\]\|\\]+)", s)
miss = [x for x in imgs_s if x not in imgs_a]
print("图引用：学生版 %d ｜ 答案版 %d ｜ 学生版图未进答案版：%s" % (len(imgs_s), len(imgs_a), miss or "无 ✓"))
print("RESULT:", "PASS" if (all_ok and not miss) else "FAIL")
sys.exit(0 if (all_ok and not miss) else 1)
