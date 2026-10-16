# -*- coding: utf-8 -*-
r"""o2_tbl_fix.py —— O2 答案版「HTML 表转 md 丢前导 `|`」修补（②-b）。

根因：源卡 GM-09-10 用 HTML `<table>`（含 `colspan=4` 标签行），`volpost --ans` 转 md 时
  把标签行与数据行**并成一行且丢前导 `|`** ⇒ pandoc 断表 ⇒ 该 4 图（7ba5/2894/66d7/46f3）落不了 docx
  ⇒ qa_volX2 报「图守恒 md=176 media=172」。
修法：按源表结构忠实重建为 4 列 md 表（标签行独立成行；`colspan=2` 以空单元格表达）。
护栏：整段精确匹配（含 \n）＋ count==1 ＋ 备份 ＋ 逆向逐字节自证 ＋ EOL 守恒。
"""
import os
import shutil
import sys

ROOT = r"C:/Obsidion/妙妙屋"
F = "04-题库/初赛模拟卷O2（有机·答案版）.md"
BAK = os.path.join(ROOT, ".workbuddy", "tmp", "opt_pipe", "_bak_o2_tbl")

H = {
    "674c": "674c71c41b271f426e59bb530792b53b030a8abfe3a371342637a98d6476df04.jpg",
    "b0c1": "b0c15cf3255078873f0b76214162d87f910b4d763b02cad4b1d7f5f766d3eabb.jpg",
    "7ba5": "7ba55bf1db4fb093efed9f3c5a02957eabb8523e1db2342c9d69d07415c58ab8.jpg",
    "2894": "2894ff33d916eb264fbd4683a863fe21ee06f6f6fb89cee12be69f9e8f60a806.jpg",
    "aceb": "aceb8ca49a5e771cb0fc93d9463d6ee8e2c2d9fa410fbedbdd6ca090c71c6ff8.jpg",
    "66d7": "66d72c3531ceb2b00af3ef5d5cbd1373b6680c23ecc838f5b3d6140400fd1bd7.jpg",
    "46f3": "46f3da733afcee5f61be7fc050a1fd23d1e8ecadb665ce6b503c5b867b6081e4.jpg",
}

OLD = "\n".join([
    "9-2-1 | E | F | G | H |",
    "|:--:|:--:|:--:|:--:|",
    "| ![[%s]] (2分) | ![[%s]] (2分) | ![[%s]] (2分) | ![[%s]] (3分) |" % (H["674c"], H["b0c1"], H["7ba5"], H["2894"]),
    "9-2-2 | ![[%s]] (3分) | ![[%s]] (1分) | ![[%s]] (1分) |" % (H["aceb"], H["66d7"], H["46f3"]),
    "|:--:|:--:|:--:|",
    "9-2-3 9-3",
])
NEW = "\n".join([
    "| 9-2-1 |  |  |  |",
    "|:--:|:--:|:--:|:--:|",
    "| E | F | G | H |",
    "| ![[%s]] (2分) | ![[%s]] (2分) | ![[%s]] (2分) | ![[%s]] (3分) |" % (H["674c"], H["b0c1"], H["7ba5"], H["2894"]),
    "| 9-2-2 |  |  |  |",
    "| ![[%s]] (3分) | ![[%s]] (1分) |  | ![[%s]] (1分) |" % (H["aceb"], H["66d7"], H["46f3"]),
    "| 9-2-3 |  |  |  |",
    "| 9-3 |  |  |  |",
])


def main():
    p = os.path.join(ROOT, F)
    os.makedirs(BAK, exist_ok=True)
    shutil.copy2(p, os.path.join(BAK, os.path.basename(p)))
    body = open(p, encoding="utf-8-sig", newline="").read()
    n = body.count(OLD)
    if n != 1:
        print("  [SKIP] 整段匹配 n=%d（预期 1）" % n)
        return 1
    out = body.replace(OLD, NEW)
    assert out.replace(NEW, OLD) == body, "逆向自证失败"
    open(p, "w", encoding="utf-8", newline="").write(out)
    print("  [OK] %s  +%d 字符（逆向自证 ✅）" % (F, len(out) - len(body)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
