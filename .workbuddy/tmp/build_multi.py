# -*- coding: utf-8 -*-
"""初赛模拟卷 VI/VII/VIII 通用组卷器（跨机构）

与北斗专用脚本的差异：
- 选题：确定性排序（-难度, -题面长度），按机构轮转 + 模块配额，USED 跨卷去重 ⇒ 可复现
- 抽取：用 mv_extract 通用抽取器（各源骨架不一致）
- 重编号：源小问前缀**从卡内实测**（吸取题-046 教训），只改 `P-M` / `**P-M**`，
          不碰 `(N)` / `①`（避免误伤化学式与条件编号）
- 分值：按题面长度分档由脚本给定，目标整卷 ~150（对齐系列 147~154）
用法：python build_multi.py [--check|--apply] [--vol VI]
"""
import re, sys, os, glob, collections, json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
import mv_extract as X

BASE = '04-题库/教材习题'
QB = '04-题库'
OUTdocx = os.path.join('00-首页', '题组Word', '初赛模拟卷')
SRCS = ['一分册能力测试', '化学能力测试', '上海中学竞赛课程', '汇智竞赛题目',
        'HChO晶体专题', 'HChO配合物专题', '高中化学竞赛教程第一分册',
        '0407物化特训', '化学竞赛初赛讲义',
        # 2026-09-25 全库普查补录（用户点名勿漏 bdwp 系；详规范 §二/§五）
        'HChO方程式专题', '结构化学基础', '高中化学竞赛教程第二分册', '赵鑫光',
        '中级无机化学', '高分子化学与动力学',
        '无机化学第6版Weller/Ch18', '无机化学第6版Weller/Ch19',
        '无机化学第6版Weller/Ch20', '无机化学第6版Weller/Ch21']
RISK = ['存疑', '待回源', '待补', '缺图', '图片缺失', 'TODO', '待核实', '答案缺失', '存议']
ORGRE = re.compile(r'有机|苯环|芳香|羧酸|烯烃|炔烃|醛基|酯基|酰胺|氨基酸|聚合物|亲核|亲电|'
                   r'离去基团|手性碳|构型翻转|Diels|Alder|Wittig|格氏|傅克|重氮|杂环|吡啶|呋喃|'
                   r'噻吩|卟啉|酞菁|冠醚|席夫碱|加成反应|消除反应|催化|烷基|羟基|醌|表面活性剂|重排')
# ── 真题口径（2026-09-22 用户两次澄清后的最终版）─────────────────────
#   ❶ **只排除「国内初赛真题」**——真出自某届国内初赛考卷的题
#   ❷ 国际真题（IChO / 国际化学竞赛）**保留**（用户：「国际真题可以有」）
#   ❸ 决赛题**保留**（用户：「决赛题也可以出现」）
#   ❹ 预赛／省赛／选拔赛／夏令营／赛区选拔／联考／自招 **都不是初赛真题 ⇒ 放行**
#      （第一版按「初赛层级」一刀切把这些也排了，属自行扩大，已被用户纠正收回）
#
# 真题标注有三类写法，只认年份式会漏掉后两类：
#   ① 年份式   「2013年全国初赛」
#   ② 届次式   「第28届中国化学奥林匹克初赛试题」
#   ③ 国际届次 「第 36 届国际竞赛试题」（允许）
CN_PRELIM = re.compile(
    r'(?:19|20)\d{2}\s*年?\s*(?:全国|省|市|中国)?\s*(?:化学\s*)?(?:竞赛\s*)?初赛'
    r'|第\s*\d{1,2}\s*届[^\n]{0,24}?初赛'
    r'|(?:初赛|奥林匹克初赛|中国化学奥林匹克初赛)\s*(?:试题|真题|原题|试卷|考题)')
# 只在「模拟」与「初赛」**紧邻**时才豁免（双向 + 常见试卷名），
# 不要宽泛匹配单个词——「实战演练」这种教程栏目名会把真真题放过去。
SIM_U = re.compile(r'初赛\s*(?:模拟|仿真)|(?:模拟|仿真)[^\n]{0,6}初赛'
                   r'|模拟\s*(?:试卷|试题|题|卷)|初赛\s*(?:自测|预演)')


