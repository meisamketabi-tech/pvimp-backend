Set-Location "D:\pvimp_backend\pvimp_frontend"

$tsx = ".\src\pages\Dashboard.tsx"

if (-not (Test-Path $tsx)) {
    throw "Dashboard.tsx پیدا نشد: $tsx"
}

$backup = ".\src\pages\Dashboard.tsx.step5.bak"
Copy-Item $tsx $backup -Force

Write-Host "===== STEP 5 : DASHBOARD JSX STRUCTURE =====" -ForegroundColor Cyan

$text = Get-Content $tsx -Raw -Encoding UTF8

# Header structure
$text = $text.Replace(
    '<div className="dashboard-header">',
    '<div className="dashboard-header dashboard-command-header">'
)

$text = $text.Replace(
    '<h1>\n                    داشبورد مدیریتی سامانه دامپزشکی\n                </h1>',
    '<div className="dashboard-header-content">\n                <div>\n                    <div className="dashboard-eyebrow">PVIMP</div>\n                    <h1>\n                        داشبورد مدیریتی سامانه دامپزشکی\n                    </h1>\n                    <p>\n                        نمای کلی وضعیت ساختار سازمانی، عملکرد و اطلاعات مکانی سامانه\n                    </p>\n                </div>\n                <div className="dashboard-header-status">\n                    <span className="dashboard-status-dot" />\n                    <span>سامانه فعال</span>\n                </div>\n            </div>'
)

# KPI grid/card classes
$text = $text.Replace(
    '<div className="dashboard-grid">',
    '<div className="dashboard-grid dashboard-kpi-grid">',
    1
)

# Add stable class to each KPI card by matching the existing map structure.
$text = $text.Replace(
    'className="dashboard-box"\n                            key={index}',
    'className={`dashboard-box dashboard-stat-card dashboard-stat-${index + 1}`}\n                            key={index}'
)

# Organization / GIS panels
$text = $text.Replace(
    '<div className="dashboard-box">\n                <h2>\n                    وضعیت ساختار سازمانی',
    '<div className="dashboard-box dashboard-section-panel">\n                <div className="dashboard-section-header">\n                    <div>\n                        <span className="dashboard-section-kicker">ORGANIZATION</span>\n                        <h2>\n                            وضعیت ساختار سازمانی'
)

# Close the inserted organization header around the first table.
$text = $text.Replace(
    '                </h2>\n\n                <table>',
    '                        </h2>\n                    </div>\n                </div>\n\n                <div className="dashboard-table-wrapper">\n                <table>',
    1
)

# Close organization table wrapper.
$text = $text.Replace(
    '                </table>\n            </div>\n\n            {/* ================================================= */}\n            {/* GIS Centers */}',
    '                </table>\n                </div>\n            </div>\n\n            {/* ================================================= */}\n            {/* GIS Centers */}',
    1
)

# GIS center panel
$text = $text.Replace(
    '<div className="dashboard-box">\n                <h2>\n                    مراکز ثبت‌شده در GIS',
    '<div className="dashboard-box dashboard-section-panel">\n                <div className="dashboard-section-header">\n                    <div>\n                        <span className="dashboard-section-kicker">GIS</span>\n                        <h2>\n                            مراکز ثبت‌شده در GIS'
)

# Replace second table opening with wrapper. This targets GIS table only.
$gisMarker = 'مراکز ثبت‌شده در GIS'
$gisIndex = $text.IndexOf($gisMarker)
if ($gisIndex -ge 0) {
    $afterGis = $text.Substring($gisIndex)
    $afterGis = $afterGis.Replace(
        '                </h2>\n\n                <table>',
        '                        </h2>\n                    </div>\n                </div>\n\n                <div className="dashboard-table-wrapper">\n                <table>',
        1
    )
    $text = $text.Substring(0, $gisIndex) + $afterGis
}

# Close GIS table wrapper before GIS Status section.
$text = $text.Replace(
    '                </table>\n            </div>\n\n            {/* ================================================= */}\n            {/* GIS Status */}',
    '                </table>\n                </div>\n            </div>\n\n            {/* ================================================= */}\n            {/* GIS Status */}',
    1
)

# GIS status panel
$text = $text.Replace(
    '<div className="dashboard-box">\n                <h2>\n                    وضعیت GIS',
    '<div className="dashboard-box dashboard-section-panel">\n                <div className="dashboard-section-header">\n                    <div>\n                        <span className="dashboard-section-kicker">GIS STATUS</span>\n                        <h2>\n                            وضعیت GIS'
)

# Insert closing header before chart placeholder, only in GIS status section.
$gisStatusMarker = 'وضعیت GIS'
$gisStatusIndex = $text.LastIndexOf($gisStatusMarker)
if ($gisStatusIndex -ge 0) {
    $tail = $text.Substring($gisStatusIndex)
    $tail = $tail.Replace(
        '                </h2>\n\n                <div className="chart-placeholder">',
        '                        </h2>\n                    </div>\n                </div>\n\n                <div className="chart-placeholder dashboard-gis-status">',
        1
    )
    $text = $text.Substring(0, $gisStatusIndex) + $tail
}

# Error panel
$text = $text.Replace(
    '<div className="dashboard-box">\n                    <div\n                        style={{',
    '<div className="dashboard-box dashboard-alert-box">\n                    <div className="dashboard-alert"\n                        style={{'
)

Set-Content $tsx $text -Encoding UTF8

Write-Host "Dashboard.tsx updated." -ForegroundColor Green

# Basic structural verification
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

foreach ($item in $required) {
    if ($verify -notmatch [regex]::Escape($item)) {
        Write-Host "Missing expected class: $item" -ForegroundColor Red
        Copy-Item $backup $tsx -Force
        throw "Step 5 structural verification failed. Original Dashboard.tsx restored."
    }
}

Write-Host "Structure verification: SUCCESS" -ForegroundColor Green
Write-Host "===== TYPESCRIPT CHECK =====" -ForegroundColor Yellow

npx tsc -b
if ($LASTEXITCODE -ne 0) {
    Copy-Item $backup $tsx -Force
    throw "TypeScript failed. Original Dashboard.tsx restored."
}

Write-Host "TypeScript: SUCCESS" -ForegroundColor Green
Write-Host "===== BUILD =====" -ForegroundColor Cyan

npm run build
if ($LASTEXITCODE -ne 0) {
    Copy-Item $backup $tsx -Force
    throw "Build failed. Original Dashboard.tsx restored."
}

Write-Host "Build: SUCCESS" -ForegroundColor Green
Write-Host "===== STEP 5 DONE =====" -ForegroundColor Green
Write-Host "Backup: $backup"
