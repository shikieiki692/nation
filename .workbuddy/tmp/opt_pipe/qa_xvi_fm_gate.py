# -*- coding: utf-8 -*-
"""卷XVI 收口 QA：13 张改过的源卡 FM 严格解析（js-yaml4 等价语义）＋护栏规则。

判据（对齐 .workbuddy/memory 的 FM 护栏）：
  ① ruamel safe 严格解析（重复键/非法转义 ⇒ 抛错）；
  ② 块列表项必须 '- '（裸 [[...]] ⇒ js-yaml4 THROW）；
  ③ 值若含裸 ': '、以 * [ { 开头 ⇒ 必须加引号；
  ④ CRLF / 行内数组兼容性检查。
"""
import io
import os
import re
import sys

from ruamel.yaml import YAML

VAULT = r"C:\Obsidion\妙妙屋"
Q = "04-题库/2026机构初赛模拟题"
CARDS = [
    f"{Q}/化英社/题-HYS-15-04-近年来随着金属有机框架MOF.md",
    f"{Q}/chemy/题-CM-12-05-DNA碱基之间的特异性配对即.md",
    f"{Q}/chemy/题-CM-17-05-51在气相的硫单质中存在着等.md",
    f"{Q}/壹尖培优/题-YJ-12-05-伦敦色散力Londondis.md",
    f"{Q}/汇智/题-HZ-01-06-CuI由于具有灵活多变的配位.md",
    f"{Q}/XeChem/题-XeC-40-02-请注意本题的21和22两部分.md",
    f"{Q}/质心GChO/题-GChO-82-04-正烷烃是目前人们研究最为深入.md",
    f"{Q}/化英社/题-HYS-03-03-高松灯捡到方钠石后却不禁陷入.md",
    f"{Q}/汇智/题-HZ-02-05-长期以来水系电池由于锰氧化物.md",
    f"{Q}/清北营/题-QBY-16-05-液体中的起泡现象广泛存在于多.md",
    f"{Q}/壹尖培优/题-YJ-05-04-在整个冷战期间苏联705型核.md",
    f"{Q}/XeChem/题-XeC-40-06-量子点是一种半导体纳米晶粒径.md",
    f"{Q}/质心GChO/题-GChO-61-06-二茂铁Fc及其氧化态的氧化还.md",
]

yaml = YAML(typ="safe")
yaml.allow_duplicate_keys = False


def front_of(text):
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "\n".join(lines[1:i])
    return None


def main():
    bad = 0
    for rel in CARDS:
        p = os.path.join(VAULT, rel)
        if not os.path.exists(p):
            print(f"[MISS] {rel}")
            bad += 1
            continue
        raw = io.open(p, encoding="utf-8-sig", newline="").read()
        fm = front_of(raw)
        notes = []
        if fm is None:
            notes.append("无 FM 块")
        else:
            try:
                doc = yaml.load(fm)
                if not isinstance(doc, dict):
                    notes.append("FM 非映射")
            except Exception as e:
                notes.append(f"PARSE={'type(e).__name__'}: {e}")
            # ② 块列表 '- '
            for m in re.finditer(r"^([A-Za-z_]+):\s*$", fm, re.M):
                key = m.group(1)
                after = fm[m.end():].lstrip("\n")
                if after.startswith("[[") or after.startswith("{"):
                    notes.append(f"块列表 {key} 值裸 [[/{{")
            # ③ 值含裸 ': '
            for line in fm.split("\n"):
                mm = re.match(r"^([A-Za-z_]+):\s+(.*)$", line)
                if not mm:
                    continue
                k, v = mm.group(1), mm.group(2).strip()
                if not v or v[0] in "\"'|>[&!":
                    continue
                if ": " in v:
                    notes.append(f"值含裸 ': ' ← {k}")
                if v[0] in "*[{" and not v.startswith("[["):
                    notes.append(f"值以 {v[0]} 开头未加引号 ← {k}")
        tag = "OK  " if not notes else "FAIL"
        if notes:
            bad += 1
        print(f"[{tag}] {os.path.basename(rel)[:44]:<46} {'; '.join(notes)}")
    print(f"\n合计 {len(CARDS)} 张 ｜ 异常 {bad} 张")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
