$ErrorActionPreference = "Stop"

$Root = "D:\pvimp_backend"
$Service = Join-Path $Root "app\services\gis\live_dashboard_kpi_service_v2.py"
$Router  = Join-Path $Root "app\api\v1\endpoints\gis_dashboard_kpi_v2.py"
$Frontend = Join-Path $Root "pvimp_frontend\src\pages\LiveKpiDashboardV2.tsx"

$ProvinceId = 5
$Stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$Backup = Join-Path $Root "_zanjan_kpi_v2_backup_$Stamp"

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "PVIMP - ZANJAN KPI V2 SCOPE" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Target province : Zanjan" -ForegroundColor Green
Write-Host "Province ID     : $ProvinceId" -ForegroundColor Green
Write-Host ""

# ------------------------------------------------------------
# Validate
# ------------------------------------------------------------

foreach ($f in @($Service,$Router,$Frontend)) {
    if (!(Test-Path $f)) {
        throw "Required file not found: $f"
    }
}

# ------------------------------------------------------------
# Backup
# ------------------------------------------------------------

New-Item -ItemType Directory -Path $Backup -Force | Out-Null

Copy-Item $Service  (Join-Path $Backup "live_dashboard_kpi_service_v2.py")
Copy-Item $Router   (Join-Path $Backup "gis_dashboard_kpi_v2.py")
Copy-Item $Frontend (Join-Path $Backup "LiveKpiDashboardV2.tsx")

Write-Host "BACKUP: $Backup" -ForegroundColor Yellow

# ------------------------------------------------------------
# Read files
# ------------------------------------------------------------

$serviceText = Get-Content $Service -Raw -Encoding UTF8
$routerText  = Get-Content $Router -Raw -Encoding UTF8
$frontText   = Get-Content $Frontend -Raw -Encoding UTF8

# ------------------------------------------------------------
# SERVICE
# ------------------------------------------------------------

# Add a single source of truth for the dashboard province.
if ($serviceText -notmatch "ZANJAN_PROVINCE_ID\s*=\s*5") {

    $marker = "from "

    $idx = $serviceText.IndexOf($marker)

    if ($idx -ge 0) {
        $lineEnd = $serviceText.IndexOf("`n", $idx)

        if ($lineEnd -ge 0) {
            $serviceText =
                $serviceText.Substring(0,$lineEnd+1) +
                "`n# =========================================================`n" +
                "# ZANJAN DASHBOARD SCOPE`n" +
                "# =========================================================`n" +
                "ZANJAN_PROVINCE_ID = 5`n" +
                "`n" +
                $serviceText.Substring($lineEnd+1)
        }
    }
}

# ------------------------------------------------------------
# ROUTER
# ------------------------------------------------------------

# Add a public constant to router so the frontend/API contract
# clearly identifies the dashboard as Zanjan-specific.
if ($routerText -notmatch "ZANJAN_PROVINCE_ID\s*=\s*5") {

    $marker = "router = APIRouter"

    if ($routerText.Contains($marker)) {
        $routerText = $routerText.Replace(
            $marker,
            "ZANJAN_PROVINCE_ID = 5`n`n$marker"
        )
    }
}

# ------------------------------------------------------------
# FRONTEND
# ------------------------------------------------------------

# Remove hard-coded province selector/list if one exists.
# The dashboard should open directly at Zanjan.
$frontText = $frontText -replace `
    '(?i)(selectedProvinceId\s*=\s*)[^;\r\n]+', `
    '${1}5'

$frontText = $frontText -replace `
    '(?i)(provinceId\s*:\s*)[^,\r\n]+', `
    '${1}5'

# Replace obvious province-list rendering with a fixed title
# only when the source contains a province selector/list.
$frontText = $frontText -replace `
    '(?i)انتخاب استان', `
    'استان زنجان'

# ------------------------------------------------------------
# WRITE UTF-8
# ------------------------------------------------------------

[System.IO.File]::WriteAllText(
    $Service,
    $serviceText,
    (New-Object System.Text.UTF8Encoding($false))
)

[System.IO.File]::WriteAllText(
    $Router,
    $routerText,
    (New-Object System.Text.UTF8Encoding($false))
)

[System.IO.File]::WriteAllText(
    $Frontend,
    $frontText,
    (New-Object System.Text.UTF8Encoding($false))
)

Write-Host ""
Write-Host "UPDATED:" -ForegroundColor Green
Write-Host $Service
Write-Host $Router
Write-Host $Frontend

# ------------------------------------------------------------
# IMPORTANT:
# Do NOT blindly alter SQL queries here.
# Verify current service query structure first.
# ------------------------------------------------------------

Write-Host ""
Write-Host "===== ZANJAN SCOPE CHECK =====" -ForegroundColor Cyan

Write-Host ""
Write-Host "--- SERVICE ---" -ForegroundColor DarkCyan
Get-Content $Service -Encoding UTF8 |
    Select-String -Pattern "ZANJAN_PROVINCE_ID|province_id|provinces|counties|units" -Context 2,4

Write-Host ""
Write-Host "--- ROUTER ---" -ForegroundColor DarkCyan
Get-Content $Router -Encoding UTF8 |
    Select-String -Pattern "ZANJAN_PROVINCE_ID|province_id|overview|provinces|counties|units" -Context 2,4

Write-Host ""
Write-Host "--- FRONTEND ---" -ForegroundColor DarkCyan
Get-Content $Frontend -Encoding UTF8 |
    Select-String -Pattern "province|استان|Zanjan|زنجان" -Context 1,2

# ------------------------------------------------------------
# PYTHON COMPILE
# ------------------------------------------------------------

Write-Host ""
Write-Host "===== PYTHON COMPILE =====" -ForegroundColor Cyan

py -3.12 -m py_compile $Service
if ($LASTEXITCODE -ne 0) {
    throw "Python compile failed: $Service"
}

py -3.12 -m py_compile $Router
if ($LASTEXITCODE -ne 0) {
    throw "Python compile failed: $Router"
}

Write-Host "Python compile: OK" -ForegroundColor Green

# ------------------------------------------------------------
# FRONTEND BUILD
# ------------------------------------------------------------

Write-Host ""
Write-Host "===== FRONTEND BUILD =====" -ForegroundColor Cyan

Push-Location (Join-Path $Root "pvimp_frontend")

npm run build

if ($LASTEXITCODE -ne 0) {
    Pop-Location
    throw "Frontend build failed."
}

Pop-Location

Write-Host "Frontend build: OK" -ForegroundColor Green

# ------------------------------------------------------------
# FINISH
# ------------------------------------------------------------

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "ZANJAN KPI V2 PREPARATION FINISHED" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Province scope: ZANJAN (ID=5)" -ForegroundColor Green
Write-Host ""
Write-Host "BACKUP:"
Write-Host $Backup
Write-Host ""
Write-Host "IMPORTANT:"
Write-Host "The SQL/data aggregation was NOT guessed or blindly rewritten."
Write-Host "Next we will verify the actual V2 service queries and then"
Write-Host "apply province_id=5 to every aggregation and drill-down."
Write-Host ""