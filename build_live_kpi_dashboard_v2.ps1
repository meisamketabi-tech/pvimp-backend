#requires -Version 5.1
<#
PVIMP - LIVE KPI DRILL-DOWN DASHBOARD V2
========================================

Architecture:
    ONE PAGE
       |
       +-- All KPIs visible
       +-- All charts visible
       |
       +-- click KPI/chart
              |
              +-- Province
                    |
                    +-- County
                          |
                          +-- Epidemiology Unit
                                |
                                +-- Unit KPIs
                                +-- Related operation timeline
                                +-- Detailed linked events

NO TAB MENU.
NO KPI CACHE.
NO FAKE DATA.
NO DELETE.
LIVE PostgreSQL reads.

The service dynamically inspects PostgreSQL information_schema and foreign keys.
It avoids assuming that every project table has exactly the same column names.

Target:
    D:\pvimp_backend
    D:\pvimp_backend\pvimp_frontend
#>

$ErrorActionPreference = "Stop"

$BackendRoot  = "D:\pvimp_backend"
$FrontendRoot = Join-Path $BackendRoot "pvimp_frontend"

$ApiDir       = Join-Path $BackendRoot "app\api\v1\endpoints"
$ServiceDir   = Join-Path $BackendRoot "app\services\gis"
$PageDir      = Join-Path $FrontendRoot "src\pages"

$BackupRoot = Join-Path $BackendRoot "_dashboard_kpi_v2_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"

if (-not (Test-Path $BackendRoot)) {
    throw "Backend path not found: $BackendRoot"
}

if (-not (Test-Path $FrontendRoot)) {
    throw "Frontend path not found: $FrontendRoot"
}

