# =============================================================================
# Phase 0 数据校验：重新生成 syllabus_gap_analysis_v3.json
# 显式 UTF-8 编码，避免 GBK/CP936 误读产生的 mojibake
# 规则与 [[知识库待补充清单]] 中的 DataviewJS 扫描保持一致
# =============================================================================

$ErrorActionPreference = 'Stop'

# 强制 UTF-8 IO（避免 PowerShell 5.1 默认 GBK 输出导致的二次乱码）
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)

# 路径常量
$VAULT_ROOT = (Get-Location).Path
$SYLLABUS_DIR = Join-Path $VAULT_ROOT '02-考纲条目'
$KP_DIR = Join-Path $VAULT_ROOT '03-知识点'
$OUTPUT_JSON = Join-Path $VAULT_ROOT '00-首页\syllabus_gap_analysis_v3.json'
$OUTPUT_REPORT = Join-Path $VAULT_ROOT '00-首页\syllabus_gap_analysis_v3_report.md'

# 排除规则（来自 DataviewJS 扫描，保持一致）
$excludeRegex = '^(中国化学奥林匹克(基本|决赛)要求-总览|(基础要求|决赛要求)-|(决赛)?\d{1,2}-|题型-|专题-|错题|外部资料-|提炼-|Arrow|ABOC|Atkins|物理化学（第)'
$topicSuffixRegex = '(专题|总论|总结|比较|入门|联系|应用|分析|初步|基础|模型|公式|策略|技巧)$'

# 1. 读取所有 KP 文件名（用于存在性和模糊匹配）
Write-Host "[1/4] 扫描 03-知识点/ 下所有 KP..." -ForegroundColor Cyan
$kpFiles = Get-ChildItem -Path $KP_DIR -Recurse -Filter '*.md' -File
$kpBasenames = $kpFiles | ForEach-Object { [System.IO.Path]::GetFileNameWithoutExtension($_.Name) }
$kpBasenameSet = [System.Collections.Generic.HashSet[string]]::new()
foreach ($n in $kpBasenames) { [void]$kpBasenameSet.Add($n) }
Write-Host "  → $($kpBasenames.Count) 个 KP" -ForegroundColor Green

# 2. 扫描所有考纲条目，提取 wikilinks
Write-Host "[2/4] 扫描 02-考纲条目/ 下所有 wikilink..." -ForegroundColor Cyan
$syllabusFiles = Get-ChildItem -Path $SYLLABUS_DIR -Recurse -Filter '*.md' -File

$allLinks = New-Object System.Collections.Generic.List[PSObject]
$wikilinkPattern = '\[\[([^\[\]\|#]+?)(?:\|[^\[\]]+)?(?:#[^\[\]]+)?\]\]'

foreach ($file in $syllabusFiles) {
    # 显式 UTF-8 读取
    $content = [System.IO.File]::ReadAllText($file.FullName, [System.Text.UTF8Encoding]::new($false))
    $relPath = $file.FullName.Substring($VAULT_ROOT.Length + 1) -replace '\\', '/'

    $matches = [regex]::Matches($content, $wikilinkPattern)
    foreach ($m in $matches) {
        $target = $m.Groups[1].Value.Trim()
        # 剥离尾部 .md 和路径前缀
        $target = $target -replace '\.md$', ''
        $target = ($target -split '/')[-1]
        $target = ($target -split '\\')[-1]
        if ([string]::IsNullOrWhiteSpace($target)) { continue }

        $allLinks.Add([PSCustomObject]@{
            Source = $relPath
            Target = $target
        })
    }
}
Write-Host "  → 提取 $($allLinks.Count) 个 wikilink 引用" -ForegroundColor Green

# 3. 分类
Write-Host "[3/4] 分类（存在 / 排除 / 专题 / 假性 / 真正缺失）..." -ForegroundColor Cyan

$stats = @{
    Existing = 0
    Excluded = 0
    TopicSuffix = 0
    FuzzyMatch = 0
    TrulyMissing = 0
}

