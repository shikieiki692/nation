# -*- coding: utf-8 -*-
"""回归测试：`docx_utils.postprocess_pandoc_docx` 必须**不改内容**。

背景：`render_gate` 只覆盖「预处理 → pandoc」这一段，**不含**产线最后一步后处理
（字体清理 / 图片约束 / Unicode 上下标转原生格式 …）。2026-09-21 用隔离实验验证过
它不伤内容，本测试把那次验证**固化为守卫** —— 以后谁改 `docx_utils`，跑它就知道有没有
把内容吃掉。

三条判据（都与实现无关）：
  ① 后处理前后，闸门口径的「产物字面 `$`」都为 0（公式没被降级成文本）；
  ② 真实 `<m:oMath>` 元素数与「上下标对象数」**不得减少**；
  ③ XML 实体归一 + Unicode 上下标字形归一后，可见文本**逐字相同**。

⚠️ 三个量具陷阱（第一版都踩过，故写死在这里）：
  · 不能用 `z.count("<m:oMath")` —— 它是 `<m:oMathPr>` / `<m:oMathPara>` 的**前缀**，
    后处理注入 `oMathPr` 会让计数虚增。→ 用 `<m:oMath(?=[ />])`。
  · 比较文本前要 `html.unescape`：python-docx 重序列化会把 `&quot;` 还原成字面引号。
  · 字形表要用 `docx_utils` **自己那两张**（`SUPER/SUBSCRIPT_CHAR_MAP`），
    否则漏掉字母型（`ₓ` `ₙ` `ⁿ`）会误报。
"""
import html
import importlib.util
import re
import subprocess
import sys
import zipfile
from pathlib import Path

V = Path(r"C:\Obsidion\妙妙屋")
SCRIPTS = V / "11-模板" / "scripts"
sys.path.insert(0, str(SCRIPTS))
PANDOC = r"C:\Users\蕾赛\AppData\Local\Pandoc\pandoc.exe"
TMP = V / ".workbuddy" / "tmp" / "_pp_check"
TMP.mkdir(parents=True, exist_ok=True)

# 取样 3 份：① 含大量 `\ce{}` 与箭头标注 ② 含 Unicode 上下标字形 ③ 含 DataviewJS/代码块
TARGETS = [
    "04-课件/学生讲义/6-有机化学/加成反应.md",
    "04-课件/学生讲义/2-结构化学/原子结构-超级充实版（自学完整）.md",
    "03-知识点/分析化学/元素分析.md",
]


def load(p, n):
    s = importlib.util.spec_from_file_location(n, p)
    m = importlib.util.module_from_spec(s)
    sys.modules[n] = m
    try:
        s.loader.exec_module(m)
    except SystemExit:
        pass
    return m


bh = load(SCRIPTS / "build-all-handout-docx.py", "bh")
du = load(SCRIPTS / "docx_utils.py", "du")
rg = load(SCRIPTS / "render_gate.py", "rg")

GLYPH = dict(du.SUPERSCRIPT_CHAR_MAP)
GLYPH.update(du.SUBSCRIPT_CHAR_MAP)
RE_OMATH = re.compile(r"<m:oMath(?=[ />])")


def norm_text(s: str) -> str:
    return "".join(GLYPH.get(c, c) for c in html.unescape(s))


def snap(p: Path):
    z = zipfile.ZipFile(p).read("word/document.xml").decode("utf-8")
    txt = "".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", z)) \
        + "".join(re.findall(r"<m:t[^>]*>([^<]*)</m:t>", z))
    return {"lit": rg._literal_dollars(z), "om": len(RE_OMATH.findall(z)),
            "sub": z.count("<m:sSub>") + z.count("<m:sSubSup>") + z.count("<m:sSup>"),
            "txt": norm_text(txt)}


fails = []
for rel in TARGETS:
    p = V / rel
    if not p.is_file():
        print("SKIP 不存在 %s" % rel)
        continue
    md = TMP / "s1.md"
    dx = TMP / "s1.docx"
    md.write_text(bh._preprocess_markdown(p.read_text(encoding="utf-8", errors="replace")), encoding="utf-8")
    subprocess.run([PANDOC, "-f", bh.PANDOC_EXTENSIONS, "-t", "docx", "-o", str(dx), str(md)], capture_output=True)
    if not dx.exists():
        print("SKIP pandoc 未产出 %s" % rel)
        continue
    b = snap(dx)
    du.postprocess_pandoc_docx(dx)
    a = snap(dx)
    msgs = []
    if a["lit"] or b["lit"]:
        msgs.append("字面$ %d→%d" % (b["lit"], a["lit"]))
    if a["om"] < b["om"]:
        msgs.append("oMath 减少 %d→%d" % (b["om"], a["om"]))
    if a["sub"] < b["sub"]:
        msgs.append("上下标对象减少 %d→%d" % (b["sub"], a["sub"]))
    if a["txt"] != b["txt"]:
        k = next((i for i in range(min(len(b["txt"]), len(a["txt"]))) if b["txt"][i] != a["txt"][i]),
                 min(len(b["txt"]), len(a["txt"])))
        msgs.append("文本不同 @%d 前=%r 后=%r" % (k, b["txt"][max(0, k - 16):k + 16], a["txt"][max(0, k - 16):k + 16]))
    name = "%s" % rel.split("/")[-1][:44]
    if msgs:
        fails.append(rel)
        print("FAIL %-46s %s" % (name, "; ".join(msgs)[:150]))
    else:
        print("PASS %-46s 字面$ %d→%d  oMath %d→%d  上下标 %d→%d"
              % (name, b["lit"], a["lit"], b["om"], a["om"], b["sub"], a["sub"]))

print()
if fails:
    print("❌ 后处理改动了内容：%s" % fails)
    sys.exit(1)
print("✅ 后处理内容守恒（3 份样本）")