New-Item -ItemType Directory -Force -Path `
    $ApiDir,$ServiceDir,$PageDir,$BackupRoot | Out-Null


function Backup-IfExists([string]$Path) {

    if (Test-Path $Path) {

        $relative = $Path.Substring($BackendRoot.Length).TrimStart('\')
        $dest = Join-Path $BackupRoot $relative
        $destDir = Split-Path $dest -Parent

        New-Item -ItemType Directory -Force -Path $destDir | Out-Null

        Copy-Item $Path $dest -Force

        Write-Host "BACKUP: $Path" -ForegroundColor DarkGray
    }
}


function Write-Utf8([string]$Path,[string]$Content) {

    $dir = Split-Path $Path -Parent

    New-Item -ItemType Directory -Force -Path $dir | Out-Null

    [System.IO.File]::WriteAllText(
        $Path,
        $Content,
        (New-Object System.Text.UTF8Encoding($false))
    )

    Write-Host "WROTE : $Path" -ForegroundColor Green
}


$ServiceFile = Join-Path $ServiceDir "live_dashboard_kpi_service_v2.py"
$RouterFile  = Join-Path $ApiDir "gis_dashboard_kpi_v2.py"
$PageFile    = Join-Path $PageDir "LiveKpiDashboardV2.tsx"
$CssFile     = Join-Path $PageDir "LiveKpiDashboardV2.css"


Backup-IfExists $ServiceFile
Backup-IfExists $RouterFile
Backup-IfExists $PageFile
Backup-IfExists $CssFile


# ============================================================
# BACKEND SERVICE
# ============================================================

$service = @'
from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session


class LiveDashboardKPIServiceV2:
    """
    PVIMP Live KPI Dashboard V2.

    Important:
    - Reads PostgreSQL live.
    - No snapshot.
    - No KPI cache.
    - No fake rows.
    - Uses information_schema and FK metadata.
    """

    def __init__(self, db: Session):
        self.db = db
        self._tables_cache: set[str] | None = None
        self._columns_cache: dict[str, set[str]] = {}
        self._fk_cache: list[dict[str, Any]] | None = None

    # ---------------------------------------------------------
    # Generic helpers
    # ---------------------------------------------------------

    @staticmethod
    def ident(value: str) -> str:
        if not value:
            raise ValueError("Empty identifier")

        if not value.replace("_", "").isalnum():
            raise ValueError(f"Unsafe identifier: {value}")

        return '"' + value + '"'

    def tables(self) -> set[str]:

        if self._tables_cache is None:

            rows = self.db.execute(
                text("""
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                      AND table_type = 'BASE TABLE'
                """)
            ).mappings().all()

            self._tables_cache = {
                str(r["table_name"])
                for r in rows
            }

        return self._tables_cache

    def has_table(self, table: str) -> bool:
        return table in self.tables()

    def cols(self, table: str) -> set[str]:

        if table in self._columns_cache:
            return self._columns_cache[table]

        if not self.has_table(table):
            return set()

        rows = self.db.execute(
            text("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_schema='public'
                  AND table_name=:table
            """),
            {"table": table}
        ).mappings().all()

        result = {
            str(r["column_name"])
            for r in rows
        }

        self._columns_cache[table] = result

        return result

    def pick(self, table: str, *candidates: str) -> str | None:

        available = self.cols(table)

        for candidate in candidates:
            if candidate in available:
                return candidate

        return None

    def scalar(
        self,
        sql: str,
        params: dict[str, Any] | None = None,
        default=0
    ):

        value = self.db.execute(
            text(sql),
            params or {}
        ).scalar()

        if value is None:
            return default

        if isinstance(value, Decimal):
            return float(value)

        return value

    def rows(
        self,
        sql: str,
        params: dict[str, Any] | None = None
    ):

        result = self.db.execute(
            text(sql),
            params or {}
        ).mappings().all()

        return [dict(r) for r in result]

    def clean(self, value):

        if isinstance(value, dict):
            return {
                k: self.clean(v)
                for k, v in value.items()
            }

        if isinstance(value, list):
            return [
                self.clean(v)
                for v in value
            ]

        if isinstance(value, (datetime, date)):
            return value.isoformat()

        if isinstance(value, Decimal):
            return float(value)

        return value

    def count(self, table: str, where="TRUE", params=None):

        if not self.has_table(table):
            return 0

        return int(
            self.scalar(
                f"""
                SELECT COUNT(*)
                FROM {self.ident(table)}
                WHERE {where}
                """,
                params,
                0
            )
        )

    def sum_column(
        self,
        table: str,
        column: str | None,
        where="TRUE",
        params=None
    ):

        if not column:
            return 0.0

        if not self.has_table(table):
            return 0.0

        if column not in self.cols(table):
            return 0.0

        return float(
            self.scalar(
                f"""
                SELECT COALESCE(
                    SUM({self.ident(column)}),
                    0
                )
                FROM {self.ident(table)}
                WHERE {where}
                """,
                params,
                0
            )
        )

    # ---------------------------------------------------------
    # FK discovery
    # ---------------------------------------------------------

    def foreign_keys(self):

        if self._fk_cache is not None:
            return self._fk_cache

        rows = self.rows("""
            SELECT
                tc.table_name AS source_table,
                kcu.column_name AS source_column,
                ccu.table_name AS target_table,
                ccu.column_name AS target_column
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
              ON tc.constraint_name = kcu.constraint_name
             AND tc.table_schema = kcu.table_schema
            JOIN information_schema.constraint_column_usage ccu
              ON ccu.constraint_name = tc.constraint_name
             AND ccu.table_schema = tc.table_schema
            WHERE tc.constraint_type='FOREIGN KEY'
              AND tc.table_schema='public'
            ORDER BY tc.table_name, kcu.column_name
        """)

        self._fk_cache = rows

        return rows

    def table_fks(self, table: str):

        return [
            x for x in self.foreign_keys()
            if x["source_table"] == table
        ]

    # ---------------------------------------------------------
    # Entity discovery
    # ---------------------------------------------------------

    def find_table(self, candidates):

        available = self.tables()

        for name in candidates:
            if name in available:
                return name

        return None

    def province_table(self):

        return self.find_table([
            "gis_provinces",
            "provinces",
            "province"
        ])

    def county_table(self):

        return self.find_table([
            "gis_counties",
            "counties",
            "county"
        ])

    def unit_table(self):

        return self.find_table([
            "gis_epidemiology_units",
            "gis_epidemiological_units",
            "epidemiology_units"
        ])

    def disease_table(self):

        return self.find_table([
            "gis_diseases",
            "diseases",
            "disease"
        ])

    # ---------------------------------------------------------
    # Names
    # ---------------------------------------------------------

    def name_column(self, table: str):

        return self.pick(
            table,
            "name_fa",
            "name",
            "title",
            "label",
            "unit_name",
            "unit_title",
            "province_name",
            "county_name",
            "disease_name"
        )

    # ---------------------------------------------------------
    # Global overview
    # ---------------------------------------------------------

    def overview(self):

        units = self.unit_table()

        total_units = self.count(units) if units else 0

        active_units = 0

        if units:

            active = self.pick(
                units,
                "is_active",
                "active",
                "enabled"
            )

            if active:
                active_units = self.count(
                    units,
                    f"{self.ident(active)} = TRUE"
                )
            else:
                active_units = total_units

        disease_reports = 0

        report_table = self.find_table([
            "gis_disease_reports",
            "gis_disease_report"
        ])

        if report_table:
            disease_reports = self.count(report_table)

        disease_occurrences = 0

        occurrence_table = self.find_table([
            "gis_disease_occurrences",
            "gis_disease_occurrence"
        ])

        if occurrence_table:
            disease_occurrences = self.count(
                occurrence_table
            )

        care_table = self.find_table([
            "gis_enable_cares",
            "gis_enable_care",
            "gis_active_cares"
        ])

        care_records = (
            self.count(care_table)
            if care_table
            else 0
        )

        vaccination_table = self.find_table([
            "gis_vaccination_performances",
            "gis_vaccination_performance"
        ])

        vaccinated_column = None
        eligible_column = None

        vaccinated = 0.0
        eligible = 0.0

        if vaccination_table:

            vaccinated_column = self.pick(
                vaccination_table,
                "vaccinated_animals",
                "vaccinated_count",
                "performed_count",
                "animal_count"
            )

            eligible_column = self.pick(
                vaccination_table,
                "eligible_animals",
                "eligible_count",
                "target_animals",
                "planned_animals"
            )

            vaccinated = self.sum_column(
                vaccination_table,
                vaccinated_column
            )

            eligible = self.sum_column(
                vaccination_table,
                eligible_column
            )

        coverage = (
            round(
                vaccinated / eligible * 100,
                2
            )
            if eligible
            else 0
        )

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
            self.count(lab_table)
            if lab_table
            else 0
        )

        sample_records = (
            self.count(sample_table)
            if sample_table
            else 0
        )

        lab_positive = 0

        if lab_table:

            status = self.pick(
                lab_table,
                "result_status",
                "status",
                "result",
                "result_value"
            )

            if status:

                lab_positive = self.count(
                    lab_table,
                    f"""
                    (
                        LOWER(
                            COALESCE(
                                CAST(
                                    {self.ident(status)}
                                    AS TEXT
                                ),
                                ''
                            )
                        ) LIKE '%positive%'
                        OR
                        LOWER(
                            COALESCE(
                                CAST(
                                    {self.ident(status)}
                                    AS TEXT
                                ),
                                ''
                            )
                        ) LIKE '%مثبت%'
                    )
                    """
                )

        lab_positive_rate = (
            round(
                lab_positive / lab_results * 100,
                2
            )
            if lab_results
            else 0
        )

        inventory_table = self.find_table([
            "gis_vaccine_inventories",
            "gis_vaccine_inventory"
        ])

        distribution_table = self.find_table([
            "gis_vaccine_distributions",
            "gis_vaccine_distribution"
        ])

        disposal_table = self.find_table([
            "gis_vaccine_disposals",
            "gis_vaccine_disposal"
        ])

        inventory = self.sum_column(
            inventory_table,
            self.pick(
                inventory_table,
                "quantity",
                "package_count",
                "packages_count",
                "stock_quantity"
            )
        ) if inventory_table else 0

        distributed = self.sum_column(
            distribution_table,
            self.pick(
                distribution_table,
                "quantity",
                "package_count",
                "packages_count"
            )
        ) if distribution_table else 0

        disposed = self.sum_column(
            disposal_table,
            self.pick(
                disposal_table,
                "quantity",
                "package_count",
                "packages_count"
            )
        ) if disposal_table else 0

        return self.clean({

            "live": True,

            "generated_at": datetime.utcnow(),

            "cards": {

                "total_units": total_units,

                "active_units": active_units,

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
                    disposed,
            },

            "charts": {

                "vaccination": self.vaccination_chart(),

                "disease": self.disease_chart(),

                "care": self.care_chart(),

                "laboratory": self.lab_chart(),

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
    # ---------------------------------------------------------

    def vaccination_chart(self):

        table = self.find_table([
            "gis_vaccination_performances",
            "gis_vaccination_performance"
        ])

        if not table:
            return []

        value = self.pick(
            table,
            "vaccinated_animals",
            "vaccinated_count",
            "performed_count",
            "animal_count"
        )

        d = self.pick(
            table,
            "vaccination_date",
            "operation_date",
            "date",
            "created_at"
        )

        if not value or not d:
            return []

        return self.rows(
            f"""
            SELECT
                TO_CHAR(
                    DATE_TRUNC(
                        'month',
                        {self.ident(d)}
                    ),
                    'YYYY-MM'
                ) AS period,

                COALESCE(
                    SUM({self.ident(value)}),
                    0
                )::numeric AS value

            FROM {self.ident(table)}

            WHERE {self.ident(d)} IS NOT NULL

            GROUP BY 1
            ORDER BY 1
            """
        )

    def disease_chart(self):

        table = self.find_table([
            "gis_disease_reports",
            "gis_disease_report"
        ])

        if not table:
            return []

        d = self.pick(
            table,
            "report_date",
            "occurrence_date",
            "date",
            "created_at"
        )

        if not d:
            return []

        return self.rows(
            f"""
            SELECT
                TO_CHAR(
                    DATE_TRUNC(
                        'month',
                        {self.ident(d)}
                    ),
                    'YYYY-MM'
                ) AS period,

                COUNT(*)::numeric AS value

            FROM {self.ident(table)}

            WHERE {self.ident(d)} IS NOT NULL

            GROUP BY 1
            ORDER BY 1
            """
        )

    def care_chart(self):

        table = self.find_table([
            "gis_enable_cares",
            "gis_enable_care",
            "gis_active_cares"
        ])

        if not table:
            return []

        d = self.pick(
            table,
            "care_date",
            "operation_date",
            "date",
            "created_at"
        )

        if not d:
            return []

        return self.rows(
            f"""
            SELECT
                TO_CHAR(
                    DATE_TRUNC(
                        'month',
                        {self.ident(d)}
                    ),
                    'YYYY-MM'
                ) AS period,

                COUNT(*)::numeric AS value

            FROM {self.ident(table)}

            WHERE {self.ident(d)} IS NOT NULL

            GROUP BY 1
            ORDER BY 1
            """
        )

    def lab_chart(self):

        table = self.find_table([
            "gis_laboratory_results",
            "gis_laboratory_result",
            "laboratory_results"
        ])

        if not table:
            return []

        d = self.pick(
            table,
            "sampling_date",
            "result_date",
            "answer_date",
            "date",
            "created_at"
        )

        if not d:
            return []

        return self.rows(
            f"""
            SELECT
                TO_CHAR(
                    DATE_TRUNC(
                        'month',
                        {self.ident(d)}
                    ),
                    'YYYY-MM'
                ) AS period,

                COUNT(*)::numeric AS value

            FROM {self.ident(table)}

            WHERE {self.ident(d)} IS NOT NULL

            GROUP BY 1
            ORDER BY 1
            """
        )

    # ---------------------------------------------------------
    # Provinces
    # ---------------------------------------------------------

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
            ORDER BY {self.ident(name)}
            """
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

                "name":
                    row["name"] or
                    f"استان {pid}",

                "value":
                    value

            })

        return self.clean(result)

    # ---------------------------------------------------------
    # Counties
    # ---------------------------------------------------------

    def counties(
        self,
        province_id: int,
        metric="all"
    ):

        table = self.county_table()

        if not table:
            return []

        province_fk = self.pick(
            table,
            "province_id"
        )

        if not province_fk:
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
            WHERE {self.ident(province_fk)}=:pid
            ORDER BY {self.ident(name)}
            """,
            {"pid": province_id}
        )

        result = []

        for row in rows:

            cid = row["id"]

            value = self.location_metric(
                "county",
                cid,
                metric
            )

            result.append({

                "id": cid,

                "name":
                    row["name"] or
                    f"شهرستان {cid}",

                "value":
                    value

            })

        return self.clean(result)

    # ---------------------------------------------------------
    # Units
    # ---------------------------------------------------------

    def units(
        self,
        county_id: int,
        metric="all"
    ):

        table = self.unit_table()

        if not table:
            return []

        county_fk = self.pick(
            table,
            "county_id"
        )

        if not county_fk:
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
            WHERE {self.ident(county_fk)}=:cid
            ORDER BY {self.ident(name)}
            """,
            {"cid": county_id}
        )

        result = []

        for row in rows:

            uid = row["id"]

            value = self.unit_metric(
                uid,
                metric
            )

            result.append({

                "id": uid,

                "name":
                    row["name"] or
                    f"واحد {uid}",

                "value":
                    value

            })

        return self.clean(result)

    # ---------------------------------------------------------
    # Metric calculation
    # ---------------------------------------------------------

    def location_metric(
        self,
        level,
        location_id,
        metric
    ):

        table = self.unit_table()

        if not table:
            return 0

        fk = (
            self.pick(table, "province_id")
            if level == "province"
            else
            self.pick(table, "county_id")
        )

        if not fk:
            return 0

        if metric == "units":
            return self.count(
                table,
                f"{self.ident(fk)}=:id",
                {"id": location_id}
            )

        if metric == "vaccination":

            vp = self.find_table([
                "gis_vaccination_performances",
                "gis_vaccination_performance"
            ])

            if not vp:
                return 0

            unit_fk = self.pick(
                vp,
                "epidemiology_unit_id"
            )

            value = self.pick(
                vp,
                "vaccinated_animals",
                "vaccinated_count",
                "performed_count",
                "animal_count"
            )

            if not unit_fk or not value:
                return 0

            return float(
                self.scalar(
                    f"""
                    SELECT COALESCE(
                        SUM(p.{self.ident(value)}),
                        0
                    )

                    FROM {self.ident(vp)} p

                    JOIN {self.ident(table)} u
                      ON u.id=p.{self.ident(unit_fk)}

                    WHERE
                        u.{self.ident(fk)}=:id
                    """,
                    {"id": location_id},
                    0
                )
            )

        source_map = {

            "disease":
                [
                    "gis_disease_reports",
                    "gis_disease_report"
                ],

            "care":
                [
                    "gis_enable_cares",
                    "gis_enable_care",
                    "gis_active_cares"
                ],

            "lab":
                [
                    "gis_laboratory_results",
                    "gis_laboratory_result"
                ],

            "samples":
                [
                    "gis_send_sample_details",
                    "gis_send_sample_detail",
                    "gis_samples"
                ],

            "all":
                []

        }

        sources = source_map.get(metric, [])

        source = self.find_table(sources)

        if source:

            source_fk = self.pick(
                source,
                "epidemiology_unit_id"
            )

            if source_fk:

                return self.count(
                    source,
                    f"""
                    {self.ident(source_fk)}
                    IN (
                        SELECT id
                        FROM {self.ident(table)}
                        WHERE {self.ident(fk)}=:id
                    )
                    """,
                    {"id": location_id}
                )

        if metric == "all":

            total = 0

            for candidate in [

                "gis_disease_reports",
                "gis_enable_cares",
                "gis_vaccination_performances",
                "gis_laboratory_results",
                "gis_send_sample_details",
                "gis_slaughter_disposals",
                "gis_spraying",
                "gis_vaccine_distributions",
                "gis_vaccine_disposals",
                "gis_disease_occurrences"

            ]:

                if not self.has_table(candidate):
                    continue

                fk2 = self.pick(
                    candidate,
                    "epidemiology_unit_id"
                )

                if not fk2:
                    continue

                total += self.count(
                    candidate,
                    f"""
                    {self.ident(fk2)}
                    IN (
                        SELECT id
                        FROM {self.ident(table)}
                        WHERE {self.ident(fk)}=:id
                    )
                    """,
                    {"id": location_id}
                )

            return total

        return 0

    def unit_metric(
        self,
        unit_id,
        metric
    ):

        sources = {

            "disease":
                [
                    "gis_disease_reports",
                    "gis_disease_report"
                ],

            "care":
                [
                    "gis_enable_cares",
                    "gis_enable_care",
                    "gis_active_cares"
                ],

            "vaccination":
                [
                    "gis_vaccination_performances",
                    "gis_vaccination_performance"
                ],

            "lab":
                [
                    "gis_laboratory_results",
                    "gis_laboratory_result"
                ],

            "samples":
                [
                    "gis_send_sample_details",
                    "gis_send_sample_detail",
                    "gis_samples"
                ],

            "spraying":
                [
                    "gis_spraying"
                ],

            "slaughter":
                [
                    "gis_slaughter_disposals"
                ],

            "all":
                []

        }

        if metric == "all":

            total = 0

            for table in [
                "gis_disease_reports",
                "gis_enable_cares",
                "gis_vaccination_performances",
                "gis_laboratory_results",
                "gis_send_sample_details",
                "gis_slaughter_disposals",
                "gis_spraying",
                "gis_vaccine_distributions",
                "gis_vaccine_disposals",
                "gis_disease_occurrences"
            ]:

                if not self.has_table(table):
                    continue

                fk = self.pick(
                    table,
                    "epidemiology_unit_id"
                )

                if fk:

                    total += self.count(
                        table,
                        f"{self.ident(fk)}=:uid",
                        {"uid": unit_id}
                    )

            return total

        table = self.find_table(
            sources.get(metric, [])
        )

        if not table:
            return 0

        fk = self.pick(
            table,
            "epidemiology_unit_id"
        )

        if not fk:
            return 0

        return self.count(
            table,
            f"{self.ident(fk)}=:uid",
            {"uid": unit_id}
        )

    # ---------------------------------------------------------
    # Unit detail
    # ---------------------------------------------------------

    def unit_detail(self, unit_id: int):

        table = self.unit_table()

        if not table:
            return {
                "unit": None,
                "operations": []
            }

        name = self.name_column(table)

        if not name:
            name = "id"

        rows = self.rows(
            f"""
            SELECT
                id,
                {self.ident(name)} AS name
            FROM {self.ident(table)}
            WHERE id=:uid
            """,
            {"uid": unit_id}
        )

        if not rows:
            return {
                "unit": None,
                "operations": []
            }

        unit = rows[0]

        cards = {

            "all":
                self.unit_metric(unit_id, "all"),

            "disease":
                self.unit_metric(unit_id, "disease"),

            "care":
                self.unit_metric(unit_id, "care"),

            "vaccination":
                self.unit_metric(unit_id, "vaccination"),

            "lab":
                self.unit_metric(unit_id, "lab"),

            "samples":
                self.unit_metric(unit_id, "samples"),

            "spraying":
                self.unit_metric(unit_id, "spraying"),

            "slaughter":
                self.unit_metric(unit_id, "slaughter"),

        }

        operations = self.operation_timeline(
            unit_id
        )

        return self.clean({

            "unit": unit,

            "cards": cards,

            "operations": operations,

            "operation_count":
                len(operations)

        })

    # ---------------------------------------------------------
    # Operation timeline
    # ---------------------------------------------------------

    def operation_timeline(self, unit_id: int):

        specs = [

            (
                "gis_vaccination_performances",
                "واکسیناسیون",
                [
                    "vaccination_date",
                    "operation_date",
                    "date",
                    "created_at"
                ]
            ),

            (
                "gis_disease_reports",
                "گزارش بیماری",
                [
                    "report_date",
                    "occurrence_date",
                    "date",
                    "created_at"
                ]
            ),

            (
                "gis_disease_occurrences",
                "وقوع بیماری",
                [
                    "occurrence_date",
                    "event_date",
                    "date",
                    "created_at"
                ]
            ),

            (
                "gis_enable_cares",
                "مراقبت فعال",
                [
                    "care_date",
                    "operation_date",
                    "date",
                    "created_at"
                ]
            ),

            (
                "gis_send_sample_details",
                "ارسال نمونه",
                [
                    "sampling_date",
                    "send_date",
                    "operation_date",
                    "date",
                    "created_at"
                ]
            ),

            (
                "gis_laboratory_results",
                "نتیجه آزمایشگاه",
                [
                    "result_date",
                    "answer_date",
                    "sampling_date",
                    "date",
                    "created_at"
                ]
            ),

            (
                "gis_slaughter_disposals",
                "کشتار/امحاء",
                [
                    "disposal_date",
                    "operation_date",
                    "date",
                    "created_at"
                ]
            ),

            (
                "gis_spraying",
                "سمپاشی",
                [
                    "spraying_date",
                    "operation_date",
                    "date",
                    "created_at"
                ]
            ),

            (
                "gis_vaccine_distributions",
                "توزیع واکسن",
                [
                    "distribution_date",
                    "operation_date",
                    "date",
                    "created_at"
                ]
            ),

            (
                "gis_vaccine_disposals",
                "دفع واکسن",
                [
                    "disposal_date",
                    "operation_date",
                    "date",
                    "created_at"
                ]
            )

        ]

        result = []

        for table, label, date_candidates in specs:

            if not self.has_table(table):
                continue

            unit_fk = self.pick(
                table,
                "epidemiology_unit_id"
            )

            if not unit_fk:
                continue

            d = self.pick(
                table,
                *date_candidates
            )

            if not d:
                continue

            columns = self.cols(table)

            select = [

                f"{self.ident(d)} AS event_date",

                f"'{label}' AS operation_type",

                "id AS source_id"

            ]

            # Disease relation
            disease_fk = self.pick(
                table,
                "disease_id"
            )

            if disease_fk:
                select.append(
                    f"{self.ident(disease_fk)} AS disease_id"
                )
            else:
                select.append(
                    "NULL AS disease_id"
                )

            # Sample relation
            sample_fk = self.pick(
                table,
                "sample_id",
                "send_sample_id",
                "sample_detail_id"
            )

            if sample_fk:
                select.append(
                    f"{self.ident(sample_fk)} AS sample_id"
                )
            else:
                select.append(
                    "NULL AS sample_id"
                )

            # Laboratory relation
            lab_fk = self.pick(
                table,
                "laboratory_result_id",
                "lab_result_id"
            )

            if lab_fk:
                select.append(
                    f"{self.ident(lab_fk)} AS laboratory_result_id"
                )
            else:
                select.append(
                    "NULL AS laboratory_result_id"
                )

            # Result status
            result_col = self.pick(
                table,
                "result_status",
                "status",
                "result",
                "result_value"
            )

            if result_col:
                select.append(
                    f"""
                    CAST(
                        {self.ident(result_col)}
                        AS TEXT
                    ) AS result_status
                    """
                )
            else:
                select.append(
                    "NULL AS result_status"
                )

            # Animal count
            animal_col = self.pick(
                table,
                "animal_count",
                "animals_count",
                "total_animals",
                "vaccinated_animals",
                "eligible_animals"
            )

            if animal_col:
                select.append(
                    f"""
                    {self.ident(animal_col)}
                    AS animal_count
                    """
                )
            else:
                select.append(
                    "NULL AS animal_count"
                )

            sql = f"""
                SELECT
                    {', '.join(select)}
                FROM {self.ident(table)}
                WHERE
                    {self.ident(unit_fk)}=:uid
                    AND
                    {self.ident(d)} IS NOT NULL
            """

            try:

                rows = self.rows(
                    sql,
                    {"uid": unit_id}
                )

                result.extend(rows)

            except Exception:
                # One malformed optional source table must not kill
                # the complete dashboard.
                continue

        result.sort(
            key=lambda x:
                str(x.get("event_date") or ""),
            reverse=True
        )

        return result[:2000]

    # ---------------------------------------------------------
    # Related operation chain
    # ---------------------------------------------------------

    def related_chain(
        self,
        unit_id: int,
        operation_id: int | None = None
    ):

        timeline = self.operation_timeline(
            unit_id
        )

        if operation_id is None:
            return timeline

        selected = None

        for event in timeline:

            if event.get("source_id") == operation_id:
                selected = event
                break

        if not selected:
            return []

        disease_id = selected.get(
            "disease_id"
        )

        sample_id = selected.get(
            "sample_id"
        )

        lab_id = selected.get(
            "laboratory_result_id"
        )

        chain = []

        for event in timeline:

            same_disease = (
                disease_id is not None
                and event.get("disease_id")
                == disease_id
            )

            same_sample = (
                sample_id is not None
                and event.get("sample_id")
                == sample_id
            )

            same_lab = (
                lab_id is not None
                and event.get("laboratory_result_id")
                == lab_id
            )

            if (
                event.get("source_id")
                == operation_id
                or same_disease
                or same_sample
                or same_lab
            ):
                chain.append(event)

        chain.sort(
            key=lambda x:
                str(x.get("event_date") or "")
        )

        return chain
'@


# ============================================================
# ROUTER
# ============================================================

$router = @'
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.gis.live_dashboard_kpi_service_v2 import (
    LiveDashboardKPIServiceV2,
)


router = APIRouter(
    prefix="/gis/dashboard/kpi-v2",
    tags=["GIS Live KPI Dashboard V2"],
)


@router.get("/overview")
def overview(
    db: Session = Depends(get_db),
):
    return LiveDashboardKPIServiceV2(db).overview()


@router.get("/provinces")
def provinces(
    metric: str = "all",
    db: Session = Depends(get_db),
):
    return {
        "metric": metric,
        "items":
            LiveDashboardKPIServiceV2(db)
            .provinces(metric)
    }


@router.get("/provinces/{province_id}/counties")
def counties(
    province_id: int,
    metric: str = "all",
    db: Session = Depends(get_db),
):
    return {
        "province_id": province_id,
        "metric": metric,
        "items":
            LiveDashboardKPIServiceV2(db)
            .counties(
                province_id,
                metric
            )
    }


@router.get("/counties/{county_id}/units")
def units(
    county_id: int,
    metric: str = "all",
    db: Session = Depends(get_db),
):
    return {
        "county_id": county_id,
        "metric": metric,
        "items":
            LiveDashboardKPIServiceV2(db)
            .units(
                county_id,
                metric
            )
    }


@router.get("/units/{unit_id}")
def unit_detail(
    unit_id: int,
    db: Session = Depends(get_db),
):
    return LiveDashboardKPIServiceV2(db).unit_detail(
        unit_id
    )


@router.get("/units/{unit_id}/chain")
def unit_chain(
    unit_id: int,
    operation_id: int | None = None,
    db: Session = Depends(get_db),
):
    return {
        "unit_id": unit_id,
        "operation_id": operation_id,
        "items":
            LiveDashboardKPIServiceV2(db)
            .related_chain(
                unit_id,
                operation_id
            )
    }
'@


# ============================================================
# FRONTEND CSS
# ============================================================

$css = @'
:root {
  --pv-bg: #04101b;
  --pv-panel: #071d2d;
  --pv-panel2: #0a2639;
  --pv-border: #14506b;
  --pv-cyan: #1bdcff;
  --pv-green: #39e598;
  --pv-yellow: #f5c84c;
  --pv-red: #ff5577;
  --pv-text: #eafaff;
  --pv-muted: #8eafbd;
}

.live-kpi-v2 {
  direction: rtl;
  min-height: 100vh;
  background:
    radial-gradient(
      circle at 50% 0%,
      #0a2b43 0%,
      #04131f 45%,
      #020910 100%
    );
  color: var(--pv-text);
  padding: 18px;
  font-family: Tahoma, Arial, sans-serif;
}

.kpi-v2-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 15px;
  margin-bottom: 16px;
}

.kpi-v2-header h1 {
  margin: 0;
  font-size: 25px;
}

.kpi-v2-header p {
  color: var(--pv-muted);
  font-size: 12px;
  margin: 7px 0 0;
}

.live-badge {
  border: 1px solid #1d9fbd;
  background: #06322d;
  color: #72ffd1;
  border-radius: 30px;
  padding: 8px 14px;
  font-size: 11px;
  white-space: nowrap;
}

.refresh-button {
  border: 1px solid var(--pv-border);
  background: #061a29;
  color: var(--pv-text);
  padding: 9px 14px;
  border-radius: 7px;
  cursor: pointer;
}

.refresh-button:hover {
  border-color: var(--pv-cyan);
}

.kpi-v2-grid {
  display: grid;
  grid-template-columns:
    repeat(6, minmax(145px, 1fr));
  gap: 10px;
  margin-bottom: 14px;
}

.kpi-v2-card {
  background:
    linear-gradient(
      180deg,
      rgba(10, 37, 57, .98),
      rgba(4, 19, 31, .98)
    );
  border: 1px solid rgba(22, 150, 190, .55);
  border-radius: 10px;
  padding: 14px;
  min-height: 100px;
  cursor: pointer;
  transition: .18s;
}

.kpi-v2-card:hover {
  transform: translateY(-2px);
  border-color: var(--pv-cyan);
  box-shadow:
    0 0 22px rgba(0, 200, 255, .14);
}

.kpi-v2-label {
  color: #9ebdca;
  font-size: 12px;
}

.kpi-v2-value {
  color: #a5efff;
  font-size: 25px;
  font-weight: 800;
  margin-top: 10px;
}

.kpi-v2-sub {
  color: var(--pv-green);
  font-size: 10px;
  margin-top: 6px;
}

.kpi-v2-layout {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 12px;
}

.kpi-v2-panel {
  background:
    linear-gradient(
      180deg,
      rgba(8, 30, 47, .97),
      rgba(4, 18, 29, .97)
    );
  border: 1px solid rgba(20, 120, 160, .55);
  border-radius: 10px;
  padding: 14px;
  margin-bottom: 12px;
}

.kpi-v2-panel h2 {
  margin: 0 0 12px;
  font-size: 15px;
}

.kpi-v2-chart {
  height: 270px;
}

.kpi-v2-chart.tall {
  height: 330px;
}

.kpi-v2-drill {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 7px;
  margin-bottom: 12px;
}

.kpi-v2-crumb {
  border: 1px solid #14516b;
  background: #061a28;
  color: #bce9f4;
  border-radius: 7px;
  padding: 7px 10px;
  cursor: pointer;
  font-size: 12px;
}

.kpi-v2-crumb.current {
  border-color: var(--pv-cyan);
  background: #0a3850;
}

.kpi-v2-arrow {
  color: #557d8d;
}

.kpi-v2-list {
  display: grid;
  grid-template-columns:
    repeat(3, minmax(180px, 1fr));
  gap: 9px;
}

.kpi-v2-location {
  background: #061b2a;
  border: 1px solid #12435a;
  border-radius: 8px;
  padding: 12px;
  cursor: pointer;
}

.kpi-v2-location:hover {
  border-color: var(--pv-cyan);
  background: #09283b;
}

.kpi-v2-location-title {
  font-size: 13px;
  font-weight: bold;
}

.kpi-v2-location-value {
  margin-top: 8px;
  color: #78eaff;
  font-size: 20px;
}

.kpi-v2-unit-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
}

.kpi-v2-timeline {
  position: relative;
  margin-top: 15px;
}

.timeline-row {
  display: grid;
  grid-template-columns:
    145px 155px 1fr;
  gap: 12px;
  border-bottom: 1px solid #14374a;
  padding: 12px 5px;
  cursor: pointer;
}

.timeline-row:hover {
  background: #082538;
}

.timeline-date {
  color: #7fdff2;
  font-size: 11px;
}

.timeline-type {
  font-weight: bold;
  color: #bfeefa;
  font-size: 12px;
}

.timeline-detail {
  color: #9dbbc6;
  font-size: 11px;
}

.timeline-chain {
  margin-top: 8px;
  background: #041521;
  border: 1px solid #18485d;
  border-radius: 8px;
  padding: 12px;
}

.chain-item {
  display: grid;
  grid-template-columns: 145px 150px 1fr;
  gap: 10px;
  padding: 8px;
  border-bottom: 1px solid #123344;
}

.kpi-v2-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 11px;
}

.kpi-v2-table th,
.kpi-v2-table td {
  padding: 9px;
  border-bottom: 1px solid #153b50;
  text-align: right;
}

.kpi-v2-table th {
  color: #85d3e5;
}

.empty-state {
  padding: 35px;
  text-align: center;
  color: #6e8e9b;
}

@media (max-width: 1200px) {
  .kpi-v2-grid {
    grid-template-columns:
      repeat(4, minmax(145px, 1fr));
  }

  .kpi-v2-layout {
    grid-template-columns: 1fr;
  }

  .kpi-v2-list {
    grid-template-columns:
      repeat(2, minmax(180px, 1fr));
  }
}

@media (max-width: 750px) {
  .kpi-v2-grid {
    grid-template-columns:
      repeat(2, minmax(135px, 1fr));
  }

  .kpi-v2-list {
    grid-template-columns: 1fr;
  }

  .timeline-row,
  .chain-item {
    grid-template-columns: 1fr;
    gap: 4px;
  }
}
'@


# ============================================================
# FRONTEND TSX
# ============================================================

$tsx = @'
import React, {
  useEffect,
  useMemo,
  useState
} from "react";

import "./LiveKpiDashboardV2.css";


const API = "/api/v1/gis/dashboard/kpi-v2";


type AnyObj = Record<string, any>;


const nf = new Intl.NumberFormat(
  "fa-IR",
  {
    maximumFractionDigits: 1
  }
);


function number(value: any) {

  return nf.format(
    Number(value || 0)
  );

}


function percent(value: any) {

  return `${nf.format(
    Number(value || 0)
  )}%`;

}


async function getJson(
  path: string
) {

  const response = await fetch(
    `${API}${path}`,
    {
      credentials: "include"
    }
  );

  if (!response.ok) {

    throw new Error(
      `${response.status}: ${await response.text()}`
    );

  }

  return response.json();

}


function Card(
  {
    label,
    value,
    sub,
    onClick
  }: {
    label: string;
    value: any;
    sub?: string;
    onClick?: () => void;
  }
) {

  return (

    <div
      className="kpi-v2-card"
      onClick={onClick}
    >

      <div className="kpi-v2-label">
        {label}
      </div>

      <div className="kpi-v2-value">
        {value}
      </div>

      {sub && (

        <div className="kpi-v2-sub">
          {sub}
        </div>

      )}

    </div>

  );

}


function LineChart(
  {
    data
  }: {
    data: AnyObj[];
  }
) {

  if (!data?.length) {

    return (
      <div className="empty-state">
        داده‌ای برای نمودار وجود ندارد
      </div>
    );

  }

  const width = 800;
  const height = 260;
  const padding = 40;

  const values =
    data.map(
      x => Number(x.value || 0)
    );

  const max =
    Math.max(
      ...values,
      1
    );

  const points =
    data.map(
      (x, i) => {

        const px =
          padding +
          (
            i *
            (
              (width - padding * 2) /
              Math.max(
                data.length - 1,
                1
              )
            )
          );

        const py =
          height -
          padding -
          (
            Number(x.value || 0) /
            max
          ) *
          (
            height -
            padding * 2
          );

        return {
          x: px,
          y: py,
          value: x.value,
          period: x.period
        };

      }
    );

  const polyline =
    points
      .map(
        p => `${p.x},${p.y}`
      )
      .join(" ");

  return (

    <svg
      viewBox={`0 0 ${width} ${height}`}
      width="100%"
      height="100%"
    >

      <line
        x1={padding}
        y1={height - padding}
        x2={width - padding}
        y2={height - padding}
        stroke="#183c50"
      />

      <polyline
        points={polyline}
        fill="none"
        stroke="#1bdcff"
        strokeWidth="4"
      />

      {points.map(
        (p, i) => (

          <g key={i}>

            <circle
              cx={p.x}
              cy={p.y}
              r="5"
              fill="#1bdcff"
            />

            <text
              x={p.x}
              y={height - 10}
              fill="#789aaa"
              fontSize="10"
              textAnchor="middle"
            >
              {String(
                p.period || ""
              ).slice(5)}
            </text>

          </g>

        )
      )}

    </svg>

  );

}


function BarChart(
  {
    data,
    onClick
  }: {
    data: AnyObj[];
    onClick?: (item: AnyObj) => void;
  }
) {

  if (!data?.length) {

    return (
      <div className="empty-state">
        داده‌ای برای نمودار وجود ندارد
      </div>
    );

  }

  const max =
    Math.max(
      ...data.map(
        x => Number(x.value || 0)
      ),
      1
    );

  return (

    <div
      style={{
        display: "flex",
        alignItems: "end",
        gap: 9,
        height: 250,
        padding: "10px 5px"
      }}
    >

      {data.slice(0, 15).map(
        (item, index) => {

          const value =
            Number(
              item.value || 0
            );

          const height =
            Math.max(
              5,
              value / max * 185
            );

          return (

            <div
              key={index}
              style={{
                flex: 1,
                minWidth: 30,
                cursor:
                  onClick
                    ? "pointer"
                    : "default",
                textAlign: "center"
              }}
              onClick={() =>
                onClick?.(item)
              }
            >

              <div
                title={number(value)}
                style={{
                  height,
                  borderRadius:
                    "5px 5px 0 0",
                  background:
                    "linear-gradient(180deg,#1bdcff,#07506b)"
                }}
              />

              <div
                style={{
                  color: "#8caebe",
                  fontSize: 9,
                  marginTop: 5,
                  overflow: "hidden"
                }}
              >
                {String(
                  item.name ||
                  item.period ||
                  ""
                ).slice(0, 13)}
              </div>

            </div>

          );

        }
      )}

    </div>

  );

}


function Breadcrumb(
  {
    level,
    province,
    county,
    unit,
    onRoot,
    onProvince,
    onCounty
  }: AnyObj
) {

  return (

    <div className="kpi-v2-drill">

      <button
        className={
          `kpi-v2-crumb ${
            level === "root"
              ? "current"
              : ""
          }`
        }
        onClick={onRoot}
      >
        کل کشور
      </button>

      {province && (

        <>

          <span className="kpi-v2-arrow">
            ←
          </span>

          <button
            className={
              `kpi-v2-crumb ${
                level === "province"
                  ? "current"
                  : ""
              }`
            }
            onClick={onProvince}
          >
            {province.name}
          </button>

        </>

      )}

      {county && (

        <>

          <span className="kpi-v2-arrow">
            ←
          </span>

          <button
            className={
              `kpi-v2-crumb ${
                level === "county"
                  ? "current"
                  : ""
              }`
            }
            onClick={onCounty}
          >
            {county.name}
          </button>

        </>

      )}

      {unit && (

        <>

          <span className="kpi-v2-arrow">
            ←
          </span>

          <button
            className="kpi-v2-crumb current"
          >
            {unit.name}
          </button>

        </>

      )}

    </div>

  );

}


function UnitTimeline(
  {
    operations,
    unitId
  }: {
    operations: AnyObj[];
    unitId: number;
  }
) {

  const [
    selected,
    setSelected
  ] = useState<AnyObj | null>(
    null
  );

  const [
    chain,
    setChain
  ] = useState<AnyObj[]>([]);

  async function openOperation(
    operation: AnyObj
  ) {

    setSelected(operation);

    try {

      const result =
        await getJson(
          `/units/${unitId}/chain?operation_id=${operation.source_id}`
        );

      setChain(
        result.items || []
      );

    } catch {

      setChain([]);

    }

  }

  return (

    <div className="kpi-v2-panel">

      <h2>
        تاریخچه و زنجیره تمام عملیات مرتبط واحد
      </h2>

      <p
        style={{
          color: "#789",
          fontSize: 11
        }}
      >
        هر ردیف قابل کلیک است و در صورت وجود
        FK مشترک، زنجیره مرتبط همان عملیات را
        نمایش می‌دهد.
      </p>

      <div className="kpi-v2-timeline">

        {operations.length === 0 && (

          <div className="empty-state">
            برای این واحد هنوز عملیات قابل نمایش
            در جداول منبع پیدا نشد.
          </div>

        )}

        {operations.map(
          (operation, index) => (

            <React.Fragment
              key={`${operation.source_id}-${index}`}
            >

              <div
                className="timeline-row"
                onClick={() =>
                  openOperation(operation)
                }
              >

                <div className="timeline-date">
                  {String(
                    operation.event_date || ""
                  ).slice(0, 19)}
                </div>

                <div className="timeline-type">
                  {operation.operation_type}
                </div>

                <div className="timeline-detail">

                  {operation.disease_id && (
                    <span>
                      بیماری: {operation.disease_id}
                      {" | "}
                    </span>
                  )}

                  {operation.sample_id && (
                    <span>
                      نمونه: {operation.sample_id}
                      {" | "}
                    </span>
                  )}

                  {operation.laboratory_result_id && (
                    <span>
                      آزمایشگاه:
                      {" "}
                      {operation.laboratory_result_id}
                      {" | "}
                    </span>
                  )}

                  {operation.result_status && (
                    <span>
                      نتیجه:
                      {" "}
                      {operation.result_status}
                    </span>
                  )}

                </div>

              </div>

              {selected?.source_id ===
                operation.source_id && (

                <div className="timeline-chain">

                  <strong>
                    زنجیره مرتبط عملیات
                  </strong>

                  {chain.length === 0 && (

                    <div
                      style={{
                        color: "#789",
                        marginTop: 8
                      }}
                    >
                      رابطه FK مشترک برای این عملیات
                      پیدا نشد یا رکورد مرتبط وجود ندارد.
                    </div>

                  )}

                  {chain.map(
                    (item, i) => (

                      <div
                        className="chain-item"
                        key={i}
                      >

                        <div>
                          {String(
                            item.event_date || ""
                          ).slice(0, 19)}
                        </div>

                        <div>
                          {item.operation_type}
                        </div>

                        <div>
                          {item.disease_id
                            ? `بیماری: ${item.disease_id}`
                            : ""}
                          {" "}
                          {item.sample_id
                            ? `نمونه: ${item.sample_id}`
                            : ""}
                          {" "}
                          {item.laboratory_result_id
                            ? `آزمایشگاه: ${item.laboratory_result_id}`
                            : ""}
                          {" "}
                          {item.result_status
                            ? `نتیجه: ${item.result_status}`
                            : ""}
                        </div>

                      </div>

                    )
                  )}

                </div>

              )}

            </React.Fragment>

          )
        )}

      </div>

    </div>

  );

}


export default function LiveKpiDashboardV2() {

  const [
    data,
    setData
  ] = useState<AnyObj | null>(
    null
  );

  const [
    metric,
    setMetric
  ] = useState("all");

  const [
    level,
    setLevel
  ] = useState<
    "root" |
    "province" |
    "county" |
    "unit"
  >("root");

  const [
    province,
    setProvince
  ] = useState<AnyObj | null>(
    null
  );

  const [
    county,
    setCounty
  ] = useState<AnyObj | null>(
    null
  );

  const [
    unit,
    setUnit
  ] = useState<AnyObj | null>(
    null
  );

  const [
    locations,
    setLocations
  ] = useState<AnyObj[]>([]);

  const [
    unitDetail,
    setUnitDetail
  ] = useState<AnyObj | null>(
    null
  );

  const [
    loading,
    setLoading
  ] = useState(true);

  const [
    error,
    setError
  ] = useState("");

  const [
    refresh,
    setRefresh
  ] = useState(0);


  useEffect(
    () => {

      setLoading(true);
      setError("");

      getJson("/overview")
        .then(setData)
        .catch(
          e => setError(
            String(e)
          )
        )
        .finally(
          () => setLoading(false)
        );

    },
    [refresh]
  );


  useEffect(
    () => {

      if (level === "root") {

        setLocations([]);

        return;

      }

      setLoading(true);

      let request = "";

      if (level === "province") {

        request =
          `/provinces?metric=${metric}`;

      }

      if (
        level === "county" &&
        province
      ) {

        request =
          `/provinces/${province.id}/counties?metric=${metric}`;

      }

      if (
        level === "unit" &&
        county
      ) {

        request =
          `/counties/${county.id}/units?metric=${metric}`;

      }

      if (!request) {

        setLoading(false);
        return;

      }

      getJson(request)
        .then(
          result =>
            setLocations(
              result.items || []
            )
        )
        .catch(
          e =>
            setError(
              String(e)
            )
        )
        .finally(
          () =>
            setLoading(false)
        );

    },
    [
      level,
      province,
      county,
      metric
    ]
  );


  useEffect(
    () => {

      if (!unit) {

        setUnitDetail(null);
        return;

      }

      setLoading(true);

      getJson(
        `/units/${unit.id}`
      )
        .then(
          setUnitDetail
        )
        .catch(
          e =>
            setError(
              String(e)
            )
        )
        .finally(
          () =>
            setLoading(false)
        );

    },
    [unit]
  );


  const cards =
    data?.cards || {};

  const charts =
    data?.charts || {};


  function drillMetric(
    selectedMetric: string
  ) {

    setMetric(
      selectedMetric
    );

    setProvince(null);
    setCounty(null);
    setUnit(null);
    setUnitDetail(null);

    setLevel(
      "province"
    );

  }


  function root() {

    setMetric("all");

    setProvince(null);
    setCounty(null);
    setUnit(null);
    setUnitDetail(null);

    setLevel("root");

  }


  function openProvince(
    item: AnyObj
  ) {

    setProvince(item);
    setCounty(null);
    setUnit(null);
    setUnitDetail(null);

    setLevel("county");

  }


  function openCounty(
    item: AnyObj
  ) {

    setCounty(item);
    setUnit(null);
    setUnitDetail(null);

    setLevel("unit");

  }


  function openUnit(
    item: AnyObj
  ) {

    setUnit(item);

    setLevel("unit");

  }


  if (
    loading &&
    !data
  ) {

    return (
      <div className="live-kpi-v2">
        در حال دریافت KPIهای زنده از PostgreSQL...
      </div>
    );

  }


  if (
    error &&
    !data
  ) {

    return (
      <div className="live-kpi-v2">

        <div className="kpi-v2-panel">

          <b>خطا:</b>

          {" "}

          {error}

        </div>

      </div>
    );

  }


  return (

    <div className="live-kpi-v2">

      <div className="kpi-v2-header">

        <div>

          <h1>
            داشبورد زنده کنترل بیماری و عملیات دامپزشکی
          </h1>

          <p>
            تمام KPIها و نمودارها در یک صفحه —
            کلیک روی هر KPI شما را تا استان،
            شهرستان و واحد هدایت می‌کند.
          </p>

        </div>

        <div
          style={{
            display: "flex",
            gap: 8,
            alignItems: "center"
          }}
        >

          <span className="live-badge">
            ● LIVE PostgreSQL
          </span>

          <button
            className="refresh-button"
            onClick={() =>
              setRefresh(
                x => x + 1
              )
            }
          >
            ↻ بروزرسانی
          </button>

        </div>

      </div>


      {level !== "root" && (

        <Breadcrumb

          level={level}

          province={province}

          county={county}

          unit={unit}

          onRoot={root}

          onProvince={() => {

            setCounty(null);
            setUnit(null);
            setUnitDetail(null);

            setLevel("county");

          }}

          onCounty={() => {

            setUnit(null);
            setUnitDetail(null);

            setLevel("unit");

          }}

        />

      )}


      {level === "root" && (

        <>

          <div className="kpi-v2-grid">

            <Card
              label="واحدهای اپیدمیولوژیک"
              value={number(
                cards.total_units
              )}
              onClick={() =>
                drillMetric("units")
              }
            />

            <Card
              label="واحدهای فعال"
              value={number(
                cards.active_units
              )}
              onClick={() =>
                drillMetric("units")
              }
            />

            <Card
              label="گزارش بیماری"
              value={number(
                cards.disease_reports
              )}
              onClick={() =>
                drillMetric("disease")
              }
            />

            <Card
              label="وقوع بیماری"
              value={number(
                cards.disease_occurrences
              )}
              onClick={() =>
                drillMetric("disease")
              }
            />

            <Card
              label="مراقبت فعال"
              value={number(
                cards.care_records
              )}
              onClick={() =>
                drillMetric("care")
              }
            />

            <Card
              label="واکسیناسیون انجام‌شده"
              value={number(
                cards.vaccinated
              )}
              sub={
                "کلیک برای Drill-down"
              }
              onClick={() =>
                drillMetric("vaccination")
              }
            />

            <Card
              label="دام واجد شرایط"
              value={number(
                cards.eligible
              )}
              onClick={() =>
                drillMetric("vaccination")
              }
            />

            <Card
              label="پوشش واکسیناسیون"
              value={percent(
                cards.vaccination_coverage
              )}
              onClick={() =>
                drillMetric("vaccination")
              }
            />

            <Card
              label="باقی‌مانده واکسیناسیون"
              value={number(
                cards.vaccination_remaining
              )}
              onClick={() =>
                drillMetric("vaccination")
              }
            />

            <Card
              label="نتایج آزمایشگاهی"
              value={number(
                cards.lab_results
              )}
              onClick={() =>
                drillMetric("lab")
              }
            />

            <Card
              label="مثبت آزمایشگاه"
              value={number(
                cards.lab_positive
              )}
              onClick={() =>
                drillMetric("lab")
              }
            />

            <Card
              label="نرخ مثبت آزمایشگاه"
              value={percent(
                cards.lab_positive_rate
              )}
              onClick={() =>
                drillMetric("lab")
              }
            />

            <Card
              label="نمونه‌ها"
              value={number(
                cards.sample_records
              )}
              onClick={() =>
                drillMetric("samples")
              }
            />

            <Card
              label="موجودی واکسن"
              value={number(
                cards.inventory
              )}
            />

            <Card
              label="توزیع واکسن"
              value={number(
                cards.distributed
              )}
            />

            <Card
              label="دفع واکسن"
              value={number(
                cards.disposed
              )}
            />

          </div>


          <div className="kpi-v2-layout">

            <div>

              <div className="kpi-v2-panel">

                <h2>
                  روند واکسیناسیون
                </h2>

                <div className="kpi-v2-chart">

                  <LineChart
                    data={
                      charts.vaccination || []
                    }
                  />

                </div>

              </div>


              <div className="kpi-v2-panel">

                <h2>
                  روند گزارش بیماری
                </h2>

                <div className="kpi-v2-chart">

                  <LineChart
                    data={
                      charts.disease || []
                    }
                  />

                </div>

              </div>

            </div>


            <div>

              <div className="kpi-v2-panel">

                <h2>
                  روند مراقبت
                </h2>

                <div className="kpi-v2-chart">

                  <LineChart
                    data={
                      charts.care || []
                    }
                  />

                </div>

              </div>


              <div className="kpi-v2-panel">

                <h2>
                  روند آزمایشگاه
                </h2>

                <div className="kpi-v2-chart">

                  <LineChart
                    data={
                      charts.laboratory || []
                    }
                  />

                </div>

              </div>

            </div>

          </div>

        </>

      )}


      {level !== "root" &&
       level !== "unit" && (

        <div className="kpi-v2-panel">

          <h2>

            {level === "province"
              ? `استان‌ها — شاخص: ${metric}`
              : `شهرستان‌ها — شاخص: ${metric}`
            }

          </h2>

          {loading ? (

            <div className="empty-state">
              در حال دریافت اطلاعات...
            </div>

          ) : (

            <div className="kpi-v2-list">

              {locations.map(
                item => (

                  <div
                    className="kpi-v2-location"
                    key={item.id}
                    onClick={() => {

                      if (
                        level ===
                        "province"
                      ) {

                        openProvince(
                          item
                        );

                      } else {

                        openCounty(
                          item
                        );

                      }

                    }}
                  >

                    <div className="kpi-v2-location-title">
                      {item.name}
                    </div>

                    <div className="kpi-v2-location-value">
                      {number(
                        item.value
                      )}
                    </div>

                  </div>

                )
              )}

            </div>

          )}

        </div>

      )}


      {level === "unit" &&
       !unit && (

        <div className="kpi-v2-panel">

          <h2>
            واحدهای اپیدمیولوژیک
          </h2>

          {loading ? (

            <div className="empty-state">
              در حال دریافت واحدها...
            </div>

          ) : (

            <div className="kpi-v2-list">

              {locations.map(
                item => (

                  <div
                    className="kpi-v2-location"
                    key={item.id}
                    onClick={() =>
                      openUnit(item)
                    }
                  >

                    <div className="kpi-v2-location-title">
                      {item.name}
                    </div>

                    <div className="kpi-v2-location-value">
                      {number(
                        item.value
                      )}
                    </div>

                    <div
                      style={{
                        color: "#789",
                        fontSize: 10,
                        marginTop: 5
                      }}
                    >
                      مشاهده جزئیات کامل واحد →
                    </div>

                  </div>

                )
              )}

            </div>

          )}

        </div>

      )}


      {unit &&
       unitDetail && (

        <>

          <div className="kpi-v2-panel">

            <div className="kpi-v2-unit-header">

              <div>

                <h2>
                  واحد:
                  {" "}
                  {unit.name}
                </h2>

                <div
                  style={{
                    color: "#789",
                    fontSize: 11
                  }}
                >
                  جزئیات کامل عملیات واقعی
                  ثبت‌شده برای این واحد
                </div>

              </div>

            </div>

          </div>


          <div className="kpi-v2-grid">

            <Card
              label="تمام عملیات"
              value={number(
                unitDetail.cards?.all
              )}
            />

            <Card
              label="بیماری"
              value={number(
                unitDetail.cards?.disease
              )}
            />

            <Card
              label="مراقبت"
              value={number(
                unitDetail.cards?.care
              )}
            />

            <Card
              label="واکسیناسیون"
              value={number(
                unitDetail.cards?.vaccination
              )}
            />

            <Card
              label="آزمایشگاه"
              value={number(
                unitDetail.cards?.lab
              )}
            />

            <Card
              label="نمونه"
              value={number(
                unitDetail.cards?.samples
              )}
            />

            <Card
              label="سمپاشی"
              value={number(
                unitDetail.cards?.spraying
              )}
            />

            <Card
              label="امحاء"
              value={number(
                unitDetail.cards?.slaughter
              )}
            />

          </div>


          <UnitTimeline
            operations={
              unitDetail.operations || []
            }
            unitId={
              Number(unit.id)
            }
          />

        </>

      )}

    </div>

  );

}
'@


# ============================================================
# WRITE FILES
# ============================================================

Write-Utf8 $ServiceFile $service
Write-Utf8 $RouterFile $router
Write-Utf8 $PageFile $tsx
Write-Utf8 $CssFile $css


# ============================================================
# BACKEND ROUTER REGISTRATION
# ============================================================

$apiCandidates = @(
    (Join-Path $BackendRoot "app\api\v1\api.py"),
    (Join-Path $BackendRoot "app\api\v1\router.py"),
    (Join-Path $BackendRoot "app\api\v1\__init__.py")
)

$apiTarget =
    $apiCandidates |
    Where-Object {
        Test-Path $_
    } |
    Select-Object -First 1


if ($apiTarget) {

    Backup-IfExists $apiTarget

    $apiText =
        Get-Content
        $apiTarget
        -Raw
        -Encoding UTF8

    $importLine =
        "from app.api.v1.endpoints.gis_dashboard_kpi_v2 import router as gis_dashboard_kpi_v2_router"

    $includeLine =
        "api_router.include_router(gis_dashboard_kpi_v2_router)"


    if (
        $apiText -notmatch
        "gis_dashboard_kpi_v2_router"
    ) {

        if (
            $apiText -notmatch
            [regex]::Escape(
                $importLine
            )
        ) {

            $matches =
                [regex]::Matches(
                    $apiText,
                    '(?m)^import .+;$'
                )

            if ($matches.Count -gt 0) {

                $last =
                    $matches[$matches.Count - 1]

                $insertAt =
                    $last.Index +
                    $last.Length

                $apiText =
                    $apiText.Insert(
                        $insertAt,
                        "`r`n$importLine"
                    )

            } else {

                $apiText =
                    "$importLine`r`n$apiText"

            }

        }


        if (
            $apiText -match
            "api_router\.include_router"
        ) {

            $apiText =
                $apiText.TrimEnd() +
                "`r`n$includeLine`r`n"

        }
        elseif (
            $apiText -match
            "router\.include_router"
        ) {

            $apiText =
                $apiText.TrimEnd() +
                "`r`n$includeLine`r`n"

        }
        else {

            Write-Host `
                "WARNING: Could not confidently find API include point." `
                -ForegroundColor Yellow

            Write-Host `
                "Router file created but not automatically included." `
                -ForegroundColor Yellow

        }


        Write-Utf8 `
            $apiTarget `
            $apiText

    }
    else {

        Write-Host `
            "V2 router already registered." `
            -ForegroundColor Yellow

    }

}
else {

    Write-Host `
        "WARNING: API router file not detected." `
        -ForegroundColor Yellow

}


# ============================================================
# FRONTEND ROUTE REGISTRATION
# ============================================================

$appCandidates =
    Get-ChildItem `
        (Join-Path $FrontendRoot "src") `
        -Recurse `
        -File `
        -Include *.tsx,*.jsx `
        -ErrorAction SilentlyContinue |
    Select-String `
        -Pattern "<Routes|createBrowserRouter|createHashRouter" `
        -List |
    Select-Object `
        -ExpandProperty Path


$appTarget =
    $appCandidates |
    Where-Object {
        $_ -match "\\App\.(tsx|jsx)$"
    } |
    Select-Object -First 1


if (-not $appTarget) {

    $appTarget =
        $appCandidates |
        Select-Object -First 1

}


if ($appTarget) {

    Backup-IfExists $appTarget

    $appText =
        Get-Content
        $appTarget
        -Raw
        -Encoding UTF8


    if (
        $appText -notmatch
        "LiveKpiDashboardV2"
    ) {

        $import =
            'import LiveKpiDashboardV2 from "./pages/LiveKpiDashboardV2";'


        if (
            $appText -notmatch
            [regex]::Escape($import)
        ) {

            $matches =
                [regex]::Matches(
                    $appText,
                    '(?m)^import .+;$'
                )

            if ($matches.Count -gt 0) {

                $last =
                    $matches[$matches.Count - 1]

                $insertAt =
                    $last.Index +
                    $last.Length

                $appText =
                    $appText.Insert(
                        $insertAt,
                        "`r`n$import"
                    )

            }
            else {

                $appText =
                    "$import`r`n$appText"

            }

        }


        if (
            $appText -match
            "<Routes"
        ) {

            $route =
                '<Route path="/live-kpi-v2" element={<LiveKpiDashboardV2 />} />'

            $pos =
                $appText.IndexOf(
                    "</Routes>"
                )

            if ($pos -ge 0) {

                $appText =
                    $appText.Insert(
                        $pos,
                        "    $route`r`n"
                    )

            }
            else {

                Write-Host `
                    "WARNING: </Routes> not found." `
                    -ForegroundColor Yellow

            }

        }


        Write-Utf8 `
            $appTarget `
            $appText

    }
    else {

        Write-Host `
            "V2 frontend already registered." `
            -ForegroundColor Yellow

    }

}
else {

    Write-Host `
        "WARNING: React router file not automatically detected." `
        -ForegroundColor Yellow

}


# ============================================================
# VALIDATION
# ============================================================

Push-Location $BackendRoot

try {

    Write-Host ""
    Write-Host "============================================================" `
        -ForegroundColor Cyan

    Write-Host "PYTHON COMPILE CHECK" `
        -ForegroundColor Cyan

    Write-Host "============================================================" `
        -ForegroundColor Cyan


    py -3.12 -m py_compile `
        $ServiceFile `
        $RouterFile


    Write-Host `
        "Python compile: OK" `
        -ForegroundColor Green


    Write-Host ""
    Write-Host "FASTAPI IMPORT CHECK" `
        -ForegroundColor Cyan


    py -3.12 -c `
        "from app.api.v1.endpoints.gis_dashboard_kpi_v2 import router; print('router import OK:', router.prefix)"


    Write-Host `
        "FastAPI router import: OK" `
        -ForegroundColor Green

}
finally {

    Pop-Location

}


