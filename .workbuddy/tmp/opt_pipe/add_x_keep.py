# -*- coding: utf-8 -*-
"""合并登记卷 X 的 8 张装饰图（水印/简笔画/音符/花体英文/竖琴）到 figcov_keep.json。"""
import io, json, collections

P = '.workbuddy/scripts/figcov_keep.json'
d = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)

REASON = ('2026-10-14 目检 卷X：**源件装饰图/水印**（「育」大字水印、简笔画小人、音符、花体「CHEM」、竖琴等，'
          '已用联系表逐张目检确认无题意）⇒ 卷内合理剔除，故意不引')
ADD = ['15f705caa38b1d0', 'de97ea9b9a2eaf8', 'ef8b376c52efb9c', 'e67ecd53a4b9a42',
       '3dd7a6fc14155c5', '6420235fcfdd95f', 'd3518e56383bdc3', '53188f49d9ee93b']
n = 0
for a in ADD:
    if not any(k.startswith(a) for k in d if not k.startswith('_')):
        d[a] = REASON
        n += 1
json.dump(d, io.open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('新增 %d 项；白名单共 %d 项' % (n, len([k for k in d if not k.startswith('_')])))
