# -*- coding: utf-8 -*-
"""卷名解析（机构模拟卷）：主系列＝「非有机」，有机专题卷（O1…）＝「有机」。

判据＝**实际存在的 md 文件**（不按卷号硬猜）⇒ 对既有 9 卷（X~XVII）行为零变化。
用法：
    import volname as VN
    VN.md_path('O1', '答案版')
    VN.docx_name('O1', '学生版·真题版式')
"""
import os

ROOT = r"C:\Obsidion\妙妙屋"
QB = os.path.join(ROOT, "04-题库")
DOCX = os.path.join(ROOT, "00-首页", "题组Word", "初赛模拟卷", "真题版式")
ZHENTI = DOCX


def kind(vol):
    for k in ("有机", "非有机"):
        if os.path.exists(os.path.join(QB, "初赛模拟卷%s（%s·答案版）.md" % (vol, k))):
            return k
    return "非有机"


def md_name(vol, tag):
    return "初赛模拟卷%s（%s·%s）.md" % (vol, kind(vol), tag)


def md_path(vol, tag):
    return os.path.join(QB, md_name(vol, tag))


def docx_name(vol, tag):
    return "初赛模拟卷%s（%s·%s）.docx" % (vol, kind(vol), tag)


def docx_path(vol, tag):
    return os.path.join(DOCX, docx_name(vol, tag))


def base(vol):
    return "初赛模拟卷%s（%s）" % (vol, kind(vol))
