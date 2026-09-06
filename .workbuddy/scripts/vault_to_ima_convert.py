# -*- coding: utf-8 -*-
"""
妙妙屋 → IMA/资料库 导入转换器（试点版）。
输入：白名单顶层目录（如 03-知识点）
输出：C:\Obsidion\导出_IMA\<top>\  (清洗后 md + _assets 图片) 及 <top>.zip
处理：
  - 剥离 YAML frontmatter（title → H1）
  - [[Name]] / [[Name|别名]] / [[Name#标题]] → 纯文本
  - ![[path]] → 解析真实图片 → 复制到 _assets → ![](相对路径)
  - 公式原样保留（IMA 可渲）
  - callout > [!x] → > **x**（轻微降级）
只读源、只写导出目录。
"""
import os, re, shutil, zipfile, sys, hashlib

ROOT = r"C:\Obsidion\妙妙屋"
EXPORT_ROOT = r"C:\Obsidion\导出_IMA"
IMG_EXT = {".jpg",".jpeg",".png",".gif",".svg",".webp",".bmp",".tif",".tiff"}

def build_basename_index():
    idx = {}
    for dp, dn, fns in os.walk(ROOT):
        for fn in fns:
            bn = fn.lower()
            rel = os.path.relpath(os.path.join(dp, fn), ROOT).replace("\\", "/")
            idx.setdefault(bn, []).append(rel)
    return idx

def resolve_image(target, bn_index):
    t = target.split("|")[0].split("#")[0].strip()
    if not t:
        return None
    lit = os.path.join(ROOT, t.replace("/", os.sep))
    if os.path.isfile(lit):
        return t.replace("\\", "/")
    bn = os.path.basename(t).lower()
    cand = bn_index.get(bn, [])
    if not cand:
        return None
    deep = os.path.dirname(t).lower().replace("\\", "/")
    for c in cand:
        if deep and deep in c.lower():
            return c
    return cand[0]

def safe_asset_name(src_rel, used):
    bn = os.path.basename(src_rel)
    if bn not in used:
        return bn
    h = hashlib.md5(src_rel.encode("utf-8")).hexdigest()[:8]
    return f"{h}_{bn}"

def split_code(text):
    return re.split(r"(```.*?```|~~~.*?~~~)", text, flags=re.DOTALL)

def convert_noncode(seg, asset_map, bn_index, assets_dir, top_dir, note_dir):
    # 图片嵌入
    def img_sub(m):
        inner = m.group(1)
        if inner.startswith("!"):
            return m.group(0)
        src = resolve_image(inner, bn_index)
        if not src:
            return f"[图片缺失:{inner}]"
        if src not in asset_map:
            dst_name = safe_asset_name(src, asset_map)
            asset_map[src] = dst_name
            shutil.copy2(os.path.join(ROOT, src.replace("/", os.sep)),
                         os.path.join(assets_dir, dst_name))
        rel = os.path.relpath(os.path.join(assets_dir, asset_map[src]), note_dir).replace("\\", "/")
        return f"![]({rel})"
    seg = re.sub(r"!\[\[([^\]]+)\]\]", img_sub, seg)
    # 双链（含可能的 ! 转嵌，已经处理图片；此处处理纯链接与笔记转嵌）
    def link_sub(m):
        inner = m.group(1)
        if inner.startswith("!"):
            return m.group(0)
        # [[T]], [[T|别名]], [[T#标题]], [[T#标题|别名]]
        target = inner
        alias = None
        if "|" in target:
            target, alias = target.split("|", 1)
        target = target.split("#")[0].strip()
        text = alias.strip() if alias else (os.path.basename(target) if target else "")
        return text
    seg = re.sub(r"\[\[([^\]]+)\]\]", link_sub, seg)
    # callout 降级
    seg = re.sub(r"^>\s*\[!([A-Za-z\u4e00-\u9fff]+)\]", r"> **\1**", seg, flags=re.MULTILINE)
    return seg

def convert_file(raw, asset_map, bn_index, assets_dir, top_dir, note_dir):
    # frontmatter
    fm = re.match(r"^---\n(.*?)\n---\n?", raw, flags=re.DOTALL)
    title = None
    body = raw
    if fm:
        for line in fm.group(1).splitlines():
            mm = re.match(r"\s*title\s*:\s*(.+)", line)
            if mm:
                title = mm.group(1).strip()
        body = raw[fm.end():]
    parts = split_code(body)
    out = []
    for i, p in enumerate(parts):
        if i % 2 == 1:
            out.append(p)
        else:
            out.append(convert_noncode(p, asset_map, bn_index, assets_dir, top_dir, note_dir))
    newbody = "".join(out)
    if title and not newbody.lstrip().startswith("# "):
        newbody = f"# {title}\n\n" + newbody
    return newbody

def process_top(top):
    bn_index = build_basename_index()
    src_top = os.path.join(ROOT, top)
    out_top = os.path.join(EXPORT_ROOT, top)
    assets_dir = os.path.join(out_top, "_assets")
    if os.path.isdir(out_top):
        shutil.rmtree(out_top)
    os.makedirs(assets_dir, exist_ok=True)
    asset_map = {}
    note_count = 0
    for dp, dn, fns in os.walk(src_top):
        for fn in fns:
            if not fn.lower().endswith(".md"):
                continue
            src = os.path.join(dp, fn)
            raw = open(src, encoding="utf-8", errors="replace").read()
            rel = os.path.relpath(dp, src_top)
            out_dir = os.path.join(out_top, rel) if rel != "." else out_top
            os.makedirs(out_dir, exist_ok=True)
            newbody = convert_file(raw, asset_map, bn_index, assets_dir, out_top, out_dir)
            open(os.path.join(out_dir, fn), "w", encoding="utf-8").write(newbody)
            note_count += 1
    # 打包 zip
    zip_path = os.path.join(EXPORT_ROOT, top + ".zip")
    if os.path.isfile(zip_path):
        os.remove(zip_path)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for dp, dn, fns in os.walk(out_top):
            for fn in fns:
                f = os.path.join(dp, fn)
                z.write(f, os.path.relpath(f, out_top))
    print(f"[完成] {top}: 笔记 {note_count} 篇, 打包图片 {len(asset_map)} 张")
    print(f"        导出目录: {out_top}")
    print(f"        ZIP(IMA Notion导入用): {zip_path}")
    # 报告缺失图片
    miss = [k for k in asset_map]  # asset_map 只存成功的
    return note_count, len(asset_map), zip_path

if __name__ == "__main__":
    top = sys.argv[1] if len(sys.argv) > 1 else "03-知识点"
    process_top(top)
