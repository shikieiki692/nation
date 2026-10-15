# -*- coding: utf-8 -*-
import os, subprocess, sys, time, re
os.chdir(r'C:\Obsidion\妙妙屋')

def run(a):
    return subprocess.run(a, capture_output=True, text=True, encoding='utf-8', errors='replace')

st = run(['git', '-c', 'core.quotepath=false', 'status', '--short', '--untracked-files=all',
          '09-审计报告', '11-模板/规范']).stdout
EXCLUDE = {'09-审计报告/2026-10-06-机构题库体检.csv'}      # 并行会话在改
files = []
for ln in st.split('\n'):
    if not ln.strip():
        continue
    p = ln[3:].strip().strip('"')
    if not p.endswith(('.md', '.csv')):
        continue
    if p in EXCLUDE or 'chemy' in p or '图升级线' in p or '图线' in p:
        continue
    files.append(p)
files = sorted(set(files))
print('提交清单 %d 个' % len(files))
for p in files[:8]:
    print('   ', p)
print('    …' if len(files) > 8 else '')

run(['git', 'reset', '-q', 'HEAD'])
for i in range(0, len(files), 100):
    run(['git', 'add', '-f', '--'] + files[i:i + 100])
got = [x for x in run(['git', '-c', 'core.quotepath=false', 'diff', '--cached', '--name-only']).stdout.split('\n') if x]
if sorted(got) != sorted(files):
    print('staged 不符：', sorted(set(got) ^ set(files))[:8])
    run(['git', 'reset', '-q', 'HEAD'])        # 失败也清暂存
    sys.exit(2)
print('staged == files (%d) ✓' % len(files))

MSG = ('docs(治理): 审计目录 type 归一 + 未跟踪报告补 FM 入库 + 规范目录补 FM\n\n'
       '- A. 09-审计报告 非规范 type **18 个全部归一为 `审计报告`**（巡检报告3/报告2/分析报告1/建卡报告1/评估报告1'
       ' + 方案/规范/计划/计划台账/任务/工作文档2/会话交接3）⇒ 该目录非归档仅剩 8 个非规范（**全在 chemy 并行领地**）\n'
       '- B. 09-审计报告 **11 个未跟踪·无 FM 报告补 FM 并首次入库**（题库全面审计×3／全库结构体检／auto-validation×7）\n'
       '- C. 11-模板/规范 **4 个无 FM 补 FM**（type 沿用同目录主流 `规范`）：组卷卡池安全闸门／组卷管线总览／'
       '讲义学习目标考纲锚点规范／讲义练习区格式规范\n'
       '- 另入库 2 个未跟踪审计产物（2026-10-05 磁盘审计报告、2026-10-07 正文重复卡诊断清单.csv）\n'
       '- 护栏：三重断言（正文逐字未变／FM 严格解析／行数增量）＋ 幂等 0 ＋ 备份（保留相对路径）\n'
       '- 闸门：FM strict 34/34；未碰并行文件（机构题库体检.csv／chemy*／图线*）')

for i in range(6):
    r = run(['git', 'commit', '--only', '-m', MSG, '--'] + files)
    if r.returncode == 0:
        print(r.stdout[-120:])
        break
    if 'cannot lock ref' in (r.stderr or ''):
        time.sleep(1.5)
        continue
    print('FAIL')
    print((r.stdout + r.stderr)[-900:])
    run(['git', 'reset', '-q', 'HEAD'])
    sys.exit(1)
run(['git', 'reset', '-q', 'HEAD', '--'] + files)
o = run(['git', '-c', 'core.quotepath=false', 'show', '--stat', 'HEAD']).stdout
print(re.findall(r'\d+ files? changed.*', o))
