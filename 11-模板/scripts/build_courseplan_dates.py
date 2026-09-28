# -*- coding: utf-8 -*-
"""课程计划「起止日期」生成器（可重复运行，幂等）。

用法：
    python build_courseplan_dates.py            # 生成/刷新 md 中的起止日期列
    python build_courseplan_dates.py --dry-run  # 只报数，不写文件

口径（2026-09-28 与用户确认）：
  学年锚点 初二＝2026—2027 学年；学期起止按 9/1 开学、1 月下旬放寒假、2 月下旬开学、7 月上旬放假。
  学期内  每周三、周六各 1 次；学期内法定假期（清明1/五一2/端午1/中秋2/国庆3/元旦1）按天加课，
          加课日若恰为周三/周六不重复；候选日按日期升序取前 N 个（N＝该期次次数），学期末多余周转为考试周。
  假期    寒假/暑假 = 集中 12 天 × 2 次（寒假避开春节块 除夕—初六，取靠前 12 天；暑假自开始后第 5 天起连续 12 天）；
          高二寒假 = 5 天 × 2 次。
  输出    §1.1 期次列写「Y.M.D — M.D」；§二 章级列写「M.D—M.D」（跨年标「（跨年）」）。

依赖：zhdate（农历换算），建议用受管 venv 运行。
"""
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

from zhdate import ZhDate

VAULT = Path(__file__).resolve().parents[2]
SRC = VAULT / "备课思路" / "未央化学竞赛课程计划（初二至高二）.md"
CACHE = VAULT / ".workbuddy" / "tmp" / "courseplan_dates"
WED, SAT = 2, 5
DRY = "--dry-run" in sys.argv

PERIODS = [
    ("初二寒假", "2027-01-23", "2027-02-21", 24, "vac"),
    ("初二下学期", "2027-02-22", "2027-07-09", 40, "sem"),
    ("初二暑假", "2027-07-10", "2027-08-31", 24, "vac"),
    ("初三上学期", "2027-09-01", "2028-01-21", 40, "sem"),
    ("初三寒假", "2028-01-22", "2028-02-20", 24, "vac"),
    ("初三下学期", "2028-02-21", "2028-07-07", 40, "sem"),
    ("初三暑假", "2028-07-08", "2028-08-31", 24, "vac"),
    ("高一上学期", "2028-09-01", "2029-01-19", 40, "sem"),
    ("高一寒假", "2029-01-20", "2029-02-25", 24, "vac"),
    ("高一下学期", "2029-02-26", "2029-07-13", 40, "sem"),
    ("高一暑假", "2029-07-14", "2029-08-31", 24, "vac"),
    ("高二上学期", "2029-09-01", "2030-01-18", 40, "sem"),
    ("高二寒假", "2030-01-19", "2030-02-24", 10, "vac"),
    ("高二下学期", "2030-02-25", "2030-07-12", 40, "sem"),
    ("高二暑假", "2030-07-13", "2030-08-31", 24, "vac"),
]
CNY = {2027: "2027-02-06", 2028: "2028-01-26", 2029: "2029-02-13", 2030: "2030-02-03"}
QINGMING = {2027: "04-05", 2028: "04-04", 2029: "04-04", 2030: "04-05"}
MODNAME = ["化学基础知识", "结构化学", "物理化学", "分析化学", "无机化学", "有机化学", "数学工具"]


def d(s):
    y, m, dd = map(int, s.split("-"))
    return date(y, m, dd)


def luan(y, m, dd):
    return ZhDate(y, m, dd).to_datetime().date()


HOLIDAYS = sorted({x for y in CNY for x in (
    d("%d-%s" % (y, QINGMING[y])), d("%d-05-01" % y), d("%d-05-02" % y),
    luan(y, 5, 5), luan(y, 8, 15), luan(y, 8, 15) + timedelta(1),
    d("%d-10-01" % y), d("%d-10-02" % y), d("%d-10-03" % y), d("%d-01-01" % y))})


def spring_block(y):
    c = d(CNY[y])
    return {c + timedelta(i) for i in range(-1, 6)}


