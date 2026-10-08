# -*- coding: utf-8 -*-
"""restructure_ans_XIII.py —— 卷 XIII **答案版 md** 的「答案区结构优化」后处理（幂等 · 可复核）。

⚠️ 只动**卷 md**（产物），**不碰源卡**（保持 `fidelity: 原书逐字`）。

问题（owner 反馈「答案的结构…要仔细」）：
  · 答案区**重复抄了一遍题面**（如 `6-3 现以 $1 mol CH_4$ …`），成品卷里冗余；
  · 答案区小问编号是**源卡题号**（第 1 题写 6-x、第 9 题写 6-x），与卷内不符；
  · 答案区**无小问标签**，多条答案连成一片，难对应题面。

处理（每题）：
  1. 以 `N-x` 开头且与题面对应小问相似度 ≥0.70 的行 ⇒ 替换为 **`**卷内N-x**`**（去冗余、加结构）；
  2. 其余以 `源前缀-x` 开头的行 ⇒ 编号前缀改为卷内题号；
  3. 其余不动。

用法：python restructure_ans_XIII.py --dry | --apply   （在 build_org 之后、出 docx 之前跑）
"""
import difflib, io, os, re, shutil, sys

sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
MD = os.path.join(R, "04-题库", "初赛模拟卷XIII（非有机·答案版）.md")
BAK = os.path.join(R, ".workbuddy/tmp/opt_pipe/xiii_ans_bak")
DRY = "--dry" in sys.argv

CLEAN = re.compile(r"\$[^$\n]*\$|\\[a-zA-Z]+|\s+|[\[\]{}()（）,，。.、；;:：'\"`*_^~|<>/\\-]")


def norm(s):
    return CLEAN.sub("", s)


txt = io.open(MD, encoding="utf-8-sig").read().replace("\r\n", "\n")
blocks = list(re.finditer(r"(?m)^### 第 (\d+) 题[^\n]*\n", txt))
if not blocks:
    print("未找到题块"); sys.exit(1)

out, stats = [], 0
prev_end = 0
for k, b in enumerate(blocks):
    volno = int(b.group(1))
    s = b.end()
    e = blocks[k + 1].start() if k + 1 < len(blocks) else len(txt)
    body = txt[s:e]
    am = re.search(r"(?m)^#### 答案\s*\n(.*?)(?=^> \*\*解析|^---\s*$|\Z)", body, re.S)
    if not am:
        continue
    qpart, apart = body[:am.start()], am.group(1)
    # 题面小问文本
    qsub = {}
    for m in re.finditer(r"(?m)^\s*(\d+-\d+(?:-\d+)*)\s*[．.、]?\s*(.{6,140})$", qpart):
        qsub[m.group(1)] = norm(m.group(2))
    rows = list(re.finditer(r"(?m)^\s*(\d+)-(\d+(?:-\d+)*)\s*([^\n]*)$", apart))
    if not rows:
        out.append(txt[prev_end:e]); prev_end = e; continue
    srcpre = rows[0].group(1)
    new_ap, n_rep = apart, 0
    for m in reversed(rows):
        rest, tail = m.group(2), m.group(3)
        old_num, new_num = "%s-%s" % (srcpre, rest), "%d-%s" % (volno, rest)
        cand = [qsub[x] for x in (old_num, new_num) if x in qsub] or list(qsub.values())
        tn = norm(tail)
        sim = max((difflib.SequenceMatcher(None, tn, c).ratio() for c in cand), default=0)
        if tn and sim >= 0.70:
            rep, n_rep = "**%s**" % new_num, n_rep + 1
        else:
            rep = new_num + tail
        new_ap = new_ap[:m.start()] + rep + new_ap[m.end():]
    if new_ap != apart:
        stats += n_rep
        # 以 group(1) 的边界重建（保留 `#### 答案` 与后随空白原样）
        body = body[:am.start(1)] + new_ap + body[am.end(1):]
    out.append(txt[prev_end:s]); out.append(body); prev_end = e
out.append(txt[prev_end:])
txt2 = "".join(out)
if txt2 == txt:
    print("(dry) 无变化" if DRY else "无变化")
    sys.exit(0)
if not DRY:
    os.makedirs(BAK, exist_ok=True)
    shutil.copy2(MD, os.path.join(BAK, os.path.basename(MD)))
    io.open(MD, "w", encoding="utf-8", newline="\n").write(txt2)
print("%s：重述转标签 %d 处；文件 %d→%d 字" % ("(dry)" if DRY else "已写盘", stats, len(txt), len(txt2)))
