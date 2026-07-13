$vaultRoot = "C:\Obsidion\妙妙屋"
$excludePatterns = @('\.trash\\', '\\skills\\', '\\copilot\\', '\\eiki\\', '\\mineru\\', '高中化学竞赛笔记')

# Build file index
$allMdFiles = Get-ChildItem -Path $vaultRoot -Recurse -Filter "*.md" | Where-Object {
    $path = $_.FullName
    $excluded = $false
    foreach ($pattern in $excludePatterns) {
        if ($path -match $pattern) { $excluded = $true; break }
    }
    -not $excluded
}

$fileIndex = @{}
$allFilesFlat = @{}
foreach ($f in $allMdFiles) {
    $relPath = $f.FullName.Substring($vaultRoot.Length + 1) -replace '\\','/'
    $nameNoExt = [System.IO.Path]::GetFileNameWithoutExtension($f.Name)
    $allFilesFlat[$relPath] = $f.FullName
    if (-not $fileIndex.ContainsKey($nameNoExt)) {
        $fileIndex[$nameNoExt] = @()
    }
    $fileIndex[$nameNoExt] += $relPath
}
Write-Host "MD file index: $($allMdFiles.Count) files"

# Index all non-md files too
$allNonMd = Get-ChildItem -Path $vaultRoot -Recurse -File | Where-Object {
    $path = $_.FullName
    $excluded = $false
    foreach ($pattern in $excludePatterns) {
        if ($path -match $pattern) { $excluded = $true; break }
    }
    -not $excluded -and $_.Extension -ne '.md'
}
foreach ($f in $allNonMd) {
    $relPath = $f.FullName.Substring($vaultRoot.Length + 1) -replace '\\','/'
    $allFilesFlat[$relPath] = $f.FullName
}
Write-Host "Total files indexed: $($allFilesFlat.Count)"

# Extract all wikilinks
$allLinks = [System.Collections.ArrayList]::new()
foreach ($file in $allMdFiles) {
    $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8 -ErrorAction SilentlyContinue
    if (-not $content) { continue }
    $matches = [regex]::Matches($content, '(?<!!)\[\[([^\]]+)\]\]|!\[\[([^\]]+)\]\]')
    foreach ($m in $matches) {
        $linkRaw = if ($m.Groups[1].Success) { $m.Groups[1].Value } else { $m.Groups[2].Value }
        $relSrc = $file.FullName.Substring($vaultRoot.Length + 1) -replace '\\','/'
        [void]$allLinks.Add(@{ SourceFile = $file.FullName; RelSource = $relSrc; LinkRaw = $linkRaw })
    }
}
Write-Host "Total wikilinks found: $($allLinks.Count)"

# Parse unique targets
$targetToSources = @{}
foreach ($link in $allLinks) {
    $target = $link.LinkRaw
    if ($target -match '^([^|]+)\|') { $target = $Matches[1] }
    if ($target -match '^#') { continue }
    if ($target -match '^(.+)#') { $target = $Matches[1] }
    $target = $target.Trim()
    if ($target -eq '') { continue }
    if (-not $targetToSources.ContainsKey($target)) {
        $targetToSources[$target] = [System.Collections.ArrayList]::new()
    }
    [void]$targetToSources[$target].Add($link.RelSource)
}
Write-Host "Unique non-heading targets: $($targetToSources.Count)"