def is_cn_prelim(blob):
    """国内初赛真题判据。

    命中 CN_PRELIM 后，只看**命中处的上下文**（不是整篇）做两类纠正：
      · 上下文标「国际 / IChO」⇒ 不是国内初赛
      · 上下文标「模拟 / 仿真 / 自测」⇒ 是本系列要收的模拟题，不是真题
    ⚠️ 不能用整篇 blob 判：来源行写「本书含初赛与决赛真题汇编」会把同书所有题误杀。

    🔴 2026-10-07 追加修复：调用方（`build_org.build_pool`）传进来的是**含 frontmatter 的
    整卡文本**，而 FM 的 `source:` 常写「化英社 第40届化英社化学奥林匹克（初赛）春季联考1」
    —— 那是**机构自己模拟卷的卷名**，被当成真题特征；实测 349 张该标记里 **342 张命中在 FM**。
    故此处先剥掉 YAML frontmatter 再判（对只传题面的调用方为 no-op）。
    """
    if blob.lstrip().startswith("---"):
        seg = blob.split("---", 2)
        if len(seg) >= 3:
            blob = seg[2]
    m = CN_PRELIM.search(blob)
    if not m:
        return False
    ctx = blob[max(0, m.start() - 36):m.end() + 24]
    if re.search(r'国际|IChO', ctx):
        return False
    if SIM_U.search(ctx):
        return False
    return True

# 「有机章节」：subject_module 与 source 会打架——丙酮溴化动力学判为化学原理，
# 但 source 白纸黑字写着「第9章 有机化学·B卷」⇒ 只看 module 会放进有机章的题
ORG_CHAP = re.compile(r'有机化学')
# 国际竞赛真题（IChO / 国际化学竞赛）——用户 2026-09-22 明确「国际真题可以有」。
# 必须是「国际竞赛/IChO/第N届国际」这类，**不认孤立的「国际」**（会误中「国际单位制」）。
def is_intl(text):
    """是否国际竞赛真题。命中 INTL_EXACT 后还要排除**引用性表述**——
    如某题注释「（相关试题参见 38th IChO PP）」，那是参考文献不是真题本身，
    按命中即判会把这类题虚报成国际真题（实测虚报 1 道）。"""
    m = INTL_EXACT.search(text)
    if not m:
        return False
    ctx = text[max(0, m.start() - 40):m.end() + 12]
    return not re.search(r'参见|参考|相关试题|详见', ctx)
INTL_EXACT = re.compile(r'国际化学竞赛|国际竞赛|IChO|International\s+Chemistry'
                        r'|第\s*\d{1,2}\s*届\s*国际|国际\s*第\s*\d{1,2}\s*届')
QUOTA = [('元素与分析', '第一部分　元素化学与分析化学', 7),
         ('结构化学', '第二部分　结构化学', 5),
         ('化学原理', '第三部分　化学原理', 4)]
VOL_PREF = {
    'VI': ['一分册能力测试', 'HChO晶体专题', 'HChO配合物专题', '0407物化特训', '高中化学竞赛教程第一分册'],
    'VII': ['化学能力测试', '上海中学竞赛课程', 'HChO晶体专题', '一分册能力测试', '高中化学竞赛教程第一分册'],
    'VIII': ['化学竞赛初赛讲义', '一分册能力测试', 'HChO配合物专题', '化学能力测试', '0407物化特训',
             '高中化学竞赛教程第一分册'],
    'IX': ['上海中学竞赛课程', '高中化学竞赛教程第一分册', '化学能力测试', '一分册能力测试',
            'HChO晶体专题', 'HChO配合物专题'],
}


def normalize_dd(txt):
    """按块结构规范化 `$$` 显示数学：块外补空行（独立成块）＋ 块内删空行。

    ⚠️ 不可用两条独立正则分别做（会互相打架，见文件头注释）。
    """
    lines = txt.split(chr(10))
    out = []
    in_math = False
    one_line = re.compile(r'^\$\$(.+)\$\$$')
    i = 0
    n = len(lines)
    while i < n:
        l = lines[i]
        s = l.strip()
        if not in_math:
            if s == '$$':
                if out and out[-1].strip() != '':
                    out.append('')
                out.append('$$')
                in_math = True
                i += 1
                continue
            if one_line.match(s):
                if out and out[-1].strip() != '':
                    out.append('')
                out.append(s)
                if i + 1 < n and lines[i + 1].strip() != '':
                    out.append('')
                i += 1
                continue
            out.append(l)
            i += 1
            continue
        # 块内
        if s == '':
            i += 1
            continue
        if one_line.match(s):
            out.append(s)
            in_math = False
            if i + 1 < n and lines[i + 1].strip() != '':
                out.append('')
            i += 1
            continue
        if s.endswith('$$'):
            out.append(l)
            in_math = False
            if i + 1 < n and lines[i + 1].strip() != '':
                out.append('')
            i += 1
            continue
        out.append(l)
        i += 1
    return chr(10).join(out)

