#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""add_allow_final.py —— 把本轮「整卡救援」造成的 oMath 倒退登记到 render_gate 允许表。"""
import os, sys
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
AL = os.path.join(R, "11-模板/scripts/render_gate_allowlist.txt")
CARDS = [
    "chemy/题-CM-149-05-自组装被广泛应用于各种纳米材.md",
    "chemy/题-CM-151-01-与ItBu结构见下图按计量比.md",
    "chemy/题-CM-72-08-8-1某种漂白剂在下会较快自.md",
    "chemy/题-CM-96-05-分子筛是一种天然或人工合成的.md",
    "化英社/题-HYS-01-06-卤原子转移反应是实现氧化态转.md",
    "化英社/题-HYS-07-07-据此回顾B的定义用63中的已.md",
    "化英社/题-HYS-10-04-41利用催化剂以发烟硫酸为工.md",
    "北京夏令营/题-BJLY-04-无机综合-07-有人将纯净的NO气体收集到一.md",
    "汇智/题-HZ-01-03-31X的某些化合物是熟知的半.md",
    "汇智/题-HZ-10-01-铅Pb在中国古代也因烧炼后能.md",
    "清北营/题-QBY-02-05-下图是某种物质的其中一种晶型.md",
    "清北营/题-QBY-07-02-金单质通常称为黄金常用作货币.md",
    "清北营/题-QBY-17-03-自旋冰SpinIce是一种特.md",
    "质心GChO/题-GChO-48-06-61回答下列与单质碘性质相关.md",
]
REASON = ("2026-10-07 整卡救援：越界块删除／题面按题界截断删除**他题内容**（含公式），"
          "oMath 下降属**预期删节**非渲染退化；full 模式 29/29 PASS。")
raw = open(AL, "rb").read().decode("utf-8-sig")
eol = "\r\n" if "\r\n" in raw else "\n"
exist = set(raw.replace("\r\n", "\n").split("\n"))
add = []
for c in CARDS:
    p = "04-题库/2026机构初赛模拟题/" + c
    if p in exist:
        print("  已存在:", c); continue
    add.append(p + "\t" + REASON)
if add:
    txt = raw.replace("\r\n", "\n")
    if not txt.endswith("\n"):
        txt += "\n"
    txt += "\n".join(add) + "\n"
    open(AL, "wb").write(txt.encode("utf-8"))
print("新增 %d 条 → %s" % (len(add), AL))
