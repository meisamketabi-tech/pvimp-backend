$ErrorActionPreference = "Stop"

$ROOT = "D:\pvimp_backend"

$SERVICE = Join-Path $ROOT "app\services\gis\live_dashboard_kpi_service_v2.py"
$ROUTER  = Join-Path $ROOT "app\api\v1\endpoints\gis_dashboard_kpi_v2.py"

$STAMP = Get-Date -Format "yyyyMMdd_HHmmss"
$BACKUP = Join-Path $ROOT "_zanjan_kpi_v2_real_scope_backup_$STAMP"

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "PVIMP - ZANJAN KPI V2 REAL DATA SCOPE" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

New-Item -ItemType Directory -Path $BACKUP -Force | Out-Null

Copy-Item $SERVICE (Join-Path $BACKUP "live_dashboard_kpi_service_v2.py") -Force
Copy-Item $ROUTER  (Join-Path $BACKUP "gis_dashboard_kpi_v2.py") -Force

Write-Host "BACKUP: $BACKUP" -ForegroundColor Yellow


# ============================================================
# SERVICE
# ============================================================

$content = Get-Content $SERVICE -Raw -Encoding UTF8

# ------------------------------------------------------------
# 1. Add Zanjan scope helpers after __init__
# ------------------------------------------------------------

$marker = @'
    # ---------------------------------------------------------
    # Generic helpers
    # ---------------------------------------------------------
'@

$insert = @'
    # ---------------------------------------------------------
    # Zanjan scope
    # ---------------------------------------------------------

    @staticmethod
    def zanjan_id():
        return 5

    def zanjan_unit_ids_sql(self, unit_table=None):
        """
        Returns SQL subquery containing ONLY epidemiology units
        belonging to Zanjan province.
        """

        table = unit_table or self.unit_table()

        if not table:
            return "SELECT NULL WHERE FALSE"

        province_fk = self.pick(
            table,
            "province_id"
        )

        if not province_fk:
            return "SELECT NULL WHERE FALSE"

        return f"""
            SELECT id
            FROM {self.ident(table)}
            WHERE {self.ident(province_fk)} = :zanjan_province_id
        """

    def scoped_count(self, table, unit_fk=None, extra_where="TRUE", params=None):

        if not table:
            return 0

        if not self.has_table(table):
            return 0

        params = dict(params or {})
        params["zanjan_province_id"] = self.zanjan_id()

        units = self.unit_table()

        if not units:
            return 0

        if not unit_fk:
            unit_fk = self.pick(
                table,
                "epidemiology_unit_id"
            )

        if not unit_fk:
            return 0

        province_fk = self.pick(
            units,
            "province_id"
        )

        if not province_fk:
            return 0

        return self.count(
            table,
            f"""
                {self.ident(unit_fk)} IN (
                    SELECT id
                    FROM {self.ident(units)}
                    WHERE {self.ident(province_fk)}
                          = :zanjan_province_id
                )
                AND
                ({extra_where})
            """,
            params
        )

    def scoped_sum_column(
        self,
        table,
        column,
        unit_fk=None,
        extra_where="TRUE",
        params=None
    ):

        if not table or not column:
            return 0.0

        if not self.has_table(table):
            return 0.0

        units = self.unit_table()

        if not units:
            return 0.0

        unit_fk = unit_fk or self.pick(
            table,
            "epidemiology_unit_id"
        )

        province_fk = self.pick(
            units,
            "province_id"
        )

        if not unit_fk or not province_fk:
            return 0.0

        params = dict(params or {})
        params["zanjan_province_id"] = self.zanjan_id()

        return float(
            self.scalar(
                f"""
                SELECT COALESCE(
                    SUM(src.{self.ident(column)}),
                    0
                )
                FROM {self.ident(table)} src
                WHERE
                    src.{self.ident(unit_fk)} IN (
                        SELECT u.id
                        FROM {self.ident(units)} u
                        WHERE u.{self.ident(province_fk)}
                              = :zanjan_province_id
                    )
                    AND
                    ({extra_where})
                """,
                params,
                0
            )
        )

    def unit_belongs_to_zanjan(self, unit_id: int):

        table = self.unit_table()

        if not table:
            return False

        province_fk = self.pick(
            table,
            "province_id"
        )

        if not province_fk:
            return False

        value = self.scalar(
            f"""
            SELECT COUNT(*)
            FROM {self.ident(table)}
            WHERE id=:unit_id
              AND {self.ident(province_fk)}
                  = :zanjan_province_id
            """,
            {
                "unit_id": unit_id,
                "zanjan_province_id": self.zanjan_id()
            },
            0
        )

        return int(value) > 0


