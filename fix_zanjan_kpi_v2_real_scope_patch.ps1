$ErrorActionPreference = "Stop"

$Root = "D:\pvimp_backend"
$Service = Join-Path $Root "app\services\gis\live_dashboard_kpi_service_v2.py"

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "PVIMP - PATCH ZANJAN KPI V2 REAL SCOPE" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

if (!(Test-Path $Service)) {
    throw "Service file not found: $Service"
}

$backup = Join-Path $Root ("_zanjan_kpi_v2_patch_backup_" + (Get-Date -Format "yyyyMMdd_HHmmss"))

New-Item -ItemType Directory -Path $backup -Force | Out-Null
Copy-Item $Service (Join-Path $backup "live_dashboard_kpi_service_v2.py") -Force

Write-Host "BACKUP: $backup" -ForegroundColor Yellow

$text = Get-Content $Service -Raw -Encoding UTF8

# ---------------------------------------------------------
# Helper: replace only first occurrence
# ---------------------------------------------------------
function Replace-First {
    param(
        [string]$Text,
        [string]$Old,
        [string]$New
    )

    $index = $Text.IndexOf($Old)

    if ($index -lt 0) {
        throw "Target text was not found."
    }

    return $Text.Substring(0, $index) +
           $New +
           $Text.Substring($index + $Old.Length)
}

# ---------------------------------------------------------
# Fix the Zanjan province scope in provinces()
# ---------------------------------------------------------

$old = @'
        rows = self.rows(
            f"""
            SELECT
                id,
                {self.ident(name)} AS name
            FROM {self.ident(table)}
            ORDER BY {self.ident(name)}
            """
        )
'@

$new = @'
        rows = self.rows(
            f"""
            SELECT
                id,
                {self.ident(name)} AS name
            FROM {self.ident(table)}
            WHERE id = :pid
            ORDER BY {self.ident(name)}
            """,
            {"pid": ZANJAN_PROVINCE_ID}
        )
'@

if ($text.Contains($old)) {
    $text = Replace-First $text $old $new
    Write-Host "provinces(): Zanjan filter patched." -ForegroundColor Green
}
else {
    Write-Host "provinces(): filter already patched or target differs." -ForegroundColor DarkYellow
}

# ---------------------------------------------------------
# Add hard Zanjan validation to counties()
# ---------------------------------------------------------

$old = @'
    def counties(
        self,
        province_id: int,
        metric="all"
    ):

        table = self.county_table()
'@

$new = @'
    def counties(
        self,
        province_id: int,
        metric="all"
    ):

        # Dashboard is exclusively scoped to Zanjan.
        if int(province_id) != ZANJAN_PROVINCE_ID:
            return []

        table = self.county_table()
'@

if ($text.Contains($old)) {
    $text = Replace-First $text $old $new
    Write-Host "counties(): hard Zanjan validation patched." -ForegroundColor Green
}
else {
    Write-Host "counties(): validation already patched or target differs." -ForegroundColor DarkYellow
}

# ---------------------------------------------------------
# Write file
# ---------------------------------------------------------

Set-Content `
    -Path $Service `
    -Value $text `
    -Encoding UTF8

Write-Host ""
Write-Host "UPDATED:" -ForegroundColor Green
Write-Host $Service

# ---------------------------------------------------------
# Python compile
# ---------------------------------------------------------

Write-Host ""
Write-Host "===== PYTHON COMPILE =====" -ForegroundColor Cyan

Push-Location $Root

try {
    py -3.12 -m py_compile `
        .\app\services\gis\live_dashboard_kpi_service_v2.py

    Write-Host "Python compile: OK" -ForegroundColor Green
}
finally {
    Pop-Location
}

# ---------------------------------------------------------
# Show relevant scope
# ---------------------------------------------------------

Write-Host ""
Write-Host "===== ZANJAN SCOPE CHECK =====" -ForegroundColor Cyan

Get-Content $Service -Encoding UTF8 |
    Select-String `
        -Pattern `
        "ZANJAN_PROVINCE_ID|def provinces|def counties|def units|province_id|WHERE id = :pid" `
        -Context 0,4

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "PATCH FINISHED" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backup:" -ForegroundColor Yellow
Write-Host $backup
Write-Host ""
Write-Host "Next: restart Uvicorn and test provinces/counties." -ForegroundColor Cyan