$results = New-Object System.Collections.Generic.List[PSObject]

foreach ($link in $allLinks) {
    $t = $link.Target

    # 3.1 存在性检查
    if ($kpBasenameSet.Contains($t)) {
        $stats.Existing++
        continue
    }

    # 3.2 排除规则
    if ($t -match $excludeRegex) {
        $stats.Excluded++
        continue
    }

    # 3.3 专题后缀
    if ($t -match $topicSuffixRegex) {
        $stats.TopicSuffix++
        continue
    }

    # 3.4 模糊匹配（子串）
    $fuzzy = $null
    foreach ($kp in $kpBasenames) {
        if ($t.Length -ge 3 -and $kp.Contains($t)) { $fuzzy = $kp; break }
        if ($kp.Length -ge 3 -and $t.Contains($kp)) { $fuzzy = $kp; break }
    }
    if ($fuzzy) {
        $stats.FuzzyMatch++
        $results.Add([PSCustomObject]@{
            Source = $link.Source
            Link = $t
            FuzzyMatch = $fuzzy
            Confidence = '高'
            Type = '假性缺失'
        })
        continue
    }

    # 3.5 真正缺失
    $stats.TrulyMissing++
    $results.Add([PSCustomObject]@{
        Source = $link.Source
        Link = $t
        FuzzyMatch = $null
        Confidence = ''
        Type = '真正缺失'
    })
}

Write-Host "  分类完成：" -ForegroundColor Green
$stats.GetEnumerator() | Sort-Object Name | ForEach-Object {
    Write-Host ("    {0,-15} : {1}" -f $_.Key, $_.Value) -ForegroundColor White
}

# 4. 输出 JSON（显式 UTF-8 无 BOM）
Write-Host "[4/4] 输出 JSON 与报告..." -ForegroundColor Cyan
$json = $results | ConvertTo-Json -Depth 4
[System.IO.File]::WriteAllText($OUTPUT_JSON, $json, [System.Text.UTF8Encoding]::new($false))

# 4.b 输出 Markdown 概要报告
$trulyMissing = $results | Where-Object { $_.Type -eq '真正缺失' }
$fuzzyMissing = $results | Where-Object { $_.Type -eq '假性缺失' }

# 真正缺失按被引次数排序
$missingGroups = $trulyMissing | Group-Object Link | Sort-Object @{e='Count';desc=$true}, @{e='Name';desc=$false}

$report = New-Object System.Text.StringBuilder
[void]$report.AppendLine('---')
[void]$report.AppendLine('title: 考纲缺口分析报告 v3')
[void]$report.AppendLine('type: 系统')
[void]$report.AppendLine('generated_by: regen-gap-analysis-v3.ps1')
[void]$report.AppendLine("generated_at: $(Get-Date -Format 'yyyy-MM-dd HH:mm')")
[void]$report.AppendLine('encoding: UTF-8（显式）')
[void]$report.AppendLine('tags: [系统, 审计, 缺口]')
[void]$report.AppendLine('---')
[void]$report.AppendLine('')
[void]$report.AppendLine('# 考纲缺口分析报告 v3（Phase 0 数据校验）')
[void]$report.AppendLine('')
[void]$report.AppendLine('## 一、扫描统计')
[void]$report.AppendLine('')
[void]$report.AppendLine('| 类别 | 数量 |')
[void]$report.AppendLine('|:---|---:|')
[void]$report.AppendLine("| 考纲条目总数 | $($syllabusFiles.Count) |")
[void]$report.AppendLine("| KP 总数 | $($kpBasenames.Count) |")
[void]$report.AppendLine("| 提取 wikilink 引用 | $($allLinks.Count) |")
[void]$report.AppendLine("| ✅ 已存在跳过 | $($stats.Existing) |")
[void]$report.AppendLine("| 🚫 排除规则跳过 | $($stats.Excluded) |")
[void]$report.AppendLine("| 📌 专题后缀跳过 | $($stats.TopicSuffix) |")
[void]$report.AppendLine("| 🔁 模糊匹配（假性缺失） | $($stats.FuzzyMatch) |")
[void]$report.AppendLine("| 🔴 **真正缺失（去重前）** | **$($stats.TrulyMissing)** |")
[void]$report.AppendLine("| 🔴 **真正缺失（去重后）** | **$($missingGroups.Count)** |")
[void]$report.AppendLine('')
[void]$report.AppendLine('## 二、真正缺失 Top 30（按被引次数）')
[void]$report.AppendLine('')
[void]$report.AppendLine('| 排名 | 缺失 KP | 被引次数 | 来源举例 |')
[void]$report.AppendLine('|:---:|---|:---:|---|')

