# -*- coding: utf-8 -*-
"""隔离实验（复核前提）：HTML 表 vs Markdown 表 → pandoc docx，数 w:tbl。
只读，输出到 .workbuddy/tmp/word_verify/iso/。
"""
import os, re, sys, io, zipfile
out = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
VAULT = r"C:\Obsidion\妙妙屋"
OUT = os.path.join(VAULT, ".workbuddy", "tmp", "word_verify", "iso")
os.makedirs(OUT, exist_ok=True)
import pypandoc

HTML_MD = """# 测试

<table><tr><td>元素</td><td>相对原子质量</td></tr><tr><td>Li</td><td>6.94</td></tr></table>

文字。
"""

MD_MD = """# 测试

| 元素 | 相对原子质量 |
| --- | --- |
| Li | 6.94 |

文字。
"""

HTML_MATH = """# 测试

<table><tr><td>元素</td><td>系数</td></tr><tr><td>$Fe^{2+}$</td><td>$K_{a}$</td></tr></table>
"""

MD_MATH = """# 测试

| 元素 | 系数 |
| --- | --- |
| $Fe^{2+}$ | $K_{a}$ |
"""

def conv(md, name, args):
    src = os.path.join(OUT, f"{name}.md")
    dst = os.path.join(OUT, f"{name}.docx")
    open(src, "w", encoding="utf-8", newline="\n").write(md)
    try:
        pypandoc.convert_file(src, "docx", outputfile=dst, extra_args=args)
    except Exception as e:
        return None, str(e)[:200]
    return dst, None

def inspect(p):
    z = zipfile.ZipFile(p)
    xml = z.read("word/document.xml").decode("utf-8", "replace")
    return dict(tbl=len(re.findall(r"<w:tbl[ >]", xml)),
                omath=len(re.findall(r"<m:oMath[ >]", xml)),
                dollar=len(re.findall(r"\$", xml)),
                raw_html=("<w:tbl" not in xml and "&lt;table" in xml))

CASES = [
    ("HTML 表（纯文字）", HTML_MD, ["--from=markdown+tex_math_dollars+pipe_tables", "--to=docx"]),
    ("MD 表（纯文字）",   MD_MD,   ["--from=markdown+tex_math_dollars+pipe_tables", "--to=docx"]),
    ("HTML 表（含公式）", HTML_MATH, ["--from=markdown+tex_math_dollars+pipe_tables", "--to=docx"]),
    ("MD 表（含公式）",   MD_MATH,   ["--from=markdown+tex_math_dollars+pipe_tables", "--to=docx"]),
    ("HTML 表（默认 reader）", HTML_MD, ["--to=docx"]),
    ("MD 表（默认 reader）",   MD_MD,   ["--to=docx"]),
]

print("== 隔离实验：HTML 表 vs MD 表 → pandoc docx ==", file=out)
print(f"{'用例':<26}{'w:tbl':>7}{'OMML':>7}{'残留$':>7}{'rawHTML':>9}", file=out)
for name, md, args in CASES:
    p, err = conv(md, name.replace(" ", "_").replace("（","_").replace("）",""), args)
    if err:
        print(f"{name:<26}  ERR {err}", file=out); continue
    d = inspect(p)
    print(f"{name:<26}{d['tbl']:>7}{d['omath']:>7}{d['dollar']:>7}{str(d['raw_html']):>9}", file=out)
out.flush()