def score_of(q):
    """按题面长度分档给分（源卡多无分值，由本系列统一拟定），目标整卷落入 147~156"""
    return 12 if q >= 2000 else (11 if q >= 1400 else (10 if q >= 700 else (9 if q >= 450 else (8 if q >= 250 else 6))))


# ── 逐条目检后的人工处置 ────────────────────────────────────────────────
# 「有机/催化/吡啶」等词常常只是无机题的语境陪衬（18e 羰基物、阻燃剂应用、
# 甲醇燃料电池、吡啶作配体），但这些不是：
EXCLUDE = {
    # 涉真实有机反应：C₂H₅OH + SOCl₂ → C₂H₅Cl，并在答案里写「亲核取代反应」
    '题-060-上海中学-离子反应-习题2',
    # 三叶结 / 索烃 + 有机配体模板合成，系超分子有机方向
    '题-354-化学能力测试-Ch4B-9-三叶结与索烃模板合成',
}


def build_pool():
    pool = collections.defaultdict(list)
    for rel in SRCS:
        for p in sorted(glob.glob(os.path.join(BASE, rel, '**', '题-*.md'), recursive=True)):
            t = open(p, encoding='utf-8').read()
            def g(k):
                m = re.search(r'^' + k + r':\s*(.*)$', t, re.M)
                return m.group(1).strip() if m else ''
            mod, stage, diff = g('subject_module'), g('exam_stage'), int(g('difficulty') or 0)
            u, src = g('used_in'), g('source')
            if os.path.basename(p)[:-3] in EXCLUDE:
                continue
            if mod not in ('元素与分析', '结构化学', '化学原理') or stage == '省预赛':
                continue
            if '初赛模拟卷' in u or [x for x in RISK if x in t]:
                continue
            # ⚠️ 真题字样可能落在**四处**：文件名 / source / FM title / 正文 H1。
            #    只查 basename+source 会漏掉把「（2013年全国决赛）」「（竞赛真题）」
            #    写在 H1 里的卡（实测漏进两张）。
            h1m = re.search(r'^#\s+(.+)$', t, re.M)
            h1 = h1m.group(1) if h1m else ''
            # 🔴 排除国内初赛真题必须用**全文**（去 HTML 注释），不能用标题+摘要：
            #    实测 31 张卡的初赛标记藏在这些地方，标题口径全部看不见——
            #      · FM `特别说明`：含第28届中国化学奥林匹克初赛真题
            #      · FM `tags`    ：tags: [化竞, 教程一分册, 2003初赛]
            #      · 题面中断    ：**8.**（1997年全国初赛试题）…
            #      · 校勘注      ：源文把本题与第 31 届全国初赛第 1 题 1-5 同题
            #    漏排初赛真题是用户明令禁止的硬约束 ⇒ 宁可误排也不能漏。
            tn = re.sub(r'<!--.*?-->', '', t, flags=re.S)
            if is_cn_prelim(tn):
                continue
            if ORG_CHAP.search(src) or ORG_CHAP.search(h1):
                continue
            if diff < 4:
                continue
            try:
                c = X.extract(p)
            except Exception:
                continue
            q = re.sub(r'\s+', '', c['question'])
            a = re.sub(r'\s+', '', c['answer'])
            if len(a) < 20 or len(q) < 60:
                continue
            if len(ORGRE.findall(c['question'] + ' ' + c['answer'])) >= 3:
                continue
            # 「练习集卡」：上海中学-化学动力学基础-习题1 实为 16 道独立小题的集合
            # （`**2.**`~`**17.**`，每题各有一套数据），当一道 10 分大题既不成立也不好排分
            if len(re.findall(r'^\*\*\s*\d{1,2}\s*[.．]\s*\*\*', c['question'] + '\n' + c['answer'], re.M)) >= 8:
                continue
            c['qlen'] = len(q)
            c['src_dir'] = rel
            # ⚠️ 判国际真题要**含 H1**：教程一分册那批的国际届次写在 H1 里
            #   （「第1讲 物质的量【竞赛对接】例5（第 36 届国际竞赛试题）」），
            #    只查 basename+source+题面会漏掉 4 张。
            # ⚠️ 要用**原始全文**（剥掉 HTML 注释）判定，不能用抽取后的 question：
            #    教程一分册那批的国际届次写在正文的 `> **来源**：…（第 36 届国际竞赛试题）` 行，
            #    而抽取器会把 `> **来源**` 当元数据剥掉 ⇒ 按 question 判会漏 4 张。
            tn = re.sub(r'<!--.*?-->', '', t, flags=re.S)
            c['intl'] = is_intl(tn)
            pool[mod].append(c)
    return pool


