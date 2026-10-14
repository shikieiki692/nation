# -*- coding: utf-8 -*-
"""对 11 张无证据卡，dump 正文中段（非空行 8~40）以判状态"""
import io, os, re

os.chdir(r'C:\Obsidion\妙妙屋')
D = '00-首页/活跃任务'
NAMES = [
 '习题册制作-执行计划-2026-08-29.md',
 '交接-2026-09-15-备课线收尾核验.md',
 '任务卡-2026-09-14-习题书裸下标收口与git健壮性复核.md',
 '任务卡-2026-09-16-组题收口与两批新批次纳入.md',
 '任务卡-KP待完善项非文字任务清零.md',
 '任务卡-KP薄壳队列与治理后续.md',
 '任务卡-validate_kb每周运行.md',
 '任务卡-学生反馈闭环建立.md',
 '任务卡-学生材料清理.md',
 '任务卡-实验模块决策.md',
 '任务卡-纸质版排版测试.md',
]
for f in NAMES:
    t = io.open(os.path.join(D, f), encoding='utf-8-sig').read()
    m = re.match(r'^---\r?\n(.*?)\r?\n---\r?\n', t, re.S)
    body = t[m.end():] if m else t
    lines = [l for l in body.split('\n') if l.strip()]
    print('━' * 100)
    print('◆', f)
    for l in lines[6:34]:
        print('   ', l[:110])
    print()
