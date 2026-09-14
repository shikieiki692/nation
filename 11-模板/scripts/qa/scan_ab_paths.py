"""A/B 污染扫描（带相对路径；排除 _归档 与 *.tmp.docx）。"""
import sys, os, re, zipfile
from xml.etree import ElementTree as ET
sys.stdout.reconfigure(encoding="utf-8")
os.chdir(r"c:\Obsidion\妙妙屋")
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

A_PATTERNS = [
    (r"\$\$", "dollar-dollar"), (r"\\begin\{", "begin-env"), (r"\\frac\{", "frac"),
    (r"\\mathrm\{", "mathrm"), (r"\\xrightarrow", "xarrow"), (r"\\Delta", "Delta"),
    (r"\\mathrm", "mathrm-bare"), (r"\\text\{", "text"),
]
B_PATTERNS = [
    (r"<table", "html-table"), (r"<tr>|</?td>", "html-cell"),
    (r"<details>|</?summary>", "html-details"), (r"<br\s*/?>", "html-br"),
    (r"&lt;|&amp;|&gt;", "html-entity"),
    (r"\^\s*\{[^}]{1,20}\}", "brace-super"), (r"_\s*\{[^}]{1,20}\}", "brace-sub"),
]

def scan(path):
    z = zipfile.ZipFile(path)
    root = ET.fromstring(z.read("word/document.xml"))
    body = root.find(W + "body")
    ha, hb = {}, {}
    for c in body:
        if c.tag != W + "p":
            continue
        t = "".join(x.text or "" for x in c.iter(W + "t"))
        if not t.strip():
            continue
        for pat, name in A_PATTERNS:
            if re.search(pat, t):
                ha[name] = ha.get(name, 0) + 1
                break
        for pat, name in B_PATTERNS:
            if re.search(pat, t):
                hb[name] = hb.get(name, 0) + 1
                break
    return ha, hb

roots = sys.argv[1:]
rows = []
for r in roots:
    for dp, dn, fn in os.walk(r):
        if "_归档" in dp.replace("\\", "/").split("/"):
            continue
        for f in fn:
            if not f.endswith(".docx") or f.startswith("~$") or ".tmp.docx" in f:
                continue
            if os.environ.get("SKIP_PRINT") == "1" and "打印版" in f:
                continue
            p = os.path.join(dp, f)
            try:
                ha, hb = scan(p)
            except Exception as e:
                print("ERR", p, e); continue
            sa, sb = sum(ha.values()), sum(hb.values())
            if sa + sb:
                rows.append((sa + sb, sa, sb, ha, hb, p.replace("\\", "/")))

rows.sort(key=lambda x: -x[0])
print("非零文件数:", len(rows))
print("=" * 118)
for tot, sa, sb, ha, hb, p in rows:
    print("%-78s A=%-4d B=%-4d" % (p[:76], sa, sb))
    print("     A=%s  B=%s" % (ha, hb))
