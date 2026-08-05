# -*- coding: utf-8 -*-
"""媒体仓库备份工具 (2026-08-04)

背景: `媒体仓库/` 是极净图库的物理仓 (~17k 文件 / ~240MB), 位于 vault 根目录（Obsidian 可索引）,
被 gitignore, 不受版本控制。本工具提供两层保护:
  1. Manifest (默认): 生成 `10-索引与统计/媒体仓库清单.json`, 记录每个文件的
     相对路径/大小/修改时间 —— 资产目录可随时审计、可在仓库级 git 跟踪。
  2. Zip 备份 (--zip): 将 `媒体仓库/` 打包到 `09-审计报告/备份/media-backup-<时间戳>.zip`
     —— 字节级完整备份。

用法:
  python scripts/backup_media.py            # 仅生成 manifest
  python scripts/backup_media.py --zip      # manifest + zip 备份
"""
import os
import json
import sys
import time
import zipfile

vault_root = r'C:\Obsidion\妙妙屋'
media_dir = os.path.join(vault_root, '媒体仓库')
manifest_out = os.path.join(vault_root, '10-索引与统计', '媒体仓库清单.json')
backup_dir = os.path.join(vault_root, '09-审计报告', '备份')


def main():
    do_zip = '--zip' in sys.argv

    if not os.path.isdir(media_dir):
        print(f"[ERR] media dir not found: {media_dir}")
        sys.exit(1)

    entries = []
    total_size = 0
    for root, _, files in os.walk(media_dir):
        for fn in files:
            full = os.path.join(root, fn)
            rel = os.path.relpath(full, media_dir).replace('\\', '/')
            st = os.stat(full)
            entries.append({
                'name': fn,
                'path': rel,
                'size': st.st_size,
                'mtime': int(st.st_mtime),
            })
            total_size += st.st_size

    entries.sort(key=lambda e: e['path'])
    manifest = {
        'generated': time.strftime('%Y-%m-%d %H:%M:%S'),
        'media_dir': '媒体仓库',
        'file_count': len(entries),
        'total_bytes': total_size,
        'files': entries,
    }
    os.makedirs(os.path.dirname(manifest_out), exist_ok=True)
    with open(manifest_out, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)

    print(f"[manifest] {len(entries)} 文件 / {total_size/1048576:.1f} MB → {manifest_out}")

    if do_zip:
        os.makedirs(backup_dir, exist_ok=True)
        stamp = time.strftime('%Y%m%d-%H%M%S')
        zip_path = os.path.join(backup_dir, f'media-backup-{stamp}.zip')
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_STORED) as z:
            for e in entries:
                z.write(os.path.join(media_dir, e['path'].replace('/', os.sep)), arcname=e['path'])
        print(f"[zip] {zip_path} ({os.path.getsize(zip_path)/1048576:.1f} MB)")


if __name__ == '__main__':
    main()
