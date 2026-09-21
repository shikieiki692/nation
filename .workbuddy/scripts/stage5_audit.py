# -*- coding: utf-8 -*-
"""阶段5：45 块逐块上下文审计。
对每块输出：文件/块序/行号/块内原文/上文 14 行（用于发现"上方已有图片引用或同内容表格"）。
"""
import io, os, re, csv

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, "04-课件", "学生讲义")
CSV = os.path.join(ROOT, ".workbuddy", "tmp", "verbatim_worklist.csv")


def is_fence(s):
    s2 = s.rstrip("\r\n")
    return s2.strip().startswith("```") and s2.strip()[3:].strip() == ""


def main():
    rows = list(csv.DictReader(io.open(CSV, encoding="utf-8-sig", newline="")))
    out = []
    for r in rows:
        rel = r["文件"]
        a, b = int(r["起行"]), int(r["止行"])
        p = os.path.join(SRC, rel)
        t = io.open(p, encoding="utf-8", newline="").read().split("\n")
        crlf = t[0].endswith("\r") if t else False
        # 上文 14 行（不含块首行）
        lo = max(0, a - 15)
        ctx = t[lo:a - 1]
        # 统计上文里的图片引用 / 表格行
        imgs = [c.strip() for c in ctx if "![[" in c]
        tbl = sum(1 for c in ctx if c.strip().startswith("|") and c.strip().endswith("|"))
        out.append("=" * 100)
        out.append("[%s] 块序%s  行 %d-%d  EOL=%s" % (rel, r["块序"], a, b, "CRLF" if crlf else "LF"))
        out.append("  引导语: %s" % r["引导语"][:70])
        out.append("  判据: %s | 建议分型: %s | CSV建议: %s" % (r["判据类别"], r["建议分型"], r["建议处置"]))
        out.append("  --- 上文14行内的图片引用: %s" % (imgs if imgs else "无"))
        out.append("  --- 上文14行内的表格行数: %d" % tbl)
        out.append("  --- 块内原文 ---")
        for i in range(a - 1, b):
            out.append("   %4d|%s" % (i + 1, t[i].rstrip("\r")))
    txt = "\n".join(out)
    dst = os.path.join(ROOT, ".workbuddy", "tmp", "stage5_audit.txt")
    io.open(dst, "w", encoding="utf-8", newline="\n").write(txt)
    print("已写出", dst, len(txt), "字符")


if __name__ == "__main__":
    main()
