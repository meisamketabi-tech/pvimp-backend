# ============================================================
# PVIMP - Vaccination KPI Command Center Theme
# Applies a dark/futuristic dashboard visual layer WITHOUT
# changing the existing vaccination API/data logic.
# ============================================================

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$project = "D:\pvimp_backend\pvimp_frontend"
Set-Location $project

$page = ".\src\pages\VaccinationVaccineReport.tsx"
$css  = ".\src\pages\VaccinationDashboard.css"

if (-not (Test-Path $page)) {
    throw "VaccinationVaccineReport.tsx not found: $page"
}

# ------------------------------------------------------------
# 1) BACKUP
# ------------------------------------------------------------
$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backup = "$page.bak_before_command_center_$stamp"
Copy-Item $page $backup -Force

if (Test-Path $css) {
    Copy-Item $css "$css.bak_$stamp" -Force
}

# ------------------------------------------------------------
# 2) CREATE THE VISUAL THEME
# ------------------------------------------------------------
@'
/* ============================================================
   PVIMP - Vaccination KPI Command Center
   Visual-only layer. Existing API/data logic is untouched.
   ============================================================ */

.vaccination-command-center {
  --vc-bg: #03111f;
  --vc-bg-2: #061a2d;
  --vc-panel: rgba(8, 30, 50, 0.92);
  --vc-panel-2: rgba(10, 40, 63, 0.82);
  --vc-border: rgba(47, 213, 255, 0.28);
  --vc-border-strong: rgba(47, 213, 255, 0.62);
  --vc-cyan: #22d3ee;
  --vc-cyan-2: #06b6d4;
  --vc-green: #20e3a2;
  --vc-yellow: #f6c945;
  --vc-red: #ff4d5f;
  --vc-magenta: #f15cff;
  --vc-text: #edfaff;
  --vc-muted: #8eafc2;
  --vc-grid: rgba(76, 203, 255, 0.055);

  position: relative;
  min-height: 100vh;
  padding: 26px 30px 60px;
  overflow: hidden;
  color: var(--vc-text);
  background:
    radial-gradient(circle at 50% -10%, rgba(0, 194, 255, 0.12), transparent 38%),
    radial-gradient(circle at 10% 70%, rgba(0, 120, 255, 0.07), transparent 30%),
    linear-gradient(180deg, #03111f 0%, #020b16 100%);
  font-family: Tahoma, "Segoe UI", sans-serif;
}

/* subtle command-center grid */
.vaccination-command-center::before {
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  background-image:
    linear-gradient(var(--vc-grid) 1px, transparent 1px),
    linear-gradient(90deg, var(--vc-grid) 1px, transparent 1px);
  background-size: 44px 44px;
  mask-image: linear-gradient(to bottom, rgba(0,0,0,.75), transparent 92%);
}

.vaccination-command-center > * {
  position: relative;
  z-index: 1;
}

/* ------------------------------------------------------------
   HEADER
   ------------------------------------------------------------ */
.vaccination-command-center .dashboard-header {
  position: relative;
  display: grid;
  grid-template-columns: auto 1fr;
  grid-template-areas:
    "back title"
    "back subtitle";
  align-items: center;
  gap: 4px 22px;
  min-height: 118px;
  margin-bottom: 18px;
  padding: 24px 28px;
  border: 1px solid var(--vc-border-strong);
  border-radius: 18px;
  background:
    linear-gradient(135deg, rgba(10, 64, 84, .88), rgba(4, 26, 45, .94));
  box-shadow:
    inset 0 0 28px rgba(34, 211, 238, .07),
    0 16px 50px rgba(0, 0, 0, .28);
  overflow: hidden;
}

.vaccination-command-center .dashboard-header::before {
  content: "";
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  height: 3px;
  background: linear-gradient(
    90deg,
    transparent,
    var(--vc-cyan),
    var(--vc-magenta),
    transparent
  );
  opacity: .9;
}

.vaccination-command-center .dashboard-header h1 {
  grid-area: title;
  margin: 0;
  color: #f5fdff;
  font-size: clamp(24px, 2.2vw, 34px);
  font-weight: 900;
  letter-spacing: -.4px;
  text-shadow: 0 0 18px rgba(34, 211, 238, .18);
}

.vaccination-command-center .dashboard-header p {
  grid-area: subtitle;
  margin: 5px 0 0;
  color: var(--vc-muted);
  font-size: 13px;
}

.vaccination-command-center .dashboard-header button {
  grid-area: back;
  align-self: start;
  min-width: 130px;
  border: 1px solid rgba(34, 211, 238, .35);
  border-radius: 10px;
  padding: 9px 14px;
  color: #dffaff;
  background: rgba(0, 160, 190, .12);
  cursor: pointer;
  transition: .2s ease;
}

.vaccination-command-center .dashboard-header button:hover {
  border-color: var(--vc-cyan);
  background: rgba(34, 211, 238, .16);
  box-shadow: 0 0 18px rgba(34, 211, 238, .16);
}

/* ------------------------------------------------------------
   KPI CARDS
   ------------------------------------------------------------ */
.vaccination-command-center .kpi-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 12px;
  margin: 0 0 16px;
}

