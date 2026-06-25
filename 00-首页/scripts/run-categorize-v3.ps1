# Launcher for categorize-v3-core.ps1

$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)

$scriptPath = Join-Path (Split-Path $MyInvocation.MyCommand.Path -Parent) 'categorize-v3-core.ps1'
$bytes = [System.IO.File]::ReadAllBytes($scriptPath)
$content = [System.Text.UTF8Encoding]::new($false).GetString($bytes)
$sb = [scriptblock]::Create($content)
& $sb
