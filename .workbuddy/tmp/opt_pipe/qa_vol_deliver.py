# -*- coding: utf-8 -*-
"""qa_vol_deliver.py —— 交付件「综合审计」（补 qa_volX2 的盲区）。

qa_volX2 已覆盖：图守恒(md↔docx)、题标题数、字面 <table>、字面 $、题面泄露、
表体全空行、清单行列、学生版无答案区。**本脚本补以下盲区**：

  A 卡↔学生版「题面图」逐一比对 → 抓 **丢图** 与 **S1（题面图落在答案区）**
  B 交付 docx **空基底**（`<m:sSub><m:e></m:e>` / `<m:sSup><m:e></m:e>`）必须 = 0
  C 卷 md **`$$` 必须独占一行**（铁律二）
  D 卷 md **表格 ragged**（同一表内列数不一致）
  E 卷 md **常见 OCR 错字**（curated 词表）
  F 学生版 **「图指代词存在但该题无图」**（S1 卷级判据）
  G 学生版图集合 ⊆ 答案版图集合

用法：python -X utf8 qa_vol_deliver.py [--vol XIV] [--all]
"""
import io
import json
import os
import re
import sys
import zipfile

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Obsidion\妙妙屋"
QB = os.path.join(ROOT, "04-题库")
DESK = os.path.join(ROOT, "00-首页", "题组Word", "初赛模拟卷", "真题版式")
PLANDIR = os.path.join(ROOT, ".workbuddy", "tmp", "opt_pipe")

TITLE_RX = re.compile(r"^### 第 (\d+) 题（", re.M)
# 已逐张目检确认为「装饰性/坏裁图」⇒ 允许被剔除（不报）
try:
    REVIEWED = set(json.load(open(os.path.join(PLANDIR, "noise_reviewed.json"), encoding="utf-8")))
except Exception:
    REVIEWED = set()
IMG_EMBED = re.compile(r"!\[\[([^\]\|\\]+)")
IMG_MD = re.compile(r"!\[\]\(images/([^)\s]+)\)")
# 「图指代词」：题面提到图却没有图 ⇒ 候选 S1
FIG_REF = re.compile(r"(下图|右图|左图|上图|如下图|如图|见图|图\s*\d)")
# curated OCR 错字（同形/形近，来自回源核验累积）
TYPO = {
    "品胞": "晶胞", "品系": "晶系", "品体": "晶体", "中的中的": "中的",
    "设立方体": "设大立方体", "正前": "正确",
}


def vol_plan(v):
    p = os.path.join(PLANDIR, "vol_plan_%s.json" % v)
    if not os.path.exists(p):
        return None
    return json.load(open(p, encoding="utf-8"))


def card_front_imgs(path):
    """卡「题目」段的图文件名集合。"""
    t = io.open(os.path.join(ROOT, path), encoding="utf-8-sig").read()
    front = t.split("\n## 参考答案")[0]
    return set(IMG_MD.findall(front))


def card_ans_imgs(path):
    """卡「参考答案」段的图文件名集合（到 `## 知识点映射` 为止）。"""
    t = io.open(os.path.join(ROOT, path), encoding="utf-8-sig").read()
    if "\n## 参考答案" not in t:
        return set()
    seg = t.split("\n## 参考答案", 1)[1].split("\n## 知识点映射")[0]
    return set(IMG_MD.findall(seg))


def split_questions(md):
    """→ [(题号, 题面段)]（按 `### 第 N 题（` 切）"""
    idx = [m.start() for m in TITLE_RX.finditer(md)]
    idx.append(len(md))
    out = []
    for a, b in zip(idx, idx[1:]):
        seg = md[a:b]
        no = TITLE_RX.match(seg).group(1)
        out.append((int(no), seg))
    return out


