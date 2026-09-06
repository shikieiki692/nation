# -*- coding: utf-8 -*-
"""汇智缺题处置：
A. 转录笔误类 → 改指正确目标（题1→1、题011→001）
B. 真缺题（分子结构-36、晶体结构-65/73）→ 从 cross_references 移除无效引用
备份后写回。"""
import re
import sys
import time
from pathlib import Path

VAULT = Path(__file__).resolve().parents[2]
BACKUP = VAULT / '09-审计报告' / '备份' / '质量修正-2026-08-31' / '汇智缺题处置'

HZ = '04-题库/教材习题/汇智竞赛题目'
CJ = '04-题库/教材习题/化学竞赛初赛讲义'

# A. 笔误改指：(文件, 旧链接片段, 新链接片段)
A_FIXES = [
    (f'{HZ}/题-汇智-分子结构-1.md', '题-汇智-分子结构-题1', '题-汇智-分子结构-1'),
    (f'{HZ}/题-汇智-分子结构-12.md', '题-汇智-分子结构-题1', '题-汇智-分子结构-1'),
    (f'{HZ}/题-汇智-晶体结构-1.md', '题-汇智-晶体结构-题7', '题-汇智-晶体结构-7'),
    (f'{HZ}/题-汇智-晶体结构-1.md', '题-汇智-晶体结构-题4', '题-汇智-晶体结构-4'),
    (f'{HZ}/题-汇智-晶体结构-1.md', '题-汇智-晶体结构-题3', '题-汇智-晶体结构-3'),
    (f'{HZ}/题-汇智-原子结构-3.md', '题-011-初赛讲义-分子结构-习题3.44', '题-001-初赛讲义-分子结构-习题3.44'),
    (f'{HZ}/题-汇智-原子结构-15.md', '题-011-初赛讲义-分子结构-习题3.44', '题-001-初赛讲义-分子结构-习题3.44'),
    (f'{HZ}/题-汇智-原子结构-18.md', '题-011-初赛讲义-分子结构-习题3.44', '题-001-初赛讲义-分子结构-习题3.44'),
]

# B. 真缺题移除：(文件, 目标链接片段)
B_REMOVE = [
    (f'{HZ}/题-汇智-分子结构-4.md', '题-汇智-分子结构-36'),
    (f'{HZ}/题-汇智-分子结构-8.md', '题-汇智-分子结构-36'),
    (f'{HZ}/题-汇智-分子结构-10.md', '题-汇智-分子结构-36'),
    (f'{HZ}/题-汇智-分子结构-16.md', '题-汇智-分子结构-36'),
    (f'{HZ}/题-汇智-分子结构-17.md', '题-汇智-分子结构-36'),
    (f'{HZ}/题-汇智-晶体结构-14.md', '题-汇智-晶体结构-73'),
    (f'{HZ}/题-汇智-晶体结构-62.md', '题-汇智-晶体结构-73'),
    (f'{HZ}/题-汇智-晶体结构-15.md', '题-汇智-晶体结构-65'),
    (f'{HZ}/题-汇智-晶体结构-19.md', '题-汇智-晶体结构-65'),
]


def write_retry(path, text, tries=5):
    for i in range(tries):
        try:
            path.write_text(text, encoding='utf-8')
            return True
        except OSError:
            time.sleep(0.5 * (i + 1))
    return False


def main():
    dry = '--dry' in sys.argv
    # 按文件聚合：A 改指 + B 移除 都基于累计文本依次应用
    jobs = {}  # rel -> [(kind, old_or_tgt, new_or_None), ...]
    for rel, old, new in A_FIXES:
        jobs.setdefault(rel, []).append(('A', old, new))
    for rel, tgt in B_REMOVE:
        jobs.setdefault(rel, []).append(('B', tgt, None))

    touched = {}
    for rel, ops in sorted(jobs.items()):
        p = VAULT / rel
        if not p.exists():
            print(f'  ⚠️ 缺失: {rel}')
            continue
        cur = p.read_text(encoding='utf-8')
        descs = []
        for kind, old, new in ops:
            if kind == 'A':
                if old not in cur:
                    print(f'  ⚠️ 未找到 [{old}] in {rel}')
                    continue
                cur = cur.replace(old, new, 1)
                descs.append(f'改指 {old[-24:]}→{new[-24:]}')
            else:  # B 移除
                pat = re.compile(r'"\[\[[^"\]]*' + re.escape(old) + r'[^"\]]*\]\]"(,\s*)?|(,\s*)"\[\[[^"\]]*' + re.escape(old) + r'[^"\]]*\]\]"')
                cur, n = pat.subn(lambda m: '', cur)
                if n == 0:
                    print(f'  ⚠️ 未找到移除目标 [{old}] in {rel}')
                    continue
                descs.append(f'移除断链 {n} 处: {old}')
        if descs:
            touched[rel] = (p.read_text(encoding='utf-8'), cur, '；'.join(descs))
    if not touched:
        print('无可执行项')
        return
    for rel, (raw, new, desc) in sorted(touched.items()):
        if dry:
            print(f'  [dry] {rel}: {desc}')
            continue
        dst = BACKUP / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if not dst.exists():
            dst.write_bytes(raw.encode('utf-8'))
        if write_retry(VAULT / rel, new):
            print(f'  [写] {rel}: {desc}')
        else:
            print(f'  ❌ 写入失败: {rel}')
    print(f'共处理文件: {len(touched)}（dry={dry}）')


if __name__ == '__main__':
    main()
