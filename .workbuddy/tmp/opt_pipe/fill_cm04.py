# -*- coding: utf-8 -*-
"""从 chemy「化学试卷-初赛模拟试题4+答案.md」抽取第9题答案段，规范化后写入 CM-04-09 卡。
- 源 md 的 `## X` 在卡内会截断答案区 ⇒ 一律降为 `**X**`
- 图片路径 `化学试卷-初赛模拟试题4+答案_images/` → `images/`
用法：python fill_cm04.py [--apply]
"""
import os, re, sys

sys.stdout.reconfigure(encoding='utf-8')
os.chdir(r'C:\Obsidion\妙妙屋')
APPLY = '--apply' in sys.argv
SRC = '2026机构初赛模拟题/10-chemy/化学试卷-初赛模拟试题4+答案.md'
CARD = '04-题库/2026机构初赛模拟题/chemy/题-CM-04-09-炔丙醇在酸性条件下易于发生下.md'
IMGD = '04-题库/2026机构初赛模拟题/chemy/images'

t = open(SRC, encoding='utf-8-sig').read().replace('\r\n', '\n')
lines = t.split('\n')
# 第9题答案段 = 从「## 9-1」到「## 第 10 题」或 EOF
start = next(i for i, l in enumerate(lines) if re.match(r'^##\s*9-1\b', l))
end = next((i for i, l in enumerate(lines[start + 1:], start + 1) if re.match(r'^##\s*(第\s*10|10-1)\b', l)), len(lines))
block = '\n'.join(lines[start:end]).strip()
print('抽取 %d 行' % (end - start))

# 规范化
block = re.sub(r'(?m)^##[ \t]*', '**', block)
block = re.sub(r'(?m)^(\*\*[^*\n]+)$', r'\1**', block)      # 补尾部 **
block = block.replace('化学试卷-初赛模拟试题4+答案_images/', 'images/')
# 校验引用的图都存在
refs = re.findall(r'!\[\]\(images/([^)]+)\)', block)
missing = [r for r in refs if not os.path.exists(os.path.join(IMGD, r))]
print('引用图 %d 张，缺 %d' % (len(refs), len(missing)))
assert not missing, missing[:5]

md = ('（源：chemy 第40届初赛模拟4 参考答案 · 第 9 题；自源 md 抽取，图片路径已归卡）\n\n'
      + block + '\n\n> 📌 据源 md 参考答案段抽取；`##` 已规范为 `**…**` 以免截断卡结构。\n')

card = open(CARD, encoding='utf-8-sig').read().replace('\r\n', '\n')
ia = card.find('## 参考答案'); ik = card.find('## 知识点映射')
assert ia > 0 and ik > ia
new = card[:ia] + '## 参考答案\n\n' + md + '\n' + card[ik:]
if APPLY:
    open(CARD, 'w', encoding='utf-8', newline='\n').write(new)
print('长度 %d → %d  %s' % (len(card), len(new), '[APPLY]' if APPLY else '[DRY-RUN]'))
