# -*- coding: utf-8 -*-
r"""脚踏实地复评（只读）：21 卷六维段计数 / 小问数 / docx 存在性 / 抽查 docx 是否含六维。"""
import io, os, re, glob, sys
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
os.chdir(R)

VOL_ORDER = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX",
             "X", "XI", "XIp", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "O1", "O2", "O3"]
tot = {"考点": 0, "易错": 0, "举一反三": 0, "溯源": 0, "落位": 0}
rows = []
for v in VOL_ORDER:
    p = os.path.join(R, "04-题库", "初赛模拟卷%s（非有机·答案版）.md" % v)
    if not os.path.exists(p):
        p = os.path.join(R, "04-题库", "初赛模拟卷%s（有机·答案版）.md" % v)
    if not os.path.exists(p):
        rows.append((v, "缺文件", "", "", "", "", "")); continue
    t = io.open(p, encoding="utf-8-sig").read().replace("\r\n", "\n")
    # 四维为「行首 > **考点**」式解析块标签；「落位」写在步骤正文内，须全文计数（勿用行首正则）
    c = {k: len(re.findall(r"^> \*\*%s\*\*" % k, t, re.M)) for k in tot if k != "落位"}
    # 两种合法写法：有答案图→「答案图落位」；零图卷（判据 43）→「答案标注落位」
    c["落位"] = t.count("答案图落位") + t.count("答案标注落位")
    for k in tot:
        tot[k] += c[k]
    # 小问数：解析块内 "> **N-x**" 标签
    sub = len(re.findall(r"^> \*\*[0-9A-Za-z\-]+(?:-[0-9A-Za-z]+)*\*\*", t, re.M))
    rows.append((v, os.path.basename(p)[:28], c["考点"], c["易错"], c["举一反三"], c["溯源"], c["落位"]))

for r in rows:
    print("%-5s %-30s 考点=%-4s 易错=%-4s 举反=%-4s 溯源=%-4s 落位=%s" % r)
print("-" * 100)
print("合计：考点 %d｜易错 %d｜举一反三 %d｜溯源 %d｜落位 %d" %
      (tot["考点"], tot["易错"], tot["举一反三"], tot["溯源"], tot["落位"]))

# docx 存在性（文件层面）
d = os.path.join(R, "00-首页", "题组Word", "初赛模拟卷", "真题版式")
fs = sorted(os.listdir(d))
print("\ndocx 目录文件数：%d" % len(fs))
miss = [v for v in VOL_ORDER if not any(f.startswith("初赛模拟卷%s（" % v) for f in fs)]
print("缺三件套的卷：", miss if miss else "无")
cnt = {}
for v in VOL_ORDER:
    cnt[v] = len([f for f in fs if f.startswith("初赛模拟卷%s（" % v)])
print("各卷 docx 数：", cnt)

# 抽查：三卷答案与解析版 docx 是否含「考点」「溯源」字样
try:
    import docx  # python-docx（PYV 环境）
except Exception as e:
    print("\n[跳过 docx 抽查] python-docx 不可用:", e)
    raise SystemExit
for v in ["VII", "VIII", "IX"]:
    fp = os.path.join(d, "初赛模拟卷%s（非有机·答案与解析版·真题版式）.docx" % v)
    if not os.path.exists(fp):
        print(v, "docx 缺失"); continue
    doc = docx.Document(fp)
    txt = "\n".join(p.text for p in doc.paragraphs)
    print("%s docx：段落 %d｜含『考点』%d｜含『溯源』%d｜含『答案图落位』%d｜含『举一反三』%d" %
          (v, len(doc.paragraphs), txt.count("考点"), txt.count("溯源"),
           txt.count("答案图落位"), txt.count("举一反三")))
