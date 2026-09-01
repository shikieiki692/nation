# -*- coding: utf-8 -*-
"""路径式断链简单修复：
B. 化学式误当链接 → 去 [[ ]] 保留文本
A. 目录链接 → 改指 README
C. 概念名 → 改指已有近义 KP
备份后写回；纯文本替换保留 YAML 格式。"""
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, '11-模板/scripts')
import validate_kb as VKB

VAULT = Path(__file__).resolve().parents[2]  # 11-模板/scripts → 仓库根
BACKUP = VAULT / '09-审计报告' / '备份' / '质量修正-2026-08-31' / '路径式断链修复'

# (文件相对路径, 旧文本, 新文本)
FIXES = [
    # ---- B. 化学式/物质描述误当链接（去 [[ ]] 保留文本）----
    ('04-题库/教材习题/无机化学例题与习题/Ch21-铬副族和锰副族/习题/21.57-简答与计算题.md',
     '[[Cr₂O₇²⁻/Cr³⁺]]', 'Cr₂O₇²⁻/Cr³⁺'),
    ('04-题库/教材习题/无机化学例题与习题/Ch22-铁系元素和铂系元素/习题/22.24-22.40-配平方程式.md',
     '[[Cl2与Fe(OH)3/KOH]]', 'Cl2与Fe(OH)3/KOH'),
    ('04-题库/教材习题/无机化学例题与习题/Ch22-铁系元素和铂系元素/习题/22.24-22.40-配平方程式.md',
     '[[CoCl2与溴水/NaOH]]', 'CoCl2与溴水/NaOH'),
    ('04-题库/教材习题/无机化学例题与习题/Ch22-铁系元素和铂系元素/习题/22.24-22.40-配平方程式.md',
     '[[NiCl2与NaOH/溴水]]', 'NiCl2与NaOH/溴水'),
    ('04-题库/教材习题/无机化学例题与习题/Ch22-铁系元素和铂系元素/习题/22.47-22.55-简答题.md',
     '[[Fe(OH)3/Co(OH)3/Ni(OH)3与浓盐酸]]', 'Fe(OH)3/Co(OH)3/Ni(OH)3与浓盐酸'),
    ('04-题库/教材习题/无机化学例题与习题/Ch22-铁系元素和铂系元素/习题/22.47-22.55-简答题.md',
     '[[FeCl3与KSCN/铁粉]]', 'FeCl3与KSCN/铁粉'),
    ('04-题库/教材习题/无机化学例题与习题/Ch22-铁系元素和铂系元素/例题/例22.5-解释实验现象.md',
     '[[NaHCO3对Fe2+/Fe3+电势影响]]', 'NaHCO3对Fe2+/Fe3+电势影响'),
    # ---- A. 目录链接（改指习题集 README）----
    ('00-首页/活跃任务/习题册制作-执行计划-2026-08-29.md',
     '[[04-课件/习题集/习题书-教师版|习题书-教师版]]', '[[04-课件/习题集/README|习题书-教师版]]'),
    ('00-首页/活跃任务/习题册制作-执行计划-2026-08-29.md',
     '[[04-课件/习题集/习题书-学生版|习题书-学生版]]', '[[04-课件/习题集/README|习题书-学生版]]'),
    # ---- C. 概念名 → 改指已有近义 KP ----
    ('04-题库/有机化学/有机结构基础与电子效应/题-有机-结构-糖类D-L构型与环状结构.md',
     '[[D/L构型]]', '[[D-L构型]]'),
    ('04-题库/有机化学/有机结构基础与电子效应/题-有机-结构-糖类旋光性与变旋光现象.md',
     '[[D/L构型]]', '[[D-L构型]]'),
    ('04-题库/真题/第32届决赛/理论/题-032决-6-炔烃氢卤化.md',
     '[[Z/E构型]]', '[[有机分子的几何构型]]'),
    ('04-题库/真题/第38届初赛/题-038-10-埃索美拉唑构型.md',
     '[[E/Z构型]]', '[[有机分子的几何构型]]'),
    ('04-题库/真题/第25届初赛/无机和结构化学/题-025-7-金刚石晶胞键连.md',
     '[[椅式/船式]]', '[[构象分析]]'),
    ('04-题库/真题/第32届初赛/有机化学/题-032-8-SN反应类型判断.md',
     '[[苄基/烯丙基正离子]]', '[[碳正离子]]'),
    # 附带：同一文件的另一个断链名（非路径式但可顺手修）
    ('04-题库/真题/第29届决赛/理论/题-029决-1-有机硅与VSEPR.md',
     '[[Na/NH₃体系]]', 'Na/NH₃体系'),  # 无近义 KP，去包保留文本（避免断链）
]

def verify_targets():
    """校验改指目标可解析"""
    for _, old, new in FIXES:
        m = re.search(r'\[\[([^\]|]+)\]\]', new)
        if m:
            tgt = m.group(1)
            if not VKB.find_wikilink_target(tgt, VAULT):
                print(f'  ❌ 改指目标不可解析: {tgt} (from {new})')
                return False
    return True

def write_retry(path, text, tries=5):
    for i in range(tries):
        try:
            path.write_text(text, encoding='utf-8')
            return True
        except OSError as e:
            time.sleep(0.5 * (i + 1))
    return False

def main():
    dry = '--dry' in sys.argv
    if not verify_targets():
        sys.exit(1)
    by_file = {}
    for rel, old, new in FIXES:
        by_file.setdefault(rel, []).append((old, new))
    changed_files = 0
    for rel, pairs in sorted(by_file.items()):
        p = VAULT / rel
        if not p.exists():
            print(f'  ⚠️ 文件不存在: {rel}')
            continue
        raw = p.read_text(encoding='utf-8')
        new_text = raw
        for old, new in pairs:
            if old not in new_text:
                print(f'  ⚠️ 未找到 [{old[:40]}] in {rel}')
                continue
            new_text = new_text.replace(old, new, 1)
        if new_text != raw:
            if not dry:
                # 备份
                dst = BACKUP / rel
                dst.parent.mkdir(parents=True, exist_ok=True)
                if not dst.exists():
                    dst.write_bytes(raw.encode('utf-8'))
                if not write_retry(p, new_text):
                    print(f'  ❌ 写入失败: {rel}')
                    continue
            changed_files += 1
            print(f'  {"[dry]" if dry else "[写]"} {rel}: {len(pairs)} 处')
    print(f'共修改文件: {changed_files} / {len(by_file)}')

if __name__ == '__main__':
    main()
