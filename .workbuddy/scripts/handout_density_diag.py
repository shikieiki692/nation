"""讲义「信息密度」诊断（**当前可用口径**）：按句子职能分层 + 篇幅/判据密度。

⚠️ 前 5 版判据全部失效，**勿用「符号数量」重做**：
  v1/v2 符号密度：用文字准确表述的判据本身无符号 ⇒ 必误伤（实测把「ρ=+1.8 推断过渡态」
        这类优质判据判成"低信息"）。
  v5 首版词表把「应」单列 ⇒ 命中「反应/效应/响应」等化学高频词，判据密度虚高到 644/千字。
⇒ 本脚本 RE_J 已限定为「应当/应该/应用」等完整词形；输出 J/E/T/M/N 五类占比 + 判据密度榜。

复跑前置（无外部依赖，只读 04-课件/学生讲义）：
    python -X utf8 .workbuddy/scripts/handout_density_diag.py
"""
"""信息密度 v5 原始说明：

v1-v3 的失败：用「符号数量」判密度 ⇒ 用文字准确表述的判据（如「正离子使负离子电子云
变形」）被判为无信息，而带一个 HCl 的废话句反而过关。**判据本身无效，已弃用。**

v4 改按**句子职能**：
  J 判据句：给出可执行规则/条件/边界/正误（必须·应当·一律·判据·当…时·若…则·优先·禁止·上限·否则·才可·只能）
  E 解释句：说明成因/理由（因为·由于·原因是·之所以·本质上是·意味着·来自·源于）
  M 元信息句：讲编排与定位（本节定位·选题口径·深度边界·建议使用方式·配图规划·版本说明）
  N 叙述句：其余（描述现象/学生状态/一般陈述）
竞赛讲义的期望配比：J 高、E 中、M≈0、N 低。
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

V = Path(r"C:\Obsidion\妙妙屋")
ROOT = V / "04-课件/学生讲义"
OUT = V / ".workbuddy/tmp/img_audit"
sys.path.insert(0, str(V / ".workbuddy/tmp"))
from diag_density2 import blocks, LINE_CJK  # noqa: E402
from diag_density4 import split_layers  # noqa: E402

# ⚠️ 首版把「应」单列 ⇒ 命中「反*应*」「效*应*」「响*应*」等化学高频词，
#    判据密度虚高到 644/千字（J 64%）⇒ 必须限定为「应当/应该/应用来」等完整词形。
RE_J = re.compile(r"必须|应当|应(?:该|用)|一律|判据|规则是|准则|只能|才可|否则|优先(?:选|考虑|占)|"
                  r"禁止|上限|下限|取值|适用范围|判(?:断|定)(?:标准|依据|顺序)|不允许|不得|"
                  r"一律不|当[^。；\n]{1,25}时|若[^。；\n]{1,20}(?:则|，)|其一|其二是|第[一二三四五]步")
RE_E = re.compile(r"因为|由于|原因是|之所以|本质上是|意味着|来源于|源于|来自|正是|"
                  r"这是(?:因为|由于)|解释了|反映出|归因于")
RE_M = re.compile(r"本节定位|本章定位|选题口径|深度边界|建议使用方式|配图规划|配图说明|"
                  r"版本说明|上节衔接|下节衔接|本讲定位|教材覆盖口径|课堂主讲主线|主框架教材|辅助教材|"
                  r"本版为|已被本页取代|本讲(?:的)?(?:典型)?例题(?:已)?(?:分别)?放在")
RE_N_TELL = re.compile(r"学生常见|很多学生|初学者|你会|你会发现|很多人|大部分人|往往(?:会)?(?:以为|觉得)|"
                       r"容易(?:误)?以为|直觉(?:上)?(?:会)?认为")


def sentences(text: str):
    t = re.sub(r"\$[^$\n]*\$", " ", text)          # 去行内公式，避免 $ 内句读干扰
    parts = re.split(r"(?<=[。！？；])\s*", t)
    return [x.strip() for x in parts if len(LINE_CJK.findall(x)) >= 6]


def main():
    rows = []
    files = sorted(p for p in ROOT.rglob("*.md")
                   if "_归档" not in p.parts and not p.name.startswith("README"))
    for p in files:
        L = split_layers(p.read_text(encoding="utf-8", errors="replace"))
        c = Counter()
        ex = {"J": [], "E": [], "M": [], "T": []}
        for para in L["l3"]:
            for s in sentences(para):
                n = len(LINE_CJK.findall(s))
                if RE_M.search(s):
                    c["M"] += n; ex["M"].append(s)
                elif RE_J.search(s):
                    c["J"] += n
                elif RE_E.search(s):
                    c["E"] += n; ex["E"].append(s)
                elif RE_N_TELL.search(s):
                    c["T"] += n; ex["T"].append(s)
                else:
                    c["N"] += n
        tot = sum(c.values()) or 1
        rows.append(dict(file=str(p.relative_to(V)), tot=tot,
                         **{k: c[k] for k in "JEMNTN" if k in c},
                         J_pct=round(c["J"] / tot * 100, 1), E_pct=round(c["E"] / tot * 100, 1),
                         M_pct=round(c["M"] / tot * 100, 1), T_pct=round(c["T"] / tot * 100, 1),
                         N_pct=round(c["N"] / tot * 100, 1),
                         j_per_k=round(c["J"] / tot * 1000, 1),
                         ex_M=ex["M"][:2], ex_T=ex["T"][:2], ex_E=ex["E"][:2]))
    (OUT / "density_v4.json").write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")

    T = sum(r["tot"] for r in rows)
    def s(k):
        return sum(r.get(k, 0) for r in rows)
    print(f"现役 {len(rows)} 份 · 正文汉字（L3，句级归集） {T:,}\n")
    print("=== 按职能分层（占正文汉字）===")
    print(f"  J 判据句（可执行规则/条件/边界）: {s('J'):>7,}  {s('J')/T*100:5.1f}%")
    print(f"  E 解释句（成因/理由）            : {s('E'):>7,}  {s('E')/T*100:5.1f}%")
    print(f"  T 教学法叙述（'学生往往以为…'）  : {s('T'):>7,}  {s('T')/T*100:5.1f}%")
    print(f"  M 元信息（定位/口径/版本）       : {s('M'):>7,}  {s('M')/T*100:5.1f}%")
    print(f"  N 其余叙述                       : {s('N'):>7,}  {s('N')/T*100:5.1f}%")

    print(f"\n=== 判据密度 bottom 15（每千字判据句最少 ⇒ 最像'读物'而非'规则表'）===")
    for r in sorted(rows, key=lambda x: x["j_per_k"])[:15]:
        print(f"  判据{r['j_per_k']:>5.1f}/千字  J{r['J_pct']:>5.1f}% E{r['E_pct']:>5.1f}% "
              f"T{r['T_pct']:>4.1f}% M{r['M_pct']:>4.1f}%  {r['tot']:>6,}字  {r['file'].split('/')[-1][:40]}")

    print(f"\n=== 教学法叙述（T）占比 top 12 ===")
    for r in sorted(rows, key=lambda x: -x["T_pct"])[:12]:
        print(f"  T{r['T_pct']:>5.1f}%  J{r['J_pct']:>5.1f}%  {r['tot']:>6,}字  {r['file'].split('/')[-1][:42]}")
        for e in r["ex_T"][:2]:
            print(f"       · {e[:110]}")

    print(f"\n=== 判据密度 top 10（可以做参照的正例）===")
    for r in sorted(rows, key=lambda x: -x["j_per_k"])[:10]:
        print(f"  判据{r['j_per_k']:>5.1f}/千字  J{r['J_pct']:>5.1f}% E{r['E_pct']:>5.1f}%  {r['tot']:>6,}字  {r['file'].split('/')[-1][:40]}")

    print(f"\n=== 元信息（M）明细（应为 0）===")
    for r in sorted(rows, key=lambda x: -x["M_pct"])[:6]:
        if r["M_pct"] <= 0.3:
            continue
        print(f"  M{r['M_pct']:>5.1f}%  {r['file'].split('/')[-1][:40]}")
        for e in r["ex_M"][:1]:
            print(f"       · {e[:120]}")


if __name__ == "__main__":
    main()
