# -*- coding: utf-8 -*-
"""打印卷 md 逐题：题面小问记法 + 答案区小问记法（判据21：点号式不重编号）。"""
import io, re, sys
sys.stdout.reconfigure(encoding="utf-8")
V = sys.argv[1] if len(sys.argv) > 1 else "XVI"
p = r"04-题库/初赛模拟卷%s（非有机·答案版）.md" % V
t = io.open(p, encoding="utf-8-sig").read()
parts = re.split(r"(?m)^### ", t)

NUM = re.compile(r"^\s{0,3}(\*\*)?([0-9]{1,2}(?:[.\-][0-9A-Za-z]{1,2})+)(\*\*)?")
for seg in parts[1:]:
    lines = seg.split("\n")
    title = lines[0]
    # 答案区分界
    ai = None
    for i, ln in enumerate(lines):
        if re.match(r"^#{2,6}\s*答案", ln.strip()) or ln.strip() == "#### 答案":
            ai = i
            break
    body = lines[1:ai] if ai else lines[1:]
    ans = lines[ai:] if ai else []
    print("\n" + "=" * 72)
    print("### " + title)
    def scan(ls, tag):
        got = []
        for ln in ls:
            s = ln.strip()
            if not s or s.startswith("!") or s.startswith(">"):
                continue
            m = NUM.match(s)
            if m and len(s) > len(m.group(0)) + 2:
                got.append(m.group(2) + " | " + s[:70])
        if got:
            print("  [" + tag + "]")
            for g in got[:26]:
                print("     " + g)
    scan(body, "题面")
    scan(ans, "答案")