'@

if ($content -notmatch "def scoped_count") {
    $content = $content.Replace($marker, $insert + $marker)
    Write-Host "Added Zanjan scope helpers." -ForegroundColor Green
}
else {
    Write-Host "Zanjan scope helpers already exist." -ForegroundColor DarkYellow
}


# ============================================================
# 2. Replace provinces() so ONLY Zanjan is returned
# ============================================================

$start = $content.IndexOf("    def provinces(self, metric=""all""):")
$end   = $content.IndexOf("    # ---------------------------------------------------------`r`n    # Counties", $start)

if ($end -lt 0) {
    $end = $content.IndexOf("    # ---------------------------------------------------------`n    # Counties", $start)
}

if ($start -ge 0 -and $end -gt $start) {

    $newMethod = @'
    def provinces(self, metric="all"):

        table = self.province_table()

        if not table:
            return []

        name = self.name_column(table)

        if not name:
            name = "id"

        rows = self.rows(
            f"""
            SELECT
                id,
                {self.ident(name)} AS name
            FROM {self.ident(table)}
            WHERE id=:pid
            ORDER BY {self.ident(name)}
            """,
            {
                "pid": self.zanjan_id()
            }
        )

        result = []

        for row in rows:

            pid = row["id"]

            value = self.location_metric(
                "province",
                pid,
                metric
            )

            result.append({
                "id": pid,
                "name": row["name"] or "زنجان",
                "value": value
            })

        return self.clean(result)

'@

    $content = $content.Substring(0, $start) +
               $newMethod +
               $content.Substring($end)

    Write-Host "provinces(): Zanjan-only." -ForegroundColor Green
}


# ============================================================
# 3. Protect counties() against non-Zanjan province
# ============================================================

$needle = @'
        if not province_fk:
            return []

        name = self.name_column(table)
'@

$replacement = @'
        if not province_fk:
            return []

        # HARD SCOPE: only Zanjan province
        if int(province_id) != self.zanjan_id():
            return []

        name = self.name_column(table)
'@

if ($content.Contains($needle)) {
    $content = $content.Replace($needle, $replacement)
    Write-Host "counties(): non-Zanjan blocked." -ForegroundColor Green
}


# ============================================================
# 4. Protect units() through county -> province relationship
# ============================================================

$needle = @'
        if not county_fk:
            return []

        name = self.name_column(table)
'@

$replacement = @'
        if not county_fk:
            return []

        # Verify county belongs to Zanjan.
        county_table = self.county_table()

        if not county_table:
            return []

        county_province_fk = self.pick(
            county_table,
            "province_id"
        )

        if not county_province_fk:
            return []

        county_exists = self.scalar(
            f"""
            SELECT COUNT(*)
            FROM {self.ident(county_table)}
            WHERE id=:county_id
              AND {self.ident(county_province_fk)}
                  = :zanjan_province_id
            """,
            {
                "county_id": county_id,
                "zanjan_province_id": self.zanjan_id()
            },
            0
        )

        if int(county_exists) == 0:
            return []

        name = self.name_column(table)
'@

if ($content.Contains($needle)) {
    $content = $content.Replace($needle, $replacement)
    Write-Host "units(): non-Zanjan counties blocked." -ForegroundColor Green
}


# ============================================================
# 5. Protect unit_detail()
# ============================================================

$needle = @'
        if not table:
            return {
                "unit": None,
                "operations": []
            }

        name = self.name_column(table)
'@

$replacement = @'
        if not table:
            return {
                "unit": None,
                "operations": []
            }

        # HARD SCOPE: unit must belong to Zanjan.
        if not self.unit_belongs_to_zanjan(unit_id):
            return {
                "unit": None,
                "cards": {},
                "operations": [],
                "operation_count": 0,
                "scope": "zanjan"
            }

        name = self.name_column(table)
'@

# only replace first occurrence near unit_detail
$unitDetailPos = $content.IndexOf("    def unit_detail(self, unit_id: int):")

