# -*- coding: utf-8 -*-
"""scan_img_labels.py —— 图内标签/水印残留「扩展扫描」（P2-11 遗留；**只读**）。

承 `scan_header_noise.py --img-adj`（只覆盖「图邻 ≤8 字符纯字母数字 token」），
本脚本扩面到三类此前未覆盖的形态：
  R3 图邻**中文**短行（2~10 汉字、无标点、非列表/标题）；
  R4 图邻**长英文**行（9~30 字符，仅 ASCII 字母/数字/空格/-/_/.，≥2 字母）；
  R5 图邻**孤立数字/单位/坐标**行（如 `450`、`100 nm`、`(0.33, 0.67, 0.25)`）。
判据：独占一行 + 行内无 Markdown 语法（# > - * ! | $ `）+ **±N 行内有图片引用**（并计 `![[ ]]`／`![]( )`／`<img src>`）。
⚠️ 只产**候选**——定性必须回源目检（上次实测：图邻 token 多数是**合法简写/图注**）。
用法：
  python scan_img_labels.py            # 各卷计划锁内的已交付卡
  python scan_img_labels.py --all      # 全库 4032 卡
  python scan_img_labels.py --near 3   # 图邻窗口（默认 2）
"""
import glob
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
BASE = os.path.join(R, "04-题库", "2026机构初赛模拟题")

IMG = re.compile(r"!\[\[|!\[\]\(|<img\b")
MD = set("#>-*!|$`[]{}")
PUNCT = set("。，；：、？！.,;:?!\"'“”‘’（）()《》〈〉—…~")


def classify(tok):
    if len(tok) > 10 or len(tok) < 2:
        return None
    if any(ch in MD for ch in tok) or any(ch in PUNCT for ch in tok):
        return None
    if re.fullmatch(r"[\u4e00-\u9fff]{2,10}", tok):            # R3 中文短行
        return "R3-中文"
    if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9 _\-/\.]{8,29}", tok) and len(re.findall(r"[A-Za-z]", tok)) >= 2:
        return "R4-长英文"                                      # R4 长英文
    if re.fullmatch(r"\d+(\.\d+)?|\d+(\.\d+)?\s*(nm|cm|mm|mL|mg|K|°C|GPa|eV|ppm|%)", tok):  # R5 数字/单位
        return "R5-数字"
    return None


def scan(p, near):
    t = open(p, encoding="utf-8-sig").read().replace("\r\n", "\n")
    lines = t.split("\n")
    img_idx = [i for i, l in enumerate(lines) if IMG.search(l)]
    hits = []
    for i, l in enumerate(lines):
        tok = l.strip().lstrip("*- ").strip()
        kind = classify(tok)
        if not kind:
            continue
        # 原始行必须是「独占行」（允许前缀 * - 作为裸列表）
        raw = l.strip()
        if raw != tok and not re.fullmatch(r"[*\-]\s+" + re.escape(tok), raw):
            continue
        j = [x for x in img_idx if abs(x - i) <= near]
        if not j:
            continue
        hits.append((i + 1, kind, tok, j[0] + 1))
    return hits


def main():
    near = 2
    if "--near" in sys.argv:
        near = int(sys.argv[sys.argv.index("--near") + 1])
    if "--all" in sys.argv:
        cards = sorted(glob.glob(os.path.join(BASE, "*", "题-*.md")))
        scope = "全库 %d 张" % len(cards)
    else:
        cards, seen = [], set()
        for f in sorted(glob.glob(os.path.join(R, ".workbuddy/tmp/opt_pipe", "vol_plan_*.json"))):
            try:
                d = json.load(open(f, encoding="utf-8"))
            except Exception:
                continue
            for _m, lst in d:
                for c in lst:
                    q = os.path.join(R, c["path"].replace("/", os.sep))
                    if q not in seen and os.path.exists(q):
                        seen.add(q)
                        cards.append(q)
        scope = "各卷计划锁内 %d 张" % len(cards)
    print("扫描范围：%s ｜ 图邻窗口 ±%d 行\n" % (scope, near))
    tot, by_kind, per = 0, {}, []
    for p in cards:
        hits = scan(p, near)
        if hits:
            per.append((p, hits))
            tot += len(hits)
            for _l, k, _t, _i in hits:
                by_kind[k] = by_kind.get(k, 0) + 1
    for p, hits in per:
        print("▸ [%s] %s" % (os.path.basename(os.path.dirname(p)), os.path.basename(p)[:44]))
        for ln, k, tok, imln in hits:
            print("    L%-5d %-8s 「%-22s」 邻图 L%d" % (ln, k, tok[:22], imln))
    print("\n合计候选 %d 处（%d 张卡）｜ 分类：%s" % (tot, len(per), by_kind))
    print("⚠️ 只筛候选：图邻 token 多数是合法简写/图注，定性必须回源目检（详见 SOP §五-b 缺陷 13）。")


if __name__ == "__main__":
    sys.exit(main())
