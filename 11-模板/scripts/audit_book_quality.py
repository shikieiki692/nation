# -*- coding: utf-8 -*-
"""习题书低质量题排查（只读）。

四维打分（2026-09-01 用户确认的口径）：
  硬指标①难度过低：difficulty ≤ 2 且非真题；
  硬指标②考纲无关：syllabus_codes 为空，且 knowledge_points 无法关联到
        02-考纲条目（标题/知识笔记/应关联正式知识点/tags 词表）；
  软标记③篇幅过短：题干去标记后 < 60 字且无图；
  软标记④缺乏解析：全部小问答案为空或命中占位词（原书未提供/答案待补充…）。

硬指标命中 → 建议降级（pack 改回章节练习，源文件保留可恢复）；
软标记 → 仅列清单供人工复核。

输出：09-审计报告/<日期>-低质量题排查清单.md
      07-资料提炼/习题书-低质量候选.json（demote_questions.py 的输入）
运行：系统 Python 3.12（需 PyYAML），vault 根目录执行。
"""
import io
import json
import re
import sys
import collections
from pathlib import Path

if not (getattr(sys.stdout, "encoding", "") == "utf-8"
        and getattr(sys.stdout, "errors", "") == "replace"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, "11-模板/scripts")
import build_module_book as B  # noqa: E402
import yaml  # noqa: E402

VAULT = Path(__file__).resolve().parents[2]
REPORT = VAULT / "09-审计报告" / f"{B.TODAY}-低质量题排查清单.md"
CAND_JSON = VAULT / "07-资料提炼" / "习题书-低质量候选.json"

MODULES = [
    ("化学原理", B.CHEM_MAP, None),
    ("有机化学", B.ORGANIC_MAP, B.ORGANIC_EXCLUDE),
    ("元素与分析", B.YSFX_MAP, None),
    ("结构化学", B.STRUCTURE_MAP, None),
]

SHORT_LEN = 60
PLACEHOLDER_RE = re.compile(r"原书未提供|略，见源文件|答案待补充|需要完整题目信息|图片待补")
NEAR_EMPTY_RE = re.compile(r"^[（(【\s]*原书未提供[解解答]*[）)】\s]*$")

# ---------------- 考纲词表 ----------------

def _norm(s):
    return re.sub(r"[\s_\-（）()【】\[\]]", "", str(s)).lower()


def load_vocab():
    """02-考纲条目 → 词表：标题、tags、knowledge_notes、应关联正式知识点。"""
    vocab = set()
    for p in (VAULT / "02-考纲条目").rglob("*.md"):
        s = p.read_text(encoding="utf-8", errors="replace")
        m = re.match(r"^---\n(.*?)\n---\n", s, re.S)
        if m:
            try:
                fm = yaml.safe_load(m.group(1)) or {}
            except Exception:
                fm = {}
            for k in ("title", "syllabus_code", "syllabus_module", "subject"):
                if fm.get(k):
                    vocab.add(_norm(fm[k]))
            for k in ("tags", "knowledge_notes", "topic_notes"):
                for v in (fm.get(k) or []):
                    vocab.add(_norm(v))
        m2 = re.search(r"## 三、应关联的正式知识点\n(.*?)(?=\n## |\Z)", s, re.S)
        if m2:
            for line in m2.group(1).splitlines():
                line = re.sub(r"^[-*\s]+", "", line).strip()
                if line:
                    vocab.add(_norm(line))
    return {v for v in vocab if len(v) >= 2}


def load_full_fm(rel_path):
    p = VAULT / "04-题库" / rel_path
    try:
        s = p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return {}
    m = re.match(r"^---\n(.*?)\n---\n", s, re.S)
    if not m:
        return {}
    try:
        return yaml.safe_load(m.group(1)) or {}
    except Exception:
        return {}


def kp_names(fm):
    kp = fm.get("knowledge_points") or []
    if isinstance(kp, str):
        kp = [kp]
    out = []
    for k in kp:
        k = str(k)
        found = re.findall(r"\[\[([^\]|#]+)", k)
        out.extend(x.strip() for x in found) if found else out.append(k.strip())
    return [x for x in out if x]


def syllabus_related(fm, vocab):
    codes = fm.get("syllabus_codes") or []
    if isinstance(codes, str):
        codes = [codes]
    if [c for c in codes if str(c).strip() and str(c).strip() != "[]"]:
        return True, "syllabus_codes=" + ",".join(str(c) for c in codes)
    kps = kp_names(fm)
    for n in kps:
        nn = _norm(n)
        if not nn:
            continue
        if nn in vocab:
            return True, f"kp[{n}]直连考纲词表"
        for v in vocab:
            if len(v) >= 4 and (v in nn or nn in v):
                return True, f"kp[{n}]≈考纲[{v}]"
    return False, "syllabus_codes空 且 kp未命中考纲词表"


def qa_texts(item):
    q, a = B.split_question_answer(item["body"], item.get("source", ""))
    q = B.collapse_hrs(B.clean_section_text(q))
    a = B.collapse_hrs(B.clean_section_text(a))
    return q, a


def strip_marks(t):
    t = re.sub(r"!\[\[[^\]]*\]\]", "", t)      # 图片
    t = re.sub(r"\$\$?[^$]*\$\$?", "F", t)     # 公式按 1 字符记
    t = re.sub(r"[*_`>#|>-]", "", t)
    return re.sub(r"\s", "", t)


