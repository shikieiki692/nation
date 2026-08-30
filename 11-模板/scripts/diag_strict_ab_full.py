import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

OLD_ROOT = r"C:\Obsidion\妙妙屋\04-课件\习题集\习题书-教师版"
NEW_ROOT = r"C:\Obsidion\妙妙屋\.tmp-strict-book\04-课件\习题集\习题书-教师版"

TEACH = re.compile(
    r"(?:小问关联|得分点|关联 KP|读题定位|关键转换|计算要点"
    r"|易错分析|解题思路|相关图片|知识点映射|错误表|课堂提问表)"
)
IMG = re.compile(r"!\[\[([0-9a-fA-F]{64}\.[A-Za-z0-9]+)\]\]")
HEAD = re.compile(r"^##\s+\d+\.\d+", re.M)
DETAILS = re.compile(r"<details>")


def stats(path):
    text = open(path, encoding="utf-8", errors="replace").read()
    imgs = IMG.findall(text)
    return {
        "heads": len(HEAD.findall(text)),
        "answers": len(DETAILS.findall(text)),
        "images": len(imgs),
        "unique_images": len(set(imgs)),
        "teaching": len(TEACH.findall(text)),
        "lines": len(text.splitlines()),
    }


def chapter_files(root):
    out = {}
    for dirpath, _, files in os.walk(root):
        for fn in files:
            if not fn.endswith(".md") or fn in {"目录.md", "_未分类submodule统计.md"}:
                continue
            rel = os.path.relpath(os.path.join(dirpath, fn), root)
            out[rel] = os.path.join(dirpath, fn)
    return out


old_files = chapter_files(OLD_ROOT)
new_files = chapter_files(NEW_ROOT)

totals = {k: 0 for k in ("heads", "answers", "images", "unique_images", "teaching", "lines")}
deltas = {k: 0 for k in ("heads", "answers", "images", "unique_images", "teaching", "lines")}

print(f"{'章节':<42}{'题头 旧→新':<12}{'答案 旧→新':<12}{'图 旧→新':<12}"
      f"{'唯一图 旧→新':<14}{'教学命中 旧→新':<15}{'行数 旧→新':<12}")
for rel in sorted(old_files):
    if rel not in new_files:
        print(f"{rel:<42} 新版本缺失")
        continue
    a = stats(old_files[rel])
    b = stats(new_files[rel])
    flag = ""
    for k in ("heads", "answers", "images", "unique_images", "teaching"):
        if a[k] != b[k]:
            flag += f" {k}!"
    print(f"{rel:<42}{a['heads']}→{b['heads']:<9}{a['answers']}→{b['answers']:<9}"
          f"{a['images']}→{b['images']:<9}{a['unique_images']}→{b['unique_images']:<11}"
          f"{a['teaching']}→{b['teaching']:<12}{a['lines']}→{b['lines']}{flag}")
    for k in totals:
        totals[k] += b[k]
        deltas[k] += b[k] - a[k]

print("\n合计（新版）:", totals)
print("合计增量:", deltas)
