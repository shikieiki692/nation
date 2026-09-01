"""
清理 knowledge_points 字段中的「非术语值」。
分行匹配，更简单可靠。
"""
import os, re, sys, json
import yaml

VAULT = r"C:\Obsidion\妙妙屋"
BAD_VALUES = {
    "综合分析", "待人工标定", "填空题", "简答题", "计算题",
    "选择题", "判断题", "单选题", "多选题", "实验题", "论述题", "证明题",
    "例题", "习题",
}

LIST_ITEM = re.compile(r'"?\[\[([^\]]+)\]\]"?')
FM_KP_LINE = re.compile(r'^knowledge_points:\s*(\[[^\n]*\]?)\s*$')
# 行的实际行尾（保留）


def remove_bad_from_kp(kp_text: str, bad: set):
    items = LIST_ITEM.findall(kp_text)
    if not items:
        return kp_text, 0, []
    kept, removed = [], []
    for it in items:
        if it.strip() in bad:
            removed.append(it)
        else:
            kept.append(it)
    if not removed:
        return kp_text, 0, []
    new = "[]" if not kept else "[" + ", ".join(f'"[[{x}]]"' for x in kept) + "]"
    return new, len(removed), removed


def process_file(rel: str, bad: set) -> tuple[bool, str, int]:
    abs_p = os.path.join(VAULT, rel)
    if not os.path.exists(abs_p):
        return False, "missing", 0

    with open(abs_p, encoding="utf-8", newline="") as f:
        text = f.read()

    # 用 splitlines(keepends=True) 同时处理 \r\n / \n / \r 三种行尾
    lines = text.splitlines(keepends=True)

    changed = 0
    removed_total = 0
    new_lines = []
    for ln in lines:
        # 去掉行尾以便匹配
        stripped = ln.rstrip("\r\n")
        m = FM_KP_LINE.match(stripped)
        if m and "knowledge_points" in stripped:
            kp_old = m.group(1)
            items = LIST_ITEM.findall(kp_old)
            if any(it.strip() in bad for it in items):
                kp_new, n_removed, _ = remove_bad_from_kp(kp_old, bad)
                if n_removed > 0:
                    # 提取原行尾（保留）
                    line_eol = ln[len(stripped):]
                    prefix = stripped[: stripped.index("[")]
                    new_ln = prefix + kp_new + line_eol
                    new_lines.append(new_ln)
                    changed += 1
                    removed_total += n_removed
                    continue
        new_lines.append(ln)

    if changed == 0:
        return False, "no change needed", 0

    new_text = "".join(new_lines)

    # 安全性断言：YAML 仍合法
    end = new_text.find("\n---", 3)
    if end == -1:
        return False, "no fm end", 0
    try:
        d = yaml.safe_load(new_text[3:end])
        if not isinstance(d, dict) or not isinstance(d.get("knowledge_points"), list):
            return False, "fm structure broken", 0
    except Exception as e:
        return False, f"yaml fail: {e}", 0

    with open(abs_p, "w", encoding="utf-8", newline="") as f:
        f.write(new_text)
    return True, f"removed {removed_total}", removed_total


def main():
    data = json.load(open(rf"{VAULT}\.workbuddy\tmp\fm_redlinks.json", encoding="utf-8"))
    files = set()
    for t, fs in data["where"].items():
        if t in BAD_VALUES:
            for f in fs:
                files.add(f)
    print(f"候选文件: {len(files)} 个")
    print(f"目标非术语值: {len(BAD_VALUES)} 个")
    print()

    n_changed = 0
    n_removed_total = 0
    fails = []
    for rel in sorted(files):
        ok, info, n = process_file(rel, BAD_VALUES)
        if ok:
            n_changed += 1
            n_removed_total += n
            print(f"  [OK]  {n:2d}  {rel}")
        elif info != "no change needed":
            fails.append((rel, info))
            print(f"  [FAIL] {rel}  ({info})")

    print()
    print(f"成功: {n_changed} 文件 / 移除 {n_removed_total} 项")
    if fails:
        print(f"失败: {len(fails)}")
        for f, i in fails: print(f"  - {f}  ({i})")


if __name__ == "__main__":
    main()
