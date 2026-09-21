"""补扫「标题行」里的裸上下标（原 scan_bare_sub2.py 把标题行当噪音跳过了）。"""
import os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
os.chdir(r"c:\Obsidion\妙妙屋")

# 裸上下标：X_{...} / X^{...} / 转义 \_{...}，且不在 $...$ 内
PAT = re.compile(r"(?<![\\$A-Za-z0-9])[A-Za-z\\][A-Za-z0-9]*[_^]\{")

ROOTS = sys.argv[1:] or ["04-题库"]
rows = []
for r in ROOTS:
    for dp, dn, fn in os.walk(r):
        for f in fn:
            if not f.endswith(".md"):
                continue
            p = os.path.join(dp, f)
            try:
                t = open(p, encoding="utf-8").read()
            except Exception:
                continue
            inf = False
            for i, l in enumerate(t.split("\n"), 1):
                s = l.strip()
                if s.startswith("```") or s.startswith("~~~"):
                    inf = not inf
                    continue
                if inf:
                    continue
                if not re.match(r"^#{1,6}\s", s):
                    continue
                # 遮蔽行内 math
                masked = re.sub(r"(?<!\\)\$[^$]*\$", "", s)
                if PAT.search(masked):
                    rows.append((p, i, s))

print("标题行命中:", len(rows), "文件:", len({r[0] for r in rows}))
for p, i, s in rows:
    print("  %s L%d: %s" % (p.replace("04-题库/", "").replace("\\", "/"), i, s[:120]))
