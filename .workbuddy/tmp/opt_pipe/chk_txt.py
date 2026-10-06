# -*- coding: utf-8 -*-
"""检查指定答案 PDF 的文字层长度（≥600 视为可自动抽取）。"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
try:
    import fitz
    try:
        fitz.TOOLS.mupdf_display_errors(False); fitz.TOOLS.mupdf_display_warnings(False)
    except Exception:
        pass
except Exception:
    fitz = None
OCR = '06-外部资料导入/OCR'
F = [
 '01-题目/质心合集新/UChO模拟试题合集答案/4th ZCHEM-UChO 答案.pdf',
 '01-题目/质心合集新/UChO模拟试题合集答案/5th ZCHEM-UChO 答案.pdf',
 '01-题目/质心合集新/GChO模拟试题合集答案/ZCHEM-GChO35解析手稿.pdf',
 '01-题目/质心合集新/GChO模拟试题合集答案/ZCHEM-GChO48参考答案与评分标准.pdf',
 '01-题目/2026一式暑期刷题班及数据/一式02/一式02答案.pdf',
 '01-题目/2026一式暑期刷题班及数据/一式03/一式03答案.pdf',
 '01-题目/化学-夏令营-北京/北京夏令营-无机巩固练习一-答案1785409364.pdf',
 '01-题目/化学-夏令营-北京/北京夏令营-无机巩固练习二-答案1785491473.pdf',
 '02-讲义/2026年化英社4月春季班/2026化英社 春季班试卷/有机/春季-有机专题1答案(已优化).pdf',
 '02-讲义/2026年化英社五一物化班/2026年化英社五一物化班/华英社 物化专题 2026五一期间/化英社2026第40届决赛物化专题2答案（清晰版）.pdf',
 '01-题目/第40届化英社化学奥林匹克（初赛）夏季/第40届化英社化学奥林匹克（决赛）夏季模拟试题1参考答案.pdf',
 '01-题目/第40届化英社化学奥林匹克（初赛）夏季/第40届化英社化学奥林匹克(初赛)夏季模拟试题3参考答案.pdf',
 '01-题目/第40届化英社化学奥林匹克（初赛）夏季/第40届化英社化学奥林匹克(初赛)夏季初赛模拟13参考答案_1.pdf',
 '01-题目/2026暑假化英社解题技巧班/第40届化英社化学奥林匹克（初赛）夏季模拟14参考答案.pdf',
 'chemy/第33届Chemy化学奥林匹克题目合集答案..pdf',
 'chemy/第34届Chemy化学奥林匹克题目合集答案..pdf',
 'chemy/第35届中国化学奥林匹克Chemy参考答案合集/第35届中国化学奥林匹克Chemy参考答案合集._1-199.pdf',
 'chemy/第37届Chemy题目合集答案/第37届Chemy题目合集答案._1-199.pdf',
 'chemy/第37届Chemy题目合集答案/第37届Chemy题目合集答案._200-314.pdf',
 '01-题目/2026年chemy寒假班/化学试卷-初赛模拟试题4+答案.pdf',
 '01-题目/2026年chemy夏令营/第40届chemy夏季班/第41届chemy联赛/第41届Chemy联赛试题答案.pdf',
 '01-题目/2026年chemy寒假班/第三十九届Chemy化学奥林匹克竞赛联赛试题答案5与评分标准.pdf',
 '01-题目/2026年方圆杭州寒假班/2026寒假有机专题资料合集/试卷1/有机化学测试题1 答案.pdf',
 '01-题目/2026年方圆杭州寒假班/方圆2026冬令营无机提高补充资料2.14/习题手稿/2.10习题三答案.pdf',
 '01-题目/2026年五一伽马初赛模拟杭州班/试题➕答案/五一伽马杭州答案1.pdf',
 '01-题目/2026年五一伽马初赛模拟杭州班/试题➕答案/五一伽马杭州答案5.pdf',
 '01-题目/2026年XEchem寒假班/Xechem模拟三（晶体）答案.pdf',
 '01-题目/2026年XEchem寒假班/Xechem模拟四答案.pdf',
 '01-题目/2026年XEchem寒假班/Xechem模拟五答案.pdf',
]
for f in F:
    p = os.path.join(OCR, f)
    if not os.path.exists(p):
        print('%-3s %s' % ('MISS', f)); continue
    if fitz is None:
        print('%-3s %s' % ('?', f)); continue
    try:
        d = fitz.open(p)
        n = sum(len(d[i].get_text()) for i in range(min(d.page_count, 80)))
        print('%-6s pg=%-3d txt=%-7d %s' % ('AUTO' if n > 600 else 'SCAN', d.page_count, n, f))
    except Exception as e:
        print('ERR %s %s' % (e, f))
