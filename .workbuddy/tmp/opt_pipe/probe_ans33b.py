import os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
F33 = os.path.join(R, "06-外部资料导入/OCR/chemy/_mineru_out/backup_mds_2026-10-02/第33届Chemy化学奥林匹克题目合集答案..md")
t = open(F33, encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")
paper = list(re.finditer(r"(?m)^#{1,6}\s*第\s*33\s*届.*?模拟试卷\s*(\d+)\s*答案[^\n]*$", t))
print("卷标题 %d 个：%s" % (len(paper), [(m.group(1), m.start()) for m in paper]))
bounds = [(int(m.group(1)), m.start(), (paper[i + 1].start() if i + 1 < len(paper) else len(t)))
          for i, m in enumerate(paper)]
for no, a, b in bounds:
    seg = t[a:b]
    qs = [(m.start() + a, m.group(0)[:36]) for m in re.finditer(r"(?m)^#{1,6}\s*第\s*(\d+)\s*题[^\n]*$", seg)]
    print("  卷%-2s %6d..%6d (%d 字) | 题数 %d: %s" % (no, a, b, len(seg), len(qs), [q[1] for q in qs]))
