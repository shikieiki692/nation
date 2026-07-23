# -*- coding: utf-8 -*-
"""一次性口径统计脚本（批次4：状态口径校准）
只读扫描，打印实测数字到 stdout。兼容 BOM / CRLF / LF。
"""
import os
import re
import sys
from collections import Counter

VAULT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def read_head(path, n=4000):
    """读取文件头部（frontmatter 区域），兼容 BOM。"""
    try:
        with open(path, "rb") as f:
            raw = f.read(n)
        return raw.decode("utf-8-sig", errors="replace")
    except OSError:
        return ""


def fm_value(text, key):
    """从 frontmatter 提取 key 的值（只做行级简单解析）。"""
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    fm = text[3:end]
    m = re.search(rf"(?m)^\s*{re.escape(key)}\s*:\s*(.+?)\s*$", fm)
    return m.group(1) if m else None


def scan_dir(rel):
    root = os.path.join(VAULT, rel)
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for fn in filenames:
            if fn.lower().endswith(".md"):
                out.append(os.path.join(dirpath, fn))
    return out


def main():
    print(f"VAULT: {VAULT}")

    # ---------- 03-知识点 ----------
    kp = scan_dir("03-知识点")
    status_c = Counter()
    bucket_c = Counter()
    bucket_status = {}
    for p in kp:
        head = read_head(p)
        st = fm_value(head, "status") or "(无status字段)"
        status_c[st] += 1
        rel = os.path.relpath(p, os.path.join(VAULT, "03-知识点"))
        top = rel.split(os.sep)[0] if os.sep in rel else "(根目录)"
        bucket_c[top] += 1
        bucket_status.setdefault(top, Counter())[st] += 1
    print("\n===== 03-知识点 =====")
    print(f"md 总数: {len(kp)}")
    print("status 分布:")
    for k, v in status_c.most_common():
        print(f"  {k}: {v}")
    print("一级子目录分桶:")
    for k, v in sorted(bucket_c.items()):
        detail = ", ".join(f"{s}:{c}" for s, c in bucket_status[k].most_common())
        print(f"  {k}: {v}  [{detail}]")

    # ---------- 04-题库 ----------
    tk = scan_dir("04-题库")
    type_timu = 0
    tk_bucket = Counter()
    tk_bucket_timu = Counter()
    for p in tk:
        head = read_head(p)
        ty = fm_value(head, "type")
        is_t = (ty or "").strip().strip("'\"") == "题目"
        if is_t:
            type_timu += 1
        rel = os.path.relpath(p, os.path.join(VAULT, "04-题库"))
        parts = rel.split(os.sep)
        top = parts[0] if len(parts) > 1 else "(根目录)"
        tk_bucket[top] += 1
        if is_t:
            tk_bucket_timu[top] += 1
    print("\n===== 04-题库 =====")
    print(f"md 总数: {len(tk)}")
    print(f"type=题目: {type_timu}")
    print("一级子目录分桶 (md总数 / 其中type=题目):")
    for k, v in sorted(tk_bucket.items()):
        print(f"  {k}: {v} / {tk_bucket_timu.get(k, 0)}")

    # ---------- 04-专题与题型/专题 ----------
    zt = scan_dir(os.path.join("04-专题与题型", "专题"))
    zt_status = Counter()
    for p in zt:
        head = read_head(p)
        st = fm_value(head, "status") or "(无status字段)"
        zt_status[st] += 1
    print("\n===== 04-专题与题型/专题 =====")
    print(f"md 总数: {len(zt)}")
    print("status 分布:")
    for k, v in zt_status.most_common():
        print(f"  {k}: {v}")

    # ---------- 04-课件/学生讲义 ----------
    kj = scan_dir("04-课件")
    kj_stu = [p for p in kj if "学生讲义" in os.path.relpath(p, VAULT)]
    print("\n===== 04-课件 =====")
    print(f"md 总数: {len(kj)}")
    print(f"学生讲义 md 数: {len(kj_stu)}")

    # ---------- 全角（待填充）frontmatter 检查 ----------
    full_paren = []
    for base in ("03-知识点", "04-题库", "04-专题与题型"):
        for p in scan_dir(base):
            head = read_head(p)
            st = fm_value(head, "status")
            if st and "（待填充）" in st:
                full_paren.append((os.path.relpath(p, VAULT), st))
    print("\n===== frontmatter status=（待填充） =====")
    print(f"文件数: {len(full_paren)}")
    for rel, st in full_paren[:80]:
        print(f"  {rel}  ->  {st}")


if __name__ == "__main__":
    main()
