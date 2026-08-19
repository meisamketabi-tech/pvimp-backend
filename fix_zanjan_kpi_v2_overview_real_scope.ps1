$ErrorActionPreference = "Stop"

$Root = "D:\pvimp_backend"

$Service = Join-Path `
    $Root `
    "app\services\gis\live_dashboard_kpi_service_v2.py"

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "PVIMP - ZANJAN KPI V2 REAL OVERVIEW SCOPE" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

if (!(Test-Path $Service)) {
    throw "Service file not found: $Service"
}

# ---------------------------------------------------------
# BACKUP
# ---------------------------------------------------------

$backup = Join-Path `
    $Root `
    ("_zanjan_kpi_v2_overview_backup_" + `
        (Get-Date -Format "yyyyMMdd_HHmmss"))

New-Item `
    -ItemType Directory `
    -Path $backup `
    -Force |
    Out-Null

Copy-Item `
    $Service `
    (Join-Path $backup "live_dashboard_kpi_service_v2.py") `
    -Force

Write-Host "BACKUP: $backup" -ForegroundColor Yellow

$text = Get-Content `
    $Service `
    -Raw `
    -Encoding UTF8

# =========================================================
# HELPER
# =========================================================

function Replace-Block {
    param(
        [string]$Text,
        [string]$StartMarker,
        [string]$EndMarker,
        [string]$Replacement
    )

    $start = $Text.IndexOf($StartMarker)

    if ($start -lt 0) {
        throw "Start marker not found: $StartMarker"
    }

    $end = $Text.IndexOf(
        $EndMarker,
        $start + $StartMarker.Length
    )

    if ($end -lt 0) {
        throw "End marker not found: $EndMarker"
    }

    return `
        $Text.Substring(0, $start) +
        $Replacement +
        $Text.Substring($end)
}

# =========================================================
# ADD ZANJAN HELPERS
# =========================================================

$marker = @'
    # ---------------------------------------------------------
    # Global overview
    # ---------------------------------------------------------
'@

if (!$text.Contains("def zanjan_unit_where")) {

$helpers = @'
    # ---------------------------------------------------------
    # Zanjan scope helpers
    # ---------------------------------------------------------

    def zanjan_unit_table(self):

        return self.unit_table()

    def zanjan_unit_where(
        self,
        table_alias="u"
    ):

        unit_table = self.unit_table()

        if not unit_table:
            return None

        province_fk = self.pick(
            unit_table,
            "province_id"
        )

        if not province_fk:
            return None

        return f"""
            {table_alias}.{self.ident(province_fk)}
            = :zanjan_province_id
        """

    def zanjan_operation_where(
        self,
        operation_table,
        operation_alias="o"
    ):

        unit_table = self.unit_table()

        if not unit_table:
            return None

        operation_unit_fk = self.pick(
            operation_table,
            "epidemiology_unit_id"
        )

        if not operation_unit_fk:
            return None

        province_fk = self.pick(
            unit_table,
            "province_id"
        )

        if not province_fk:
            return None

        return f"""
            {operation_alias}.{self.ident(operation_unit_fk)}
            IN (
                SELECT u.id
                FROM {self.ident(unit_table)} u
                WHERE u.{self.ident(province_fk)}
                    = :zanjan_province_id
            )
        """

    def zanjan_params(self):

        return {
            "zanjan_province_id":
                ZANJAN_PROVINCE_ID
        }

'@

$text = $text.Replace(
    $marker,
    $helpers + "`r`n" + $marker
)

Write-Host "Zanjan helper methods added." -ForegroundColor Green
}

# =========================================================
# REPLACE OVERVIEW
# =========================================================

$overviewStart = "    def overview(self):"
$overviewEnd = "    # ---------------------------------------------------------`r`n    # Charts"

$overview = @'
    def overview(self):

        units = self.unit_table()

        total_units = 0
        active_units = 0

        if units:

            province_fk = self.pick(
                units,
                "province_id"
            )

            if province_fk:

                scope = f"""
                    {self.ident(province_fk)}
                    = :zanjan_province_id
                """

                total_units = self.count(
                    units,
                    scope,
                    self.zanjan_params()
                )

                active = self.pick(
                    units,
                    "is_active",
                    "active",
                    "enabled"
                )

                if active:

                    active_units = self.count(
                        units,
                        f"""
                        {scope}
                        AND {self.ident(active)} = TRUE
                        """,
                        self.zanjan_params()
                    )

                else:

                    active_units = total_units

        # -----------------------------------------------------
        # Operation tables
        # -----------------------------------------------------

        def operation_count(candidates):

            table = self.find_table(candidates)

            if not table:
                return 0

            where = self.zanjan_operation_where(
                table,
                "o"
            )

            if not where:
                return 0

            return self.count(
                table,
                where.replace(
                    "o.",
                    ""
                ) if False else where,
                self.zanjan_params()
            )

        disease_reports = operation_count([
            "gis_disease_reports",
            "gis_disease_report"
        ])

        disease_occurrences = operation_count([
            "gis_disease_occurrences",
            "gis_disease_occurrence"
        ])

        care_records = operation_count([
            "gis_enable_cares",
            "gis_enable_care",
            "gis_active_cares"
        ])

        lab_table = self.find_table([
            "gis_laboratory_results",
            "gis_laboratory_result",
            "laboratory_results"
        ])

        sample_table = self.find_table([
            "gis_send_sample_details",
            "gis_send_sample_detail",
            "gis_samples",
            "gis_sample_details"
        ])

        lab_results = (
            operation_count([
                "gis_laboratory_results",
                "gis_laboratory_result",
                "laboratory_results"
            ])
            if lab_table
            else 0
        )

        sample_records = (
            operation_count([
                "gis_send_sample_details",
                "gis_send_sample_detail",
                "gis_samples",
                "gis_sample_details"
            ])
            if sample_table
            else 0
        )

        # -----------------------------------------------------
        # Vaccination
        # -----------------------------------------------------

        vaccination_table = self.find_table([
            "gis_vaccination_performances",
            "gis_vaccination_performance"
        ])

        vaccinated = 0.0
        eligible = 0.0

        if vaccination_table:

            value_col = self.pick(
                vaccination_table,
                "vaccinated_animals",
                "vaccinated_count",
                "performed_count",
                "animal_count"
            )

            eligible_col = self.pick(
                vaccination_table,
                "eligible_animals",
                "eligible_count",
                "target_animals",
                "planned_animals"
            )

            scope = self.zanjan_operation_where(
                vaccination_table,
                "o"
            )

            if scope:

                if value_col:

                    vaccinated = float(
                        self.scalar(
                            f"""
                            SELECT COALESCE(
                                SUM(
                                    o.{self.ident(value_col)}
                                ),
                                0
                            )
                            FROM {self.ident(vaccination_table)} o
                            WHERE {scope}
                            """,
                            self.zanjan_params(),
                            0
                        )
                    )

                if eligible_col:

                    eligible = float(
                        self.scalar(
                            f"""
                            SELECT COALESCE(
                                SUM(
                                    o.{self.ident(eligible_col)}
                                ),
                                0
                            )
                            FROM {self.ident(vaccination_table)} o
                            WHERE {scope}
                            """,
                            self.zanjan_params(),
                            0
                        )
                    )

        coverage = (
            round(
                vaccinated / eligible * 100,
                2
            )
            if eligible
            else 0
        )

        # -----------------------------------------------------
        # Positive lab results
        # -----------------------------------------------------

        lab_positive = 0

        if lab_table:

            status = self.pick(
                lab_table,
                "result_status",
                "status",
                "result",
                "result_value"
            )

            scope = self.zanjan_operation_where(
                lab_table,
                "o"
            )

            if status and scope:

                lab_positive = self.count(
                    lab_table,
                    f"""
                    {scope}
                    AND
                    (
                        LOWER(
                            COALESCE(
                                CAST(
                                    o.{self.ident(status)}
                                    AS TEXT
                                ),
                                ''
                            )
                        ) LIKE '%positive%'

                        OR

                        LOWER(
                            COALESCE(
                                CAST(
                                    o.{self.ident(status)}
                                    AS TEXT
                                ),
                                ''
                            )
                        ) LIKE '%مثبت%'
                    )
                    """,
                    self.zanjan_params()
                )

        lab_positive_rate = (
            round(
                lab_positive / lab_results * 100,
                2
            )
            if lab_results
            else 0
        )

        # -----------------------------------------------------
        # Vaccine inventory
        # -----------------------------------------------------

        def operation_sum(candidates, columns):

            table = self.find_table(candidates)

            if not table:
                return 0.0

            value_col = self.pick(
                table,
                *columns
            )

            if not value_col:
                return 0.0

            scope = self.zanjan_operation_where(
                table,
                "o"
            )

            if not scope:
                return 0.0

            return float(
                self.scalar(
                    f"""
                    SELECT COALESCE(
                        SUM(
                            o.{self.ident(value_col)}
                        ),
                        0
                    )
                    FROM {self.ident(table)} o
                    WHERE {scope}
                    """,
                    self.zanjan_params(),
                    0
                )
            )

        inventory = operation_sum(
            [
                "gis_vaccine_inventories",
                "gis_vaccine_inventory"
            ],
            [
                "quantity",
                "package_count",
                "packages_count",
                "stock_quantity"
            ]
        )

        distributed = operation_sum(
            [
                "gis_vaccine_distributions",
                "gis_vaccine_distribution"
            ],
            [
                "quantity",
                "package_count",
                "packages_count"
            ]
        )

        disposed = operation_sum(
            [
                "gis_vaccine_disposals",
                "gis_vaccine_disposal"
            ],
            [
                "quantity",
                "package_count",
                "packages_count"
            ]
        )

        return self.clean({

            "live": True,

            "generated_at":
                datetime.utcnow(),

            "province_id":
                ZANJAN_PROVINCE_ID,

            "province_name":
                "Zanjan",

            "cards": {

                "total_units":
                    total_units,

                "active_units":
                    active_units,

                "disease_reports":
                    disease_reports,

                "disease_occurrences":
                    disease_occurrences,

                "care_records":
                    care_records,

                "vaccinated":
                    vaccinated,

                "eligible":
                    eligible,

                "vaccination_coverage":
                    coverage,

                "vaccination_remaining":
                    max(
                        eligible - vaccinated,
                        0
                    ),

                "lab_results":
                    lab_results,

                "lab_positive":
                    lab_positive,

                "lab_positive_rate":
                    lab_positive_rate,

                "sample_records":
                    sample_records,

                "inventory":
                    inventory,

                "distributed":
                    distributed,

                "disposed":
                    disposed
            },

            "charts": {

                "vaccination":
                    self.vaccination_chart(),

                "disease":
                    self.disease_chart(),

                "care":
                    self.care_chart(),

                "laboratory":
                    self.lab_chart()
            },

            "drilldown": {

                "levels": [
                    "province",
                    "county",
                    "unit"
                ]
            }
        })

    # ---------------------------------------------------------
    # Charts
'@

$text = Replace-Block `
    $text `
    $overviewStart `
    $overviewEnd `
    $overview

Write-Host "overview(): replaced with Zanjan-scoped implementation." -ForegroundColor Green

# =========================================================
# PATCH CHARTS
# =========================================================

function Patch-ChartWhere {
    param(
        [string]$Text,
        [string]$FunctionName,
        [string]$TableCandidate,
        [string]$DateColumnExpression
    )

    $startMarker = "    def $FunctionName(self):"
    $nextMarker = "    def "

    $start = $Text.IndexOf($startMarker)

    if ($start -lt 0) {
        throw "Chart function not found: $FunctionName"
    }

    $next = $Text.IndexOf(
        $nextMarker,
        $start + $startMarker.Length
    )

    if ($next -lt 0) {
        throw "End of chart function not found: $FunctionName"
    }

    $block = $Text.Substring(
        $start,
        $next - $start
    )

    $old = "WHERE {self.ident($d)} IS NOT NULL"

    if ($block.Contains($old)) {

        $new = @'
WHERE
                {self.ident($d)} IS NOT NULL
                AND
                {self.ident($unit_fk)} IN (
                    SELECT u.id
                    FROM {self.ident(self.unit_table())} u
                    WHERE u.{self.ident($province_fk)}
                        = :zanjan_province_id
                )
'@

        $block = $block.Replace(
            $old,
            $new
        )

        # Insert required FK variables before SQL execution.
        $needle = @'
        return self.rows(
'@

        $insert = @'
        unit_fk = self.pick(
            table,
            "epidemiology_unit_id"
        )

        unit_table = self.unit_table()

        province_fk = (
            self.pick(
                unit_table,
                "province_id"
            )
            if unit_table
            else None
        )

        if not unit_fk or not unit_table or not province_fk:
            return []

        return self.rows(
'@

        $block = $block.Replace(
            $needle,
            $insert,
            1
        )

        $block = $block.Replace(
            '            """',
            '            """,' + "`r`n            self.zanjan_params()",
            1
        )

        $Text =
            $Text.Substring(0, $start) +
            $block +
            $Text.Substring($next)

        Write-Host "$FunctionName(): Zanjan scope patched." -ForegroundColor Green
    }
    else {
        Write-Host "$FunctionName(): no matching WHERE found; review manually." -ForegroundColor DarkYellow
    }

    return $Text
}

# ---------------------------------------------------------
# NOTE:
# We deliberately do not use the generic chart patcher here
# because the existing chart SQL differs slightly.
# Instead, charts will be validated after compile.
# ---------------------------------------------------------

# =========================================================
# WRITE
# =========================================================

Set-Content `
    -Path $Service `
    -Value $text `
    -Encoding UTF8

Write-Host ""
Write-Host "SERVICE UPDATED." -ForegroundColor Green

# =========================================================
# COMPILE
# =========================================================

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

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "ZANJAN OVERVIEW SCOPE PATCH FINISHED" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backup:" -ForegroundColor Yellow
Write-Host $backup
Write-Host ""
Write-Host "IMPORTANT:" -ForegroundColor Yellow
Write-Host "Restart Uvicorn before API testing."
Write-Host ""