$rank = 0
foreach ($g in $missingGroups | Select-Object -First 30) {
    $rank++
    $samples = ($g.Group | Select-Object -First 3 -ExpandProperty Source) -join '; '
    if ($g.Count -gt 3) { $samples += " ...+$($g.Count - 3)" }
    [void]$report.AppendLine("| $rank | $($g.Name) | $($g.Count) | $samples |")
}

[void]$report.AppendLine('')
[void]$report.AppendLine('## 三、被引次数分布')
[void]$report.AppendLine('')
$distGroups = $missingGroups | Group-Object Count | Sort-Object @{e={[int]$_.Name};desc=$true}
[void]$report.AppendLine('| 被引次数 | 缺失 KP 数 |')
[void]$report.AppendLine('|:---:|:---:|')
foreach ($d in $distGroups) {
    [void]$report.AppendLine("| $($d.Name) | $($d.Count) |")
}

[void]$report.AppendLine('')
[void]$report.AppendLine('## 四、模块分布（按 Source 一级路径）')
[void]$report.AppendLine('')
$bySrc = $trulyMissing | ForEach-Object {
    $parts = $_.Source -split '/'
    if ($parts.Count -ge 3) { "$($parts[1])/$($parts[2])" }
    else { $parts[1] }
} | Group-Object | Sort-Object @{e='Count';desc=$true}
[void]$report.AppendLine('| 模块 | 真正缺失引用次数 |')
[void]$report.AppendLine('|:---|:---:|')
foreach ($s in $bySrc) {
    [void]$report.AppendLine("| $($s.Name) | $($s.Count) |")
}

[void]$report.AppendLine('')
[void]$report.AppendLine('## 五、与 v2 的对比')
[void]$report.AppendLine('')
[void]$report.AppendLine('| 指标 | v2 (JSON) | v3 (本次) | 差异 |')
[void]$report.AppendLine('|:---|---:|---:|:---|')
[void]$report.AppendLine("| 真正缺失（条目级） | 188 | $($stats.TrulyMissing) | 见下 |")
[void]$report.AppendLine("| 真正缺失（去重 KP 名） | ? | $($missingGroups.Count) | 新增统计维度 |")
[void]$report.AppendLine('')
[void]$report.AppendLine('> v2 JSON 因 mojibake 编码污染，部分"真正缺失"实为 GBK 误读，本次显式 UTF-8 应已修复。')

[System.IO.File]::WriteAllText($OUTPUT_REPORT, $report.ToString(), [System.Text.UTF8Encoding]::new($false))

Write-Host ""
Write-Host "完成！" -ForegroundColor Green
Write-Host "  JSON  -> $OUTPUT_JSON" -ForegroundColor White
Write-Host "  报告  -> $OUTPUT_REPORT" -ForegroundColor White
Write-Host ""
Write-Host "新口径数字：" -ForegroundColor Yellow
Write-Host "  真正缺失（条目级） : $($stats.TrulyMissing)" -ForegroundColor Yellow
Write-Host "  真正缺失（去重KP） : $($missingGroups.Count)" -ForegroundColor Yellow
