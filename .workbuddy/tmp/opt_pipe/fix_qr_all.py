# -*- coding: utf-8 -*-
"""fix_qr_all.py —— 删除源卡的页眉二维码噪点图（目检确认的 53 张）。
排除清单＝目检确认的 14 张正常题目图（照片/分子模型/晶体图）。
"""
import json, os, re, sys
R = r"C:\Obsidion\妙妙屋"
sys.stdout.reconfigure(encoding="utf-8")
BK = os.path.join(R, ".workbuddy/tmp/opt_pipe/qr_backup")
os.makedirs(BK, exist_ok=True)
apply = "--apply" in sys.argv

sel = json.load(open(os.path.join(R, ".workbuddy/tmp/opt_pipe/qr_sel.json"), encoding="utf-8"))
EX = {"1c24460c", "5664b432", "7499a1c1", "25153726", "c24d1d74", "da22b014", "ecdf6489",
      "210982ec", "1e9bc2ee", "276f6094", "aed1cdc3", "cd61927b", "29d6296e", "9f31937b"}

qr = {}
for r, fp in sel:
    base = os.path.basename(fp)
    if base[:8] in EX:
        continue
    qr[base] = round(r, 3)
print("待删二维码图 %d 张（已排除目检确认的正常图 %d 张）" % (len(qr), len(sel) - len(qr)))

D = os.path.join(R, "04-题库/2026机构初赛模拟题")
cards = []
for p in sorted(__import__("glob").glob(D + "/**/题-*.md", recursive=True)):
    t = open(p, encoding="utf-8-sig", errors="replace").read()
    hit = [n for n in qr if n in t]
    if hit:
        cards.append((p, hit))
print("涉及卡 %d 张，共 %d 处引用" % (len(cards), sum(len(h) for _, h in cards)))

tot = 0
for p, hit in cards:
    t = open(p, encoding="utf-8-sig").read().replace("\r\n", "\n")
    orig = t
    n = 0
    for h in hit:
        # ① 表格单元格 ⇒ 置空（保结构）
        t, c1 = re.subn(r'<td>\s*<img src="images/%s"\s*/>\s*</td>' % re.escape(h), "<td></td>", t)
        # ② 独立/行内图片
        t, c2 = re.subn(r'[ \t]*!\[\]\(images/%s\)[ \t]*\n?' % re.escape(h), "", t)
        t, c3 = re.subn(r'\s*!\[\]\(images/%s\)\s*' % re.escape(h), " ", t)
        n += c1 + c2 + c3
    if n == 0:
        print("  ! 未匹配到引用：", os.path.basename(p)[:46]); continue
    t = re.sub(r"\n{3,}", "\n\n", t)
    if apply:
        bfp = os.path.join(BK, os.path.basename(p) + ".orig")
        if not os.path.exists(bfp):
            open(bfp, "w", encoding="utf-8", newline="\n").write(orig)
        open(p, "w", encoding="utf-8", newline="\n").write(t)
    tot += n
    print("  %-50s 删 %d 处" % (os.path.basename(p)[:50], n))
print("\n合计删除 %d 处" % tot, "（dry-run）" if not apply else "（已写入）")
