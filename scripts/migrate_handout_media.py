# -*- coding: utf-8 -*-
"""讲义在用图迁移脚本 (2026-08-04)

把编译集讲义（超级充实/基础版）引用的 `![[media/xxx.jpg]]` 图片,
以 SHA-256 内容哈希名复制进 `.obsidian/media/`, 并把讲义引用改写为 `![[<hash>.jpg]]`,
使现役讲义脱离对旧 `media/` 的硬依赖 (双轨归一)。

安全设计:
- 默认 DRY-RUN, 仅报告; 加 `--apply` 才实际复制与改写。
- 保留宽度别名 `|420`。
- 保留原文件行尾 (CRLF/LF)。
- SVG 边角不迁移 (管线 SVG→PNG 逻辑依赖原路径), 仅记录。
- 同一内容不同旧名 → 同一哈希, 自动去重 (检测 .obsidian/media 已存在则复用)。
- 输出映射表到 10-索引与统计/讲义media迁移映射.json。

用法: python scripts/migrate_handout_media.py [--apply]
"""
import os
import re
import json
import hashlib
import shutil
import sys

vault_root = r'C:\Obsidion\妙妙屋'
handout_dir = os.path.join(vault_root, '04-课件', '学生讲义')
old_media = os.path.join(vault_root, 'media')
new_media = os.path.join(vault_root, '媒体仓库')
mapping_out = os.path.join(vault_root, '10-索引与统计', '讲义media迁移映射.json')

IMG_REF = re.compile(
    r'!\[\[media/([^\]\|\n]+?\.(?:jpg|jpeg|png|gif|webp))(\|[^\]]*)?\]\]',
    re.IGNORECASE,
)


def is_compiled(name: str) -> bool:
    return name.endswith('.md') and ('超级充实' in name or '基础版' in name)


def main():
    apply = '--apply' in sys.argv

    # 1) gather refs from compiled handouts
    ref_files = {}  # oldname -> set(files)
    for fn in os.listdir(handout_dir):
        if not is_compiled(fn):
            continue
        fp = os.path.join(handout_dir, fn)
        with open(fp, encoding='utf-8', newline='') as f:
            text = f.read()
        for m in IMG_REF.finditer(text):
            ref_files.setdefault(m.group(1), set()).add(fp)

    print(f"编译集讲义唯一 media/ 引用文件: {len(ref_files)}")
    if not ref_files:
        print("没有需要迁移的引用。")
        return

    # 2) build mapping + copy
    mapping = {}
    copied = reused = svg_skip = 0
    missing = []
    for name in sorted(ref_files):
        if name.lower().endswith('.svg'):
            svg_skip += 1
            mapping[name] = {'hash': None, 'status': 'svg-skip'}
            continue
        src = os.path.join(old_media, name)
        if not os.path.exists(src):
            missing.append(name)
            mapping[name] = {'hash': None, 'status': 'missing-src'}
            continue
        with open(src, 'rb') as f:
            digest = hashlib.sha256(f.read()).hexdigest()
        ext = os.path.splitext(name)[1].lower()
        hashname = digest + ext
        dst = os.path.join(new_media, hashname)
        if os.path.exists(dst):
            reused += 1
        elif apply:
            shutil.copy2(src, dst)
            copied += 1
        else:
            copied += 1  # would-copy
        mapping[name] = {'hash': hashname, 'status': 'ok'}

    print(f"迁移计划: 复制 {copied} · 复用已存在 {reused} · SVG跳过 {svg_skip} · 源缺失 {len(missing)}")
    for m in missing:
        print(f"  [MISS] {m}")

    # 3) rewrite refs
    rewritten = {}
    total = 0
    for fn in sorted(os.listdir(handout_dir)):
        if not is_compiled(fn):
            continue
        fp = os.path.join(handout_dir, fn)
        with open(fp, encoding='utf-8', newline='') as f:
            text = f.read()

        def repl(m):
            name = m.group(1)
            alias = m.group(2) or ''
            h = mapping.get(name, {}).get('hash')
            if not h:
                return m.group(0)
            return f'![[{h}{alias}]]'

        new_text, n = IMG_REF.subn(repl, text)
        if n:
            rewritten[fn] = n
            total += n
            if apply:
                with open(fp, 'w', encoding='utf-8', newline='') as f:
                    f.write(new_text)

    print(f"改写: 文件 {len(rewritten)} 个 · 引用 {total} 处")
    if not apply:
        print("\n⚠️ DRY-RUN: 未写入任何文件。加 --apply 执行。")
        for fn, n in sorted(rewritten.items()):
            print(f"    {fn}: {n} refs")
        return

    # 4) save mapping + summary
    summary = {
        'built_at': '2026-08-04',
        'unique_sources': len(ref_files),
        'copied': copied,
        'reused': reused,
        'svg_skip': svg_skip,
        'missing_src': missing,
        'rewritten_files': len(rewritten),
        'refs_replaced': total,
        'mapping': mapping,
    }
    with open(mapping_out, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 完成。映射表: 10-索引与统计/讲义media迁移映射.json")


if __name__ == '__main__':
    main()
