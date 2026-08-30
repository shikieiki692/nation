import argparse
import io
import os
import re
import sys
from pathlib import Path

_stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stdout = _stdout

VAULT_ROOT = Path(__file__).resolve().parents[2]
MEDIA_ROOT_DEFAULT = VAULT_ROOT / "媒体仓库"
HASH_NAME_RE = re.compile(r"[0-9a-fA-F]{64}\.[A-Za-z0-9]+")

"""校验生成结果：题头数 = question_count = 答案 details 数，图片嵌入格式正确。"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".preview_build", help="习题书输出根目录")
    ap.add_argument("--media-root", default=str(MEDIA_ROOT_DEFAULT), help="媒体仓库根目录")
    ap.add_argument(
        "--edition", choices=["student", "teacher"], default=None,
        help="校验版本：student 要求无答案 details；teacher 要求答案块数=题数。默认读 frontmatter。",
    )
    args = ap.parse_args()
    root = os.path.abspath(args.root)
    if not os.path.isdir(root):
        raise SystemExit(f"输出目录不存在: {root}")
    media_root = os.path.abspath(args.media_root)
    if not os.path.isdir(media_root):
        raise SystemExit(f"媒体仓库不存在: {media_root}")
    edition_override = args.edition

    files = []
    for dirpath, _, fns in os.walk(root):
        for fn in fns:
            if fn.endswith(".md") and fn not in {"目录.md", "_未分类submodule统计.md"}:
                files.append(os.path.join(dirpath, fn))
    files.sort()

    errors = []
    total_questions = 0
    total_placeholders = 0
    total_embeds = 0
    total_hash_embeds = 0
    total_named_embeds = 0
    total_missing_embed_names = 0
    total_md_imgs = 0
    total_path_embeds = 0
    total_broken_embeds = 0
    total_broken_bang = 0

    for path in files:
        text = open(path, encoding="utf-8").read()
        rel = os.path.relpath(path, root).replace(os.sep, "/")
        fm = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        if not fm:
            errors.append(f"{rel}: 缺少 frontmatter")
            continue
        m = re.search(r"(?m)^question_count: (\d+)", fm.group(1))
        if not m:
            errors.append(f"{rel}: 缺少 question_count")
            continue
        fm_edition = (re.search(r"(?m)^edition: (\w+)", fm.group(1)) or [None, None])[1]
        if edition_override and fm_edition and fm_edition != edition_override:
            errors.append(f"{rel}: frontmatter edition={fm_edition} 与参数 edition={edition_override} 不一致")
        edition = edition_override or fm_edition or "teacher"
        if edition not in {"student", "teacher"}:
            errors.append(f"{rel}: edition 字段非法（{edition}）")
            edition = "teacher"
        declared = int(m.group(1))
        qheads = len(re.findall(r"(?m)^##\s+\d+\.\d+\b", text))
        details = len(re.findall(r"(?m)^<details>$", text))
        placeholders = text.count("（原书未提供解答）")
        embed_basenames = []
        hash_embeds = 0
        named_embeds = 0
        path_embeds = 0
        missing_names = set()
        broken_embeds = len(re.findall(r"!\[\[([^\]\n]*\n[^\]]*)\]\]", text))
        for raw_embed in re.findall(r"!\[\[([^\]\n]+)\]\]", text):
            target = raw_embed.strip().split("|", 1)[0].strip()
            base = os.path.basename(target.replace("\\", "/")).strip()
            if not base:
                continue
            if "/" in target or "\\" in target:
                path_embeds += 1
            embed_basenames.append(base)
            if HASH_NAME_RE.fullmatch(base):
                hash_embeds += 1
            else:
                named_embeds += 1
            if not os.path.isfile(os.path.join(media_root, base)):
                missing_names.add(base)
        embeds = len(embed_basenames)
        missing_embeds = len(missing_names)
        broken_bang = len(re.findall(r"!(?=[0-9a-fA-F]{64}\.[A-Za-z0-9]+)", text))
        md_imgs = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text)
        md_hash_imgs = [
            x for x in md_imgs
            if re.search(r"[0-9a-fA-F]{64}", os.path.basename(x.replace("\\", "/")))
        ]
        total_questions += declared
        total_placeholders += placeholders
        total_embeds += embeds
        total_hash_embeds += hash_embeds
        total_named_embeds += named_embeds
        total_missing_embed_names += missing_embeds
        total_md_imgs += len(md_imgs)
        total_path_embeds += path_embeds
        total_broken_embeds += broken_embeds
        total_broken_bang += broken_bang
        if declared != qheads:
            errors.append(f"{rel}: question_count={declared} 但题头={qheads}")
        if edition == "student":
            if details != 0:
                errors.append(f"{rel}: 学生版应无答案 details，实得 {details}")
            if "<summary>" in text:
                errors.append(f"{rel}: 学生版仍含 <summary> 答案入口")
        else:
            if qheads != details:
                errors.append(f"{rel}: 题头={qheads} 但 details={details}")
        if missing_embeds:
            sample = "、".join(sorted(missing_names)[:8])
            errors.append(f"{rel}: 媒体仓库缺失 {missing_embeds} 个图片（{sample}{'...' if missing_embeds > 8 else ''}）")
        if broken_bang:
            errors.append(f"{rel}: 仍有 {broken_bang} 个 !哈希.jpg 旧格式")
        if path_embeds:
            errors.append(f"{rel}: 仍有 {path_embeds} 个路径式 Obsidian 图片嵌入")
        if broken_embeds:
            errors.append(f"{rel}: 疑似 {broken_embeds} 个未闭合 Obsidian 图片嵌入")
        if md_hash_imgs:
            errors.append(f"{rel}: 仍有 {len(md_hash_imgs)} 个哈希 Markdown 图链未转换")

    print(f"文件数: {len(files)}")
    print(f"登记题数: {total_questions}")
    print(f"无解答占位: {total_placeholders}")
    print(f"答案 details 块: {sum(len(re.findall(r'(?m)^<details>$', open(path, encoding='utf-8').read())) for path in files)}")
    print(f"Obsidian 图片嵌入: {total_embeds}")
    print(f"  其中纯哈希嵌入: {total_hash_embeds}")
    print(f"  其中非哈希/路径嵌入: {total_named_embeds}")
    print(f"媒体仓库缺失图片(唯一): {total_missing_embed_names}")
    print(f"路径式嵌入: {total_path_embeds}")
    print(f"疑似未闭合嵌入: {total_broken_embeds}")
    print(f"残留 Markdown 图链: {total_md_imgs}（非哈希按原样保留）")
    print(f"残留 !哈希.jpg 旧格式: {total_broken_bang}")
    if errors:
        print("\n校验失败：")
        for e in errors:
            print(f"  {e}")
        raise SystemExit(1)
    print("\n校验通过：题头数、question_count 与版本答案规则一致。")


if __name__ == "__main__":
    main()