if ($unitDetailPos -ge 0) {

    $tail = $content.Substring($unitDetailPos)

    if ($tail.Contains($needle)) {
        $tail = $tail.Replace($needle, $replacement, 1)
        $content = $content.Substring(0, $unitDetailPos) + $tail
        Write-Host "unit_detail(): Zanjan-only." -ForegroundColor Green
    }
}


# ============================================================
# 6. Force overview() to Zanjan
# ============================================================

$overviewStart = $content.IndexOf("    def overview(self):")
$chartsStart   = $content.IndexOf("    # ---------------------------------------------------------`r`n    # Charts", $overviewStart)

if ($chartsStart -lt 0) {
    $chartsStart = $content.IndexOf("    # ---------------------------------------------------------`n    # Charts", $overviewStart)
}

if ($overviewStart -ge 0 -and $chartsStart -gt $overviewStart) {

    $overview = $content.Substring(
        $overviewStart,
        $chartsStart - $overviewStart
    )

    # total units
    $overview = $overview.Replace(
        'total_units = self.count(units) if units else 0',
        'total_units = self.scoped_count(units) if units else 0'
    )

    # active units
    $overview = $overview.Replace(
        'active_units = self.count(',
        'active_units = self.scoped_count('
    )

    # disease reports
    $overview = $overview.Replace(
        'disease_reports = self.count(report_table)',
        'disease_reports = self.scoped_count(report_table)'
    )

    # disease occurrences
    $overview = $overview.Replace(
        'disease_occurrences = self.count(',
        'disease_occurrences = self.scoped_count('
    )

    # care
    $overview = $overview.Replace(
        'self.count(care_table)',
        'self.scoped_count(care_table)'
    )

    # vaccination sum
    $overview = $overview.Replace(
        'vaccinated = self.sum_column(',
        'vaccinated = self.scoped_sum_column('
    )

    # laboratory
    $overview = $overview.Replace(
        'lab_results = self.count(lab_table)',
        'lab_results = self.scoped_count(lab_table)'
    )

    # samples
    $overview = $overview.Replace(
        'sample_records = self.count(sample_table)',
        'sample_records = self.scoped_count(sample_table)'
    )

    # inventory / distribution / disposal
    $overview = $overview.Replace(
        'inventory = self.sum_column(',
        'inventory = self.scoped_sum_column('
    )

    $overview = $overview.Replace(
        'distributed = self.sum_column(',
        'distributed = self.scoped_sum_column('
    )

    $overview = $overview.Replace(
        'disposed = self.sum_column(',
        'disposed = self.scoped_sum_column('
    )

    $content =
        $content.Substring(0, $overviewStart) +
        $overview +
        $content.Substring($chartsStart)

    Write-Host "overview(): Zanjan scoped." -ForegroundColor Green
}


# ============================================================
# 7. Scope charts
# ============================================================

function Add-ScopedChartWhere {
    param(
        [string]$Block
    )

    $Block = $Block.Replace(
        'WHERE {self.ident(d)} IS NOT NULL',
        @'
WHERE
                {self.ident(d)} IS NOT NULL
                AND
                EXISTS (
                    SELECT 1
                    FROM {self.ident(self.unit_table())} u
                    WHERE u.id IN (
                        SELECT p.{self.ident(self.pick(table, "epidemiology_unit_id"))}
                        FROM {self.ident(table)} p
                    )
                    AND u.{self.ident(self.pick(self.unit_table(), "province_id"))}
                        = :zanjan_province_id
                )
'@
    )

    return $Block
}

# Instead of attempting dangerous generic chart SQL replacement,
# inject a province guard directly before execution using unit IDs.
# This is handled below by replacing chart WHERE clauses individually.

$chartNames = @(
    "vaccination_chart",
    "disease_chart",
    "care_chart",
    "lab_chart"
)

