# -*- coding: utf-8 -*-
"""S1 遗留定性辅助（只读）：对清单内每张卡输出结构信息，并导出答案区图片供目检。

输出（文本）：
  · 题面区：图指代词命中行 + 图引用数
  · 答案区：图引用数 + 前 900 字（看是否重述题面）
  · 导出：answer 区所有图 → tmp/s1_export/<card>/
用法：python s1_triage.py [--export]
"""
import os
import re
import sys
import glob
import shutil

sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
BASE = os.path.join(R, "04-题库", "2026机构初赛模拟题")
OUT = os.path.join(R, ".workbuddy", "tmp", "opt_pipe", "s1_export")

# csv 中未定性的 26 张（不含已目检 10 张）
TODO = [
    ("2ChO", "题-2ChO-01-04-在苯溶液中将105mmolT.md"),
    ("2ChO", "题-2ChO-02-07-在分子被激发到单线态激发态后.md"),
    ("XeChem", "题-XeC-07-04-beginarraycmat.md"),
    ("XeChem", "题-XeC-15-04-自从的发现以来已制备出多种结.md"),
    ("chemy", "题-CM-106-01-1-1在C减压下丙二酸用脱水.md"),
    ("chemy", "题-CM-123-07-利用手性助剂可实现双键不对称.md"),
    ("chemy", "题-CM-127-02-臭氧是一类人类生活生产以及研.md"),
    ("chemy", "题-CM-165-02-顾名思义超酸是一类酸度极强的.md"),
    ("chemy", "题-CM-17-07-超分子自组装的选择性.md"),
    ("chemy", "题-CM-65-06-6-1化学式为的化合物中含有.md"),
    ("化英社", "题-HYS-01-01-某金属元素M在自然界中分布广.md"),
    ("化英社", "题-HYS-02-01-已知XYZ是同族元素其相对原.md"),
    ("化英社", "题-HYS-03-01-M单质与稀酸反应速率较慢这可.md"),
    ("化英社", "题-HYS-03-05-硫与铜元素可形成多种化合物它.md"),
    ("壹尖培优", "题-YJ-05-02-一种第七周期金属元素M与氧和.md"),
    ("汇智", "题-HZ-02-01-1999年化学家通过以下实验.md"),
    ("汇智", "题-HZ-02-04-蜂窝状层状氧化物由于其独特的.md"),
    ("汇智", "题-HZ-02-05-奎宁分子结构如右图所示是从金.md"),
    ("汇智", "题-HZ-38-02-21Nature报道了某同素.md"),
    ("清北营", "题-QBY-08-06-对高分子反应规律的探寻具有重.md"),
    ("质心GChO", "题-GChO-42-04-下图展示了某过渡元素X相关的.md"),
    ("质心GChO", "题-GChO-42-06-有着独特的螺旋结构是平面单元.md"),
    ("质心GChO", "题-GChO-73-06-61某课题组于2019年合成.md"),
    ("质心GChO", "题-GChO-82-06-61金属X反应活性较低加热时.md"),
    ("质心UChO", "题-UChO-01-05-tabletrtd1molN.md"),
    ("质心UChO", "题-UChO-02-03-A立方晶系所有的空间环境相同.md"),
]

IMGREF = re.compile(r"!\[\[([^\]]+)\]\]|!\[\]\(([^)]+)\)")
FIGWORD = re.compile(r"下图|上图|右图|左图|如图|见图|图\s*[0-9１-９]")


def main():
    export = "--export" in sys.argv
    if export and os.path.isdir(OUT):
        shutil.rmtree(OUT)
    print("S1 遗留定性：%d 张\n" % len(TODO))
    for inst, name in TODO:
        p = os.path.join(BASE, inst, name)
        if not os.path.exists(p):
            print("!! 缺文件:", p)
            continue
        t = open(p, encoding="utf-8-sig").read().replace("\r\n", "\n")
        i, j = t.find("## 题目"), t.find("## 参考答案")
        q = t[i + 5:j] if j > i > 0 else t[i + 5:]
        a = t[j:] if j > 0 else ""
        qimgs = IMGREF.findall(q)
        aimgs = IMGREF.findall(a)

        def names(lst):
            return [x[0] or x[1] for x in lst]

        qn, an = names(qimgs), names(aimgs)
        print("=" * 78)
        print("▸ [%s] %s" % (inst, name))
        print("  题面区图 %d 张 ｜ 答案区图 %d 张" % (len(qn), len(an)))
        # 题面图指代行
        fw = [(k + 1, ln.strip()) for k, ln in enumerate(q.split("\n")) if FIGWORD.search(ln)]
        print("  题面图指代词命中 %d 行：" % len(fw))
        for ln_no, ln in fw[:6]:
            print("     Q%-4d %s" % (ln_no, ln[:96]))
        # 答案区前 700 字
        head = re.sub(r"\n{2,}", "\n", a[:900]).strip()
        print("  答案区开头：")
        for ln in head.split("\n")[:10]:
            print("     A| %s" % ln[:96])
        if an:
            print("  答案区图引用顺序：")
            for k, n in enumerate(an[:10]):
                print("     %d) %s" % (k + 1, n[:70]))
        if export and an:
            d = os.path.join(OUT, name.replace(".md", ""))
            os.makedirs(d, exist_ok=True)
            for n in an:
                src = os.path.join(BASE, inst, "images", os.path.basename(n))
                if os.path.exists(src):
                    shutil.copy2(src, os.path.join(d, os.path.basename(n)))
            print("  → 已导出 %d 图到 %s" % (len(an), d))
    print("\n" + "=" * 78)


if __name__ == "__main__":
    main()
