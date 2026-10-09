# -*- coding: utf-8 -*-
"""从交付 docx 里抠出「空基底」元素并还原上下文，判定是缺陷还是良性（同位素等）。"""
import os, re, sys, zipfile
sys.stdout.reconfigure(encoding="utf-8")
D = r"C:\Obsidion\妙妙屋\00-首页\题组Word\初赛模拟卷\真题版式"

EMPTY = re.compile(r"<m:(sSub|sSup)>(?:(?!</m:\1>).)*?<m:e></m:e>", re.S)


def ctx(x, pos, n=90):
    """取该位置前后的可见文本（w:t + m:t）。"""
    head = x[:pos]
    tail = x[pos:pos + 700]
    def txt(s):
        return "".join(re.findall(r"<(?:w|m):t[^>]*>([^<]*)</(?:w|m):t>", s))
    return txt(head)[-n:], txt(tail)[:n]


for name in ("初赛模拟卷X（非有机·答案与解析版·真题版式）.docx",
             "初赛模拟卷XIp（非有机·学生版·真题版式）.docx",
             "初赛模拟卷XI（非有机·答案与解析版·真题版式）.docx"):
    p = os.path.join(D, name)
    x = zipfile.ZipFile(p).read("word/document.xml").decode("utf-8")
    hits = list(EMPTY.finditer(x))
    print("=" * 78)
    print("%s  空基底 %d 处" % (name[:40], len(hits)))
    for m in hits[:14]:
        b, a = ctx(x, m.start())
        kind = m.group(1)
        print("   [%s] …%s‖%s…" % (kind, b[-40:], a[:40]))