def vote_prefix(c):
    """从卡内实测源小问前缀 P（`**P-M**` 优先，其次裸 `P-M`）

    ⚠️ 投票后**必须回查计数**：只看 Counter 会把 `(2026-09-18)` 一类日期、路径里的
    数字串投成前缀。实测「上海中学-化学动力学基础-习题1」投出 P=9，卡内却一个
    `9-M` 都没有 —— 本次因凑不出匹配侥幸没误改，但这是悬在头上的刀。
    """
    blob = c['question'] + '\n' + c['answer']
    star = collections.Counter()
    for m in re.finditer(r'\*\*\s*(\d{1,2})[-.．]\s*(\d{1,2})\s*\*\*', blob):
        star[int(m.group(1))] += 1
    bare = collections.Counter()
    for m in re.finditer(r'(?<![\w\d.])(\d{1,2})-(\d{1,2})(?![\w\d.])', blob):
        v = int(m.group(1))
        if 1 <= v <= 30:
            bare[v] += 1
    vc = collections.Counter()
    for k, n in star.items():
        vc[k] += n * 2
    for k, n in bare.items():
        vc[k] += n
    if not vc:
        return None
    cand, _ = vc.most_common(1)[0]
    # 回查：该前缀必须真的能以 **P-M** 或 裸 P-M 的形式出现
    if star.get(cand, 0) == 0 and bare.get(cand, 0) == 0:
        return None
    return cand


def renumber(text, new_no, prefix):
    if prefix is None:
        return text
    p = str(prefix)
    text = re.sub(r'\*\*\s*' + p + r'\s*[-.．]\s*(\d{1,2})\s*\*\*',
                  lambda m: '**%d-%s**' % (new_no, m.group(1)), text)
    text = re.sub(r'(?<![\w\d.])' + p + r'-(\d{1,2})(?![\w\d.])',
                  lambda m: '%d-%s' % (new_no, m.group(1)), text)
    return text


def student_clean(s):
    """学生版净化：剔 HTML 校勘注 + 「与真题同题/小问移除」类说明。

    卷 I~V 的学生版已按此口径生成；本批次初版漏做，导致学生版里出现
    「原书 14-4 小问与 …第25届决赛真题… 完全同题」——既泄露真题信息又暴露编排痕迹。
    """
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    # ⚠️ 必须**整行**匹配，不能用 `[^）]{0,400}）` 非贪婪到第一个右括号：
    #    这类句子内部常有嵌套括号（如「X（Au 57.43%，Bartlett 类比），按 SOP…」），
    #    非贪婪会在嵌套的 `）` 处收尾，只删前半句、残留「，按 SOP「完全同题不入库」…）」
    #    半句在校勘注里——实测卷 VIII 第14题就是这么漏的。
    s = re.sub(r'(?m)^[ \t]*（原书.*）[ \t]*$', '', s)
    s = re.sub(r'(?m)^[ \t]*（\s*\d{1,2}-\d{1,2}\s*解答随小问移除.*）[ \t]*$', '', s)
    # 题面开头的**出处括注**也属「题目来源」，学生版一并剥掉（答案版保留以溯源）：
    #   「（第 17 届 IChO 试题）制备含 O₂⁻…」「（第40届IChO试题）当将氯气通入…」
    #   只认**段首**且内容必含赛事标志词的括注，避免误伤正文里的普通括号。
    for _ in range(2):
        s2 = re.sub(r'^[（(]\s*[^）)]{0,26}?'
                    r'(?:IChO|国际竞赛|国际化学|竞赛试题|联赛|联考|自招|初赛|决赛|真题|原题)'
                    r'[^）)]{0,12}?[）)]\s*', '', s, count=1, flags=re.M)
        if s2 == s:
            break
        s = s2
    s = re.sub(r'\n{3,}', '\n\n', s)
    return s.strip('\n')