def main():
    vocab = load_vocab()
    print(f"考纲词表: {len(vocab)} 个规范词")
    hard, soft = [], []
    total = 0

    for module, cmap, exclude in MODULES:
        pool = [q for q in B.gather_questions(module)
                if q.get("submodule") not in set(exclude or [])]
        pool = [q for q in pool if not B.is_gap_item(q)]
        # 按"入书题"粒度分组（大题合并组整组评估、整组处置）
        groups = collections.OrderedDict()
        for item in pool:
            k = B.da_key(item["file"]) or item["file"]  # 非大题小问按文件名独立成组
            groups.setdefault(k, []).append(item)
        for k, g in groups.items():
            total += 1
            g = sorted(g, key=lambda x: B._natkey(x["file"]))
            head = g[0]
            paths = [x["path"] for x in g]
            fms = [load_full_fm(p) for p in paths]
            difficulty = max(x["difficulty"] for x in g)
            is_exam = bool(B.exam_label(head))
            q_texts, a_texts = zip(*(qa_texts(x) for x in g))
            q_all = "\n".join(q_texts)
            a_all = "\n".join(a_texts)
            q_len = len(strip_marks(q_all))
            has_img = "![[" in q_all

            reasons, evid = [], []
            # ① 难度过低
            if difficulty <= 2 and not is_exam:
                reasons.append("难度过低")
                evid.append(f"difficulty={difficulty} 非真题")
            # ② 考纲无关
            if not is_exam:
                any_rel = False
                det = []
                for fm in fms:
                    rel, why = syllabus_related(fm, vocab)
                    det.append(why)
                    any_rel = any_rel or rel
                if not any_rel:
                    reasons.append("考纲无关")
                    evid.append("; ".join(det)[:100])
            # ③ 篇幅过短
            if q_len < SHORT_LEN and not has_img:
                reasons.append("篇幅过短")
                evid.append(f"题干有效字数={q_len} 无图")
            # ④ 缺乏解析
            if all((not t.strip()) or PLACEHOLDER_RE.search(t) or NEAR_EMPTY_RE.match(t)
                   for t in a_texts):
                reasons.append("缺乏解析")
                evid.append("答案空/占位: " + (a_all.strip()[:40] or "(空)"))

            entry = {
                "module": module, "paths": paths, "difficulty": difficulty,
                "is_exam": is_exam, "q_len": q_len, "title": B.short_title(head),
                "reasons": reasons, "evidence": evid,
            }
            if any(r in reasons for r in ("难度过低", "考纲无关")):
                # 处置分层：难度过低/篇幅过短 → 降级；仅考纲无关 → 多为元数据缺失，先补码不降级
                if "难度过低" in reasons or "篇幅过短" in reasons:
                    entry["action"] = "降级"
                else:
                    entry["action"] = "补元数据"
                hard.append(entry)
            elif reasons:
                entry["action"] = "复核"
                soft.append(entry)

    hard.sort(key=lambda e: (e["module"], e["paths"][0]))
    soft.sort(key=lambda e: (e["module"], e["paths"][0]))
    print(f"入书题粒度共 {total} 题；硬指标命中 {len(hard)}，仅软标记 {len(soft)}")

    # 报告
    L = []
    L.append("---")
    L.append('title: "习题书低质量题排查清单"')
    L.append("type: 审计报告")
    L.append(f"updated: {B.TODAY}")
    L.append("question_count: " + str(len(hard) + len(soft)))
    L.append("---")
    L.append("")
    L.append(f"# 习题书低质量题排查清单（{B.TODAY}）")
    L.append("")
    L.append(f"> 入书题（大题合并组）共 **{total}** 题。硬指标命中（建议降级）**{len(hard)}** 题；"
             f"仅软标记（供人工复核）**{len(soft)}** 题。")
    L.append("> 硬指标：①difficulty≤2 且非真题；②syllabus_codes 空且 knowledge_points "
             "未命中 02-考纲词表。软标记：③题干<60字无图；④答案空/占位。")
    L.append("")

    def table(rows, note):
        if not rows:
            L.append(f"## {note}（0 条）")
            L.append("")
            return
        L.append(f"## {note}（{len(rows)} 条）")
        L.append("")
        mig = collections.Counter(e["action"] for e in rows)
        L.append("处置建议分布：" + "、".join(f"{k} {n}" for k, n in mig.most_common()))
        L.append("")
        L.append("| 模块 | 难度 | 真题 | 题干字数 | 题目 | 源文件 | 判定理由 | 处置建议 |")
        L.append("|:--|:--|:--|:--|:--|:--|:--|:--|")
        for e in rows:
            L.append(f"| {e['module']} | {e['difficulty']} | {'是' if e['is_exam'] else '否'} "
                     f"| {e['q_len']} | {e['title'] or '(无标题)'} "
                     f"| {'<br>'.join(e['paths'])} | {'；'.join(e['evidence'])} | {e['action']} |")
        L.append("")

    table([e for e in hard if e["action"] == "降级"],
          "硬指标命中·建议降级（难度过低或篇幅过短）")
    table([e for e in hard if e["action"] == "补元数据"],
          "硬指标命中·建议补 syllabus_codes 元数据（内容仍属考纲范围，不降级）")
    table(soft, "仅软标记·供复核")
    REPORT.write_text("\n".join(L), encoding="utf-8")
    print(f"报告已写入: {REPORT}")

    # 候选 JSON（demote_questions.py 输入；只含硬指标命中）
    CAND_JSON.parent.mkdir(exist_ok=True)
    CAND_JSON.write_text(json.dumps({
        "generated": B.TODAY,
        "note": "习题书低质量降级候选（硬指标命中）；demote_questions.py 按此批量降级。",
        "total": len(hard),
        "entries": hard,
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"候选清单已写入: {CAND_JSON}（{len(hard)} 条）")


if __name__ == "__main__":
    main()
