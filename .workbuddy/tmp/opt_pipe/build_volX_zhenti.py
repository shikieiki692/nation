# -*- coding: utf-8 -*-
"""卷X → 真题版式 docx（复用 build_chusai_zhenti_layout.py 的全部排版手术）。

差异点：卷X 用机构题源，图片散在 04-题库/2026机构初赛模拟题/*/images/，
不在「媒体仓库」。做法：先建暂存媒体目录并把本卷引用的图复制进去，
再 monkey-patch 真题版式脚本的 MEDIA 常量为该暂存目录。

用法：python build_volX_zhenti.py [--answer|--student]   默认两种都出。
"""
import glob
import io
import os
import re
import shutil
import sys
from pathlib import Path

VAULT = Path(r"C:\Obsidion\妙妙屋")
QB = VAULT / "04-题库"
ORGBASE = QB / "2026机构初赛模拟题"
SCRIPTS = VAULT / ".workbuddy" / "scripts"
WORK = VAULT / ".workbuddy" / "tmp" / "volX_zhenti"
STAGE = WORK / "media"
for d in (WORK, STAGE):
    d.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(SCRIPTS))
# 注意：build_chusai_zhenti_layout 在 import 时会把 sys.stdout 换成一个 utf-8
# 包装器（基于当时的底层 buffer）。不要在这之前/之后自行重设 stdout，否则
# 旧包装器被 GC 时会连带关掉底层 buffer（ValueError: I/O operation on closed file）。
import build_chusai_zhenti_layout as Z   # noqa: E402

VOL = "X"
MEDIA_FILES = ["初赛模拟卷X（非有机·答案版）.md", "初赛模拟卷X（非有机·学生版）.md"]


def prepare_media():
    """把卷X 两版 md 里引用的所有图复制到 STAGE，返回 (引用总数, 缺图列表)。"""
    idx = {}
    for p in glob.glob(str(ORGBASE / "*" / "images" / "*")):
        idx.setdefault(os.path.basename(p), p)
    need, missing = set(), []
    for md in MEDIA_FILES:
        t = (QB / md).read_text(encoding="utf-8")
        for m in re.finditer(r"!\[\[([^\]\|\\]+?)(?:\\?\|\d+)?\]\]", t):
            need.add(m.group(1).strip())
    for name in need:
        src = idx.get(name)
        if src and os.path.exists(src):
            shutil.copyfile(src, STAGE / name)
        else:
            missing.append(name)
    return len(need), missing


def main():
    only_ans = "--answer" in sys.argv
    only_stu = "--student" in sys.argv
    n, missing = prepare_media()
    print("图准备：引用 %d 张，已铺 %d 张，缺 %d" % (n, len(os.listdir(STAGE)), len(missing)))
    for m in missing[:10]:
        print("   [缺图]", m)
    # ★ monkey-patch：真题版式脚本按 MEDIA 找图
    Z.MEDIA = STAGE
    # ★ 真题版式脚本的图正则不认 `![[hash.jpg\|250]]`（layout_figs 并排表格的转义形态），
    #   会整张漏掉 ⇒ 换成容忍转义竖线的版本（与 build_org_docx.resolve_images 一致）。
    _orig_resolve = Z.resolve_images

    def resolve_images2(body, log):
        def rep(m):
            name = m.group(1).strip()
            src = STAGE / name
            if not src.exists():
                log.append(f"   [缺图] {name}")
                return ""
            return f"![]({name})"
        return re.sub(r"!\[\[([^\]\|\\]+?)(?:\\?\|\d+)?\]\]", rep, body)

    Z.resolve_images = resolve_images2
    Z.TMP.mkdir(parents=True, exist_ok=True)
    ref = Z.build_reference()
    print("reference:", ref)

    if only_ans:
        eds = ["answer"]
    elif only_stu:
        eds = ["student"]
    else:
        eds = ["student", "answer"]
    done = []
    for ed in eds:
        t = Z.convert_one(VOL, ref, ed)
        if t:
            done.append(t)
    print("\n完成 %d 个：%s" % (len(done), Z.OUTDIR))
    return 0


if __name__ == "__main__":
    sys.exit(main())
