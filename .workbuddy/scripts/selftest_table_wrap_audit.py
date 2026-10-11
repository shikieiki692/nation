# -*- coding: utf-8 -*-
"""table_wrap_audit 自证（P1-7 精神）：判据必须能抓到**已知缺陷样本**，否则放宽＝瞎。

做法：取卷 XVI 学生版 docx，把颜色表**还原成修复前的错误网格**（20 根 gridCol×600tw、
21 个 tcW×600tw、tblW 9752tw ⇒ 总宽 12000tw > 表宽），另存临时文件，跑审计。
预期：审计报「✗ grid 总宽 > 表宽」；对**未改**的原件应报 OK。
"""
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

VAULT = Path(r"C:\Obsidion\妙妙屋")
SRC = VAULT / "00-首页/题组Word/初赛模拟卷/真题版式/初赛模拟卷XVI（非有机·学生版·真题版式）.docx"
TMP = VAULT / ".workbuddy/tmp/opt_pipe/_selftest"
TMP.mkdir(parents=True, exist_ok=True)
BAD = TMP / "坏网格样本.docx"
PY = sys.executable
AUDIT = VAULT / ".workbuddy/scripts/table_wrap_audit.py"

# 1) 由原件造两个「坏网格」样本：A=列数不齐（20 根）、B=总宽超（21 根×600=12600>9752）
zin = zipfile.ZipFile(SRC)
NAMES = [it.filename for it in zin.infolist()]
DATA = {n: zin.read(n) for n in NAMES}          # ★ 一次读全（避免多次 read 触发 zip 头部错乱）
zin.close()
xml = DATA["word/document.xml"].decode("utf-8")
tbls = re.findall(r"<w:tbl>[\s\S]*?</w:tbl>", xml)
target = [t for t in tbls if "缁" in t][0]


def make_sample(ncol_grid, tag, w=600):
    bad = re.sub(r"<w:tblGrid>[\s\S]*?</w:tblGrid>",
                 "<w:tblGrid>" + f'<w:gridCol w:w="{w}"/>' * ncol_grid + "</w:tblGrid>", target, count=1)
    bad = re.sub(r'<w:tcW w:type="dxa" w:w="\d+"/>', f'<w:tcW w:type="dxa" w:w="{w}"/>', bad)
    bad = re.sub(r"<w:tblCellMar>[\s\S]*?</w:tblCellMar>", "", bad)
    p = TMP / f"坏网格样本{tag}.docx"
    xml2 = xml.replace(target, bad)
    with zipfile.ZipFile(p, "w", zipfile.ZIP_DEFLATED) as z:
        for n in NAMES:
            z.writestr(n, xml2.encode("utf-8") if n == "word/document.xml" else DATA[n])
    print("样本已生成：", p.name)
    return p


BAD_A = make_sample(20, "-A-列数不齐")
BAD_B = make_sample(21, "-B-总宽超")


def run(p, label):
    r = subprocess.run([PY, "-X", "utf8", str(AUDIT), str(p)], capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    out = (r.stdout or "")
    hit = [l.strip() for l in out.splitlines() if l.strip().startswith("[表") and ("✗" in l or "折行" in l)]
    print(f"  [{label}] 缺陷行: {hit if hit else '无（OK）'}")
    return hit


print("\n① 样本A：gridCol 20 ≠ 单元格 21（预期报网格错误）:")
h1 = run(BAD_A, "样本A")
print("\n② 样本B：21 根 gridCol 总宽 12600tw > 表宽 9752tw（预期报总宽超）:")
h2 = run(BAD_B, "样本B")
print("\n③ 原件（预期无缺陷）:")
h3 = run(SRC, "原件")
ok = bool(h1) and bool(h2) and not h3
print("\n自证结果:", "✅ PASS（两条判据都有牙、原件干净）" if ok else "❌ FAIL（判据未抓到已知缺陷）")
sys.exit(0 if ok else 1)