.vaccination-command-center .kpi-card {
  position: relative;
  min-height: 112px;
  padding: 16px 17px;
  border: 1px solid var(--vc-border);
  border-radius: 14px;
  background:
    linear-gradient(145deg, rgba(11, 43, 66, .94), rgba(5, 23, 39, .94));
  box-shadow:
    inset 0 0 24px rgba(34, 211, 238, .025),
    0 8px 26px rgba(0,0,0,.20);
  overflow: hidden;
}

.vaccination-command-center .kpi-card::after {
  content: "";
  position: absolute;
  right: 12px;
  left: 12px;
  bottom: 0;
  height: 2px;
  background: linear-gradient(
    90deg,
    transparent,
    var(--vc-cyan),
    transparent
  );
  opacity: .5;
}

.vaccination-command-center .kpi-card:hover {
  border-color: rgba(34, 211, 238, .55);
  transform: translateY(-1px);
  box-shadow:
    inset 0 0 24px rgba(34, 211, 238, .05),
    0 10px 30px rgba(0,0,0,.28);
}

.vaccination-command-center .kpi-title {
  color: var(--vc-muted);
  font-size: 12px;
  font-weight: 700;
  margin-bottom: 11px;
}

.vaccination-command-center .kpi-value {
  color: #f4fbff;
  font-size: clamp(25px, 2vw, 34px);
  line-height: 1;
  font-weight: 900;
  letter-spacing: -.7px;
  text-shadow: 0 0 14px rgba(34, 211, 238, .10);
}

/* emphasize the first KPI */
.vaccination-command-center .kpi-card:first-child {
  border-color: rgba(34, 211, 238, .62);
  background:
    radial-gradient(circle at 80% 10%, rgba(34,211,238,.14), transparent 42%),
    linear-gradient(145deg, rgba(10, 61, 80, .96), rgba(4, 27, 43, .96));
}

/* ------------------------------------------------------------
   PANELS / GRID
   ------------------------------------------------------------ */
.vaccination-command-center .dashboard-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  gap: 14px;
  margin-top: 14px !important;
}

.vaccination-command-center .dashboard-panel,
.vaccination-command-center .panel {
  position: relative;
  border: 1px solid var(--vc-border);
  border-radius: 16px;
  padding: 18px;
  background:
    linear-gradient(145deg, rgba(8, 31, 51, .96), rgba(3, 18, 31, .96));
  box-shadow:
    inset 0 0 34px rgba(34, 211, 238, .025),
    0 10px 34px rgba(0,0,0,.22);
}

.vaccination-command-center .dashboard-panel::before,
.vaccination-command-center .panel::before {
  content: "";
  position: absolute;
  top: 0;
  right: 22px;
  width: 90px;
  height: 2px;
  background: linear-gradient(90deg, var(--vc-cyan), transparent);
  opacity: .75;
}

.vaccination-command-center .dashboard-panel h2,
.vaccination-command-center .panel h2 {
  margin: 0 0 13px;
  color: #e9fbff;
  font-size: 16px;
  font-weight: 900;
}

.vaccination-command-center .dashboard-panel > p,
.vaccination-command-center .panel > p {
  color: var(--vc-muted);
}

/* ------------------------------------------------------------
   CHARTS
   ------------------------------------------------------------ */
.vaccination-command-center .recharts-wrapper {
  direction: ltr;
}

.vaccination-command-center .recharts-cartesian-axis-tick-value {
  fill: #91afc0 !important;
  font-size: 11px;
}

.vaccination-command-center .recharts-cartesian-axis-line,
.vaccination-command-center .recharts-cartesian-axis-tick-line {
  stroke: rgba(145, 196, 216, .25) !important;
}

.vaccination-command-center .recharts-cartesian-grid-horizontal line,
.vaccination-command-center .recharts-cartesian-grid-vertical line {
  stroke: rgba(109, 185, 214, .08) !important;
}

.vaccination-command-center .recharts-legend-item-text {
  color: #b8d2df !important;
  font-size: 11px;
}

.vaccination-command-center .recharts-tooltip-wrapper .recharts-default-tooltip {
  border: 1px solid rgba(34,211,238,.35) !important;
  border-radius: 10px !important;
  background: rgba(3, 18, 31, .96) !important;
  color: #effcff !important;
  box-shadow: 0 10px 30px rgba(0,0,0,.4);
}

/* ------------------------------------------------------------
   TABLES
   ------------------------------------------------------------ */
.vaccination-command-center table {
  color: #dff5ff;
}

.vaccination-command-center thead {
  background:
    linear-gradient(90deg, rgba(12, 67, 88, .9), rgba(7, 35, 56, .9));
}

.vaccination-command-center th {
  padding: 12px 10px !important;
  color: #9feaff !important;
  font-size: 11px !important;
  font-weight: 900;
  white-space: nowrap;
  border-bottom: 1px solid rgba(34,211,238,.25);
}

