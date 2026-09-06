$content = Get-Content 'mineru02/第39届化学竞赛决赛第1场试题答案.md' -Raw -Encoding utf8

# Match both formats: "# 第 N 题 ... (M 分)" and "第 N 题 ... (M 分)" (standalone line)
$pattern = '(?:\r?\n|^)(#?\s*第\s*(\d+)\s*题\s+(.+?)\s*\((?:共)?(\d+)\s*分\)\s*)(?:\r?\n|$)'
$matches = [regex]::Matches($content, $pattern)

Write-Host "Found $($matches.Count) problems"

$problems = @()
for ($i = 0; $i -lt $matches.Count; $i++) {
    $m = $matches[$i]
    $num = [int]$m.Groups[2].Value
    $title = $m.Groups[3].Value.Trim()
    $score = [int]$m.Groups[4].Value
    $start = $m.Index
    $end = if ($i -lt $matches.Count - 1) { $matches[$i+1].Index } else { $content.Length }
    $probContent = $content.Substring($start, $end - $start).Trim()

    # Extract images referenced in this problem
    $imgPattern = '!\[\]\(第39届化学竞赛决赛第1场试题答案_images/([^)]+)\)'
    $imgMatches = [regex]::Matches($probContent, $imgPattern)
    $images = @()
    foreach ($img in $imgMatches) {
        $images += $img.Groups[1].Value
    }

    # Also match <img src="images/..."> format
    $imgPattern2 = '<img\s+src="images/([^"]+)"'
    $imgMatches2 = [regex]::Matches($probContent, $imgPattern2)
    foreach ($img in $imgMatches2) {
        $images += $img.Groups[1].Value
    }

    $problems += [PSCustomObject]@{
        Num = $num
        Title = $title
        Score = $score
        Content = $probContent
        Images = ($images | Select-Object -Unique)
    }

    Write-Host "题 ${num}: ${title} (${score}分) - $($images.Count) images"
}

# Export for later use
$problems | ForEach-Object {
    [PSCustomObject]@{
        Num = $_.Num
        Title = $_.Title
        Score = $_.Score
        ImageCount = $_.Images.Count
        Images = ($_.Images -join ', ')
    }
} | Export-Csv 'mineru02/problems.csv' -NoTypeInformation -Encoding utf8

Write-Host "`nSaved to problems.csv"
