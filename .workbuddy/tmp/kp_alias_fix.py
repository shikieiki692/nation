# -*- coding: utf-8 -*-
"""B2｜KP 真孤儿 alias 承接（0 新建）—— CRLF 安全版。

政策依据：00-首页/活跃任务/断链内容建设backlog.md
  「现有 KP 足够，优先复用，0 新建」＋「断链由现有近义 KP 通过 frontmatter aliases 承接」。

做法：把孤儿 token 追加进**归属页**的 aliases（仅改 aliases 一行；EOL 保全）。
护栏：① CRLF 感知（`\r?`）；② 前置断言「aliases 键恰 0 或 1 个」；③ 幂等；④ 后置断言「恰 1 个」；
      ⑤ 落盘后逐文件 yaml 严格解析。
"""
import os
import re
import sys
import yaml

VAULT = r"C:/Obsidion/妙妙屋"
KP = os.path.join(VAULT, "03-知识点")

MAP = [
    ("化学原理/配合物几何构型.md", "三方柱", "页内含『三帽三方柱』『三棱柱』配位多面体"),
    ("无机和结构化学/氮族元素.md", "肼", "页内 5 处肼（N2H4）内容"),
    ("无机和结构化学/小分子活化.md", "氮气活化", "页内『N₂ 是最难活化的小分子之一』专节"),
    ("化学原理/基尔霍夫定律.md", "绝热燃烧", "页内『绝热火焰温度/最高温度』解题范式"),
    ("无机和结构化学/配位化学.md", "配位方式", "页内含端基/桥联/螯合配位方式"),
    ("无机和结构化学/硅烷.md", "硅烯", "页内回链 [[题-34决理-2-1-3-硅烷配位聚合物]]（同卡）"),
]

RE_ALIAS = re.compile(r"^aliases:[ \t]*\[(.*?)\][ \t]*(\r?\n|$)", re.M)
RE_TITLE = re.compile(r"^title:.*?(\r?\n|$)", re.M)


def fix(path, token):
    p = os.path.join(KP, path)
    raw = open(p, encoding="utf-8-sig", newline="").read()
    bom = "\ufeff" if raw.startswith("\ufeff") else ""
    body = raw[1:] if bom else raw

    keys = re.findall(r"^aliases:", body, flags=re.M)
    if len(keys) > 1:
        return ("DUP_KEY_PRE", p, None)

    m = RE_ALIAS.search(body)
    if m:
        inner = m.group(1)
        items = [x.strip() for x in inner.split(",") if x.strip()]
        if token in items:
            return ("EXISTS", p, None)
        new_inner = (inner.rstrip() + ", " + token) if inner.strip() else token
        new = "aliases: [%s]" % new_inner + m.group(2)
        out = body[:m.start()] + new + body[m.end():]
        if not out.endswith(m.group(2)) and m.group(2):
            pass
        if m.group(2) == "" and not out.endswith("\n"):
            out += "\n"
    else:
        mt = RE_TITLE.search(body)
        if not mt:
            return ("NO_TITLE", p, None)
        eol = mt.group(1) or "\n"
        out = body[:mt.end()] + "aliases: [%s]%s" % (token, eol) + body[mt.end():]

    if out == body:
        return ("NOCHANGE", p, None)
    if len(re.findall(r"^aliases:", out, flags=re.M)) != 1:
        return ("DUP_KEY_POST", p, None)

    open(p, "w", encoding="utf-8", newline="").write(bom + out)
    # 落盘后严格解析
    t = open(p, encoding="utf-8-sig", newline="").read()
    try:
        d = yaml.safe_load(t[3:t.find("\n---", 3)])
        assert isinstance(d, dict) and token in [str(x) for x in d.get("aliases", [])]
    except Exception as e:
        return ("PARSE_FAIL:%s" % e, p, None)
    return ("OK", p, out)


def main():
    ok = 0
    for path, token, why in MAP:
        st, p, _ = fix(path, token)
        if st == "OK":
            ok += 1
        print("  [%s] %-32s <= %s   (%s)" % (st, path, token, why))
    print("\n已改 %d / %d" % (ok, len(MAP)))
    return 0 if ok == len(MAP) else 1


if __name__ == "__main__":
    sys.exit(main())