def build_calendar():
    cal = {}
    for name, s, e, target, kind in PERIODS:
        s, e = d(s), d(e)
        days, cur = [], s
        while cur <= e:
            days.append(cur)
            cur += timedelta(1)
        if kind == "sem":
            pool = sorted({x for x in days if x.weekday() in (WED, SAT)}
                          | {x for x in HOLIDAYS if s <= x <= e})
            assert len(pool) >= target, "%s 候选日 %d < %d" % (name, len(pool), target)
            chosen = pool[:target]
        else:
            free = [x for x in days if x not in spring_block(s.year)]
            if target == 24:
                if s.month >= 7:
                    i0 = days.index(s) + 5
                    teach = days[i0:i0 + 12]
                else:
                    teach = free[:12]
            else:
                teach = free[:5]
            chosen = [x for x in teach for _ in (0, 1)]
        assert len(chosen) == target, "%s %d != %d" % (name, len(chosen), target)
        cal[name] = {"start": chosen[0].isoformat(), "end": chosen[-1].isoformat(),
                     "days": [x.isoformat() for x in chosen]}
    return cal


def fmt_long(a, b):
    ya, ma, da = a.split("-")
    yb, mb, db = b.split("-")
    return ("%s.%d.%d — %d.%d" % (ya, int(ma), int(da), int(mb), int(db)) if ya == yb
            else "%s.%d.%d — %s.%d.%d" % (ya, int(ma), int(da), yb, int(mb), int(db)))


def fmt_short(ds):
    y1, m1, d1 = map(int, ds[0].split("-"))
    y2, m2, d2 = map(int, ds[-1].split("-"))
    s = "%d.%d—%d.%d" % (m1, d1, m2, d2)
    return s + ("（跨年）" if y1 != y2 else "")


