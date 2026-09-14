"""扫描 docx 产物中的排版污染：A 类 LaTeX 源码态泄漏、HTML 标签泄漏、真表格计数。"""
import sys, os, re, zipfile, json
from xml.etree import ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

# A 类：LaTeX 源码态（这些串出现在 w:t 里即为泄漏）
A_PATTERNS = [
    (r"\$\$", "dollar-dollar"),
    (r"\\begin\{", "begin-env"),
    (r"\\frac\{", "frac"),
    (r"\\mathrm\{", "mathrm"),
    (r"\\xrightarrow", "xarrow"),
    (r"\\Delta", "Delta"),
    (r"\\mathrm", "mathrm-bare"),
    (r"\\text\{", "text"),
]
# B 类：花括号上标残留 / HTML 标签
B_PATTERNS = [
    (r"<table", "html-table"),
    (r"<tr>|</?td>", "html-cell"),
    (r"<details>|</?summary>", "html-details"),
    (r"<br\s*/?>", "html-br"),
    (r"&lt;|&amp;|&gt;", "html-entity"),
    (r"\^\s*\{[^}]{1,20}\}", "brace-super"),
    (r"_\s*\{[^}]{1,20}\}", "brace-sub"),
]

def scan(path):
    z = zipfile.ZipFile(path)
    root = ET.fromstring(z.read("word/document.xml"))
    body = root.find(W + "body")
    n_tbl = sum(1 for c in body if c.tag == W + "tbl")
    n_omml = len(list(root.iter("{http://schemas.openxmlformats.org/officeDocument/2006/math}oMath")))
    n_oommlpara = len(list(root.iter("{http://schemas.openxmlformats.org/officeDocument/2006/math}oMathPara")))
    hits_a = {}
    hits_b = {}
    samples = []
    for c in body:
        if c.tag != W + "p":
            continue
        t = "".join(x.text or "" for x in c.iter(W + "t"))
        if not t.strip():
            continue
        for pat, name in A_PATTERNS:
            if re.search(pat, t):
                hits_a[name] = hits_a.get(name, 0) + 1
                if len(samples) < 8:
                    samples.append(("A/" + name, t[:160]))
                break
        for pat, name in B_PATTERNS:
            if re.search(pat, t):
                hits_b[name] = hits_b.get(name, 0) + 1
                if len(samples) < 8:
                    samples.append(("B/" + name, t[:160]))
                break
    return dict(tbl=n_tbl, omml=n_omml, omath_para=n_oommlpara, A=hits_a, B=hits_b, samples=samples)

if __name__ == "__main__":
    roots = sys.argv[1:]
    files = []
    for r in roots:
        for dp, dn, fn in os.walk(r):
            for f in fn:
                if f.endswith(".docx") and not f.startswith("~$"):
                    if os.environ.get("SKIP_PRINT") == "1" and "打印版" in f:
                        continue
                    files.append(os.path.join(dp, f))
    files.sort()
    tot_a = tot_b = 0
    rows = []
    for p in files:
        try:
            r = scan(p)
        except Exception as e:
            print("ERR", p, e); continue
        sa = sum(r["A"].values()); sb = sum(r["B"].values())
        tot_a += sa; tot_b += sb
        rows.append((sa, sb, r, p))
    rows.sort(key=lambda x: -(x[0] + x[1]))
    print("文件数 %d | A类(LaTeX源码态) 合计 %d | B类(HTML/花括号) 合计 %d" % (len(rows), tot_a, tot_b))
    print("-" * 100)
    for sa, sb, r, p in rows:
        if sa + sb == 0:
            continue
        print("%-72s A=%-4d B=%-4d tbl=%-3d omml=%-4d" % (os.path.basename(p)[:70], sa, sb, r["tbl"], r["omml"]))
        print("        A:", r["A"])
        print("        B:", r["B"])
