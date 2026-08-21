Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Set-Location "D:\pvimp_backend\pvimp_frontend"

$tsx = ".\src\pages\Dashboard.tsx"

if (-not (Test-Path $tsx)) {
    throw "Dashboard.tsx پیدا نشد: $tsx"
}

$backup = ".\src\pages\Dashboard.tsx.step5.bak"

Copy-Item $tsx $backup -Force

Write-Host ""
Write-Host "===== STEP 5 : DASHBOARD TSX STRUCTURE =====" -ForegroundColor Cyan
Write-Host "Backup: $backup" -ForegroundColor DarkGray
Write-Host ""

$text = Get-Content $tsx -Raw -Encoding UTF8

# ---------------------------------------------------------
# STEP 5
# فقط className ها را اصلاح می‌کنیم.
# منطق React / API / state / JSX محتوا تغییر نمی‌کند.
# ---------------------------------------------------------

# Root dashboard
$text = [regex]::Replace(
    $text,
    'className="dashboard-page"',
    'className="dashboard-page dashboard-command-center"',
    1
)

# Header
$text = [regex]::Replace(
    $text,
    'className="dashboard-header"',
    'className="dashboard-header dashboard-command-header"',
    1
)

# KPI grid - فقط اولین dashboard-grid
$text = [regex]::Replace(
    $text,
    'className="dashboard-grid"',
    'className="dashboard-grid dashboard-kpi-grid"',
    1
)

# KPI cards:
# چهار dashboard-box اول بعد از KPI grid را مشخص می‌کنیم.
$kpiPattern = '(?s)(className="dashboard-grid dashboard-kpi-grid">.*?)(</div>\s*\r?\n\s*\r?\n\s*/\* ================================================= \*/\s*\r?\n\s*/\* Organization Structure)'
$kpiMatch = [regex]::Match($text, $kpiPattern)

if ($kpiMatch.Success) {
    $kpiBlock = $kpiMatch.Groups[1].Value

    $kpiBlock = [regex]::Replace(
        $kpiBlock,
        'className="dashboard-box"',
        'className="dashboard-box dashboard-stat-card"',
        4
    )

    $text = $text.Remove(
        $kpiMatch.Index,
        $kpiMatch.Length
    ).Insert(
        $kpiMatch.Index,
        $kpiBlock + $kpiMatch.Groups[2].Value
    )
}

# Organization / GIS sections:
# هر dashboard-box که h2 دارد، به عنوان section panel مشخص می‌شود.
$text = [regex]::Replace(
    $text,
    '(?s)<div\s+className="dashboard-box">\s*<h2>',
    '<div className="dashboard-box dashboard-section-panel">' + "`r`n" + '                <h2>'
)

# جدول‌های داشبورد
$text = [regex]::Replace(
    $text,
    '<table>',
    '<div className="dashboard-table-wrapper">' + "`r`n" +
    '                        <table>',
    [System.Text.RegularExpressions.RegexOptions]::None
)

$text = [regex]::Replace(
    $text,
    '</table>',
    '</table>' + "`r`n" +
    '                    </div>',
    [System.Text.RegularExpressions.RegexOptions]::None
)

# GIS status section
$text = [regex]::Replace(
    $text,
    'className="chart-placeholder"',
    'className="chart-placeholder dashboard-gis-status"',
    1
)

# Section headers
# h2 های اصلی را به wrapper مخصوص عنوان تبدیل نمی‌کنیم تا JSX ریسک نکند.
# فقط classهای موجود را نگه می‌داریم.

Set-Content $tsx $text -Encoding UTF8

Write-Host "Dashboard.tsx written." -ForegroundColor Green
Write-Host ""

# ---------------------------------------------------------
# STRUCTURAL VERIFICATION
# ---------------------------------------------------------

$verify = Get-Content $tsx -Raw -Encoding UTF8

$required = @(
    'dashboard-command-center',
    'dashboard-command-header',
    'dashboard-kpi-grid',
    'dashboard-stat-card',
    'dashboard-section-panel',
    'dashboard-table-wrapper',
    'dashboard-gis-status'
)

foreach ($className in $required) {
    if ($verify -notmatch [regex]::Escape($className)) {
        Write-Host "Missing expected class: $className" -ForegroundColor Red

        Copy-Item $backup $tsx -Force

        throw "Step 5 structural verification failed. Original Dashboard.tsx restored."
    }
}

# مطمئن شویم متن placeholder قبلی وارد فایل نشده است.
if ($verify -match 'PASTE THE COMPLETE DASHBOARD\.TSX CODE') {
    Copy-Item $backup $tsx -Force
    throw "Invalid placeholder text detected. Original Dashboard.tsx restored."
}

Write-Host "Structural verification: PASS" -ForegroundColor Green
Write-Host ""

# ---------------------------------------------------------
# TYPESCRIPT
# ---------------------------------------------------------

Write-Host "===== TYPESCRIPT CHECK =====" -ForegroundColor Yellow

npx tsc -b

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "TYPESCRIPT FAILED - restoring backup..." -ForegroundColor Red
    Copy-Item $backup $tsx -Force
    throw "Step 5 TypeScript check failed. Original Dashboard.tsx restored."
}

Write-Host "TypeScript: PASS" -ForegroundColor Green
Write-Host ""

# ---------------------------------------------------------
# BUILD
# ---------------------------------------------------------

Write-Host "===== BUILD =====" -ForegroundColor Cyan

npm run build

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "BUILD FAILED - restoring backup..." -ForegroundColor Red
    Copy-Item $backup $tsx -Force
    throw "Step 5 build failed. Original Dashboard.tsx restored."
}

Write-Host ""
Write-Host "===== STEP 5 DONE =====" -ForegroundColor Green
Write-Host "Dashboard.tsx updated successfully."
Write-Host "Backup: $backup"
Write-Host "TypeScript: SUCCESS"
Write-Host "Build: SUCCESS"
