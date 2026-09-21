"""pandoc 方言行为级防护：docx 线必须禁用 `superscript`/`subscript`（2026-09-21 格式线）。

【为什么必须禁】
本库源 md 里 `~` 的**主导用法是区间记号**（`70~80℃`、`400~430`、`pH 2~3`），
且经全库普查（非源层 340 处 / 173 份）**没有一处**是把 `~x~` 当化学下标写的。
而 pandoc 的 `subscript` 扩展要求定界符之间**不含空格**，中文行内标点恰好前后无空格
⇒ 区间会被**静默吞成下标**：
    `300~500°C（573~773 K）` → `300\\textsubscript{500°C（573}773 K）`
**已出货实证**：`00-首页/学生讲义PDF/化学平衡-超级充实版（自学完整）.pdf`（18 页）中
印的是 `工业上选用300500°C(573773K)配铁催化剂` —— 区间被吃掉。

【为什么禁用是安全的】
管线自己的上下标机制是「ASCII → Unicode 字形 → docx 原生 vertAlign」
（见 `_SIMPLE_SUPERSCRIPT_MAP` / `docx_utils` 后处理），**不依赖** pandoc 两个扩展。
实测：`CaF₂`（Unicode）在新方言下仍产生下标。

本测试既是「常量断言」也是「行为断言」，并提供**反向自证**（模拟旧方言必须报错），
以免判据本身失效。
"""
import importlib.util
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

VAULT = Path(r"C:\Obsidion\妙妙屋")
PANDOC = r"C:\Users\蕾赛\AppData\Local\Pandoc\pandoc.exe"

n_pass = n_fail = 0


def report(name, ok, extra=""):
    global n_pass, n_fail
    n_pass += ok
    n_fail += (not ok)
    print("%-4s %-46s %s" % ("PASS" if ok else "FAIL", name, extra))


def load(path, name):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s)
    sys.modules[name] = m
    try:
        s.loader.exec_module(m)
    except SystemExit:
        pass
    return m


bh = load(VAULT / "11-模板" / "scripts" / "build-all-handout-docx.py", "bh_dialect")
rg = load(VAULT / "11-模板" / "scripts" / "render_gate.py", "rg_dialect")

# ① 常量断言：管线方言必须显式禁用
ext = bh.PANDOC_EXTENSIONS
report("管线方言含 -superscript", "-superscript" in ext, ext[-46:])
report("管线方言含 -subscript", "-subscript" in ext)

# ② 无漂移：闸门侧读的就是管线那一份
report("render_gate 方言 == 管线方言", rg.PANDOC_EXT == ext)

# ③ 行为断言（docx 产物）
def docx_facts(ext_str, md):
    with tempfile.TemporaryDirectory() as td:
        s = Path(td) / "t.md"
        o = Path(td) / "t.docx"
        s.write_text(md, encoding="utf-8")
        subprocess.run([PANDOC, str(s), "--from=" + ext_str, "-o", str(o)], capture_output=True)
        x = zipfile.ZipFile(o).read("word/document.xml").decode("utf-8")
    txt = "".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", x))
    return x.count('vertAlign w:val="subscript"'), txt


RANGE_MD = "工业上选用 300~500°C（573~773 K）配铁催化剂。"
n_sub, txt = docx_facts(ext, RANGE_MD)
report("区间在管线方言下**不产生下标**", n_sub == 0, "subscript=%d" % n_sub)
report("区间可见字符保留", "300~500" in txt, repr(txt[:34]))

# Unicode 上下标：原样穿过 pandoc，之后由 `docx_utils.postprocess_pandoc_docx`
# 转成 Word 原生 vertAlign（该步已有独立回归测试 `test_postprocess_preserves_content.py`）。
# 此处只断言「不被吃掉」——因为一旦 re-enable `subscript`，pandoc 会去啃 `~…~`。
n_sub2, txt2 = docx_facts(ext, "CaF₂ 与 NH₃。")
report("Unicode ₂ 原样存活（不靠扩展）", ("₂" in txt2 and "₃" in txt2), repr(txt2[:20]))

# ④ 反向自证：模拟「未禁用」的旧方言，上面的断言必须会响
OLD_EXT = ext.replace("-superscript-subscript", "")
assert OLD_EXT != ext, "无法构造旧方言，检查管线"
n_old, txt_old = docx_facts(OLD_EXT, RANGE_MD)
report("反向自证·旧方言确实吞字（判据会响）", n_old >= 1 and "300~500" not in txt_old,
       "subscript=%d 文本=%r" % (n_old, txt_old[:26]))

print()
print("=" * 62)
print("PASS %d / FAIL %d" % (n_pass, n_fail))
sys.exit(1 if n_fail else 0)
