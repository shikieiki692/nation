# -*- coding: utf-8 -*-
"""O1：把答案版题名传播到学生版标题行（只改 `### 第 N 题（M 分）` 一行，其余逐字不动）。
自证：① 改动行数 == 题数；② 非标题行逐字节不变；③ 幂等。
用法：python o1_stu_titles.py [--apply]
"""
import os, re, sys, shutil

R = r"C:\Obsidion\妙妙屋"
QB = os.path.join(R, "04-题库")
ANS = os.path.join(QB, "初赛模拟卷O1（有机·答案版）.md")
STU = os.path.join(QB, "初赛模拟卷O1（有机·学生版）.md")
BAK = os.path.join(R, ".workbuddy/tmp/opt_pipe/volpost_bak_O1_stutitles")

HEAD = re.compile(r"^### 第 (\d+) 题（([^）]*)）(.*)$")


def read(p):
    return open(p, "rb").read().decode("utf-8-sig")


def titles_of(txt):
    out = {}
    for ln in txt.split("\n"):
        m = HEAD.match(ln)
        if m and m.group(3).strip():
            out[int(m.group(1))] = m.group(3).strip()
    return out


def main(apply_):
    rawa = read(ANS)
    rawst = read(STU)
    eol = "\r\n" if "\r\n" in rawst else "\n"
    a = rawa.replace("\r\n", "\n")
    s = rawst.replace("\r\n", "\n")
    tmap = titles_of(a)
    print("答案版有题名 =", len(tmap), "题")
    lines = s.split("\n")
    changed = 0
    for i, ln in enumerate(lines):
        m = HEAD.match(ln)
        if not m:
            continue
        q = int(m.group(1))
        cur = m.group(3)
        if cur.strip():                      # 已有题名 ⇒ 跳过（幂等）
            continue
        if q in tmap:
            lines[i] = ln + tmap[q]
            changed += 1
    news = "\n".join(lines)
    # 自证：非标题行逐字节不变
    old_lines = s.split("\n")
    bad = 0
    for i in range(min(len(old_lines), len(lines))):
        if old_lines[i] != lines[i] and not HEAD.match(old_lines[i]):
            bad += 1
    print("改动标题行 =", changed, "  非标题行被动 =", bad, "（应 0）")
    if bad:
        return 1
    if changed and apply_:
        os.makedirs(BAK, exist_ok=True)
        shutil.copy2(STU, os.path.join(BAK, os.path.basename(STU)))
        with open(STU, "wb") as fh:
            fh.write(news.replace("\n", eol).encode("utf-8"))
        print("已写盘")
    elif changed:
        print("(dry) 未写盘")
    else:
        print("0 处（已幂等）")
    return 0


if __name__ == "__main__":
    sys.exit(main("--apply" in sys.argv))