def check_vol(v):
    print("=" * 78)
    print("卷 %s" % v)
    plan = vol_plan(v)
    cards = [c["path"] for _m, lst in plan for c in lst] if plan else []
    stu_p = os.path.join(QB, "初赛模拟卷%s（非有机·学生版）.md" % v)
    ans_p = os.path.join(QB, "初赛模拟卷%s（非有机·答案版）.md" % v)
    stu = io.open(stu_p, encoding="utf-8-sig").read()
    ans = io.open(ans_p, encoding="utf-8-sig").read()
    stu_q = split_questions(stu)
    ans_q = split_questions(ans)
    issues = []

    # A 卡题面图 ⊆ 学生版该题图
    for i, path in enumerate(cards):
        want = card_front_imgs(path)
        if i >= len(stu_q):
            issues.append(("A", "题 %d 缺学生版段落" % (i + 1)))
            continue
        got = set(IMG_EMBED.findall("".join(stu_q[i][1].split("#### 答案")[:1])))
        miss = {x for x in want if x not in got and x not in REVIEWED}
        if miss:
            issues.append(("A", "题 %d 卡题面图缺失 %d 张（例 %s）｜卡=%s 学生版=%s"
                           % (i + 1, len(miss), sorted(miss)[0][:16], sorted(want), sorted(got))))

    # B 空基底（答案版 docx）
    for tag, fn in (("学生版", "初赛模拟卷%s（非有机·学生版·真题版式）.docx" % v),
                    ("答案版", "初赛模拟卷%s（非有机·答案与解析版·真题版式）.docx" % v),
                    ("答题卡", "初赛模拟卷%s（非有机·答题卡）.docx" % v)):
        p = os.path.join(DESK, fn)
        if not os.path.exists(p):
            issues.append(("B", "%s docx 缺失" % tag))
            continue
        x = zipfile.ZipFile(p).read("word/document.xml").decode("utf-8")
        n = len(re.findall(r"<m:sSub><m:e></m:e>", x)) + len(re.findall(r"<m:sSup><m:e></m:e>", x))
        if n:
            issues.append(("B", "%s 空基底 %d" % (tag, n)))

    # H 卡答案区图 ⊆ 答案版该题图
    for i, path in enumerate(cards):
        want = card_ans_imgs(path)
        if not want or i >= len(ans_q):
            continue
        got = set(IMG_EMBED.findall(ans_q[i][1]))
        miss = {x for x in want if x not in got and x not in REVIEWED}
        if miss:
            issues.append(("H", "题 %d 卡答案图缺失 %d 张（例 %s）" % (i + 1, len(miss), sorted(miss)[0][:16])))

    # C `$$` 独占行（★ 只认**铁律二的真实失败模式**：行首非 `$` 且行尾为 `$$`）
    for tag, md in (("学生版", stu), ("答案版", ans)):
        bad = [(i + 1, l[:60]) for i, l in enumerate(md.split("\n"))
               if re.match(r"^[^$\n]", l) and re.search(r"\$\$[ \t]*$", l)]
        if bad:
            issues.append(("C", "%s `$$` 行尾粘连 %d（例 行%d: %s）" % (tag, len(bad), bad[0][0], bad[0][1])))

    # D 表格 ragged
    for tag, md in (("学生版", stu), ("答案版", ans)):
        tbl, n0, bad = [], 0, []
        for i, l in enumerate(md.split("\n") + [""]):
            s = l.strip()
            if s.startswith("|"):
                c = len(re.split(r"(?<!\\)\|", s.strip("|"))) - 1
                if not tbl:
                    n0, tbl = c, [i + 1]
                elif c != n0:
                    bad.append(i + 1)
            else:
                tbl = []
        if bad:
            issues.append(("D", "%s 表格 ragged %d 行（例 行%s）" % (tag, len(bad), bad[:3])))

    # E OCR 错字
    for tag, md in (("学生版", stu), ("答案版", ans)):
        hit = {k: md.count(k) for k in TYPO if k in md}
        if hit:
            issues.append(("E", "%s OCR 错字 %s" % (tag, hit)))

    # F 「题面提到图但无图」
    for no, seg in stu_q:
        body = seg.split("#### 答案")[0]
        if FIG_REF.search(body) and not IMG_EMBED.search(body):
            issues.append(("F", "题 %d 题面提图但 0 图" % no))

    # G 学生版图 ⊆ 答案版图
    ms, ma = set(IMG_EMBED.findall(stu)), set(IMG_EMBED.findall(ans))
    if ms - ma:
        issues.append(("G", "学生版有而答案版无的图 %d" % len(ms - ma)))

    for k, m in issues:
        print("  ✗ [%s] %s" % (k, m))
    if not issues:
        print("  ✓ 全部通过")
    return issues


def main():
    if "--all" in sys.argv:
        vols = ["X", "XIp", "XI", "XII", "XIII", "XIV", "XV"]
    elif "--vol" in sys.argv:
        vols = [sys.argv[sys.argv.index("--vol") + 1]]
    else:
        vols = ["XIV"]
    tot = {}
    for v in vols:
        for k, _ in check_vol(v):
            tot[k] = tot.get(k, 0) + 1
    print("=" * 78)
    print("汇总：", tot if tot else "全部通过")


if __name__ == "__main__":
    main()
