# -*- coding: utf-8 -*-
"""① 习题册制作-执行计划 → completed；② 7 张手写卡补三字段（含链接存在性校验）
   dry 默认；--apply 落盘
"""
import io, os, re, sys

os.chdir(r'C:\Obsidion\妙妙屋')
D = '00-首页/活跃任务'
APPLY = '--apply' in sys.argv

ALL = set()
for dp, dn, fn in os.walk('.'):
    dn[:] = [d for d in dn if d not in ('.git',)]
    for f in fn:
        if f.endswith('.md'):
            ALL.add(os.path.relpath(os.path.join(dp, f), '.').replace('\\', '/')[:-3])

def rd(p): return io.open(p, encoding='utf-8-sig').read()
def wr(p, t): io.open(p, 'w', encoding='utf-8', newline='').write(t)

def split(t):
    m = re.match(r'^---\r?\n(.*?)\r?\n---\r?\n', t, re.S)
    return (m.group(1), t[m.end():], m.start(), m.end()) if m else (None, None, None, None)

def block(key, items):
    return '\n'.join([key + ':'] + ['  - "%s"' % x.replace('"', "'") for x in items])

def ensure_field(fm, key, items, log):
    """写入/替换块列表字段；返回新 fm"""
    keep = []
    for it in items:
        links = re.findall(r'\[\[([^\]|#]+)', it)
        bad = [l for l in links if l.strip().lstrip('./') not in ALL and '.workbuddy/' not in l]
        if bad:
            log.append('   ⚠️ 丢弃不存在的链接 %s（%s）' % (bad, key))
            it = None
        keep.append(it)
    items = [x for x in keep if x]
    if not items:
        log.append('   ⚠️ %s 无有效内容，跳过' % key); return fm
    lines = fm.split('\n')
    idx = None
    for i, l in enumerate(lines):
        if re.match(r'^%s\s*:' % re.escape(key), l):
            idx = i; break
    if idx is None:
        lines.append(block(key, items))
    else:
        j = idx + 1
        while j < len(lines) and re.match(r'^\s+', lines[j]):
            j += 1
        lines[idx:j] = block(key, items).split('\n')
    return '\n'.join(lines)

# ══════ ① 习题册制作 → completed ══════
P1 = os.path.join(D, '习题册制作-执行计划-2026-08-29.md')
t = rd(P1); fm, body, a, b = split(t)
assert fm
n1 = fm
n1 = re.sub(r'^status:[ \t]*.*$', 'status: completed', n1, count=1, flags=re.M)
if not re.search(r'^completed:', n1, re.M):
    n1 = re.sub(r'^(updated:[ \t]*.*)$', r'\1\ncompleted: 2026-08-30', n1, count=1, flags=re.M)
if APPLY and n1 != fm:
    wr(P1, '---\n' + n1 + '\n---\n' + body)
print('① 习题册制作-执行计划 → status: completed ｜ completed: 2026-08-30（依据：执行顺序 A→B→Q-A~Q-D→正式版替换→阶段 D/E 全 ✅）')
print('   status %s' % ('已改' if APPLY else '[dry]'))

