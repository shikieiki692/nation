# -*- coding: utf-8 -*-
"""本轮提交（机构组卷线）——逐路径精确 add + 暂存区核对 + commit。
只 add 本会话改动；禁目录级 add；禁 --no-verify。
"""
import subprocess, sys, os, glob

sys.stdout.reconfigure(encoding='utf-8')
os.chdir(r'C:\Obsidion\妙妙屋')


def run(args, check=True):
    p = subprocess.run(['git'] + args, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if check and p.returncode != 0:
        print('!! git %s -> %d\n%s\n%s' % (' '.join(args[:2]), p.returncode, p.stdout, p.stderr))
    return p


# ── 0. 基线 ─────────────────────────────────────────────
base = set(x for x in run(['diff', '--cached', '--name-only', '-z']).stdout.split('\0') if x)
print('暂存基线：%d 个' % len(base))

B = '04-题库/2026机构初赛模拟题/'
CARDS = [
    B + 'XeChem/题-XeC-40-04-方钴矿系skutterudi.md',
    B + 'chemy/题-CM-14-04-第111号元素轮是第七周期超.md',
    B + 'chemy/题-CM-175-02-氟磷酸钙中掺杂的平均价态的测.md',
    B + 'chemy/题-CM-19-01-一氟化硼BF是由硼与氟元素形.md',
    B + '伽马/题-GM-05-04-Te的卤化物有着非常丰富的结.md',
    B + '化英社/题-HYS-02-06-在噪声中偏向于随机里定轨在化.md',
    B + '化英社/题-HYS-11-04-分子氙通常被视为惰性物质因为.md',
    B + '北京夏令营/题-BJLY-01-04-人们对低价Ge的研究从未停止.md',
    B + '北京夏令营/题-BJLY-01-07-71一种三价铝物种与足量的钾.md',
    B + '北京夏令营/题-BJLY-01-08-81K结构可描述如下正六边形.md',
    B + '北京夏令营/题-BJLY-02-08-称取与32的乙醇溶液混合然后.md',
    B + '北京夏令营/题-BJLY-02-09-某过渡金属X的单质A在生活中.md',
    B + '清北营/题-QBY-01-07-光合作用是个复杂的过程在人们.md',
    B + '清北营/题-QBY-11-06-多核金I硫化物团簇具有丰富的.md',
    B + '清北营/题-QBY-17-02-碳族元素需要得到或失去四个电.md',
]
OTHER = [
    '04-题库/初赛模拟卷X（非有机·学生版）.md',
    '04-题库/初赛模拟卷X（非有机·答案版）.md',
    '00-首页/题组Word/初赛模拟卷/真题版式/初赛模拟卷X（非有机·学生版·真题版式）.docx',
    '00-首页/题组Word/初赛模拟卷/真题版式/初赛模拟卷X（非有机·答案与解析版·真题版式）.docx',
    '00-首页/活跃任务/交接提示词-2026-10-06-机构模拟题组卷线.md',
    '09-审计报告/2026-10-06-卷X回源三元核验报告.md',
    '09-审计报告/2026-10-06-机构模拟题题库改进方案.md',
    '09-审计报告/2026-10-06-机构题库全量体检报告.md',
    '09-审计报告/2026-10-06-机构题库体检.csv',
    '09-审计报告/2026-10-06-无答案卡回收可行性报告.md',
    '11-模板/规范/机构模拟题组卷管线SOP.md',
    '.workbuddy/memory/MEMORY.md',
    '.workbuddy/memory/2026-10-06.md',
]
TOOLS = ['.workbuddy/tmp/opt_pipe/' + f for f in [
    'build_org.py', 'verify_dump.py', 'pdf_pages.py', 'pdf_text_check.py', 'crop_page.py',
    'probe_text.py', 'trim_save.py', 'extract_ans.py', 'fix_cards_volX.py', 'fix_hys02_ans.py',
    'pool_funnel.py', 'pool_alt.py', 'year_probe.py', 'year_breakdown.py', 'sample_probe.py',
    'pool_census.py', 'inst_census.py', 'audit_org_bank.py',
    'noans_list.py', 'locate_answer_pdf.py', 'ans_inventory.py', 'ans_pairing.py',
    'chk_txt.py', 'fill_bjly1.py', 'fill_bjly2.py', 'dedup_fp.py',
]]
IMGS = (sorted(glob.glob(B + '北京夏令营/images/bjly0*_ans_*.jpg'))
        + [B + '伽马/images/gm05_ans_4-1_Te2Br_TeI.jpg',
           B + '清北营/images/qby17_ans_2-3-3-2_D_F.jpg'])

# ── 1. 存在性核对 ──────────────────────────────────────
missing = [p for p in (CARDS + OTHER + TOOLS + IMGS) if not os.path.exists(p)]
assert not missing, '缺文件：%s' % missing
print('待提交：卡 %d ＋ 其它 %d ＋ 工具 %d ＋ 图 %d = %d'
      % (len(CARDS), len(OTHER), len(TOOLS), len(IMGS), len(CARDS) + len(OTHER) + len(TOOLS) + len(IMGS)))

# ── 2. 逐路径 add ──────────────────────────────────────
for p in CARDS + OTHER:
    run(['add', '--', p])
for p in TOOLS + IMGS:          # .workbuddy/tmp 与 题库 images 被 gitignore ⇒ -f
    run(['add', '-f', '--', p])

def _n(s):
    return s.replace('\\', '/').strip()


staged = set(_n(x) for x in run(['diff', '--cached', '--name-only', '-z']).stdout.split('\0') if x)
intended = set(_n(x) for x in (CARDS + OTHER + TOOLS + IMGS))
extra = staged - intended
miss = intended - staged
print('暂存 %d ；多出 %d ；漏 %d' % (len(staged), len(extra), len(miss)))
if extra:
    print('!! 多出（须排查）：', sorted(extra)[:10])
if miss:
    print('!! 漏：', sorted(miss)[:10])
assert not extra and not miss, '暂存区 != 本会话路径集合 ⇒ 停手'

# ── 3. commit ─────────────────────────────────────────
MSG = ('feat(组卷线): 跨卷同题指纹去重 + 无答案卡回收（北京夏令营 5 张）＋卷X 回源补齐\n'
       '\n'
       '- build_org.py: 题面指纹改 deep_fp + 5-gram Jaccard≥0.80 模糊判重；'
       '既往卷卡指纹种子化 ⇒ 跨卷同题不重选（卷X HYS-40-01 ≡ 卷XI HYS-03-01）\n'
       '- 无答案卡回收：北京夏令营 练习一 4/7/8＋练习二 8/9（题/图/答案回源答案册；'
       '图型小问直抽内嵌位图、文字/公式型裁区免转录）；新增答案图 29 张\n'
       '- 卷X 回源三元核验：10 卡补答案/改字/裁图/删越界段（图 71/71、qa 0）\n'
       '- 新工具：noans_list / locate_answer_pdf / ans_pairing / fill_bjly1,2 / dedup_fp / '
       'pool_census / audit_org_bank / verify_dump / pdf_pages / crop_page 等\n'
       '- 报告：卷X回源核验 / 题库改进方案 / 全量体检 / 无答案卡回收可行性；SOP 定版 v1.0')
p = run(['commit', '-m', MSG])
print('\n--- commit rc=%d ---' % p.returncode)
print(p.stdout[-1500:])
if p.returncode != 0:
    print(p.stderr[-2500:])
else:
    print(run(['log', '--oneline', '-1']).stdout)
