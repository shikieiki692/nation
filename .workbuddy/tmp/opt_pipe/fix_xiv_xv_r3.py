# -*- coding: utf-8 -*-
"""fix_xiv_xv_r3.py —— 2026-10-09 逐页视觉核验后的源卡修复（卷 XIV / XV）。

修复项（全部经**回源**确认）：
  ① 卷 XIV 第3题 3-3-1 答案图丢失 —— 根因＝`noise_of()` 把「浅色晶体投影图」误判为
     watermark（dark=0.000 < 0.005）⇒ 加入 `noise_keep.json` 允许清单（白名单优先于规则）。
  ② 卷 XIV 第1题 1-4-2 题面截断 —— 源 PDF p6 完整句含「计算出的理论密度 D=3.243 g/cm³，
     据此计算 M 的化学式。」；卡把后半句切进了答案区 ⇒ 移回题面 + 删答案区重复片段。
  ③ 卷 XIV 第1题 答案区首标签缺失（源答案页有 `5-1-1（共 4 分）`）⇒ 补 `5-1-1 `。
  ④ 卷 XIV 第5题 `5-1` 未独立成行（埋在 Ramsdell 段尾）⇒ 拆行。
  ⑤ 卷 XIV 第10题 `10-3-1` 未独立成行（粘在提示段尾）⇒ 拆行。
  ⑥ 卷 XIV 第7题 `6-1 中的中的五种`（源 PDF p4 为「6-1 中的五种」）⇒ 删重复「中的」（2 处）。
  ⑦ 卷 XIV 第8题 `设立方体的棱长为 a₁`（源为「设**大**立方体」）⇒ 补「大」。
  ⑧ 卷 XV 第1题 `4-3-1` 未独立成行（粘在 `**4-3**` 回显行尾）⇒ 拆行（保留回显作小标题）。

用法：python -X utf8 fix_xiv_xv_r3.py [--apply]
"""
import io
import os
import sys
import shutil
import datetime

R = r"C:\Obsidion\妙妙屋"
HERE = os.path.join(R, ".workbuddy", "tmp", "opt_pipe")
Q = os.path.join(R, "04-题库", "2026机构初赛模拟题")
BAKDIR = os.path.join(HERE, "card_bak_r3")
APPLY = "--apply" in sys.argv

CM01 = os.path.join(Q, "chemy", "题-CM-01-05-很多具有钙钛矿结构的化合物是.md")
HYS = os.path.join(Q, "化英社", "题-HYS-01-02-研究钙钛矿衍生结构时常用Ra.md")
CH2 = os.path.join(Q, "2ChO", "题-2ChO-04-05-51金红石是典型的四方晶体类.md")
QBY = os.path.join(Q, "清北营", "题-QBY-08-06-611堆积层永远是晶体结构问.md")
HZ11 = os.path.join(Q, "汇智", "题-HZ-11-05-在晶体结构的研究中将晶胞拆分.md")
HZ07 = os.path.join(Q, "汇智", "题-HZ-07-04-41著名的钙钛矿型晶体想必大.md")

# (路径, 旧串, 新串, 说明, 期望命中数)
EDITS = [
    (CM01,
     "计算出的理论密度 $D = 3.243 \\, g/cm^{3}$ ，据此计算 M 的化学式。\n\n",
     "",
     "②b 答案区删「1-4-2 题干后半句」重复段", 1),
    (CM01,
     "$b = 46.305 \\, \\text{Å}$ ， $c = 8.436 \\, \\text{Å}$ ，",
     "$b = 46.305 \\, \\text{Å}$ ， $c = 8.436 \\, \\text{Å}$ ，"
     "计算出的理论密度 $D = 3.243 \\, \\mathrm{g/cm^{3}}$ ，据此计算 M 的化学式。",
     "②a 题面补全 1-4-2", 1),
    (CM01,
     "## 参考答案\n\n（共 4 分）",
     "## 参考答案\n\n5-1-1（共 4 分）",
     "③ 答案区补 5-1-1 标签", 1),
    (HYS,
     "六方对称性。2-1 钛酸钡",
     "六方对称性。\n\n2-1 钛酸钡",
     "④ 题面 5-1 独立成行", 1),
    (CH2,
     "结合对称性看)5-3-1 写出晶体的化学式。",
     "结合对称性看)\n\n5-3-1 写出晶体的化学式。",
     "⑤ 题面 5-3-1 独立成行", 1),
    (QBY,
     "6-1 中的中的五种",
     "6-1 中的五种",
     "⑥ 删重复「中的」", 2),
    (HZ11,
     "设立方体的棱长为 $a_{1}$",
     "设大立方体的棱长为 $a_{1}$",
     "⑦ 补「大」立方体", 1),
    (HZ07,
     "配位数为其对应价态常见配位数。4-3-1 给出可以体现其结构的化学式,并标注对应Au的价态。",
     "配位数为其对应价态常见配位数。\n\n"
     "**4-3-1** 给出可以体现其结构的化学式,并标注对应Au的价态。",
     "⑧ 4-3-1 独立成行", 1),
]

KEEP = os.path.join(HERE, "noise_keep.json")
NEW_KEEP = "1ec0e9504a8e52a962998d97d2e9f9387016dda6f3b2ae404fbbc41e547348f6.jpg"


def main():
    cache = {}

    def load(p):
        if p not in cache:
            cache[p] = io.open(p, encoding="utf-8-sig").read()
        return cache[p]

    ok = True
    for path, old, new, tag, want in EDITS:
        t = load(path)
        n = t.count(old)
        if n != want:
            print("!! [%s] 命中 %d 次（应为 %d）" % (tag, n, want))
            ok = False
            continue
        cache[path] = t.replace(old, new)
        print("OK [%s] ×%d" % (tag, n))
    if not ok:
        print("\n有未命中项，未写盘。")
        return

    # noise_keep.json 允许清单
    kt = io.open(KEEP, encoding="utf-8").read()
    if NEW_KEEP in kt:
        print("OK [① noise_keep] 已存在，跳过")
    else:
        arr = kt.rstrip()
        assert arr.endswith("]"), arr[-30:]
        arr = arr[:-1].rstrip()
        if not arr.endswith("["):
            arr += ","
        arr += '\n "%s"\n]\n' % NEW_KEEP
        print("OK [① noise_keep] 追加浅色晶体图")

    if not APPLY:
        print("\n(dry) 未写盘。加 --apply 执行。")
        return

    os.makedirs(BAKDIR, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%m%d_%H%M")
    for p in sorted(cache):
        shutil.copy2(p, os.path.join(BAKDIR, os.path.basename(p) + ".bak-" + stamp))
        io.open(p, "w", encoding="utf-8", newline="\n").write(cache[p])
        print("写盘", os.path.basename(p)[:52])
    io.open(KEEP, "w", encoding="utf-8", newline="\n").write(arr)
    print("写盘 noise_keep.json")
    print("\n完成；备份目录 =", BAKDIR)


main()
