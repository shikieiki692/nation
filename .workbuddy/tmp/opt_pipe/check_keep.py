import csv, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, ".workbuddy/tmp/opt_pipe")
sys.argv = ["x", "--vol", "CK", "--all-years"]
import build_org as BO
R = r"C:\Obsidion\妙妙屋"
HDR = re.compile(r'第\s*(\d{1,2})\s*[题題愿腰段顾][^\n]{0,24}[（(]\s*\d+\s*分')

def _ns_map(s):
    chs, idx = [], []
    for i, c in enumerate(s):
        if not c.isspace():
            chs.append(c); idx.append(i)
    return "".join(chs), idx

def map_back(raw, cleaned, cutpos):
    cn, _ = _ns_map(cleaned); rn, ridx = _ns_map(raw)
    n = len(re.sub(r"\s+", "", cleaned[:cutpos]))
    anchor = cn[max(0, n - 60):n]
    p = rn.find(anchor)
    if p < 0 or len(anchor) < 8:
        return None
    e = p + len(anchor)
    return ridx[e - 1] + 1 if 0 < e <= len(ridx) else None

rows = [r for r in csv.DictReader(open(os.path.join(R, "09-审计报告/2026-10-07-不可组卷题目清单.csv"), encoding="utf-8-sig"))
        if r["reason"] == "题面泄露"]
for r in rows:
    p = os.path.join(R, r["path"])
    t = open(p, encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")
    i = t.find("## 题目"); j = t.find("## 参考答案")
    own = BO.own_qno(t, p)
    rawq = t[i:j]
    c = BO.X.extract(p)
    q = BO.html_table_to_md(BO.conv_imgs(BO.clean_q(c["question"])))
    q1 = re.sub(r'^#{0,4}[^\S\n]*第[^\S\n]*%s[^\S\n]*[题題][^\n]*$' % (own if own else r'\d+'), '', q, flags=re.M)
    pos = None
    for m in HDR.finditer(q1):
        if own is None or int(m.group(1)) != own:
            pos = m.start(); break
    if pos is None:
        continue
    cut = map_back(rawq, q, pos)
    if cut is None:
        print("### %s | 回映射失败" % os.path.basename(p)[:50]); continue
    keep = rawq[:cut].rstrip()
    ownsub = re.findall(r'(?m)^\s*\*{0,2}(%s)\s*[-－]\s*\d' % own, keep)
    print("=" * 96)
    print("%s | own=%s | 留 %d 字 | 本卡小问出现 %d 次 %s" % (os.path.basename(p)[:50], own, len(keep), len(ownsub), sorted(set(ownsub))))
    print("  保留段 首 260: …%s…" % re.sub(r"\s+", " ", keep[:260]))
    print("  保留段 尾 200: …%s…" % re.sub(r"\s+", " ", keep[-200:]))
