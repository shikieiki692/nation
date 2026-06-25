# Phase 0 Step 2-3: 对比 v2 与 v3，并抽查 10 条真正缺失

$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)

$VAULT = (Get-Location).Path
$v2Path = Join-Path $VAULT '00-首页\syllabus_gap_analysis_v2.json'
$v3Path = Join-Path $VAULT '00-首页\syllabus_gap_analysis_v3.json'

# 读 v2 v3（让 .NET 自动检测 BOM，正确处理 UTF-8 with BOM 和 UTF-8 no BOM）
$v2Text = [System.IO.File]::ReadAllText($v2Path, [System.Text.UTF8Encoding]::new($true))
# 显式剥离开头 BOM 字符（有时 ReadAllText 不剥离）
$v2Text = $v2Text.TrimStart([char]0xFEFF)
$v2 = $v2Text | ConvertFrom-Json

$v3Text = [System.IO.File]::ReadAllText($v3Path, [System.Text.UTF8Encoding]::new($false))
$v3Text = $v3Text.TrimStart([char]0xFEFF)
$v3 = $v3Text | ConvertFrom-Json

Write-Host "=== Step 2: v2 vs v3 对比 ===" -ForegroundColor Cyan

$v2Missing = $v2 | Where-Object { $_.Type -eq '真正缺失' }
$v3Missing = $v3 | Where-Object { $_.Type -eq '真正缺失' }

Write-Host "v2 真正缺失条目数: $($v2Missing.Count)"
Write-Host "v3 真正缺失条目数: $($v3Missing.Count)"

# 找出 v2 独有（含 mojibake）和 v3 独有（v2 漏报）
$v2Set = $v2Missing | ForEach-Object { "$($_.Source)|||$($_.Link)" }
$v3Set = $v3Missing | ForEach-Object { "$($_.Source)|||$($_.Link)" }

$v2Only = $v2Set | Where-Object { $_ -notin $v3Set }
$v3Only = $v3Set | Where-Object { $_ -notin $v2Set }
$both = $v2Set | Where-Object { $_ -in $v3Set }

Write-Host ""
Write-Host "v2 独有（疑似 mojibake / 编码污染）: $($v2Only.Count)"
Write-Host "v3 独有（v2 漏报，UTF-8 修复后才发现）: $($v3Only.Count)"
Write-Host "两版共有: $($both.Count)"

# 抽样 v2 独有的 5 条
Write-Host ""
Write-Host "--- v2 独有（前 5 条，疑似 mojibake）---"
$v2Only | Select-Object -First 5 | ForEach-Object {
    $parts = $_ -split '\|\|\|'
    Write-Host "  Source: $($parts[0])"
    Write-Host "  Link:   $($parts[1])"
    Write-Host ""
}

# 抽样 v3 独有的 5 条
Write-Host "--- v3 独有（前 5 条，UTF-8 修复后新发现的真实缺失）---"
$v3Only | Select-Object -First 5 | ForEach-Object {
    $parts = $_ -split '\|\|\|'
    Write-Host "  Source: $($parts[0])"
    Write-Host "  Link:   $($parts[1])"
    Write-Host ""
}

Write-Host "=== Step 3: 抽查 v3 真正缺失 10 条（验证文件确实不存在）===" -ForegroundColor Cyan

# 从 v3 真正缺失里抽 10 条，验证 03-知识点/ 下确实没有同名文件
$kpFiles = Get-ChildItem '03-知识点' -Recurse -Filter '*.md' -File
$kpBasenames = [System.Collections.Generic.HashSet[string]]::new()
foreach ($f in $kpFiles) { [void]$kpBasenames.Add([System.IO.Path]::GetFileNameWithoutExtension($f.Name)) }

# 抽样：取 v3 真正缺失中按字母顺序均匀分布的 10 条
$samples = $v3Missing | Sort-Object Link | ForEach-Object { $_ } | Group-Object Link | Sort-Object Name
$sampleStep = [Math]::Max(1, [int]($samples.Count / 10))
$picked = @()
for ($i = 0; $i -lt $samples.Count -and $picked.Count -lt 10; $i += $sampleStep) {
    $picked += $samples[$i]
}

$confirmed = 0
$contradicted = 0
foreach ($s in $picked) {
    $name = $s.Name
    $exists = $kpBasenames.Contains($name)
    if ($exists) {
        Write-Host ("  ❌ {0,-30} v3 标为缺失，但实际存在 (BUG)" -f $name) -ForegroundColor Red
        $contradicted++
    } else {
        # 同时做模糊匹配检查
        $fuzzy = $kpFiles.BaseName | Where-Object { $_ -like "*$name*" -or $name -like "*$_*" } | Select-Object -First 1
        if ($fuzzy) {
            Write-Host ("  ⚠️  {0,-30} v3 标为缺失，模糊匹配到: $fuzzy" -f $name) -ForegroundColor Yellow
        } else {
            Write-Host ("  ✅ {0,-30} 确认不存在（真正缺失）" -f $name) -ForegroundColor Green
            $confirmed++
        }
    }
}

Write-Host ""
Write-Host "抽查结论: $confirmed 条确认不存在, $contradicted 条矛盾" -ForegroundColor White

Write-Host ""
Write-Host "=== Step 3b: 验证 v2 独有的 mojibake 条目实际目标 ===" -ForegroundColor Cyan
Write-Host "（如果 v2 独有的 mojibake 条目对应的 真实 KP 名实际存在，则证明 v2 误报）"

# 取 v2 独有的前 10 条 mojibake 条目，看它们的 Source 文件里的真实 wikilink
$v2OnlySamples = $v2Only | Select-Object -First 10
foreach ($entry in $v2OnlySamples) {
    $parts = $entry -split '\|\|\|'
    $sourceFile = Join-Path $VAULT ($parts[0] -replace '/', '\')
    $mojibakeLink = $parts[1]
    if (Test-Path $sourceFile) {
        $sourceBytes = [System.IO.File]::ReadAllBytes($sourceFile)
        $sourceText = [System.Text.UTF8Encoding]::new($false).GetString($sourceBytes)
        # 提取所有 wikilink
        $links = [regex]::Matches($sourceText, '\[\[([^\[\]\|#]+?)(?:\|[^\[\]]+)?(?:#[^\[\]]+)?\]\]') | ForEach-Object {
            ($_.Groups[1].Value -split '/')[-1] -replace '\.md$', ''
        }
        $existingLinks = $links | Where-Object { $kpBasenames.Contains($_) }
        $missingLinks = $links | Where-Object { -not $kpBasenames.Contains($_) }
        Write-Host "  v2 报: $mojibakeLink (源: $($parts[0]))"
        Write-Host "    源文件含 wikilink 总数: $($links.Count), 存在: $($existingLinks.Count), 缺失: $($missingLinks.Count)"
        if ($missingLinks.Count -gt 0) {
            Write-Host "    源文件实际缺失链接示例: $($missingLinks -join ', ')" -ForegroundColor Yellow
        }
        Write-Host ""
    }
}
