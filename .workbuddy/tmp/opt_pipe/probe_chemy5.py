import os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
FILES = {
    "32": os.path.join(R, "06-外部资料导入/OCR/chemy/_mineru_out/backup_mds_2026-10-02/第32届中国化学奥林匹克Chemy题目合集答案..md"),
    "33": os.path.join(R, "06-外部资料导入/OCR/chemy/_mineru_out/backup_mds_2026-10-02/第33届Chemy化学奥林匹克题目合集答案..md"),
}
# 卡: (届, 卷号, 题号, 分值)
CARDS = [
    ("32", 9, 5, 12, "题-CM-58-05"),
    ("32", None, 3, 10, "题-CM-60-03（决赛模拟）"),
    ("33", 2, 4, 11, "题-CM-62-04"),
    ("33", 5, 5, 10, "题-CM-65-05"),
    ("33", 8, 3, 8, "题-CM-68-03"),
]
for key in ("32", "33"):
    f = FILES[key]
    if not os.path.exists(f):
        print("缺失", f); continue
    t = open(f, encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")
    print("=" * 96)
    print("第%s届答案册 | %d 字" % (key, len(t)))
    heads = [(m.start(), m.group(0)[:56]) for m in re.finditer(r"(?m)^#\s*(?:第\s*[0-9]+\s*届.*?答案|第\s*\d+\s*题)[^\n]*$", t)]
    print("  标题数 %d" % len(heads))
    for no, pos, cn, score, name in [c for c in [(c[0], c[1], c[2], c[3], c[4]) for c in CARDS] if c[0] == key]:
        pat = r"第\s*%d\s*题[^\n]{0,20}" % cn
        hits = [(m.start(), m.group(0)[:44]) for m in re.finditer(pat, t)]
        print("  ---- %s（第%d题，%d分）: 全文「第%d题」出现 %d 次" % (name, cn, score, cn, len(hits)))
        for h in hits[:6]:
            print("       %7d  %s" % h)
