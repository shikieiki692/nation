#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rescue_ovf2.py —— 救「越界」卡（v2：块删除，支持交错/粗体/表格）。

与闸门判据一致：
  越界标记 = 行首 `#{0,4}**N-M`（N>own） | `第N题`（N>own 且非引用） | 表格全跨度单元格内 `N-M`
  本卡标记 = 行首 `#{0,4}**own-M` | `第own题`
策略：删 [首个越界标记, 其后首个本卡标记) —— 越过界在尾部时即等价于截断。
"""
import csv, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
sys.path.insert(0, os.path.join(R, ".workbuddy/tmp/opt_pipe"))
_orig = list(sys.argv)
sys.argv = ["x", "--vol", "RO2", "--all-years"]
import build_org as BO

LIM = int(_orig[_orig.index("--limit") + 1]) if "--limit" in _orig else 999
apply = "--apply" in _orig
ONLY = [a for a in _orig[1:] if not a.startswith("--") and a != str(LIM)]
BK = os.path.join(R, ".workbuddy/tmp/opt_pipe/ovf2_backup")
os.makedirs(BK, exist_ok=True)

CITE_BEFORE = re.compile(r'参考|参见|对应|来源|引自|选自|出自|详见|考试|试题|试卷|组卷|见')

def own_marker_re(own):
    return re.compile(r'(?m)^[ \t]*(?:#{1,4}[ \t]*)?\*{0,2}[ \t]*%d\s*[-－]\s*\d{1,2}(?![0-9])' % own)

def ovf_markers(a, own):
    """返回 [(pos, token, kind)]，按位置升序。"""
    out = []
    # ① 行首小问组 N-M
    for m in re.finditer(r'(?m)^[ \t]*(?:#{1,4}[ \t]*)?\*{0,2}[ \t]*(\d{1,2})\s*[-－]\s*\d{1,2}(?![0-9])', a):
        if int(m.group(1)) > own:
            out.append((m.start(), m.group(0).strip(), 'subq'))
    # ② 第N题（非引用）
    for m in re.finditer(r'第\s*(\d{1,2})\s*题', a):
        n = int(m.group(1))
        if n > own:
            pre = a[max(0, m.start() - 16):m.start()]
            if CITE_BEFORE.search(pre):
                continue
            out.append((m.start(), m.group(0), 'qno'))
    # ③ 表格全跨度单元格内 N-M（删除范围为「含该单元格的 <tr> 起 → </table>」）
    for m in re.finditer(r'<td[^>]*colspan\s*=\s*"\d+"[^>]*>\s*(\d{1,2})\s*[-－]\s*\d{1,2}', a):
        if int(m.group(1)) > own:
            tr = a.rfind('<tr', 0, m.start())
            out.append((tr if tr >= 0 else m.start(), re.sub(r'<[^>]+>', '', a[m.start():m.start()+46]), 'table'))
    out.sort()
    return out

rows = [r for r in csv.DictReader(open(os.path.join(R, "09-审计报告/2026-10-07-不可组卷题目清单.csv"), encoding="utf-8-sig"))
        if r["reason"] == "越界（含他题内容）"]
if ONLY:
    rows = [r for r in rows if any(o in os.path.basename(r["path"]) for o in ONLY)]
print("越界卡 %d 张（处理 %d）\n" % (len(rows), min(LIM, len(rows))))

n = 0
for r in rows:
    if n >= LIM:
        break
    p = os.path.join(R, r["path"])
    t = open(p, encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")
    i = t.find("## 题目"); j = t.find("## 参考答案"); k = t.find("## 知识点映射")
    if not (0 <= i < j < k):
        print("  结构异常", os.path.basename(p)[:44]); continue
    own = BO.own_qno(t, p)
    if not own:
        print("  跳过（无题号）", os.path.basename(p)[:44]); continue
    araw = t[j + len("## 参考答案"):k]
    mk = ovf_markers(araw, own)
    if not mk:
        print("  ⚠ 无越界标记（可能为引用假阳性）:", os.path.basename(p)[:44]); continue
    start = mk[0][0]
    # 表格类：删到 </table>（不含闭合标签，保表结构）
    if mk[0][2] == 'table':
        te = araw.find('</table>', start)
        end = te if te >= 0 else len(araw)
    else:
        om = own_marker_re(own).search(araw, mk[0][0] + 1)
        end = om.start() if om else len(araw)
    keep = (araw[:start].rstrip() + "\n\n" + araw[end:].lstrip()).strip()
    # 剔除旧校勘注（避免双注）
    keep = re.sub(r'\n*>? ?⛔ 校勘（2026-10-07）：[^\n]*\n?', '\n', keep).strip()
    drop = araw[start:end].strip()
    print("═" * 92)
    print("%s | own=%d | 标记=%r(%s) | 答案 %d → 删 %d 字 留 %d 字" %
          (os.path.basename(p)[:48], own, mk[0][1][:24], mk[0][2], len(araw), len(drop), len(keep)))
    print("   删段首 90: …%s…" % re.sub(r"\s+", " ", drop[:90]))
    print("   删段尾 70: …%s…" % re.sub(r"\s+", " ", drop[-70:]))
    print("   接缝: …%s…|…%s…" % (re.sub(r"\s+", " ", araw[max(0, start - 55):start]), re.sub(r"\s+", " ", araw[end:end + 55])))
    if apply:
        bfp = os.path.join(BK, os.path.basename(p) + ".orig")
        if not os.path.exists(bfp):
            open(bfp, "w", encoding="utf-8", newline="\n").write(t)
        note = "\n\n> ⛔ 校勘（2026-10-07）：源卡答案区**混入了他题内容**（%d 字：%s），已按题界剔除；如需该题请查源卷。\n" % (len(drop), mk[0][1][:20])
        newt = t[:j + len("## 参考答案")] + "\n\n" + keep + note + t[k:]
        open(p, "w", encoding="utf-8", newline="\n").write(newt)
        print("   ✔ 已写入")
    n += 1
print("\n%s" % ("已写入" if apply else "（dry-run）"))
