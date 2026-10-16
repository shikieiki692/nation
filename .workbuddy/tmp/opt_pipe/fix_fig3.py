# -*- coding: utf-8 -*-
r"""A3｜④-e 三处真缺陷的 vol md 层最小修补（修补后 docx 重建即愈）。

判据/依据：09-审计报告/2026-10-16-机构模拟卷④-e残余核查与师-生一致闸门通用化.md §二/§三。
原则：**只补「引而无图」的那一处**，其余字节不动；EOL 守恒；逐处 count==1 断言；先备份。
"""
import os
import re
import shutil
import sys

ROOT = r"C:/Obsidion/妙妙屋"
BAK = os.path.join(ROOT, ".workbuddy", "tmp", "opt_pipe", "_bak_fig3")
os.makedirs(BAK, exist_ok=True)

B = "b820c9b294946eae7e961f0511d94691cbb1b6e7c2d0a839b7dc40498e7b5dd6.jpg"
C1 = "143ca87a54061c3956ccb480feb22aef092f177264fe6e25c062ca85fb9e12bc.jpg"
C2 = "7e7ab009ad656c8c262b775a4dfb6692be5c809399d19217d5cd2eb924073f3f.jpg"
R = "490596bc3de9bbd3421a390c55ce4108f6d50dc039a635472223103c9ff8dc0d.jpg"

JOBS = [
    # (相对路径, 模式, 正则/字面, 替换, 处数)
    ("04-题库/初赛模拟卷X（非有机·答案版）.md", "re",
     r"(\*\*6-2-2\*\* 仅通过题目条件判断, \$L_\{Ph\}\$ 可能有一下两种结构。)(\r?\n\r?\n)(但是将后者带入反应体系)",
     r"\1\2![[%s]]\2\3" % B, 1),
    ("04-题库/初赛模拟卷XI（非有机·学生版）.md", "lit",
     "| | ![[8d3112e549b32ad877253a55e22aa27113fe7f10ef479397353d90738c45fc25.jpg]] | ![[066d8ddbc928572318d9b54e795cc4cb3e668d13ccfce64105eedb4669cd69e6.jpg]] |",
     "| ![[%s]] | ![[8d3112e549b32ad877253a55e22aa27113fe7f10ef479397353d90738c45fc25.jpg]] | ![[066d8ddbc928572318d9b54e795cc4cb3e668d13ccfce64105eedb4669cd69e6.jpg]] |" % C1, 1),
    ("04-题库/初赛模拟卷XI（非有机·学生版）.md", "lit",
     "| | ![[202b83c990bba174ba02ff460d3c8fa5d5fac5279d3ae09714400a24c8fafc18.jpg]] | ![[eba4f12ab3514e16439e88ef552ef4214a3ca7ca4ba01995601d8477ff40b3d9.jpg]] |",
     "| ![[%s]] | ![[202b83c990bba174ba02ff460d3c8fa5d5fac5279d3ae09714400a24c8fafc18.jpg]] | ![[eba4f12ab3514e16439e88ef552ef4214a3ca7ca4ba01995601d8477ff40b3d9.jpg]] |" % C2, 1),
    ("04-题库/初赛模拟卷XI（非有机·答案版）.md", "lit",
     "| | ![[8d3112e549b32ad877253a55e22aa27113fe7f10ef479397353d90738c45fc25.jpg]] | ![[066d8ddbc928572318d9b54e795cc4cb3e668d13ccfce64105eedb4669cd69e6.jpg]] |",
     "| ![[%s]] | ![[8d3112e549b32ad877253a55e22aa27113fe7f10ef479397353d90738c45fc25.jpg]] | ![[066d8ddbc928572318d9b54e795cc4cb3e668d13ccfce64105eedb4669cd69e6.jpg]] |" % C1, 1),
    ("04-题库/初赛模拟卷XI（非有机·答案版）.md", "lit",
     "| | ![[202b83c990bba174ba02ff460d3c8fa5d5fac5279d3ae09714400a24c8fafc18.jpg]] | ![[eba4f12ab3514e16439e88ef552ef4214a3ca7ca4ba01995601d8477ff40b3d9.jpg]] |",
     "| ![[%s]] | ![[202b83c990bba174ba02ff460d3c8fa5d5fac5279d3ae09714400a24c8fafc18.jpg]] | ![[eba4f12ab3514e16439e88ef552ef4214a3ca7ca4ba01995601d8477ff40b3d9.jpg]] |" % C2, 1),
    ("04-题库/初赛模拟卷XIp（非有机·答案版）.md", "lit",
     "| 7-1 | |",
     "| 7-1 | ![[%s]] |" % R, 1),
]


def main():
    # 备份
    for rel in sorted({j[0] for j in JOBS}):
        d = os.path.join(BAK, os.path.basename(rel))
        if not os.path.exists(d):
            shutil.copy2(os.path.join(ROOT, rel), d)
    todo = {}
    for rel, mode, pat, rep, cnt in JOBS:
        todo.setdefault(rel, []).append((mode, pat, rep, cnt))

    ok = 0
    for rel, items in todo.items():
        p = os.path.join(ROOT, rel)
        raw = open(p, encoding="utf-8-sig", newline="").read()
        bom = "\ufeff" if raw.startswith("\ufeff") else ""
        body = raw[1:] if bom else raw
        out = body
        for mode, pat, rep, cnt in items:
            if mode == "re":
                n = len(re.findall(pat, out))
                if n != cnt:
                    print("  [SKIP n=%d] %s :: %s" % (n, rel, pat[:40]))
                    continue
                out = re.sub(pat, rep, out, count=cnt)
            else:
                n = out.count(pat)
                if n != cnt:
                    print("  [SKIP n=%d] %s :: %s" % (n, rel, pat[:40]))
                    continue
                out = out.replace(pat, rep, cnt)
        if out == body:
            print("  [NOCHANGE] %s" % rel)
            continue
        open(p, "w", encoding="utf-8", newline="").write(bom + out)
        print("  [OK] %-40s +%d 字符" % (rel, len(out) - len(body)))
        ok += 1
    print("\n已改 %d / %d 文件" % (ok, len(todo)))
    return 0 if ok == len(todo) else 1


if __name__ == "__main__":
    sys.exit(main())
