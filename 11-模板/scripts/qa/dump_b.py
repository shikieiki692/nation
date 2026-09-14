"""列出所有 docx 中含 `_{`/`^{`/`$` 的段落（B 类），判断是哪种污染。"""
import os, re, zipfile, collections
from xml.etree import ElementTree as ET
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
os.chdir(r"c:\Obsidion\妙妙屋")

files = []
for dp, dn, fn in os.walk("00-首页/题组Word/习题书"):
    for f in fn:
        if f.endswith(".docx") and not f.startswith("~$") and "打印版" not in f:
            files.append(os.path.join(dp, f))
files.sort()

pat = re.compile(r'\$|\^\s*\{|_\s*\{')
kinds = collections.Counter()
rows = []
for p in files:
    root = ET.fromstring(zipfile.ZipFile(p).read("word/document.xml"))
    for c in root.find(W + "body"):
        if c.tag != W + "p":
            continue
        t = "".join(x.text or "" for x in c.iter(W + "t"))
        if not t.strip() or not pat.search(t):
            continue
        k = ("dollar" if "$" in t else
             "brace-super" if re.search(r'\^\s*\{', t) else "brace-sub")
        kinds[k] += 1
        rows.append((k, os.path.basename(p), t))
print("总命中:", len(rows), dict(kinds))
print("=" * 110)
for k, f, t in rows[:34]:
    print("[%s] %s" % (k, f[:40]))
    print("    ", t[:190])