def strip_src_no(text, prefix):
    """删正文开头的源题序号（`**2.**` / `**题目**：` / 裸 `9.`）。

    ⚠️ 不能只按 vote_prefix 剥：上海中学卡正文以 `**2.**` 开头但卡内没有 `P-M`，
        vote_prefix 返回 None ⇒ 源题序号会原样留在卷里（卷内已有 ### 第 N 题统领，
        「**2.**」既误导又破坏观感）。故一律按行首形态剥，且只认
       `**N.**`（点号），避开 HChO 卡题面开头的小问标签 `**1-1**`。

    ⚠️ 裸 `9.` 比加粗形式更危险：**小问编号也长这样**（卷 VIII 第 1 题题面就以
       「1. 推出 A~E…」开头）。判据取「首行序号 ≠ 1 **且** 文内存在从 1 起的小问」：
         首行 `9.` + 小问 `(1)(2)`  ⇒ 9 是源题号，剥
         首行 `1.` + 小问 `(1)(2)`  ⇒ 1 就是第 1 问，留
    """
    s = text.strip('\n')
    s = re.sub(r'^\*\*\s*\d{1,2}\s*[.．、]\s*\*\*[\s　]*', '', s, count=1)
    s = re.sub(r'^\*\*\s*题目\s*\*\*\s*[：:]\s*', '', s, count=1)
    m = re.match(r'^(\d{1,2})\s*[.．]\s+', s)
    if m and int(m.group(1)) != 1:
        rest = s[m.end():]
        has_subs = bool(re.search(r'[(（]1[)）]', rest)) or bool(re.search(r'^\s*1\s*[.．]\s+', rest, re.M))
        if has_subs:
            s = rest
    return s


def _unused(x):
    return x