def main():
    CAL = build_calendar()
    text = SRC.read_text(encoding="utf-8", newline="")
    lines = text.split("\r\n")

    # --- 解析 §二 章序与次数 ---
    mods, i = [], 0
    while i < len(lines):
        if lines[i].strip() == "| 章 | 节 | 知识点 | 教材来源 | 起止日期 | 次数 |":
            mods.append([])
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                c = [x.strip() for x in lines[i].strip().strip("|").split("|")]
                if c[0] and c[5].isdigit():
                    mods[-1].append((c[0], int(c[5])))
                i += 1
            continue
        i += 1
    assert len(mods) == 7, len(mods)
    chap_total = {nm: k for m in mods[:6] for nm, k in m}
    CHAPMAP = {re.sub(r"\s+", "", nm): nm for nm in chap_total}

    # --- 解析 §1.1 各期次模块序列 ---
    a = next(i for i, l in enumerate(lines) if l.strip() == "### 1.1 时间与次数总表")
    b = next(i for i, l in enumerate(lines) if i > a and l.strip().startswith("### 1.2"))
    plan = {}
    for i in range(a, b):
        if not lines[i].strip().startswith("|"):
            continue
        c = [x.strip().replace("**", "") for x in lines[i].strip().strip("|").split("|")]
        if len(c) != 5 or c[0] in ("期次", "合计") or set("".join(c)) <= set(":- "):
            continue
        if c[0].startswith("高二"):
            continue
        total = int(c[3].split("＋")[0])
        seq = []
        for seg in c[4].split("｜"):
            seg = seg.strip()
            if not seg or "外出" in seg:
                continue
            mm = re.search(r"（(?:余 )?(\d+)(?:，开局)?）$", seg)
            assert mm, seg
            k = int(mm.group(1))
            nm = re.sub(r"^[^（）]*[·：]", "", seg[:mm.start()].strip())
            if nm in MODNAME:
                seq += mods[0]
            else:
                key = re.sub(r"\s+", "", nm)
                assert key in CHAPMAP, "章名未对上：%r" % seg
                seq.append((CHAPMAP[key], k))
        assert sum(k for _, k in seq) == total, (c[0], total)
        plan[c[0]] = seq

    # --- 铺日期 ---
    chap_days = {}
    for p, seq in plan.items():
        days, idx = CAL[p]["days"], 0
        for nm, k in seq:
            chap_days.setdefault(nm, []).extend(days[idx:idx + k])
            idx += k
        assert idx == len(days), p
    for nm, k in chap_total.items():
        assert len(chap_days.get(nm, [])) == k, (nm, k)

    # --- 写回 ---
    out, i, n1, n2, n3 = [], 0, 0, 0, 0
    mods_span, mods_note = {}, {}
    for mi, m in enumerate(mods[:6]):
        ds = sorted(d for nm, _ in m for d in chap_days.get(nm, []))
        mods_span[mi + 1] = fmt_long(ds[0], ds[-1]) if ds else "—"
        # 分块：相邻上课日间隔 > 200 天视为进入下一轮
        blocks, cur = [], [ds[0]]
        for a, b in zip(ds, ds[1:]):
            if (date.fromisoformat(b) - date.fromisoformat(a)).days > 200:
                blocks.append(cur)
                cur = []
            cur.append(b)
        blocks.append(cur)
        if len(blocks) > 1:
            mods_note[mi + 1] = "分 %d 段：" % len(blocks) + "｜".join(
                "%s %s" % (("第一轮初步", "第三轮深化")[i] if len(blocks) == 2 else "第 %d 段" % (i + 1),
                           fmt_long(b[0], b[-1]))
                for i, b in enumerate(blocks)) + "（其余为两段之间的间隔期）"
    while i < len(lines):
        s = lines[i].strip()
        mh = re.fullmatch(r"### (\d)\.(.+?)(?:（\d{4}\.\d{1,2}\.\d{1,2}.*?）)?", s)
        if mh and MODNAME[int(mh.group(1)) - 1] == mh.group(2).strip() \
                and int(mh.group(1)) in mods_span:
            k = int(mh.group(1))
            out.append("### %s.%s（%s）" % (mh.group(1), mh.group(2).strip(), mods_span[k]))
            if k in mods_note:
                # 已有同内容分段注则不重复插入
                if not (i + 1 < len(lines) and lines[i + 1].strip() == "> " + mods_note[k]):
                    out.append("> " + mods_note[k])
            n3 += 1
            i += 1
            continue
        if s.startswith("> 分 ") and s.endswith("（其余为两段之间的间隔期）"):
            i += 1
            continue                              # 旧的分段注由上面重写
        if s == "| 期次 | 起止日期 | 排课形式 | 次数（校内＋外出） | 课程模块（括号内为次数） |":
            out.append(lines[i]); i += 1; out.append(lines[i]); i += 1
            while i < len(lines) and lines[i].strip().startswith("|"):
                c = [x.strip() for x in lines[i].strip().strip("|").split("|")]
                key = c[0].replace("**", "")
                c[1] = fmt_long(CAL[key]["start"], CAL[key]["end"]) if key in CAL else "—"
                n1 += key in CAL
                out.append("| " + " | ".join(c) + " |"); i += 1
            continue
        if s == "| 章 | 节 | 知识点 | 教材来源 | 起止日期 | 次数 |":
            out.append(lines[i]); i += 1; out.append(lines[i]); i += 1
            while i < len(lines) and lines[i].strip().startswith("|"):
                c = [x.strip() for x in lines[i].strip().strip("|").split("|")]
                nm = CHAPMAP.get(re.sub(r"\s+", "", c[0]))
                c[4] = fmt_short(sorted(chap_days[nm])) if nm else "—"
                n2 += bool(nm)
                out.append("| " + " | ".join(c) + " |"); i += 1
            continue
        out.append(lines[i]); i += 1

    assert n1 == 15 and n2 == 63 and n3 == 6, (n1, n2, n3)
    new = "\r\n".join(out)

    if not DRY:
        SRC.write_text(new, encoding="utf-8", newline="")
        assert SRC.read_text(encoding="utf-8", newline="") == new
    CACHE.mkdir(parents=True, exist_ok=True)
    (CACHE / "calendar.json").write_text(json.dumps(CAL, ensure_ascii=False, indent=1), encoding="utf-8")
    print("[%s] 期次 %d / 章 %d / 模块 %d；md 变更 %d 行" %
          ("dry-run" if DRY else "ok", n1, n2, n3,
           sum(1 for x, y in zip(text.split("\r\n"), out) if x != y)))


if __name__ == "__main__":
    main()
