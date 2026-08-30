import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

OLD_ROOT = r"C:\Obsidion\妙妙屋\04-课件\习题集\习题书-教师版"
NEW_ROOT = r"C:\Obsidion\妙妙屋\.tmp-strict-book\04-课件\习题集\习题书-教师版"
SOURCE_ROOT = r"C:\Obsidion\妙妙屋\04-题库"

CHAPTERS = [
    ("第一篇-化学原理", "1-热力学.md"),
    ("第二篇-结构化学", "3-晶体结构.md"),
    ("第三篇-有机化学", "2-立体化学.md"),
]
IMG = re.compile(r"!\[\[([0-9a-fA-F]{64}\.[A-Za-z0-9]+)\]\]")
QHEAD = re.compile(r"^##\s+(\d+\.\d+)\s+", re.M)
SRC_IMG = re.compile(r"!\[\[([0-9a-fA-F]{64}\.[A-Za-z0-9]+)\]\]")


def imgs_in(path):
    if not os.path.isfile(path):
        return set()
    return set(IMG.findall(open(path, encoding="utf-8", errors="replace").read()))


def source_buckets(module, chapter, hashes):
    # 只对缺失图做源文件定位，按“答案区/题目区/教学块”粗分。
    buckets = {}
    for root, _, files in os.walk(SOURCE_ROOT):
        for fn in files:
            if not fn.endswith(".md"):
                continue
            p = os.path.join(root, fn)
            text = open(p, encoding="utf-8", errors="replace").read()
            found = SRC_IMG.findall(text)
            for h in found:
                if h not in hashes:
                    continue
                lines = text.splitlines()
                line_no = next((i + 1 for i, l in enumerate(lines) if h in l), 0)
                before = "\n".join(lines[max(0, line_no - 8):line_no])
                if re.search(r"参考答案|参考解答|解答|解析", before[-600:]):
                    bucket = "answer"
                elif re.search(r"解题思路|知识点映射|易错分析|相关图片|题目图示与结构参考", before[-600:]):
                    bucket = "teaching"
                else:
                    bucket = "question"
                buckets.setdefault(h, set()).add(bucket)
    return buckets


def debug_locate(hashes):
    found = {}
    for root, _, files in os.walk(SOURCE_ROOT):
        for fn in files:
            if not fn.endswith(".md"):
                continue
            p = os.path.join(root, fn)
            text = open(p, encoding="utf-8", errors="replace").read()
            for h in hashes:
                if h in text:
                    found.setdefault(h, []).append(os.path.relpath(p, SOURCE_ROOT))
    for h in sorted(hashes):
        print(f"  {h[:24]} -> {found.get(h, ['NOT FOUND'])[:3]}")


for folder, fn in CHAPTERS:
    old = imgs_in(os.path.join(OLD_ROOT, folder, fn))
    new = imgs_in(os.path.join(NEW_ROOT, folder, fn))
    removed = old - new
    added = new - old
    print(f"\n{folder}/{fn}: old={len(old)} new={len(new)} removed={len(removed)} added={len(added)}")
    if not removed:
        continue
    buckets = source_buckets(folder, fn, removed)
    debug_locate(removed)