# ══════ ② 7 张手写卡补字段 ══════
JOBS = {
 '习题册制作-执行计划-2026-08-29.md': {
   'source_notes': ['2026-08-29 习题书线会话；四篇习题书（化学原理 / 结构化学 / 有机化学 / 元素与分析）由中间态推进至可印刷成品的执行计划',
                    '成书口径依据 [[04-题库/习题集体系总纲]]'],
   'related_notes': ['[[00-首页/活跃任务/习题书V2内容瘦身与排版迭代计划]]', '[[00-首页/活跃任务/任务卡-2026-08-30-题库现状评估与扩充计划]]'],
   'evidence': ['2026-08-30 正式版替换落地：31 章 / 1,685 题、答案块 1,685、无解答占位 0；教师版嵌入图 2,016 张（纯哈希 1,999 / 非哈希 17）',
                '2026-08-30 Word 全量重建 `Done. 31 converted, 0 errors`；样章 `5-对称性与群论.docx` 预检 `Passed: 1, Files with errors: 0`',
                '[[09-审计报告/_归档-历史快照/2026-08-30-习题书新旧对账]]', '[[09-审计报告/_归档-历史快照/2026-08-30-习题书Q-D收尾结论]]'],
 },
 '交接-2026-09-15-备课线收尾核验.md': {
   'source_notes': ['2026-09-15 备课线会话交接；供新会话独立核验课程计划 / 命题分析 / 章后层 / 图库四项产出'],
   'related_notes': ['[[00-首页/活跃任务/待办交接清单]]', '[[备课思路/备课与教学思路待办]]'],
   'evidence': ['本会话交付 19 笔提交（未 push）：`ff2f21ba5` 课程计划 +3 章 5 节、`04dbe080f` 命题拆解扩至 35-40 届、`c7f257357` 章1 复习课 + 习题课等',
                '[[00-首页/工作日志/2026-09-15]]'],
 },
 '任务卡-2026-09-11-讲义ASCII图转图片.md': {
   'source_notes': ['从 [[00-首页/活跃任务/任务卡-2026-09-11-讲义等宽段治理]] 拆分而来（主卡处理可规则化块，本卡处理剩余真图块）'],
   'related_notes': ['[[00-首页/活跃任务/任务卡-2026-09-11-讲义等宽段治理]]'],
   'evidence': ['2026-09-12 批次13：真代码块 34 → 0（换库图 3 + 转正文/表格/嵌套列表 31）；等宽段 705 → 660',
                '2026-09-12 批次14：6 处由「转文本」升级为 RDKit/matplotlib 重画（羧酸根共振式、卡宾单/三线态、NBS 结构式、Re/Si 面、邻基参与、1,2-迁移）；索引登记 6 行',
                '[[00-首页/工作日志/2026-09-11]]', '[[00-首页/工作日志/2026-09-12]]'],
 },
 '任务卡-2026-09-11-讲义等宽段治理.md': {
   'source_notes': ['2026-09-11 讲义线会话；治理讲义 md 中 Word 代码块（围栏块）残留'],
   'related_notes': ['[[00-首页/活跃任务/任务卡-2026-09-11-讲义ASCII图转图片]]', '[[09-审计报告/讲义等宽段治理-口径与清单-2026-09-11]]'],
   'evidence': ['2026-09-12 收官：真代码块 158 → 0（全库归零）',
                '2026-09-13 复核（`.workbuddy/scripts/verbatim_worklist.py`）：活跃源 md 72 份，围栏块总数 = 1（属并行会话新建文件，不在本卡范围）⇒ 本卡范围内剩余 = 0',
                '[[00-首页/工作日志/2026-09-11]]', '[[00-首页/工作日志/2026-09-13]]'],
 },
 '任务卡-2026-09-13-git仓库膨胀治理.md': {
   'source_notes': ['2026-09-13 基础设施 / 运维线会话；`.git` 由 12 GB 治理至 4.3 GB（非知识库内容线）'],
   'related_notes': ['[[00-首页/工作日志/2026-09-13]]'],
   'evidence': ['诊断：`.idx` 有对象 SHA 登记但 `.pack` 无实体数据的**畸形 pack 12 个**（对象数 0~563 却体积 1.6 MB~2.75 GB，`git cat-file -e` 全失败）'],
 },
 '任务卡-2026-09-14-习题书裸下标收口与git健壮性复核.md': {
   'source_notes': ['2026-09-14 习题书线会话交接卡（新开对话入口）；含 §1 会话边界与冲突区、§2 事实快照（本机实测 + 复现命令）'],
   'related_notes': ['[[00-首页/活跃任务/习题书V2内容瘦身与排版迭代计划]]'],
   'evidence': ['[[09-审计报告/习题书Word排版污染治理-2026-09-14]]', '[[09-审计报告/全库docx排版体检-2026-09-14]]',
                '[[09-审计报告/git对象库损坏与恢复-2026-09-14]]', '[[09-审计报告/习题书裸下标-ACD待批清单-2026-09-14]]',
                '[[00-首页/工作日志/2026-09-14]]'],
 },
 '任务卡-2026-09-16-组题收口与两批新批次纳入.md': {
   'evidence': ['2026-09-16 23:30 两批导入材料归位入库：`北斗化学习题/` → `06-外部资料导入/OCR/北斗化学试题/`（与 14 份源 PDF 同目录）；`竞赛教程第二分册测试/` 同目录',
                '北斗 **70 题已入库**（`04-题库/教材习题/北斗学友/`）；《化学竞赛能力测试·高中第二分册》**36 卷 / 357 计分项**入库（提交 `0a9a6c60e`）',
                '题库全量体检 **5,379 题 / 0E 202W / 七字段零缺失**',
                '[[09-审计报告/2026-09-16-题库现状评估与第一轮组题方案]]'],
 },
 '任务卡-PPT制作方法探究与试点.md': {
   'source_notes': ['2026-06 课件 / 讲义线会话；探究 PPT 教学呈现方法并以「原子结构」为试点（2026-06-29 更新：方法试点已完成，正式推广不在当前主线）'],
 },
}

for f, fields in JOBS.items():
    p = os.path.join(D, f)
    t = rd(p); fm, body, a, b = split(t)
    if fm is None:
        print('◆ %s  ⚠️ 无 FM，跳过' % f); continue
    log = []
    nfm = fm
    for k, v in fields.items():
        nfm = ensure_field(nfm, k, v, log)
    print('◆ %s' % f[:56])
    for k in fields:
        print('   + %s' % k)
    for l in log:
        print(l)
    if APPLY and nfm != fm:
        wr(p, '---\n' + nfm + '\n---\n' + body)
print()
print('%s 完成' % ('已应用' if APPLY else 'DRY（加 --apply 落盘）'))
