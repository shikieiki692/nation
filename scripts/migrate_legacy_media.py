# -*- coding: utf-8 -*-
"""旧 media/ 引用全量迁移脚本 (2026-08-04, P1)

把 04-课件/学生讲义 下**所有** .md（含 _归档/_待升级/结构化学第一轮复习）中
依赖旧根目录 `media/` 的图片引用迁移到 `.obsidian/media/<sha256>.jpg`：

  1. `![[media/NAME.ext]]`            -> `![[<sha256>.ext]]`
  2. 无前缀旧引用 `![[NAME.ext]]`（NAME 存在于旧 media/ 且不在 .obsidian/media）-> `![[<sha256>.ext]]`

安全设计:
- 默认 DRY-RUN; 加 `--apply` 才写。
- 保留宽度别名 `|420`、CRLF。
- SVG 边角不迁移（管线 SVG→PNG 逻辑依赖原路径），仅记录。
- 源缺失/已哈希 引用保持不变。
用法: python scripts/migrate_legacy_media.py [--apply]
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

MEDIA_REF = re.compile(r'!\[\[media/([^\]\|\n]+?\.(?:jpg|jpeg|png|gif|webp))(\|[^\]]*)?\]\]', re.IGNORECASE)
# 无前缀图片引用（basename 无路径分隔符）
PLAIN_REF = re.compile(r'!\[\[([^\]\|\n/\\]+?\.(?:jpg|jpeg|png|gif|webp))(\|[^\]]*)?\]\]', re.IGNORECASE)


def sha256_copy(src, name):
    with open(src, 'rb') as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    ext = os.path.splitext(name)[1].lower()
    hashname = digest + ext
    dst = os.path.join(new_media, hashname)
    return hashname, dst


def main():
    apply = '--apply' in sys.argv
    # 旧 media/ 文件集合 + 新媒体集合
    old_files = set(os.listdir(old_media)) if os.path.isdir(old_media) else set()
    media_rec = set()
    for root, _, files in os.walk(new_media):
        for fn in files:
            media_rec.add(fn)

    touched = {}   # file -> n refs
    copied = reused = svg_skip = missing = 0
    missing_names = []

    for dirpath, _, files in os.walk(handout_dir):
        for fn in files:
            if not fn.endswith('.md'):
                continue
            fp = os.path.join(dirpath, fn)
            rel = os.path.relpath(fp, vault_root).replace('\\', '/')
            with open(fp, encoding='utf-8', newline='') as f:
                text = f.read()
            mapping = {}  # old basename -> hashname
            n_changes = 0

            def resolve(name, ext_marker):
                nonlocal copied, reused, svg_skip, missing
                if name.lower().endswith('.svg'):
                    svg_skip += 1
                    return None
                src = os.path.join(old_media, name)
                if not os.path.exists(src):
                    missing += 1
                    missing_names.append(name)
                    return None
                if name in mapping:
                    return mapping[name]
                hashname, dst = sha256_copy(src, name)
                if os.path.exists(dst):
                    reused += 1
                elif apply:
                    shutil.copy2(src, dst)
                    copied += 1
                else:
                    copied += 1
                mapping[name] = hashname
                return hashname

            def repl_media(m):
                nonlocal n_changes
                h = resolve(m.group(1), 'media')
                if not h:
                    return m.group(0)
                n_changes += 1
                return f'![[{h}{m.group(2) or ""}]]'

            def repl_plain(m):
                nonlocal n_changes
                name = m.group(1)
                # 已在 media 的哈希名不动；仅在旧 media/ 存在的旧名才迁移
                if name in media_rec:
                    return m.group(0)
                if name not in old_files:
                    return m.group(0)
                h = resolve(name, 'plain')
                if not h:
                    return m.group(0)
                n_changes += 1
                return f'![[{h}{m.group(2) or ""}]]'

            new_text = MEDIA_REF.sub(repl_media, text)
            new_text = PLAIN_REF.sub(repl_plain, new_text)
            if n_changes:
                touched[rel] = n_changes
                if apply:
                    with open(fp, 'w', encoding='utf-8', newline='') as f:
                        f.write(new_text)

    print(f"将迁移 {len(touched)} 个文件 · {sum(touched.values())} 处引用")
    print(f"复制 {copied} · 复用 {reused} · SVG跳过 {svg_skip} · 源缺失 {missing}")
    if not apply:
        print("\n⚠️ DRY-RUN。加 --apply 执行。")
        for rel, n in sorted(touched.items(), key=lambda x: -x[1]):
            print(f"    {n:3}  {rel}")
        return
    print(f"\n✅ 完成。")

    # 记录映射摘要
    summary = {
        'built_at': '2026-08-04',
        'files': len(touched),
        'refs': sum(touched.values()),
        'copied': copied,
        'reused': reused,
        'svg_skip': svg_skip,
        'missing_src': missing,
    }
    with open(os.path.join(vault_root, '10-索引与统计', '旧media迁移摘要.json'), 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main()