def pick_vol(pool, vol, used, intl_first=False, minq=0, max_per_src=99):
    """minq：题面最短字数（卷 IX 要求全是大题 ⇒ 250）
        max_per_src：同一机构每卷最多几题（防一家独大，卷 IX 取 3）"""
    picks = []
    per_src = collections.Counter()
    for mod, _, need in QUOTA:
        by_src = collections.defaultdict(list)
        for c in sorted(pool[mod], key=lambda x: (-x['difficulty'], -x['qlen'])):
            if c['path'] in used:
                continue
            if c['qlen'] < minq:
                continue
            by_src[c['src_dir']].append(c)
        order = VOL_PREF[vol] + [s for s in SRCS if s not in VOL_PREF[vol]]
        got, r = [], 0
        # 卷 IX：国际竞赛真题优先（用户「国际真题可以有」），取够 need 的 2/3 即收手，
        # 剩下留给机构轮转，保证跨机构分布不被国际真题挤掉
        if intl_first:
            intl = [c for lst in list(by_src.values()) for c in lst
                    if c.get('intl') and c['qlen'] >= 150]
            intl.sort(key=lambda x: (-x['difficulty'], -x['qlen']))
            # 国际真题对机构上限**放宽 1 题**：否则教程一分册在结构/元素段占满 3 题后，
            # 原理段那 2 张国际竞赛改编题就再也进不来（实测正是如此）。
            for c in intl[: max(1, need * 2 // 3)]:
                if per_src[c['src_dir']] >= max_per_src + 1:
                    continue
                got.append(c)
                used.add(c['path'])
                per_src[c['src_dir']] += 1
                by_src[c['src_dir']].remove(c)
        while len(got) < need and r < 10:
            prog = False
            for s in order:
                if len(got) >= need:
                    break
                if per_src[s] >= max_per_src:
                    continue
                lst = by_src.get(s, [])
                if r < len(lst):
                    got.append(lst[r])
                    used.add(lst[r]['path'])
                    per_src[s] += 1
                    prog = True
            if not prog:
                break
            r += 1
        picks.append((mod, got))
    return picks


def desc_of(c):
    """题名：优先取 H1 里的语义部分；若 H1 只是文件名复读，退回 source 派生"""
    t = c['title']
    nm = os.path.basename(c['path'])[:-3]
    # 剥 `题-NNN-源缩写-` 一类的编号前缀
    s = re.sub(r'^[^\u4e00-\u9fff]{0,24}[-–—]\s*', '', t)
    s = re.sub(r'^\s*题[-–]?\d{1,4}[-–.．\s]*', '', s)
    # 上海中学卡 H1 形如「题-053-2：盐类溶解度…」，剥前缀后会剩「2：…」
    s = re.sub(r'^\s*\d{1,2}\s*[：:]\s*', '', s)
    s = s.strip(' 　-–—:：')
    # H1 与文件名高度重合 ⇒ 无语义信息，退回 source
    if len(s) < 6 or s.replace(' ', '') in nm.replace(' ', ''):
        src = c['source_norm'] or c['source'] or ''
        s = re.sub(r'^.*?·', '', c['source'])[:40].strip() or src
        s = s or '综合推断题'
    return s[:40]


def esc(s):
    """frontmatter 值：js-yaml4 遇裸 `: ` / 行首特殊符会 THROW（Obsidian 里文件直接消失）"""
    s = str(s)
    if (':' in s and re.search(r':\s|\s:', s)) or s[:1] in ('*', '[', '{', '&', '!', '|', '>', '%', '@', '`') \
            or s[:1] == '-' or '\n' in s or '"' in s:
        s = '"' + s.replace('\\', '').replace('"', "'") + '"'
    return s


CN_NUM = {6: 'VI', 7: 'VII', 8: 'VIII'}


def write_vol(vol, picks, flat):
    ROM = ['VI', 'VII', 'VIII', 'IX']
    assert vol in ROM, vol
    rom = vol
    total = sum(score_of(c['qlen']) for _, c, _ in flat)
    orgs = sorted({c['src_dir'] for _, c, _ in flat})
    seg_start = {}
    idx = 1
    for mod, got in picks:
        seg_start[mod] = (idx, idx + len(got) - 1)
        idx += len(got)
    seg_score = {}
    for mod, got in picks:
        seg_score[mod] = sum(score_of(c['qlen']) for c in got)

    n4 = sum(1 for _, c, _ in flat if c['difficulty'] == 4)
    n5 = sum(1 for _, c, _ in flat if c['difficulty'] == 5)
    nfin = sum(1 for _, c, _ in flat if c['stage'] == '决赛')
    n_intl = sum(1 for _, c, _ in flat if c.get('intl'))

    ans, stu = [], []
    for tag, out in (('答案版', ans), ('学生版', stu)):
        is_ans = (tag == '答案版')
        out.append('---')
        out.append('title: 初赛模拟卷%s（非有机·%s）' % (rom, tag))
        out.append('type: 题组')
        out.append('role: 竞赛模拟训练卷')
        out.append('created: 2026-09-22')
        out.append('updated: 2026-09-22')
        out.append('tags: [化竞, 模拟卷, 初赛, 非有机, 多源]')
        # 学生版不暴露来源机构名（用户对 canvas 的要求：「不要出现题目来源和难度」）
        out.append('source: ' + ('题库多家机构合编' if not is_ans
                                 else esc('题库多家机构合编（含 ' + '、'.join(orgs) + '）')))
        out.append('source_category: 竞赛导向·竞赛教辅')
        out.append('exam_stage: 初赛')
        out.append('question_count: %d' % len(flat))
        out.append('满分: %d' % total)
        out.append('---')
        out.append('')
        out.append('# 初赛模拟卷 %s（非有机 · %s）' % (rom, tag))
        out.append('')
        # 前序卷列表按卷序号自动推导，别硬编码（加卷 IX 时这里会 ValueError）
        allv = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX']
        segtxt = '、'.join(
            '%s（第 %d–%d 题，%d 分）' % (lbl, seg_start[m][0], seg_start[m][1], seg_score[m])
            for m, lbl, _ in QUOTA)
        if is_ans:
            prev = ', '.join('[[04-题库/初赛模拟卷%s（非有机·答案版）|卷 %s]]' % (x, x)
                             for x in allv[:allv.index(vol)])
            out.append('> **组卷口径**：16 题跨 **%d 个来源机构**抽取（%s），均满足 '
                       '`exam_stage=初赛`、`difficulty≥⭐⭐⭐⭐`、`fidelity=原书逐字`；'
                       '**已剔除全部有机化学题目与国内初赛真题**%s，并与 %s 用题零重复。'
                       % (len(orgs), '、'.join(orgs),
                          ('；按用户口径**保留国际竞赛真题 %d 题**与决赛难度题' % n_intl) if n_intl else
                          '（国际竞赛真题与决赛难度题按用户口径允许）', prev))
            out.append('> **范围**：' + segtxt + '，**满分 %d 分，建议用时 180 分钟**；'
                       '难度 ⭐⭐⭐⭐ ×%d、⭐⭐⭐⭐⭐ ×%d。' % (total, n4, n5))
            out.append('> 题卡溯源见卷末选题清单。')
        else:
            # 学生版：只给作答所需信息，与 I~V 学生版形态一致（无来源、无难度、无清单指引）
            out.append('> **考试说明**：本卷共 16 题，满分 %d 分，建议用时 180 分钟。' % total)
            out.append('> **范围**：' + segtxt + '。')
            out.append('> 请将答案写在答题纸上，写出必要的推理与计算过程。')
        out.append('')
        out.append('---')
        out.append('')

        cnt = 0
        for mod, lbl, _ in QUOTA:
            got = dict(picks)[mod]
            out.append('## %s（第 %d–%d 题，共 %d 分）' % (lbl, seg_start[mod][0], seg_start[mod][1], seg_score[mod]))
            out.append('')
            for i, c in enumerate(got, seg_start[mod][0]):
                cnt += 1
                sc = (c.get('fixed_score') or score_of(c['qlen']))
                pre = vote_prefix(c)
                q = renumber(strip_src_no(c['question'], pre), i, pre)
                a = renumber(strip_src_no(c['answer'], pre), i, pre)
                # 学生版**不写题名**：题卡标题多为「高中化学竞赛教程第一分册 第1讲【竞赛对接】例5」
                # 「初赛讲义 第8讲…习题8.13」「（第17届IChO）」这类的出处描述，
                # 属「题目来源」——用户明令学生版不得出现。与系列 I~V 学生版形态对齐：
                # 只留 `### 第 N 题（M 分）`，题面直接开始。
                out.append('### 第 %d 题（%d 分）%s' % (i, sc, desc_of(c) if is_ans else ''))
                out.append('')
                if is_ans:
                    srcshort = c['source'] or c['src_dir']
                    out.append('> 来源：%s｜难度 %s' % (srcshort, c['stars'] or '—'))
                    out.append('')
                out.append(q if is_ans else student_clean(q))
                out.append('')
                if is_ans:
                    out.append('#### 答案')
                    out.append('')
                    out.append(a)
                    out.append('')
                out.append('---')
                out.append('')
        # 卷末选题清单：只给答案版（学生版不溯源、不标难度与来源）
        if is_ans:
            # 卷末清单
            out.append('## 附：选题清单（题卡溯源）')
            out.append('')
            out.append('| 卷内题号 | 分值 | 题名 | 题卡 | 来源 | 难度 |')
            out.append('|:---:|:---:|---|---|---|:---:|')
            for i, c, _sub in [(None, cc, None) for _, cc, _ in flat]:
                pass
            n = 0
            for mod, got in picks:
                for c in got:
                    n += 1
                    rel_p = os.path.relpath(c['path'], '.').replace(os.sep, '/')
                    out.append('| %d | %d | %s | [[%s\\|%s]] | %s | %s |' % (
                        n, (c.get('fixed_score') or score_of(c['qlen'])), desc_of(c), rel_p,
                        os.path.basename(c['path'])[:-3], c['src_dir'], c['stars'] or '—'))
            out.append('')
            out.append('合计 %d 分；难度 ⭐⭐⭐⭐ ×%d、⭐⭐⭐⭐⭐ ×%d；有机化学 0 题、真题 0 题；跨 %d 个来源机构。'
                       % (total, n4, n5, len(orgs)))
            out.append('> 难度星级取自题卡 `difficulty` 字段。**本库 `exam_stage` 字段不可信**（同一难度既标初赛又标决赛），故本卷不按考段标注。')
        out.append('')

    for tag, out in (('答案版', ans), ('学生版', stu)):
        txt = '\n'.join(out)
        # 规范 `$$` 块：夹在 `$$` 与公式之间的空行会让 pandoc 的 tex_math_dollars 放弃识别，
        # 整块降级为碎片 + 字面 $$（实测卷 VIII 第 8 题三块）。
        # 注意要在**成卷 md 源**上修，只在 docx 管线里修会导致「md 与 docx 口径不一致」。
        txt = normalize_dd(txt)
        p = os.path.join(QB, '初赛模拟卷%s（非有机·%s）.md' % (rom, tag))
        open(p, 'w', encoding='utf-8', newline='\n').write(txt)
    print('  → 卷 %s 已写出（%d 题 / %d 分 / %d 机构）' % (rom, len(flat), total, len(orgs)))
    return flat


PLAN_PATH = os.path.join('.workbuddy', 'tmp', 'vol_plan.json')


def load_plan(vols):
    """按固化清单重建 picks；卡片内容仍实时抽取（内容可变，选题与分值不变）。

    动机（本轮踩到的真坑）：pick 依赖 pool，而 pool 会因「回填 used_in」这一动作
    本身而改变（48 张候选被自己排除）⇒ 重跑选题整体漂移（156 分漂到 146 分）。
    有 plan 后不再重新挑选，组卷幂等。
    """
    if not os.path.exists(PLAN_PATH):
        return None
    plan = json.load(open(PLAN_PATH, encoding='utf-8'))
    res = {}
    for vol in vols:
        if vol not in plan:
            continue
        picks = []
        for mod, items in plan[vol]:
            got = []
            for it in items:
                c = X.extract(it['path'])
                c['qlen'] = len(re.sub(r'\s+', '', c['question']))
                c['src_dir'] = it['src_dir']
                c['fixed_score'] = it['score']
                # intl **从原文重判**，不依赖 plan 存储：旧 plan 没有该字段，
                # 照 plan 读会得到 False ⇒ 卷头「保留国际竞赛真题 N 题」算出 0。
                tn = re.sub(r'<!--.*?-->', '', open(it['path'], encoding='utf-8').read(), flags=re.S)
                c['intl'] = is_intl(tn)
                got.append(c)
            picks.append((mod, got))
        res[vol] = picks
    return res


def save_plan(allpicks):
    out = {}
    for vol, picks in allpicks.items():
        out[vol] = [[mod, [dict(path=c['path'].replace(os.sep, '/'), src_dir=c['src_dir'],
                                score=(c.get('fixed_score') or score_of(c['qlen'])),
                                intl=bool(c.get('intl')))
                           for c in got]]
                    for mod, got in picks]
    json.dump(out, open(PLAN_PATH, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('  [plan] 选题已固化 ->', PLAN_PATH)


def main():
    args = sys.argv[1:]
    mode = 'apply' if '--apply' in args else 'check'
    vols = [a for a in args if a in VOL_PREF] or ['VI', 'VII', 'VIII', 'IX']
    # 混合模式：plan 里有的卷照 plan 组装；plan 缺的卷（如新增的 IX）再动态挑，
    # 且动态挑之前必须把 plan 已占用的题灌进 used ⇒ 否则会与前几卷撞题。
    fixed = load_plan(vols) or {}
    allpicks = dict(fixed)          # ← 先装入 plan 里已有的卷，不可漏
    used = set()
    for _v in fixed:
        for _m, got in fixed[_v]:
            for c in got:
                used.add(c['path'])
    dyn = [v for v in vols if v not in fixed]
    if dyn:
        print('  [plan] 固化清单缺 %s ⇒ 仅对这些卷动态挑选（其余照 plan）' % dyn)
        pool = build_pool()
        for vol in dyn:
            allpicks[vol] = pick_vol(pool, vol, used,
                                     intl_first=(vol == 'IX'),
                                     minq=(250 if vol == 'IX' else 0),
                                     max_per_src=(3 if vol == 'IX' else 99))
    else:
        print('  [plan] 命中固化清单 %s，跳过动态挑选' % sorted(fixed))
        allpicks = fixed
    for vol in vols:
        picks = allpicks[vol]
        flat = [(mod, c, i) for mod, got in picks for i, c in enumerate(got, 1)]
        total = sum((c.get('fixed_score') or score_of(c['qlen'])) for _, c, _ in flat)
        orgs = sorted({c['src_dir'] for _, c, _ in flat})
        print('=' * 96)
        print(f'卷 {vol}   {len(flat)} 题   满分 {total}   机构 {len(orgs)}')
        if mode == 'check':
            for mod, c, i in flat:
                hits = ORGRE.findall(c['question'] + ' ' + c['answer'])
                pre = vote_prefix(c)
                print(f'  {i:2d} d{c["difficulty"]}{"决" if c["stage"]=="决赛" else "初"} '
                      f'q{c["qlen"]:5d} {(c.get("fixed_score") or score_of(c["qlen"])):2d}分 '
                      f'前缀{pre} 图{len(c["imgs"])} '
                      f'有机{len(hits)} [{c["src_dir"][:12]:12s}] {os.path.basename(c["path"])[:-3][:44]}')
        else:
            write_vol(vol, picks, flat)
    # ⚠️ 不能只在 plan 不存在时保存：加了新卷（IX）后 plan 已存在但缺该卷,
    #    不覆盖写 ⇒ 下次跑会重新动态挑（而候选池已因回填改变）⇒ 选题漂移。
    if mode != 'check':
        save_plan(allpicks)
    return 0


if __name__ == '__main__':
    sys.exit(main())
