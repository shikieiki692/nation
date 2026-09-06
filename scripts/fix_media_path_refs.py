# -*- coding: utf-8 -*-
"""media/ 路径式引用修复脚本 (2026-08-04)

把 `![[media/03-教材书籍/.../<hash>.<ext>]]` 这类路径式引用改为裸哈希 `![[<hash>.<ext>]]`，
前提是哈希文件已存在于 `媒体仓库/`（Obsidian 全库按文件名解析）。

安全设计:
- 默认 DRY-RUN; 加 `--apply` 才写。
- 只改 hash 在 `媒体仓库/` 存在的引用；不在的保留。
- 保留宽度别名 `|420`、CRLF/LF。
用法: python scripts/fix_media_path_refs.py [--apply]
"""
import os
import re
import json
import sys

VAULT = r'C:\Obsidion\妙妙屋'
WAREHOUSE = os.path.join(VAULT, '媒体仓库')
PATH_REF = re.compile(r'!\[\[media/([^\]\|\n]+?\.(?:jpg|jpeg|png|gif|webp|svg))(\|[^\]]*)?\]\]', re.IGNORECASE)


def main():
    apply = '--apply' in sys.argv
    wh = set(os.listdir(WAREHOUSE)) if os.path.isdir(WAREHOUSE) else set()
    changes = {}  # file -> [(old, new)]
    total = 0
    for root, _, files in os.walk(VAULT):
        if any(x in root for x in ['\\.git', '\\.obsidian', '\\.claude', 'node_modules', '\\.trash', '\\.kb', '09-审计报告\\备份']):
            continue
        for fn in files:
            if not fn.endswith('.md'):
                continue
            fp = os.path.join(root, fn)
            rel = os.path.relpath(fp, VAULT).replace('\\', '/')
            with open(fp, encoding='utf-8', errors='ignore', newline='') as f:
                text = f.read()
            new_text = text
            n = 0

            def repl(m):
                nonlocal n
                pathpart = m.group(1)
                alias = m.group(2) or ''
                if '/' not in pathpart:
                    return m.group(0)
                hashname = pathpart.split('/')[-1]
                if hashname not in wh:
                    return m.group(0)
                n += 1
                return f'![[{hashname}{alias}]]'

            new_text = PATH_REF.sub(repl, new_text)
            if n:
                changes[rel] = n
                total += n
                if apply:
                    with open(fp, 'w', encoding='utf-8', newline='') as f:
                        f.write(new_text)
    print(f"{'已修复' if apply else '待修复'}文件 {len(changes)} 个 · 引用 {total} 处")
    if not apply:
        print("\n⚠️ DRY-RUN。加 --apply 执行。")
        for rel, n in sorted(changes.items()):
            print(f"    {n:3}  {rel}")
    else:
        print("✅ 完成。")


if __name__ == '__main__':
    main()