# ============================================================
# FRONTEND BUILD
# ============================================================

Push-Location $FrontendRoot

try {

    Write-Host ""
    Write-Host "============================================================" `
        -ForegroundColor Cyan

    Write-Host "FRONTEND BUILD" `
        -ForegroundColor Cyan

    Write-Host "============================================================" `
        -ForegroundColor Cyan


    if (
        Test-Path "package.json"
    ) {

        npm run build

        Write-Host `
            "Frontend build: OK" `
            -ForegroundColor Green

    }
    else {

        Write-Host `
            "package.json not found." `
            -ForegroundColor Yellow

    }

}
finally {

    Pop-Location

}


# ============================================================
# FINISH
# ============================================================

Write-Host ""
Write-Host "============================================================" `
    -ForegroundColor Cyan

Write-Host "PVIMP LIVE KPI DASHBOARD V2 FINISHED" `
    -ForegroundColor Cyan

Write-Host "============================================================" `
    -ForegroundColor Cyan

Write-Host ""

Write-Host "Backup:"
Write-Host $BackupRoot

Write-Host ""

Write-Host "Backend service:"
Write-Host $ServiceFile

Write-Host ""

Write-Host "Backend router:"
Write-Host $RouterFile

Write-Host ""

Write-Host "Frontend page:"
Write-Host $PageFile

Write-Host ""

Write-Host "Frontend CSS:"
Write-Host $CssFile

Write-Host ""

Write-Host "API:"
Write-Host "  /api/v1/gis/dashboard/kpi-v2/overview"
Write-Host "  /api/v1/gis/dashboard/kpi-v2/provinces"
Write-Host "  /api/v1/gis/dashboard/kpi-v2/provinces/{province_id}/counties"
Write-Host "  /api/v1/gis/dashboard/kpi-v2/counties/{county_id}/units"
Write-Host "  /api/v1/gis/dashboard/kpi-v2/units/{unit_id}"
Write-Host "  /api/v1/gis/dashboard/kpi-v2/units/{unit_id}/chain"

Write-Host ""

Write-Host "Frontend:"
Write-Host "  /live-kpi-v2"

Write-Host ""

Write-Host "IMPORTANT:"
Write-Host "Restart Uvicorn after successful build."

Write-Host ""
Write-Host "============================================================" `
    -ForegroundColor Cyan