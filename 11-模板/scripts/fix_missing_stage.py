import os, re, json

vault = r'C:\Obsidion\妙妙屋'
with open(os.path.join(vault, '02-数据库', 'stage-migration-gap.json'), 'r', encoding='utf-8') as f:
    data = json.load(f)

STATUS_TO_STAGE = {
    '已填充': 'published', 'stub': 'draft', '骨架': 'draft',
    '已审校': 'published', '初稿': 'review',
    '草稿': 'draft', '样板试跑': 'review', '已生成（桥梁增强）': 'published',
    '精品': 'published', '框架': 'draft',
    'draft': 'draft', 'review': 'review', 'published': 'published',
    'deprecated': 'deprecated', 'archived': 'archived',
}

fixed = 0
skipped = 0
for item in data['files']:
    fp = os.path.join(vault, item['file'])
    if not os.path.isfile(fp):
        skipped += 1
        continue
    try:
        with open(fp, 'r', encoding='utf-8') as fh:
            content = fh.read()
    except:
        skipped += 1
        continue

    status = item.get('status', 'N/A')
    stage = STATUS_TO_STAGE.get(status)
    if not stage:
        skipped += 1
        continue

    status_escaped = re.escape(status)
    new_content = re.sub(
        r'^(status:\s*' + status_escaped + r'\s*)$',
        r'\1\nstage: ' + stage,
        content,
        count=1,
        flags=re.MULTILINE
    )
    if new_content == content:
        skipped += 1
        continue

    with open(fp, 'w', encoding='utf-8') as fh:
        fh.write(new_content)
    fixed += 1
    rel = item['file']
    print('  OK ' + rel + ' -> stage: ' + stage)

print('')
print('总计: 修复 ' + str(fixed) + ', 跳过 ' + str(skipped))
