param(
    [string]$VaultRoot = "C:\Obsidion\妙妙屋",
    [string]$OutputDir = "00-首页\学生讲义Word",
    [string]$OutputName = "结构化学专题课-学生用合集（完整版）.docx"
)

[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$OutputEncoding = [Console]::OutputEncoding

$permMd = Join-Path $VaultRoot "04-课件\专题课\第一轮结构化学专题课-学生用合集（完整版）.md"

# --- Step 1: Source files ---
$sources = @(
    "04-课件\专题课\第一轮结构化学专题课-01-Lewis与VSEPR实战.md",
    "04-课件\专题课\第一轮结构化学专题课-02-MO理论与立体电子效应.md",
    "04-课件\专题课\第一轮结构化学专题课-03-晶体结构基础.md",
    "04-课件\专题课\第一轮结构化学专题课-04-晶体结构进阶.md",
    "04-课件\专题课\第一轮结构化学专题课-05-配位化合物.md",
    "04-课件\专题课\第一轮结构化学专题课-06-跨模块综合实战.md"
)

# --- Step 2: Image path mapping ---
# wiki-link ![[subfolder/file.jpg]] -> ![img](mineru/01-真题/subfolder/file.jpg)
$imgMap = @{
    "第35届中国化学奥林匹克初赛试题_images/" = "mineru/01-真题/第35届中国化学奥林匹克初赛试题_images/"
    "第36届中国化学奥林匹克初赛试题第二场_images/" = "mineru/01-真题/第36届中国化学奥林匹克初赛试题第二场_images/"
    "第37届中国化学奥林匹克初赛试题_images/" = "mineru/01-真题/第37届中国化学奥林匹克初赛试题_images/"
    "第38届中国化学奥林匹克初赛试题_images/" = "mineru/01-真题/第38届中国化学奥林匹克初赛试题_images/"
    "第39届中国化学奥林匹克初赛试题_images/" = "mineru/01-真题/第39届中国化学奥林匹克初赛试题_images/"
    "2024年第38届化学竞赛决赛试题及解析_images/" = "mineru02/2024年第38届化学竞赛决赛试题及解析_images/"
}

function Convert-WikiImages {
    param([string]$text)
    # Use -replace for each known image prefix
    $result = $text
    # Collect all wiki-link image paths first, then replace each individually
    $allMatches = [System.Collections.ArrayList]::new()
    foreach ($m in [regex]::Matches($result, '!\[\[([^\]]+\.(?:jpg|jpeg|png|gif|webp))\]\]')) {
        [void]$allMatches.Add(@{ Index = $m.Index; Length = $m.Length; Value = $m.Groups[1].Value })
    }
    # Process in reverse to preserve indices
    for ($i = $allMatches.Count - 1; $i -ge 0; $i--) {
        $entry = $allMatches[$i]
        $inner = $entry.Value -replace '\\', '/'
        $newPath = $null
        foreach ($prefix in $imgMap.Keys) {
            if ($inner.Contains($prefix)) {
                $newPath = $inner.Replace($prefix, $imgMap[$prefix])
                break
            }
        }
        if (-not $newPath) {
            $filename = [System.IO.Path]::GetFileName($entry.Value)
            foreach ($prefix in $imgMap.Keys) {
                $testPath = Join-Path $VaultRoot ($imgMap[$prefix] + $filename)
                if (Test-Path $testPath) {
                    $newPath = $imgMap[$prefix] + $filename
                    break
                }
            }
        }
        if (-not $newPath) { $newPath = $inner }
        $before = $result.Substring(0, $entry.Index)
        $after = $result.Substring($entry.Index + $entry.Length)
        $result = "${before}![img](${newPath})${after}"
    }
    return $result
}

function Clean-ForStudent {
    param([string]$text)
    $c = $text
    # Strip YAML frontmatter
    $c = $c -replace '(?s)^---\s*\n.*?\n---\s*\n', ''
    # Strip title heading (first # line)
    $c = $c -replace '(?m)^#\s+结构化学专题课[：:].*\n', ''
    # Strip course positioning blockquote
    $c = $c -replace '(?s)>\s*\*\*课程定位\*\*[^\n]*\n(>\s*[^\n]*\n)*', ''
    # Strip "**课堂操作**" lines
    $c = $c -replace '(?m)^\s*\*\*课堂操作\*\*[^\n]*\n?', ''
    # Strip all time references
    $c = $c -replace '\s*（\d+\s*min[^）]*）', ''
    $c = $c -replace '\s*\(\d+\s*min[^)]*\)', ''
    $c = $c -replace '\s*建议用时[^\n|]*\|?', ''
    $c = $c -replace '\s*\|\s*建议用时[^\n]*', ''
    # Strip "**分值**" lines
    $c = $c -replace '(?m)^\s*\*\*分值\*\*[^\n]*\n?', ''
    # Strip source references
    $c = $c -replace '(?m)^>\s*来源：\[\[[^\]]*\]\]\s*\n?', ''
    # Strip "四、总结" section and everything after
    $c = $c -replace '(?s)\n##\s*四、总结.*$', ''
    # Strip footer
    $c = $c -replace '(?s)\n\*本专题依据.*$', ''
    # Remove excessive blank lines
    $c = $c -replace '(\r?\n){3,}', "`n`n"
    # Fix double/triple --- separators
    $c = $c -replace '(?m)^---\s*\n---\s*\n?', "---`n"
    return $c.Trim()
}

Write-Host "Building combined student handout..."

$parts = @()
$parts += "# 结构化学专题课 学生用讲义（合集）`n"
$parts += "> 本讲义整合6节题目驱动专题课，涵盖Lewis与VSEPR、MO理论、晶体结构基础与进阶、配位化合物、跨模块综合实战，覆盖考纲§9-17全部考点。`n"

foreach ($src in $sources) {
    $fullPath = Join-Path $VaultRoot $src
    $content = Get-Content $fullPath -Raw -Encoding UTF8
    $content = Clean-ForStudent $content
    $content = Convert-WikiImages $content
    $parts += $content
    Write-Host "  + $([System.IO.Path]::GetFileName($src))"
}

$combined = $parts -join "`n`n---`n`n"

# Write temp markdown
$tempMd = Join-Path $VaultRoot "00-首页\学生讲义Word\_temp_combined.md"
$combined | Out-File $tempMd -Encoding UTF8
Write-Host "Temp MD: $tempMd ($([math]::Round((Get-Item $tempMd).Length/1024))KB)"

# Post-process: convert Unicode subscripts to LaTeX math
Write-Host "Converting Unicode subscripts to LaTeX math..."
$fixSubScript = Join-Path $VaultRoot "00-首页\学生讲义Word\_fix_subscripts.py"
python $fixSubScript $tempMd

# Copy to permanent location
Copy-Item $tempMd $permMd -Force
Write-Host "Saved to: $permMd"

# Reload the converted content for pandoc
$combined = Get-Content $tempMd -Raw -Encoding UTF8
$size = [math]::Round((Get-Item $tempMd).Length / 1024)
Write-Host "Converted MD: $size KB"

# --- Step 3: Generate docx with reference template ---
$refDocx = Join-Path $VaultRoot "11-模板\scripts\templates\custom-reference.docx"
$outputPath = Join-Path $VaultRoot "$OutputDir\$OutputName"

if (-not (Test-Path $refDocx)) {
    Write-Host "ERROR: Reference docx not found: $refDocx"
    exit 1
}

Write-Host "Reference template: $refDocx"
Write-Host "Generating: $outputPath"

# Kill any open Word instances
$wordProcs = Get-Process WINWORD -ErrorAction SilentlyContinue
if ($wordProcs) {
    Write-Host "Closing Word..."
    $wordProcs | Stop-Process -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
}

# Convert with reference docx
$mdBase = [System.IO.Path]::GetDirectoryName($tempMd)
$pandocArgs = @(
    $tempMd,
    "--from", "markdown",
    "--to", "docx",
    "--reference-doc", $refDocx,
    "--resource-path", $mdBase,
    "--resource-path", $VaultRoot,
    "-o", $outputPath
)
Write-Host "pandoc $($pandocArgs -join ' ')"
& pandoc @pandocArgs

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: pandoc failed with exit code $LASTEXITCODE"
    exit $LASTEXITCODE
}

$size = [math]::Round((Get-Item $outputPath).Length / 1024)
Write-Host "`nPandoc done: $outputPath ($size KB)"

# --- Step 4: Post-process docx — set math font to Times New Roman ---
Write-Host "Post-processing: setting math font to Times New Roman..."
$fixFontScript = Join-Path $VaultRoot "00-首页\学生讲义Word\_fix_math_font.py"
python $fixFontScript $outputPath

$size2 = [math]::Round((Get-Item $outputPath).Length / 1024)
Write-Host "Final: $outputPath ($size2 KB)"

# Verify image count
$wikiImgCount = ([regex]::Matches($combined, '!\[\[')).Count
$mdImgCount = ([regex]::Matches($combined, '!\[img\]')).Count
Write-Host "Wiki-link images remaining: $wikiImgCount"
Write-Host "Converted images: $mdImgCount"
