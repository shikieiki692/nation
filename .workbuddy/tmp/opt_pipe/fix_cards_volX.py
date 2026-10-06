# -*- coding: utf-8 -*-
"""fix_cards_volX.py —— 卷X 回源补齐：确定性文字修正（带断言 + 保持行尾/BOM）。

回源依据：原 PDF 逐页目视（见 `09-审计报告/2026-10-06-卷X回源三元核验报告.md`）。
默认 dry-run；`--apply` 才写盘。
"""
import sys
import io

sys.stdout.reconfigure(encoding='utf-8')
BASE = '04-题库/2026机构初赛模拟题'

# 每项：(卡路径, [(旧串, 新串, 期望次数), ...])
JOBS = [
    # 1. HYS-11-04：题面「氮」被 OCR 成「氙/氪氙」等（原 PDF p4-p7 为氮）
    (BASE + '/化英社/题-HYS-11-04-分子氙通常被视为惰性物质因为.md', [
        ('氪氙三键', '氮氮三键', 1),
        ('分子氙', '分子氮', 2),
        ('聚合氙', '聚合氮', 1),
        ('氙氙单键', '氮氮单键', 2),
        ('氮氙单键', '氮氮单键', 2),
        ('氙气和氙气的流速', '氮气和氩气的流速', 1),
    ]),
    # 2. XeC-40-04：小问「4-2 8 个小立方体」被并成「4-28 个」；答案区游离「(e)」行
    (BASE + '/XeChem/题-XeC-40-04-方钴矿系skutterudi.md', [
        ('4-28 个小立方体中有 6 个含', '4-2 8 个小立方体中有 6 个含', 2),
        ('(e) 以 Co₃ 为基准，La:Yb:Co:Sb=0.12:0.20:4.00:11.84', '', 1),
    ]),
    # 3. CM-14-04：元素 111 錀(Rg) 被写成「轮/铊」（形近/同音替换）
    (BASE + '/chemy/题-CM-14-04-第111号元素轮是第七周期超.md', [
        ('元素轮是', '元素錀是', 1),
        ('元素铊是', '元素錀是', 1),
        ('“轮牌”', '“錀牌”', 1),
        ('“铊牌”', '“錀牌”', 1),
        ('长寿的轮同位素', '长寿的錀同位素', 1),
        ('长寿的铊同位素', '长寿的錀同位素', 1),
        ('第一种轮的同位素', '第一种錀的同位素', 1),
        ('第一种铊的同位素', '第一种錀的同位素', 1),
        ('你有轮牌吗', '你有錀牌吗', 1),
    ]),
]


def main():
    apply = '--apply' in sys.argv
    for path, reps in JOBS:
        raw = open(path, 'rb').read()
        bom = raw[:3] == b'\xef\xbb\xbf'
        full = raw.decode('utf-8-sig')
        # 只改「正文」（跳过 FM 与 H1，避免与文件名不一致）
        i = full.find('\n# ')
        if i >= 0:
            j = full.find('\n', i + 1)
            head, t = full[:j + 1], full[j + 1:]
        else:
            head, t = '', full
        ok = True
        for old, new, exp in reps:
            n = t.count(old)
            if n != exp:
                print('  ✗ [%s] 期望 %d 处「%s」，实为 %d 处 ⇒ 跳过本卡'
                      % (path.split('/')[-1], exp, old, n))
                ok = False
                break
            t = t.replace(old, new)
        if not ok:
            continue
        if apply:
            open(path, 'wb').write((b'\xef\xbb\xbf' if bom else b'') + (head + t).encode('utf-8'))
        print('  ✓ %s：%d 条替换%s' % (path.split('/')[-1], len(reps), '（已写盘）' if apply else '（dry-run）'))
    print('done.')


if __name__ == '__main__':
    main()
