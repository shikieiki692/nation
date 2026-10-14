# -*- coding: utf-8 -*-
r"""清理 SOP.md 中被误插的 `git show --stat` 输出（L60–L66），并把 L59 补回完整。"""
import io, shutil, datetime

P = '11-模板/规范/机构模拟题组卷管线SOP.md'
BAK = '.workbuddy/tmp/opt_pipe/_bak/sop_clean_%s' % datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
import os
os.makedirs(BAK, exist_ok=True)
shutil.copy2(P, os.path.join(BAK, os.path.basename(P)))

lines = io.open(P, encoding='utf-8', newline='').read().split('\n')
# 定位：以「提交脚本加固（同日）」开头的那一行起，到「1 file changed」行止
start = next(i for i, l in enumerate(lines) if '提交脚本加固（同日）' in l)
end = next(i for i, l in enumerate(lines) if l.strip().startswith('1 file changed'))
print('污染区间：L%d–L%d' % (start + 1, end + 1))
for i in range(start, end + 1):
    print('   %-3d %s' % (i + 1, lines[i][:80]))

GOOD = ('> **提交脚本加固（同日）**：隔离索引提交（read-tree → add → commit）**会把并行会话「已删未提交」的文件'
        '一并提交为 delete**（本次实伤：误删对方的 chemy 报告，已 fixup 补回）。'
        '⇒ **必用 `git commit --only -m … <paths>`**，或提交后**必扫 `git show --stat HEAD` '
        '有无 `delete mode` / 陌生路径**。')
new = lines[:start] + [GOOD] + lines[end + 1:]
d = '\n'.join(new)
# 断言：污染文本已消失
assert 'Author: shikieiki692' not in d
assert '1 file changed' not in d
io.open(P, 'w', encoding='utf-8', newline='').write(d)
print('已清理；体积 %d→%d ｜ 备份 %s' % (len('\n'.join(lines)), len(d), BAK))
