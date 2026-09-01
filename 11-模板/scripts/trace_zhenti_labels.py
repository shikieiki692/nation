# -*- coding: utf-8 -*-
"""
trace_zhenti_labels.py —— 习题集真题标注溯源补全
扫描 04-课件/习题集/第一轮化学原理-*习题集.md 中 [真题·第N届...] 标签，
用题面特征 token 在 04-题库/真题/第N届*/ 中匹配原题文件，
把标签补全为 [真题·第N届初赛/决赛·题号] 格式。
用法：python trace_zhenti_labels.py            # dry-run
      python trace_zhenti_labels.py --write   # 实写
"""
import io, os, re, sys, glob, argparse

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

VAULT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROOT = os.path.join(VAULT, "04-课件", "习题集")
ZT = os.path.join(VAULT, "04-题库", "真题")
FILES = [f for f in os.listdir(ROOT)
         if f.startswith("第一轮化学原理-") and f.endswith("习题集.md")]

STOP = {"mol", "kJ", "mmol", "atm", "kPa", "Pa", "min", "ml", "mL", "molL",
        "the", "and", "of"}
HEAD_RE = re.compile(r"^(#{2,3}) (第?[0-9]+题|题 ?[0-9]+)(.*)$")
LABEL_RE = re.compile(r"\[真题·第 ?(\d+) ?届(初赛|决赛|初赛第二场)?[^]]*\]")
NUM_RE = re.compile(r"\d+(?:\.\d+)?")
LAT_RE = re.compile(r"[A-Za-z][A-Za-z0-9]*")

def tokens(text):
    """特征 token：≥2位数字/带小数 + 非停用词拉丁词"""
    toks = set()
    for n in NUM_RE.findall(text):
        if "." in n or len(n.lstrip("0")) >= 2:
            toks.add("n" + n)
    for w in LAT_RE.findall(text):
        if len(w) >= 2 and w.lower() not in STOP:
            toks.add(w)
    return toks

def body_tokens(body):
    """只取题面（参考答案前），答案为习题集自撰不可作依据"""
    cut = re.split(r"\*\*参考答案\*\*|\*\*答案\*\*|\*\*解答\*\*", body)[0]
    return tokens(cut)

def corpus():
    """预载真题库各届文件 token"""
    out = []
    for p in glob.glob(os.path.join(ZT, "第*届*", "*", "*.md")):
        rel = os.path.relpath(p, ZT)
        m = re.match(r"第(\d+)届(初赛|决赛|初赛第二场)", rel)
        if not m:
            continue
        s = io.open(p, encoding="utf-8", errors="replace").read()
        out.append((rel, m.group(1), m.group(2), tokens(s), s))
    return out

def qnum_from_name(fn):
    """题-033-3-xxx.md -> 第3题；题-033-7-1-xxx.md -> 7-1；
    决赛式：题-027决-10~11-xxx -> 第10~11题；题-34决理-1-5-1-xxx -> 1-5-1"""
    m = re.match(r"题-(\d+)(?:决理|决|理)?-([\d]+(?:[-~][\d]+)*)-", fn)
    if not m:
        return None
    parts = m.group(2).split("-")
    if len(parts) > 1 or "~" in m.group(2):
        return m.group(2)
    return f"第{parts[0]}题"

def main(write=False):
    ZT_CORPUS = corpus()
    for fname in FILES:
        path = os.path.join(ROOT, fname)
        s = io.open(path, encoding="utf-8").read()
        lines = s.split("\n")
        # 切题块
        blocks = []  # (head_idx, head_text)
        for i, ln in enumerate(lines):
            m = HEAD_RE.match(ln)
            if m:
                blocks.append(i)
        blocks.append(len(lines))
        changed = 0
        for bi in range(len(blocks) - 1):
            hi = blocks[bi]
            hm = HEAD_RE.match(lines[hi])
            lm = LABEL_RE.search(hm.group(3))
            if not lm:
                continue
            year, stage = lm.group(1), lm.group(2)
            body = "\n".join(lines[hi + 1: blocks[bi + 1]])
            qt = body_tokens(body)
            if len(qt) < 4:
                print(f"? {fname}:{hi+1} {lines[hi][:40]} 特征token不足，跳过")
                continue
            best, bscore = None, 0.0
            for rel, y, st, ct, _cs in ZT_CORPUS:
                if y != year:
                    continue
                if stage and st != stage:
                    continue
                score = len(qt & ct) / len(qt)
                if score > bscore:
                    best, bscore = (rel, st), score
            if best and bscore >= 0.35:
                rel, st = best
                qn = qnum_from_name(os.path.basename(rel))
                if qn:
                    new_label = f"[真题·第{year}届{st}·{qn}]"
                    new_head = lines[hi].replace(lm.group(0), new_label)
                    flag = "W" if write else "D"
                    print(f"{flag} {fname}:{hi+1}  {lm.group(0)} -> {new_label}"
                          f"  (score={bscore:.2f}, {os.path.basename(rel)})")
                    if write and new_head != lines[hi]:
                        lines[hi] = new_head
                        changed += 1
                else:
                    print(f"? {fname}:{hi+1} 命中{rel}但文件名无题号")
            else:
                print(f"? {fname}:{hi+1} {lines[hi][:46]} "
                      f"最佳 {best[0] if best else '无'} score={bscore:.2f} 保留原样")
        if write and changed:
            io.open(path, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
            print(f"== {fname} 更新 {changed} 处")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    main(ap.parse_args().write)
