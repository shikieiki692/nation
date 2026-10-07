# -*- coding: utf-8 -*-
"""修 HZ-37-09：题面区尾部串入他题（1-1-2…）⇒ 截断 + 校勘注。"""
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = r'C:\Obsidion\妙妙屋'
p = os.path.join(ROOT, r'04-题库\2026机构初赛模拟题\汇智\题-HZ-37-09-91关于晶格能下列说法正确的.md')
t = open(p, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n')

i = t.find('## 题目'); j = t.find('## 参考答案')
seg = t[i:j]
cut = seg.find('\n\n1-1-2 写出反应 1')
assert cut > 0, '未找到切点'
dropped = seg[cut:].strip()
keep = seg[:cut].rstrip()
note = ('\n\n> 📄 校勘（2026-10-07）：源卡题面区尾部**串入了另一题**（`1-1-2 写出反应 1~3 的化学方程式…` '
        '及其解答与《…模拟试题 1 答案》标题，共 %d 字），非本卡内容 ⇒ 已截断（本卡 9-1~9-3-2 完整保留）。' % len(dropped))

new_t = t[:i] + keep + note + '\n\n' + t[j:]
open(p, 'w', encoding='utf-8', newline='\n').write(new_t)

# 复核
t2 = open(p, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n')
i2 = t2.find('## 题目'); j2 = t2.find('## 参考答案'); k2 = t2.find('## 知识点映射')
print('结构:', {h: t2.count(h) for h in ['## 题目', '## 参考答案', '## 知识点映射']})
print('题面区 %d 字 / 答案区 %d 字' % (len(t2[i2:j2]), len(t2[j2:k2])))
print('丢弃内容首 80: %r' % dropped[:80])
print('题面区尾部 200: %r' % t2[i2:j2][-200:])
