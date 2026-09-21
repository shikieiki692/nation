"""阶段6 字体补丁：把已存在的产物 docx 的代码块字体改为等宽（SimSun）。

与修好的管线（docx_utils.postprocess_pandoc_docx 的 MONO_STYLES/MONO_FONT 豁免）产出等价，
用于让**不重导**的历史产物也立刻受益。

改动范围（严格限定）：
  1. word/styles.xml —— styleId 为 VerbatimChar / SourceCode 的样式，其 rFonts 四属性设为 SimSun
  2. word/document.xml —— pStyle 为 SourceCode 的段落内，所有 rFonts 四属性设为 SimSun
不碰正文/标题/表格样式，不碰行内代码 run（非 SourceCode 段落内）。

用法：
  python patch_mono_font.py            # dry-run，只统计
  python patch_mono_font.py --apply    # 落盘
"""
import re
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(r"C:\Obsidion\妙妙屋")
OUT = ROOT / "06-学生侧材料" / "讲义"
BAK = ROOT / ".workbuddy" / "tmp" / "bak_mono"
MONO = "SimSun"
TARGETS = ("VerbatimChar", "SourceCode")
ATTRS = ("ascii", "hAnsi", "eastAsia", "cs")

PARA = re.compile(r"<w:p[ >].*?</w:p>", re.S)
PS = re.compile(r'<w:pStyle w:val="([^"]+)"')


def mono_rfonts(prefix: str) -> str:
    p = prefix + ":" if prefix else ""
    return "<%srFonts %s/>" % (p, " ".join('%s%s="%s"' % (p, a, MONO) for a in ATTRS))


def patch_styles(xml: str) -> tuple:
    """返回 (新 xml, 改动数)。

    注意：同一份 styles.xml 里前缀可能是**混合**的（实测 VerbatimChar 用 ns0:、
    SourceCode 用 w:），所以既不能假定统一前缀，也不能用样式标签的前缀去拼 rFonts ——
    前缀要从实际命中的 rFonts 元素上取。
    """
    n = 0
    for sid in TARGETS:
        pat = re.compile(r"<([A-Za-z0-9]+):style\b[^>]*styleId=\"%s\".*?</\1:style>" % sid, re.S)
        mm = pat.search(xml)
        if not mm:
            continue
        seg = mm.group(0)
        new_seg = seg
        rf = re.search(r"<([A-Za-z0-9]+):rFonts\b[^>]*/>", new_seg, re.S)
        if rf:
            new_seg = new_seg[:rf.start()] + mono_rfonts(rf.group(1)) + new_seg[rf.end():]
        else:
            own = re.match(r"<([A-Za-z0-9]+):style", new_seg).group(1)
            rpr_open = re.search(r"<([A-Za-z0-9]+):rPr\b[^>]*>", new_seg)
            if rpr_open:
                new_seg = (new_seg[:rpr_open.end()] + mono_rfonts(own)
                           + new_seg[rpr_open.end():])
            else:
                close = "</%s:style>" % own
                new_seg = new_seg.replace(
                    close, "<%s:rPr>%s</%s:rPr>%s" % (own, mono_rfonts(own), own, close), 1)
        if new_seg != seg:
            xml = xml[:mm.start()] + new_seg + xml[mm.end():]
            n += 1
    return xml, n


def patch_document(xml: str) -> tuple:
    """只改 pStyle=SourceCode 的段落。"""
    n = 0
    out, pos = [], 0
    for mm in PARA.finditer(xml):
        block = mm.group(0)
        ps = PS.search(block)
        if not ps or ps.group(1) != "SourceCode":
            continue
        new_block = re.sub(r"<(\w+:)?rFonts\b[^>]*/>",
                           lambda m: mono_rfonts((m.group(1) or "w:")[:-1]),
                           block)
        if new_block != block:
            out.append((mm.start(), mm.end(), new_block))
            n += 1
    for s, e, b in reversed(out):
        xml = xml[:s] + b + xml[e:]
    return xml, n


def main(argv):
    apply = "--apply" in argv
    BAK.mkdir(parents=True, exist_ok=True)
    files, changed, sk, sd = [], 0, 0, 0
    for dp, dns, fns in __import__("os").walk(OUT):
        rel0 = Path(dp).relative_to(OUT).parts
        if rel0 and rel0[0] == "_archive":
            continue
        for fn in sorted(fns):
            if fn.endswith(".docx") and not fn.startswith("~$"):
                files.append(Path(dp) / fn)

    for p in files:
        z = zipfile.ZipFile(p)
        info = z.infolist()
        data = {i.filename: z.read(i.filename) for i in info}
        z.close()
        if "word/styles.xml" not in data or "word/document.xml" not in data:
            continue
        st = data["word/styles.xml"].decode("utf-8")
        dc = data["word/document.xml"].decode("utf-8")
        st2, n1 = patch_styles(st)
        dc2, n2 = patch_document(dc)
        if n1 == 0 and n2 == 0:
            continue
        changed += 1
        sk += n1
        sd += n2
        if apply:
            shutil.copy2(p, BAK / (p.stem + ".docx"))
            data["word/styles.xml"] = st2.encode("utf-8")
            data["word/document.xml"] = dc2.encode("utf-8")
            with zipfile.ZipFile(p, "w", zipfile.ZIP_DEFLATED) as w:
                for i in info:
                    w.writestr(i, data[i.filename])

    print("活跃产物 docx：%d 份" % len(files))
    print("需改动：%d 份（样式改 %d 处，SourceCode 段落改 %d 个）" % (changed, sk, sd))
    if not apply:
        print("\n[dry-run] 未落盘。加 --apply 执行（改前自动备份到 %s）。" % BAK)
    else:
        print("\n[applied] 完成，备份在 %s" % BAK)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
