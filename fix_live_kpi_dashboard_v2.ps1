#requires -Version 5.1

$ErrorActionPreference = "Stop"

$BackendRoot = "D:\pvimp_backend"
$RouterFile  = Join-Path $BackendRoot "app\api\v1\router.py"
$ServiceFile = Join-Path $BackendRoot "app\services\gis\live_dashboard_kpi_service_v2.py"
$EndpointFile = Join-Path $BackendRoot "app\api\v1\endpoints\gis_dashboard_kpi_v2.py"
$FrontendFile = Join-Path $BackendRoot "pvimp_frontend\src\pages\LiveKpiDashboardV2.tsx"

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "PVIMP - FIX LIVE KPI DASHBOARD V2" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# ------------------------------------------------------------
# Validate files
# ------------------------------------------------------------

foreach ($p in @($RouterFile,$ServiceFile,$EndpointFile,$FrontendFile)) {
    if (-not (Test-Path $p)) {
        throw "Required file not found: $p"
    }
}

Write-Host "Required V2 files: OK" -ForegroundColor Green

# ------------------------------------------------------------
# Backup router
# ------------------------------------------------------------

$backupDir = Join-Path $BackendRoot "_dashboard_kpi_v2_fix_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
New-Item -ItemType Directory -Force -Path $backupDir | Out-Null

$routerBackup = Join-Path $backupDir "router.py"
Copy-Item $RouterFile $routerBackup -Force

Write-Host "Router backup: $routerBackup" -ForegroundColor DarkGray

# ------------------------------------------------------------
# Read router
# ------------------------------------------------------------

$routerText = [System.IO.File]::ReadAllText(
    $RouterFile,
    [System.Text.UTF8Encoding]::new($false)
)

# ------------------------------------------------------------
# V2 import
# ------------------------------------------------------------

$importBlock = @'
# =========================================================
# Live GIS Dashboard KPI V2
# =========================================================

from app.api.v1.endpoints.gis_dashboard_kpi_v2 import (
    router as gis_dashboard_kpi_v2_router,
)

'@

if ($routerText -notmatch "gis_dashboard_kpi_v2_router") {

    $marker = "from app.api.v1.endpoints.gis_dashboard_kpi import ("

    $index = $routerText.IndexOf($marker)

    if ($index -ge 0) {
        $routerText = $routerText.Insert($index, $importBlock)
    }
    else {
        # Fallback: insert after FastAPI import
        $fastapiMarker = "from fastapi import APIRouter"
        $fastapiIndex = $routerText.IndexOf($fastapiMarker)

        if ($fastapiIndex -ge 0) {
            $lineEnd = $routerText.IndexOf("`n", $fastapiIndex)

            if ($lineEnd -ge 0) {
                $routerText = $routerText.Insert(
                    $lineEnd + 1,
                    "`r`n" + $importBlock
                )
            }
            else {
                $routerText = $importBlock + $routerText
            }
        }
        else {
            throw "Could not find a safe location for V2 import."
        }
    }

    Write-Host "V2 import added." -ForegroundColor Green
}
else {
    Write-Host "V2 import already exists." -ForegroundColor Yellow
}

# ------------------------------------------------------------
# V2 include_router
# ------------------------------------------------------------

$includeLine = "api_router.include_router(gis_dashboard_kpi_v2_router)"

if ($routerText -notmatch [regex]::Escape($includeLine)) {

    $anchor = "api_router.include_router(gis_dashboard_kpi_router)"

    $anchorIndex = $routerText.IndexOf($anchor)

    if ($anchorIndex -ge 0) {

        $lineEnd = $routerText.IndexOf("`n", $anchorIndex)

        if ($lineEnd -ge 0) {
            $insertText = "`r`n# =========================================================`r`n# Live GIS Dashboard KPI V2`r`n# =========================================================`r`n$includeLine"

            $routerText = $routerText.Insert(
                $lineEnd + 1,
                $insertText
            )
        }
        else {
            $routerText += "`r`n`r`n$includeLine`r`n"
        }

    }
    else {

        # Fallback: add after router registry loop.
        $routerText = $routerText.TrimEnd() +
            "`r`n`r`n# =========================================================`r`n" +
            "# Live GIS Dashboard KPI V2`r`n" +
            "# =========================================================`r`n" +
            "$includeLine`r`n"
    }

    Write-Host "V2 router registration added." -ForegroundColor Green
}
else {
    Write-Host "V2 router registration already exists." -ForegroundColor Yellow
}

# ------------------------------------------------------------
# Write router UTF-8 without BOM
# ------------------------------------------------------------

[System.IO.File]::WriteAllText(
    $RouterFile,
    $routerText,
    [System.Text.UTF8Encoding]::new($false)
)

Write-Host "Updated: $RouterFile" -ForegroundColor Green

# ------------------------------------------------------------
# Python compile
# ------------------------------------------------------------

Push-Location $BackendRoot

try {

    Write-Host ""
    Write-Host "===== PYTHON COMPILE =====" -ForegroundColor Cyan

    py -3.12 -m py_compile `
        $ServiceFile `
        $EndpointFile

    Write-Host "V2 Python compile: OK" -ForegroundColor Green

    Write-Host ""
    Write-Host "===== ROUTER IMPORT =====" -ForegroundColor Cyan

    py -3.12 -c "from app.api.v1.router import api_router; print('api_router import OK'); print('routes:', len(api_router.routes))"

    Write-Host "Router import: OK" -ForegroundColor Green

    Write-Host ""
    Write-Host "===== V2 ROUTER IMPORT =====" -ForegroundColor Cyan

    py -3.12 -c "from app.api.v1.endpoints.gis_dashboard_kpi_v2 import router; print('V2 router import OK:', router.prefix)"

    Write-Host "V2 router import: OK" -ForegroundColor Green

}
finally {
    Pop-Location
}

# ------------------------------------------------------------
# Frontend validation
# ------------------------------------------------------------

$FrontendRoot = Join-Path $BackendRoot "pvimp_frontend"

if (Test-Path (Join-Path $FrontendRoot "package.json")) {

    Push-Location $FrontendRoot

    try {

        Write-Host ""
        Write-Host "===== FRONTEND BUILD =====" -ForegroundColor Cyan

        npm run build

        if ($LASTEXITCODE -ne 0) {
            throw "Frontend build failed."
        }

        Write-Host "Frontend build: OK" -ForegroundColor Green

    }
    finally {
        Pop-Location
    }

}
else {
    Write-Host "package.json not found. Frontend build skipped." -ForegroundColor Yellow
}

# ------------------------------------------------------------
# Final verification
# ------------------------------------------------------------

Write-Host ""
Write-Host "===== FINAL ROUTER CHECK =====" -ForegroundColor Cyan

$verify = [System.IO.File]::ReadAllText(
    $RouterFile,
    [System.Text.UTF8Encoding]::new($false)
)

if ($verify -match "gis_dashboard_kpi_v2_router") {
    Write-Host "V2 router registration: PRESENT" -ForegroundColor Green
}
else {
    throw "V2 router registration was not found after modification."
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "V2 ROUTER FIX FINISHED" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backend:"
Write-Host "  $ServiceFile"
Write-Host "  $EndpointFile"
Write-Host ""
Write-Host "Frontend:"
Write-Host "  $FrontendFile"
Write-Host ""
Write-Host "API:"
Write-Host "  /api/v1/gis/dashboard/kpi/v2/..."
Write-Host ""
Write-Host "Backup:"
Write-Host "  $backupDir"
Write-Host ""
Write-Host "Next step:"
Write-Host "  Restart Uvicorn and test the V2 API."
Write-Host ""