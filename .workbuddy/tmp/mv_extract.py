# -*- coding: utf-8 -*-
"""初赛模拟卷·通用题卡抽取器

各「机构源」的题卡骨架不一致（H1 写法、`## 题目` 有无、答案节标题各异），
北斗专用组装脚本无法复用，故做通用抽取：
  题面 = H1 之后 → 首个答案节标题之前（剥 `> **来源**` 等元信息行）
  答案 = 答案节 → 首个「尾部元数据节」之前

答案节标题：`## 参考答案` / `## 解答` / `## 答案` / 其后可带冒号空格
尾部元数据节：`## 知识点映射` `## 相关题目` `## 解析要点` `## 解题思路`
              `## 知识点` `## 关联` `## 本讲习题` `## 习题`
"""
import re, os

ANS_RE = re.compile(r'^#{2,4}\s*(?:参考答案|解答|答案|详解|解析)\s*[::]?\s*$', re.M)
TAIL_RE = re.compile(
    r'^#{2,4}\s*(?:知识点映射|相关题目|解析要点|解题思路|知识点|考点|'
    r'关联与查重|关联|本讲习题|习题|目录讨论|点评)\s*[::]?\s*$', re.M)
META_LINE = re.compile(r'^>\s*\*\*(?:来源|难度|教学层级|分值)\*\*\s*[:：]')
QTITLE_RE = re.compile(r'^#{2,4}\s*(?:题目|本讲习题|习题)\s*[::]?\s*$', re.M)
DET_RE = re.compile(r'^<details>\s*$', re.M)


def load_card(path):
    t = open(path, encoding='utf-8', newline='').read()
    # CRLF 归一（只读侧；写文件仍按本仓库既有行尾），否则 CR 会混进题意影响后续正则
    t = t.replace('\r\n', '\n').replace('\r', '\n')
    e = [i for i, l in enumerate(t.split('\n')) if i > 3 and l.strip() == '---']
    if not e:
        raise ValueError('无 frontmatter: ' + path)
    lines = t.split('\n')
    fm_raw = '\n'.join(lines[1:e[0]])
    fm = {}
    for ln in fm_raw.split('\n'):
        m = re.match(r'^([A-Za-z_\u4e00-\u9fff]+):\s*(.*)$', ln)
        if m:
            fm[m.group(1)] = m.group(2).strip().strip('"')
    body = '\n'.join(lines[e[0] + 1:])
    return fm, body, path


def extract(path):
    """返回 dict: title / question / answer / source / stars / stage / org / imgs"""
    fm, body, _ = load_card(path)
    # --- H1 剥离，取其后的首段作为题名 ---
    m1 = re.search(r'^#\s+(.+?)\s*$', body, re.M)
    title = m1.group(1).strip() if m1 else os.path.basename(path)[:-3]
    after_h1 = body[m1.end():] if m1 else body

    ans_m = ANS_RE.search(after_h1)
    tail_m = TAIL_RE.search(after_h1)
    # ⚠️ 部分源（化学能力测试等）的答案**没有标题**，直接是 `<details><summary>查看答案…`
    # ⇒ 折叠块起点也必须作为答案起点候选，否则题面会把答案整个吞进去（实测抽成答案 0 字）
    det_m = DET_RE.search(after_h1)
    starts = [x.start() for x in (ans_m, det_m) if x]
    q_end = min(starts) if starts else (tail_m.start() if tail_m else len(after_h1))
    question = after_h1[:q_end]
    # 若题面里显式有 `## 题目`，以其后开始
    qt = QTITLE_RE.search(question)
    if qt:
        question = question[qt.end():]
    # 剥 `> **来源**…` 元信息行与 H1
    question = '\n'.join(l for l in question.split('\n') if not META_LINE.match(l))

    # 答案：答案起点 → 尾部元数据节
    answer = ''
    if starts:
        a_start = min(starts)
        a_start = after_h1.find('\n', a_start) + 1  # 跳过标题行本身
        a_end = len(after_h1)
        t2 = TAIL_RE.search(after_h1, a_start)
        if t2:
            a_end = t2.start()
        answer = after_h1[a_start:a_end]
        # 剥 <details>/<summary> 外壳：Word 里 details 无折叠语义，留着会输出为原始 HTML 或怪段落
        answer = re.sub(r'</?details>', '', answer)
        answer = re.sub(r'<summary>.*?</summary>', '', answer, flags=re.S)
    answer = '\n'.join(l for l in answer.split('\n') if not l.lstrip().startswith('> 答案见'))
    answer = re.sub(r'^>\s*答案见\s*\[\[[^\]]*\]\]\s*$', '', answer, flags=re.M)

    def clean(s):
        s = s.strip('\n')
        s = re.sub(r'\n{3,}', '\n\n', s)
        s = re.sub(r'^\s*---\s*$', '', s, flags=re.M)
        s = re.sub(r'\n{3,}', '\n\n', s)
        return s.strip('\n')

    question, answer = clean(question), clean(answer)
    diff = int(fm.get('difficulty', 0) or 0)
    imgs = re.findall(r'!\[\[([^\]\|]+\.(?:jpg|png|jpeg|gif))', question + answer)
    return dict(
        title=title, question=question, answer=answer,
        source=fm.get('source', ''), source_norm=fm.get('source_norm', ''),
        difficulty=diff, stars='⭐' * diff if diff else '',
        stage=fm.get('exam_stage', ''), module=fm.get('subject_module', ''),
        imgs=imgs, path=path)
