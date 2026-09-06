# -*- coding: utf-8 -*-
"""
03-知识点/高中化学基础 · P2 图片治理
  1) 把教材 OCR 来源仓的图复制到 媒体仓库/（哈希原名，源图保留不删）
  2) 引用改写：![图注](../../来源仓/x.jpg) -> ![[x.jpg|图注]]

依据：00-首页/规则-配图来源优先级.md 硬规则 1、4
      （OCR/来源仓只是来源；进入知识点页前复制到媒体仓库，引用写 ![[哈希名.jpg]]）

用法：
  python fix_gaozhong_p2.py            # 预演
  python fix_gaozhong_p2.py --apply    # 落盘（复制图片 + 改写引用）
"""
import os
import re
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8")

VAULT = r"C:\Obsidion\妙妙屋"
TARGET = os.path.join(VAULT, "03-知识点", "高中化学基础")
MEDIA = os.path.join(VAULT, "媒体仓库")

APPLY = "--apply" in sys.argv

IMG = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
# wikilink 别名里不能出现的字符
UNSAFE_ALIAS = re.compile(r"[|\[\]\n\r]")

copied = 0
skipped_same = 0
conflict = []  # 媒体仓库已存在但内容不同
missing = []
rewritten = 0
alias_dropped = 0
total_bytes = 0
touched = set()

for fn in sorted(os.listdir(TARGET)):
    if not fn.endswith(".md"):
        continue
    fp = os.path.join(TARGET, fn)
    src = open(fp, encoding="utf-8").read()

    def img_sub(mo):
        global copied, skipped_same, rewritten, alias_dropped, total_bytes
        alt, path = mo.group(1), mo.group(2).strip()
        if path.startswith(("http://", "https://", "data:")):
            return mo.group(0)

        abs_p = os.path.normpath(os.path.join(TARGET, path))
        if not os.path.isfile(abs_p):
            missing.append((fn, path))
            return mo.group(0)

        base = os.path.basename(abs_p)
        dst = os.path.join(MEDIA, base)

        if os.path.isfile(dst):
            if os.path.getsize(dst) == os.path.getsize(abs_p):
                skipped_same += 1
            else:
                conflict.append((fn, base, os.path.getsize(abs_p), os.path.getsize(dst)))
                return mo.group(0)  # 内容存疑，跳过不改写
        else:
            total_bytes += os.path.getsize(abs_p)
            if APPLY:
                shutil.copy2(abs_p, dst)
            copied += 1

        # 别名安全化
        a = alt.strip()
        if a and not UNSAFE_ALIAS.search(a):
            new = f"![[{base}|{a}]]"
        else:
            if a:
                alias_dropped += 1
            new = f"![[{base}]]"

        rewritten += 1
        return new

    out = IMG.sub(img_sub, src)
    if out != src:
        touched.add(fn)
        if APPLY:
            with open(fp, "w", encoding="utf-8", newline="") as fh:
                fh.write(out)

print("=" * 70)
print("P2 图片治理" + ("（已应用）" if APPLY else "（预演，未落盘）"))
print("=" * 70)
print(f"复制到媒体仓库  : {copied} 张（{total_bytes/1024/1024:.2f} MB）")
print(f"媒体仓库已有同图: {skipped_same} 张（跳过复制）")
print(f"引用改写        : {rewritten} 处，涉及 {len(touched)} 个文件")
print(f"别名被丢弃      : {alias_dropped} 处（含非法字符）")
print(f"内容冲突        : {len(conflict)} 张（未处理）")
print(f"源图缺失        : {len(missing)} 处")

if conflict:
    print("\n--- 内容冲突（媒体仓库已存在同名但大小不同，已跳过）---")
    for fn, b, s1, s2 in conflict:
        print(f"  {fn}  {b[:32]}...  源 {s1}B vs 仓 {s2}B")
if missing:
    print("\n--- 源图缺失 ---")
    for fn, p in missing:
        print(f"  {fn} -> {p[:80]}")
if not APPLY:
    print("\n（预演模式，加 --apply 落盘；源图一律保留不删）")
