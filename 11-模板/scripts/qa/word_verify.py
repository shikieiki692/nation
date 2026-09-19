# -*- coding: utf-8 -*-
"""Word 管线端到端验证：同一文件「转换前(HEAD) vs 转换后(工作区)」各转 docx，
   数 w:tbl / w:drawing / OMML 公式数，验证本批转换的真实收益。
只读源文件，docx 输出到 .workbuddy/tmp/word_verify/。
"""
import os, re, sys, io, subprocess, zipfile, json
out = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
VAULT = r"C:\Obsidion\妙妙屋"
TMP = os.path.join(VAULT, ".workbuddy", "tmp")
OUT = os.path.join(TMP, "word_verify")
os.makedirs(OUT, exist_ok=True)

# 挑样本：本批转换文件，覆盖「含公式表」「纯文字表」「rowspan 表」三类
SAMPLES = [
    # (相对路径, 说明)
    ("06-外部资料导入/25-32届真题解析/中国化学奥林匹克竞赛试题解析（第4版）裴坚,卞江,柳晗宇Z-Library_210-380.md", "含公式 + rowspan"),
    ("06-外部资料导入/OCR/化学能力测试OCR源/（已压缩）化学竞赛能力测试.md", "含公式 + rowspan(2行表头)"),
    ("mineru/03-教材书籍/普通化学原理（第4版）/普通化学原理第4版 1-200.md", "纯文字表"),
    ("06-外部资料导入/33-34届决赛/第33届中国化学奥林匹克（决赛）理论试题（解析版）.md", "纯文字表(真题)"),
]

def md2docx(md_text, tag):
    import pypandoc
    src = os.path.join(OUT, f"_{tag}.md")
    dst = os.path.join(OUT, f"{tag}.docx")
    open(src, "w", encoding="utf-8", newline="\n").write(md_text)
    try:
        pypandoc.convert_file(src, "docx", outputfile=dst,
                              extra_args=["--from=markdown+tex_math_dollars+pipe_tables",
                                          "--to=docx"])
    except Exception as e:
        return None, f"pandoc err: {e}"
    return dst, None

def inspect(docx_path):
    """返回 w:tbl 数、w:drawing 数、OMML 公式数（m:oMath）"""
    try:
        z = zipfile.ZipFile(docx_path)
        xml = z.read("word/document.xml").decode("utf-8", "replace")
    except Exception as e:
        return None
    return dict(
        tbl=len(re.findall(r"<w:tbl[ >]", xml)),
        drawing=len(re.findall(r"<w:drawing[ >]", xml)),
        omath=len(re.findall(r"<m:oMath[ >]", xml)),
        katex_src=len(re.findall(r"\\frac|\\mathrm|\\times", xml)),
    )

rows = []
for rel, desc in SAMPLES:
    p = os.path.join(VAULT, rel)
    if not os.path.exists(p):
        print(f"跳过（不存在）: {rel}", file=out); continue
    cur = open(p, encoding="utf-8").read()
    r = subprocess.run(["git", "show", f"HEAD:{rel}"], capture_output=True, cwd=VAULT)
    old = r.stdout.decode("utf-8", "replace") if r.returncode == 0 else None
    if old is None:
        print(f"跳过（HEAD 无）: {rel}", file=out); continue

    do, eo = md2docx(old, f"BEFORE_{len(rows)}")
    dn, en = md2docx(cur, f"AFTER_{len(rows)}")
    io_ = inspect(do) if do else None
    in_ = inspect(dn) if dn else None
    rows.append(dict(rel=rel, desc=desc, before=io_, after=in_, eo=eo, en=en))

print("== Word 管线端到端验证（pandoc 3.10）==", file=out)
print(f"{'样本':<44}{'w:tbl':>14}{'公式(OMML)':>14}", file=out)
print(f"{'':44}{'前 → 后':>14}{'前 → 后':>14}", file=out)
for r in rows:
    b, a = r["before"], r["after"]
    if not b or not a:
        print(f"{r['desc']:<44}  ERR {r['eo'] or ''} {r['en'] or ''}", file=out); continue
    print(f"{r['desc']:<44}{b['tbl']:>6} → {a['tbl']:<6}{b['omath']:>6} → {a['omath']:<6}", file=out)
print("\n（w:tbl = Word 表格数；公式(OMML) = m:oMath 数）", file=out)
json.dump(rows, open(os.path.join(TMP, "_word_verify.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
out.flush()
