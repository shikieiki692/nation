#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""docx_verify.py — 讲义 docx 终端产物复核工具（质量战 P0-3 固化）

来源：批40~55 精读线手工 zipfile 复核流程的正式化。
用法：
  python docx_verify.py --path <md 或 docx 路径>          # 单份（md 自动映射同目录名 docx）
  python docx_verify.py --all                             # 扫 06-学生侧材料/讲义/ 全部 docx
检查项：
  media 数 vs FM image_count（md 侧）/ docx 内嵌图数
  正文 TAB、字面 $（math 泄漏）、θ 计数与可疑误转模式（θC/θK/θmol 等）、° 计数
输出：每文件一行摘要；--strict 时 θ可疑/字面$/TAB 非零 → exit 1。
"""
import os, re, sys, argparse, zipfile

_here = os.path.dirname(os.path.abspath(__file__))
VAULT = _here
for _ in range(6):
    if os.path.isdir(os.path.join(VAULT, "06-学生侧材料")):
        break
    VAULT = os.path.dirname(VAULT)
DOCX_ROOT = os.path.join(VAULT, "06-学生侧材料", "讲义")

# θ 可疑模式：仅 °C 温度误转特征「θC」（批46 实证「0 θC」）。
# 注意：θ 后跟变量名/下标（ΔGθsolv、EθF、kθAθB）是标准态记号连排，合法——宽模式 θ[A-Za-z] 误报率 100%，弃用。
PAT_THETA_SUSPECT = re.compile(r"θC")


def fm_image_count(md_path):
    try:
        with open(md_path, encoding="utf-8", errors="replace") as f:
            head = f.read(4000)
    except OSError:
        return None
    m = re.search(r"^image_count:\s*(\d+)", head, re.M)
    return int(m.group(1)) if m else None


def verify(docx):
    with zipfile.ZipFile(docx) as z:
        media = [n for n in z.namelist() if n.startswith("word/media/")]
        xml = z.read("word/document.xml").decode("utf-8", errors="replace")
    text = re.sub(r"<[^>]+>", "", xml)
    theta_ctx = [text[max(0, m.start() - 10):m.end() + 6].replace("\n", " ")
                 for m in re.finditer("θ", text)]
    suspects = [c for c in theta_ctx if PAT_THETA_SUSPECT.search(c)]
    return {
        "docx": docx,
        "media": len(media),
        "tab": "\t" in xml,
        "literal_dollar": text.count("$"),
        "theta": text.count("θ"),
        "theta_suspect": suspects,
        "deg": text.count("°"),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", help="md 或 docx 路径（单份）")
    ap.add_argument("--all", action="store_true", help="扫讲义 docx 全量")
    ap.add_argument("--theta-context", action="store_true", help="输出全部 θ 上下文")
    ap.add_argument("--strict", action="store_true", help="可疑项非零则 exit 1")
    args = ap.parse_args()

    docs = []
    if args.path:
        p = args.path
        if p.endswith(".md"):
            cand = os.path.join(DOCX_ROOT, os.path.relpath(p, os.path.join(VAULT, "04-课件", "学生讲义")))
            cand = cand[:-3] + ".docx"
            p = cand
        if not os.path.exists(p):
            print(f"🔴 docx 不存在: {p}")
            sys.exit(1)
        docs = [p]
    elif args.all:
        for dp, dn, fns in os.walk(DOCX_ROOT):
            if "_归档" in dp or "_archive" in dp:
                dn[:] = []
                continue
            for fn in fns:
                if fn.endswith(".docx"):
                    docs.append(os.path.join(dp, fn))
    else:
        ap.error("需要 --path 或 --all")

    print(f"🔍 docx_verify 开始（受检 {len(docs)} 份）...")
    n_bad = 0
    for d in sorted(docs):
        r = verify(d)
        rel = os.path.relpath(d, VAULT)
        flags = []
        if r["literal_dollar"]:
            flags.append(f"字面$×{r['literal_dollar']}")
        if r["tab"]:
            flags.append("TAB")
        if r["theta_suspect"]:
            flags.append(f"θ可疑×{len(r['theta_suspect'])}: {r['theta_suspect'][:2]}")
        md = d[:-5] + ".md"
        fm_ic = fm_image_count(md.replace("06-学生侧材料", "04-课件").replace(os.sep + "讲义" + os.sep, os.sep + "学生讲义" + os.sep)) if os.path.exists(md) else None
        ic = f"media={r['media']}" + (f"/FM={fm_ic}" if fm_ic is not None else "")
        tag = "✅" if not flags else "🔴"
        if flags:
            n_bad += 1
        print(f"  {tag} {rel}  θ={r['theta']} °={r['deg']} {ic} {'; '.join(flags)}")
        if args.theta_context and r["theta"]:
            for c in r["theta_ctx"]:
                print(f"        θ… {c}")
    print(f"\n📊 结果: 受检 {len(docs)} | 🔴 可疑 {n_bad}")
    sys.exit(1 if (args.strict and n_bad) else 0)


if __name__ == "__main__":
    main()
