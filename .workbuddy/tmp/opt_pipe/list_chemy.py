import csv, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
rows = [r for r in csv.DictReader(open(os.path.join(R, "09-审计报告/2026-10-07-不可组卷题目清单.csv"), encoding="utf-8-sig"))
        if r["reason"] == "无答案/占位"]
SF = re.compile(r"^source_file:\s*\"?(.*?)\"?\s*$", re.M)
SN = re.compile(r"^source_norm:\s*\"?(.*?)\"?\s*$", re.M)
H1 = re.compile(r"^#{1,4}\s*第\s*([0-9一二三四五六七八九十]+)\s*题[^\n]*", re.M)
for r in rows:
    p = os.path.join(R, r["path"])
    t = open(p, encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")
    fm = t.split("---", 2)[1] if t.startswith("---") else ""
    s = (SF.search(fm).group(1) if SF.search(fm) else "")
    n = (SN.search(fm).group(1) if SN.search(fm) else "")
    if "Chemy" not in s and "ChO" not in s:
        continue
    m = H1.search(t)
    print("%-54s" % os.path.basename(r["path"])[:54])
    print("    source_file = %s" % s[:86])
    print("    source_norm = %s" % n[:70])
    print("    H1标题      = %s" % (m.group(0)[:46] if m else "—"))
