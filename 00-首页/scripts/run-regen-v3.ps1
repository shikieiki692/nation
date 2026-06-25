# Launcher: read the actual script as UTF-8 explicitly, then execute via dot-sourcing.
# PowerShell 5.1 on Windows reads .ps1 files using system code page (CP936) by default
# when no BOM is present, which breaks Chinese characters. This launcher bypasses that.

$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)

$scriptPath = Join-Path (Split-Path $MyInvocation.MyCommand.Path -Parent) 'regen-gap-analysis-v3-core.ps1'
$bytes = [System.IO.File]::ReadAllBytes($scriptPath)
$content = [System.Text.UTF8Encoding]::new($false).GetString($bytes)

# Wrap in a script block so $MyInvocation etc still works
$sb = [scriptblock]::Create($content)
& $sb
