# -*- coding: utf-8 -*-
r"""O3 卷级后处理补丁：修「判噪剔图后表格塌列」2 处（幂等）。

病根：layout_figs 并排图生成 3 列表头，而某组实际只有 2 张图（或组内 1 张被判噪剔除）
      ⇒ 数据行 2 格 vs 表头 3 列 ⇒ pipe_tbl_audit「行格数不符」。
处置：把这两张表的**表头与分隔行**同步为 2 列（内容零丢失：C/U 标签保留、两张图保留）。
⚠️ 只在卷 md 层修补（与 add_analysis／--titles 同层）；build_org --apply 重建会抹掉 ⇒ 已登记进
   vol_meta_O3.json 的 post_patches，由 build_volX_zhenti.py 自动重放（幂等：已是 2 列则跳过）。
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Obsidion\妙妙屋"
MDS = [
    os.path.join(ROOT, "04-题库", "初赛模拟卷O3（有机·答案版）.md"),
    os.path.join(ROOT, "04-题库", "初赛模拟卷O3（有机·学生版）.md"),
]

# (旧表头块, 新表头块) —— 以「表头+分隔行」为锚，避免误伤
FIXES = [
    ("| C | U |  |\n| :---: | :---: | :---: |",
     "| C | U |\n| :---: | :---: |"),
    ("|  |  |  |\n| :---: | :---: | :---: |\n| ![[fc4748f8ba6ccae494045a81dc3bd7420ff21940233b6e4e55d8b68dcadcf788.jpg\\|175]]",
     "|  |  |\n| :---: | :---: |\n| ![[fc4748f8ba6ccae494045a81dc3bd7420ff21940233b6e4e55d8b68dcadcf788.jpg\\|175]]"),
]

# ★ 标题卫生：源卡把「水印文字」与「答案区分值注」存成了 md 标题 ⇒ 在卷内造成「标题跳跃」
#   （validate_kb 报 #### 跳过 ## 级）。处置：水印整行删除；分值注**降级为粗体正文**（信息不丢）。
LINE_FIXES = [
    ("# 清北营教育\n\n", ""),                    # 水印文字（源卡 L82 即有）
    ("## 产物 3 分，过渡态 3 分", "**产物 3 分，过渡态 3 分**"),
    ("## (本小问共2分)", "**(本小问共2分)**"),
    ("## (本小问共6分)", "**(本小问共6分)**"),
]


def main():
    tot = 0
    for md in MDS:
        if not os.path.exists(md):
            print("  ⛔ 缺文件：%s" % md)
            return 1
        txt = io.open(md, encoding="utf-8-sig", newline="").read().replace("\r\n", "\n")
        n = 0
        for old, new in FIXES:
            if old in txt:
                txt = txt.replace(old, new, 1)
                n += 1
        for old, new in LINE_FIXES:
            if old in txt:
                txt = txt.replace(old, new)
                n += 1
        if n:
            io.open(md, "w", encoding="utf-8", newline="\n").write(txt)
        tot += n
        print("  %s：修补 %d 处" % (os.path.basename(md), n))
    print("o3_tblfix：合计修补 %d 处（幂等，已修则 0）" % tot)
    return 0


if __name__ == "__main__":
    sys.exit(main())
