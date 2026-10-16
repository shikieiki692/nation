# -*- coding: utf-8 -*-
r"""登记 A3 的卷 md 层修补进 vol_meta_<卷>.json::md_patches（SOP §五-i⑦）。"""
import io
import json
import os
import sys

O = r"C:/Obsidion/妙妙屋/.workbuddy/tmp/opt_pipe"

ADD = {
    "X": {
        "script": "fix_fig3.py",
        "why": "④-e 真缺陷修复：答案 6-2-2「$L_{Ph}$ 可能有以下两种结构」后**补回丢失图** "
               "`![[b820c9b2…]]`（源卡 QBY-11-06 该处为 HTML `<img src=images/b820c9b2…>`，"
               "旧版建卷器表内/段内 HTML 图未落卷 ⇒ `git log -S` 证构建期即丢）。"
               "⚠️ 该图源件带「清北营」灰字水印 ⇒ 已用 `xv_dewm` 口径**去水印后原地替换**"
               "（备份 `.workbuddy/tmp/dewm/b820c9b2.orig.jpg`；图在 `04-题库/**/images/` 属 gitignore，不入库）。",
        "apply": "python .workbuddy/tmp/opt_pipe/fix_fig3.py",
        "added": "2026-10-16",
    },
    "XI": {
        "script": "fix_fig3.py",
        "why": "④-e 真缺陷修复：第 10 题 10-1「方向」表**首列 2 个空单元格**补回坐标轴图标 "
               "`![[143ca87a…]]`（b/a）与 `![[7e7ab009…]]`（c/b）（源卡 CM-12-07 HTML 表首列图未落卷）。"
               "**学生版与答案版同改**（该表在题面区，两版须一致）。两图标**无任何水印**（目检）。",
        "apply": "python .workbuddy/tmp/opt_pipe/fix_fig3.py",
        "added": "2026-10-16",
    },
    "XIp": {
        "script": "fix_fig3.py",
        "why": "④-e 真缺陷修复：答案 7-1 行 **`| 7-1 | |` 空单元格**补回分子玫瑰花结结构图 "
               "`![[490596bc…]]`（源卡 QBY-10-04 该处为 HTML `<td><img src=images/490596bc…>`）。"
               "⚠️ 源件带「清北营」灰字水印 ⇒ 已 `xv_dewm` 去水印后原地替换"
               "（备份 `.workbuddy/tmp/dewm/490596bc.orig.jpg`）。",
        "apply": "python .workbuddy/tmp/opt_pipe/fix_fig3.py",
        "added": "2026-10-16",
    },
}


def main():
    for vol, entry in ADD.items():
        p = os.path.join(O, "vol_meta_%s.json" % vol)
        if not os.path.isfile(p):
            print("  [MISS] vol_meta_%s.json" % vol)
            continue
        d = json.load(io.open(p, encoding="utf-8"))
        mp = d.setdefault("md_patches", [])
        if any(x.get("script") == "fix_fig3.py" for x in mp):
            print("  [EXISTS] %s" % vol)
            continue
        mp.append(entry)
        with io.open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(d, ensure_ascii=False, indent=1))
        print("  [OK] %s  md_patches=%d" % (vol, len(mp)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
