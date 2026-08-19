$ErrorActionPreference = "Stop"

$path = "D:\pvimp_backend\app\services\gis\live_dashboard_kpi_service.py"

Write-Host ""
Write-Host "===== FIX LIVE DASHBOARD PERSIAN ENCODING =====" -ForegroundColor Cyan
Write-Host "File: $path" -ForegroundColor Gray

if (-not (Test-Path $path)) {
    throw "File not found: $path"
}

# Read original file as UTF-8
$content = [System.IO.File]::ReadAllText(
    $path,
    [System.Text.UTF8Encoding]::new($false)
)

$replacements = @{
    "ÙˆØ§Ú©Ø³ÛŒÙ†Ø§Ø³ÛŒÙˆÙ†" = "واکسیناسیون"
    "Ù…Ø±Ø§Ù‚Ø¨Øª ÙØ¹Ø§Ù„" = "مراقبت فعال"
    "Ú¯Ø²Ø§Ø±Ø´ Ø¨ÛŒÙ…Ø§Ø±ÛŒ" = "گزارش بیماری"
    "ÙˆÙ‚ÙˆØ¹ Ø¨ÛŒÙ…Ø§Ø±ÛŒ" = "وقوع بیماری"
    "Ø§Ø±Ø³Ø§Ù„ Ù†Ù…ÙˆÙ†Ù‡" = "ارسال نمونه"
    "Ù†ØªÛŒØ¬Ù‡ Ø¢Ø²Ù…Ø§ÛŒØ´Ú¯Ø§Ù‡" = "نتیجه آزمایشگاه"
    "Ú©Ø´ØªØ§Ø± / Ø§Ù…Ø­Ø§Ø¡" = "کشتار / امحاء"
    "Ø³Ù…Ù¾Ø§Ø´ÛŒ" = "سمپاشی"
    "ØªÙˆØ²ÛŒØ¹ ÙˆØ§Ú©Ø³Ù†" = "توزیع واکسن"
    "Ø¯ÙØ¹ ÙˆØ§Ú©Ø³Ù†" = "دفع واکسن"
    "Ø¨Ø¯ÙˆÙ† Ù†Ø§Ù…": "بدون نام"
    "Ù…Ø«Ø¨Øª" = "مثبت"
}

$before = $content

foreach ($key in $replacements.Keys) {
    $content = $content.Replace($key, $replacements[$key])
}

# Also repair the common mojibake form of "مثبت" if it exists in SQL.
$content = $content.Replace("Ù…Ø«Ø¨Øª", "مثبت")

# Backup
$backup = "$path.bak_before_farsi_fix"

[System.IO.File]::WriteAllText(
    $backup,
    $before,
    [System.Text.UTF8Encoding]::new($false)
)

# Write UTF-8 WITHOUT BOM
[System.IO.File]::WriteAllText(
    $path,
    $content,
    [System.Text.UTF8Encoding]::new($false)
)

Write-Host ""
Write-Host "===== RESULT =====" -ForegroundColor Green
Write-Host "Original backup:" -ForegroundColor Yellow
Write-Host $backup

Write-Host ""
Write-Host "Checking mojibake markers..." -ForegroundColor Cyan

$check = [System.IO.File]::ReadAllText(
    $path,
    [System.Text.UTF8Encoding]::new($false)
)

$badMarkers = @(
    "Ùˆ",
    "Ù…",
    "Ø",
    "Û",
    "Ú",
    "â€"
)

$found = @()

foreach ($marker in $badMarkers) {
    if ($check.Contains($marker)) {
        $found += $marker
    }
}

if ($found.Count -eq 0) {
    Write-Host "OK - no common Persian mojibake markers found." -ForegroundColor Green
}
else {
    Write-Host "WARNING - possible mojibake still exists:" -ForegroundColor Red
    $found | Sort-Object -Unique | ForEach-Object {
        Write-Host "  $_" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "File size:" -ForegroundColor Cyan
(Get-Item $path).Length

Write-Host ""
Write-Host "===== SAMPLE =====" -ForegroundColor Cyan

Get-Content $path -Encoding UTF8 |
    Select-String -Pattern "واکسیناسیون|مراقبت فعال|گزارش بیماری|نتیجه آزمایشگاه|ارسال نمونه|سمپاشی|توزیع واکسن|دفع واکسن" |
    Select-Object -First 20

Write-Host ""
Write-Host "===== DONE =====" -ForegroundColor Green