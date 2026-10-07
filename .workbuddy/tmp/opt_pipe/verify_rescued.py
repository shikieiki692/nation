import glob, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
KEYS = ("题-CM-58-05", "题-CM-60-03", "题-CM-62-04", "题-CM-65-05", "题-CM-68-03", "题-CM-84-01", "题-CM-89-06")
for k in KEYS:
    hits = glob.glob(os.path.join(R, "04-题库/2026机构初赛模拟题/**/") + k + "*.md", recursive=True)
    if not hits:
        print("miss", k); continue
    p = hits[0]
    t = open(p, encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")
    j = t.find("## 参考答案"); kk = t.find("## 知识点映射")
    a = t[j + len("## 参考答案"):kk]
    print("=" * 96)
    print("%s | 答案区 %d 字" % (os.path.basename(p)[:56], len(a)))
    print(re.sub(r"\n{2,}", "\n", a)[:420])
