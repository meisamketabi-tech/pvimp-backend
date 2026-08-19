$ErrorActionPreference = "Stop"

$BackendRoot  = "D:\pvimp_backend"
$FrontendRoot = Join-Path $BackendRoot "pvimp_frontend"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "FIX LIVE KPI API PROXY - V2" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

$configCandidates = @(
    "vite.config.ts",
    "vite.config.js",
    "vite.config.mts",
    "vite.config.mjs"
) | ForEach-Object { Join-Path $FrontendRoot $_ }

$config = $configCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1

if (-not $config) {
    $config = Join-Path $FrontendRoot "vite.config.ts"

    @'
import { defineConfig } from "vite";

export default defineConfig({
  server: {
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true
      }
    }
  }
});
'@ | Set-Content -Path $config -Encoding UTF8

    Write-Host "No Vite config existed." -ForegroundColor Yellow
    Write-Host "Created: $config" -ForegroundColor Green
}
else {
    Write-Host "Found Vite config: $config" -ForegroundColor Green

    $text = Get-Content $config -Raw -Encoding UTF8

    if ($text -match 'proxy\s*:') {
        Write-Host "A proxy section already exists. No automatic rewrite performed." -ForegroundColor Yellow
    }
    elseif ($text -match 'defineConfig\s*\(\s*\{') {
        $backup = "$config.bak_live_kpi_v2"
        if (-not (Test-Path $backup)) {
            Copy-Item $config $backup -Force
            Write-Host "Backup: $backup" -ForegroundColor Yellow
        }

        $inject = @'
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

        $newText = [regex]::Replace(
            $text,
            'defineConfig\s*\(\s*\{\s*',
            $inject,
            1
        )

        if ($newText -eq $text) {
            throw "Could not safely add the /api proxy to $config"
        }

        Set-Content -Path $config -Value $newText -Encoding UTF8
        Write-Host "Added /api proxy: OK" -ForegroundColor Green
    }
    else {
        throw "Existing Vite config has an unrecognized structure. No changes made."
    }
}

$page = Join-Path $FrontendRoot "src\pages\LiveKpiDashboard.tsx"
if (-not (Test-Path $page)) {
    throw "LiveKpiDashboard.tsx not found: $page"
}

Write-Host ""
Write-Host "=== Frontend build ===" -ForegroundColor Cyan

Push-Location $FrontendRoot
try {
    npm run build
    if ($LASTEXITCODE -ne 0) {
        throw "Frontend build failed with exit code $LASTEXITCODE"
    }
}
finally {
    Pop-Location
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "API PROXY CONFIGURED SUCCESSFULLY" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Start backend in another PowerShell:"
Write-Host "  cd D:\pvimp_backend"
Write-Host "  py -3.12 -m uvicorn app.main:app --reload"
Write-Host ""
Write-Host "Then start frontend:"
Write-Host "  cd D:\pvimp_backend\pvimp_frontend"
Write-Host "  npm run dev"
Write-Host ""
Write-Host "Open:"
Write-Host "  http://localhost:5173/live-kpi"
Write-Host "============================================================"
