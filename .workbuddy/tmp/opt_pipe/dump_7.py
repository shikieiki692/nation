# -*- coding: utf-8 -*-
"""7 张手写卡的内容速览（供写三字段）"""
import io, os, re
os.chdir(r'C:\Obsidion\妙妙屋')
D = '00-首页/活跃任务'
T = ['习题册制作-执行计划-2026-08-29.md', '交接-2026-09-15-备课线收尾核验.md',
     '任务卡-2026-09-11-讲义ASCII图转图片.md', '任务卡-2026-09-11-讲义等宽段治理.md',
     '任务卡-2026-09-13-git仓库膨胀治理.md', '任务卡-2026-09-14-习题书裸下标收口与git健壮性复核.md',
     '任务卡-2026-09-16-组题收口与两批新批次纳入.md', '任务卡-PPT制作方法探究与试点.md']
PATHRE = re.compile(r'(09-审计报告/[^\s`）)、，]+?\.md|00-首页/工作日志/\d{4}-\d{2}-\d{2}|11-模板/[^\s`）)、，]+?\.md)')
for f in T:
    t = io.open(os.path.join(D, f), encoding='utf-8-sig').read()
    m = re.match(r'^---\r?\n(.*?)\r?\n---\r?\n', t, re.S)
    s, b = (m.group(1), t[m.end():]) if m else ('', t)
    lines = [l for l in b.split('\n') if l.strip()]
    print('═' * 96)
    print('◆', f)
    for l in lines[:12]:
        print('   ', l[:110])
    paths = []
    for p in PATHRE.findall(t):
        if p not in paths:
            paths.append(p)
    print('   -- 引用路径:', paths[:6] or '—')
    print()
