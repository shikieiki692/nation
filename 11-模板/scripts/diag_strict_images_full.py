import io
import os
import re
import sys
from collections import Counter, defaultdict

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

OLD_ROOT = r"C:\Obsidion\妙妙屋\04-课件\习题集\习题书-教师版"
NEW_ROOT = r"C:\Obsidion\妙妙屋\.tmp-strict-book\04-课件\习题集\习题书-教师版"
SOURCE_ROOT = r"C:\Obsidion\妙妙屋\04-题库"

IMG = re.compile(r"!\[\[([0-9a-fA-F]{64}\.[A-Za-z0-9]+)\]\]")
HEADING = re.compile(r"^#{1,6}[ \t]*(.*)$")
TEACHING_HEADING = re.compile(
    r"^(?:解题思路|知识点映射|易错分析|相关图片|题目图示与结构参考|知识扩展|知识拓展"
    r"|方法点拨|思路点拨|关联知识点|易错点|常见错误|小问关联|得分点|读题定位|关键转换|计算要点)"
)
ANSWER_HEADING = re.compile(r"^(?:参考答案|参考解答|答案|解答|解析)")
QUESTION_HEADING = re.compile(r"^#{1,6}[ \t]*(?:题目|题)\b|^#{1,6}[ \t]*\d+")


def imgs_in(path):
    if not os.path.isfile(path):
        return set()
    return set(IMG.findall(open(path, encoding="utf-8", errors="replace").read()))


def chapter_files(root):
    out = []
    for dirpath, _, files in os.walk(root):
        for fn in files:
            if not fn.endswith(".md") or fn in ("目录.md", "_未分类submodule统计.md"):
                continue
            rel = os.path.relpath(os.path.join(dirpath, fn), root)
            out.append(rel)
    return sorted(out)


def classify_source(hash_name, source_index):
    """返回该哈希在源库中全部出现位置的归属信息。"""
    hits = []
    for rel, text in source_index:
        if hash_name not in text:
            continue
        lines = text.splitlines()
        for i, line in enumerate(lines):
            if hash_name not in line:
                continue
            section = "other"
            answer_seen = False
            for j in range(i, -1, -1):
                m = HEADING.match(lines[j])
                if not m:
                    continue
                title = m.group(1).strip()
                if TEACHING_HEADING.match(title):
                    section = "teaching"
                elif ANSWER_HEADING.match(title):
                    section = "answer"
                    answer_seen = True
                elif QUESTION_HEADING.match(title) or title.startswith("题目"):
                    section = "question"
                break
            # 没有标题时按答案/题目先后粗分
            if section == "other":
                prefix = "\n".join(lines[: i + 1])
                if re.search(r"##[ \t]+参考答案|##[ \t]+答案|##[ \t]+解答|##[ \t]+解析", prefix):
                    section = "answer_after"
                elif re.search(r"##[ \t]+题目", prefix):
                    section = "question_after"
            flags = []
            if line.lstrip().startswith("|") or ("|" in line and hash_name in line):
                flags.append("in_table")
            if len(IMG.findall(line)) > 1:
                flags.append("multi_image")
            if re.search(r"-{3,}\s*!\[\[", line):
                flags.append("glued_separator")
            if re.search(r"^#{1,6}", line):
                flags.append("heading_glue")
            text_parts = [p for p in re.split(r"!\[\[[^\]]+\]\]", line) if p.strip()]
            if text_parts:
                flags.append("same_line_text")
            hits.append((rel, i + 1, section, ",".join(flags) or "-", line.strip()[:80]))
    return hits


def main():
    print("建立源库索引...")
    source_index = []
    for root, _, files in os.walk(SOURCE_ROOT):
        for fn in files:
            if not fn.endswith(".md"):
                continue
            p = os.path.join(root, fn)
            rel = os.path.relpath(p, SOURCE_ROOT)
            source_index.append((rel, open(p, encoding="utf-8", errors="replace").read()))
    print(f"源文件数: {len(source_index)}")

    bucket_totals = Counter()
    flag_totals = Counter()
    detail_rows = []
    chapter_summary = []

    for rel in chapter_files(OLD_ROOT):
        new_path = os.path.join(NEW_ROOT, rel)
        old_path = os.path.join(OLD_ROOT, rel)
        old = imgs_in(old_path)
        new = imgs_in(new_path)
        removed = sorted(old - new)
        if not removed:
            continue
        rows = []
        for h in removed:
            hits = classify_source(h, source_index)
            if not hits:
                hits = [("NOT FOUND", 0, "other", "-", "")]
            buckets = Counter(x[2] for x in hits)
            flags = Counter()
            for x in hits:
                for f in x[3].split(","):
                    if f and f != "-":
                        flags[f] += 1
            for b, c in buckets.items():
                bucket_totals[b] += c
            for f, c in flags.items():
                flag_totals[f] += c
            sample = " | ".join(f"{x[0]}:{x[1]} [{x[2]}] {x[4]}" for x in hits[:2])
            rows.append((h, buckets, sample))
            detail_rows.append((rel, h, dict(buckets), sample))
        chapter_summary.append((rel, len(old), len(new), len(removed), rows))

    print(f"\n{'章节':<52}{'旧图':<6}{'新图':<6}{'删图':<6}")
    for rel, old_n, new_n, rm_n, rows in chapter_summary:
        print(f"{rel:<52}{old_n:<6}{new_n:<6}{rm_n:<6}")

    print("\n=== 删除图片归属（bucket 计数，按出现位置统计）===")
    for b, c in bucket_totals.most_common():
        print(f"  {b}: {c}")
    print("\n=== 高风险行标记 ===")
    for f, c in flag_totals.most_common():
        print(f"  {f}: {c}")

    print("\n=== 每张被删图片明细 ===")
    for rel, h, buckets, sample in detail_rows:
        print(f"\n[{rel}] {h[:24]}")
        print(f"  归属: {buckets}")
        print(f"  {sample}")


if __name__ == "__main__":
    main()
