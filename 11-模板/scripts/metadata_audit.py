#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""元数据体检（只读）—— FM 解析 / type / role / 值隐患 四维一次扫。

用法：
    python metadata_audit.py                    # 全库摘要
    python metadata_audit.py --scope 00-首页 09-审计报告
    python metadata_audit.py --report <输出.md>

判据来源：
  - type 三层枚举（系统/活跃任务卡/工作日志）＝ 00-首页/_治理-规范/Frontmatter角色词表.md §二
    （**只适用于前台系统层**；题库/知识点/课件等内容域各有自己的 type，不在此列）
  - role 词表 ＝ 同文件 §三（含本会话新增 会话交接 / 启动提示词）
  - FM 严格解析 ＝ ruamel YAML 1.2 safe + 拒重复键（与 jsyaml_verify.js 同后端）

退出码：0 = 无 P1 问题；1 = 有 P1（FM 解析失败）；2 = 参数错误。
"""
import argparse
import collections
import datetime as _dt
import io
import os
import re
import sys

from ruamel.yaml import YAML

# ---- 系统层 scope（type 三层枚举适用的目录）----
# 仅列「整目录都是系统层」的目录。注意 06-学生侧材料 / 备课思路 是
# 混合目录（既有系统 README，也有内容页如 学生讲义/测试卷/教学过程），
# 其内容型 type 属各域自有体系，不按系统层判 —— 故不入本表。
SYS_SCOPE = {'00-首页', '02-数据库', '10-索引与统计'}
SPILL = {'01-考纲导航', '02-考纲条目', '03-知识点', '04-专题与题型', '05-真题库', '05-问答',
         '07-资料提炼', '09-审计报告'}
SPEC_TYPE = {'系统', '活跃任务卡', '工作日志'}
SPEC_ROLE = {
    '人工入口', '人工导览', '会话快照', '执行聚合', '方向指引', '关系说明', '执行协议',
    '标准作业流程', '速查卡', '任务调度参考', '操作说明', '工具说明', '资源索引', '日志索引',
    '方法论', '历史缺口 / 监控', '历史评估样例', '维护备忘', '规范词表', '质量仪表', '架构设计',
    '模块级连接推进', '模块级连接覆盖', '挂接度巡检', '治理规划', '会话交接', '启动提示词',
}
# 源材料目录：无 FM 属正常
RAW_SCOPE = {'06-外部资料导入', '2026机构初赛模拟题', '2026其他资料', 'chemy试题', 'minerai',
             'mineru', 'mineru02', 'bdwp资源', 'clayden 有机化学', '中级无机化学', '人教版初中化学教材',
             '北斗40套', '各省预赛题目', '媒体仓库', '无机化学 习题集', '物理化学上下册',
             '结构化学习题与解析', '高中化学竞赛笔记', '高考化学', 'MATHEMATICS', '37决', '40届初赛',
             '重新ocr', 'scratch'}
SKIP_TOP = {'.git', '.workbuddy', '.claude', 'node_modules', 'kb-vault-mcp', 'pptx-workspace', 'skills', 'eiki'}
ARCHIVE_MARK = ('_归档', '_archive', '/归档', '归档/', '/归档-')


def is_archived(rel):
    return any(m in rel for m in ARCHIVE_MARK)


def strict_ok(fm):
    y = YAML(typ='safe', pure=True)
    y.version = (1, 2)
    y.allow_duplicate_keys = False
    try:
        y.load(fm)
        return None
    except Exception as e:
        return str(e).splitlines()[0] if str(e) else type(e).__name__


# FM 行：key: value
LINE = re.compile(r'^([A-Za-z_][A-Za-z0-9_\-]*):[ \t]*(.*)$')


def scan(scopes):
    res = collections.defaultdict(list)     # 问题类别 -> [rel]
    stat = collections.Counter()
    for dp, dn, fn in os.walk('.'):
        d = dp.replace('\\', '/')
        top = (d[2:] if d.startswith('./') else d).split('/')[0]
        if top in SKIP_TOP:
            dn[:] = []
            continue
        if top != '.' and scopes and top not in scopes:
            dn[:] = []
            continue
        dn[:] = [x for x in dn if x not in ('node_modules',)]
        for f in fn:
            if not f.endswith('.md'):
                continue
            p = os.path.join(dp, f).replace('\\', '/')
            rel = p[2:] if p.startswith('./') else p
            if is_archived(rel):
                continue
            try:
                t = io.open(p, encoding='utf-8-sig', errors='replace').read()
            except Exception:
                continue
            m = re.match(r'^---[ \t]*\r?\n(.*?)\r?\n---(\r?\n|$)', t, re.S)
            if not m:
                stat['no_fm'] += 1
                if top not in RAW_SCOPE:
                    res['无 frontmatter'].append(rel)
                continue
            stat['has_fm'] += 1
            fm = m.group(1)
            err = strict_ok(fm)
            if err:
                res['FM 解析失败(P1)'].append('%s  ← %s' % (rel, err))
                continue
            y = YAML(typ='safe', pure=True)
            y.version = (1, 2)
            d = y.load(fm) or {}
            ty = d.get('type')
            if top in SYS_SCOPE:
                if not ty:
                    res['系统层缺 type'].append(rel)
                elif ty not in SPEC_TYPE:
                    res['系统层 type 非规范'].append('%s  (type=%s)' % (rel, ty))
            # role 检查仅限 00-首页（只有它有「系统页角色索引」这一消费方；
            # 其余目录的系统页常用领域专属 role，属合法，不作判据）
            if top == '00-首页' and ty == '系统':
                r = d.get('role')
                if not r:
                    res['系统页缺 role'].append(rel)
                elif r not in SPEC_ROLE:
                    res['系统页 role 漂移'].append('%s  (role=%s)' % (rel, r))
            if not ty and top not in RAW_SCOPE and top not in SYS_SCOPE:
                # sidecar（绘图/图注产物）不视为缺口
                if ('/media/' not in '/' + rel) and ('/.chem_media/' not in rel) and not rel.startswith('.chem_media/'):
                    res['缺 type'].append(rel)
            # FM 值隐患：内嵌裸双引号（外层双引号包裹且内部还有 "）
            for ln in fm.split('\n'):
                mm = LINE.match(ln)
                if not mm:
                    continue
                v = mm.group(2).strip()
                if len(v) >= 2 and v[0] == '"' and v[-1] == '"' and '"' in v[1:-1]:
                    res['FM 值内嵌裸引号'].append('%s  (%s)' % (rel, ln[:70]))
    return res, stat


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--scope', nargs='*', default=None)
    ap.add_argument('--report', default=None)
    a = ap.parse_args()
    os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    res, stat = scan(set(a.scope) if a.scope else None)

    L = []
    L.append('---')
    L.append('title: 元数据体检报告')
    L.append('type: 审计报告')
    L.append('date: %s' % _dt.date.today().isoformat())
    L.append('generated_by: 11-模板/scripts/metadata_audit.py')
    L.append('---')
    L.append('')
    L.append('# 元数据体检报告')
    L.append('')
    L.append('扫过：有 FM %d ｜ 无 FM %d' % (stat['has_fm'], stat['no_fm']))
    L.append('')
    order = ['FM 解析失败(P1)', 'FM 值内嵌裸引号', '系统层缺 type', '系统层 type 非规范',
             '系统页缺 role', '系统页 role 漂移', '缺 type', '无 frontmatter']
    for k in order:
        items = res.get(k, [])
        L.append('## %s：%d' % (k, len(items)))
        for it in items[:60]:
            L.append('- ' + it)
        if len(items) > 60:
            L.append('- …（另有 %d 条）' % (len(items) - 60))
        L.append('')
    out = '\n'.join(L)
    print(out)
    if a.report:
        io.open(a.report, 'w', encoding='utf-8', newline='').write(out + '\n')
        print('→ 已写 %s' % a.report)
    return 1 if res.get('FM 解析失败(P1)') else 0


if __name__ == '__main__':
    sys.exit(main())
