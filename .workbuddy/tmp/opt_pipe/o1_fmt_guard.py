# -*- coding: utf-8 -*-
"""volpost --fmt 事后自证：6 张源卡的**题面区字节必须完全不变**（铁律四）。
题面区定义：文件头 → 首个 `## 参考答案` 或 `<details>` 之前。
另报：改动是否只在答案区；行数守恒。
"""
import subprocess, sys, re, os

R = r"C:\Obsidion\妙妙屋"
CARDS = [
    "04-题库/2026机构初赛模拟题/chemy/题-CM-21-08-氮杂环庚烷azepanes是.md",
    "04-题库/2026机构初赛模拟题/伽马/题-GM-04-03-31几种分类311热塑性塑料.md",
    "04-题库/2026机构初赛模拟题/化英社/题-HYS-01-08-耐甲氧西林金黄色葡萄球菌MR.md",
    "04-题库/2026机构初赛模拟题/化英社/题-HYS-40-07-早在1979年研究人员就报道.md",
    "04-题库/2026机构初赛模拟题/壹尖培优/题-YJ-02-08-光化学在自然界和日常生活中扮.md",
    "04-题库/2026机构初赛模拟题/壹尖培优/题-YJ-12-06-61请按照酸性从强到弱给以下.md",
]

ANS_MARK = re.compile(r'(?m)^#{1,3}\s*参考答案|<details')


def q_head(txt):
    """返回题面区（答案区起点之前），以及切点索引。"""
    m = ANS_MARK.search(txt)
    if not m:
        return txt, len(txt)
    return txt[:m.start()], m.start()


def git_show(path):
    out = subprocess.run(["git", "show", "HEAD:" + path], cwd=R,
                         capture_output=True)
    if out.returncode != 0:
        return None
    return out.stdout.decode("utf-8-sig", "replace")


bad = 0
for rel in CARDS:
    cur = open(os.path.join(R, rel), encoding="utf-8-sig").read()
    old = git_show(rel)
    if old is None:
        print("[SKIP 不在 HEAD]", rel)
        continue
    qc, ic = q_head(cur)
    qo, io = q_head(old)
    ok = (qc == qo)
    if not ok:
        bad += 1
    # 统计行数
    lc, lo = cur.count("\n") + 1, old.count("\n") + 1
    print("%s %s  题面区%s  行数 %d→%d  字节 %d→%d" % (
        "OK " if ok else "FAIL", os.path.basename(rel)[:28],
        "不变" if ok else "**变了**", lo, lc, len(old.encode()), len(cur.encode())))
    if not ok:
        # 打印首个差异点
        for i in range(min(len(qc), len(qo))):
            if qc[i] != qo[i]:
                print("     首差 @%d  旧=%r 新=%r" % (
                    i, qo[max(0, i-40):i+40], qc[max(0, i-40):i+40]))
                break

print("\n题面区被改 =", bad, "（应为 0）")
sys.exit(1 if bad else 0)
