# -*- coding: utf-8 -*-
"""伽马 GM-25 系列「题面截断」范围探针（只读）。
用法：
    python gm_scope.py            # 只做「题面小问 vs 答案区小问」比对（秒级）
    python gm_scope.py --pool     # 追加池状态（build_pool，约 1 分钟）
判定：题面缺的小问 = 答案区出现、题面未出现的小问号 ⇒ 即「被吞进答案区的题干」。
"""
import os, re, sys, glob

sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
D = os.path.join(R, "04-题库", "2026机构初赛模拟题", "伽马")
SUB = re.compile(r"(?m)^[ \t>*]*\*{0,2}(\d+)-(\d+)")


def key(s):
    a, b = s.split("-")
    return (int(a), int(b))


def main():
    rows = []
    for p in sorted(glob.glob(os.path.join(D, "题-GM-25-*.md"))):
        ls = open(p, encoding="utf-8-sig").read().replace("\r\n", "\n").split("\n")
        ai = next((k for k, l in enumerate(ls) if l.startswith("## 参考答案")), len(ls))
        qs = sorted(set("%s-%s" % t for t in SUB.findall("\n".join(ls[:ai]))), key=key)
        as_ = sorted(set("%s-%s" % t for t in SUB.findall("\n".join(ls[ai:]))), key=key)
        miss = [x for x in as_ if x not in qs and key(x)[1] <= 20]  # 过滤 5-75 类误匹配
        rows.append((os.path.basename(p), qs, as_, miss))

    print("%-42s %-22s %-26s %s" % ("卡", "题面小问", "答案区小问", "题面缺"))
    print("-" * 104)
    for name, qs, as_, miss in rows:
        print("%-42s %-22s %-26s %s" % (name[:40], ",".join(qs) or "无",
                                        ",".join(as_) or "无", ",".join(miss) or "—"))
    bad = [r for r in rows if r[3]]
    print("-" * 104)
    print("判定：题面截断 %d 张 ⇒ %s" % (len(bad), "、".join(r[0][:14] for r in bad) or "无"))

    if "--pool" in sys.argv:
        import importlib.util as u
        os.chdir(R)
        sp = u.spec_from_file_location("B", os.path.join(R, ".workbuddy", "tmp", "opt_pipe", "build_org.py"))
        B = u.module_from_spec(sp); sp.loader.exec_module(B); B.ALL_YEARS = True
        pool = B.build_pool()
        print("\n池规模：%d（元素 %d / 结构 %d / 原理 %d）" % (
            sum(len(v) for v in pool.values()), len(pool.get("元素与分析", [])),
            len(pool.get("结构化学", [])), len(pool.get("化学原理", []))))
        for name, _q, _a, miss in rows:
            p = os.path.join(D, name)
            why = B.why_not_in_pool(p)
            print("  %-40s %s" % (name[:38], "★在池" if why is None else "掉池：" + str(why)))


if __name__ == "__main__":
    main()
