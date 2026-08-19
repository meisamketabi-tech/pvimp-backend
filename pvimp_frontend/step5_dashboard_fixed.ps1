Set-Location "D:\pvimp_backend\pvimp_frontend"

$tsx = ".\src\pages\Dashboard.tsx"

if (-not (Test-Path $tsx)) {
    throw "Dashboard.tsx پیدا نشد: $tsx"
}

$backup = ".\src\pages\Dashboard.tsx.step5.bak"
Copy-Item $tsx $backup -Force

Write-Host "===== STEP 5 : DASHBOARD TSX STRUCTURE =====" -ForegroundColor Cyan
Write-Host "Backup: $backup" -ForegroundColor DarkGray

$text = Get-Content $tsx -Raw -Encoding UTF8

function Replace-FirstLiteral {
    param(
        [string]$Source,
        [string]$Old,
        [string]$New
    )

    $index = $Source.IndexOf($Old, [System.StringComparison]::Ordinal)
    if ($index -lt 0) {
        return $Source
    }

    return $Source.Substring(0, $index) +
           $New +
           $Source.Substring($index + $Old.Length)
}

# ---------------------------------------------------------
# 1) Header
# ---------------------------------------------------------
$text = Replace-FirstLiteral `
    $text `
    '<div className="dashboard-header">' `
    '<div className="dashboard-header dashboard-command-header">'

# ---------------------------------------------------------
# 2) KPI grid: only the first dashboard-grid
# ---------------------------------------------------------
$text = Replace-FirstLiteral `
    $text `
    '<div className="dashboard-grid">' `
    '<div className="dashboard-grid dashboard-kpi-grid">'

# ---------------------------------------------------------
# 3) KPI cards
# ---------------------------------------------------------
$text = Replace-FirstLiteral `
    $text `
    'className="dashboard-box"
                            key={index}' `
    'className={`dashboard-box dashboard-stat-card dashboard-stat-${index + 1}`}
                            key={index}'

# ---------------------------------------------------------
# 4) Remaining dashboard boxes -> section panels
#    This happens after the KPI card has been converted.
# ---------------------------------------------------------
$text = $text.Replace(
    '<div className="dashboard-box">',
    '<div className="dashboard-box dashboard-section-panel">'
)

# ---------------------------------------------------------
# 5) Error alert
# ---------------------------------------------------------
$text = $text.Replace(
    '<div className="dashboard-box dashboard-section-panel">
                    <div',
    '<div className="dashboard-box dashboard-alert-box">
                    <div'
)

# ---------------------------------------------------------
# 6) Tables: wrap every table in one responsive container.
#    Dashboard.tsx currently contains two tables.
# ---------------------------------------------------------
$text = $text.Replace(
    '<table>',
    '<div className="dashboard-table-wrapper">
                <table>'
)

$text = $text.Replace(
    '</table>',
    '</table>
                </div>'
)

# ---------------------------------------------------------
# 7) Section headers
# ---------------------------------------------------------
$text = $text.Replace(
    '<h2>
                    وضعیت ساختار سازمانی
                </h2>',
    '<div className="dashboard-section-header">
                    <div>
                        <span className="dashboard-section-kicker">ORGANIZATION</span>
                        <h2>وضعیت ساختار سازمانی</h2>
                    </div>
                </div>'
)

$text = $text.Replace(
    '<h2>
                    مراکز ثبت‌شده در GIS
                </h2>',
    '<div className="dashboard-section-header">
                    <div>
                        <span className="dashboard-section-kicker">GIS</span>
                        <h2>مراکز ثبت‌شده در GIS</h2>
                    </div>
                </div>'
)

$text = $text.Replace(
    '<h2>
                    وضعیت GIS
                </h2>',
    '<div className="dashboard-section-header">
                    <div>
                        <span className="dashboard-section-kicker">GIS STATUS</span>
                        <h2>وضعیت GIS</h2>
                    </div>
                </div>'
)

# ---------------------------------------------------------
# 8) GIS status placeholder
# ---------------------------------------------------------
$text = $text.Replace(
    '<div className="chart-placeholder">',
    '<div className="chart-placeholder dashboard-gis-status">'
)

# ---------------------------------------------------------
# 9) Verify
# ---------------------------------------------------------
Set-Content $tsx $text -Encoding UTF8

$verify = Get-Content $tsx -Raw -Encoding UTF8

$required = @(
    'dashboard-command-header',
    'dashboard-kpi-grid',
    'dashboard-stat-card',
    'dashboard-section-panel',
    'dashboard-section-header',
    'dashboard-table-wrapper',
    'dashboard-gis-status'
)

$failed = $false

foreach ($item in $required) {
    if ($verify -notmatch [regex]::Escape($item)) {
        Write-Host "Missing expected class: $item" -ForegroundColor Red
        $failed = $true
    }
}

if ($failed) {
    Copy-Item $backup $tsx -Force
    throw "Step 5 structural verification failed. Original Dashboard.tsx restored."
}

Write-Host "Structure verification: SUCCESS" -ForegroundColor Green

# ---------------------------------------------------------
# 10) TypeScript
# ---------------------------------------------------------
Write-Host ""
Write-Host "===== TYPESCRIPT CHECK =====" -ForegroundColor Yellow

npx tsc -b

if ($LASTEXITCODE -ne 0) {
    Write-Host "TypeScript FAILED - restoring backup..." -ForegroundColor Red
    Copy-Item $backup $tsx -Force
    throw "Step 5 TypeScript check failed. Original Dashboard.tsx restored."
}

Write-Host "TypeScript: SUCCESS" -ForegroundColor Green

# ---------------------------------------------------------
# 11) Build
# ---------------------------------------------------------
Write-Host ""
Write-Host "===== BUILD =====" -ForegroundColor Cyan

npm run build

if ($LASTEXITCODE -ne 0) {
    Write-Host "BUILD FAILED - restoring backup..." -ForegroundColor Red
    Copy-Item $backup $tsx -Force
    throw "Step 5 build failed. Original Dashboard.tsx restored."
}

Write-Host "Build: SUCCESS" -ForegroundColor Green

Write-Host ""
Write-Host "===== STEP 5 DONE =====" -ForegroundColor Green
Write-Host "Dashboard.tsx updated successfully."
Write-Host "Backup: $backup"
Write-Host "TypeScript: SUCCESS"
Write-Host "Build: SUCCESS"
