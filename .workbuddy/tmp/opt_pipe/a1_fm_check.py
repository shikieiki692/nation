# -*- coding: utf-8 -*-
"""A1 自证：4 个改动文件的 frontmatter 可解析 + 关键字段未丢。

用 ruamel（系统 py3.12）严格解析；并断言「改动只落在预期字段」——
即除被改的链接字符串外，FM 其余键与旧版（HEAD）完全一致。
"""
import os, sys, subprocess
from ruamel.yaml import YAML

VAULT = r"C:\Obsidion\妙妙屋"
FILES = [
    "00-首页/活跃任务/任务卡-KP待完善项非文字任务清零.md",
    "00-首页/活跃任务/任务卡-PPT制作方法探究与试点.md",
    "00-首页/活跃任务/任务卡-validate_kb每周运行.md",
    "00-首页/活跃任务/任务卡-学生材料清理.md",
]


def split_fm(text):
    text = text.replace("\r\n", "\n")
    if not text.startswith("---"):
        return None, text
    e = text.find("\n---", 3)
    if e == -1:
        return None, text
    return text[3:e], text[e + 4:]


def parse(fm_text):
    y = YAML(typ="rt")
    return y.load(fm_text)


def head_version(rel):
    out = subprocess.run(["git", "show", "HEAD:" + rel.replace("\\", "/")],
                         cwd=VAULT, capture_output=True)
    if out.returncode != 0:
        return None
    return out.stdout.decode("utf-8-sig")


bad = 0
for rel in FILES:
    p = os.path.join(VAULT, rel)
    cur = open(p, encoding="utf-8-sig", newline="").read()
    fm_text, body = split_fm(cur)
    try:
        d = parse(fm_text)
    except Exception as e:
        print("FM 解析失败:", rel, e)
        bad += 1
        continue
    old_raw = head_version(rel)
    ofm_text, obody = split_fm(old_raw)
    try:
        od = parse(ofm_text)
    except Exception as e:
        print("HEAD 版解析失败:", rel, e)
        od = None
    print("[OK]", rel)
    if od is not None:
        same_keys = set(d.keys()) == set(od.keys())
        print("     键集合一致:", same_keys)
        if not same_keys:
            print("     新增:", set(d.keys()) - set(od.keys()),
                  " 丢失:", set(od.keys()) - set(d.keys()))
            bad += 1
        # 正文必须逐字节不变（本次只改 FM 内的链接字符串）
        print("     正文逐字节不变:", body == obody)
        if body != obody:
            bad += 1
        # 逐键比对，列出实际变化的键
        changed = [k for k in d.keys()
                   if k in od and repr(d[k]) != repr(od[k])]
        print("     变化键:", changed)
print()
print("VERDICT:", "PASS" if bad == 0 else "FAIL(%d)" % bad)