.vaccination-command-center td {
  padding: 11px 10px !important;
  color: #c9e0ea !important;
  font-size: 11px !important;
  border-top: 1px solid rgba(105, 164, 188, .10) !important;
}

.vaccination-command-center tbody tr {
  transition: background .16s ease, transform .16s ease;
}

.vaccination-command-center tbody tr:hover {
  background: rgba(34, 211, 238, .055);
}

/* status column readability */
.vaccination-command-center td:last-child {
  font-weight: 800;
}

/* ------------------------------------------------------------
   MANAGEMENT SUMMARY
   ------------------------------------------------------------ */
.vaccination-command-center .ai-box {
  border-color: rgba(241, 92, 255, .35) !important;
  background:
    radial-gradient(circle at 85% 15%, rgba(241,92,255,.10), transparent 35%),
    linear-gradient(145deg, rgba(24, 25, 54, .96), rgba(6, 18, 35, .96));
}

.vaccination-command-center .ai-box::before {
  background: linear-gradient(90deg, var(--vc-magenta), transparent);
}

.vaccination-command-center .ai-box h2 {
  color: #f6d9ff;
}

/* ------------------------------------------------------------
   ERROR / LOADING
   ------------------------------------------------------------ */
.vaccination-command-center button {
  font-family: inherit;
}

.vaccination-command-center .panel button {
  border: 1px solid rgba(34,211,238,.45);
  border-radius: 10px;
  padding: 9px 16px;
  color: #e9fbff;
  background: rgba(34,211,238,.10);
  cursor: pointer;
}

/* ------------------------------------------------------------
   SCROLLBARS
   ------------------------------------------------------------ */
.vaccination-command-center ::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.vaccination-command-center ::-webkit-scrollbar-track {
  background: #03111f;
}

.vaccination-command-center ::-webkit-scrollbar-thumb {
  background: #0b536b;
  border-radius: 20px;
}

.vaccination-command-center ::-webkit-scrollbar-thumb:hover {
  background: #0d7f9f;
}

/* ------------------------------------------------------------
   RESPONSIVE
   ------------------------------------------------------------ */
@media (max-width: 1280px) {
  .vaccination-command-center {
    padding: 22px 20px 50px;
  }

  .vaccination-command-center .kpi-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

@media (max-width: 900px) {
  .vaccination-command-center .dashboard-grid {
    grid-template-columns: 1fr;
  }

  .vaccination-command-center .dashboard-header {
    grid-template-columns: 1fr;
    grid-template-areas:
      "title"
      "subtitle"
      "back";
  }

  .vaccination-command-center .dashboard-header button {
    justify-self: start;
  }
}

@media (max-width: 620px) {
  .vaccination-command-center {
    padding: 14px 10px 36px;
  }

  .vaccination-command-center .kpi-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 9px;
  }

  .vaccination-command-center .kpi-card {
    min-height: 95px;
    padding: 13px;
  }

  .vaccination-command-center .kpi-value {
    font-size: 23px;
  }

  .vaccination-command-center .dashboard-panel,
  .vaccination-command-center .panel {
    padding: 12px;
  }
}
'@ | Set-Content $css -Encoding UTF8

# ------------------------------------------------------------
# 3) IMPORT THE THEME CSS
# ------------------------------------------------------------
$text = Get-Content $page -Raw -Encoding UTF8

if ($text -notmatch 'VaccinationDashboard\.css') {
    $text = $text -replace '(import React, [^\r\n]+;\r?\n)', ('$1import "./VaccinationDashboard.css";' + [Environment]::NewLine)
}

# Add a page-specific wrapper class to every dashboard-page instance.
$text = $text -replace 'className="dashboard-page"', 'className="dashboard-page vaccination-command-center"'

Set-Content $page $text -Encoding UTF8

# ------------------------------------------------------------
# 4) BUILD CHECK
# ------------------------------------------------------------
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "PVIMP VACCINATION COMMAND CENTER APPLIED" -ForegroundColor Green
Write-Host "Backup: $backup" -ForegroundColor DarkGray
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

npm run build

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "BUILD FAILED - restoring page backup..." -ForegroundColor Red
    Copy-Item $backup $page -Force
    throw "Frontend build failed. Original VaccinationVaccineReport.tsx restored."
}

Write-Host ""
Write-Host "BUILD OK" -ForegroundColor Green
Write-Host ""

# ------------------------------------------------------------
# 5) OPTIONAL GIT CHECKPOINT
# ------------------------------------------------------------
Write-Host "Git status:" -ForegroundColor Yellow
git status --short

Write-Host ""
Write-Host "برای ثبت بک‌آپ روی Git:" -ForegroundColor Yellow
Write-Host 'git add src/pages/VaccinationVaccineReport.tsx src/pages/VaccinationDashboard.css'
Write-Host 'git commit -m "ui: redesign vaccination KPI command center"'
Write-Host 'git push'

