# -*- coding: utf-8 -*-
"""
2026-08-31 题库格式批量修复（质量审计 B 组）
  1. 中文夹半角标点：中文,中文 / 中文;中文 / 中文:中文 / 中文!中文 / 中文?中文 → 全角
  2. 全角空格 \u3000 → 半角空格
安全策略：跳过 ``` 代码块；只处理题目类文件（type=题目/真题/例题）；写盘前备份已在 09-审计报告/备份/质量修正-2026-08-31 完成。
输出：修改清单 JSON + 控制台统计。
用法：python fix_question_format.py
"""
import re, json, sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
import audit_question_bank as A

VAULT = A.VAULT
OUT_JSON = VAULT / "09-审计报告" / "缓存-格式修复清单.json"
QUESTION_TYPES = {"题目", "真题", "例题"}
SKIP_DIR_PARTS = {".obsidian", ".git", "node_modules", "__pycache__", ".chem_media"}

# 中文夹半角标点（前、后均为中文）
CN_SEMI_RE = re.compile(r"([\u4e00-\u9fff])([,;:!?])([\u4e00-\u9fff])")
HALF_TO_FULL = {",": "，", ";": "；", ":": "：", "!": "！", "?": "？"}
FW_SPACE_RE = re.compile(r"\u3000")


def fix_text(text: str):
    """返回 (新文本, 统计dict)。跳过代码块。"""
    stats = {"cn_semi": 0, "fw_space": 0}
    out_lines = []
    in_code = False
    for line in text.splitlines(keepends=True):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            out_lines.append(line)
            continue
        if in_code:
            out_lines.append(line)
            continue
        new_line = line
        if CN_SEMI_RE.search(new_line):
            def rep(m):
                return m.group(1) + HALF_TO_FULL[m.group(2)] + m.group(3)
            new_line = CN_SEMI_RE.sub(rep, new_line)
            stats["cn_semi"] += 1
        if FW_SPACE_RE.search(new_line):
            new_line = FW_SPACE_RE.sub(" ", new_line)
            stats["fw_space"] += 1
        out_lines.append(new_line)
    return "".join(out_lines), stats


def write_with_retry(p: Path, text: str, max_try=4):
    for i in range(max_try):
        try:
            p.write_text(text, encoding="utf-8")
            return True
        except OSError as e:
            if i == max_try - 1:
                return False
            import time
            time.sleep(0.6)


def main():
    files = []
    for root in ("04-题库", "05-真题库"):
        base = VAULT / root
        for p in sorted(base.rglob("*.md")):
            rel = p.relative_to(VAULT).as_posix()
            if any(sp in rel for sp in SKIP_DIR_PARTS):
                continue
            files.append(p)
    changed = []
    failed = []
    total = {"cn_semi": 0, "fw_space": 0, "files": 0}
    for p in files:
        raw = p.read_text(encoding="utf-8")
        fm, body = A.strip_fm(raw)
        ftype = str(fm.get("type", "")).strip()
        if ftype not in QUESTION_TYPES:
            continue
        new_text, stats = fix_text(raw)
        if stats["cn_semi"] or stats["fw_space"]:
            if write_with_retry(p, new_text):
                changed.append({"rel": p.relative_to(VAULT).as_posix(),
                                "cn_semi": stats["cn_semi"], "fw_space": stats["fw_space"]})
                total["cn_semi"] += stats["cn_semi"]
                total["fw_space"] += stats["fw_space"]
                total["files"] += 1
            else:
                failed.append(p.relative_to(VAULT).as_posix())
    OUT_JSON.write_text(json.dumps({"total": total, "changed": changed, "failed": failed}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"修改文件数: {total['files']} | 中文夹半角标点: {total['cn_semi']} | 全角空格: {total['fw_space']} | 失败: {len(failed)}")
    if failed:
        print("失败文件:", failed[:10])
    print("→", OUT_JSON)


if __name__ == "__main__":
    main()
