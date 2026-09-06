# -*- coding: utf-8 -*-
"""
妙妙屋 → 外部知识库(IMA / WorkBuddy资料库) 导入可行性探测。
只读分析，不改任何文件。产出结构化报告到 stdout。
"""
import os, re, sys, json

ROOT = r"C:\Obsidion\妙妙屋"
WL = ["03-知识点","04-题库","01-考纲导航","02-考纲条目","04-专题与题型",
      "05-真题库","05-问答","05-错题与反思","12-教学洞察","高考化学","备课思路"]

IMG_EXT = {".jpg",".jpeg",".png",".gif",".svg",".webp",".bmp",".tif",".tiff"}

def strip_codeblocks(text):
    # 去掉 ```...``` 和 ~~~...~~~ 围栏代码块（保留其余）
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"~~~.*?~~~", "", text, flags=re.DOTALL)
    return text

def main():
    # 1) 建立全库 basename 索引（用于跨目录解析图片）
    print(">> 建立全库文件索引 ...", flush=True)
    bn_index = {}   # lower basename -> [relpath,...]
    total_files = 0
    for dp, dn, fns in os.walk(ROOT):
        for fn in fns:
            total_files += 1
            bn = fn.lower()
            rel = os.path.relpath(os.path.join(dp, fn), ROOT)
            bn_index.setdefault(bn, []).append(rel.replace("\\", "/"))
    print(f">> 全库文件数={total_files}, 唯一 basename={len(bn_index)}", flush=True)

    # 2) 遍历白名单 md
    stat = {
        "md_total":0, "with_fm":0, "fm_keys":{},
        "wl_total":0, "wl_plain":0, "wl_alias":0, "wl_heading":0, "wl_transclude_note":0,
        "embed_total":0, "embed_img_ok":0, "embed_img_missing":0, "embed_note_transclude":0,
        "math_block":0, "math_inline_any":0, "math_odd_dollar":0,
        "callout":0, "tag":0, "mermaid":0, "blockref":0,
        "big_files":[],
        "missing_samples":[], "missing_srcdirs":{},
    }
    wl_re = re.compile(r"\[\[([^\]]+)\]\]")
    img_re = re.compile(r"!\[\[([^\]]+)\]\]")
    fm_re = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
    callout_re = re.compile(r"^>\s*\[!([A-Za-z\u4e00-\u9fff]+)\]", re.MULTILINE)
    tag_re = re.compile(r"(?:^|\s)#([A-Za-z0-9_\u4e00-\u9fff/-]+)")
    mermaid_re = re.compile(r"```mermaid", re.IGNORECASE)
    blockref_re = re.compile(r"#\^[\w-]+")

    for wd in WL:
        base = os.path.join(ROOT, wd)
        if not os.path.isdir(base):
            continue
        for dp, dn, fns in os.walk(base):
            for fn in fns:
                if not fn.lower().endswith(".md"):
                    continue
                fpath = os.path.join(dp, fn)
                try:
                    raw = open(fpath, encoding="utf-8", errors="replace").read()
                except Exception as e:
                    continue
                stat["md_total"] += 1
                rel = os.path.relpath(fpath, ROOT).replace("\\", "/")
                size = os.path.getsize(fpath)
                if size > 200*1024:
                    stat["big_files"].append((rel, size//1024))

                # frontmatter
                fm = fm_re.match(raw)
                if fm:
                    stat["with_fm"] += 1
                    for line in fm.group(1).splitlines():
                        m = re.match(r"\s*([\w-]+)\s*:", line)
                        if m:
                            stat["fm_keys"][m.group(1)] = stat["fm_keys"].get(m.group(1),0)+1

                body = strip_codeblocks(raw)

                # 图片嵌入
                for m in img_re.finditer(body):
                    tgt = m.group(1).split("|")[0].split("#")[0].strip()
                    if not tgt:
                        continue
                    stat["embed_total"] += 1
                    resolved = None
                    lit = os.path.join(ROOT, tgt.replace("/", os.sep))
                    if os.path.isfile(lit):
                        resolved = tgt.replace("\\","/")
                    else:
                        bn = os.path.basename(tgt).lower()
                        cand = bn_index.get(bn, [])
                        if cand:
                            # 优先选路径里包含 tgt 去目录部分的那条
                            deep = os.path.dirname(tgt).lower().replace("\\","/")
                            pick = None
                            for c in cand:
                                if deep and deep in c.lower():
                                    pick = c; break
                            if not pick:
                                pick = cand[0]
                            resolved = pick
                    if resolved:
                        ext = os.path.splitext(resolved)[1].lower()
                        if ext in IMG_EXT:
                            stat["embed_img_ok"] += 1
                        else:
                            stat["embed_note_transclude"] += 1
                    else:
                        stat["embed_img_missing"] += 1
                        if len(stat["missing_samples"]) < 25:
                            stat["missing_samples"].append(tgt)
                        sd = tgt.split("/")[0]
                        stat["missing_srcdirs"][sd] = stat["missing_srcdirs"].get(sd,0)+1

                # 双链（去掉图片嵌入后剩余的 [[ ]]）
                for m in wl_re.finditer(body):
                    inner = m.group(1)
                    if inner.startswith("!"):   # 已算作嵌入
                        continue
                    stat["wl_total"] += 1
                    has_alias = "|" in inner
                    has_head = "#" in inner
                    if has_head and not has_alias and not inner.split("#")[0].strip():
                        stat["wl_transclude_note"] += 1
                    if has_alias:
                        stat["wl_alias"] += 1
                    elif has_head:
                        stat["wl_heading"] += 1
                    else:
                        stat["wl_plain"] += 1

                # 公式
                noblock = re.sub(r"\$\$.*?\$\$", "", body, flags=re.DOTALL)
                if "$$" in raw:
                    stat["math_block"] += 1
                if re.search(r"(?<!\$)\$(?!\$)[^$\n]+?(?<!\$)\$(?!\$)", raw):
                    stat["math_inline_any"] += 1
                # 奇数 $ 检测（去掉 $$ 块后）
                dollars = noblock.count("$")
                if dollars % 2 == 1:
                    stat["math_odd_dollar"] += 1

                # 其它语法
                if callout_re.search(body): stat["callout"] += 1
                if tag_re.search(body): stat["tag"] += 1
                if mermaid_re.search(raw): stat["mermaid"] += 1
                if blockref_re.search(body): stat["blockref"] += 1

    # 输出
    print("\n================ 探测报告 ================")
    print(f"白名单 md 总数: {stat['md_total']}")
    print(f"含 frontmatter: {stat['with_fm']}  (前键: {dict(list(stat['fm_keys'].items())[:12])})")
    print(f"\n-- 双链 [[ ]] --")
    print(f"  总数={stat['wl_total']}  纯[[Name]]={stat['wl_plain']}  [[Name|别名]]={stat['wl_alias']}  [[Name#标题]]={stat['wl_heading']}  疑似笔记转嵌={stat['wl_transclude_note']}")
    print(f"\n-- 图片/嵌入 ![[ ]] --")
    print(f"  嵌入总数={stat['embed_total']}  图片解析成功={stat['embed_img_ok']}  图片缺失={stat['embed_img_missing']}  笔记转嵌={stat['embed_note_transclude']}")
    if stat['embed_total']:
        ok = stat['embed_img_ok']; miss = stat['embed_img_missing']
        print(f"  图片解析成功率={ok/(ok+miss)*100:.1f}%  (缺失率={miss/(ok+miss)*100:.1f}%)")
    print(f"  缺失来源目录 Top: {dict(sorted(stat['missing_srcdirs'].items(), key=lambda x:-x[1])[:10])}")
    print(f"  缺失样例: {stat['missing_samples'][:10]}")
    print(f"\n-- 公式 --")
    print(f"  含 $$ 块={stat['math_block']}  含内联$= {stat['math_inline_any']}  奇数$(疑似残缺)={stat['math_odd_dollar']}")
    print(f"\n-- 其它 Obsidian 语法(含文件数) --")
    print(f"  callout> [!..]={stat['callout']}  #标签={stat['tag']}  mermaid代码块={stat['mermaid']}  块引用#^={stat['blockref']}")
    print(f"\n-- 大文件(>200KB, {len(stat['big_files'])} 个) Top8 --")
    for rel,sz in sorted(stat['big_files'], key=lambda x:-x[1])[:8]:
        print(f"  {sz}KB  {rel}")
    print("==========================================")

if __name__ == "__main__":
    main()
