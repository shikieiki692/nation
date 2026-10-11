# -*- coding: utf-8 -*-
"""列出 S1 清单卡「答案区每张图引用」的上下文（前 70 字），用于语义定性。"""
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
BASE = os.path.join(R, "04-题库", "2026机构初赛模拟题")
import importlib.util as _u
spec = _u.spec_from_file_location("t", os.path.join(R, ".workbuddy/tmp/opt_pipe/s1_triage.py"))
_m = _u.module_from_spec(spec)
spec.loader.exec_module(_m)
TODO = _m.TODO

IMG = re.compile(r"!\[\[([^\]]+)\]\]|!\[\]\(([^)]+)\)|<img[^>]+src=\"([^\"]+)\"")


def main():
    for inst, name in TODO:
        p = os.path.join(BASE, inst, name)
        if not os.path.exists(p):
            continue
        t = open(p, encoding="utf-8-sig").read().replace("\r\n", "\n")
        j = t.find("## 参考答案")
        if j < 0:
            continue
        q = t[t.find("## 题目") + 5:j]
        a = t[j:]
        # 题面图指代行
        fw = [ln.strip() for ln in q.split("\n") if re.search(r"下图|上图|右图|左图|如图|见图", ln)]
        am = list(IMG.finditer(a))
        if not am and not fw:
            continue
        print("=" * 74)
        print("▸ [%s] %s  （题面图 %d / 答案图 %d）"
              % (inst, name[:36], len(re.findall(r"!\[\[|!\[\]\(|<img", q)), len(am)))
        for ln in fw[:4]:
            print("  题面指代| %s" % ln[:92])
        for k, m in enumerate(am[:8]):
            s = m.start()
            pre = a[max(0, s - 80):s].replace("\n", "⏎")
            pre = re.sub(r"\s+", " ", pre)[-70:]
            print("  图%d 前文: …%s" % (k + 1, pre))
    print("=" * 74)


if __name__ == "__main__":
    main()
