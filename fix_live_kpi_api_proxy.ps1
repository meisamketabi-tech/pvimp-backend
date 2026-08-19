$ErrorActionPreference = "Stop"

$BackendRoot  = "D:\pvimp_backend"
$FrontendRoot = Join-Path $BackendRoot "pvimp_frontend"
$ViteConfigCandidates = @(
    (Join-Path $FrontendRoot "vite.config.ts"),
    (Join-Path $FrontendRoot "vite.config.js"),
    (Join-Path $FrontendRoot "vite.config.mts"),
    (Join-Path $FrontendRoot "vite.config.mjs")
)

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "FIX LIVE KPI API PROXY" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

$config = $ViteConfigCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $config) {
    throw "No vite.config.ts/js/mts/mjs was found in $FrontendRoot"
}

Write-Host "Vite config: $config" -ForegroundColor Green
$text = Get-Content $config -Raw -Encoding UTF8

# Backup once.
$backup = "$config.bak_live_kpi"
if (-not (Test-Path $backup)) {
    Copy-Item $config $backup -Force
    Write-Host "Backup: $backup" -ForegroundColor Yellow
}

# If a proxy already exists, do not blindly duplicate it.
if ($text -match 'proxy\s*:\s*\{') {
    if ($text -match "['""]?/api['""]?\s*:\s*\{") {
        Write-Host "An /api Vite proxy already exists. No config rewrite performed." -ForegroundColor Yellow
    }
    else {
        throw "vite.config already has a proxy section, but its structure is not safely recognizable. Inspect the file before changing it."
    }
}
else {
    # Add proxy to the object returned by defineConfig({...}).
    # Handles the common Vite shape:
    # export default defineConfig({
    #   plugins: [...]
    # })
    if ($text -notmatch 'defineConfig\s*\(\s*\{') {
        throw "Could not find defineConfig({ ... }) in vite.config. Inspect the file before changing it."
    }

    $replacement = @'
defineConfig({
  server: {
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true
      }
    }
  },
'@

    $text2 = [regex]::Replace(
        $text,
        'defineConfig\s*\(\s*\{\s*',
        $replacement,
        1
    )

    if ($text2 -eq $text) {
        throw "Could not inject Vite API proxy."
    }

    Set-Content -Path $config -Value $text2 -Encoding UTF8
    Write-Host "Added Vite /api -> http://127.0.0.1:8000 proxy: OK" -ForegroundColor Green
}

# Confirm the dashboard page uses the expected relative /api path.
$page = Join-Path $FrontendRoot "src\pages\LiveKpiDashboard.tsx"
if (Test-Path $page) {
    $pageText = Get-Content $page -Raw -Encoding UTF8
    if ($pageText -match 'fetch\s*\(\s*[`"''`]*/api/v1/gis/dashboard/kpi') {
        Write-Host "Dashboard API path detected: /api/v1/gis/dashboard/kpi..." -ForegroundColor Green
    }
    else {
        Write-Host "WARNING: Dashboard fetch path was not automatically confirmed." -ForegroundColor Yellow
    }
}

# Build.
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
Write-Host "API PROXY FIX FINISHED" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "IMPORTANT:"
Write-Host "1. Start FastAPI in a separate PowerShell:"
Write-Host "   cd D:\pvimp_backend"
Write-Host "   py -3.12 -m uvicorn app.main:app --reload"
Write-Host ""
Write-Host "2. Start Vite:"
Write-Host "   cd D:\pvimp_backend\pvimp_frontend"
Write-Host "   npm run dev"
Write-Host ""
Write-Host "3. Open:"
Write-Host "   http://localhost:5173/live-kpi"
Write-Host "============================================================" -ForegroundColor Cyan