# Check each target
$brokenLinks = @{}
$skippedCount = 0
foreach ($target in $targetToSources.Keys) {
    # Skip template placeholders, code vars, etc.
    if ($target -match '^\{' -or $target -match '^\$' -or $target -match '^<' -or $target -match '^`') {
        $skippedCount++; continue
    }
    if ($target -match '^\.\.\.' -or $target -match '^\^' -or $target -match '^\\') {
        $skippedCount++; continue
    }
    # Skip hash-named images
    if ($target -match '^[0-9a-f]{20,}\.' ) {
        $skippedCount++; continue
    }

    $found = $false
    if ($target -match '[/\\]') {
        $targetNorm = $target -replace '\\','/'
        if ($allFilesFlat.ContainsKey($targetNorm)) { $found = $true }
        elseif ($allFilesFlat.ContainsKey("$targetNorm.md")) { $found = $true }
        else {
            $parts = $targetNorm -split '/'
            $fileName = $parts[-1]
            if ($fileIndex.ContainsKey($fileName)) { $found = $true }
        }
    } else {
        if ($fileIndex.ContainsKey($target)) { $found = $true }
    }

    if (-not $found) {
        $brokenLinks[$target] = $targetToSources[$target]
    }
}

Write-Host ""
Write-Host "=== SCAN COMPLETE ==="
Write-Host "Skipped (template/code/placeholder): $skippedCount"
Write-Host "Broken targets (real): $($brokenLinks.Count)"

# Categorize
$imgExts = '\.jpg$|\.png$|\.svg$|\.gif$|\.jpeg$|\.webp$|\.bmp$'
$pathBroken = @{}
$nameBroken = @{}
$imgBroken = @{}
foreach ($target in $brokenLinks.Keys) {
    $sources = $brokenLinks[$target]
    if ($target -match $imgExts) {
        $imgBroken[$target] = $sources
    } elseif ($target -match '[/\\]') {
        $pathBroken[$target] = $sources
    } else {
        $nameBroken[$target] = $sources
    }
}

Write-Host ""
Write-Host "### PATH-BASED BROKEN LINKS ($($pathBroken.Count))"
foreach ($t in ($pathBroken.Keys | Sort-Object)) {
    $cnt = $pathBroken[$t].Count
    $first2 = $pathBroken[$t] | Select-Object -First 2
    $srcStr = ($first2 -join '; ')
    if ($cnt -gt 2) { $srcStr += " ... (+$($cnt - 2))" }
    Write-Host "  [[$t]] ($cnt) <- $srcStr"
}

Write-Host ""
Write-Host "### IMAGE BROKEN LINKS ($($imgBroken.Count))"
foreach ($t in ($imgBroken.Keys | Sort-Object)) {
    $cnt = $imgBroken[$t].Count
    Write-Host "  [[$t]] ($cnt)"
}

Write-Host ""
Write-Host "### NAME-BASED BROKEN LINKS ($($nameBroken.Count))"
foreach ($t in ($nameBroken.Keys | Sort-Object)) {
    $cnt = $nameBroken[$t].Count
    $first2 = $nameBroken[$t] | Select-Object -First 2
    $srcStr = ($first2 -join '; ')
    if ($cnt -gt 2) { $srcStr += " ... (+$($cnt - 2))" }
    Write-Host "  [[$t]] ($cnt) <- $srcStr"
}

# Affected files
$affectedFiles = @{}
foreach ($target in $brokenLinks.Keys) {
    foreach ($src in $brokenLinks[$target]) {
        $affectedFiles[$src] = $true
    }
}
$totalInstances = 0
foreach ($target in $brokenLinks.Keys) {
    $totalInstances += $brokenLinks[$target].Count
}
Write-Host ""
Write-Host "=== SUMMARY ==="
Write-Host "Scanned files: $($allMdFiles.Count)"
Write-Host "Total wikilinks: $($allLinks.Count)"
Write-Host "Unique targets checked: $($targetToSources.Count)"
Write-Host "Skipped (template/code): $skippedCount"
Write-Host "Broken link targets: $($brokenLinks.Count)"
Write-Host "  Path-based: $($pathBroken.Count)"
Write-Host "  Image/embed: $($imgBroken.Count)"
Write-Host "  Name-based: $($nameBroken.Count)"
Write-Host "Affected source files: $($affectedFiles.Count)"
Write-Host "Total broken link instances: $totalInstances"
