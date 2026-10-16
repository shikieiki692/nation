# -*- coding: utf-8 -*-
"""卷 md 守卫：验证 old→new 的**所有改动行**都落在「答案区」。
答案区定义（逐行扫描）：`#### 答案` 起 → 下一个 `### 第` 或 `## 第…部分` 或 EOF。
用法：python o1_volguard.py <old.md> <new.md>
"""
import re, sys, difflib

QN = re.compile(r'^#{2,3}\s*(第\s*\d+\s*题|第[一二三四五]部分|附[:：])')
ANS = re.compile(r'^\s*#{2,6}\s*答案')


def answer_line_mask(lines):
    """返回同长度 bool 列表：该行是否属于答案区。"""
    mask = []
    inans = False
    for ln in lines:
        if ANS.match(ln):
            inans = True
        elif QN.match(ln):
            inans = False
        mask.append(inans)
    return mask


def main(old_p, new_p):
    old = open(old_p, encoding="utf-8-sig").read().replace("\r\n", "\n").split("\n")
    new = open(new_p, encoding="utf-8-sig").read().replace("\r\n", "\n").split("\n")
    mnew = answer_line_mask(new)
    sm = difflib.SequenceMatcher(None, old, new, autojunk=False)
    bad = 0
    total = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        total += 1
        # 新侧行号 j1..j2-1（纯删时 j1==j2，看旧侧 i1 就近映射）
        rows = list(range(j1, j2)) if j2 > j1 else [max(0, min(len(mnew) - 1, j1))]
        outside = [r for r in rows if not mnew[r]]
        if outside:
            bad += 1
            print("  ✗ %-8s 新行 %s 落题面区：%r" % (
                tag, outside[:3], [new[r][:60] for r in outside[:2]]))
    print("改动块 %d，其中落题面区 %d（应为 0）" % (total, bad))
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
