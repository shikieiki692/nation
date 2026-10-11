# -*- coding: utf-8 -*-
"""逐条复现 build_pool 对 HZ-01-06 的判定（对比 HEAD~1 修复前 / HEAD 修复后）。"""
import importlib.util
import os
import re
import subprocess
import sys

VAULT = r"C:\Obsidion\妙妙屋"
OPT = os.path.join(VAULT, ".workbuddy", "tmp", "opt_pipe")
sys.path.insert(0, OPT)
os.chdir(VAULT)

spec = importlib.util.spec_from_file_location("BORG", os.path.join(OPT, "build_org.py"))
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)
B = M.B
X = M.X

REL = "04-题库/2026机构初赛模拟题/汇智/题-HZ-01-06-CuI由于具有灵活多变的配位.md"
TMP = os.path.join(OPT, "qa_tmp_cards")
os.makedirs(TMP, exist_ok=True)


def git_show(rev):
    r = subprocess.run(["git", "show", f"{rev}:{REL}"], cwd=VAULT, capture_output=True)
    return r.stdout.decode("utf-8") if r.returncode == 0 else None


def gate(text, label):
    p = os.path.join(TMP, os.path.basename(REL))
    open(p, "w", encoding="utf-8", newline="").write(text)
    t = text
    hits = []
    m = re.search(r'^subject_module:\s*(.*)$', t, re.M); mod = m.group(1).strip() if m else ''
    m = re.search(r'^exam_stage:\s*(.*)$', t, re.M); stage = m.group(1).strip() if m else ''
    m = re.search(r'^difficulty:\s*(\d+)', t, re.M); diff = int(m.group(1)) if m else 0
    m = re.search(r'^source_norm:\s*(.*)$', t, re.M); norm = m.group(1).strip() if m else ''
    m = re.search(r'^source_file:\s*(.*)$', t, re.M); sf = m.group(1).strip() if m else ''
    m = re.search(r'^source:\s*(.*)$', t, re.M); src = m.group(1).strip() if m else ''

    def rep(cond, name):
        if cond:
            hits.append(name)

    rep(M.in_2526(norm, sf) == 0 and not M.ALL_YEARS, "年份闸(非25-26)")
    rep(bool(M.BATCH_BAD.search(norm)), "讲稿批次")
    rep(mod not in ('元素与分析', '结构化学', '化学原理') or stage == '省预赛', "模块/省预赛")
    rep(diff < 4 or [x for x in B.RISK if x in t], "难度<4 或 RISK")
    tn = re.sub(r'<!--.*?-->', '', t, flags=re.S)
    rep(B.is_cn_prelim(tn) and os.path.basename(p) not in M.load_pool_keep(), "is_cn_prelim")
    h1m = re.search(r'^#\s+(.+)$', t, re.M); h1 = h1m.group(1) if h1m else ''
    rep(bool(B.ORG_CHAP.search(src) or B.ORG_CHAP.search(h1)), "ORG_CHAP")
    c = X.extract(p)
    rawq, rawa = c['question'], c['answer']
    rep(bool(M.PLACEHOLDER.search(rawq)), "占位闸(题面)")
    if M.PLACEHOLDER.search(rawa) and '![' not in rawa:
        _body = "\n".join(l for l in rawa.split("\n")
                          if l.strip() and not M.NOTE_LINE.search(l.strip()))
        rep(len(re.sub(r"\s+", "", _body)) < 25, "占位闸(答案)")
    rep(M.has_fake_struct(rawa) or M.has_fake_struct(rawq), "ASCII 假结构")
    rep((len(rawa) >= 400 and rawa.count('$') == 0 and rawq.count('$') >= 10
         and '![' not in rawa and not re.search(r'[\u4e00-\u9fff]', rawa)), "公式乱码闸")
    q0 = M.conv_imgs(M.clean_q(rawq)); a0 = M.clean_a(M.conv_imgs(rawa), q0)
    q, a = M.html_table_to_md(q0), M.html_table_to_md(a0)
    own = M.own_qno(t, p)
    _qchk = re.sub(r'^#{0,4}[^\S\n]*第[^\S\n]*%s[^\S\n]*[题題][^\n]*$' % M.num_alt(own), '', q, flags=re.M)
    rep(bool(M.LEAK.search(_qchk)), "题面泄露 LEAK")
    qn = re.sub(r'\s+', '', q); an = re.sub(r'\s+', '', a)
    rep(len(an) < 25 or len(qn) < 60, "过短")
    rep(len(B.ORGRE.findall(q + ' ' + a)) >= 3, "ORGRE>=3")
    rep(len(re.findall(r'^\*\*\s*\d{1,2}\s*[.．]\s*\*\*', q + '\n' + a, re.M)) >= 8, "加粗小问>=8")
    rep(bool(M.HANDWRITTEN.search(M._HW_STRIP.sub(' ', q + ' ' + a))), "手写解析稿闸")
    if '![[' not in a:
        _an = re.sub(r'\s+', '', a); _qn = re.sub(r'\s+', '', q)
        _r = M.contain_ratio(_an, _qn)
        rep(len(_an) >= 40 and (_r >= 0.80 or (_r >= 0.70 and len(_an) * (1 - _r) < 80)),
            f"答案可用闸-回显(ratio={_r:.2f})")
        rep(bool(M.GARB2PAT.search(a)), "GARB2 乱码宏")
    _of = M.overflow_reason(q, a, own)
    rep(bool(_of), f"越界闸({_of})")
    print(f"[{label}] own={own} 命中: {hits if hits else '无（在池）'}")
    return hits


head = git_show("HEAD")          # 修复后（=工作区）
prev = git_show("HEAD~1")        # 修复前
print("== 修复后（HEAD）==")
gate(head, "HEAD")
print("== 修复前（HEAD~1）==")
gate(prev, "HEAD~1")
