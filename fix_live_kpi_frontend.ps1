$ErrorActionPreference = "Stop"

$BackendRoot  = "D:\pvimp_backend"
$FrontendRoot = Join-Path $BackendRoot "pvimp_frontend"
$RouterFile   = Join-Path $FrontendRoot "src\router\AppRouter.tsx"
$PageFile     = Join-Path $FrontendRoot "src\pages\LiveKpiDashboard.tsx"
$CssFile      = Join-Path $FrontendRoot "src\pages\LiveKpiDashboard.css"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "FIX LIVE KPI FRONTEND" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# 1) Verify the generated page actually exists.
if (-not (Test-Path $PageFile)) {
    throw "LiveKpiDashboard.tsx not found: $PageFile"
}
if (-not (Test-Path $CssFile)) {
    throw "LiveKpiDashboard.css not found: $CssFile"
}
Write-Host "KPI page exists: OK" -ForegroundColor Green

# 2) Fix AppRouter.tsx import path.
if (-not (Test-Path $RouterFile)) {
    throw "AppRouter.tsx not found: $RouterFile"
}

$router = Get-Content $RouterFile -Raw -Encoding UTF8

$oldImport = 'import LiveKpiDashboard from "./pages/LiveKpiDashboard";'
$newImport = 'import LiveKpiDashboard from "../pages/LiveKpiDashboard";'

if ($router.Contains($oldImport)) {
    $router = $router.Replace($oldImport, $newImport)
    Set-Content -Path $RouterFile -Value $router -Encoding UTF8
    Write-Host "Fixed AppRouter import: OK" -ForegroundColor Green
}
elseif ($router.Contains($newImport)) {
    Write-Host "AppRouter import already correct: OK" -ForegroundColor Green
}
else {
    throw "LiveKpiDashboard import was not found in AppRouter.tsx. Current file must be inspected before changing it."
}

# 3) Remove accidental PowerShell build files copied into frontend root.
$badFiles = @(
    (Join-Path $FrontendRoot "build_live_kpi_dashboard.ps1"),
    (Join-Path $FrontendRoot "build_live_kpi_dashboard_fixed.ps1")
)

foreach ($f in $badFiles) {
    if (Test-Path $f) {
        Remove-Item -LiteralPath $f -Force
        Write-Host "Removed accidental frontend-root file: $f" -ForegroundColor Yellow
    }
}

# 4) Clear Vite cache if present.
$viteCache = Join-Path $FrontendRoot "node_modules\.vite"
if (Test-Path $viteCache) {
    Remove-Item $viteCache -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "Cleared Vite cache." -ForegroundColor Yellow
}

# 5) Build frontend and fail correctly if TypeScript/Vite fails.
Push-Location $FrontendRoot
try {
    Write-Host ""
    Write-Host "=== npm run build ===" -ForegroundColor Cyan
    npm run build
    if ($LASTEXITCODE -ne 0) {
        throw "Frontend build failed with exit code $LASTEXITCODE"
    }
    Write-Host "Frontend build: OK" -ForegroundColor Green
}
finally {
    Pop-Location
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "FIX FINISHED SUCCESSFULLY" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Dashboard route: /live-kpi"
Write-Host "Now start frontend from:"
Write-Host "  D:\pvimp_backend\pvimp_frontend"
Write-Host "with: npm run dev"
