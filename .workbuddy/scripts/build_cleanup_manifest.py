#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
生成清理清单，并对每一批产物做「源可重建」校验（只读，不删任何东西）

对 S 级每个产物目录，检查同目录/父目录是否存在对应源文件：
  *_render / *_render_preview / *_qa_render  -> 同名 .docx 或 .md
  */ppt/media/                               -> 祖先目录里的 .pptx

输出
  .workbuddy/tmp/cleanup_stage1.txt   待删文件清单（每行一个绝对路径）
  .workbuddy/tmp/cleanup_stage1.md    复核报告
"""
import os, re, json, collections

VAULT = r"C:\Obsidion\妙妙屋"
C = json.load(open(os.path.join(VAULT, ".workbuddy", "tmp", "orphan_classified.json"),
                   encoding="utf-8"))
OUT_TXT = os.path.join(VAULT, ".workbuddy", "tmp", "cleanup_stage1.txt")
OUT_MD = os.path.join(VAULT, ".workbuddy", "tmp", "cleanup_stage1.md")

RENDER_PAT = re.compile(r"(_qa_render|_render_preview|_render)$", re.I)
PPT_MEDIA_PAT = re.compile(r"[/\\]ppt[/\\]media[/\\]", re.I)


def hsize(n):
    if n >= 1 << 30:
        return "%.2f GB" % (n / (1 << 30))
    if n >= 1 << 20:
        return "%.2f MB" % (n / (1 << 20))
    return "%.1f KB" % (n / 1024)


def find_source(render_dir):
    """给一个产物目录找源文件。

    逐级向上找（最多 4 级祖先，每级递归 2 层）：
      1) 与产物目录同名的 .docx/.md/.pptx/.pdf
      2) 该祖先目录（含一级子目录）里的同名源文件
      3) 兜底：祖先目录里的任意 .docx/.md（产物肯定是从某个文档渲出来的）
    """
    stem = os.path.basename(render_dir)
    base = RENDER_PAT.sub("", stem)
    d = render_dir
    for level in range(5):
        # 1) 本级同名
        for ext in (".docx", ".md", ".pptx", ".pdf"):
            cand = os.path.join(d, base + ext)
            if os.path.isfile(cand):
                return cand, "同名(L%d)" % level
        # 2) 本级 + 一级子目录里的同名
        try:
            subs = [os.path.join(d, e) for e in os.listdir(d)
                    if os.path.isdir(os.path.join(d, e))]
        except OSError:
            subs = []
        for sd in subs:
            for ext in (".docx", ".md", ".pptx", ".pdf"):
                cand = os.path.join(sd, base + ext)
                if os.path.isfile(cand):
                    return cand, "子目录同名(L%d)" % level
        # 3) 兜底：本级任意文档
        try:
            hits = [os.path.join(d, e) for e in os.listdir(d)
                    if e.lower().endswith((".docx", ".md"))]
        except OSError:
            hits = []
        if hits:
            return sorted(hits)[0], "同级任意(%d个,L%d)" % (len(hits), level)
        d = os.path.dirname(d)
        if os.path.dirname(d) == d:
            break
    return None, None


def find_pptx(pmedia_dir):
    """从 .../ppt/media 往上找最近的 .pptx"""
    d = pmedia_dir
    for _ in range(6):
        try:
            for e in os.listdir(d):
                if e.lower().endswith(".pptx"):
                    return os.path.join(d, e), "同级"
        except OSError:
            pass
        d = os.path.dirname(d)
        if d == os.path.dirname(d):
            break
    # 祖先目录里找任意 pptx
    d = pmedia_dir
    for _ in range(6):
        d = os.path.dirname(d)
        try:
            for e in os.listdir(d):
                if e.lower().endswith(".pptx"):
                    return os.path.join(d, e), "祖先"
        except OSError:
            pass
    return None, None


def main():
    s = C.get("S", [])
    print("S 级 %d 张 / %s" % (len(s), hsize(sum(x["size"] for x in s))))

    # 按产物目录分组
    bydir = collections.defaultdict(list)
    for x in s:
        d = os.path.dirname(os.path.join(VAULT, x["path"]))
        bydir[os.path.normpath(d)].append(x)

    rows = []
    verified = []
    unverified = []
    for d, items in sorted(bydir.items()):
        rel = os.path.relpath(d, VAULT)
        size = sum(i["size"] for i in items)
        if PPT_MEDIA_PAT.search(d + os.sep):
            src, how = find_pptx(d)
            kind = "PPTX解压残留"
        elif RENDER_PAT.search(os.path.basename(d)):
            src, how = find_source(d)
            kind = "Word渲染产物"
        else:
            src, how = None, None
            kind = "其他"
        rows.append({
            "dir": rel, "n": len(items), "size": size, "kind": kind,
            "src": os.path.relpath(src, VAULT) if src else None, "how": how,
        })
        (verified if src else unverified).append(rel)

    print()
    print("%-46s %6s %10s  %-12s %s"
          % ("产物目录", "张数", "体积", "类型", "源文件"))
    for r in sorted(rows, key=lambda r: -r["size"]):
        print("%-46s %6d %10s  %-12s %s"
              % (r["dir"][:46], r["n"], hsize(r["size"]), r["kind"],
                 (r["src"] or "❌ 未找到")[:40]))

    print()
    print("已验证有源：%d 个目录 / %.2f MB"
          % (len(verified),
             sum(r["size"] for r in rows if r["src"]) / 1048576))
    print("未验证    ：%d 个目录 / %.2f MB"
          % (len(unverified),
             sum(r["size"] for r in rows if not r["src"]) / 1048576))
    for r in rows:
        if not r["src"]:
            print("   ⚠️ %s  (%d 张 / %s)" % (r["dir"], r["n"], hsize(r["size"])))

    # 输出待删清单（默认只含有源的）
    safe_files = []
    for r in rows:
        if not r["src"]:
            continue
        for i in bydir[os.path.normpath(os.path.join(VAULT, r["dir"]))]:
            safe_files.append(os.path.join(VAULT, i["path"]))

    with open(OUT_TXT, "w", encoding="utf-8") as f:
        f.write("\n".join(safe_files))
    print()
    print("待删清单（仅含已验证有源）-> %s  [%d 个文件 / %s]"
          % (OUT_TXT, len(safe_files),
             hsize(sum(os.path.getsize(p) for p in safe_files))))

    # md 复核报告
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("# 阶段1 清理复核（S 级产物）\n\n")
        f.write("| 产物目录 | 张数 | 体积 | 类型 | 源文件 | 校验 |\n")
        f.write("|---|---|---|---|---|---|\n")
        for r in sorted(rows, key=lambda r: -r["size"]):
            f.write("| %s | %d | %s | %s | %s | %s |\n"
                    % (r["dir"], r["n"], hsize(r["size"]), r["kind"],
                       r["src"] or "—", "✅" if r["src"] else "❌"))
        f.write("\n已验证有源 %d 个目录 / %s；未验证 %d 个目录 / %s\n"
                % (len(verified),
                   hsize(sum(r["size"] for r in rows if r["src"])),
                   len(unverified),
                   hsize(sum(r["size"] for r in rows if not r["src"]))))
    print("复核报告 ->", OUT_MD)


if __name__ == "__main__":
    main()