foreach ($chartName in $chartNames) {

    $pos = $content.IndexOf("    def $chartName(")

    if ($pos -lt 0) {
        continue
    }

    $next = $content.IndexOf(
        "    def ",
        $pos + 10
    )

    if ($next -lt 0) {
        $next = $content.Length
    }

    $block = $content.Substring(
        $pos,
        $next - $pos
    )

    # Add params to rows() only if the chart already has
    # epidemiology_unit_id and a normal WHERE.
    if ($block -match "WHERE\s+\{self\.ident\(d\)\} IS NOT NULL") {

        $block = $block.Replace(
            'WHERE {self.ident(d)} IS NOT NULL',
            @'
WHERE
                {self.ident(d)} IS NOT NULL
                AND
                {self.ident(self.pick(table, "epidemiology_unit_id"))}
                IN (
                    SELECT id
                    FROM {self.ident(self.unit_table())}
                    WHERE
                        {self.ident(self.pick(self.unit_table(), "province_id"))}
                        = :zanjan_province_id
                )
'@
        )

        # Add params to rows(...) SQL call
        $block = $block.Replace(
            'ORDER BY 1',
            'ORDER BY 1'
        )

        $block = $block.Replace(
            '        )',
            '        , {"zanjan_province_id": self.zanjan_id()} )',
            1
        )

        $content =
            $content.Substring(0, $pos) +
            $block +
            $content.Substring($next)

        Write-Host "$chartName(): Zanjan scoped." -ForegroundColor Green
    }
}


# ============================================================
# 8. Write service
# ============================================================

Set-Content `
    -Path $SERVICE `
    -Value $content `
    -Encoding UTF8

Write-Host ""
Write-Host "SERVICE UPDATED:" -ForegroundColor Green
Write-Host $SERVICE


# ============================================================
# ROUTER
# ============================================================

$routerContent = Get-Content $ROUTER -Raw -Encoding UTF8

if ($routerContent -notmatch "ZANJAN_PROVINCE_ID") {

    $routerContent = $routerContent.Replace(
        'router = APIRouter(',
        @'
ZANJAN_PROVINCE_ID = 5

router = APIRouter(
'@
    )
}


# ------------------------------------------------------------
# Provinces endpoint: ignore arbitrary province
# ------------------------------------------------------------

$routerContent = $routerContent.Replace(
    'LiveDashboardKPIServiceV2(db)' + "`r`n" + '            .provinces(metric)',
    'LiveDashboardKPIServiceV2(db)' + "`r`n" + '            .provinces(metric)'
)


# ------------------------------------------------------------
# Counties endpoint: hard block
# ------------------------------------------------------------

if ($routerContent -notmatch "province_id != ZANJAN_PROVINCE_ID") {

    $routerContent = $routerContent.Replace(
        'def counties(',
        @'
def counties(
'@
    )

    $needle = @'
    return {
        "province_id": province_id,
'@

    $replacement = @'
    if province_id != ZANJAN_PROVINCE_ID:
        return {
            "province_id": province_id,
            "metric": metric,
            "items": []
        }

    return {
        "province_id": province_id,
'@

    if ($routerContent.Contains($needle)) {
        $routerContent = $routerContent.Replace(
            $needle,
            $replacement
        )
    }
}


Set-Content `
    -Path $ROUTER `
    -Value $routerContent `
    -Encoding UTF8

Write-Host "ROUTER UPDATED:" -ForegroundColor Green
Write-Host $ROUTER


# ============================================================
# PYTHON COMPILE
# ============================================================

Write-Host ""
Write-Host "===== PYTHON COMPILE =====" -ForegroundColor Cyan

Push-Location $ROOT

py -3.12 -m py_compile `
    .\app\services\gis\live_dashboard_kpi_service_v2.py `
    .\app\api\v1\endpoints\gis_dashboard_kpi_v2.py

if ($LASTEXITCODE -ne 0) {
    throw "Python compile FAILED."
}

Write-Host "Python compile: OK" -ForegroundColor Green


# ============================================================
# FINAL CHECK
# ============================================================

Write-Host ""
Write-Host "===== ZANJAN SCOPE MARKERS =====" -ForegroundColor Cyan

Select-String `
    -Path $SERVICE `
    -Pattern `
        "ZANJAN_PROVINCE_ID",
        "scoped_count",
        "scoped_sum_column",
        "unit_belongs_to_zanjan",
        "def provinces",
        "def counties",
        "def units",
        "def unit_detail" |
    Select-Object LineNumber, Line

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "ZANJAN KPI V2 REAL SCOPE FINISHED" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Province: Zanjan"
Write-Host "Province ID: 5"
Write-Host ""
Write-Host "Backup:"
Write-Host $BACKUP
Write-Host ""

Pop-Location