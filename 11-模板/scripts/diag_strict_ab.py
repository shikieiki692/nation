import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

OLD_ROOT = r"C:\Obsidion\妙妙屋\04-课件\习题集\习题书-教师版"
NEW_ROOT = r"C:\Obsidion\妙妙屋\.tmp-strict-book\04-课件\习题集\习题书-教师版"

CHAPTERS = [
    ("第一篇-化学原理", "1-热力学.md"),
    ("第二篇-结构化学", "3-晶体结构.md"),
    ("第三篇-有机化学", "2-立体化学.md"),
]

TEACH = re.compile(r"(?:小问关联|得分点|关联 KP|读题定位|关键转换|计算要点"
                   r"|易错分析|解题思路|相关图片|知识点映射)")
IMG = re.compile(r"!\[\[([0-9a-fA-F]{64}\.[A-Za-z0-9]+)\]\]")
HEAD = re.compile(r"^##\s+\d+\.\d+", re.M)
DETAILS = re.compile(r"<details>")


def stats(path):
    if not os.path.isfile(path):
        return None
    text = open(path, encoding="utf-8", errors="replace").read()
    return {
        "heads": len(HEAD.findall(text)),
        "answers": len(DETAILS.findall(text)),
        "images": len(IMG.findall(text)),
        "teaching": len(TEACH.findall(text)),
        "lines": len(text.splitlines()),
    }


for folder, fn in CHAPTERS:
    old = stats(os.path.join(OLD_ROOT, folder, fn))
    new = stats(os.path.join(NEW_ROOT, folder, fn))
    if old is None or new is None:
        print(f"{folder}/{fn}: missing ({old is None}, {new is None})")
        continue
    print(f"{folder}/{fn}: 旧={old} 新={new}")
